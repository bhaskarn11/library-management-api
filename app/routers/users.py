from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union
from fastapi.security import OAuth2PasswordRequestForm


from ..database import get_db
from app import schemas
from app.authentication import Token, get_current_active_user, authenticate_user
from app.crud import create_user, get_user_by_id, update_user

router = APIRouter(
    prefix="/users",
)


@router.get("/{id}", response_model=schemas.User, tags=["Users"])
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = get_user_by_id(db, id)
        if user:
            return user
        return HTTPException(status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # print(e.with_traceback())
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/", tags=["Users"])
def post_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.patch("/{id}", tags=["Users"])
def patch_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user, id)


@router.delete("/{id}", tags=["Users"])
def delete_user():
    pass


@router.post("/auth", response_model=Token, tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_user(db, form_data.username, form_data.password)


# @router.get("/me", response_model=schemas.User, tags=["Authentication"])
# def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
#     return current_user

