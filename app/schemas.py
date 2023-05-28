from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

# Tokens
class Token(BaseModel):
    access_token: str
    token_type: str
    expire: str

class TokenData(BaseModel):
    username: str|None = None
    scopes: list[str]


class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    active: bool = True
    profile_pic: str|None = None
    register_date: datetime = datetime.now()
    # teams: list["Team"] = []
    scopes: list[str] = ["me:read", "me:write"]
    access_level: int = 0
    active: bool = True

    # class Config:
    #     orm_mode = True

class UserInDB(User,UserCreate):
    pass


class Tag(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    color: str = "#000000"


class Task(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    parent: str # project if root
    created_at: datetime = datetime.now()
    due_on: datetime|None = None
    completed_at: datetime|None = None
    color: str = "#000000"
    responsibles: list[User]
    tags: list[Tag]

class Project(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    access_level: int = 0
    color: str = "#000000"
    status: str|None = None
    tasks: list[Task]
    admins: list[User]


class TeamCreate(BaseModel):
    name: str
    access_level: int = 0
    members: list[User] = []
    projects: list[Project] = []
    slug: str|None = None

class Team(TeamCreate):
    admins: list[User]

class TeamInDB(Team):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
