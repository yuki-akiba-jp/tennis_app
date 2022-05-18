from wtforms import Form
from wtforms.fields import (HiddenField, IntegerField, RadioField, StringField,
                            SubmitField, TextAreaField)


class CreateForm(Form):
    age = IntegerField('age:')
    gender = RadioField('gender', choices=[('man', 'man'), ('woman', 'woman')])
    name = StringField('name:')
    submit = SubmitField('submit')


class UpdateForm(Form):
    id = HiddenField()
    age = IntegerField('age:')
    gender = HiddenField()
    name = StringField('name:')
    play_times = IntegerField('play_times:')
    submit = SubmitField('submit')


class DeleteForm(Form):
    id = HiddenField()
    submit = SubmitField('delete')
