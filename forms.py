from wtforms import Form
from wtforms.fields import (HiddenField, IntegerField, StringField,
                            SubmitField, TextAreaField)


class CreateForm(Form):
    # 新しいメンバーを作るためのフォーム
    name = StringField('名前は:')
    age = IntegerField('年齢は:')
    comment = TextAreaField('コメント:')
    submit = SubmitField('作成')


class UpdateForm(Form):
    # メンバー情報を更新するフォーム
    id = HiddenField()
    name = StringField('名前は:')
    age = IntegerField('年齢は:')
    comment = TextAreaField('コメント:')
    submit = SubmitField('更新')


class DeleteForm(Form):
    # メンバー情報を削除するフォーム
    id = HiddenField()
    submit = SubmitField('削除')
