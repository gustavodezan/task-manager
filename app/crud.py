from typing import Annotated
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from . import schemas
from .database import GetDB
from .exceptions import not_found, already_exists

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
            return schemas.UserInDB(**user)
    
    def get_by_email(self, email: str) -> schemas.UserInDB:
        user = self.db.find_one({"email":email})
        if user:
            print("user _id:",user["_id"])
            return schemas.UserInDB(**user)
    
    def get_all(self) -> list[schemas.UserInDB]:
        return [schemas.UserInDB(**user) for user in self.db.find()]

    def create(self, user: schemas.User):
        if self.get_by_email(user.email):
            raise already_exists("User")
        user = jsonable_encoder(user)
        new_user = self.db.insert_one(user)
        return self.get(new_user.inserted_id)

class Team(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.db = db.team
        # self.db.drop()
    
    def get(self, team_id: int):
        team = self.db.find_one({"_id": team_id})
        if team:
            print("team _id:",team["_id"])
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

    def create(self, team: schemas.Team):
        if self.get_by_slug(team.slug):
            raise already_exists("Team with that name")
        team = jsonable_encoder(team)
        new_team = self.db.insert_one(team)
        return self.get(new_team.inserted_id)





