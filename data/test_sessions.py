import sqlalchemy
from .db_session import SqlAlchemyBase


class Test_session(SqlAlchemyBase):
    __tablename__ = 'test_sessions'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
        sqlalchemy.ForeignKey("users.id"), nullable=True)
    answers = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user = sqlalchemy.orm.relation('User')

    def setUser(self, user_id):
        self.user = user_id
