from flask import Flask, url_for, redirect, Response, render_template, request
from lab1 import lab1

app = Flask (__name__)
app.register_blueprint(lab1)


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
###
#@app.errorhandler(Exception)
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


   
@app.route('/lab2/a/')
def a():
    return render_template('slash.html', message = 'Со слэшем')          
   
@app.route('/lab2/a')
def a2():
    return render_template('slash.html', message = 'Без слэша') 

flower_list_with_prices = [
        {'name': 'роза', 'price': 10.99},
        {'name': 'тюльпан', 'price': 5.99},
        {'name': 'незабудка', 'price': 3.99},
        {'name': 'ромашка', 'price': 2.99}
    ]

@app.route('/lab2/flowers/', defaults={'flower_id': None})
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id is None:
        return render_template('flower_id.html', message='Введите id цветка в строку URL')
    elif flower_id < 0 or flower_id >= len(flower_list_with_prices):
        return render_template('flower_id.html', message='Такого цветка нет. Введите правильный id в строку URL'), 404
    else:
        return render_template('flower_id.html', name=flower_list_with_prices[flower_id]['name']), 200


@app.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        if any(f['name'].lower() == name.lower() for f in flower_list_with_prices):
            return render_template('add_flower.html', message=f'Цветок "{name}" уже существует', flower_list_with_prices=flower_list_with_prices)
        flower_list_with_prices.append({'name': name, 'price': price})
        return redirect(url_for('flower_amount'))
    return render_template('add_flower.html', flower_list_with_prices=flower_list_with_prices)

@app.route('/lab2/delete_flower/<int:flower_id>', methods=['GET'])
def delete_flower(flower_id):
    if flower_id >= len(flower_list_with_prices) or flower_id < 0:
        return 'Цветок с таким номером не найден', 404
    
    del flower_list_with_prices[flower_id]
    return redirect(url_for('flower_amount'))

@app.route('/lab2/delete_all_flowers/')
def delete_all_flowers():
    flower_list_with_prices.clear()
    return redirect(url_for('flower_amount'))



@app.route('/lab2/flower_amount/')
def flower_amount():
    return render_template('flower_amount.html', 
                           total=len(flower_list_with_prices),
                           flower_list_with_prices=flower_list_with_prices)

@app.route('/lab2/reset_flowers/')
def reset_flowers():
    global flower_list_with_prices
    flower_list_with_prices = []
    return render_template('reset_flowers.html', message='Список цветов сброшен')


@app.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Акишин Максим', 2, 22, 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
        ]
    return render_template('example.html', 
                           name=name, lab_num=lab_num, group=group, course=course, fruits=fruits)


@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')


@app.route('/lab2/filters/')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/', defaults={'a': 1, 'b': 1})
@app.route('/lab2/calc/<int:a>/', defaults={'b': 1})
@app.route('/lab2/calc/<int:a>/<int:b>')
def calculator(a, b):
    result = {
        'Сумма': a + b,
        'Вычитание': a - b,
        'Умножение': a * b,
        'Деление': a / b,
        'Возведение в степень': a ** b
    }
    return render_template('calculator.html', a=a, b=b, result=result)

@app.route('/lab2/calc/')
def redirect_to_default():
    return redirect(url_for('calculator', a=1, b=1))

@app.route('/lab2/calc/<int:a>/')
def redirect_to_default_b(a):
    return redirect(url_for('calculator', a=a, b=1))


# Данные о книгах
books = [
    {
        'author': 'Джордж Оруэлл',
        'title': 'Скотный двор',
        'genre': 'Антиутопия',
        'pages': 112
    },
    {
        'author': 'Эрих Мария Ремарк',
        'title': 'Триумфальная арка',
        'genre': 'Роман',
        'pages': 544
    },
    {
        'author': 'Эрих Мария Ремарк',
        'title': 'Триумфальная арка',
        'genre': 'Роман',
        'pages': 544
    },
    {
        'author': 'Артур Конан Дойл',
        'title': 'Собака Баскервилей',
        'genre': 'Детектив',
        'pages': 240
    },
    {
        'author': 'Джон Рональд Руэл Толкин',
        'title': 'Властелин колец',
        'genre': 'Фэнтези',
        'pages': 1178
    },
    {
        'author': 'Агата Кристи',
        'title': 'Убийство в "Восточном экспрессе"',
        'genre': 'Детектив',
        'pages': 256
    },
    {
        'author': 'Рэй Брэдбери',
        'title': 'Марсианские хроники',
        'genre': 'Научная фантастика',
        'pages': 288
    },
    {
        'author': 'Харпер Ли',
        'title': 'Убить пересмешника',
        'genre': 'Роман',
        'pages': 320
    },
    {
        'author': 'Маргарет Митчелл',
        'title': 'Унесенные ветром',
        'genre': 'Исторический роман',
        'pages': 1037
    },
    {
        'author': 'Уильям Голдинг',
        'title': 'Повелитель мух',
        'genre': 'Роман',
        'pages': 288
    },
    {
        'author': 'Альбер Камю',
        'title': 'Посторонний',
        'genre': 'Роман',
        'pages': 123
    }
]

@app.route('/lab2/books/')
def show_books():
    return render_template('books.html', books=books)

objects = [
    {
        'name': 'Андрей Первозванный. 1912',
        'image': 'Андрей Первозванный. 1912.jpg',
        'description': 'Андрей Первозванный — эскадренный броненосец типа «Андрей Первозванный», с 10.10.1907 г. — линейный корабль («преддредноутного типа») русского флота. Заложен 28 апреля 1905 года на Адмиралтейском судостроительном заводе (г. Санкт-Петербург), конструктор — корабельный инженер Скворцов. Спущен на воду 7 октября 1906 года, вступил в строй в мае 1912 года.'
    },
    {
        'name': 'Бородино. 1904',
        'image': 'Бородино. 1904.jpg',
        'description': 'Броненосцы типа «Бородино» — серия эскадренных броненосцев Российского императорского флота строившихся в период с 1901 по 1905 из пяти кораблей: «Бородино», «Император Александр III», «Орёл», «Князь Суворов», «Слава». Самая крупная серия русских броненосцев — «Бородино», была создана в рамках кораблестроительной программы «Для нужд Дальнего Востока» 1898—1905 годов.'
    },
    {
        'name': 'Гангут. 1915',
        'image': 'Гангут. 1915.jpg',
        'description': '«Гангут» (с 1925 года «Октя́брьская револю́ция») — линкор русского и советского флота, последний (по дате закладки и дате спуска на воду) из четырёх дредноутов балтийской серии типа «Севастополь». Линкор-дредноут «Гангут» стал четвёртым кораблём русского флота, названным в честь победы в Гангутском сражении.'
    },
    {
        'name': 'Евстафий. 1914',
        'image': 'Евстафий. 1914.jpg',
        'description': '«Евстафий» — русский линкор додредноутного типа. Головной корабль серии броненосцев типа «Евстафий» (1911—1919). Во время Первой мировой войны — флагман Черноморского флота.'
    },
    {
        'name': 'Император Павел I',
        'image': 'Император Павел I.jpg',
        'description': '«Император Павел I» (после 19 апреля 1917 года — «Республика») — российский эскадренный броненосец типа «Андрей Первозванный».'
    }
]

@app.route('/lab2/objects/')
def show_objects():
    return render_template('objects.html', objects=objects)



