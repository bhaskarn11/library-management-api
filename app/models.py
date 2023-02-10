from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from .database import Base

import enum


class UserTypes(enum.Enum):
    BORROWER = "BORROWER"
    STAFF = "STAFF"
    ADMIN = "ADMIN"


class ItemTypes(enum.Enum):
    BOOK = "BOOK"
    JOURNAL = "JOURNAL"
    MAGAZINE = "MAGAZINE"
    NEWSPAPER = "NEWSPAPER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    join_date = Column(Date)
    type = Column(Enum(UserTypes, name="UserTypes", create_constraint=True))

    borrows = relationship("Borrow", back_populates="borrower")


# class Borrower(Base):
#     __tablename__ = "borrowers"
#     id = Column(Integer, primary_key=True, index=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    isbn = Column(String, nullable=True, unique=True)
    publish_date = Column(Date)
    publisher = Column(String)
    available = Column(Boolean, default=True)
    type = Column(Enum(ItemTypes, name="ItemTypes", create_constraint=True))


# class Author(Base):
#     __tablename__ = "authors"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#
#     books = relationship("Book", back_populates="")


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    issue_date = Column(Date)
    due_date = Column(Date)
    item_id = Column(Integer, ForeignKey("items.id"))
    items = relationship("Item")
    issuer_id = Column(Integer, ForeignKey("users.id"))
    borrower_id = Column(Integer, ForeignKey("users.id"))

    borrower = relationship("User", back_populates="borrows")
