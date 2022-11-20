
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

from backend import db
from backend.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username,
                    hashed_password=generate_password_hash(password))
        flash(username)
        flash(password)

        with db.session.begin(subtransactions=True):
            db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    elif request.method == 'GET':
        return render_template('register.jinja')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        message = ''

        if not user:
            message = 'no user'
            return render_template('login.jinja', message=message)

        if user.validate_password(password):
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            message = 'username or password is wrong'
            return render_template('login.jinja', message=message)

    return render_template('login.jinja')


@auth_bp.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/user_update', methods=['GET', 'POST'])
@login_required
def user_update():
    if request.method == 'POST':
        user = current_user
        with db.session.begin(subtransactions=True):
            user.username = request.form['username']
            user.password = request.form['password']
            user.update_at = datetime.now()
        db.session.commit()
        flash('user infomation is successfully updated')
        return redirect(url_for('auth.login'))
