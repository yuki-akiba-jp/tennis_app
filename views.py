import random
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_manager, login_required,
                         login_user, logout_user)

from app import app
from forms import (ChangePasswordForm, ForgotPasswordForm, PlayerCreateForm,
                   PlayerDeleteForm, PlayersGroupCreateForm,
                   PlayersGroupDeleteForm, PlayersGroupUpdateForm,
                   PlayerUpdateForm, ResetPasswordForm, UserForm,
                   UserLoginForm, UserRegisterForm)
from models import PasswordResetToken, Player, PlayersGroup, User, db

login_manager = login_manager.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def app_top():
    return render_template('app_top.html')


@app.route('/user_home')
def user_home():
    if current_user.is_authenticated:
        groups_by_query = PlayersGroup.query.filter_by(
            user_id=current_user.get_id())
        groups = [group for group in groups_by_query]

        form = PlayersGroupDeleteForm(request.form)
        return render_template('user_home.html', groups=groups, form=form)
    return render_template('login.html')


@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        with db.session.begin(subtransactions=True):
            user.create_new_user()
        db.session.commit()
        token = ''
        with db.session.begin(subtransactions=True):
            token = PasswordResetToken.publish_token(user)
        db.session.commit()

# in this case,just print
# send by email is better
        # print(
        #     f'to set password URL: http://127.0.0.1:5000/reset_password/{token}'
        # )
        # flash('sent URL for setting password')

        return redirect(url_for('reset_password', token=token))
    return render_template('user_register.html', form=form)


