#users/views.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from caloriesgame import db
from caloriesgame.models import User, WorkoutSession
from caloriesgame.users.forms import Registration, Login, UpdateUserInfo
from caloriesgame.users.picture_handler import add_profile_pic
from werkzeug.security import generate_password_hash,check_password_hash

users = Blueprint('users', __name__)


#register
@users.route('/register', methods=['GET','POST'])
def register():
    form = Registration()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


#login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        # Grabbing the user from the User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Log in Success!')


            #either go to the targeted page or back to the home page

            #If a user was trying to visit a page that requires a login
            #flask saves that URL as 'next'
            next = request.args.get('next')

            #check if that next exists, otherwise we'll go to
            #the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('main.index')

            return redirect(next)
    return render_template('login.html', form=form)


#logout
@users.route('/logout')
def logout():
	#built-in function
	logout_user()

	#direct back to home page
	return redirect(url_for("main.index"))

#profile page
@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserInfo()

    if form.validate_on_submit():
        print(form)
        if form.avatar.data:
            username = current_user.username

            #using picture_handler.py functions
            pic = add_profile_pic(form.avatar.data,username)

            current_user.avatar = pic
        current_user.username = form.username.data
        db.session.commit()
        flash('Profile Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username

    profile_image = url_for('static', filename='profile_pics/' + current_user.avatar)
    return render_template('account.html', avatar=profile_image, form=form)

#page for each user
@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    workout_sessions = WorkoutSession.query.filter_by(owner=user).order_by(WorkoutSession.date.desc()).paginate(page=page, per_page=10)
    return render_template('user_workouts.html', workout_sessions=workout_sessions, user=user)
#list of pks









