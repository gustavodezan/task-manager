# from fastapi.testclient import TestClient
from fastapi import HTTPException
import sqlalchemy.exc
import pytest

from app import schemas, models
from tests.unit.default_db import dbs


# GET
def test_get_all():
    workspaces = dbs.workspace.get_all()
    assert isinstance(workspaces, list)
    for workspace in workspaces:
        assert isinstance(workspace, models.Workspace)

def test_get():
    workspaces = dbs.workspace.get_all()
    if len(workspaces) > 0:
        workspace = dbs.workspace.get(workspaces[0].id)
        assert isinstance(workspace, models.Workspace)
    else:
        assert workspaces == []

def test_get_inexistent():
    not_team = dbs.workspace.get(-1)
    assert not_team == None

# def test_get_wrong_type():
#     with pytest.raises(sqlalchemy.exc.DataError) as excinfo:
#         not_team = dbs.workspace.get('oi')
#         # assert not_team == None
#     assert excinfo.errisinstance(sqlalchemy.exc.DataError)

def test_get_member_workspaces():
    test_user_id = 2
    workspaces = dbs.workspace.get_member_workspaces(test_user_id)
    assert isinstance(workspaces, list)
    for workspace in workspaces:
        assert isinstance(workspace, models.Workspace)
        assert test_user_id in [m.id for m in workspace.members]

def test_get_member_workspaces_member_invalid_user():
    test_user_id = -1
    workspaces = dbs.workspace.get_member_workspaces(test_user_id)
    assert workspaces == []

# POST
global_id = ''

def test_create():
    global global_id

    data = schemas.Workspace(name="test_crud_workspace")
    workspace = dbs.workspace.create(data)
    assert isinstance(workspace, models.Workspace)
    assert workspace.name == data.name
    global_id = workspace.id
    
# PUT
# @pytest.mark.skip()
def test_update():
    global global_id

    data = schemas.WorkspaceUpdate(id=global_id, name="new name")
    workspace = dbs.workspace.update(data)
    assert workspace.name == data.name

def test_not_update():
    global global_id

    _team = dbs.workspace.get(global_id)
    data = schemas.WorkspaceUpdate(id=global_id)
    workspace = dbs.workspace.update(data)

    assert workspace.name == _team.name

# DELETE
def test_delete():
    global global_id
    assert dbs.workspace.delete(global_id)

def test_delete_inexistent():
    global global_id
    with pytest.raises(HTTPException) as excinfo:
        dbs.workspace.delete(global_id)
    assert excinfo.errisinstance(HTTPException)

# def test_close_db():
#     close_db()