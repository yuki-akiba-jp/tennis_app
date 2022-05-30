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
def home():
    if current_user.is_authenticated:
        return redirect(url_for('players_groups'))
    # return render_template('home.html')
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

        # メールに飛ばすほうがいい
        print(
            f'パスワード設定用URL: http://127.0.0.1:5000/reset_password/{token}'
        )
        flash('パスワード設定用のURLをお送りしました。ご確認ください')
        return redirect(url_for('login'))
    return render_template('user_register.html', form=form)


@app.route('/reset_password/<uuid:token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm(request.form)
    reset_user_id = PasswordResetToken.get_user_id_by_token(token)
    if not reset_user_id:
        pass

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
            flash('パスワード再登録用のURLを発行しました。')
        else:
            flash('存在しないユーザです')
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
        print('current_user:', current_user)
        user = User.select_user_by_id(current_user.get_id())
        print('user:', user)
        print('type of user:', type(user))
        password = form.password.data
        with db.session.begin(subtransactions=True):
            user.save_new_password(password)
        db.session.commit()
        flash('password is successfully changed')
        return redirect(url_for('user_update'))
    return render_template('change_password.html', form=form)


def dicide_players(players):
    players.sort(key=lambda player: player.play_times)
    same_playtimes_players = []
    for player in players:
        if player.play_times == players[0].play_times:
            same_playtimes_players.append(player)

    if len(same_playtimes_players) >= 4:
        random.shuffle(same_playtimes_players)
        return same_playtimes_players[:4]

    return players[:4]


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_user_by_email(form.email.data)
        if user and user.is_active and user.validate_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('home'))

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


@app.route('/players_in_the_group/<int:players_group_id>')
@login_required
def players_in_the_group(players_group_id):
    players = Player.query.filter_by(
        belonged_players_group_id=players_group_id)
    form = PlayerDeleteForm(request.form)
    dicided_players = dicide_players(players)
    return render_template('players_in_the_group.html', dicided_players=dicided_players, players=players, form=form)


@app.route('/next_game')
@login_required
def next_game():
    players = Player.query.all()
    played_players = dicide_players(players)
    for player in played_players:
        with db.session.begin(subtransactions=True):
            player.inclement_play_times()
        db.session.commit()
    form = PlayerDeleteForm(request.form)

    dicided_players = dicide_players(players)

    return render_template('players_in_the_group.html', dicided_players=dicided_players, players=players, form=form)


@app.route('/create_players_group', methods=['GET', 'POST'])
@login_required
def create_players_group(belonged_players_group_id):
    form = (request.form)
    if request.method == 'POST' and form.validate():
        group_name = form.group_name.data
        user_id = current_user.get_id()

        with db.session.begin(subtransactions=True):
            new_players_group = PlayersGroup(
                group_name=group_name, user_id=user_id)
            db.session.add(new_players_group)
        db.session.commit()
        return redirect(url_for('players_groups'))
    return render_template('create_players_group.html', form=form)


@app.route('/update_players_group/<int:players_group_id>', methods=['GET', 'POST'])
@login_required
def update_players_group(players_group_id):
    form = PlayersGroupUpdateForm(request.form)
    players_group = PlayersGroup.query.get(players_group_id)

    if request.method == 'POST' and form.validate():
        id = form.id.data
        group_name = form.group_name.data

        with db.session.begin(subtransactions=True):
            players_group = PlayersGroup.query.get(id)
            players_group.group_name = group_name
            db.session.add(players_group)
        db.session.commit()
        return redirect(url_for('players_groups'))
    return render_template('update_players_group.html', form=form, players_group=players_group)


@app.route('/delete_players_group', methods=['GET', 'POST'])
@login_required
def delete_players_group():
    form = PlayersGroupDeleteForm(request.form)

    if request.method == 'POST' and form.validate():
        with db.session.begin(subtransactions=True):
            id = form.id.data
            players_group = PlayersGroup.query.get(id)
            db.session.delete(players_group)
        db.session.commit()
        return redirect(url_for('players_groups'))
    return redirect(url_for('players_groups'))


@app.route('/create_player/<int:belonged_players_group_id>', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('players_in_the_group'))
    return render_template('create_player.html', form=form)


@app.route('/update_player/<int:player_id>', methods=['GET', 'POST'])
@login_required
def update_player(player_id):
    form = PlayerUpdateForm(request.form)
    player = Player.query.get(player_id)

    if request.method == 'POST' and form.validate():
        id = form.id.data
        name = form.name.data
        play_times = form.play_times.data

        with db.session.begin(subtransactions=True):
            player = Player.query.get(id)
            player.name = name
            player.play_times = play_times
        db.session.commit()
        return redirect(url_for('players_in_the_group'))
    return render_template('update_player.html', form=form, player=player)


@app.route('/delete_player', methods=['GET', 'POST'])
@login_required
def delete_player():
    form = PlayerDeleteForm(request.form)

    if request.method == 'POST' and form.validate():
        with db.session.begin(subtransactions=True):
            id = form.id.data
            player = Player.query.get(id)
            db.session.delete(player)
        db.session.commit()
        return redirect(url_for('players_in_the_group'))
    return redirect(url_for('players_in_the_group'))


def init_db():
    with db.session.begin(subtransactions=True):
        new_user = User(username='a', email='a@a.com')
        new_user.save_new_password('iiiiiiii')
        db.session.add(new_user)

        # new_players_group = PlayersGroup(
        #     group_name='init_db', user_id=new_user.id)
        # new_player = Player(name='a', gender='man',
        #                     belonged_players_group_id=new_players_group.id)
        # db.session.add(new_players_group)
        # db.session.add(new_player)
    db.session.commit()
    test_users = User.query.all()
    for user in test_users:
        print(user.username)
        print(user.id)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False, use_debugger=True)
