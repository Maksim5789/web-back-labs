from flask import Blueprint, redirect, url_for, render_template, request, session, current_app
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path

# 7 Вариант

rgz = Blueprint('rgz', __name__)

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


@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('rgz/login.html', error='Заполните поля')

    # Подключение к базе данных
    conn, cur = db_connect()

    # Выполнение SQL-запроса с параметризованным запросом
    # if current_app.config['DB_TYPE'] == 'postgres':
    #     cur.execute("SELECT * FROM admin WHERE login=%s;", (login,))
    # else:
    #     cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
    cur.execute("SELECT * FROM admin WHERE login=?;", (login,))
    user = cur.fetchone()  # Получаем одну строку

    if not user:  
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
    # Проверка пароля
    if not check_password_hash(user['password'], password):  
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('rgz/success_login.html', login=login)

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)  # Удаляем логин из сессии
    return redirect('/rgz/login')

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('rgz/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    # Проверяем, есть ли уже зарегистрированный пользователь
    cur.execute("SELECT COUNT(*) FROM admin;")
    user_count = cur.fetchone()[0]
    
    if user_count >= 1:  # Если уже есть хотя бы один пользователь
        db_close(conn, cur)
        return render_template('rgz/register.html', error='Регистрация доступна только для одного пользователя')

    # Проверяем, существует ли пользователь с таким логином
    cur.execute("SELECT login FROM admin WHERE login=?", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)

    # Вставляем нового пользователя
    cur.execute("INSERT INTO admin (login, password) VALUES (?, ?)", (login, password_hash))

    db_close(conn, cur)
    return render_template('rgz/success.html', login=login)


@rgz.route('/rgz/books', methods=['GET'])
def list_books():
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
        query += " AND amount_of_pages >= ?"  # Изменено с pages на amount_of_pages
        params.append(filter_pages_from)
    if filter_pages_to is not None:
        query += " AND amount_of_pages <= ?"  # Изменено с pages на amount_of_pages
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


