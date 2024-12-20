from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/index.html')

@lab9.route('/lab9/age/', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form['age']
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)

@lab9.route('/lab9/gender/', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form['gender']
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)

@lab9.route('/lab9/preference/', methods=['GET', 'POST'])
def preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        preference = request.form['preference']
        return redirect(url_for('lab9.sub_preference', name=name, age=age, gender=gender, preference=preference))
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)

@lab9.route('/lab9/sub_preference/', methods=['GET', 'POST'])
def sub_preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    if request.method == 'POST':
        sub_preference = request.form['sub_preference']
        return redirect(url_for('lab9.congratulations', name=name, age=age, gender=gender, category=preference, subcategory=sub_preference))
    return render_template('lab9/sub_preference.html', name=name, age=age, gender=gender, preference=preference)

@lab9.route('/lab9/congratulations/')
def congratulations():
    name = request.args.get('name')
    age = int(request.args.get('age'))  # Преобразуем возраст в целое число
    gender = request.args.get('gender')
    category = request.args.get('category', '').strip().lower()  # Приводим к нижнему регистру и убираем пробелы
    subcategory = request.args.get('subcategory', '').strip().lower()  # Приводим к нижнему регистру и убираем пробелы

    # Отладочный вывод
    print(f"Category: {category}, Subcategory: {subcategory}")

    # Инициализация переменных
    gift = None
    image = None

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
            greeting = f"Поздравляю вас, {name}! Желаю, чтобы воплощались все мечты и достигались цели, а стремление к ним было вдохновляющим и интересным. Пусть открываются новые перспективные грани и возможности, а удача просто преследует везде и всюду, и как талисман, помогает во всех делах и начинаниях. Пусть будет много радостных событий и хороших людей рядом."
        else:
            greeting = f"Поздравляю вас, {name}! Желаю оставаться такой же красивой, милой и прекрасной! Любви и радости желаю, крепкого здоровья, сил, сил, терпения! Будьте по-настоящему счастливы!"
    else:
        if gender == 'male':
            greeting = f"Поздравляю тебя, {name}, желаю побольше приятностей и поменьше неприятностей! Никогда не сомневайся в себе и достигай своих целей!"
        else:
            greeting = f"Поздравляю тебя, {name}, желаю, чтобы каждый день будет для тебя приятным сюрпризом! Сияй, как самая яркая звёздочка на небе! "

    # Проверка, что переменные gift и image были инициализированы
    if gift is None or image is None:
        return "Ошибка: не удалось определить подарок или картинку."

    return render_template('lab9/congratulations.html', greeting=greeting, gift=gift, image=image)