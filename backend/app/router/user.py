from typing import Annotated
from fastapi import APIRouter, Depends

from .. import schemas, auth
from ..exceptions import not_found, already_exists
from ..dependencies import GetDBs


router = APIRouter()



@router.get("/all", response_model=list[schemas.UserResponse])
def get_user(user: auth.CurrentUser, dbs: GetDBs):
    """Return all users in the same workspace"""
    workspace = dbs.workspace.get(user.workspaces[0].id)
    if not workspace:
        raise not_found("Workspace")

    return dbs.user.get_all_from_workspace(workspace.id)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: str, user: auth.CurrentUser, dbs: GetDBs):
    """Return user data"""
    user = dbs.user.get_if_from_workspace(user_id, user.workspaces[0].id)
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