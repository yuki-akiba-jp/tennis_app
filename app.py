# model-exam/app.py
import os

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sec key'
try:
    db_url = os.getenv('DATABASE_URL')
    db_url = db_url.replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
except:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
