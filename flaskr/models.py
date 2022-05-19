# models.py
from app import app
from flask import Flask
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flaskr import db, login_manager

db = SQLAlchemy(app)
Migrate(app, db)


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def add_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class Player(db.Model):

    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    name = db.Column(db.Text)
    play_times = db.Column(db.Integer)

    def __init__(self, age, gender, name):
        self.age = age
        self.gender = gender
        self.name = name
        self.play_times = 0
