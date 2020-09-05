# main/views.py

from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/info')
def info():
	return render_template('info.html')