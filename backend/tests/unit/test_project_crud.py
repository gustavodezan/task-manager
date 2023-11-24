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

# def test_get_wrong_type():
#     with pytest.raises(sqlalchemy.exc.DataError) as excinfo:
#         not_project = dbs.project.get('oi')
#         # assert not_project == None
#     assert excinfo.errisinstance(sqlalchemy.exc.DataError)

def test_get_by_slug():
    projects = dbs.project.get_all()
    if len(projects) > 0:
        project = dbs.project.get_by_slug(projects[0].slug)
        assert isinstance(project, models.Project)
    else:
        assert projects == []

def test_get_by_slug_inexistent():
    project = dbs.project.get_by_slug("")
    assert project == None

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

def test_delete_test_project():
    project = dbs.project.get_by_slug("test-crud-project")
    if project:
        status = dbs.project.delete(project.id)
        assert status == True
    else:
        assert project == None

def test_create():
    global global_id

    data = schemas.ProjectCreate(name="test_crud_project", workspace_id=1)
    project = dbs.project.create(data)
    assert isinstance(project, models.Project)
    assert project.name == data.name
    assert project.slug == data.slug
    global_id = project.id

# def test_create_wo_name():
#     with pytest.raises(HTTPException) as excinfo:
#         project = dbs.project.create(schemas.ProjectCreate(name="", workspace_id=1))
#     assert excinfo.errisinstance(HTTPException)
    
#     with pytest.raises(HTTPException) as excinfo:
#         project = schemas.Project(name="name")
#         project = dbs.project.create(project)
#     assert excinfo.errisinstance(HTTPException)
    
    
    
# PUT
# @pytest.mark.skip()
def test_update():
    global global_id

    data = schemas.ProjectUpdate(id=global_id, name="new name old-slug")
    project = dbs.project.update(data)
    assert project.name == data.name
    assert project.slug != None

def test_not_update():
    global global_id

    _project = dbs.project.get(global_id)
    data = schemas.ProjectUpdate(id=global_id)
    project = dbs.project.update(data)

    assert project.name == _project.name
    assert project.slug == _project.slug


# DELETE
def test_delete():
    global global_id
    assert dbs.project.delete(global_id)

def test_delete_inexistent():
    global global_id
    with pytest.raises(HTTPException) as excinfo:
        dbs.project.delete(global_id)
    assert excinfo.errisinstance(HTTPException)

# def test_close_db():
#     close_db()