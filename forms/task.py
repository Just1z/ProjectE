from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    number = StringField('Номер задачи', validators=[DataRequired()])
    task = StringField('Условие задачи', validators=[DataRequired()])
    answer = StringField('Ответ', validators=[DataRequired()])
    files = FileField('Файлы')
    img = FileField('Картинка')
    submit = SubmitField('Добавить')
