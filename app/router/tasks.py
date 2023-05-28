# from fastapi import APIRouter, Depends, HTTPException, status
# from app.auth import get_current_active_user
# from app import crud
# from app.schemas import Task, Project, Team, User

# router = APIRouter()

# @router.get("/id/{id}", response_model=Task)
# def get_all_teams(id: str, user: User = Depends(get_current_active_user)):
#     """Return a task by its id"""
#     task = crud.Task.get(id)
#     if task.team not in user.teams:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
#     return task

# @router.post("/create", response_model=Task)
# def create_new_team(task: Task, user: User = Depends(get_current_active_user)):
#     """Create a new task"""
#     if task.team not in user.teams:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    
#     new_task = crud.Task.create(task.dict())
    
#     _project = crud.Project.get(new_task["parent"])
#     _project["tasks"].append(new_task["key"])
#     crud.Project.update(_project)
#     return new_task

# @router.put("update", response_model=Task)
# def create_new_team(task: Task, user: User = Depends(get_current_active_user)):
#     """Update task info"""
#     if task.team not in user.teams:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
#     return crud.Task.update(task)