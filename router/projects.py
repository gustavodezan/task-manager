from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_active_user
from app import crud
from app.schemas import Project, Team, User

router = APIRouter()

@router.get("/id/{id}", response_model=list[Project])
def get_all_teams(id: str, user: Project = Depends(get_current_active_user)):
    """Return all teams the user's in"""
    project = crud.Project.get(id)
    team = crud.Team.get(project.team)
    if user.key not in team.members:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    return project

@router.post("/create", response_model=Project)
def create_new_team(project: Project):
    """Create a new team"""
    return crud.Project.create(project.dict())

@router.put("update", response_model=Project)
def create_new_team(project: Project):
    """Update team info"""
    return crud.Project.update(project)