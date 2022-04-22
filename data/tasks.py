import sqlalchemy
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    html = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
