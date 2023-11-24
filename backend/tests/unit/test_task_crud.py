# # from fastapi.testclient import TestClient
# from fastapi import HTTPException
# import sqlalchemy.exc
# import pytest

# from app import schemas, models
# from tests.unit.default_db import dbs


# # GET
# def test_get_all():
#     tasks = dbs.task.get_all()
#     assert isinstance(tasks, list)
#     for task in tasks:
#         assert isinstance(task, models.Task)

# def test_get():
#     tasks = dbs.task.get_all()
#     if len(tasks) > 0:
#         task = dbs.task.get(tasks[0].id)
#         assert isinstance(task, models.Task)
#     else:
#         assert tasks == []

# def test_get_inexistent():
#     not_task = dbs.task.get(-1)
#     assert not_task == None

# # def test_get_wrong_type():
# #     with pytest.raises(sqlalchemy.exc.DataError) as excinfo:
# #         not_task = dbs.task.get('oi')
# #         # assert not_task == None
# #     assert excinfo.errisinstance(sqlalchemy.exc.DataError)

# def test_get_member_tasks():
#     test_user_id = 2
#     tasks = dbs.task.get_member_tasks(test_user_id)
#     assert isinstance(tasks, list)
#     for task in tasks:
#         assert isinstance(task, models.Task)
#         assert test_user_id in [m.id for m in task.members]

# def test_get_member_tasks_member_invalid_user():
#     test_user_id = -1
#     tasks = dbs.task.get_member_tasks(test_user_id)
#     assert tasks == []

# # POST
# global_id = ''

# def test_delete_test_task():
#     task = dbs.task.get_by_slug("test-crud-task")
#     if task:
#         status = dbs.task.delete(task.id)
#         assert status == True
#     else:
#         assert task == None

# def test_create():
#     global global_id

#     data = schemas.TaskCreate(name="test_crud_task", workspace_id=1)
#     task = dbs.task.create(data)
#     assert isinstance(task, models.Task)
#     assert task.name == data.name
#     global_id = task.id

# # def test_create_wo_name():
# #     with pytest.raises(HTTPException) as excinfo:
# #         task = dbs.task.create(schemas.TaskCreate(name="", workspace_id=1))
# #     assert excinfo.errisinstance(HTTPException)
    
# #     with pytest.raises(HTTPException) as excinfo:
# #         task = schemas.Task(name="name")
# #         task = dbs.task.create(task)
# #     assert excinfo.errisinstance(HTTPException)
    
    
    
# # PUT
# # @pytest.mark.skip()
# def test_update():
#     global global_id

#     data = schemas.TaskUpdate(id=global_id, name="new name old-slug")
#     task = dbs.task.update(data)
#     assert task.name == data.name

# def test_not_update():
#     global global_id

#     _task = dbs.task.get(global_id)
#     data = schemas.TaskUpdate(id=global_id)
#     task = dbs.task.update(data)

#     assert task.name == _task.name


# # DELETE
# def test_delete():
#     global global_id
#     assert dbs.task.delete(global_id)

# def test_delete_inexistent():
#     global global_id
#     with pytest.raises(HTTPException) as excinfo:
#         dbs.task.delete(global_id)
#     assert excinfo.errisinstance(HTTPException)

# # def test_close_db():
# #     close_db()