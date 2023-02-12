from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union

from ..database import get_db
from ..schemas import ItemCreate, ItemUpdate, Item, BorrowCreate
from app.crud import get_item_by_id, create_item, remove_item, update_item, create_borrow

router = APIRouter(
    prefix="/items"
)

@router.get("/{id}", response_model=Item, tags=["Items"])
def get_items(id: int, db: Session = Depends(get_db)):
    try:
        return get_item_by_id(id, db)
    except:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{id}", tags=["Items"])
def delete_items(id: int, db: Session = Depends(get_db)):
    try:
        return remove_item(id, db)
    except:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/{id}", response_model=ItemUpdate, tags=["Items"])
def patch_items(id: int, db: Session = Depends(get_db)):
    try:
        return update_item(id, db)
    except:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/", response_model=Item, tags=["Items"])
def post_items(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        return create_item(item, db)
    except:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/borrow", tags=["Borrower Issue Endpoint"])
def create_borrow_order(borrow: BorrowCreate, db: Session = Depends(get_db)):
    try:
        db_b = create_borrow(borrow, db)
        return db_b
    except:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
