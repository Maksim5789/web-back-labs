from flask import Blueprint, redirect, url_for, render_template, request, make_response
lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get ('name') or "аноним"
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age') or "неизвестный"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = "Заполните поле!"
    age = request.args.get('age')
    if age == '':
        errors['age'] = "Заполните поле!"
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит - 120 рублей, чёрный чай - 80 рублей, зелёный чай - 70 рублей.
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удорожает напиток на 30 рублей, а сахара - на 10
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')  # Получаем цену из параметров URL
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    # Получаем параметры из запроса
    color = request.args.get('color')
    color_back = request.args.get('color_back')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    resp = make_response(render_template('lab3/settings.html', 
                                         color=request.cookies.get('color', 'black'), 
                                         color_back=request.cookies.get('color_back', '#659DBD'),
                                         font_size=request.cookies.get('font_size', '20px'),
                                         font_style=request.cookies.get('font_style', 'Arial')))
    
    # Устанавливаем куки, если параметры переданы
    if color:
        resp.set_cookie('color', color)
    if color_back:
        resp.set_cookie('color_back', color_back)
    if font_size:
        resp.set_cookie('font_size', font_size)
    if font_style:
        resp.set_cookie('font_style', font_style)
        
    return resp

@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))  # Переход на главную страницу настроек
    
    # Очищаем куки
    resp.set_cookie('color', 'black', expires=0)
    resp.set_cookie('color_back', '#659DBD', expires=0)
    resp.set_cookie('font_size', '20px', expires=0)
    resp.set_cookie('font_style', 'Arial', expires=0)
    
    return resp

# Два раза нажимаем на ОК, чтобы потом код брал данные из куки, а потом можно очистить (вернуть к настройкам по умолчанию)


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        fio = request.form.get('fio')
        shelf = request.form.get('shelf')
        linen = 'linen' in request.form
        baggage = 'baggage' in request.form
        age = request.form.get('age')
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        travel_date = request.form.get('date')
        insurance = 'insurance' in request.form

        # Проверка на пустые поля
        if not (fio and shelf and age and departure and destination and travel_date):
            return "Все поля должны быть заполнены!", 400
        
        # Проверка на возраст
        try:
            age = int(age)
        except ValueError:
            return "Возраст должен быть числом!", 400
        
        if age < 1 or age > 120:
            return "Возраст должен быть от 1 до 120 лет!", 400

        # Расчет стоимости билета
        price = 1000 if age >= 18 else 700
        if shelf in ['lower', 'lower_side']:
            price += 100
        if linen:
            price += 75
        if baggage:
            price += 250
        if insurance:
            price += 150

        ticket_type = "Детский билет" if age < 18 else "Взрослый билет"

        return render_template('lab3/ticket.html', fio=fio, shelf=shelf, age=age,
                               departure=departure, destination=destination,
                               travel_date=travel_date, insurance=insurance,
                               price=price, ticket_type=ticket_type)

    # Если метод GET, просто возвращаем форму
    return render_template('lab3/form.html')


# Пример списка книг
books = [
    {'title': 'Книга 1', 'price': 500, 'author': 'Автор 1', 'genre': 'Фантастика'},
    {'title': 'Книга 2', 'price': 1000, 'author': 'Автор 2', 'genre': 'Фантастика'},
    {'title': 'Книга 3', 'price': 1500, 'author': 'Автор 3', 'genre': 'Драма'},
    {'title': 'Книга 4', 'price': 2000, 'author': 'Автор 4', 'genre': 'Приключения'},
    {'title': 'Книга 5', 'price': 2500, 'author': 'Автор 5', 'genre': 'Научная фантастика'},
    {'title': 'Книга 6', 'price': 3000, 'author': 'Автор 6', 'genre': 'Триллер'},
    {'title': 'Книга 7', 'price': 3500, 'author': 'Автор 7', 'genre': 'Ужасы'},
    {'title': 'Книга 8', 'price': 4000, 'author': 'Автор 8', 'genre': 'История'},
    {'title': 'Книга 9', 'price': 4500, 'author': 'Автор 9', 'genre': 'Поэзия'},
    {'title': 'Книга 10', 'price': 5000, 'author': 'Автор 10', 'genre': 'Биография'},
    {'title': 'Книга 11', 'price': 5500, 'author': 'Автор 11', 'genre': 'Эссе'},
    {'title': 'Книга 12', 'price': 6000, 'author': 'Автор 12', 'genre': 'Фантастика'},
    {'title': 'Книга 13', 'price': 6500, 'author': 'Автор 13', 'genre': 'Драма'},
    {'title': 'Книга 14', 'price': 7000, 'author': 'Автор 14', 'genre': 'Приключения'},
    {'title': 'Книга 15', 'price': 7500, 'author': 'Автор 15', 'genre': 'Научная фантастика'},
    {'title': 'Книга 16', 'price': 8000, 'author': 'Автор 16', 'genre': 'Триллер'},
    {'title': 'Книга 17', 'price': 8500, 'author': 'Автор 17', 'genre': 'Ужасы'},
    {'title': 'Книга 18', 'price': 9000, 'author': 'Автор 18', 'genre': 'История'},
    {'title': 'Книга 19', 'price': 9500, 'author': 'Автор 19', 'genre': 'Поэзия'},
    {'title': 'Книга 20', 'price': 10000, 'author': 'Автор 20', 'genre': 'Биография'},
]

@lab3.route('/lab3/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        min_price = request.form.get('min_price', type=int)
        max_price = request.form.get('max_price', type=int)
        filtered_books = [book for book in books if min_price <= book['price'] <= max_price]
        return render_template('lab3/results.html', books=filtered_books)
    return render_template('lab3/search.html')








