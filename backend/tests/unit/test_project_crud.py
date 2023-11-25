# from fastapi.testclient import TestClient
from fastapi import HTTPException
import sqlalchemy.exc
import pytest

from app import schemas, models
from tests.unit.default_db import dbs


# GET
def test_get_all():
    projects = dbs.project.get_all()
    assert isinstance(projects, list)
    for project in projects:
        assert isinstance(project, models.Project)

def test_get():
    projects = dbs.project.get_all()
    if len(projects) > 0:
        project = dbs.project.get(projects[0].id)
        assert isinstance(project, models.Project)
    else:
        assert projects == []

def test_get_inexistent():
    not_project = dbs.project.get(-1)
    assert not_project == None

def test_get_member_projects():
    test_user_id = 2
    projects = dbs.project.get_member_projects(test_user_id)
    assert isinstance(projects, list)
    for project in projects:
        assert isinstance(project, models.Project)
        assert test_user_id in [m.id for m in project.members]

def test_get_member_projects_member_invalid_user():
    test_user_id = -1
    projects = dbs.project.get_member_projects(test_user_id)
    assert projects == []

# POST
global_id = ''

def test_create():
    global global_id

    data = schemas.ProjectCreate(name="test_crud_project", team_id=73)
    project = dbs.project.create(data)
    assert isinstance(project, models.Project)
    assert project.name == data.name
    global_id = project.id
    
# PUT
# @pytest.mark.skip()
def test_update():
    global global_id

    data = schemas.ProjectUpdate(id=global_id, name="new name")
    project = dbs.project.update(data)
    assert project.name == data.name

def test_not_update():
    global global_id

    _project = dbs.project.get(global_id)
    data = schemas.ProjectUpdate(id=global_id)
    project = dbs.project.update(data)

    assert project.name == _project.name


# DELETE
def test_delete():
    global global_id
    assert dbs.project.delete(global_id)

def test_delete_inexistent():
    global global_id
    with pytest.raises(HTTPException) as excinfo:
        dbs.project.delete(global_id)
    assert excinfo.errisinstance(HTTPException)

