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

class User(Crud):
    def get(self, user_id: str) -> schemas.UserInDB:
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            return schemas.UserInDB(**user.__dict__)
    
    def get_by_email(self, email: str) -> schemas.UserInDB:
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if user:
            # print("user _id:",user["_id"])
            return schemas.UserInDB(**user.__dict__)
    
    def get_all(self) -> list[schemas.UserInDB]:
        query = self.db.query(models.User)
        return [schemas.UserInDB(**user.__dict__) for user in query.all()]

    def get_for_auth(self, email: str) -> schemas.UserWPass:
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if user:
            return schemas.UserWPass(**user.__dict__)

    def create(self, user: schemas.UserSubmit):
        if not isinstance(user, schemas.UserSubmit):
            raise invalid_format()
        if self.get_by_email(user.email):
            raise already_exists("User")
        # user = jsonable_encoder(user)
        new_value = models.User(**user.model_dump())
        self.db.add(new_value)
        self.db.commit()
        self.db.refresh(new_value)
        return schemas.UserInDB(**new_value.__dict__)
    
    def update(self, user: schemas.UserUpdate):
        if not isinstance(user, schemas.UserUpdate):
            raise invalid_format()
        new_value = user.model_dump(exclude_unset=True)
        query = self.db.query(models.User).filter(models.User.id == user.id)
        old_value = query.first()

        if not old_value:
            raise not_found("User")
        
        query.filter(models.User.id == user.id).update(new_value, synchronize_session=False)
        self.db.commit()
        self.db.refresh(old_value)
        return schemas.UserInDB(**old_value.__dict__)

    def delete(self, user_id: str):
        query = self.db.query(models.User).filter(models.User.id == user_id)
        value = query.first()

        if not value:
            raise not_found("User")
        
        query.delete(synchronize_session="evaluate")
        self.db.commit()
        return True

class Workspace(Crud):
    pass
    # def get(self, workspace_id: int):
    #     workspace = self.db.find_one({"_id": workspace_id})
    #     if workspace:
    #         print("workspace _id:",workspace["_id"])
    #         return schemas.WordspaceInDB(**workspace)

    # def get_all(self):
    #     return [schemas.WorkspaceInDB(**workspace) for workspace in self.db.find()]

class Team(Crud):
    def get(self, team_id: int):
        team = self.db.find_one({"_id": team_id})
        if team:
            # print("team _id:",team["_id"])
            return schemas.TeamInDB(**team)
    
    def get_by_slug(self, slug: str):
        team = self.db.find_one({"slug": slug})
        if team:
            return schemas.TeamInDB(**team)
    
    def get_member_teams(self, user_id: str):
        teams = self.db.find({"members": user_id})
        member_teams = []
        for team in teams:
            if team:
                member_teams.append(schemas.TeamInDB(**team))
        return member_teams
    
    def get_all(self):
        return [schemas.TeamInDB(**team) for team in self.db.find()]

    def create(self, team: schemas.TeamInDB):
        if not isinstance(team, schemas.TeamInDB):
            raise invalid_format()
        if self.get_by_slug(team.slug):
            raise already_exists("Team with that name")
        team = jsonable_encoder(team)
        new_team = self.db.insert_one(team)
        return self.get(new_team.inserted_id)
    
    def update(self, team: schemas.TeamUpdate):
        if not self.get(team.id):
            raise not_found("Team")
        new_team = team.model_dump(exclude_unset=True)
        new_team.pop("id")
        if new_team == {}:
            return False
        updated_team = self.db.update_one({"_id":team.id}, {"$set":new_team})
        if updated_team.raw_result['updatedExisting']:
            return True
        return False

    def delete(self, team_id: str):
        if not self.get(team_id):
            raise not_found("Team")
        self.db.delete_one({"_id":team_id})
        return True


