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
    teams: list[str]

class UserInDB(User):
    password: str
    scopes: list[str] = ["me:read", "me:write"]
    access_level: int = 0

class Tag(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    color: str = "#000000"

class Task(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    parent: str # project if root
    create_at: datetime = datetime.now()
    due_on: datetime|None = None
    completed_at: datetime|None = None
    color: str = "#000000"
    responsibles: list[str]
    tags: list[str]

class Project(BaseModel):
    key: Optional[str] = None
    name: str
    team: str
    access_level: Optional[int] = 0
    color: Optional[str] = "#000000"
    status: Optional[str] = None
    tasks: Optional[list[str]] = []

class Team(BaseModel):
    key: Optional[str]
    name: str
    members: Optional[list[str]] = []
    access_level: Optional[int] = 0
    projects: Optional[list[str]] = []