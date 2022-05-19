import random
from datetime import datetime

from app import app
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from models import Player, db

from flaskr import db
from flaskr.forms import (CreatePlayerForm, DeletePlayerForm,
                          ForgotPasswordForm, LoginUserForm, RegisterUserForm,
                          ResetPasswordForm, UpdatePlayerForm)

bp = Blueprint('app', __name__, url_prefix='')


def dicide_players(players):
    def get_a_player_by_random(possible_players):
        index = random.randrange(len(possible_players))
        return_player = possible_players[index]
        possible_players.pop(index)
        return return_player

    players.sort(key=lambda player: player.play_times)
    possible_players = []
    if len(players) < 4:
        print("players are less than four")
        return players

    for player in players:
        possible_players.append(player)

    return_players = []
    for index in range(4):

        return_players.append(get_a_player_by_random(possible_players))
    return return_players


def login():
    pass


def logout():
    pass


@app.route('/')
def home():
    pass


@app.route('/players_list')
def players_list():
    players = Player.query.all()
    form = DeletePlayerForm(request.form)
    next_players = dicide_players(players)
    return render_template('players_list.html', players=players, form=form, next_players=next_players)


@app.route('/create_player', methods=['GET', 'POST'])
def create_player():
    form = CreatePlayerForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        age = form.age.data
        gender = form.gender.data

        with db.session.begin(subtransactions=True):
            new_player = Player(name=name, age=age, gender=gender)
            db.session.add(new_player)
        db.session.commit()
        return redirect(url_for('players_list'))
    return render_template('create_player.html', form=form)


@app.route('/update_player/<int:player_id>', methods=['GET', 'POST'])
def update_player(player_id):
    form = UpdatePlayerForm(request.form)
    player = Player.query.get(player_id)
    if request.method == 'POST' and form.validate():
        id = form.id.data
        name = form.name.data
        age = form.age.data
        gender = player.gender
        play_times = form.play_times.data
        with db.session.begin(subtransactions=True):
            player = Player.query.get(id)
            player.name = name
            player.age = age
            player.gender = gender
            player.play_times = play_times
        db.session.commit()
        return redirect(url_for('players_list'))
    return render_template('update_player.html', form=form, player=player)


@app.route('/delete_player', methods=['GET', 'POST'])
def delete_player():
    form = DeletePlayerForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.session.begin(subtransactions=True):
            id = form.id.data
            player = Player.query.get(id)
            db.session.delete(player)
        db.session.commit()
        return redirect(url_for('players_list'))
    return redirect(url_for('players_list'))


if __name__ == '__main__':
    app.run(debug=True)
