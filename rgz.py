from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, jsonify
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
import requests
import json


# 7 Вариант

rgz = Blueprint('rgz', __name__)

# Подключенеи к БД

@rgz.route('/rgz/')
def main():
    return render_template('rgz/main.html', login = session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        # Подключение к базе данных
        conn = sqlite3.connect(r'C:\Users\PC\Desktop\Документы\ВУЗ\3 курс\Web-программирование\База данных\rgz_db') 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn,cur):
    conn.commit()
    cur.close()
    conn.close()




# @rgz.route('/rgz/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('rgz/login.html')
    
#     login = request.form.get('login')
#     password = request.form.get('password')

#     if not (login and password):
#         return render_template('rgz/login.html', error='Заполните поля')

#     # Подключение к базе данных
#     conn, cur = db_connect()

#     # Выполнение SQL-запроса с параметризованным запросом
#     # if current_app.config['DB_TYPE'] == 'postgres':
#     #     cur.execute("SELECT * FROM admin WHERE login=%s;", (login,))
#     # else:
#     #     cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
#     cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
#     user = cur.fetchone()  # Получаем одну строку

#     if not user:  
#         db_close(conn, cur)
#         return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
#     # Проверка пароля
#     if not check_password_hash(user['password'], password):  
#         db_close(conn, cur)
#         return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
#     session['login'] = login
#     db_close(conn, cur)
#     return render_template('rgz/success_login.html', login=login)

# @rgz.route('/rgz/logout')
# def logout():
#     session.pop('login', None)  # Удаляем логин из сессии
#     return redirect('/rgz/login')


# Авторизация

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Unsupported Media Type'}), 415
        
        data = request.get_json()
        
        if not data or 'method' not in data or data['method'] != 'login':
            return jsonify({'error': 'Invalid request'}), 400

        params = data.get('params', {})
        login = params.get('login')
        password = params.get('password')

        if not (login and password):
            return jsonify({'error': 'Заполните поля'}), 400

        # Подключение к базе данных
        conn, cur = db_connect()

        # Выполнение SQL-запроса с параметризованным запросом
        cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
        user = cur.fetchone()  # Получаем одну строку

        if not user:  
            db_close(conn, cur)
            return jsonify({'error': 'Логин и/или пароль неверны'}), 401
        
        # Проверка пароля
        if not check_password_hash(user['password'], password):  
            db_close(conn, cur)
            return jsonify({'error': 'Логин и/или пароль неверны'}), 401
        
        session['login'] = login
        db_close(conn, cur)
        
        # Возвращаем URL для рендеринга success_login.html
        return jsonify({'result': {'redirect': '/rgz/success_login'}})

@rgz.route('/rgz/success_login', methods=['GET'])
def success_login():
    login = session.get('login')
    if not login:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return render_template('rgz/success_login.html', login=login)

# Выход из аккаунта

