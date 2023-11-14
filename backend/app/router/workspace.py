from fastapi import APIRouter, Depends, HTTPException, status
from ..auth import get_current_active_user
from .. import crud, schemas, auth


router = APIRouter()


@router.post('')
def create_workspace():
    return