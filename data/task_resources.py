from flask import jsonify, request, make_response
from flask_restful import Resource, abort, reqparse
from flask_login import current_user

from main import app

from . import db_session
from .tasks import Task
from .users import User

parser = reqparse.RequestParser()
parser.add_argument("id", required=True, type=int)
parser.add_argument("html", required=True)
parser.add_argument("answer", required=True)
parser.add_argument("files", required=False, default="")
parser.add_argument("number", required=True, type=int)


def log_info(func):
    def wrapper(*args, **kwargs):
        message = f"api {request.remote_addr} - {func.__doc__}; kwargs: {kwargs}."
        app.logger.info(message)
        return func(*args, **kwargs)

    return wrapper


def check_entry(task_id):
    """
    Проверка существования записи в базе данных с таким task_id. В случае отсутствия записи
    принудительно отправляет 404 ошибку с соответствующим сообщением.
    :param task_id: поле id в таблице tasks
    :return: None
    """
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if not task:
        log_message = f"{request.remote_addr} - error: {task_id} not found"
        app.logger.info(log_message)
        abort(404, message=f"error: {task_id} not found")


def check_authentication():
    """
    Проверка аутентификации в системе для корректной работы api. В случае отсутствия аутентификации
    принудительно отправляет 401 ошибку с соответствующим сообщением. Иначе возвращает user_id
    :return: user_id
    """
    if not request.json:
        return abort(400, message=f"error: empty request")
    elif not all(key in request.json for key in ["login", "password"]):
        return abort(400, message=f"error: bad request")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == request.json["login"]).first()
    if user and user.check_password(request.json["password"]):
        app.logger.info(f"api {request.remote_addr} - logged in as User(id={user.id})")
        return user.id
    log_message = f"api {request.remote_addr} - error: unauthorized"
    app.logger.info(log_message)
    abort(401, message=f"error: unauthorized")


def check_permission(task_id, user_id):
    """
    Проверка на авторство задачи (имеет ли user право на правку заданий). В случае отсутствия записи
    принудительно отправляет 400 ошибку с соответствующим сообщением.
    :param task_id: поле id в таблице tasks
    :param user_id: поле author_id в таблице tasks, id в таблице users
    :return: None
    """
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if task.author_id not in (0, user_id):
        log_message = f"api {request.remote_addr} User(id={user_id}) Task(id={task_id}) - error: access denied"
        app.logger.warning(log_message)
        abort(400, message=f"error: forbidden")


class TaskResource(Resource):
    @log_info
    def get(self, task_id):
        """TaskResource.get()"""
        check_entry(task_id)

        session = db_session.create_session()
        task = session.query(Task).get(task_id)
        return jsonify({"task": task.to_dict(
            only=("id", "html", "answer", "files"))})

    @log_info
    def delete(self, task_id):
        """TaskResource.delete()"""
        check_entry(task_id)
        user_id = check_authentication()
        check_permission(task_id, user_id)

        session = db_session.create_session()
        task = session.query(Task).get(task_id)
        session.delete(task)
        session.commit()
        return jsonify({"message": "success"})

    @log_info
    def put(self, task_id):
        """TaskResources.put()"""
        check_entry(task_id)
        user_id = check_authentication()
        check_permission(task_id, user_id)

        db_sess = db_session.create_session()
        task = db_sess.query(Task).get(task_id)
        if not task:
            return jsonify({"message": "error: task not found"})
        elif not request.json:
            return jsonify({"message": "error: empty request"})
        if request.json.get("id"):
            task.id = request.json["id"]
        if request.json.get("html"):
            task.html = request.json["html"]
        if request.json.get("answer"):
            task.answer = request.json["answer"]
        if request.json.get("files"):
            task.files = request.json["files"]
        if request.json.get("number"):
            task.number = request.json["number"]

        db_sess.commit()
        return jsonify({"message": "success"})


class TaskListResources(Resource):
    @log_info
    def get(self):
        """TaskListResources.get()"""
        session = db_session.create_session()
        task = session.query(Task).all()
        return jsonify({"task": [item.to_dict(
            only=("id", "html", "answer", "files")) for item in task]})

    @log_info
    def post(self):
        """TaskListResources.post()"""
        user_id = check_authentication()
        args = parser.parse_args()
        session = db_session.create_session()
        task = Task(
            id=args["id"],
            html=args["html"],
            answer=args["answer"],
            files=args["files"],
            number=args["number"],
            author_id=user_id
        )
        session.add(task)
        session.commit()
        return jsonify({"message": "success"})
