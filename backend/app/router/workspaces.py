from fastapi import APIRouter, Depends, HTTPException, status
from ..auth import get_current_active_user
from .. import crud, schemas, auth
from ..dependencies import GetDBs


router = APIRouter()


@router.get('')
def get_all(dbs: GetDBs):
    return dbs.workspace.get_all()
    return dbs.workspace.get_members_workspaces()

@router.get('/{workspace_id}')
def get_all(workspace_id: int, dbs: GetDBs):
    return dbs.workspace.get(workspace_id)
    return dbs.workspace.get_members_workspaces()

@router.post('', response_model=schemas.WorkspaceInDB)
def create_workspace(workspace: schemas.Workspace, dbs: GetDBs):
    print(workspace)
    return dbs.workspace.create(workspace)

