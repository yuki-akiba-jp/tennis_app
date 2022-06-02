from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (HiddenField, IntegerField, PasswordField,
                            SelectField, StringField, SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo

from models import User


class UserLoginForm(FlaskForm):

    username = StringField('username:')
    email = StringField(
        'email:', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'password:',
        validators=[DataRequired(),
                    EqualTo('confirm_password', message='again')]
    )
    confirm_password = PasswordField(
        'password again', validators=[DataRequired()]
    )
    submit = SubmitField('login')


class UserUpdateForm(FlaskForm):
    id = HiddenField()
    username = StringField('username:')
    email = StringField(
        'email:', validators=[DataRequired(), Email()]
    )
    submit = SubmitField('update')


class UserRegisterForm(FlaskForm):
    email = StringField(
        'email:', validators=[DataRequired(), Email('Wrong Email Address')]
    )
    username = StringField('name:', validators=[DataRequired()])
    submit = SubmitField('register')

    def validate_email(self, field):
        if User.select_user_by_email(field.data):
            raise ValidationError('this Email Address is used')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(), EqualTo(
            'confirm_password', message='password is not same')]
    )
    confirm_password = PasswordField(
        'confirm_password', validators=[DataRequired()]
    )
    submit = SubmitField('update password')

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('password should be more than 8 characters')


class ForgotPasswordForm(FlaskForm):
    email = StringField('mail:', validators=[DataRequired(), Email()])
    submit = SubmitField('set new password')

    def validate_email(self, field):
        if not User.select_user_by_email(field.data):
            raise ValidationError("this email does't exist")


class UserForm(FlaskForm):
    email = StringField(
        'email:', validators=[DataRequired(), Email('email address is wrong')]
    )
    username = StringField('name:', validators=[DataRequired()])
    submit = SubmitField('update user infomation')

    def validate(self):
        if not super(FlaskForm, self).validate():
            return False
        user = User.select_user_by_email(self.email.data)
        if user:
            if user.id != int(current_user.get_id()):
                flash('this email address is already used')
                return False
        return True


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(), EqualTo(
            'confirm_password', message='password is not same')]
    )
    confirm_password = PasswordField(
        'confirm_password', validators=[DataRequired()]
    )
    submit = SubmitField('update password')

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError("this email does't exist")


class PlayerCreateForm(FlaskForm):
    name = StringField('name:')
    gender = SelectField('gender', choices=[
                         ('man', 'man'), ('woman', 'woman')])
    submit = SubmitField('submit')


class PlayerUpdateForm(FlaskForm):
    id = HiddenField()
    name = StringField('name:')
    gender = SelectField('gender', choices=[
                         ('man', 'man'), ('woman', 'woman')])
    play_times = IntegerField('play_times:')
    submit = SubmitField('update')


class PlayerDeleteForm(FlaskForm):
    id = HiddenField()
    submit = SubmitField('delete')


class PlayersGroupCreateForm(FlaskForm):
    group_name = StringField('group_name')
    submit = SubmitField('submit')


class PlayersGroupUpdateForm(FlaskForm):
    id = HiddenField()
    group_name = StringField('name:')
    submit = SubmitField('update group name')


class PlayersGroupDeleteForm(FlaskForm):
    id = HiddenField()
    submit = SubmitField('delete')
