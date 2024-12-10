from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, jsonify, flash, abort
import sqlite3
from os import path
from datetime import datetime
import shortuuid

lab7 = Blueprint('lab7', __name__)

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

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify([dict(film) for film in films])

@lab7.route('/lab7/rest-api/films/<string:id>', methods=['GET'])
def get_film(id):
    print(f"Fetching film with id: {id}")  # Отладочное сообщение
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    db_close(conn, cur)

    if film is None:
        print(f"Film with id {id} not found")  # Отладочное сообщение
        abort(404)

    print(f"Film found: {film}")  # Отладочное сообщение
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<string:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = ?", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # Проверка названий
    title = film.get('title', '').strip()
    title_ru = film.get('title_ru', '').strip()
    
    if not title and not title_ru:
        return {'title': 'Заполните оригинальное название'}, 400
    
    if not title and title_ru:
        film['title'] = title_ru
    
    if not title_ru and title:
        return {'title_ru': 'Заполните русское название'}, 400
    
    # Проверка года
    year = film.get('year')
    if not year or not isinstance(year, int) or year < 1895 or year > datetime.now().year:
        return {'year': f'Год должен быть от 1895 до {datetime.now().year}'}, 400
    
    # Проверка описания
    description = film.get('description', '').strip()
    if not description or len(description) > 2000:
        return {'description': 'Описание должно быть непустым и не более 2000 символов'}, 400
    
    # Генерация уникального ID
    film_id = shortuuid.uuid()[:8]  # Генерируем короткий UUID

    # Проверка на уникальность ID
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = ?", (film_id,))
    existing_film = cur.fetchone()
    
    if existing_film:
        return {'id': 'Сгенерированный ID уже существует. Попробуйте снова.'}, 400

    # Проверка на существующее русское название
    cur.execute("SELECT * FROM films WHERE title_ru = ?", (title_ru,))
    existing_film_ru = cur.fetchone()
    if existing_film_ru:
        return {'title_ru': 'Фильм с таким русским названием уже существует'}, 400

    # Проверка на существующее оригинальное название
    cur.execute("SELECT * FROM films WHERE title = ?", (title,))
    existing_film_title = cur.fetchone()
    if existing_film_title:
        return {'title': 'Фильм с таким оригинальным названием уже существует'}, 400

    # Добавляем фильм в базу данных
    cur.execute("INSERT INTO films (id, title, title_ru, year, description) VALUES (?, ?, ?, ?, ?)",
                (film_id, film['title'], film['title_ru'], film['year'], film['description']))
    db_close(conn, cur)
    
    return {'id': film_id}, 201

@lab7.route('/lab7/rest-api/films/<string:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    # Проверка существования фильма с таким ID
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    existing_film = cur.fetchone()
    
    if not existing_film:
        return {'id': 'Фильм с таким ID не существует'}, 404

    # Проверка названий
    title = film.get('title', '').strip()
    title_ru = film.get('title_ru', '').strip()
    
    if not title and not title_ru:
        return {'title': 'Заполните оригинальное название'}, 400
    
    if not title and title_ru:
        film['title'] = title_ru
    
    if not title_ru and title:
        return {'title_ru': 'Заполните русское название'}, 400
    
    # Проверка года
    year = film.get('year')
    if not year or not isinstance(year, int) or year < 1895 or year > datetime.now().year:
        return {'year': f'Год должен быть от 1895 до {datetime.now().year}'}, 400
    
    # Проверка описания
    description = film.get('description', '').strip()
    if not description or len(description) > 2000:
        return {'description': 'Описание должно быть непустым и не более 2000 символов'}, 400
    
    # Проверка на существующее русское название (исключая текущий фильм)
    cur.execute("SELECT * FROM films WHERE title_ru = ? AND id != ?", (title_ru, id))
    existing_film_ru = cur.fetchone()
    if existing_film_ru:
        return {'title_ru': 'Фильм с таким русским названием уже существует'}, 400

    # Проверка на существующее оригинальное название (исключая текущий фильм)
    cur.execute("SELECT * FROM films WHERE title = ? AND id != ?", (title, id))
    existing_film_title = cur.fetchone()
    if existing_film_title:
        return {'title': 'Фильм с таким оригинальным названием уже существует'}, 400

    # Обновляем фильм в базе данных
    cur.execute("UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?",
                (film['title'], film['title_ru'], film['year'], film['description'], id))
    db_close(conn, cur)
    
    return jsonify(film), 200