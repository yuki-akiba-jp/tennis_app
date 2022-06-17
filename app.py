# model-exam/app.py
import os

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sec key'
db_url = os.environ.get('DATABASE_URL')
# or 'postgresql://postgres:postgres@localhost/data'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jrqhkjpytckayx:289ee399abda48dfb0691a002dac52fdcd0bfd7590cf967555f44bf06ecd91dc@ec2-54-157-16-196.compute-1.amazonaws.com:5432/ddsvin4q4o32o4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
