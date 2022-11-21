from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from backend import login_manager
from backend.models import Player, PlayersGroup, User, db


@login_manager.user_loader
def load_user(user_id):
    # return User.query.filter_by(int(user_id))
    return User.query.get(int(user_id))


view_bp = Blueprint('views', __name__, url_prefix='/')


def get_groups(current_user):
    groups_by_query = PlayersGroup.query.filter_by(
        user_id=current_user.get_id())
    groups = [group for group in groups_by_query]
    return groups


@view_bp.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.jinja', groups=get_groups(current_user=current_user))
    return redirect(url_for('auth.login'))


@view_bp.route('/create_group', methods=['GET', 'POST'])
@ login_required
def create_group():
    if request.method == 'POST':
        group_name = request.form['group_name']
        user_id = current_user.get_id()

        with db.session.begin(subtransactions=True):
            new_group = PlayersGroup(
                name=group_name, user_id=user_id)
            db.session.add(new_group)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('create_group.jinja')


@view_bp.route('/update_group/<int:group_id>', methods=['GET', 'POST'])
@ login_required
def update_group(group_id):
    if request.method == 'POST':
        with db.session.begin(subtransactions=True):
            group = PlayersGroup.query.get(group_id)
            group.name = request.form['group_name']
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('update_group.jinja')


@view_bp.route('/delete_group/<int:group_id>', methods=['POST'])
@ login_required
def delete_group(group_id):

    if request.method == 'POST':
        with db.session.begin(subtransactions=True):
            group = PlayersGroup.query.get(id=group_id)
            db.session.delete(group)
        db.session.commit()
        return redirect(url_for('views.home'))


@ view_bp.route('/create_player/<int:group_id>', methods=['GET', 'POST'])
@ login_required
def create_player(group_id):
    if request.method == 'POST':
        player_name = request.form['player_name']
        player_gender = request.form['player_gender']

        with db.session.begin(subtransactions=True):
            new_player = Player(
                name=player_name, gender=player_gender, belonged_group_id=group_id)
            db.session.add(new_player)
        db.session.commit()

        return redirect(url_for('show_group'), group_id=group_id)
    return render_template('create_player.jinja')


@ view_bp.route('/update_player/<int:player_id>', methods=['GET', 'POST'])
@ login_required
def update_player(player_id):
    player = Player.query.get(player_id)
    group_id = player.belonged_group_id

    if request.method == 'POST':
        with db.session.begin(subtransactions=True):
            player = Player.query.get(id)
            player.name = request.form['player_name']
            player.gender = request.form['player_gender']
            player.play_times = request.form['play_times']
        db.session.commit()
        return redirect(url_for('show_group'), group_id=group_id)
    return render_template('update_player.jinja')


@view_bp.route('/show_group/<int:group_id>', methods=['GET'])
def show_group(group_id):
    return render_template('show_group.jinja')
