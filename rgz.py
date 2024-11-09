from flask import Blueprint, redirect, url_for, render_template, request, session, current_app
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    return render_template('rgz/main.html')