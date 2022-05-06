import os
import logging
from base64 import b64encode
from datetime import timedelta
from configparser import ConfigParser
from flask import Flask, render_template, redirect, request
from flask import session as flask_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api, abort
from sqlalchemy.sql.expression import func
from werkzeug.datastructures import FileStorage

from functions import generate_code, normalize_html
from data import db_session
from data.users import User
from data.variants import Variants
from data.tasks import Task
from data.test_sessions import TestSession
from data import task_resources
from forms.user import RegisterForm, LoginForm
from forms.task import TaskForm
from forms.variants import VariantForm

db_session.global_init("db/kege.db")
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
api = Api(app)

config = ConfigParser()
config.read("settings.ini")
app.config["SECRET_KEY"] = config["settings"]["secret_key"]
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(401)
def error401(error):
    return render_template(
        "error.html", title="Не авторизованы",
        text1="Ошибка 401",
        text2="Зарегистрируйтесь или войдите в свой аккаунт, чтобы просматривать данную страницу.")


@app.errorhandler(404)
def error404(error):
    return render_template(
        "error.html", title="Не найдено",
        text1="Ошибка 404", text2="Страница не найдена :/")


@app.errorhandler(500)
def error500(error):
    return render_template(
        "error.html", title="Ошибка",
        text1="Ошибка 500",
        text2="Произошла непредвиденная ошибка. Просим прощения за неудобства.")


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
                'register.html', title='Регистрация', form=form, error_message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   error_message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            login=form.login.data,
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
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               error_message="Неправильный логин или пароль",
                               form=form, title='Вход')
    return render_template('login.html', title='Вход', form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/profile")
@login_required
def profile():
    session = db_session.create_session()
    tasks = session.query(Task).filter(Task.author_id == current_user.id).all()
    tasks = [[t.id, t.html] for t in tasks]
    variants = session.query(Variants).filter(Variants.author_id == current_user.id).all()
    variants = [[v.id, v.tasks] for v in variants]
    return render_template("profile.html", title='КЕГЭ', tasks=tasks, variants=variants)


@app.route("/result/", methods=["GET"])
def result():
    code = request.args.get("sess")
    if not code:
        return redirect("/")
    session = db_session.create_session()
    right_answers = session.query(TestSession).filter(
        TestSession.id == code).first().answers.split(",")
    data = {"right_answers": right_answers, "title": "Результаты"}
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
            if not tasks:
                abort(404)
            tasks_ids = list(map(int, tasks.tasks.split(', ')))
            time = tasks.time
        else:
            var_id = "-"
            for i, count in enumerate(tasks):
                number = i + 1
                if i >= 19:
                    number += 2
                tasks = session.query(Task).filter(
                    Task.number == number).order_by(func.random()).limit(int(count))
                tasks_ids.extend(task.id for task in tasks)
            time = 14100
        flask_session["tasks_ids"] = tasks_ids
        flask_session["var_id"] = var_id
        flask_session["time"] = time
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
    data = {
        "tasks": [], "title": "КЕГЭ",
        "time": flask_session.get("time", 14100),
        "numbers": [], "count": 0, "exam": "false"
        }
    files = []
    answers = []
    tasks = session.query(Task).filter(Task.id.in_(tasks_ids)).all()
    tasks = [next(t for t in tasks if t.id == task_id) for task_id in tasks_ids]
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
            data["count"] += 3
            files.extend((None, None))
            data["numbers"].extend((19, 20, 21))
        else:
            data["tasks"].append(text)
            answers.append(ans)
            data["count"] += 1
            data["numbers"].append(task.number)
        files.append(file)
    # Заносим сессию в базу данных
    test_session_code = generate_code()  # Код сессии
    # Вероятность получения уже существующего кода -> 0
    test_session = TestSession(id=test_session_code, answers=",".join(answers))
    if current_user.is_authenticated:
        test_session.setUser(current_user.id)
    session.add(test_session)
    session.commit()
    data["files"] = files
    data["code"] = test_session_code
    data["kim_number"] = flask_session.get("var_id")
    if data["numbers"] == [i for i in range(1, 28)]:
        data["exam"] = "true"
    return render_template("case.html", **data)


@app.route("/task_database")
def task_database():
    return render_template("task_database.html", title="База заданий")


@app.route("/task_database/")
def show_task():
    if request.args.get("number"):
        number = request.args.get("number")
        session = db_session.create_session()
        if current_user.is_authenticated:
            tasks = session.query(Task).filter(
                Task.number == number, (Task.author_id == 0) | (Task.author_id == current_user.id)).order_by(Task.id).all()
        else:
            tasks = session.query(Task).filter(
                Task.number == number, Task.author_id == 0).order_by(Task.id).all()
        tasks_data = [[t.id, t.html, t.answer, t.files] for t in tasks]
        if tasks_data:
            data = {"title": f"Задание {number if 19 != number else '19-21'}", "tasks": tasks_data}
            return render_template("show_task.html", **data)
        return abort(404)
    elif request.args.get("id"):
        id = request.args.get("id")
        if len(id.split(',')) == 1:
            session = db_session.create_session()
            if current_user.is_authenticated:
                tasks = session.query(Task).filter(
                    Task.id == id, (Task.author_id == 0) | (Task.author_id == current_user.id)).first()
            else:
                tasks = session.query(Task).filter(Task.id == id, Task.author_id == 0).first()
            if tasks:
                number = tasks.number
                tasks_data = [[tasks.id, tasks.html, tasks.answer, tasks.files]]
                data = {"title": f"Задание {number if 19 != number else '19-21'}", "tasks": tasks_data}
            return abort(404)
        else:
            session = db_session.create_session()
            tasks_data = []
            for i in id.split(','):
                tasks = session.query(Task).filter(Task.id == i, Task.author_id == 0).first()
                if tasks:
                    tasks_data.append([tasks.id, tasks.html, tasks.answer])
            data = {"title": "Просмотр варианта", "tasks": tasks_data}
        return render_template("show_task.html", **data)
    return redirect("/task_database")


@app.route("/add_task", methods=["GET", "POST"])
@login_required
def new_task():
    form = TaskForm()
    if request.method == "POST":
        db_sess = db_session.create_session()

        number = form.number.data
        if not number.isnumeric():
            message = "Необходимо ввести корректный номер задачи."
            return render_template(
                "add_task.html", title="Добавить задание", form=form, message=message)
        if not 1 <= int(number) <= 27:
            message = "Необходимо ввести корректный номер задачи."
            return render_template(
                "add_task.html", title="Добавить задание", form=form, message=message)
        if int(number) in ("20", "21"):
            message = "Для задач по теории игр необходимо указывать в поле 'Номер задачи' номер 19."
            return render_template(
                "add_task.html", title="Добавить задание", form=form, message=message)

        condition = form.task.data
        answer = form.answer.data
        file1: FileStorage = form.file1.data
        file2: FileStorage = form.file2.data
        image: FileStorage = form.img.data
        html = f'<p>{condition}</p>'
        if image.filename:
            if "." not in image.filename or not any(
                    ext in image.filename for ext in ("jpeg", "png", "jpg", "gif", "bmp")):
                message = "Ошибка. Изображение является некорректным."
                return render_template(
                    "add_task.html", title="Добавить задание", form=form, message=message)
            ext = image.filename.split(".")[1]
            image.stream.seek(0)
            html += f'<img max-width=500px src="data:image/{ext};base64,{b64encode(image.stream.read()).decode("utf-8")}"/>'

        files = []
        last_task = db_sess.query(Task).order_by(Task.id)[-1]

        if file1.filename:
            if "." not in file1.filename:
                message = "Ошибка. Файл 1 является некорректным"
                return render_template(
                    "add_task.html", title="Добавить задание", form=form, message=message)
            path = f"db/files/{last_task.id + 1}_"
            with open(path + f"1.{file1.filename.split('.')[1]}", "wb") as dst:
                file1.stream.seek(0)
                file1.save(dst)
                files.append(path + f"1.{file1.filename.split('.')[1]}")
            if file2.filename:
                if "." not in file2.filename:
                    message = "Ошибка. Файл 2 является некорректным"
                    return render_template(
                        "add_task.html", title="Добавить задание", form=form, message=message)
                with open(path + f"2.{file2.filename.split('.')[1]}", "wb") as dst:
                    file2.stream.seek(0)
                    file2.save(dst)
                    files.append(path + f"1.{file1.filename.split('.')[1]}")
        if not file1.filename and file2.filename:
            message = "Ошибка. Отсутствует файл 1"
            return render_template(
                "add_task.html", title="Добавить задание", form=form, message=message)
        task = Task(
            html=html,
            answer=answer,
            files=" ".join(map(lambda i, path: f'<a href="{path}">Файл {i}</a>', enumerate(files, 1))),
            number=number,
            author_id=current_user.id
        )
        db_sess.add(task)
        db_sess.commit()
        app.logger.info(f"{current_user} added new task. Task ID: {last_task.id + 1}")
        return redirect("/task_database")
    return render_template("add_task.html", title="Добавить задание", form=form)


@app.route('/task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    form = TaskForm()
    if request.method == "GET":
        session = db_session.create_session()
        tasks = session.query(Task).filter(Task.id == id, Task.author_id == current_user.id).first()
        if tasks:
            form.number.data = tasks.number
            form.task.data = tasks.html
            form.answer.data = tasks.answer
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        tasks = session.query(Task).filter(Task.id == id).first()
        if tasks:
            tasks.number = form.number.data
            tasks.html = form.task.data
            tasks.answer = form.answer.data

            file1: FileStorage = form.file1.data
            file2: FileStorage = form.file2.data
            files = []
            last_task = session.query(Task).order_by(Task.id)[-1]
            if file1.filename or file2.filename:
                if file1.filename:
                    if "." not in file1.filename:
                        message = "Ошибка. Файл 1 является некорректным"
                        return render_template(
                            "edit_task.html", title="Добавить задание", form=form, message=message)
                    path = f"db/files/{last_task.id + 1}_"
                    with open(path + f"1.{file1.filename.split('.')[1]}", "wb") as dst:
                        file1.stream.seek(0)
                        file1.save(dst)
                    if file2.filename:
                        if "." not in file2.filename:
                            message = "Ошибка. Файл 2 является некорректным"
                            return render_template(
                                "edit_task.html", title="Добавить задание", 
                                form=form, message=message)
                        with open(path + f"2.{file2.filename.split('.')[1]}", "wb") as dst:
                            file2.stream.seek(0)
                            file2.save(dst)
                if not file1.filename and file2.filename:
                    message = "Ошибка. Отсутствует файл 1"
                    return render_template(
                        "edit_task.html", title="Добавить задание", form=form, message=message)
                tasks.files = " ".join(map(lambda e: f'<a href="{e}"</a>', files))
            session.commit()
            return redirect('/profile')
        else:
            abort(404)
    return render_template('edit_task.html', title='Редактировать задачу', form=form)


@app.route('/task_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def task_delete(id):
    session = db_session.create_session()
    task = session.query(Task).filter(Task.id == id, Task.author_id == current_user.id).first()
    if task:
        session.delete(task)
        session.commit()
    else:
        abort(404)
    return redirect('/profile')


@app.route("/add_variant", methods=['GET', 'POST'])
@login_required
def add_variant():
    form = VariantForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        variant = Variants(tasks=', '.join(form.task.raw_data),
                           time=int(form.time.data) * 60,
                           author_id=current_user.id)
        session.add(variant)
        session.commit()
        return redirect('/')
    return render_template('add_variant.html', title='Создание варианта', form=form)


@app.route('/variant/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_variant(id):
    form = VariantForm()
    if request.method == "GET":
        session = db_session.create_session()
        variants = session.query(Variants).filter(
            Variants.id == id, Variants.author_id == current_user.id).first()
        if variants:
            tasks = variants.tasks.split(', ')
            form.time.data = variants.time
            return render_template('edit_variant.html', title='Редактировать вариант',
                form=form, tasks=tasks, count=len(tasks))
        abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        variants = session.query(Variants).filter(Variants.id == id).first()
        if variants:
            variants.tasks = ', '.join(form.task.raw_data)
            variants.time = form.time.data
            session.commit()
            return redirect('/profile')
        else:
            abort(404)
    return render_template('edit_task.html', title='Редактировать задачу', form=form)


@app.route('/variant_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def variant_delete(id):
    session = db_session.create_session()
    variant = session.query(Variants).filter(
        Variants.id == id, Variants.author_id == current_user.id).first()
    if variant:
        session.delete(variant)
        session.commit()
    else:
        abort(404)
    return redirect('/profile')


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title='КЕГЭ')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    api.add_resource(task_resources.TaskListResources, '/api/tasks/')
    api.add_resource(task_resources.TaskResource, '/api/tasks/<int:task_id>')
    app.run(host="0.0.0.0", port=port)
