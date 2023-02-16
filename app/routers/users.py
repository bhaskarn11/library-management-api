from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union
from fastapi.security import OAuth2PasswordRequestForm


from ..database import get_db
from app import schemas
from app.authentication import Token, authenticate_user, create_access_token, get_current_active_user
from app.crud import create_user, get_user_by_id, update_user

router = APIRouter(
    prefix="/users"
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
def post_user(user: schemas.UserCreate, db: Session = Depends(get_db), auth=Depends(get_current_active_user)):
    return create_user(db, user)


@router.patch("/{id}", tags=["Users"])
def patch_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user, id)


@router.delete("/{id}", tags=["Users"])
def delete_user():
    pass


@router.post("/auth", response_model=Token, tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user:
        token = create_access_token({"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    return HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access or User not found")


@router.get("/me", response_model=schemas.User,tags=["Authentication"])
def read_users_me(current_user: schemas.User  = Depends(get_current_active_user)):
    return current_user

