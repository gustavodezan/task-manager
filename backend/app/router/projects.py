from fastapi import APIRouter, Depends, HTTPException, status
from ..auth import get_current_active_user
from .. import crud, schemas, auth
from ..dependencies import GetDBs, TaskDB


router = APIRouter()


# @router.get("/id/{id}", response_model=Project)
# def get_all_teams(id: str, user: Project = Depends(get_current_active_user)):
#     """Return all teams the user's in"""
#     project = crud.Project.get(id)
#     if project.team not in user.teams:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
#     return project

# @router.get("/tasks/{project_id}")
# def get_project_tasks(project_id: str, user: Project = Depends(get_current_active_user)):
#     """Return all tasks under project"""
#     project = crud.Project.get(project_id)
#     project = Project(**project)
#     if project.team not in user.teams:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
#     tasks = []
#     for task in project.tasks:
#         tasks.append(crud.Task.get(task))
#     return tasks

@router.get('', response_model=list[schemas.Project])
def get_all_tasks(dbs: GetDBs):
    return dbs.project.get_all()


@router.post('', response_model=schemas.Project)
def create_new_team(project: schemas.ProjectCreate, dbs: GetDBs):
    """Create a new team"""
    return dbs.project.create(project)
    

    return project
# @router.put("update", response_model=Project)
# def create_new_team(project: Project, user: User = Depends(get_current_active_user)):
#     """Update team info"""
#     if project.team not in user.teams:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
#     return crud.Project.update(project)