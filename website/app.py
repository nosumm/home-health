from flask import Flask, render_template, redirect, url_for, flash, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MINO_SONG'

people = ['Samuel Awuah', 'Shujian Lao', 'Will J Lee', 'Christin Lin', 'Mino Song', 'Noah S Staveley']


@app.route("/")
def index():
    return render_template('index.html', people=people)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'sxp0728@126.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check the username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', title='Register', form=form)


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == '__main__':
    app.run(debug=True)