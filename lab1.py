
from flask import Blueprint, redirect, url_for, render_template, Response
lab1 = Blueprint('lab1',__name__)


@lab1.route ("/lab1/")
def lab():
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Лабораторная работа 1</title>   
            </head>
 
            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Лабораторная работа №1
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
                    <h2>Список роутов:</h2>
                    <ul>
                    <li><a href="/">Главная страница</a></li>                    
                    <li><a href="/lab1/web">Web-сервер на flask</a></li>                   
                    <li><a href="/lab1/author">Автор</a></li>                 
                    <li><a href="/lab1/oak">Дуб</a></li>                
                    <li><a href="/lab1/counter">Счётчик</a></li>               
                    <li><a href="/lab1/info">Информация об авторе</a></li>        
                    <li><a href="/400">Ошибка 400</a></li>        
                    <li><a href="/401">Ошибка 401</a></li>        
                    <li><a href="/402">Ошибка 402</a></li>         
                    <li><a href="/403">Ошибка 403</a></li>        
                    <li><a href="/404">Ошибка 404</a></li>             
                    <li><a href="/405">Ошибка 405</a></li>                
                    <li><a href="/418">Ошибка 418</a></li>
                    <li><a href="/500">Ошибка 500</a></li>          
                    <li><a href="/lab1/about">Цифровизация в оценке бизнеса</a></li>
                    <li><a href="/lab1/resource">Состояние ресурса</a></li>
                    <li><a href="/lab1/created">Создание ресурса</a></li>
                    <li><a href="/lab1/delete">Удаление ресурса</a></li>                  
                    </ul>
                </div>
                
                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>   
            </body>
        </html>'''

@lab1.route("/lab1/web")
def web():
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Web-сервер на flask</title>
                <style>
                div{
                    margin: 20px;
                }
                </style>   
            </head>

            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Лабораторная работа №1
                    <hr>
                </header>

                <div>
                    <h1>web-сервер на flask</h1>
                    <a href="/lab1">Меню лабораторной работы №1</a>
                </div>

    
                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>
            </body>
        </html>''', 200, {
            'X-Server': 'sample', 'Content-Type': 'text/html; charset=utf-8'
            }
  
@lab1.route("/lab1/author")
def author():
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    name = "Акишин Максим Валерьевич"
    group = "ФБИ-22"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <title>Автор</title>
                <style>
                div{
                    margin: 20px;
                }
                </style>    
            </head>

            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Лабораторная работа №1
                    <hr>
                </header>

                <div style: margin:20px;">

                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="/lab1">Меню лабораторной работы №1</a>

                </div>

                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>
            </body>
        </html>'''

@lab1.route ('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!doctype html>
        <html>
            <head>
                <title>Дуб</title>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <style>
                div {
                    margin: 20px;
                }

                a {
                    margin:20px;
                    padding-bottom: 150px;
                }

                img {
                    border: 5px solid black;
                }
                </style> 
            </head>
            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Лабораторная работа №1
                    <hr>
                </header>

                <div>
                    <h1>Дуб</h1>
                    <img src="''' + path + '''">
                <div>

                <a href="/lab1">Меню лабораторной работы №1</a>
            
                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>
            </body>
        </html>
        '''

count = 0

@lab1.route ('/lab1/counter')
def counter():
    global count
    count += 1
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!doctype html>
        <html>
            <head>
                <title>Счётчик</title>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <style>
                    div {
                        margin: 20px;
                    }
                </style>
            </head>

            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Лабораторная работа №1
                    <hr>
                </header>
                
                <div>
                    Сколько раз заходили: ''' + str(count) + '''
                    <p> </p>
                    <a href="/lab1">Меню лабораторной работы №1</a>  
                    <a href="/lab1/reset">Сбросить счётчик</a>
                </div>

                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>
            </body>
        </html>
        '''

@lab1.route ('/lab1/reset')
def reset_counter():
    global count
    count = 0
    css_path = url_for("static", filename="lab1.css")  # путь к файлу lab1.css
    return '''<!doctype html>
        <html>
            <head>
                <title>Сброс счётчика</title>
                <link rel="stylesheet" type="text/css" href="''' + css_path + '''">  <!-- подключение CSS файла -->
                <style>
                    div {
                        margin: 20px;
                    }
                </style>
            </head>
            
            <body>
                <header>
                    НГТУ, ФБ, WEB-программирование, часть 2. Лабораторная работа №1
                    <hr>
                </header>
                
                <div>
                    <p>Счётчик успешно сброшен</p>
                    <a href="/lab1">Меню лабораторной работы №1</a>  
                    <a href="/lab1/counter">Счётчик</a>
                </div>

                <footer>
                    <hr>
                    &copy; Акишин Максим, ФБИ-22, 3 курс, 2024
                </footer>
            </body>
        </html>
        '''

@lab1.route ("/lab1/info")
def info():
    return redirect("/lab1/author")


resource_created = False

@lab1.route('/lab1/created')
def created():
    global resource_created
    if not resource_created:
        resource_created = True
        return render_template('lab1/create.html'), 201
    else:
        return render_template('lab1/err_cr.html'), 400
    
@lab1.route('/lab1/delete')
def delete():
    global resource_created
    if resource_created:
        resource_created = False
        return render_template('lab1/delete.html'), 200
    else:
        return render_template('lab1/err_del.html'), 400
    
@lab1.route('/lab1/resource')
def resource():
    status = 'Ресурс создан' if resource_created else 'Ресурс ещё не создан'
    return render_template('lab1/resource.html', status=status)

@lab1.route('/lab1/about')
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
                    In addition, neural networks have begun to be lab1reciated, machine learning is actively used; the importance of crypto economics is growing, etc. 
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

                <div style="text-align: center; margin-bottom: 30px">
                    <img src="''' + path + '''">
                </div>

                <div style="text-align: left; margin-bottom: 100px">
                    <a href="/lab1">Меню лабораторной работы №1</a>
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