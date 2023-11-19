from typing import Annotated
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
import abc
from . import schemas
from .database import GetDB
from .exceptions import not_found, already_exists, invalid_format
import uuid

class Crud:
    def __init__(self, db: GetDB):
        self.db = db

class User(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.db = db.user
        # self.db.drop()

    def get(self, user_id: str) -> schemas.UserInDB:
        user = self.db.find_one({"_id":user_id})
        if user:
            return schemas.User(**user)
    
    def get_by_email(self, email: str) -> schemas.UserInDB:
        user = self.db.find_one({"email":email})
        if user:
            # print("user _id:",user["_id"])
            return schemas.User(**user)
    
    def get_all(self) -> list[schemas.UserInDB]:
        return [schemas.UserInDB(**user) for user in self.db.find()]

    def create(self, user: schemas.UserInDB):
        if self.get_by_email(user.email):
            raise already_exists("User")
        user = jsonable_encoder(user)
        new_user = self.db.insert_one(user)
        return self.get(new_user.inserted_id)
    
    def delete(self, user_id: str):
        if not self.get(user_id):
            raise not_found("User")
        self.db.delete_one({"_id":user_id})
        return True

class Workspace(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.db = db.team

    def get(self, workspace_id: int):
        workspace = self.db.find_one({"_id": workspace_id})
        if workspace:
            print("workspace _id:",workspace["_id"])
            return schemas.WordspaceInDB(**workspace)

class Team(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.db = db.team

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


