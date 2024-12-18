from flask import Blueprint, redirect, url_for, render_template, request, session, current_app
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login = session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        # Подключение к базе данных
        conn = sqlite3.connect(r'C:\Users\PC\Desktop\Документы\ВУЗ\3 курс\Web-программирование\База данных\database_web') 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "lab8.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn,cur):
    conn.commit()
    cur.close()
    conn.close()


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab8/login.html', error='Заполните поля')

    # Подключение к базе данных
    conn, cur = db_connect()

    # Выполнение SQL-запроса с параметризованным запросом
    # if current_app.config['DB_TYPE'] == 'postgres':
    #     cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    # else:
    #     cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()  # Получаем одну строку

    if not user:  
        db_close(conn, cur)
        return render_template('lab8/login.html', error='Логин и/или пароль неверны')
    
    # Проверка пароля
    if not check_password_hash(user['password'], password):  
        db_close(conn, cur)
        return render_template('lab8/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab8/success_login.html', login=login)


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на заполнение всех полей
    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Заполните все поля')
    
    # Проверка на существование пользователя
    login_exists = users.query.filter_by(login=login_form).first()  # Убедитесь, что users — это класс модели
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    
    # Хэширование пароля
    password_hash = generate_password_hash(password_form)
    
    # Создание нового пользователя
    new_user = users(login=login_form, password=password_hash)  # Убедитесь, что users — это класс модели
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/lab8/')


@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab8/login')
    
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # Валидация пустых полей
    if not title or not article_text:
        return render_template('lab8/create_article.html', error='Название и текст статьи не могут быть пустыми.')

    conn, cur = db_connect()

    # if current_app.config['DB_TYPE'] == 'postgres':
    #     cur.execute(f"SELECT * FROM users WHERE login=%s;", (login,))
    # else:
    #     cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    login_id = cur.fetchone()["id"]

    # if current_app.config['DB_TYPE'] == 'postgres':
    #     cur.execute(
    #         f"INSERT INTO articles (user_id, title, article) VALUES (%s, %s, %s);", (user_id, title, article_text))
    # else:
    #     cur.execute(
    #         "INSERT INTO articles (user_id, title, article) VALUES (?, ?, ?);", (user_id, title, article_text))
        
    cur.execute(
            "INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?);", (login_id, title, article_text))

    cur.fetchone()

    db_close(conn,cur)
    return redirect('/lab8')

@lab8.route('/lab8/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab8/login')
    
    conn, cur = db_connect()
    
    cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute("SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC;", (login_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab8/articles.html', articles=articles)

@lab8.route('/lab8/logout')
def logout():
    session.pop('login', None)  # Удаляем логин из сессии
    return redirect('/lab8/login')


@lab8.route('/lab8/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn, cur = db_connect()
    
    if request.method == 'GET':
        cur.execute("SELECT * FROM articles WHERE id=?;", (id,))
        article = cur.fetchone()
        db_close(conn, cur)
        
        if not article:
            return render_template('lab8/error.html', error='Статья не найдена.')  # Можно сделать отдельный шаблон для ошибок

        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # Валидация пустых полей
    if not title or not article_text:
        # При наличии ошибки отображаем её
        return render_template('lab8/edit_article.html', article=article, error='Название и текст статьи не могут быть пустыми.')

    cur.execute("UPDATE articles SET title=?, article=? WHERE id=?;", (title, article_text, id))
    db_close(conn, cur)
    return redirect('/lab8/list')

@lab8.route('/lab8/delete/<int:id>', methods=['POST'])
def delete(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM articles WHERE id=?;", (id,))
    db_close(conn, cur)
    return redirect('/lab8/list')

@lab8.route('/lab8/public_list')
def public_list():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM articles WHERE public=1;")
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab8/public_articles.html', articles=articles)


@lab8.route('/lab8/toggle_favorite/<int:id>', methods=['POST'])
def toggle_favorite(id):
    conn, cur = db_connect()
    cur.execute("SELECT is_favorite FROM articles WHERE id=?", (id,))
    article = cur.fetchone()

    new_value = 1 if article['is_favorite'] == 0 else 0
    cur.execute("UPDATE articles SET is_favorite=? WHERE id=?", (new_value, id))
    db_close(conn, cur)
    return redirect('/lab8/list')


@lab8.route('/lab8/toggle_public/<int:id>', methods=['POST'])
def toggle_public(id):
    conn, cur = db_connect()
    cur.execute("SELECT is_public FROM articles WHERE id=?;", (id,))
    is_public = cur.fetchone()["is_public"]

    new_public_status = 0 if is_public else 1  # 0 - приватная, 1 - публичная
    cur.execute("UPDATE articles SET is_public=? WHERE id=?;", (new_public_status, id))
    
    db_close(conn, cur)
    return redirect('/lab8/list')


@lab8.route('/lab8/like_article/<int:id>', methods=['POST'])
def like_article(id):
    conn, cur = db_connect()

    # Получение текущего состояния лайка
    cur.execute("SELECT likes FROM articles WHERE id=?", (id,))
    article = cur.fetchone()
    
    if article:
        new_likes = 1 if article['likes'] == 0 else 0  # Инверсируем состояние лайка (допоскаем только два состояния)
        cur.execute("UPDATE articles SET likes=? WHERE id=?", (new_likes, id))

    db_close(conn, cur)
    return redirect('/lab8/public_list')


