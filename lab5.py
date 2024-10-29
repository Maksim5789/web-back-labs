# Это Ваш файл lab5.py (или как он у Вас называется)
from flask import Blueprint, redirect, url_for, render_template, request

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('lab5.list_articles', username=username))
    return render_template('lab5/login.html')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

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
