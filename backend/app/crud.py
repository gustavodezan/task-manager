import abc
import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import schemas, models
from .database import GetDB
from .exceptions import already_exists, invalid_format, not_found


class Crud:
    def __init__(self, db: GetDB):
        self.db: Session = db
        self.model = schemas.BaseModel
        self.create_schemas = schemas.BaseModel
        self.update_schemas = schemas.BaseModel

    def get(self, obj_id: int):
        obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        return obj

    def get_all(self) -> list:
        query = self.db.query(self.model)
        return query.all()

    def create(self, new_obj):
        """It's needed to specialize this method in order to apply db insertion validators"""
        if not isinstance(new_obj, self.create_schemas):
            raise invalid_format()

        to_add = {}
        for key in new_obj.__dict__.keys():
            if isinstance(getattr(new_obj,key), list):
                to_add[key] = getattr(new_obj,key).copy()
                getattr(new_obj,key).clear()
        
        new_value = self.model(**new_obj.model_dump())

        for key, value in to_add.items():
            for item in value:
                getattr(new_value, key).append(item)

        self.db.add(new_value)
        self.db.commit()
        self.db.refresh(new_value)
        return new_value

    def update(self, new_obj):
        """Default update method for any CRUD Class. For more complex updates it should be specialized"""
        # if not isinstance(new_obj, self.update_schemas):
        #     raise invalid_format()
        if not self.get(new_obj.id):
            raise not_found(self.__class__.__name__)
        new_value: dict = new_obj.model_dump(exclude_unset=True)
        
        list_updates = []
        for key in new_value.keys:
            if type(new_value[key]) == list:
                list_updates.append((key, new_value[key]))
        
        query = self.db.query(self.model).filter(self.model.id == new_obj.id)
        old_value = query.first()

        if not old_value:
            raise not_found(self.__class__.__name__)
        
        query.filter(self.model.id == new_obj.id).update(new_value, synchronize_session=False)
        self.db.commit()
        self.db.refresh(old_value)
        return old_value
    
    def delete(self, obj_id: int) -> bool:
        """In cases it's needed to manully change/delete values after the delete operation, it should come after the return of that method"""
        query = self.db.query(self.model).filter(self.model.id == obj_id)
        value = query.first()

        if not value:
            raise not_found(self.__class__.__name__)
        
        query.delete(synchronize_session="evaluate")
        self.db.commit()
        return True

