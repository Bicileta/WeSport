#models.py
from caloriesgame import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

# friends = db.Table('friends',
# 	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
# 	db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
# )

class User(db.Model, UserMixin):
	
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	avatar = db.Column(db.String(128),nullable=False,default='./default_avatar.png')
	email = db.Column(db.String(128), unique=True, index=True)
	username = db.Column(db.String(128), index=True)
	password_hash = db.Column(db.String(128))
	age = db.Column(db.Integer, default='20')
	current_weight = db.Column(db.Float, default='60')

	workouts = db.relationship('WorkoutSession', backref='owner', lazy='dynamic')
	
	#relationships:
	#a list of integer for friend ids
	#friends

	#each user has many pks
	#pks = db.relationship('PK',backref='contestant',lazy=True)

	#each user has many interests
	#interests = db.relationship('Exercise')

	# friends = db.relationship('User', #defining the relationship, User is left side entity
 #        secondary = friends, 
 #        primaryjoin = (friends.c.user_id == id), 
 #        secondaryjoin = (friends.c.friend_id == id),
 #        lazy = 'dynamic'
 #    ) 


	def __init__(self,email,username,password):
		self.email = email
		self.username = username
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return f"Username: {self.username}"




class WorkoutSession(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	users = db.relationship(User)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
	date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	timeLasted = db.Column(db.Integer,nullable=False)

	def __init__(self,user_id,timeLasted):
		self.user_id = user_id
		self.timeLasted = timeLasted
	
	def __repr__(self):
		return f"workout id: {self.id}"




