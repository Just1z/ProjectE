import os
from datetime import timedelta
from configparser import ConfigParser
from flask import Flask, render_template, redirect, request
from flask import session as flask_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from sqlalchemy.sql.expression import func
from functions import generate_code, to_100, normalize_html
from data import db_session
from data.users import User
from data.variants import Variants
from data.tasks import Task
from data.test_sessions import TestSession
from data import task_resources
from forms.user import RegisterForm, LoginForm

db_session.global_init("db/kege.db")
app = Flask(__name__)
api = Api(app)
config = ConfigParser()
config.read("settings.ini")
app.config["SECRET_KEY"] = config["settings"]["secret_key"]
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
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
            return render_template(
                'register.html', title='Регистрация', form=form, message="Пароли не совпадают")
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


@app.route("/case/<int:case_id>")
def case(case_id):
    session = db_session.create_session()
    tasks = session.query(Variants).filter(Variants.id == case_id).first()
    tasks_ids = list(map(int, tasks.tasks.split(', ')))
    flask_session["var_id"] = str(case_id)
    return test(tasks_ids)


@app.route("/result/", methods=["GET"])
def result():
    code = request.args.get("sess")
    session = db_session.create_session()
    right_answers = session.query(TestSession).filter(
        TestSession.id == code).first().answers.split(",")
    primary_points = 0
    #answers = 
    data = {"right_answers": right_answers, "title": "Результаты",
            "primary_points": primary_points, "secondary_points": to_100(primary_points)}
    return render_template("result.html", **data)


@app.route("/generator", methods=["GET", "POST"])
def generator():
    if request.method == "POST":
        for i in request.form.lists():
            if i[0] == "task_input":
                tasks = i[1]
            if i[0] == "var_id":
                var_id = i[1][0]
        session = db_session.create_session()
        tasks_ids = []
        if var_id:
            tasks = session.query(Variants).filter(Variants.id == var_id).first()
            tasks_ids = list(map(int, tasks.tasks.split(', ')))
        else:
            for i, count in enumerate(tasks):
                number = i + 1
                if i >= 19:
                    number += 2
                tasks = session.query(Task).filter(
                    Task.number ==number).order_by(func.random()).limit(int(count))
                tasks_ids.extend(task.id for task in tasks)
        flask_session["tasks_ids"] = tasks_ids
        flask_session["var_id"] = "-"
        return redirect("/test", 301)
    return render_template("generator.html", title="Генератор")


@app.route("/test")
def test(tasks_ids=None):
    if not tasks_ids:
        if flask_session.get("tasks_ids", []):
            tasks_ids = flask_session.get("tasks_ids")
        else:
            return redirect("/", 304)
    session = db_session.create_session()
    data = {"tasks": [], "title": "КЕГЭ", "time": 14100, "numbers": [], "count": 0}
    files = []
    answers = []
    tasks = session.query(Task).filter(Task.id.in_(tasks_ids)).all()
    tasks = [next(t for t in tasks if t.id == t_id) for t_id in tasks_ids]
    for task in tasks:
        text = normalize_html(task.html)
        ans = task.answer
        file = task.files
        if 'Вопрос 1.' in text:
            ans = [i[3:] for i in ans.split('<br/>')]
            ind2 = text.index('Вопрос 2')
            ind3 = text.index('Вопрос 3')
            data["tasks"].append(text[:ind2].replace('Вопрос 1.', ''))
            data["tasks"].append(text[ind2:ind3].replace('Вопрос 2.', ''))
            data["tasks"].append(text[ind3:].replace('Вопрос 3.', ''))
            answers.extend(ans)
            files.extend((None, None))
            data["numbers"].extend((19, 20, 21))
            data["count"] += 3
        else:
            data["tasks"].append(text)
            answers.append(ans)
            data["numbers"].append(task.number)
            data["count"] += 1
        files.append(file)
    test_session_code = generate_code()
    test_session = TestSession(id=test_session_code, answers=",".join(answers))
    if current_user.is_authenticated:
        test_session.setUser(current_user.id)
    session.add(test_session)
    session.commit()
    data["files"] = files
    data["code"] = test_session_code
    if flask_session.get("var_id"):
        data["kim_number"] = flask_session.get("var_id")
    return render_template("case.html", **data)


@app.route("/task_database")
def task_database():
    return render_template("task_database.html", title="База заданий")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title='КЕГЭ')


@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html", title="Страница не найдена")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.register_blueprint(task_resources.blueprint)
    api.add_resource(task_resources.TaskListResources, '/api/v2/tasks/')
    api.add_resource(task_resources.TaskResource, '/api/v2/tasks/<int:task_id>')
    app.run(host="0.0.0.0", port=port)
