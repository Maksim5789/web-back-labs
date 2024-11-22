from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, jsonify, flash
import sqlite3
from os import path
import hashlib

lab6 = Blueprint('lab6', __name__)

# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        # Подключение к базе данных
        conn = sqlite3.connect(r'C:\Users\PC\Desktop\Документы\ВУЗ\3 курс\Web-программирование\База данных\database_web') 
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

@lab6.route('/lab6/')
def lab():
    username = session.get('login', 'Анонимус')  # Получаем имя пользователя из сессии или устанавливаем "Анонимус"
    return render_template('lab6/lab6.html', username=username)

@lab6.route('/lab6/json-rpc-api', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    if data['method'] == 'info':
        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices")
        offices = cur.fetchall()
        db_close(conn, cur)
        print("Offices from DB:", offices)  # Отладочный вывод
        return {
            'jsonrpc': '2.0',
            'result': [dict(office) for office in offices],
            'id': id
        }
    
    if data['method'] == 'register':
        login = data['params']['login']
        password = data['params']['password']
        hashed_password = hash_password(password)

        conn, cur = db_connect()
        cur.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = cur.fetchone()

        if user:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Пользователь с таким логином уже существует'
                },
                'id': id
            }

        cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, hashed_password))
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    
    if data['method'] == 'login':
        login = data['params']['login']
        password = data['params']['password']
        hashed_password = hash_password(password)

        conn, cur = db_connect()
        cur.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, hashed_password))
        user = cur.fetchone()
        db_close(conn, cur)

        if user:
            session['login'] = login
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        else:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Неверный логин или пароль'
                },
                'id': id
            }
    
    if data['method'] == 'logout':
        session.pop('login', None)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices WHERE number = ?", (office_number,))
        office = cur.fetchone()
        if office and office['tenant'] != '':
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        cur.execute("UPDATE offices SET tenant = ? WHERE number = ?", (login, office_number))
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    
    if data['method'] == 'unbooking':
        office_number = data['params']
        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices WHERE number = ?", (office_number,))
        office = cur.fetchone()
        if office and office['tenant'] != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'You are not the tenant of this office'
                },
                'id': id
            }
        cur.execute("UPDATE offices SET tenant = '' WHERE number = ?", (office_number,))
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }