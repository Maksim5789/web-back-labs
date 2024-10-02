from flask import Blueprint, redirect, url_for, render_template, request
lab2 = Blueprint('lab2',__name__)

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/a/')
def a():
    return render_template('slash.html', message = 'Со слэшем')          
   
@lab2.route('/lab2/a')
def a2():
    return render_template('slash.html', message = 'Без слэша') 

flower_list_with_prices = [
        {'name': 'роза', 'price': 10.99},
        {'name': 'тюльпан', 'price': 5.99},
        {'name': 'незабудка', 'price': 3.99},
        {'name': 'ромашка', 'price': 2.99}
    ]

@lab2.route('/lab2/flowers/', defaults={'flower_id': None})
@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id is None:
        return render_template('flower_id.html', message='Введите id цветка в строку URL')
    elif flower_id < 0 or flower_id >= len(flower_list_with_prices):
        return render_template('flower_id.html', message='Такого цветка нет. Введите правильный id в строку URL'), 404
    else:
        return render_template('flower_id.html', name=flower_list_with_prices[flower_id]['name']), 200


@lab2.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        if any(f['name'].lower() == name.lower() for f in flower_list_with_prices):
            return render_template('add_flower.html', message=f'Цветок "{name}" уже существует', flower_list_with_prices=flower_list_with_prices)
        flower_list_with_prices.append({'name': name, 'price': price})
        return redirect(url_for('lab2.flower_amount'))
    return render_template('add_flower.html', flower_list_with_prices=flower_list_with_prices)

@lab2.route('/lab2/delete_flower/<int:flower_id>', methods=['GET'])
def delete_flower(flower_id):
    if flower_id >= len(flower_list_with_prices) or flower_id < 0:
        return 'Цветок с таким номером не найден', 404
    
    del flower_list_with_prices[flower_id]
    return redirect(url_for('lab2.flower_amount'))

@lab2.route('/lab2/delete_all_flowers/')
def delete_all_flowers():
    flower_list_with_prices.clear()
    return redirect(url_for('lab2.flower_amount'))

@lab2.route('/lab2/flower_amount/')
def flower_amount():
    return render_template('flower_amount.html', 
                           total=len(flower_list_with_prices),
                           flower_list_with_prices=flower_list_with_prices)

@lab2.route('/lab2/reset_flowers/')
def reset_flowers():
    global flower_list_with_prices
    flower_list_with_prices = []
    return render_template('reset_flowers.html', message='Список цветов сброшен')

@lab2.route('/lab2/example')
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

@lab2.route('/lab2/filters/')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@lab2.route('/lab2/calc/', defaults={'a': 1, 'b': 1})
@lab2.route('/lab2/calc/<int:a>/', defaults={'b': 1})
@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calculator(a, b):
    result = {
        'Сумма': a + b,
        'Вычитание': a - b,
        'Умножение': a * b,
        'Деление': a / b,
        'Возведение в степень': a ** b
    }
    return render_template('calculator.html', a=a, b=b, result=result)

@lab2.route('/lab2/calc/')
def redirect_to_default():
    return redirect(url_for('calculator', a=1, b=1))

@lab2.route('/lab2/calc/<int:a>/')
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

@lab2.route('/lab2/books/')
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

@lab2.route('/lab2/objects/')
def show_objects():
    return render_template('objects.html', objects=objects)


