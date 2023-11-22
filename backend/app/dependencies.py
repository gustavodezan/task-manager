from typing import Annotated
from fastapi import Depends
from . import crud
from .database import GetDB

UserDB = Annotated[crud.User, Depends(crud.User)]
TeamDB = Annotated[crud.Team, Depends(crud.Team)]
WorkspaceDB = Annotated[crud.Workspace, Depends(crud.Workspace)]

class DBs:
    def __init__(self, db: GetDB):
        self.db: db = db
        self.user: crud.User = crud.User(db)
        self.team: crud.Team = crud.Team(db)
        # self.workspace: crud.Workspace = crud.Workspace(db)

GetDBs = Annotated[DBs, Depends(DBs)]