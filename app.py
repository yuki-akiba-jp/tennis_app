# model-exam/app.py
import os

from flask import Flask

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__name__))

app.config['SECRET_KEY'] = 'sec key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI') or 'postgresql://postgres:postgres@localhost/data'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
