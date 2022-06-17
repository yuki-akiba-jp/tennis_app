# models.py
from datetime import datetime, timedelta
from uuid import uuid4

from flask_login import UserMixin, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import  check_password_hash, generate_password_hash
from werkzeug.security import check_password_hash, generate_password_hash

from app import app

db = SQLAlchemy(app)
Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    hashed_password = db.Column(db.String(256))

    is_active = db.Column(db.Boolean, unique=False, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def validate_password(self, password):
        # return check_password_hash(self.hashed_password, password)
        hashed_password = password[5:]+password[:5]
        if self.hashed_password == hashed_password:
            return True
        else:
            return False

    def create_new_user(self):
        db.session.add(self)

    @classmethod
    def select_user_by_id(cls, id):
        return cls.query.get(id)

    def save_new_password(self, new_password):
        # self.hashed_password = generate_password_hash(new_password)
        self.hashed_password = new_password[5:] + new_password[:5]
        self.is_active = True


class Player(db.Model):

    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    belonged_players_group_id = db.Column(db.Integer)
    name = db.Column(db.String)
    gender = db.Column(db.String)
    play_times = db.Column(db.Integer)

    def __init__(self, name, gender, belonged_players_group_id):
        self.name = name
        self.gender = gender
        self.belonged_players_group_id = belonged_players_group_id
        self.play_times = 0

    def inclement_play_times(self):
        self.play_times = self.play_times+1


class PasswordResetToken(db.Model):

    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(
        db.String(256),
        unique=True,
        index=True,
        server_default=str(uuid4)
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expire_at = db.Column(db.DateTime, default=datetime.now)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, token, user_id, expire_at):
        self.token = token
        self.user_id = user_id
        self.expire_at = expire_at

    @classmethod
    def publish_token(cls, user):
        token = str(uuid4())
        new_token = cls(
            token,
            user.id,
            datetime.now() + timedelta(days=1)
        )
        db.session.add(new_token)
        return token

    @classmethod
    def get_user_id_by_token(cls, token):
        now = datetime.now()
        record = cls.query.filter_by(token=str(token)).filter(
            cls.expire_at > now).first()
        if record:
            return record.user_id
        else:
            return None

    @classmethod
    def delete_token(cls, token):
        cls.query.filter_by(token=str(token)).delete()


class PlayersGroup(db.Model):
    __tablename__ = 'players_group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, group_name, user_id):
        self.group_name = group_name
        self.user_id = user_id
