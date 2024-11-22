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