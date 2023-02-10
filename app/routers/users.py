from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Union

from ..database import get_db
from ..schemas import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{id}", response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):
    pass


@router.post("/")
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    pass


@router.patch("/{id}")
def patch_user():
    pass


@router.delete("/{id}")
def delete_user():
    pass


