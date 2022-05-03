import sqlalchemy
from .db_session import SqlAlchemyBase


class Variants(SqlAlchemyBase):
    __tablename__ = 'variants'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tasks = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=14100)
