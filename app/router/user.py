from typing import Annotated
from fastapi import APIRouter, Depends

from .. import crud, schemas, auth


router = APIRouter()


@router.get("/", response_model=schemas.User)
def get_user(user: auth.CurrentUser):
    """Return user data"""
    return user

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
    user = schemas.UserInDB(**user.dict())
    user.password = auth.get_password_hash(user.password)
    user = user_db.create(user)
    return user