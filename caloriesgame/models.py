#models.py
from caloriesgame import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

class User(db.Model, UserMixin):
	
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	avatar = db.Column(db.String(128),nullable=False,default='default_avatar.png')
	email = db.Column(db.String(128), unique=True, index=True)
	username = db.Column(db.String(128), index=True)
	password_hash = db.Column(db.String(128))

	#a list of integer for friend ids
	#friends

	#each user has many pks
	#pks = db.relationship('PK',backref='contestant',lazy=True)

	#each user has many interests
	#interests = db.relationship('Exercise')


	def __init__(self,email,username,password):
		self.email = email
		self.username = username
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return f"Username: {self.username}"


class Exercise(db.Model):
	users = db.relationship(User)
	id = db.Column(db.Integer,primary_key=True)


class PK(db.Model):
	__tablename__ = 'pks'
	id = db.Column(db.Integer, primary_key=True)
	contestant_one_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	contestant_two_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

	#need more such as calories...winners...

	def __init__(self,contestant_one_id,contestant_two_id):
		self.contestant_one_id = contestant_one_id
		self.contestant_two_id = contestant_two_id

	def __repr__(self):
		return f"PK id: {self.id}"


# class Group(db.Model):
# 	pass







