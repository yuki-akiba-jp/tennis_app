# model-exam/app.py
import os

import psycopg2
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sec key'
db_url = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
# app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:postgres@localhost/data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
