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
        return redirect(url_for('lab9.congratulations', name=name, age=age, gender=gender, preference=preference, sub_preference=sub_preference))
    return render_template('lab9/sub_preference.html', name=name, age=age, gender=gender, preference=preference)

@lab9.route('/lab9/congratulations/')
def congratulations():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    sub_preference = request.args.get('sub_preference')

    # Логика для выбора поздравления и картинки
    if gender == 'male':
        greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро вырос, был умным..."
        gift = "мешочек конфет"
        image = "candies.jpg"  # Путь к картинке с конфетами
    else:
        greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро выросла, была умной..."
        gift = "тортик"
        image = "cake.jpg"  # Путь к картинке с тортом

    return render_template('lab9/congratulations.html', greeting=greeting, gift=gift, image=image)
