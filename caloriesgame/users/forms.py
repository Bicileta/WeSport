#forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from caloriesgame.models import User

class Login(FlaskForm):
	email = StringField('Email', validators = [DataRequired(),Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	submit = SubmitField('Sign In')

class Registration(FlaskForm):
	email = StringField('Email', validators=[DataRequired(),Email()])
	username = StringField('UserName', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Dont Match!')])
	pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
	submit = SubmitField('Sign up')

	def validate_email(self,email):
		if User.query.filter_by(email=self.email.data).first():
			raise ValidationError('This email address already exists!')


class UpdateUserInfo(FlaskForm):
	username = StringField('UserName', validators=[DataRequired()])
	avatar = FileField('Edit Avatar',validators=[FileAllowed(['png','jpg'])])
	submit = SubmitField('Update')
