from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, jsonify, flash, abort
import sqlite3
from os import path
import hashlib

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
    films[id] = film  # Обновляем фильм в списке
    return films[id], 200  # Возвращаем обновленный фильм с кодом 200 OK