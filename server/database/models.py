from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from . import connection

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(100))
    password = Column(String(100))


def create_table():
    Base.metadata.create_all(bind=connection.engine)


create_table()