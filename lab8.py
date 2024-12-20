from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, flash
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy.exc import IntegrityError

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
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember')  # Получаем значение галочки

    if not (login_form and password_form):
        return render_template('lab8/login.html', error='Заполните поля')
    
    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=bool(remember))  # Устанавливаем remember
            return redirect('/lab8/')
    
    return render_template('/lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')


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
    
    # Автоматический логин после регистрации
    login_user(new_user, remember=False)  # Добавлено для автоматического входа
    
    return redirect('/lab8/')


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required # Добавляем декоратор для авторизации
def create():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # Валидация пустых полей
    if not title or not article_text:
        return render_template('lab8/create_article.html', error='Название и текст статьи не могут быть пустыми.')

    try:
        new_article = articles(login_id=current_user.id, title=title, article_text=article_text) # Используем current_user
        db.session.add(new_article)
        db.session.commit()
        return redirect('/lab8')
    except IntegrityError as e:
        db.session.rollback() # Отмена транзакции в случае ошибки
        return render_template('lab8/create_article.html', error=f'Ошибка при создании статьи: {e}')  #Обработка ошибки
    except Exception as e:
        db.session.rollback() # Отмена транзакции в случае ошибки
        return render_template('lab8/create_article.html', error=f'Произошла неизвестная ошибка: {e}')  #Обработка ошибки


@lab8.route('/lab8/personal_articles/')
@login_required
def personal_articles():
    # Доступ к статьям, связанным с текущим пользователем
    articles = current_user.articles
    return render_template('lab8/personal_articles.html', articles=articles)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/edit/<int:id>', methods=['GET', 'POST'])
@login_required  # Проверка, что пользователь авторизован
def edit(id):
    article = articles.query.get_or_404(id)  # Получаем статью по ID или возвращаем 404 ошибку

    # Проверка, является ли текущий пользователь автором статьи
    if article.login_id != current_user.id:  
        flash('У Вас нет прав на редактирование этой статьи.', 'error')  # Используем flash для вывода ошибки
        return redirect(url_for('lab8.personal_articles'))  # Перенаправляем на страницу со статьями

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)  # Отображаем форму редактирования

    title = request.form.get('title')  # Получаем название статьи из формы
    article_text = request.form.get('article_text')  # Получаем текст статьи из формы

    # Валидация: проверяем, что поля не пустые
    if not title or not article_text:
        return render_template('lab8/edit_article.html', article=article, error='Название и текст статьи не могут быть пустыми.')

    # Обновляем поля статьи
    article.title = title
    article.article_text = article_text  # Исправлено: используем правильное имя поля
    db.session.commit()  # Сохраняем изменения в базе данных

    return redirect(url_for('lab8.personal_articles'))  


 

@lab8.route('/lab8/delete/<int:id>', methods=['POST'])
@login_required  # Проверка, что пользователь авторизован
def delete(id):
    article = articles.query.get_or_404(id)  # Получаем статью по ID или возвращаем 404 ошибку

    # Проверка, является ли текущий пользователь автором статьи
    if article.login_id != current_user.id:
        flash('У Вас нет прав на удаление этой статьи.', 'error')  # Используем flash для вывода ошибки
        return redirect(url_for('lab8.personal_articles'))  # Перенаправляем на страницу со статьями

    db.session.delete(article)  # Удаляем статью
    db.session.commit()  # Сохраняем изменения в базе данных

    flash('Статья успешно удалена.', 'success')  # Сообщение об успешном удалении
    return redirect(url_for('lab8.personal_articles'))  # Перенаправляем на страницу со статьями


@lab8.route('/lab8/public_articles/')
@login_required
def public_articles():
    # Получение статей для текущего пользователя
    articles = current_user.articles  # articles определены в модели users
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


