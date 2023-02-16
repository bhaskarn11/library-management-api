from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime, timedelta
from typing import List

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
    db_user.delete()
    db.commit()
    return db_user


def get_item_by_id(id: int, db: Session):
    db_item = db.query(models.Item).filter_by(id=id).first()
    return db_item


def create_item(item: schemas.ItemCreate, db: Session):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(item: schemas.ItemUpdate, id: int, db: Session):
    # print(item)
    db_item = db.query(models.Item).filter_by(id=id).first()
    db_item.title = item.title if item.title else db_item.title
    db_item.description = item.description if item.description else db_item.description
    db_item.isbn = item.isbn if item.isbn else db_item.isbn
    db_item.type = item.type if item.type else db_item.type
    db_item.publisher = item.publisher if item.publisher else db_item.publisher

    db.commit()
    db.refresh(db_item)
    return db_item


def remove_item(id: int, db: Session):
    i = db.query(models.Item).filter_by(id=id)
    i.delete()
    db.commit()
    db.refresh()
    return i


def create_borrow(borrow: schemas.BorrowCreate, items, db: Session):
    t = datetime.utcnow()
    db_borrow = models.Borrow(borrower_id=borrow.borrower_id, items=items)
    db_borrow.issue_date = t
    db_borrow.due_date = t + timedelta(days=15)
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow
