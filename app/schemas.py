from pydantic import BaseModel
from typing import Union, List
from datetime import date


class ItemBase(BaseModel):
    title: str
    description: Union[str, None]
    isbn: str
    publisher: str
    type: str
    available: bool


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    publish_date: date

    class Config:
        orm_mode = True


class BorrowCreate(BaseModel):
    issuer_id: int
    borrower_id: int
    items: List[Item]


class Borrow(BaseModel):
    id: int
    issue_date: date
    due_date: date
    item: Item

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    username: str
    type: str


class UserCreate(UserBase):
    password: str
    join_date: date


class UserUpdate(UserBase):
    password: str


class User(UserBase):
    id: int
    join_date: date
    borrows: List[Borrow] = []

    class Config:
        orm_mode = True
