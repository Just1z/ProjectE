from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class VariantForm(FlaskForm):
    task = IntegerField('ID задачи', validators=[DataRequired()])
    time = IntegerField('Время на прохождения экзамена (в минутах)', validators=[DataRequired()])
    submit = SubmitField('Добавить')