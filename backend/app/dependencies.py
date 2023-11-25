from typing import Annotated
from fastapi import Depends
from . import crud
from .database import GetDB

UserDB = Annotated[crud.User, Depends(crud.User)]
WorkspaceDB = Annotated[crud.Workspace, Depends(crud.Workspace)]
TeamDB = Annotated[crud.Team, Depends(crud.Team)]
ProjectDB = Annotated[crud.Project, Depends(crud.Project)]
TaskDB = Annotated[crud.Task, Depends(crud.Task)]

class DBs:
    def __init__(self, db: GetDB):
        self.db: db = db
        self.user: crud.User = crud.User(db)
        self.workspace: crud.Workspace = crud.Workspace(db)
        self.team: crud.Team = crud.Team(db)
        self.project: crud.Project = crud.Project(db)
        self.task: crud.Task = crud.Task(db)

GetDBs = Annotated[DBs, Depends(DBs)]