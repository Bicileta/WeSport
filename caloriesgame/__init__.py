# caloriesgame/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
###################
#### DATABASE #####
###################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'bicileta'

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


###################
from caloriesgame.main.views import main
from caloriesgame.error_pages.handlers import error_pages
from caloriesgame.users.views import users

app.register_blueprint(main)
app.register_blueprint(error_pages)
app.register_blueprint(users)