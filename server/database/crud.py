from sqlalchemy.orm import Session
import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user_data: dict):
    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
