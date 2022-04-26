import os
import functions
from random import choice
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.variants import Variants
from data.tasks import Task
from data.test_sessions import Test_session
from forms.user import RegisterForm, LoginForm

db_session.global_init("db/kege.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ocPMh2NRBFmFfwgV9t2SMarBX4JzNd'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Вход')
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/profile")
def profile():
    return render_template("profile.html", title='КЕГЭ')


@app.route("/case/<int:id>")
def case(id):
    session = db_session.create_session()
    tasks = session.query(Variants).filter(Variants.id == id).first()
    tasks = tasks.tasks.split(', ')
    data = {"tasks": [], "kim_number": "1", "br_number": 1, "title": "КЕГЭ"}
    answers = []
    for i in range(len(tasks)):
        task = session.query(Task).filter(Task.id == tasks[i]).first()
        text = task.html
        ans = task.answer
        if 'Вопрос 1.' in text:
            ans = [i[3:] for i in ans.split('<br/>')]
            ind2 = text.index('Вопрос 2')
            ind3 = text.index('Вопрос 3')
            data["tasks"].append(text[:ind2].replace('Вопрос 1.', ''))
            data["tasks"].append(text[ind2:ind3].replace('Вопрос 2.', ''))
            data["tasks"].append(text[ind3:].replace('Вопрос 3.', ''))
            answers.extend(ans)
        else:
            data["tasks"].append(text)
            answers.append(ans)
    # Заносим сессию в базу данных
    test_session_code = functions.generate_code() # Код сессии
    # Вероятность получения уже существующего кода -> 0
    test_session = Test_session(id=test_session_code, answers=",".join(answers))
    if current_user.is_authenticated:
        test_session.setUser(current_user)
    session.add(test_session)
    session.commit()
    data["code"] = test_session_code
    return render_template("case.html", **data)


@app.route("/result/", methods=["GET"])
def result():
    code = request.args.get('sess')
    session = db_session.create_session()
    right_answers = session.query(Test_session).filter(
        Test_session.id == code).first().answers.split(",")
    data = {"right_answers": right_answers, "title": "Результаты"}
    return render_template("result.html", **data)


@app.route("/generator")
def generator():
    return render_template("generator.html", title="Генератор")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title='КЕГЭ')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
