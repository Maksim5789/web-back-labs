from flask import Flask, url_for, redirect, Response, render_template, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz

import os
from os import path
from db import db 
from db.models import users
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'маню_ня_ня_ни_ни').encode('utf-8')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

# Настройки базы данных
db_name = 'lab8'
host_ip = '127.0.0.1'
host_port = 5432
db_type = 'sqlite'  # Установите 'postgres' для использования PostgreSQL

# Установка конфигурации для SQLAlchemy
if db_type == 'postgres':
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://username:password@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "lab8.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Инициализация db с приложением
db.init_app(app)


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)


@app.route ("/")
@app.route ("/index")
def main():
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>НГТУ, ФБ, Лабораторные работы</title>   
            </head>
 
            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
                    <hr>
                </header>
                
                <div style="text-align: center; margin: 20px;">
                <h1>Список работ</h1>
                <a href="/lab1">Первая лабораторная работа</a>
                <p> </p>
                <a href="/lab2/">Вторая лабораторная работа</a>          
                <p> </p>
                <a href="/lab3/">Третья лабораторная работа</a>
                <p> </p>
                <a href="/lab4/">Четвёртая лабораторная работа</a>
                <p> </p>
                <a href="/lab5/">Пятая лабораторная работа</a>
                <p> </p>
                <a href="/lab6/">Шестая лабораторная работа</a>
                <p> </p>
                <a href="/lab7/">Седьмая лабораторная работа</a>
                <p> </p>
                <a href="/lab8/">Восьмая лабораторная работа</a>
                <p> </p>
                <a href="/lab9/">Девятая лабораторная работа</a>
                <p> </p>
                <a href="/rgz/">Расчётно-графическое задание</a>
                </div>
                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>   
            </body>
        </html>'''

@app.errorhandler(404)
def not_found(error):
    path = url_for("static", filename="404.jpg")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Ошибка 404</title>
                <style>
                    img {
                        width: 700px;
                        height: 400px;
                        margin: 20px;
                        border: 5px solid black;
                    }
                </style>   
            </head>
 
            <body>
                <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 404</h1>

                <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
                    К сожалению, страница, которую вы ищете, не существует или перемещена. Пожалуйста, проверьте правильность написания адреса и попробуйте снова.
                </div>

                <div style="text-align: center;">
                    <img src="''' + path + '''">
                </div>
            </body>
        </html>''', 404

@app.route('/400')
def error_400():
    path = url_for("static", filename="400.png")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Ошибка 400</title>
                <style>
                    img {
                        width: 700px;
                        height: 400px;
                        margin: 20px;
                        border: 5px solid black;
                    }
                </style>   
            </head>
 
            <body>
                <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 400</h1>

                <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
                    Запрос к серверу содержит синтаксическую ошибку.
                </div>

                <div style="text-align: center;">
                    <img src="''' + path + '''">
                </div>
            </body>
        </html>''', 400

@app.route('/401')
def error_401():
    path = url_for("static", filename="401.jpg")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Ошибка 401</title>
                <style>
                    img {
                        width: 700px;
                        height: 400px;
                        margin: 20px;
                        border: 5px solid black;
                    }
                </style>   
            </head>
 
            <body>
                <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 401</h1>

                <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
                    Не авторизован.
                </div>

                <div style="text-align: center;">
                    <img src="''' + path + '''">
                </div>
            </body>
        </html>''', 401

@app.route('/402')
def error_402():
    path = url_for("static", filename="402.jpg")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Ошибка 402</title>
                <style>
                    img {
                        width: 700px;
                        height: 400px;
                        margin: 20px;
                        border: 5px solid black;
                    }
                </style>   
            </head>
 
            <body>
                <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 402</h1>

                <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
                    Необходима оплата.
                </div>

                <div style="text-align: center;">
                    <img src="''' + path + '''">
                </div>
            </body>
        </html>''', 402

@app.route('/403')
def error_403():
    path = url_for("static", filename="403.jpg")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Ошибка 403</title>
                <style>
                    img {
                        width: 600px;
                        height: 400px;
                        margin: 20px;
                        border: 5px solid black;
                    }
                </style>   
            </head>
 
            <body>
                <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 403</h1>

                <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
                    Запрещено (отказано в доступе).
                </div>

                <div style="text-align: center;">
                    <img src="''' + path + '''">
                </div>
            </body>
        </html>''', 403

@app.route('/405')
def error_405():
    path = url_for("static", filename="405.jpg")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Ошибка 405</title>
                <style>
                    img {
                        width: 700px;
                        height: 400px;
                        margin: 20px;
                        border: 5px solid black;
                    }
                </style>   
            </head>
 
            <body>
                <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 405</h1>

                <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
                    Метод не поддерживается.
                </div>

                <div style="text-align: center;">
                    <img src="''' + path + '''">
                </div>
            </body>
        </html>''', 405

@app.route('/418')
def error_418():
    path = url_for("static", filename="418.jpg")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Ошибка 418</title>
                <style>
                    img {
                        width: 700px;
                        height: 400px;
                        margin: 20px;
                        border: 5px solid black;
                    }
                </style>   
            </head>
 
            <body>
                <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 418</h1>

                <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
                    Я чайник.
                </div>

                <div style="text-align: center;">
                    <img src="''' + path + '''">
                </div>
            </body>
        </html>''', 418

# @app.errorhandler(Exception)
# def internal_server_error(error):
#     path = url_for("static", filename="500.png")
#     css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
#     return '''<!DOCTYPE html>
#         <html>
#             <head>
#                 <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
#                 <title>Ошибка 500</title>
#                 <style>
#                     img {
#                         width: 700px;
#                         height: 400px;
#                         margin: 20px;
#                         border: 5px solid black;
#                     }
#                 </style>   
#             </head>
 
#             <body>
#                 <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 500</h1>

#                 <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
#                     Извините, произошла непредвиденная ошибка. Повторите попытку позже.
#                 </div>

#                 <div style="text-align: center;">
#                     <img src="''' + path + '''">
#                 </div>
#             </body>
#         </html>''', 500

@app.route('/500')
def index500():
# Генерируем ошибку деления на ноль
    1 / 0


   

