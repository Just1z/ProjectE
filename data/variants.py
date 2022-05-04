import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Variants(SqlAlchemyBase):
    __tablename__ = 'variants'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tasks = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=14100)
    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("users.id"))
    user = orm.relation("User")