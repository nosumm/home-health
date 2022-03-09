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
from flask import current_app

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
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Log In', form=form)

# log out route 
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# route for sign up page --> creates new user in database 
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    global packet_queue
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)