from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    number = StringField('Номер задачи', validators=[DataRequired()])
    task = StringField('Условие задачи', validators=[DataRequired()])
    answer = StringField('Ответ', validators=[DataRequired()])
    file1 = FileField('Файл 1')
    file2 = FileField('Файл 2')
    img = FileField('Картинка')
    submit = SubmitField('Добавить')
