
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sec key'
    basedir = os.path.abspath(os.path.dirname(__name__))

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # try:
    #     db_url = os.getenv('DATABASE_URL')
    #     db_url = db_url.replace("postgres://", "postgresql://")
    #     app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    # except:
    #     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/data'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    from backend.views import view_bp
    app.register_blueprint(view_bp)
    from backend.auth import auth_bp
    app.register_blueprint(auth_bp)
    db.init_app(app)
    login_manager.init_app(app)
    from backend.database import init_db
    with app.app_context():
        db.create_all()

    with app.app_context():
        from backend.models import User
        user = User(username='username',
                    hashed_password=generate_password_hash('pw'))
        db.session.add(user)
        db.session.commit()
    return app
