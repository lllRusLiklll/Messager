from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    title = StringField('Тема сообщения', validators=[DataRequired()])
    content = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Сохранить')