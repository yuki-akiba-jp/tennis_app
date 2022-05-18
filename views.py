import random

from flask import redirect, render_template, request, url_for

from app import app
from forms import CreateForm, DeleteForm, UpdateForm
from models import Member, db


def dicide_players(members):
    def get_a_player_by_random(possible_players):
        index = random.randrange(len(possible_players))
        return_player = possible_players[index]
        possible_players.pop(index)
        return return_player

    members.sort(key=lambda member: member.play_times)
    possible_players = []
    if len(members) < 4:
        print("players are less than four")
        return members

    for member in members:
        possible_players.append(member)

    return_players = []
    for index in range(4):

        return_players.append(get_a_player_by_random(possible_players))
    return return_players


@app.route('/')
@app.route('/members_list')
def members_list():
    members = Member.query.all()
    form = DeleteForm(request.form)
    next_players = dicide_players(members)
    return render_template('members_list.html', members=members, form=form, next_players=next_players)


@app.route('/create_member', methods=['GET', 'POST'])
def create_member():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        age = form.age.data
        gender = form.gender.data

        with db.session.begin(subtransactions=True):
            new_member = Member(name=name, age=age, gender=gender)
            db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('members_list'))
    return render_template('create_member.html', form=form)


@app.route('/update_member/<int:member_id>', methods=['GET', 'POST'])
def update_member(member_id):
    form = UpdateForm(request.form)
    member = Member.query.get(member_id)
    if request.method == 'POST' and form.validate():
        id = form.id.data
        name = form.name.data
        age = form.age.data
        gender = member.gender
        play_times = form.play_times.data
        with db.session.begin(subtransactions=True):
            member = Member.query.get(id)
            member.name = name
            member.age = age
            member.gender = gender
            member.play_times = play_times
        db.session.commit()
        return redirect(url_for('members_list'))
    return render_template('update_member.html', form=form, member=member)


@app.route('/delete_member', methods=['GET', 'POST'])
def delete_member():
    form = DeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.session.begin(subtransactions=True):
            id = form.id.data
            member = Member.query.get(id)
            db.session.delete(member)
        db.session.commit()
        return redirect(url_for('members_list'))
    return redirect(url_for('members_list'))


if __name__ == '__main__':
    app.run(debug=True)
