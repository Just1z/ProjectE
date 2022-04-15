import csv
import base64
from data import db_session
from data.tasks import Task


db_session.global_init("db/kege.db")
session = db_session.create_session()
answers = open('kpolyakov/answers.csv', encoding="utf8")
reader = csv.reader(answers, delimiter=',', quotechar='"')
next(reader)
session.query(Task).delete()
for index, row in enumerate(reader):
    if index == 27:
        break
    img = open(f"tasks/1/{index + 1}.png", "rb")
    encoded_string = base64.b64encode(img.read())
    html = f"""<img src="data:image/png;base64, {encoded_string}"/>"""
    task = Task(id=f"1_{index + 1}", html=html, answer=row[1])
    session.add(task)
    print(f"Added task {index + 1}")

session.commit()
print("Done")
