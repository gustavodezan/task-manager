from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Tokens
class Token(BaseModel):
    access_token: str
    token_type: str
    expire: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []

class User(BaseModel):
    key: str
    name: str
    email: str
    active: Optional[bool] = True
    profile_pic: Optional[bytes] = None
    register_date: Optional[str] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class UserInDB(User):
    password: str
    scopes: Optional[list[str]] = ["me:read", "me:write"]
    access_level: Optional[int] = 0

class Tags(BaseModel):
    key: str
    name: str
    color: str

class Tasks(BaseModel):
    key: str
    name: str
    due_on: str
    create_at: str
    color: str
    responsibles: list[User.key]
    tags: list[Tags.key]

class Projects(BaseModel):
    key: str
    name: str
    access_level: int
    color: str
    status: str
    tasks: list[Tasks.key]

class Team(BaseModel):
    key: str
    name: str
    access_level: str
    projects: list[Projects.key]