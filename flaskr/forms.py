from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms.fields import (HiddenField, IntegerField, PasswordField,
                            RadioField, StringField, SubmitField,
                            TextAreaField)
from wtforms.form import Form
from wtforms.validators import DataRequired, Email, EqualTo

from flaskr.models import User


class CreatePlayerForm(FlaskForm):
    age = IntegerField('age:')
    gender = RadioField('gender', choices=[('man', 'man'), ('woman', 'woman')])
    name = StringField('name:')
    submit = SubmitField('submit')


class UpdatePlayerForm(FlaskForm):
    id = HiddenField()
    age = IntegerField('age:')
    gender = HiddenField()
    name = StringField('name:')
    play_times = IntegerField('play_times:')
    submit = SubmitField('submit')


class DeletePlayerForm(FlaskForm):
    id = HiddenField()
    submit = SubmitField('delete')


class LoginUserForm(FlaskForm):
    email = StringField('mail', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


class RegisterUserForm(FlaskForm):
    email = StringField('mail', validators=[
                        DataRequired(), Email('wrong email')])
    username = StringField('name', validators=[DataRequired()])
    password = PasswordField(
        'password', validators=[DataRequired(), EqualTo('password_confirm', message='password is not equal')]
    )
    password_confirm = PasswordField(
        'confirm password', validators=[DataRequired()])
    submit = SubmitField('register')

    def validate_email(self, field):
        if User.select_by_email(field.data):
            raise ValidationError('this email has already been registered')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(), EqualTo(
            'confirm_password', message='password is not equal')]
    )
    confirm_password = PasswordField(
        'confirm_password', validators=[DataRequired()]
    )
    submit = SubmitField('update password')

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('password should be more than 8 character')


class ForgotPasswordForm(FlaskForm):
    email = StringField('mail:', validators=[DataRequired(), Email()])
    submit = SubmitField('register password again')

    def validate_email(self, field):
        if not User.select_user_by_email(field.data):
            raise ValidationError("this email addres doesn't exist")
