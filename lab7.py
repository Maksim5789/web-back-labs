from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, jsonify, flash, abort
import sqlite3
from os import path
import hashlib
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

films = [
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "A skilled thief is given a final chance to redeem himself by performing an impossible heist: infiltrating dreams to steal valuable secrets."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Two imprisoned men bond over several years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Темный рыцарь",
        "year": 2008,
        "description": "Batman sets out to dismantle the remaining criminal organizations that plague Gotham, facing the formidable Joker who seeks to undermine Batman's influence."
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    # Проверка на корректность id
    if id < 0 or id >= len(films):
        abort(404)  # Возвращаем ошибку 404, если id выходит за пределы
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    # Проверка на корректность id
    if id < 0 or id >= len(films):
        abort(404)  # Возвращаем ошибку 404, если id выходит за пределы
    del films[id]
    return '', 204  # Возвращаем статус 204 No Content

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    # Проверка на корректность id
    if id < 0 or id >= len(films):
        abort(404)  # Возвращаем ошибку 404, если id выходит за пределы
    
    film = request.get_json()  # Получаем данные из запроса
    
    # Проверка названий
    title = film.get('title', '').strip()  # Убираем лишние пробелы, если поле отсутствует, используем пустую строку
    title_ru = film.get('title_ru', '').strip()  # Убираем лишние пробелы, если поле отсутствует, используем пустую строку
    
    # Если оба названия пустые
    if not title and not title_ru:
        return {'title': 'Заполните оригинальное название'}, 400
    
    # Если пустое только оригинальное название, заполняем его значением из русского названия
    if not title and title_ru:
        film['title'] = title_ru
    
    # Если пустое русское название, а оригинальное заполнено
    if not title_ru and title:
        return {'title_ru': 'Заполните русское название'}, 400
    
    # Проверка года
    year = film.get('year')
    if not year or not isinstance(year, int) or year < 1895 or year > datetime.now().year:
        return {'year': f'Год должен быть от 1895 до {datetime.now().year}'}, 400
    
    # Проверка описания
    description = film.get('description', '').strip()  # Убираем лишние пробелы, если поле отсутствует, используем пустую строку
    if not description or len(description) > 2000:
        return {'description': 'Описание должно быть непустым и не более 2000 символов'}, 400
    
    # Обновляем фильм в списке
    films[id] = film
    
    # Возвращаем обновленный фильм с кодом 200 OK
    return films[id], 200

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()  # Получаем данные из тела запроса
    
    # Проверка названий
    title = film.get('title', '').strip()  # Убираем лишние пробелы, если поле отсутствует, используем пустую строку
    title_ru = film.get('title_ru', '').strip()  # Убираем лишние пробелы, если поле отсутствует, используем пустую строку
    
    # Если оба названия пустые
    if not title and not title_ru:
        return {'title': 'Заполните оригинальное название'}, 400
    
    # Если пустое только оригинальное название, заполняем его значением из русского названия
    if not title and title_ru:
        film['title'] = title_ru
    
    # Если пустое русское название, а оригинальное заполнено
    if not title_ru and title:
        return {'title_ru': 'Заполните русское название'}, 400
    
    # Проверка года
    year = film.get('year')
    if not year or not isinstance(year, int) or year < 1895 or year > datetime.now().year:
        return {'year': f'Год должен быть от 1895 до {datetime.now().year}'}, 400
    
    # Проверка описания
    description = film.get('description', '').strip()  # Убираем лишние пробелы, если поле отсутствует, используем пустую строку
    if not description or len(description) > 2000:
        return {'description': 'Описание должно быть непустым и не более 2000 символов'}, 400
    
    # Добавляем новый фильм в конец списка
    films.append(film)
    
    # Получаем индекс нового элемента
    new_index = len(films) - 1
    
    # Возвращаем индекс нового элемента с кодом 201 Created
    return {'id': new_index}, 201