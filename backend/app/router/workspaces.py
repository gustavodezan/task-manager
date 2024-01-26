from fastapi import APIRouter, Depends, HTTPException, status
from ..auth import CurrentUser
from .. import crud, schemas, auth, exceptions, service
from ..dependencies import GetDBs


router = APIRouter()


@router.get('', response_model=list[schemas.WorkspaceShort])
def get_all(dbs: GetDBs, user: CurrentUser):
    workspaces = dbs.workspace.get_member_workspaces(user.id)
    return workspaces

@router.get('/{workspace_id}', response_model=schemas.WorkspaceShort)
def get_all(workspace_id: int, user: CurrentUser, dbs: GetDBs):
    return dbs.workspace.get_if_member_in(workspace_id, user.id)

@router.post('', response_model=schemas.WorkspaceInDB)
def create_workspace(workspace: schemas.Workspace, user: CurrentUser, dbs: GetDBs):
    if user.id not in workspace.members:
        workspace.members.append(user.id)
    members = []
    for member_id in workspace.members:
        member = dbs.user.get(member_id)
        if member:
            members.append(member)
    workspace.members = members
    return dbs.workspace.create(workspace)

@router.put('', response_model=schemas.WorkspaceInDB)
def update_workspace(workspace: schemas.WorkspaceUpdate, user: CurrentUser, dbs: GetDBs):
    _workspace = dbs.workspace.get(workspace.id)
    if not _workspace or not service.check_if_user_can_change_workspace(user, _workspace):
        raise exceptions.not_found('Workspace')

    return dbs.workspace.update(workspace)

@router.delete('/{workspace_id}')
def delete_workspace(workspace_id: int, user: CurrentUser, dbs: GetDBs):
    workspace = dbs.workspace.get(workspace_id)
    if not workspace or not service.check_if_user_can_change_workspace(user, workspace):
        raise exceptions.not_found('Workspace')
    
    return dbs.workspace.delete(workspace_id)
