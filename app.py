from flask import Flask, url_for, redirect, Response
app = Flask (__name__)


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
                <a href="/lab1">Первая лабораторная работа</a>
                </div>
                
                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>   
            </body>
        </html>'''


@app.route ("/lab1")
def lab1():
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Лабораторная работа 1</title>   
            </head>
 
            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
                    <hr>
                </header>
                
                <div style="text-align: left; margin: 20px;">
                    Flask &mdash; фреймворк для создания веб&mdash;приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков &mdash; минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </div>

                <div style="text-align: left; margin: 20px;">
                    Список роутов:
                </div>

                <div style="text-align: left; margin: 20px;">
                    <a href="/">Главная страница</a>
                </div>
                
                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>   
            </body>
        </html>'''


@app.route("/lab1/web")
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
            'X-Server': 'sample', 'Content-Type': 'text/html; charset=utf-8'
            }
  
@app.route("/lab1/author")
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


@app.route ("/lab1/info")
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
                        width: 700px;
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


@app.errorhandler(Exception)
def internal_server_error(err):
    path = url_for("static", filename="500.png")
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
                <h1 style="text-size: 20px; margin: 20px; font-family: 'Tahoma', Arial, sans-serif;">Ошибка 500</h1>

                <div style="text-align: left; margin: 20px; font-family: 'Times new Roman', Arial, sans-serif;">
                    Извините, произошла непредвиденная ошибка. Повторите попытку позже.
                </div>

                <div style="text-align: center;">
                    <img src="''' + path + '''">
                </div>
            </body>
        </html>''', 500

@app.route('/500')
def index500():
# Генерируем ошибку деления на ноль
    1 / 0

@app.route('/about')
def about():
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    path = url_for("static", filename="dig.jpg")
    resp = Response('''
        <!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <style>
                    img {
                        width: 700px;
                        height: 400px;
                        border: 5px solid black;
                    }
                </style>   
            </head>
 
            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2
                    <hr>
                </header>
                
                <h1 style="text-size: 20px; margin: 20px;">The importance of digitalization for business valuation</h1>
                <div style="text-align: left; margin: 20px;">
                    Over the past 77 years, the capabilities of computer technology, which underlie most information processes, have expanded significantly. 
                    In our modern world, information has become a key strategic asset in any developing society. The states of the world often wage an "information war" against each other, 
                    humanity divides the atom into small pieces, creates virtual worlds on the network, etc. These two aspects &mdash; technological and social &mdash; together form the phenomena 
                    of informatization, which lead to the digitalization of society. In this sense, V.S. Shiplyuk. correctly indicates that the sequence of industrial revolutions 
                    led to the digital era, which arose as a result of automation and informatization processes within the framework of the fourth industrial revolution.
                    <p> </p>
                    The modern world economy is experiencing a new development round associated with digitalization as global phenomenon, caused by scientific 
                    and technological progress and the corresponding new opportunities of integration human activities into a virtual environment, and also transfers many functions to the computer, 
                    in particular, artificial intelligence. Thus, according to the well&mdash;known “Datareportal” report, in 2022, digital behavior in the world demonstrated 
                    some of the deepest changes that were observed for the last years, even comparing with transformation called by COVID&mdash;19 pandemic.
                    <p> </p>
                    At the beginning of 2023 were 5.16 billion web users (64.4 percent of world population), among them 4.7 billion social media users [Digital 2023: Global Overview Report, 2023], 
                    and at the same time the growth in number of web users is exponentially consistent. Truly, today if you have access to web you can use digital technologies 
                    and this using continue to grow steadily; digitalization permeate in both peoples and company's lives. This is not surprising, because the importance 
                    of digital technologies and platforms is growing significantly in global problems solving and in reacting to different challenges and shocks 
                    (for instance, COVID&mdash;19 pandemic), and they also create new jobs and markets, expand access to finances and improve business efficiency and transparency.
                    <p> </p>
                    Modern opportunities and problems of digitalization of economy are important for economic systems of many countries, in this case continuing transfer 
                    from industrial economy to digital economy strongly changes business in terms of new manufacturing factors, organizations, models and contexts, 
                    which requires a new theoretical basis, including when evaluating a business. And, for example, over the past few years, organizations 
                    have increasingly used artificial intelligence to benefit businesses through the use of big data processing technologies and significant increases in computing power. 
                    In addition, neural networks have begun to be appreciated, machine learning is actively used; the importance of crypto economics is growing, etc. 
                    The use of breakthrough digital technologies allows modern companies to minimize resource consumption by using information 
                    and communication technology tools within the framework of Industry 4.0.
                    <p> </p>
                    At the same time, in the context of increased turbulence in the global economy and finance caused by the sequence of these crises: 
                    epistemological (for example, consequences of COVID&mdash;19 pandemic), geopolitical (for instance, modern war conflicts), energy (for example, energy crisis), 
                    logistic (for instance, supply chains), ecological (for example, CO2 emissions) and other crises, when making organizational changes, the goal 
                    of any business should be to increase long&mdash;term value, because digitalization contributes to the introduction of different elements 
                    of a stable business model [Broccardo, 2023]. And according to the “Compass of digital economy for 2022”, developed by the Stanista company [Digital Economy Compass, 2022], 
                    the events of 2022 led to a tightening of monetary policy and increased uncertainty, which triggered a global cost of living crisis affecting 
                    the financial development of businesses, while digital finance can play a key role in providing access to finance and creating new economic opportunities.
                </div>

                <div style="text-align: center; padding-bottom: 100px">
                    <img src="''' + path + '''">
                </div>
                
                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>
            </body>
        </html>
    ''')
    resp.headers['Content-Language'] = 'en'
    resp.headers['X-Custom-Header-One'] = 'Header Value One'
    resp.headers['X-Custom-Header-Two'] = 'Header Value Two'
    return resp
   

   
            
   