@rgz.route('/rgz/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        session.pop('login', None)  # Удаляем логин из сессии
        return redirect('/rgz/login')
    
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Unsupported Media Type'}), 415
        
        data = request.get_json()
        
        if not data or 'method' not in data or data['method'] != 'logout':
            return jsonify({'error': 'Invalid request'}), 400

        session.pop('login', None)  # Удаляем логин из сессии
        
        # Возвращаем URL для редиректа на страницу входа
        return jsonify({'result': {'redirect': '/rgz/login'}})
    
# Регистрация

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Unsupported Media Type'}), 415
        
        data = request.get_json()
        
        if not data or 'method' not in data or data['method'] != 'register':
            return jsonify({'error': 'Invalid request'}), 400

        params = data.get('params', {})
        login = params.get('login')
        password = params.get('password')

        if not (login and password):
            return jsonify({'error': 'Заполните все поля'}), 400
        
        conn, cur = db_connect()

        # Проверяем, есть ли уже зарегистрированный пользователь
        cur.execute("SELECT COUNT(*) FROM admin;")
        user_count = cur.fetchone()[0]
        
        if user_count >= 1:  # Если уже есть хотя бы один пользователь
            db_close(conn, cur)
            return jsonify({'error': 'Регистрация доступна только для одного пользователя'}), 400

        # Проверяем, существует ли пользователь с таким логином
        cur.execute("SELECT login FROM admin WHERE login=?", (login,))
        
        if cur.fetchone():
            db_close(conn, cur)
            return jsonify({'error': 'Такой пользователь уже существует'}), 400
        
        password_hash = generate_password_hash(password)

        # Вставляем нового пользователя
        cur.execute("INSERT INTO admin (login, password) VALUES (?, ?)", (login, password_hash))
        conn.commit()

        db_close(conn, cur)
        
        # Возвращаем URL для рендеринга success.html
        return jsonify({'result': {'redirect': '/rgz/success'}})

@rgz.route('/rgz/success', methods=['GET'])
def success():
    login = session.get('login')
    if not login:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return render_template('rgz/success.html', login=login)

# Список книг

@rgz.route('/rgz/books', methods=['GET', 'POST'])
def list_books():
    if request.method == 'GET':
        # Обработка GET запроса для рендеринга HTML
        page = int(request.args.get('page', 1))
        filter_title = request.args.get('title', '')
        filter_author = request.args.get('author', '')
        filter_pages_from = request.args.get('pages_from', type=int)
        filter_pages_to = request.args.get('pages_to', type=int)
        filter_publisher = request.args.get('publisher', '')

        conn, cur = db_connect()
        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if filter_title:
            query += " AND title LIKE ?"
            params.append(f"%{filter_title}%")
        if filter_author:
            query += " AND author LIKE ?"
            params.append(f"%{filter_author}%")
        if filter_pages_from is not None:
            query += " AND amount_of_pages >= ?"
            params.append(filter_pages_from)
        if filter_pages_to is not None:
            query += " AND amount_of_pages <= ?"
            params.append(filter_pages_to)
        if filter_publisher:
            query += " AND publisher LIKE ?"
            params.append(f"%{filter_publisher}%")

        query += " LIMIT 20 OFFSET ?"
        params.append((page - 1) * 20)

        # Выполняем основной запрос
        cur.execute(query, params)
        books = cur.fetchall()

        # Получаем общее количество книг для пагинации
        count_query = "SELECT COUNT(*) FROM books WHERE 1=1"
        count_params = []
        if filter_title:
            count_query += " AND title LIKE ?"
            count_params.append(f"%{filter_title}%")
        if filter_author:
            count_query += " AND author LIKE ?"
            count_params.append(f"%{filter_author}%")
        if filter_pages_from is not None:
            count_query += " AND amount_of_pages >= ?"
            count_params.append(filter_pages_from)
        if filter_pages_to is not None:
            count_query += " AND amount_of_pages <= ?"
            count_params.append(filter_pages_to)
        if filter_publisher:
            count_query += " AND publisher LIKE ?"
            count_params.append(f"%{filter_publisher}%")

        cur.execute(count_query, count_params)
        total_count = cur.fetchone()[0]

        db_close(conn, cur)
        
        return render_template('rgz/books.html', books=books, page=page, total_count=total_count, request=request)

    elif request.method == 'POST':
        # Обработка POST запроса для JSON-RPC
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Content-Type. Expected application/json.'}, 'id': None}), 415

        try:
            data = request.json
        except json.JSONDecodeError:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}, 'id': None}), 400
        
        if data.get('jsonrpc') != '2.0' or data.get('method') != 'list_books':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Request'}, 'id': data.get('id')}), 400
        
        params = data.get('params', {})
        page = int(params.get('page', 1))
        filter_title = params.get('title', '')
        filter_author = params.get('author', '')
        filter_pages_from = params.get('pages_from', None)
        filter_pages_to = params.get('pages_to', None)
        filter_publisher = params.get('publisher', '')

        conn, cur = db_connect()
        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if filter_title:
            query += " AND title LIKE ?"
            params.append(f"%{filter_title}%")
        if filter_author:
            query += " AND author LIKE ?"
            params.append(f"%{filter_author}%")
        if filter_pages_from is not None:
            query += " AND amount_of_pages >= ?"
            params.append(filter_pages_from)
        if filter_pages_to is not None:
            query += " AND amount_of_pages <= ?"
            params.append(filter_pages_to)
        if filter_publisher:
            query += " AND publisher LIKE ?"
            params.append(f"%{filter_publisher}%")

        query += " LIMIT 20 OFFSET ?"
        params.append((page - 1) * 20)

        # Выполняем основной запрос
        cur.execute(query, params)
        books = cur.fetchall()

        # Получаем общее количество книг для пагинации
        count_query = "SELECT COUNT(*) FROM books WHERE 1=1"
        count_params = []
        if filter_title:
            count_query += " AND title LIKE ?"
            count_params.append(f"%{filter_title}%")
        if filter_author:
            count_query += " AND author LIKE ?"
            count_params.append(f"%{filter_author}%")
        if filter_pages_from is not None:
            count_query += " AND amount_of_pages >= ?"
            count_params.append(filter_pages_from)
        if filter_pages_to is not None:
            count_query += " AND amount_of_pages <= ?"
            count_params.append(filter_pages_to)
        if filter_publisher:
            count_query += " AND publisher LIKE ?"
            count_params.append(f"%{filter_publisher}%")

        cur.execute(count_query, count_params)
        total_count = cur.fetchone()[0]

        db_close(conn, cur)
        
        # Формируем ответ в формате JSON-RPC
        response = {
            'jsonrpc': '2.0',
            'result': {
                'books': books,
                'page': page,
                'total_count': total_count
            },
            'id': data.get('id')
        }
        
        return jsonify(response)

