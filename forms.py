from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (HiddenField, IntegerField, PasswordField,
                            RadioField, StringField, SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo

from models import User


class UserLoginForm(FlaskForm):

    username = StringField('name:')
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


# 登録用のForm
class UserRegisterForm(FlaskForm):
    email = StringField(
        'email:', validators=[DataRequired(), Email('Wrong Email Address')]
    )
    username = StringField('name:', validators=[DataRequired()])
    submit = SubmitField('register')

    def validate_email(self, field):
        if User.select_user_by_email(field.data):
            raise ValidationError('this Email Address is used')

# パスワード設定用のフォーム


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'パスワード',
        validators=[DataRequired(), EqualTo(
            'confirm_password', message='パスワードが一致しません')]
    )
    confirm_password = PasswordField(
        'パスワード確認: ', validators=[DataRequired()]
    )
    submit = SubmitField('パスワードを更新する')

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは8文字以上です')


class ForgotPasswordForm(FlaskForm):
    email = StringField('メール: ', validators=[DataRequired(), Email()])
    submit = SubmitField('パスワードを再設定する')

    def validate_email(self, field):
        if not User.select_user_by_email(field.data):
            raise ValidationError('そのメールアドレスは存在しません')


class UserForm(FlaskForm):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email('メールアドレスが誤っています')]
    )
    username = StringField('名前: ', validators=[DataRequired()])
    submit = SubmitField('登録情報更新')

    def validate(self):
        if not super(Form, self).validate():
            return False
        user = User.select_user_by_email(self.email.data)
        if user:
            if user.id != int(current_user.get_id()):
                flash('そのメールアドレスはすでに登録されています')
                return False
        return True


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'パスワード',
        validators=[DataRequired(), EqualTo(
            'confirm_password', message='パスワードが一致しません')]
    )
    confirm_password = PasswordField(
        'パスワード確認: ', validators=[DataRequired()]
    )
    submit = SubmitField('パスワードの更新')

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは8文字以上です')


class PlayerCreateForm(FlaskForm):
    name = StringField('name:')
    gender = RadioField('gender', choices=[('man', 'man'), ('woman', 'woman')])
    submit = SubmitField('submit')


class PlayerUpdateForm(FlaskForm):
    id = HiddenField()
    name = StringField('name:')
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
    submit = SubmitField('update')


class PlayersGroupDeleteForm(FlaskForm):
    id = HiddenField()
    submit = SubmitField('delete')
