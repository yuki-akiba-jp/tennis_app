# model-exam/app.py
import os
from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__name__))

app.config['SECRET_KEY'] = 'sec key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
engine = create_engine(os.environ.get('DATABASE_URL') or 'sqlite:///' + basedir,convert_unicode=True,echo=True)
