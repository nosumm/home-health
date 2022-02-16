from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm, SignupForm, EditProfileForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from config import Config
from datetime import datetime
# add for thingspeak communication
import urllib
from bs4 import BeautifulSoup
import re # for regex
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# admin class
class people():
    people = ['Samuel Awuah', 'Shujian Lao', 'Will J Lee', 'Christin Lin', 'Mino Song', 'Noah S Staveley']
    def __repr__(self):
        return 'People {}>'.format(self.people)
    
# classes - for user database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)  # email field format is validated
    DOB = db.Column(db.String(6), index=True, unique=True)      # DOB field format is validated
    password_hash = db.Column(db.String(128))
    packets = db.relationship("Packet", backref='author', lazy='dynamic')
    packet_count = db.Column(db.Integer, index=True, unique=False)
    admin = db.Column(db.Integer, index=True, unique=False)

    def __repr__(self):
        self.id = id
        self.admin = admin
        self.admin = False
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def validate_DOB(self, DOB):
        try:
            datetime.strptime(DOB, '%m-%d-%Y')
        except ValueError:
            raise ValueError("oops, we want your DOB in a specific format. Please try again.")
    
    def validate_email(self, email):
        # regular expression for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            pass
        else:
            raise ValueError("oops, please enter a valid email")
        
            
@login.user_loader
def load_user(id):
    return User.query.get(int(id))                                 
    
class Packet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        self.id = id
        self.user_id = User.id
        return '<Packet {}>'.format(self.body)


# ROUTES

@app.route("/")
@app.route('/index')
@login_required
def index():
    return render_template("index_login.html", title='Home Page')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Packet': Packet}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, admin=False)
        user.set_password(form.password.data)
        user.validate_DOB(form.DOB.data)
        user.validate_email(form.email.data) 
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    #if(user.admin == True):         
    return render_template('user.html', user=user, packets=user.packets.all()) 

@app.route('/edit_profile', methods=['GET', 'POST'])
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
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.DOB.data = current_user.DOB
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
    
@app.route('/newtest/<username>')
def newtest(username):
    user = User.query.filter_by(username=username).first_or_404()
    new_packet(user) # call packet create helper function
    # render user page again with new packet added
    return render_template('user.html', user=user, packets=user.packets.all())
  
@app.route('/deletetests/<username>')
def delete_all_tests(username):
    user = User.query.filter_by(username=username).first_or_404()
    delete_all_packets(user) # call helper
    return render_template('user.html', user=user, packets=user.packets.all())  

@app.route('/deletetest/<username>/<packet_id>')
def deletetest(username, packet_id):
    user = User.query.filter_by(username=username).first_or_404()
    p = Packet.query.filter_by(id=packet_id).first_or_404()
    db.session.delete(p)
    db.session.commit()
    return render_template('user.html', user=user, packets=user.packets.all())  

@app.route('/about')
def about():
    return render_template('about.html', people=people.people) 


# this function grabs data from a thingspeak channel
# creates a new packet and inserts the data into the body field
def new_packet(user):
    thingspeak_read = urllib.request.urlopen('https://thingspeak.com/channels/289288/fields/1/1')
    thingspeak_data = thingspeak_read.read()
    body_contents = str(thingspeak_data) + "TEST#" + str(len(user.packets.all()))
    p = Packet(body=body_contents, author=user) # create a new packet associated with user with thingspeak data as the content of the body
    # add new packet to db
    db.session.add(p)
    db.session.commit()
    
# this function deletes all packets for the given user
def delete_all_packets(user):
    packets = user.packets.all() 
    for p in packets:
        # add new packet to db
        db.session.delete(p)
    db.session.commit()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
    
    
# admin functions

#@app.route('/admin/<username>')
#def view_users(username):
#    user = User.query.filter_by(username=username).first_or_404() # grab admin user
    # todo - validate admin
    # render user page again with new packet added
#    return render_template('view_users.html')
      
if __name__ == '__main__':
    app.jinja_env.cache = {} # clear cache -> optimize page load time
    app.run(debug=True)
    
    
