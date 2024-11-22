from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, jsonify, flash
import sqlite3
from os import path
import hashlib

rgz = Blueprint('rgz', __name__)

# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        # Подключение к базе данных
        conn = sqlite3.connect(r'C:\Users\PC\Desktop\Документы\ВУЗ\3 курс\Web-программирование\База данных\rgz_db') 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "rgz_bd.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@rgz.route('/rgz/')
def lab():
    username = session.get('login', 'Анонимус')  # Получаем имя пользователя из сессии или устанавливаем "Анонимус"
    return render_template('rgz/rgz.html', username=username)

@rgz.route('/rgz/json-rpc-api', methods=['POST'])
def api():
    data = request.json
    id = data['id']
   
    if data['method'] == 'register':
        login = data['params']['login']
        password = data['params']['password']
        hashed_password = hash_password(password)

        conn, cur = db_connect()
        cur.execute("SELECT * FROM admin")
        user = cur.fetchone()

        if user:
            db_close(conn, cur)
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Администратор уже зарегистрирован'
                },
                'id': id
            })

        cur.execute("INSERT INTO admin (login, password) VALUES (?, ?)", (login, hashed_password))
        db_close(conn, cur)
        return jsonify({
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        })
    
    if data['method'] == 'login':
        login = data['params']['login']
        password = data['params']['password']
        hashed_password = hash_password(password)

        conn, cur = db_connect()
        cur.execute("SELECT * FROM admin WHERE login = ? AND password = ?", (login, hashed_password))
        user = cur.fetchone()
        db_close(conn, cur)

        if user:
            session['login'] = login
            return jsonify({
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            })
        else:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Неверный логин или пароль'
                },
                'id': id
            })
    
    if data['method'] == 'logout':
        session.pop('login', None)
        return jsonify({
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        })
    
    if data['method'] == 'get_books':
        title = data['params'].get('title', '')
        author = data['params'].get('author', '')
        min_pages = data['params'].get('min_pages', '')
        max_pages = data['params'].get('max_pages', '')
        publisher = data['params'].get('publisher', '')
        sort_by = data['params'].get('sort_by', 'title')
        page = int(data['params'].get('page', 1))

        conn, cur = db_connect()

        # Формируем SQL-запрос для получения списка книг
        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")
        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")
        if min_pages:
            query += " AND amount_of_pages >= ?"
            params.append(min_pages)
        if max_pages:
            query += " AND amount_of_pages <= ?"
            params.append(max_pages)
        if publisher:
            query += " AND publisher LIKE ?"
            params.append(f"%{publisher}%")

        query += f" ORDER BY {sort_by}"
        query += " LIMIT 20 OFFSET ?"
        params.append((page - 1) * 20)

        print(f"SQL Query: {query}")  # Отладочное сообщение
        print(f"SQL Params: {params}")  # Отладочное сообщение

        try:
            cur.execute(query, params)
            books = cur.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Database error'
                },
                'id': id
            })

        # Формируем SQL-запрос для подсчета общего количества книг
        count_query = "SELECT COUNT(*) FROM books WHERE 1=1"
        count_params = []

        if title:
            count_query += " AND title LIKE ?"
            count_params.append(f"%{title}%")
        if author:
            count_query += " AND author LIKE ?"
            count_params.append(f"%{author}%")
        if min_pages:
            count_query += " AND amount_of_pages >= ?"
            count_params.append(min_pages)
        if max_pages:
            count_query += " AND amount_of_pages <= ?"
            count_params.append(max_pages)
        if publisher:
            count_query += " AND publisher LIKE ?"
            count_params.append(f"%{publisher}%")

        cur.execute(count_query, count_params)
        total_books = cur.fetchone()[0]
        total_pages = (total_books + 19) // 20

        db_close(conn, cur)

        print(f"Books: {books}")  # Отладочное сообщение

        return jsonify({
            'jsonrpc': '2.0',
            'result': {
                'books': [dict(book) for book in books],
                'total_pages': total_pages
            },
            'id': id
        })
    
    if data['method'] == 'add_book':
        login = session.get('login')
        if not login:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            })

        title = data['params']['title']
        author = data['params']['author']
        year_of_publication = data['params']['year_of_publication']
        amount_of_pages = data['params']['amount_of_pages']
        publisher = data['params']['publisher']
        book_cover = data['params'].get('book_cover', '')

        conn, cur = db_connect()
        try:
            cur.execute("INSERT INTO books (title, author, year_of_publication, amount_of_pages, publisher, book_cover) VALUES (?, ?, ?, ?, ?, ?)",
                        (title, author, year_of_publication, amount_of_pages, publisher, book_cover))
            db_close(conn, cur)
            return jsonify({
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            })
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Database error'
                },
                'id': id
            })
    
    if data['method'] == 'get_book':
        book_id = data['params']['id']
        conn, cur = db_connect()
        try:
            cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            book = cur.fetchone()
            db_close(conn, cur)
            if book:
                return jsonify({
                    'jsonrpc': '2.0',
                    'result': {
                        'book': dict(book)
                    },
                    'id': id
                })
            else:
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 6,
                        'message': 'Книга не найдена'
                    },
                    'id': id
                })
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Database error'
                },
                'id': id
            })
    
    if data['method'] == 'delete_book':
        login = session.get('login')
        if not login:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            })

        book_id = data['params']['id']
        conn, cur = db_connect()
        try:
            cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
            db_close(conn, cur)
            return jsonify({
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            })
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Database error'
                },
                'id': id
            })
    
    login = session.get('login')
    if not login:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        })
        
    return jsonify({
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    })