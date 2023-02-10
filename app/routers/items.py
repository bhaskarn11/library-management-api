from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Union

from ..database import get_db
from ..schemas import ItemCreate, ItemUpdate, Item

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@router.get("/{id}", response_model=Item)
def get_items(id: int, db: Session = Depends(get_db)):
    pass

@router.delete("/{id}")
def delete_items(id: int, db: Session = Depends(get_db)):
    pass


@router.patch("/{id}", response_model=ItemUpdate)
def patch_items(id: int, db: Session = Depends(get_db)):
    pass


@router.post("/", response_model=Item)
def post_items(item: ItemCreate, db: Session = Depends(get_db)):
    pass

