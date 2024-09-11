from flask import Flask, url_for, redirect
app = Flask (__name__)

@app.route("/web")
def web():
    return """<!doctype html> 
        <html> 
            <body> 
                <h1>web-сервер на flask</h1>
                <a href="/author">author</a>
                <a href="/lab1/oak">lab1/oak</a>
                <a href="/lab1/counter">lab1/counter</a>
            </body> 
        </html>""", 200, {
            'X-Server': 'sample', 'Content-Type': 'text/plain; charset=utf-8'
            }
  
@app.route("/author")
def author():
    name = "Акишин Максим Валерьевич"
    group = "ФБИ-22"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route ('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
        <p> </p>
        <a href="/web">web</a>    
    </body>
</html>
'''


count = 0

@app.route ('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз заходили: ''' + str(count) + '''
        <p> </p>
        <a href="/web">web</a>  
        <a href="/lab1/reset">lab1/reset</a> 
    </body>
</html>
'''

@app.route ('/lab1/reset')
def reset_counter():
    global count
    count = 0
    return "Счётчик успешно сброшен"


@app.route ("/info")
def info():
    return redirect("/author")

@app.route ("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i><div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы", 404