# Страница аккаунта

@rgz.route('/rgz/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        # Обработка GET запроса для рендеринга HTML
        if 'login' not in session:
            return redirect(url_for('rgz.login'))  # Перенаправление на страницу входа

        login = session['login']

        # Подключение к базе данных
        conn, cur = db_connect()

        # Получение информации о пользователе
        cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
        user = cur.fetchone()

        # Закрываем соединение
        db_close(conn, cur)

        if user is None:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': 404, 'message': 'User not found'}, 'id': None}), 404

        # Рендеринг HTML страницы
        return render_template('rgz/account.html', user=user)

    elif request.method == 'POST':
        # Обработка POST запроса для JSON-RPC
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Content-Type. Expected application/json'}, 'id': None}), 415

        try:
            data = request.json
        except json.JSONDecodeError:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}, 'id': None}), 400
        
        if data.get('jsonrpc') != '2.0' or data.get('method') != 'get_account_info':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Request'}, 'id': data.get('id')}), 400
        
        if 'login' not in session:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': 401, 'message': 'Unauthorized'}, 'id': data.get('id')}), 401

        login = session['login']

        # Подключение к базе данных
        conn, cur = db_connect()

        # Получение информации о пользователе
        cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
        user = cur.fetchone()

        # Закрываем соединение
        db_close(conn, cur)

        if user is None:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': 404, 'message': 'User not found'}, 'id': data.get('id')}), 404

        # Возвращаем данные в формате JSON-RPC
        return jsonify({
            'jsonrpc': '2.0',
            'result': {
                'name': user['name'],
                'login': user['login']
            },
            'id': data.get('id')
        }), 200

# Редактирование аккаунта

@rgz.route('/rgz/edit_account', methods=['GET', 'POST'])
def edit_account():
    if 'login' not in session:
        return redirect(url_for('rgz.login'))

    login = session['login']

    # Подключение к базе данных
    conn, cur = db_connect()

    # Получение информации о пользователе
    cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
    user = cur.fetchone()

    if request.method == 'GET':
        # Обработка GET запроса для рендеринга HTML
        db_close(conn, cur)
        return render_template('rgz/edit_account.html', user=user)

    elif request.method == 'POST':
        # Обработка POST запроса для JSON-RPC
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Content-Type. Expected application/json'}, 'id': None}), 415

        try:
            data = request.json
        except json.JSONDecodeError:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}, 'id': None}), 400
        
        if data.get('jsonrpc') != '2.0' or data.get('method') != 'edit_account':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Request'}, 'id': data.get('id')}), 400
        
        params = data.get('params', {})
        new_login = params.get('login')
        new_password = params.get('password')

        # Обновление данных пользователя
        if new_login and new_login != login:  # Проверяем, чтобы новый логин не был пустым и отличался от текущего
            cur.execute("UPDATE admin SET login=? WHERE login=?;", (new_login, login))
            session['login'] = new_login  # Обновляем сессию до нового логина
            login = new_login  # Обновляем переменную login для последующих операций

        if new_password:
            hashed_password = generate_password_hash(new_password)  # Используйте функцию для хеширования
            cur.execute("UPDATE admin SET password=? WHERE login=?;", (hashed_password, login))

        conn.commit()  # Сохраняем изменения
        db_close(conn, cur)

        # Возвращаем данные в формате JSON-RPC
        return jsonify({
            'jsonrpc': '2.0',
            'result': {
                'message': 'Account updated successfully',
                'redirect': '/rgz/account'
            },
            'id': data.get('id')
        }), 200


