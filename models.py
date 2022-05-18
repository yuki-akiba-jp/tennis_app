# models.py
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)
Migrate(app, db)


class Member(db.Model):

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
