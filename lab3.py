from flask import Blueprint, redirect, url_for, render_template, request
lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    return render_template('lab3.html')

@lab3.route('/lab3/cookie')
def cookie():
    return 'Установка cookie', 200, {'Set-Cookie': 'name=Alex'}