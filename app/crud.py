from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

from passlib.context import CryptContext

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")

def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter_by(username=username).first()
    return user


def get_user_by_id(db: Session, id: int):
    user = db.query(models.User).filter_by(id=id).first()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, username=user.username, type=user.type)
    db_user.hashed_password = pwd_context.hash(user.password)
    db_user.join_date = datetime.utcnow()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserUpdate, id: int):
    db_user = db.query(models.User).filter_by(id=id).first()
    db_user.username = user.username if user.username else db_user.username
    db_user.name = user.name if user.name else db_user.name
    db_user.type = user.type if user.type else db_user.type
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user_by_id(db: Session, id: int):
    db_user = db.query(models.User).filter_by(id=id)
    db_user.delete(synchronize_session=True)
    db.commit()
    return db_user
