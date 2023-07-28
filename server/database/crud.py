from contextlib import contextmanager
from sqlalchemy.orm import Session
from . import connection
from . import models


@contextmanager
def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_user(db: Session, user_id: int):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     return user


def create_user(name, email, password):
    with get_db() as db:
        user = models.User(name=name, email=email, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_all_users():
    with get_db() as db:
        users = db.query(models.User).all()
    return users


def get_user_by_id(user_id):
    with get_db() as db:
        user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def update_user(user_id, name, email, password):
    with get_db() as db:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.name = name
            user.email = email
            user.password = password
            db.commit()
            db.refresh(user)
    return user


def delete_user(user_id):
    with get_db() as db:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
    return user


def main():
    # Test CRUD operation
    with get_db() as db:
        user = create_user(name="John Doe", email="john@example.com", password="secret")
        print("User created:", user)


if __name__ == "__main__":
    main()