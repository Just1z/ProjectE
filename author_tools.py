"""Инструменты для добавления на сайт авторских задач"""
from requests import get, post, put, delete

LOGIN_ = "login"
PASSWORD_ = "password"
BASE_URL = "http://192.168.43.230:5000/api/tasks/"


def get_task(task_id):
    """Возвращает информацию о task_id, если существует такая запись. Иначе bad request"""
    url = BASE_URL + str(task_id)
    response = get(url)
    return response.json()


def get_tasks():
    """Возвращает информацию о всех задачах в базе"""
    response = get(BASE_URL)
    return response.json()


def put_task(task_id, email, password, **put_data):
    """Вносит изменение в задание с task_id, если автор задачи - это автор запроса.
    put_data = {"id": new_id,
        "html": new_html,
        "answer": new_answer,
        "files": new_files,
        "number": new_number}"""
    url = BASE_URL + str(task_id)
    data = {"email": email, "password": password}
    data.update(put_data)
    response = put(url, json=data)
    return response.json()


def delete_task(task_id, email, password):
    """Удаляет запись о task_id, если автор задачи - это автор запроса"""
    url = BASE_URL + str(task_id)
    login_data = {"email": email, "password": password}
    response = delete(url, json=login_data)
    return response.json()


def post_task(email, password, **post_data):
    """Добавляет запись о задаче под авторством того, кто отправил запрос
    post_data = {
        "id": task_id",
        "html": html_text,
        "answer": answ,
        "number": number,
        "files": files}"""
    data = {"email": email, "password": password}
    data.update(post_data)
    response = post(BASE_URL, json=data)
    return response.json()
