from flask import Blueprint, redirect, url_for, render_template, request, make_response
lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get ('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color)

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
                                         color=request.cookies.get('color'), 
                                         color_back=request.cookies.get('color_back'),
                                         font_size=request.cookies.get('font_size'),
                                         font_style=request.cookies.get('font_style')))
    
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

    
  