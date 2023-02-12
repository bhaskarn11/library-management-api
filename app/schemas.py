from pydantic import BaseModel
from typing import Union, List
from datetime import date
from enum import Enum


class AuthorBase(BaseModel):
    name: str


class Author(AuthorBase):
    id: int


class ItemBase(BaseModel):
    title: str
    description: Union[str, None]
    isbn: str
    publisher: str
    type: str


class ItemCreate(ItemBase):
    available: bool = True
    publish_date: date = '2022-02-01'
    authors: List[AuthorBase] = []



class ItemUpdate(ItemBase):
    title: Union[str, None]
    isbn: Union[str, None]
    publisher: Union[str, None]
    type: Union[str, None]


class Item(ItemBase):
    id: int
    publish_date: date
    type: Enum
    available: bool
    authors: List[Author] = []
    class Config:
        orm_mode = True


class BorrowItem(BaseModel):
    item_id: int

class BorrowCreate(BaseModel):
    
    borrower_id: int
    items: List[BorrowItem]


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


class UserUpdate(BaseModel):
    name: Union[str, None]
    username: Union[str, None]
    type: Union[str, None]


class User(UserBase):
    id: int
    join_date: date
    disabled: bool
    type: Enum
    borrows: List[Borrow] = []

    class Config:
        orm_mode = True
