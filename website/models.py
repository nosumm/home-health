import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import rq
import re # for regex
from website import db, login


# User class for db
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)          # email field format is validated
    DOB = db.Column(db.String(6), index=True, unique=True)              # DOB field format is validated
    password_hash = db.Column(db.String(128))
    packets = db.relationship("Packet", backref='author', lazy='dynamic')
    packet_count = db.Column(db.Integer, index=True)                    # TODO: managing the users packet counter
    admin = db.Column(db.Integer, index=True, default=False)

    def __repr__(self):
        self.id = id
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def validate_DOB(self, DOB):
        try:
            datetime.strptime(DOB, '%m-%d-%Y')
        except ValueError:
            raise ValidationError("oops, we want your DOB in a specific format. Please try again.")
    
    def validate_email(self, email):
        # regular expression for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            pass
        else:
            raise ValidationError("oops, please enter a valid email")
    
    def set_admin(self, username):
        user = User.query.filter_by(username=username).first()
        try: 
            people.usernames.index(username)
            if SignupForm.admin_code == people.usernames:
                self.admin = True
            else:
                self.admin = False
        except ValueError:
            self.admin = False
            
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
# this route loads the user with the given id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# packet class for db
class Packet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # this timestamp represents when the test was ordered
    test_taken = db.Column(db.String(50), index=True, default=None)             # this timestamp represents when the test was taken
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    test_type = db.Column(db.String(150), default=None)

    def __repr__(self):
        self.id = id
        self.user_id = User.id
        return '<Packet {}>'.format(self.body)
# admin class to store admin users 
class people():
    people = ['Samuel Awuah', 'Shujian Lao', 'Will J Lee', 'Christin Lin', 'Mino Song', 'Noah S Staveley']
    usernames = ['samuel_awuah, shujian_lao', 'will_lee', 'christin_lin', 'mino_song', 'noah_s', 'nstave']
    def __repr__(self):
        return 'People {}>'.format(self.people)
    