from flask import Blueprint, redirect, url_for, render_template, request, session, current_app, jsonify, flash
import sqlite3
from os import path
import hashlib

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')