class User(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.model: models.User = models.User
        self.create_schemas: schemas.UserSubmit = schemas.UserSubmit
        self.update_schemas: schemas.UserUpdate = schemas.UserUpdate

    def get(self, user_id: int) -> schemas.UserInDB:
        return super().get(user_id)

    def get_by_email(self, email: str, validate: bool = False) -> schemas.UserInDB:
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if user:
            # print("user _id:",user["_id"])
            if validate:
                return schemas.UserInDB(**user.__dict__)
            return user

    def get_all(self) -> list[schemas.UserInDB]:
        return super().get_all()
    
    def get_all_from_workspace(self, workspace_id) -> list[schemas.UserInDB]:
        users = self.db.query(self.model).join(self.model.workspaces).filter(models.Workspace.id == workspace_id).all()
        return users
    
    def get_if_from_workspace(self, user_id, workspace_id) -> list[schemas.UserInDB]:
        user = self.db.query(self.model).join(self.model.workspaces).filter(
            self.model.id == user_id,
            models.Workspace.id == workspace_id).first()
        return user

    def get_for_auth(self, email: str) -> schemas.UserWPass:
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if user:
            return schemas.UserWPass(**user.__dict__)

    def create(self, user: schemas.UserSubmit) -> schemas.UserInDB:
        if self.get_by_email(user.email):
            raise already_exists("User")
        return super().create(user)
    
    def update(self, user: schemas.UserSubmit) -> schemas.UserInDB:
        return super().update(user)

class Workspace(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.model: models.Workspace = models.Workspace
        self.create_schemas: schemas.Workspace = schemas.Workspace
        self.update_schemas: schemas.WorkspaceUpdate = schemas.WorkspaceUpdate

    def get(self, workspace_id: int) -> schemas.WorkspaceInDB:
        return super().get(workspace_id)

    def get_if_member_in(self, workspace_id: int, user_id: int) -> schemas.WorkspaceInDB:
        workspaces = self.db.query(models.Workspace).filter(self.model.id == workspace_id).join(models.Workspace.members).filter(models.User.id == user_id)
        return workspaces.first()

    def get_member_workspaces(self, user_id: int) -> schemas.WorkspaceInDB:
        workspaces = self.db.query(models.Workspace).join(models.Workspace.members).filter(models.User.id == user_id)
        return workspaces.all()

    def get_all(self) -> list[schemas.WorkspaceInDB]:
        return super().get_all()

    def create(self, workspace: schemas.Workspace) -> schemas.WorkspaceInDB:
        return super().create(workspace)
    
    def update(self, workspace: schemas.WorkspaceUpdate):
        return super().update(workspace)

class Team(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.model: models.Team = models.Team
        self.create_schemas: schemas.TeamCreate = schemas.TeamCreate
        self.update_schemas: schemas.TeamUpdate = schemas.TeamUpdate

    def get(self, team_id: int) -> schemas.TeamInDB:
        return super().get(team_id)

    def get_by_slug(self, slug: str, validate: bool = False):
        team = self.db.query(models.Team).filter(models.Team.slug == slug).first()
        if team:
            if validate:
                return schemas.TeamInDB(**team.__dict__)
            return team
    
    def get_member_teams(self, user_id: str):
        teams = self.db.query(models.Team).join(models.Team.members).filter(models.User.id == user_id)
        return teams.all()
    
    def get_all(self):
        return super().get_all()

    def add_members(self, team_id:int, members: list[int]) -> schemas.TeamInDB:
        team = self.get(team_id, validate=False)
        for member in members:
            if type(member) != int:
                continue
            _user = User(self.db).get(member, validate=False)
            if _user:
                team.members.append(_user)
        self.db.commit()
        return self.get(team_id)
                

    def create(self, team: schemas.TeamCreate) -> schemas.TeamInDB:
        if self.get_by_slug(team.slug):
            raise already_exists("Team with that name")
        return super().create(team)

    def update(self, team: schemas.TeamUpdate) -> schemas.TeamInDB:
        return super().update(team)

class Project(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.model: models.Project = models.Project
        self.create_schemas: schemas.ProjectCreate = schemas.ProjectCreate
        self.update_schemas: schemas.ProjectUpdate = schemas.ProjectUpdate

    def get(self, project_id: int) -> schemas.Project:
        return super().get(project_id)
    
    def get_member_projects(self, user_id: int) -> list[schemas.Project]:
        projects = self.db.query(self.model).join(self.model.members).filter(models.User.id == user_id)
        return projects.all()
    
    def create(self, project: schemas.ProjectCreate) -> schemas.Project:
        return super().create(project)

    def update(self, project: schemas.ProjectUpdate) -> schemas.Project:
        return super().update(project)
    
    def delete(self, project_id: int):
        return super().delete(project_id)

class Task(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.model: models.Task = models.Task
        self.create_schemas: schemas.TaskCreate = schemas.TaskCreate
        self.update_schemas: schemas.TaskUpdate = schemas.TaskUpdate

    def get(self, task_id: int) -> schemas.Task:
        return super().get(task_id)
    
    def get_member_tasks(self, user_id: int) -> list[schemas.Task]:
        tasks = self.db.query(self.model).join(self.model.members).filter(models.User.id == user_id)
        return tasks.all()
    
    def create(self, task: schemas.TaskCreate) -> schemas.Task:
        return super().create(task)

    def update(self, task: schemas.TaskUpdate) -> schemas.Task:
        return super().update(task)
    
    def delete(self, task_id: int):
        return super().delete(task_id)
