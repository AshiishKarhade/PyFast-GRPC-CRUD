from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
import connection
from contextlib import contextmanager

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(100))
    password = Column(String(100))


def create_table():
    Base.metadata.create_all(bind=connection.engine)


@contextmanager
def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db, name, email, password):
    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def main():
    # Create table if not exists
    create_table()
    # Test CRUD operation
    with get_db() as db:
        user = create_user(db, name="John Doe", email="john@example.com", password="secret")
        print("User created:", user)


if __name__ == "__main__":
    main()