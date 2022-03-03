from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_babel import _
from website import db
from website.auth import bp
from website.auth.forms import LoginForm, SignupForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from website.models import User
from website.auth.email import send_password_reset_email
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from website.models import people

# home page for guests (not logged in)
@bp.route('/')
@bp.route('/index_guest')
def index_guest():
    return render_template("index_guest.html", title='Home Page')
# route for log in page
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Log In', form=form)

# log out route 
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

# route for sign up page --> creates new user in database 
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    global packet_queue
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.validate_DOB(form.DOB.data)
        user.validate_email(form.email.data)
        user.set_admin(form.username.data)
        user.packet_count = 0
        db.session.add(user)
        db.session.commit()
        MESSAGE = 'Congratulations ' + user.username + ' you are now a registered user!'
        flash(MESSAGE)
        if user.admin == True:
            flash('This is an admin account')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', title='Sign up', form=form)

# this route renders the user profile page 
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()        
    return render_template('user.html', user=user, packets=user.packets.all())

# this app route loads the home page 
# you must log in to view the home page 
# right now the home page simply displays a custom greeting for the user
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template("index_login.html", title='Home Page')

# route for edit profile form 
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.DOB = form.DOB.data
        current_user.validate_DOB(form.DOB.data)
        current_user.validate_email(form.email.data) 
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.DOB.data = current_user.DOB
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)
    
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('auth.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)