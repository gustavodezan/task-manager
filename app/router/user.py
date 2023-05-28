from typing import Annotated
from fastapi import APIRouter, Depends
# from app.auth import get_current_active_user
from .. import crud, schemas


router = APIRouter()


@router.get("/", response_model=list[schemas.User])
def get_user(user_db: crud.UserDB):
    """Return user data"""
    return user_db.get_all()

@router.get("/all", response_model=list[schemas.User])
def get_user(user_db: crud.UserDB):
    """Return user data"""
    return user_db.get_all()

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: str, user_db: crud.UserDB):
    """Return user data"""
    return user_db.get(user_id)

@router.post("/new", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, user_db: crud.UserDB):
    user = schemas.User(**user.dict())
    user = user_db.create(user)
    print(user)
    return user