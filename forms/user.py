import re
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError

VALID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"

def login_check(form, field):
    if not re.fullmatch(r'^[a-zA-ZА-Яа-яёЁ0-9_-]{3,20}$', field.data):
        raise ValidationError(
            'Логин должен состоять из 3-20 символов латиницы, кириллицы, цифр, "-" и "_". ')


def password_check(form, field):
    if not re.fullmatch(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z-]{8,30}$', field.data):
        raise ValidationError(
            'Пароль должен состоять из 8-30 символов, и иметь прописные '
            ' и строчные буквы латиницы, а также цифры')


def name_check(form, field):
    if not re.fullmatch(r'^[А-Яа-яёЁ]{2,}$', field.data):
        raise ValidationError('Имя должно состоять только из букв кириллицы')


class RegisterForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), login_check])
    password = PasswordField('Password', validators=[DataRequired(), password_check])
    password_again = PasswordField('Repeat password', validators=[
        DataRequired(), EqualTo('password_again', message='Пароли должны совпадать')])
    surname = StringField('Surname', validators=[DataRequired(), name_check])
    name = StringField('Name', validators=[DataRequired(), name_check])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')