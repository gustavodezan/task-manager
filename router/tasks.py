from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_active_user
from app import crud
from app.schemas import Task, Project, Team, User

router = APIRouter()

@router.get("/id/{id}", response_model=Task)
def get_all_teams(id: str, user: User = Depends(get_current_active_user)):
    """Return all teams the user's in"""
    task = crud.Task.get(id)
    if task.team not in user.teams:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    return task

@router.post("/create", response_model=Task)
def create_new_team(task: Task, user: User = Depends):
    """Create a new team"""
    if task.team not in user.teams:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    return crud.Task.create(task.dict())

@router.put("update", response_model=Task)
def create_new_team(task: Task, user: User = Depends):
    """Update team info"""
    if task.team not in user.teams:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    return crud.Task.update(task)