@app.route('/reset_password/<uuid:token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm(request.form)
    reset_user_id = PasswordResetToken.get_user_id_by_token(token)
    if not reset_user_id:
        flash('this URL is invalid, please confirm URL')

    if request.method == 'POST' and form.validate():
        password = form.password.data
        user = User.select_user_by_id(reset_user_id)
        with db.session.begin(subtransactions=True):
            user.save_new_password(password)
            PasswordResetToken.delete_token(token)
        db.session.commit()
        flash('password is changed')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = User.select_user_by_email(email)
        if user:
            with db.session.begin(subtransactions=True):
                token = PasswordResetToken.publish_token(user)
            db.session.commit()
            reset_url = f'http://127.0.0.1:5000/reset_password/{token}'
            print(reset_url)
            flash('sent URL for reregister password')
        else:
            flash('invalid user')
    return render_template('forgot_password.html', form=form)


@app.route('/user_update', methods=['GET', 'POST'])
@login_required
def user_update():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user_id = current_user.get_id()
        user = User.select_user_by_id(user_id)
        with db.session.begin(subtransactions=True):
            user.username = form.username.data
            user.email = form.email.data
            user.update_at = datetime.now()
        db.session.commit()
        flash('user infomation is successfully updated')
    return render_template('user.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_user_by_id(current_user.get_id())
        password = form.password.data
        with db.session.begin(subtransactions=True):
            user.save_new_password(password)
        db.session.commit()
        flash('password is successfully changed')
        return redirect(url_for('user_update'))
    return render_template('change_password.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_user_by_email(form.email.data)
        if user and user.is_active and user.validate_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('user_home'))

        elif not user:
            flash('no user')
        elif not user.is_active:
            flash('invalid user')
        elif not user.validate_password(form.password.data):
            flash('username or password is wrong')

    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/players_groups')
@login_required
def players_groups():
    groups = PlayersGroup.query.filter_by(user_id=current_user.get_id())
    form = PlayersGroupDeleteForm(request.form)
    return render_template('players_groups.html', groups=groups, form=form)


@app.route('/players_in_the_group/<int:belonged_players_group_id>')
@login_required
def players_in_the_group(belonged_players_group_id):
    players_by_queru = Player.query.filter_by(
        belonged_players_group_id=belonged_players_group_id)
    players = [player for player in players_by_queru]

    form = PlayerDeleteForm(request.form)
    dicided_players = dicide_players(players)
    return render_template('players_in_the_group.html', dicided_players=dicided_players, players=players,  form=form, belonged_players_group_id=belonged_players_group_id)


def dicide_players(players):
    to_return_players = []
    for player in players:
        to_return_players.append(player)
    to_return_players.sort(key=lambda player: player.play_times)
    same_playtimes_players = []
    for player in to_return_players:
        if player.play_times == to_return_players[0].play_times:
            same_playtimes_players.append(player)

    if len(same_playtimes_players) >= 4:
        random.shuffle(same_playtimes_players)
        return same_playtimes_players[:4]

    return to_return_players[:4]


def sort_players(players):
    to_return_players = []
    for player in players:
        to_return_players.append(player)
    to_return_players.sort(key=lambda player: player.play_times)
    return to_return_players


@app.route('/next_game/<int:belonged_players_group_id>')
@login_required
def next_game(belonged_players_group_id):
    players = Player.query.filter_by(
        belonged_players_group_id=belonged_players_group_id)
    players_group = PlayersGroup.query.get(belonged_players_group_id)
    played_players = dicide_players(players)

    players = sort_players(players)

    for player in played_players:
        with db.session.begin(subtransactions=True):
            player.inclement_play_times()
        db.session.commit()
    players = Player.query.filter_by(
        belonged_players_group_id=belonged_players_group_id)
    players = sort_players(players)
    form = PlayerDeleteForm(request.form)

    return render_template('players_in_the_group.html', dicided_players=played_players, players=players, form=form, players_group=players_group, belonged_players_group_id=belonged_players_group_id)


@ app.route('/create_players_group', methods=['GET', 'POST'])
@ login_required
def create_players_group():
    form = PlayersGroupCreateForm(request.form)
    if request.method == 'POST' and form.validate():
        group_name = form.group_name.data
        user_id = current_user.get_id()

        with db.session.begin(subtransactions=True):
            new_players_group = PlayersGroup(
                group_name=group_name, user_id=user_id)
            db.session.add(new_players_group)
        db.session.commit()
        return redirect(url_for('user_home'))
    return render_template('create_players_group.html', form=form)


@ app.route('/update_players_group/<int:belonged_players_group_id>', methods=['GET', 'POST'])
@ login_required
def update_players_group(belonged_players_group_id):
    form = PlayersGroupUpdateForm(request.form)
    players_group = PlayersGroup.query.get(belonged_players_group_id)
    players = Player.query.filter_by(
        belonged_players_group_id=belonged_players_group_id)
    dicided_players = dicide_players(players)

    if request.method == 'POST' and form.validate():
        id = form.id.data
        group_name = form.group_name.data

        with db.session.begin(subtransactions=True):
            players_group = PlayersGroup.query.get(id)
            players_group.group_name = group_name
            db.session.add(players_group)
        db.session.commit()
        return redirect(url_for('players_in_the_group', dicided_players=dicided_players, players=players, form=form,  belonged_players_group_id=belonged_players_group_id))
    return render_template('update_players_group.html', form=form, players_group=players_group, belonged_players_group_id=belonged_players_group_id)


@ app.route('/delete_players_group', methods=['GET', 'POST'])
@ login_required
def delete_players_group():
    form = PlayersGroupDeleteForm(request.form)

    if request.method == 'POST' and form.validate():
        with db.session.begin(subtransactions=True):
            id = form.id.data
            players_group = PlayersGroup.query.get(id)
            db.session.delete(players_group)
        db.session.commit()
        return redirect(url_for('user_home'))
    return redirect(url_for('user_home'))


@ app.route('/create_player/<int:belonged_players_group_id>', methods=['GET', 'POST'])
@ login_required
def create_player(belonged_players_group_id):
    form = PlayerCreateForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        gender = form.gender.data

        with db.session.begin(subtransactions=True):
            new_player = Player(
                name=name, gender=gender, belonged_players_group_id=belonged_players_group_id)
            db.session.add(new_player)
        db.session.commit()

        players = Player.query.filter_by(
            belonged_players_group_id=belonged_players_group_id)
        dicided_players = dicide_players(players)
        players = sort_players(players)
        form = PlayerDeleteForm(request.form)

        return render_template('players_in_the_group.html', dicided_players=dicided_players, players=players, form=form,  belonged_players_group_id=belonged_players_group_id)
    return render_template('create_player.html', form=form, belonged_players_group_id=belonged_players_group_id)


@ app.route('/update_player/<int:player_id>', methods=['GET', 'POST'])
@ login_required
def update_player(player_id):
    form = PlayerUpdateForm(request.form)
    player = Player.query.get(player_id)

    players = Player.query.filter_by(
        belonged_players_group_id=player.belonged_players_group_id)
    dicided_players = dicide_players(players)
    players = sort_players(players)

    if request.method == 'POST' and form.validate():
        id = form.id.data
        name = form.name.data
        gender = form.gender.data
        play_times = form.play_times.data

        with db.session.begin(subtransactions=True):
            player = Player.query.get(id)
            player.name = name
            player.gender = gender
            player.play_times = play_times
        db.session.commit()
        return redirect(url_for('players_in_the_group', dicided_players=dicided_players, players=players, form=form,  belonged_players_group_id=player.belonged_players_group_id))
    form.gender.default = player.gender
    form.process()
    return render_template('update_player.html', form=form, player=player, player_id=player.id)


@ app.route('/delete_player/<int:belonged_players_group_id>', methods=['GET', 'POST'])
@ login_required
def delete_player(belonged_players_group_id):
    form = PlayerDeleteForm(request.form)

    players = Player.query.filter_by(
        belonged_players_group_id=belonged_players_group_id)
    dicided_players = dicide_players(players)
    players = sort_players(players)

    if request.method == 'POST' and form.validate():
        id = form.id.data
        with db.session.begin(subtransactions=True):
            player = Player.query.get(id)
            db.session.delete(player)
        db.session.commit()
        return redirect(url_for('players_in_the_group', dicided_players=dicided_players, players=players, form=form,  belonged_players_group_id=player.belonged_players_group_id))
        # return render_template('players_in_the_group.html', dicided_players=dicided_players, players=players, form=form,  belonged_players_group_id=belonged_players_group_id)
    return render_template('players_in_the_group.html', dicided_players=dicided_players, players=players, form=form,  belonged_players_group_id=belonged_players_group_id)


def init_db():
    with db.session.begin(subtransactions=True):
        new_user = User(username='test', email='test@test.com')
        new_user.save_new_password('testtest')
        db.session.add(new_user)

    db.session.commit()


if __name__ == '__main__':
    init_db()
    app.run()
