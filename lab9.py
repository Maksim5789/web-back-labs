from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

# Очистка сессии (сброс данных)
@lab9.route('/lab9/reset/')
def reset():
    session.clear()  # Очищаем все данные сессии
    return redirect(url_for('lab9.main'))

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name  # Сохраняем имя в сессии
        return redirect(url_for('lab9.age'))
    
    # Проверяем, есть ли уже данные в сессии
    if 'greeting' in session and 'gift' in session and 'image' in session:
        return render_template('lab9/congratulations.html', greeting=session['greeting'], gift=session['gift'], image=session['image'])
    
    return render_template('lab9/index.html')

@lab9.route('/lab9/age/', methods=['GET', 'POST'])
def age():
    if 'name' not in session:
        return redirect(url_for('lab9.main'))
    
    if request.method == 'POST':
        age = request.form['age']
        session['age'] = age  # Сохраняем возраст в сессии
        return redirect(url_for('lab9.gender'))
    
    return render_template('lab9/age.html', name=session['name'])

@lab9.route('/lab9/gender/', methods=['GET', 'POST'])
def gender():
    if 'name' not in session or 'age' not in session:
        return redirect(url_for('lab9.main'))
    
    if request.method == 'POST':
        gender = request.form['gender']
        session['gender'] = gender  # Сохраняем пол в сессии
        return redirect(url_for('lab9.preference'))
    
    return render_template('lab9/gender.html', name=session['name'], age=session['age'])

@lab9.route('/lab9/preference/', methods=['GET', 'POST'])
def preference():
    if 'name' not in session or 'age' not in session or 'gender' not in session:
        return redirect(url_for('lab9.main'))
    
    if request.method == 'POST':
        preference = request.form['preference']
        session['preference'] = preference  # Сохраняем предпочтение в сессии
        return redirect(url_for('lab9.sub_preference'))
    
    return render_template('lab9/preference.html', name=session['name'], age=session['age'], gender=session['gender'])

@lab9.route('/lab9/sub_preference/', methods=['GET', 'POST'])
def sub_preference():
    if 'name' not in session or 'age' not in session or 'gender' not in session or 'preference' not in session:
        return redirect(url_for('lab9.main'))
    
    if request.method == 'POST':
        sub_preference = request.form['sub_preference']
        session['sub_preference'] = sub_preference  # Сохраняем подкатегорию в сессии
        return redirect(url_for('lab9.congratulations'))
    
    return render_template('lab9/sub_preference.html', name=session['name'], age=session['age'], gender=session['gender'], preference=session['preference'])

@lab9.route('/lab9/congratulations/')
def congratulations():
    if 'name' not in session or 'age' not in session or 'gender' not in session or 'preference' not in session or 'sub_preference' not in session:
        return redirect(url_for('lab9.main'))
    
    name = session['name']
    age = int(session['age'])  # Преобразуем возраст в целое число
    gender = session['gender']
    category = session['preference'].strip().lower()  # Приводим к нижнему регистру и убираем пробелы
    subcategory = session['sub_preference'].strip().lower()  # Приводим к нижнему регистру и убираем пробелы

    # Логика для выбора картинки и надписи подарка
    if category == 'что-то вкусное':
        if subcategory == 'сытное':
            image = 'Торт.png'
            gift = "тортик"
        elif subcategory == 'сладкое':
            image = 'Конфеты.png'
            gift = "мешочек конфет"
        else:
            return "Ошибка: неверная подкатегория для категории 'Что-то вкусное'."
    elif category == 'что-то красивое':
        if subcategory == 'природа':
            image = 'Природа.jpg'
            gift = "картина"
        elif subcategory == 'искусство':
            image = 'Искусство.jpg'
            gift = "ёлочная игрушка"
        else:
            return "Ошибка: неверная подкатегория для категории 'Что-то красивое'."
    else:
        return "Ошибка: неверная категория."

    # Логика для выбора поздравления
    if age >= 18:  # Проверка на возраст
        if gender == 'male':
            greeting = f"Поздравляю вас с новым годом, {name}! Желаю, чтобы воплощались все мечты и достигались цели, а стремление к ним было вдохновляющим и интересным!"
        else:
            greeting = f"Поздравляю вас с новым годом, {name}! Желаю оставаться такой же красивой, милой и прекрасной!"
    else:
        if gender == 'male':
            greeting = f"Поздравляю тебя с новым годом, {name}, желаю побольше приятностей и поменьше неприятностей! Никогда не сомневайся в себе и достигай своих целей!"
        else:
            greeting = f"Поздравляю тебя с новым годом, {name}, желаю, чтобы каждый день будет для тебя приятным сюрпризом! Сияй, как самая яркая звёздочка на небе! "

    # Сохраняем данные в сессии
    session['greeting'] = greeting
    session['gift'] = gift
    session['image'] = image

    return render_template('lab9/congratulations.html', greeting=greeting, gift=gift, image=image)