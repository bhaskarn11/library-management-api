from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from app import models
from ..schemas import ItemCreate, ItemUpdate, Item, BorrowCreate, Borrow
from app.crud import get_item_by_id, create_item, remove_item, update_item, create_borrow
from app.authentication import get_current_active_user

router = APIRouter(
    prefix="/items",
    dependencies=[Depends(get_current_active_user)]
)

@router.get("/{id}", response_model=Item, tags=["Items"])
def get_items(id: int, db: Session = Depends(get_db)):
    try:
        item = get_item_by_id(id, db)
        if item is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item bot found with this id")
        return item
    except:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{id}", tags=["Items"])
def delete_items(id: int, db: Session = Depends(get_db)):
    try:
        return remove_item(id, db)
    except:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/{id}", response_model=Item, tags=["Items"])
def patch_items(id: int,item: ItemUpdate, db: Session = Depends(get_db)):
    try:
        return update_item(item, id, db)
    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while processing")


@router.post("/", response_model=Item, tags=["Items"])
def post_items(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        # print(item)
        return create_item(item, db)
    except Exception as e:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Couldn't create item")


@router.post("/borrow", response_model=Borrow, tags=["Borrower Issue Endpoint"])
def create_borrow_order(borrow: BorrowCreate, db: Session = Depends(get_db)):
    item_ids = [item.item_id for item in borrow.items]  # only five items are allowd
    items = db.query(models.Item).filter(models.Item.id.in_(item_ids), models.Item.available == True).limit(5).all()
    if not items:
        return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Items not found")
    try:
        db_b = create_borrow(borrow, items, db)
        return db_b
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Problem creating borrow request")


@router.post("/search", tags=["Items search endpoint"])
def search_items(f: str, query: str):
    # f = filters.split(",")
    # print(f)
    return {"filter": f, "query": query}