# Удаление аккаунта
@rgz.route('/rgz/delete_account', methods=['POST'])
def delete_account():
    # Проверка Content-Type
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Content-Type. Expected application/json'}, 'id': None}), 415

    try:
        data = request.json
    except json.JSONDecodeError:
        return jsonify({'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}, 'id': None}), 400
    
    # Проверка обязательных полей в JSON-RPC запросе
    if data.get('jsonrpc') != '2.0' or data.get('method') != 'delete_account':
        return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Request'}, 'id': data.get('id')}), 400
    
    # Проверка авторизации
    if 'login' not in session:
        return jsonify({'jsonrpc': '2.0', 'error': {'code': 401, 'message': 'Unauthorized'}, 'id': data.get('id')}), 401

    login = session['login']

    try:
        # Подключение к базе данных
        conn, cur = db_connect()

        # Удаление пользователя
        cur.execute("DELETE FROM admin WHERE login=?;", (login,))
        conn.commit()

    except sqlite3.Error as e:
        # Обработка ошибок базы данных
        return jsonify({'jsonrpc': '2.0', 'error': {'code': -32000, 'message': f'Database error: {str(e)}'}, 'id': data.get('id')}), 500

    finally:
        # Закрытие соединения с базой данных
        db_close(conn, cur)

    # Удаляем сессию
    session.pop('login', None)

    # Возвращаем данные в формате JSON-RPC
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'message': 'Account deleted successfully',
            'redirect': '/rgz/login'
        },
        'id': data.get('id')
    }), 200



# Страница управления книгами

@rgz.route('/rgz/manage_books', methods=['GET', 'POST'])
def manage_books():
    if request.method == 'GET':
        # Проверяем, есть ли активная сессия и существует ли логин
        if 'login' not in session:
            return redirect(url_for('rgz.login'))  # Если нет, перенаправляем на страницу входа

        # Отображение страницы управления книгами
        return render_template('rgz/manage_books.html')

    elif request.method == 'POST':
        # Обработка POST запроса для JSON-RPC
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Content-Type. Expected application/json'}, 'id': None}), 415

        try:
            data = request.json
        except json.JSONDecodeError:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}, 'id': None}), 400
        
        if data.get('jsonrpc') != '2.0' or data.get('method') != 'manage_books':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Request'}, 'id': data.get('id')}), 400
        
        if 'login' not in session:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': 401, 'message': 'Unauthorized'}, 'id': data.get('id')}), 401

        # Возвращаем данные в формате JSON-RPC
        return jsonify({
            'jsonrpc': '2.0',
            'result': {
                'message': 'Manage books page accessed successfully',
                'redirect': '/rgz/manage_books'
            },
            'id': data.get('id')
        }), 200


# Редактирование книг

@rgz.route('/rgz/edit_book', methods=['GET', 'POST'])
def edit_book():
    if 'login' not in session:
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()
    book = None
    search_attempt = False  # Инициализируем переменную

    if request.method == 'GET':
        # Поиск книги по ID
        book_id = request.args.get('id')
        if book_id:
            cur.execute("SELECT * FROM books WHERE id=?;", (book_id,))
            book = cur.fetchone()

            if book is None:
                search_attempt = True  # Устанавливаем флаг, если книга не найдена

        db_close(conn, cur)
        return render_template('rgz/edit_book.html', book=book, search_attempt=search_attempt)

    elif request.method == 'POST':
        # Обработка POST запроса для JSON-RPC
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Content-Type. Expected application/json'}, 'id': None}), 415

        try:
            data = request.json
        except json.JSONDecodeError:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}, 'id': None}), 400
        
        if data.get('jsonrpc') != '2.0' or data.get('method') != 'edit_book':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Request'}, 'id': data.get('id')}), 400
        
        params = data.get('params', {})
        book_id = params.get('id')
        title = params.get('title')
        author = params.get('author')
        year_of_publication = params.get('year_of_publication')
        publisher = params.get('publisher')
        book_cover = params.get('book_cover')
        amount_of_pages = params.get('amount_of_pages')

        cur.execute(""" 
            UPDATE books 
            SET title=?, author=?, year_of_publication=?, publisher=?, book_cover=?, amount_of_pages=? 
            WHERE id=?;
        """, (title, author, year_of_publication, publisher, book_cover, amount_of_pages, book_id))

        conn.commit()
        db_close(conn, cur)

        # Возвращаем данные в формате JSON-RPC
        return jsonify({
            'jsonrpc': '2.0',
            'result': {
                'message': 'Book updated successfully',
                'redirect': '/rgz/manage_books'
            },
            'id': data.get('id')
        }), 200

