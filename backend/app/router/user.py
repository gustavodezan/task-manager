from typing import Annotated
from fastapi import APIRouter, Depends

from .. import schemas, auth
from ..exceptions import not_found, already_exists
from ..dependencies import GetDBs


router = APIRouter()



@router.get("/all", response_model=list[schemas.UserResponse])
def get_user(dbs: GetDBs):
    """Return user data"""
    print(dbs.user.get_all())
    return dbs.user.get_all()

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: str, dbs: GetDBs):
    """Return user data"""
    user = dbs.user.get(user_id)
    if not user:
        raise not_found("User")
    return user

@router.get("/", response_model=schemas.UserResponse)
def get_user(user: auth.CurrentUser):
    """Return user data"""
    return user

@router.post("/", response_model=schemas.UserResponse)
def create_new_user(user: schemas.UserSubmit, dbs: GetDBs):
    user.password = auth.get_password_hash(user.password)
    user = dbs.user.create(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: str, dbs: GetDBs):
    """Delete specified team"""
    # if user.access_level < x
    return dbs.user.delete(user_id)