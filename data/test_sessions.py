import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class TestSession(SqlAlchemyBase):
    __tablename__ = 'test_sessions'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"), nullable=True)
    answers = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user = orm.relation('User')

    def setUser(self, user_id):
        self.user_id = user_id