# Страница добавления книги

@rgz.route('/rgz/add_book', methods=['GET', 'POST'])
def add_book():
    if 'login' not in session:
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()
    success_message = None
    error_message = None
    search_attempt = False
    book = None

    if request.method == 'GET':
        # Поиск книги по ID
        book_id = request.args.get('id')
        if book_id:
            cur.execute("SELECT * FROM Books WHERE id=?;", (book_id,))
            book = cur.fetchone()
            if book is None:
                search_attempt = True

        db_close(conn, cur)
        return render_template('rgz/add_book.html', book=book, search_attempt=search_attempt, success_message=success_message, error_message=error_message)

    elif request.method == 'POST':
        # Обработка POST запроса для JSON-RPC
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Content-Type. Expected application/json'}, 'id': None}), 415

        try:
            data = request.json
        except json.JSONDecodeError:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}, 'id': None}), 400
        
        if data.get('jsonrpc') != '2.0' or data.get('method') != 'add_book':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Request'}, 'id': data.get('id')}), 400
        
        params = data.get('params', {})
        book_id = params.get('id')
        title = params.get('title')
        author = params.get('author')
        year_of_publication = params.get('year_of_publication')
        publisher = params.get('publisher')
        book_cover = params.get('book_cover')
        amount_of_pages = params.get('amount_of_pages')

        # Проверка на пустые поля
        if not all([book_id, title, author, year_of_publication, publisher, book_cover, amount_of_pages]):
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'All fields must be filled'}, 'id': data.get('id')}), 400

        # Проверяем, существует ли книга с таким ID
        cur.execute("SELECT * FROM Books WHERE id=?;", (book_id,))
        existing_book = cur.fetchone()

        if existing_book:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'Book with this ID already exists'}, 'id': data.get('id')}), 400

        # Вставляем данные в таблицу books
        try:
            cur.execute("""
                INSERT INTO Books (id, title, author, year_of_publication, publisher, book_cover, amount_of_pages)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (book_id, title, author, year_of_publication, publisher, book_cover, amount_of_pages))
            conn.commit()
        except Exception as e:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32000, 'message': str(e)}, 'id': data.get('id')}), 500

        db_close(conn, cur)

        # Возвращаем данные в формате JSON-RPC
        return jsonify({
            'jsonrpc': '2.0',
            'result': {
                'message': 'Book added successfully',
                'redirect': '/rgz/manage_books'
            },
            'id': data.get('id')
        }), 200

# Страница удаления книги

@rgz.route('/rgz/delete_book', methods=['GET', 'POST'])
def delete_book():
    if 'login' not in session:
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()
    success_message = None
    error_message = None

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('rgz/delete_book.html', success_message=success_message, error_message=error_message)

    elif request.method == 'POST':
        # Обработка POST запроса для JSON-RPC
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Content-Type. Expected application/json'}, 'id': None}), 415

        try:
            data = request.json
        except json.JSONDecodeError:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32700, 'message': 'Parse error'}, 'id': None}), 400
        
        if data.get('jsonrpc') != '2.0' or data.get('method') != 'delete_book':
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32600, 'message': 'Invalid Request'}, 'id': data.get('id')}), 400
        
        params = data.get('params', {})
        book_id = params.get('id')

        if not book_id:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'Book ID cannot be empty'}, 'id': data.get('id')}), 400

        # Проверяем, существует ли книга с таким ID
        cur.execute("SELECT * FROM Books WHERE id=?;", (book_id,))
        existing_book = cur.fetchone()

        if not existing_book:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'Book with this ID not found'}, 'id': data.get('id')}), 404

        # Удаляем книгу
        try:
            cur.execute("DELETE FROM Books WHERE id=?;", (book_id,))
            conn.commit()
        except Exception as e:
            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32000, 'message': str(e)}, 'id': data.get('id')}), 500

        db_close(conn, cur)

        # Возвращаем данные в формате JSON-RPC
        return jsonify({
            'jsonrpc': '2.0',
            'result': {
                'message': 'Book deleted successfully',
                'redirect': '/rgz/manage_books'
            },
            'id': data.get('id')
        }), 200




# Старый код

# from flask import Blueprint, redirect, url_for, render_template, request, session, current_app
# import sqlite3
# from werkzeug.security import check_password_hash, generate_password_hash
# from os import path

# # 7 Вариант

# rgz = Blueprint('rgz', __name__)

# @rgz.route('/rgz/')
# def main():
#     return render_template('rgz/main.html', login = session.get('login'))

# def db_connect():
#     if current_app.config['DB_TYPE'] == 'postgres':
#         # Подключение к базе данных
#         conn = sqlite3.connect(r'C:\Users\PC\Desktop\Документы\ВУЗ\3 курс\Web-программирование\База данных\rgz_db') 
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#     else:
#         dir_path = path.dirname(path.realpath(__file__))
#         db_path = path.join(dir_path, "database.db")
#         conn = sqlite3.connect(db_path)
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#     return conn, cur

# def db_close(conn,cur):
#     conn.commit()
#     cur.close()
#     conn.close()


# @rgz.route('/rgz/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('rgz/login.html')
    
#     login = request.form.get('login')
#     password = request.form.get('password')

#     if not (login and password):
#         return render_template('rgz/login.html', error='Заполните поля')

#     # Подключение к базе данных
#     conn, cur = db_connect()

#     # Выполнение SQL-запроса с параметризованным запросом
#     # if current_app.config['DB_TYPE'] == 'postgres':
#     #     cur.execute("SELECT * FROM admin WHERE login=%s;", (login,))
#     # else:
#     #     cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
#     cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
#     user = cur.fetchone()  # Получаем одну строку

#     if not user:  
#         db_close(conn, cur)
#         return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
#     # Проверка пароля
#     if not check_password_hash(user['password'], password):  
#         db_close(conn, cur)
#         return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
#     session['login'] = login
#     db_close(conn, cur)
#     return render_template('rgz/success_login.html', login=login)

# @rgz.route('/rgz/logout')
# def logout():
#     session.pop('login', None)  # Удаляем логин из сессии
#     return redirect('/rgz/login')

# @rgz.route('/rgz/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('rgz/register.html')
    
#     login = request.form.get('login')
#     password = request.form.get('password')

#     if not (login and password):
#         return render_template('rgz/register.html', error='Заполните все поля')
    
#     conn, cur = db_connect()

#     # Проверяем, есть ли уже зарегистрированный пользователь
#     cur.execute("SELECT COUNT(*) FROM admin;")
#     user_count = cur.fetchone()[0]
    
#     if user_count >= 1:  # Если уже есть хотя бы один пользователь
#         db_close(conn, cur)
#         return render_template('rgz/register.html', error='Регистрация доступна только для одного пользователя')

#     # Проверяем, существует ли пользователь с таким логином
#     cur.execute("SELECT login FROM admin WHERE login=?", (login,))
    
#     if cur.fetchone():
#         db_close(conn, cur)
#         return render_template('rgz/register.html', error='Такой пользователь уже существует')
    
#     password_hash = generate_password_hash(password)

#     # Вставляем нового пользователя
#     cur.execute("INSERT INTO admin (login, password) VALUES (?, ?)", (login, password_hash))

#     db_close(conn, cur)
#     return render_template('rgz/success.html', login=login)


# @rgz.route('/rgz/books', methods=['GET'])
# def list_books():
#     page = int(request.args.get('page', 1))
#     filter_title = request.args.get('title', '')
#     filter_author = request.args.get('author', '')
#     filter_pages_from = request.args.get('pages_from', type=int)
#     filter_pages_to = request.args.get('pages_to', type=int)
#     filter_publisher = request.args.get('publisher', '')

#     conn, cur = db_connect()
#     query = "SELECT * FROM books WHERE 1=1"
#     params = []

#     if filter_title:
#         query += " AND title LIKE ?"
#         params.append(f"%{filter_title}%")
#     if filter_author:
#         query += " AND author LIKE ?"
#         params.append(f"%{filter_author}%")
#     if filter_pages_from is not None:
#         query += " AND amount_of_pages >= ?"  # Изменено с pages на amount_of_pages
#         params.append(filter_pages_from)
#     if filter_pages_to is not None:
#         query += " AND amount_of_pages <= ?"  # Изменено с pages на amount_of_pages
#         params.append(filter_pages_to)
#     if filter_publisher:
#         query += " AND publisher LIKE ?"
#         params.append(f"%{filter_publisher}%")

#     query += " LIMIT 20 OFFSET ?"
#     params.append((page - 1) * 20)

#     # Выполняем основной запрос
#     cur.execute(query, params)
#     books = cur.fetchall()

#     # Получаем общее количество книг для пагинации
#     count_query = "SELECT COUNT(*) FROM books WHERE 1=1"
#     count_params = []
#     if filter_title:
#         count_query += " AND title LIKE ?"
#         count_params.append(f"%{filter_title}%")
#     if filter_author:
#         count_query += " AND author LIKE ?"
#         count_params.append(f"%{filter_author}%")
#     if filter_pages_from is not None:
#         count_query += " AND amount_of_pages >= ?" 
#         count_params.append(filter_pages_from)
#     if filter_pages_to is not None:
#         count_query += " AND amount_of_pages <= ?"  
#         count_params.append(filter_pages_to)
#     if filter_publisher:
#         count_query += " AND publisher LIKE ?"
#         count_params.append(f"%{filter_publisher}%")

#     cur.execute(count_query, count_params)
#     total_count = cur.fetchone()[0]

#     db_close(conn, cur)
    
#     return render_template('rgz/books.html', books=books, page=page, total_count=total_count, request=request)



# @rgz.route('/rgz/account')
# def account():
#     if 'login' not in session:
#         return redirect('/rgz/login')

#     login = session['login']

#     # Подключение к базе данных
#     conn, cur = db_connect()

#     # Получение информации о пользователе
#     cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
#     user = cur.fetchone()

#     # Закрываем соединение
#     db_close(conn, cur)

#     return render_template('rgz/account.html', user=user)

# @rgz.route('/rgz/edit_account', methods=['GET', 'POST'])
# def edit_account():
#     if 'login' not in session:
#         return redirect('/rgz/login')

#     login = session['login']

#     # Подключение к базе данных
#     conn, cur = db_connect()

#     # Получение информации о пользователе
#     cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
#     user = cur.fetchone()

#     if request.method == 'POST':
#         new_login = request.form.get('login')
#         new_password = request.form.get('password')

#         # Обновление данных пользователя
#         if new_login and new_login != login:  # Проверяем, чтобы новый логин не был пустым и отличался от текущего
#             cur.execute("UPDATE admin SET login=? WHERE login=?;", (new_login, login))
#             session['login'] = new_login  # Обновляем сессию до нового логина
#             login = new_login  # Обновляем переменную login для последующих операций

#         if new_password:
#             hashed_password = generate_password_hash(new_password)  # Используйте функцию для хеширования
#             cur.execute("UPDATE admin SET password=? WHERE login=?;", (hashed_password, login))

#         conn.commit()  # Сохраняем изменения
#         db_close(conn, cur)
#         return redirect('/rgz/account')

#     db_close(conn, cur)
#     return render_template('rgz/edit_account.html', user=user)



# @rgz.route('/rgz/delete_account', methods=['POST'])
# def delete_account():
#     if 'login' not in session:
#         return redirect('/rgz/login')

#     login = session['login']

#     # Подключение к базе данных
#     conn, cur = db_connect()

#     # Удаление пользователя
#     cur.execute("DELETE FROM admin WHERE login=?;", (login,))
#     conn.commit()

#     db_close(conn, cur)

#     session.pop('login', None)  # Удаляем сессию
#     return redirect('/rgz/login')


# @rgz.route('/rgz/manage_books', methods=['GET'])
# def manage_books():
#     # Проверяем, есть ли активная сессия и существует ли логин
#     if 'login' not in session:
#         return redirect('/rgz/login')  # Если нет, перенаправляем на страницу входа

#     # Отображение страницы управления книгами
#     return render_template('rgz/manage_books.html')

# @rgz.route('/rgz/edit_book', methods=['GET', 'POST'])
# def edit_book():
#     if 'login' not in session:
#         return redirect('/rgz/login')

#     conn, cur = db_connect()
#     book = None
#     search_attempt = False  # Инициализируем переменную

#     if request.method == 'POST':
#         # Обновление данных книги
#         book_id = request.form.get('id')
#         title = request.form.get('title')
#         author = request.form.get('author')
#         year_of_publication = request.form.get('year_of_publication')
#         publisher = request.form.get('publisher')
#         book_cover = request.form.get('book_cover')
#         amount_of_pages = request.form.get('amount_of_pages')

#         cur.execute(""" 
#             UPDATE books 
#             SET title=?, author=?, year_of_publication=?, publisher=?, book_cover=?, amount_of_pages=? 
#             WHERE id=?;
#         """, (title, author, year_of_publication, publisher, book_cover, amount_of_pages, book_id))

#         db_close(conn, cur)
#         return redirect('/rgz/manage_books')

#     # Поиск книги по ID
#     book_id = request.args.get('id')
#     if book_id:
#         cur.execute("SELECT * FROM books WHERE id=?;", (book_id,))
#         book = cur.fetchone()

#         if book is None:
#             search_attempt = True  # Устанавливаем флаг, если книга не найдена

#     db_close(conn, cur)
#     return render_template('rgz/edit_book.html', book=book, search_attempt=search_attempt)

# @rgz.route('/rgz/add_book', methods=['GET', 'POST'])
# def add_book():
#     if 'login' not in session:
#         return redirect('/rgz/login')

#     conn, cur = db_connect()
#     success_message = None
#     error_message = None
#     search_attempt = False
#     book = None

#     if request.method == 'POST':
#         # Получаем данные из формы
#         book_id = request.form.get('id')
#         title = request.form.get('title')
#         author = request.form.get('author')
#         year_of_publication = request.form.get('year_of_publication')
#         publisher = request.form.get('publisher')
#         book_cover = request.form.get('book_cover')
#         amount_of_pages = request.form.get('amount_of_pages')

#         # Проверка на пустые поля
#         if not all([book_id, title, author, year_of_publication, publisher, book_cover, amount_of_pages]):
#             error_message = "Ошибка: Все поля должны быть заполнены."
#         else:
#             # Проверяем, существует ли книга с таким ID
#             cur.execute("SELECT * FROM Books WHERE id=?;", (book_id,))
#             existing_book = cur.fetchone()

#             if existing_book:
#                 error_message = "Ошибка: Книга с таким ID уже существует."
#             else:
#                 # Вставляем данные в таблицу books
#                 try:
#                     cur.execute("""
#                         INSERT INTO Books (id, title, author, year_of_publication, publisher, book_cover, amount_of_pages)
#                         VALUES (?, ?, ?, ?, ?, ?, ?);
#                     """, (book_id, title, author, year_of_publication, publisher, book_cover, amount_of_pages))
#                     conn.commit()
#                     success_message = "Книга успешно добавлена!"
#                 except Exception as e:
#                     error_message = f"Произошла ошибка: {str(e)}"

#     # Поиск книги по ID
#     book_id = request.args.get('id')
#     if book_id:
#         cur.execute("SELECT * FROM Books WHERE id=?;", (book_id,))
#         book = cur.fetchone()
#         if book is None:
#             search_attempt = True

#     db_close(conn, cur)
#     return render_template('rgz/add_book.html', book=book, search_attempt=search_attempt, success_message=success_message, error_message=error_message)

# @rgz.route('/rgz/delete_book', methods=['GET', 'POST'])
# def delete_book():
#     if 'login' not in session:
#         return redirect('/rgz/login')

#     conn, cur = db_connect()
#     success_message = None
#     error_message = None

#     if request.method == 'POST':
#         book_id = request.form.get('id')

#         if not book_id:
#             error_message = "Ошибка: ID книги не может быть пустым."
#         else:
#             # Проверяем, существует ли книга с таким ID
#             cur.execute("SELECT * FROM Books WHERE id=?;", (book_id,))
#             existing_book = cur.fetchone()

#             if not existing_book:
#                 error_message = "Ошибка: Книга с таким ID не найдена."
#             else:
#                 # Удаляем книгу
#                 try:
#                     cur.execute("DELETE FROM Books WHERE id=?;", (book_id,))
#                     conn.commit()
#                     success_message = "Книга успешно удалена!"
#                 except Exception as e:
#                     error_message = f"Произошла ошибка: {str(e)}"

#     db_close(conn, cur)
#     return render_template('rgz/delete_book.html', success_message=success_message, error_message=error_message)

