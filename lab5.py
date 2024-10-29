from flask import Blueprint, redirect, url_for, render_template, request, session
import sqlite3



# Создаём RealDictCursor для sqlite3
class DictCursor(sqlite3.Cursor):
    def fetchone(self):
        row = super().fetchone()
        if row is None:
            return None
        return dict(zip(self.description, row))

    def fetchall(self):
        rows = super().fetchall()
        return [dict(zip(self.description, row)) for row in rows]
    
# Функция для получения курсора, который возвращает результаты как словари
def dict_factory(cursor, row):
    return {col[0]: row[col[0]] for col in cursor.description}

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login = session.get('login'))

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните поля')

    # Подключение к базе данных
    conn = sqlite3.connect(r'C:\Users\PC\Desktop\Документы\ВУЗ\3 курс\Web-программирование\База данных\database_web') 
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Выполнение SQL-запроса с параметризованным запросом
    cur.execute("SELECT * FROM users WHERE login=?", (login,))
    user = cur.fetchone()  # Получаем одну строку

    if not user or user['password'] != password:  # Проверка пользователя и пароля
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    cur.close()
    conn.close()
    return render_template('lab5/success_login.html', login=login)



     


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    

    # Подключение к базе данных
    conn = sqlite3.connect(r'C:\Users\PC\Desktop\Документы\ВУЗ\3 курс\Web-программирование\База данных\database_web') 

    # Создание курсора
    cur = conn.cursor()

    # Выполнение SQL-запроса
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)




@lab5.route('/lab5/list')
def list_articles():
    username = request.args.get('username', 'anonymous')
    return render_template('lab5/list.html', articles=articles, username=username)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        articles.append({'title': title, 'content': content})
        return redirect(url_for('lab5.list_articles'))
    return render_template('lab5/create.html')
