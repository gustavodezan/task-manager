# from fastapi import APIRouter, Depends, HTTPException, status
# from app.auth import get_current_active_user
# from app import crud
# from app.schemas import Tag, Project, Team, User

# router = APIRouter()

# @router.get("/id/{id}", response_model=Tag)
# def get_all_teams(id: str, user: User = Depends(get_current_active_user)):
#     """Return all teams the user's in"""
#     tag = crud.Tag.get(id)
#     return tag

# @router.post("/create", response_model=Tag)
# def create_new_team(tag: Tag):
#     """Create a new team"""
#     return crud.Tag.create(tag.dict())

# @router.put("update", response_model=Tag)
# def create_new_team(tag: Tag):
#     """Update team info"""
#     return crud.Tag.update(tag)