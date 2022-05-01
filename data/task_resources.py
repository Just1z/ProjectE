import flask
from flask import jsonify, request
from flask_restful import Resource, abort, reqparse

from . import db_session
from .tasks import Task
from .users import User

blueprint = flask.Blueprint(
    'task_api',
    __name__,
    template_folder='templates'
)

parser = reqparse.RequestParser()
parser.add_argument("id", required=True, type=int)
parser.add_argument("html", required=True)
parser.add_argument("answer", required=True)
parser.add_argument("files", required=False, default="")


def is_entry(task_id):
    """
    Проверка существования записи в базе данных с таким task_id. В случае отсутствия записи
    принудительно отправляет 404 ошибку с соответствующим сообщением.
    :param task_id: поле id в таблице tasks
    :return: None
    """
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if not task:
        abort(404, message=f"error: {task_id} not found")


@blueprint.route("/api/v1/tasks")
def get_tasks():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).all()
    return jsonify(
        {
            "tasks":
                [item.to_dict(only=("id", "html", "answer", "files"))
                 for item in tasks]
        }
    )


@blueprint.route("/api/v1/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).get(task_id)
    if not tasks:
        return jsonify({"message": "error: task not found"})
    return jsonify(
        {
            "tasks": tasks.to_dict(only=(
                "id", "html", "answer", "files"))
        }
    )


@blueprint.route("/api/v1/tasks", methods=["POST"])
def new_task():
    if not request.json:
        return jsonify({"message": "error: empty request"})
    elif not all(key in request.json for key in
                 ["id", "html", "answer", "files"]):
        return jsonify({"message": "error: bad request"})
    try:
        db_sess = db_session.create_session()
        task = Task(
            id=request.json["id"],
            html=request.json["html"],
            answer=request.json["answer"],
            files=request.json["files"]
        )
        db_sess.add(task)
        db_sess.commit()
        return jsonify({"message": "success"})
    except Exception as error:
        return jsonify({"error": str(error)})


@blueprint.route("/api/v1/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db_sess = db_session.create_session()

    task = db_sess.query(Task).get(task_id)
    if not task:
        return jsonify({"message": "error: task not found"})
    try:
        db_sess.delete(task)
        db_sess.commit()
        return jsonify({"message": "success"})
    except Exception as error:
        return jsonify({"message": "error: " + str(error)})


class TaskResource(Resource):
    def get(self, task_id):
        is_entry(task_id)
        session = db_session.create_session()
        task = session.query(Task).get(task_id)
        return jsonify({"task": task.to_dict(
            only=("id", "html", "answer", "files"))})

    def delete(self, task_id):
        is_entry(task_id)
        session = db_session.create_session()
        task = session.query(Task).get(task_id)
        session.delete(task)
        session.commit()
        return jsonify({"message": "success"})

    def put(self, task_id):
        db_sess = db_session.create_session()
        task = db_sess.query(Task).get(task_id)
        if not task:
            return jsonify({"message": "error: task not found"})
        elif not request.json:
            return jsonify({"message": "error: empty request"})
        if request.json.get("id"):
            task.team_leader = request.json["id"]
        if request.json.get("html"):
            task.job = request.json["html"]
        if request.json.get("answer"):
            task.work_size = request.json["answer"]
        if request.json.get("files"):
            task.collaborators = request.json["files"]
        db_sess.commit()
        return jsonify({"message": "success"})


class TaskListResources(Resource):
    def get(self):
        session = db_session.create_session()
        task = session.query(Task).all()
        return jsonify({"task": [item.to_dict(
            only=("id", "html", "answer", "files")) for item in task]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        task = Task(
            id=args["id"],
            html=args["html"],
            answer=args["answer"],
            files=args["files"]
        )
        session.add(task)
        session.commit()
        return jsonify({"message": "success"})
