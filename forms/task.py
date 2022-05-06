from re import fullmatch
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError


def number_check(form, field):
    if not fullmatch(r'^([1-9]|[1][\d]|2[2-7])$', field.data):
        raise ValidationError("Номер задачи должен быть числом от 1 до 27")


class TaskForm(FlaskForm):
    number = StringField('Номер задачи', validators=[DataRequired(), number_check])
    task = StringField('Условие задачи', validators=[DataRequired()])
    answer = StringField('Ответ', validators=[DataRequired()])
    file1 = FileField('Файл 1')
    file2 = FileField('Файл 2')
    img = FileField('Картинка')
    submit = SubmitField('Добавить')
