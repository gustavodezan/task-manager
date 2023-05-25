from fastapi import APIRouter, Depends
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/me")
def get_user(user: str = Depends(get_current_active_user)):
    """Return user data"""
    return user