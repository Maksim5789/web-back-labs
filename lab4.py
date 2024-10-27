from flask import Blueprint, redirect, url_for, render_template, request, make_response, session, flash
lab4 = Blueprint('lab4',__name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error = 'Я запрещаю вам делить на ноль!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/add-form')
def add_form():
    return render_template('lab4/add-form.html')

@lab4.route('/lab4/add', methods=['POST'])
def add():
    x1 = request.form.get('x1')  
    x2 = request.form.get('x2')  
    # Преобразуем в 0, если пустая строка
    if x1 == '':
        x1 = 0
    else:
        x1 = int(x1)
    
    if x2 == '':
        x2 = 0
    else:
        x2 = int(x2)

    result = x1 + x2
    return render_template('lab4/add.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/multiply-form')
def multiply_form():
    return render_template('lab4/multiply-form.html')

@lab4.route('/lab4/multiply', methods=['POST'])
def multiply():
    x1 = request.form.get('x1')  
    x2 = request.form.get('x2')  

    # Преобразуем в 1, если пустая строка
    if x1 == '':
        x1 = 1
    else:
        x1 = int(x1)
    
    if x2 == '':
        x2 = 1
    else:
        x2 = int(x2)

    result = x1 * x2
    return render_template('lab4/multiply.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/subtract-form')
def subtract_form():
    return render_template('lab4/subtract-form.html')

@lab4.route('/lab4/subtract', methods=['POST'])
def subtract():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/subtract.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/subtract.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/power-form')
def power_form():
    return render_template('lab4/power-form.html')

@lab4.route('/lab4/power', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/power.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/power.html', error='0 в степени 0 определено как неопределенность!')

    result = x1 ** x2
    return render_template('lab4/power.html', x1=x1, x2=x2, result=result)

tree_count = 0
max = 10  # Максимальное количество деревьев

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=max)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:  # Проверка на положительное значение
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < max:  # Проверка на максимальное значение
            tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб', 'gender': 'male'},
    {'login': 'michael', 'password': '777', 'name': 'Майкл', 'gender': 'male'},
    {'login': 'gabriel', 'password': '888', 'name': 'Габриэль', 'gender': 'male'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            name = session['name']
        else:
            authorized = False
            name = ''
        return render_template('lab4/login.html', authorized=authorized, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')
    error = None

    if not login:
        error = 'Не введён логин и/или пароль'
    elif not password:
        error = 'Не введён логин и/или пароль'
    else:
        for user in users:
            if login == user['login'] and password == user['password']:
                session['login'] = login
                session['name'] = user['name']  # Сохраняем имя пользователя
                return redirect('/lab4/login')

        error = 'Неверные логин и/или пароль'

    return render_template('lab4/login.html', error=error, authorized=False, login=login) #password=password)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = None
    temperature = None

    if request.method == 'POST':
        temp_input = request.form.get('temperature')
        
        if temp_input is None or temp_input.strip() == "":
            message = "Ошибка: не задана температура"
        else:
            try:
                temperature = float(temp_input)
                
                if temperature < -12:
                    message = "Не удалось установить температуру — слишком низкое значение"
                elif temperature > -1:
                    message = "Не удалось установить температуру — слишком высокое значение"
                elif -12 <= temperature <= -9:
                    message = f"Установлена температура: {temperature}°C ❄️❄️❄️"
                elif -8 <= temperature <= -5:
                    message = f"Установлена температура: {temperature}°C ❄️❄️"
                elif -4 <= temperature <= -1:
                    message = f"Установлена температура: {temperature}°C ❄️"

            except ValueError:
                message = "Ошибка: температура должна быть числом"

    return render_template('/lab4/fridge.html', message=message, temperature=temperature)


# Определим цены на зерно
prices = {
    'ячмень': 12345,
    'овёс': 8522,
    'пшеница': 8722,
    'рожь': 14111
}

@lab4.route('/lab4/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')

        # Проверка на пустое значение веса
        if not weight:
            flash('Ошибка: вес не был указан.', 'error')
            return render_template('/lab4/order.html')

        try:
            weight = float(weight)
        except ValueError:
            flash('Ошибка: введите корректное значение веса.', 'error')
            return render_template('/lab4/order.html')

        # Проверка на отрицательные значения
        if weight <= 0:
            flash('Ошибка: вес должен быть больше 0.', 'error')
            return render_template('/lab4/order.html')

        # Проверка на наличие зерна
        if weight > 500:
            flash('Ошибка: такого объёма сейчас нет в наличии.', 'error')
            return render_template('/lab4/order.html')

        # Рассчитываем сумму заказа
        price_per_ton = prices.get(grain_type)

        if price_per_ton is None:
            flash('Ошибка: некорректный тип зерна.', 'error')
            return render_template('/lab4/order.html')

        total_amount = price_per_ton * weight

        # Применение скидки при большом объёме
        discount = 0
        if weight > 50:
            discount = total_amount * 0.1
            total_amount -= discount

        # Формируем сообщение
        message = f'Заказ успешно сформирован. Вы заказали {grain_type}. Вес: {weight} т. Сумма к оплате: {total_amount:.2f} руб.'
        
        if discount > 0:
            message += f' Применена скидка за большой объём: {discount:.2f} руб.'

        flash(message, 'success')
        return render_template('/lab4/order.html')

    return render_template('/lab4/order.html')
