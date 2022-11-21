from datetime import datetime, timedelta
from uuid import uuid4

from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from backend import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    hashed_password = db.Column(db.String(256))
    # is_active = db.Column(db.Boolean, unique=False, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

    def validate_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_id(self):
        return self.id


class Player(db.Model):

    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    belonged_group_id = db.Column(db.Integer)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    play_times = db.Column(db.Integer)

    def __init__(self, name, gender, belonged_group_id):
        self.name = name
        self.gender = gender
        self.belonged_group_id = belonged_group_id
        self.play_times = 0

    def inclement_play_times(self):
        self.play_times = self.play_times+1


class PlayersGroup(db.Model):
    __tablename__ = 'players_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
