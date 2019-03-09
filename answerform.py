from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    title = StringField('Тема сообщения', validators=[DataRequired()])
    content = TextAreaField('Сообщение', validators=[DataRequired()])
    file = FileField('Добавить файл')
    submit = SubmitField('Добавить')