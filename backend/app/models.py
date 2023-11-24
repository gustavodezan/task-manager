from datetime import datetime
from typing import Optional

from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from . import constants
from .constants import DB_ENCRYPTION_KEY
from .database import Base, engine


member_team_association = Table(
    'member_team', Base.metadata,
    Column('member_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id'))
)

member_workspace_association = Table(
    'member_workspace', Base.metadata,
    Column('member_id', Integer, ForeignKey('users.id')),
    Column('workspace_id', Integer, ForeignKey('workspaces.id'))    
)

member_project_association = Table(
    'member_project', Base.metadata,
    Column('member_id', Integer, ForeignKey('users.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))    
)

member_tasks_association = Table(
    'member_task', Base.metadata,
    Column('member_id', Integer, ForeignKey('users.id')),
    Column('task_id', Integer, ForeignKey('tasks.id'))    
)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    email: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'), unique=True)
    password: Mapped[str]
    profile_pic: Mapped[str|None] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    active: Mapped[bool] = mapped_column(default=True)
    access_level: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime]
    last_modified: Mapped[datetime|None]

    tasks_created: Mapped[list['Task']] = relationship(back_populates='created_by')

    workspaces: Mapped[list['Workspace']] = relationship('Workspace', secondary=member_workspace_association, back_populates='members')
    teams: Mapped[list['Team']] = relationship('Team', secondary=member_team_association, back_populates='members')
    projects: Mapped[list['Project']] = relationship('Project', secondary=member_project_association, back_populates='members')
    tasks: Mapped[list['Task']] = relationship('Task', secondary=member_tasks_association, back_populates='members')


class Workspace(Base):
    __tablename__ = 'workspaces'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    created_at: Mapped[datetime]
    last_modified: Mapped[datetime|None]

    teams: Mapped[list['Team']] = relationship(back_populates='workspace')
    members: Mapped[list['User']] = relationship('User', secondary=member_workspace_association, back_populates='workspaces')

class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    slug: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    active: Mapped[bool]
    created_at: Mapped[datetime]
    last_modified: Mapped[datetime|None]

    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspaces.id', ondelete='CASCADE'))
    workspace: Mapped['Workspace'] = relationship(back_populates='teams', foreign_keys=workspace_id)

    projects: Mapped[list['Project']] = relationship(back_populates='team')

    members: Mapped[list['User']] = relationship('User', secondary=member_team_association, back_populates='teams')

class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    color: Mapped[str]
    active: Mapped[bool]
    created_at: Mapped[datetime]
    last_modified: Mapped[datetime|None]
    
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id', ondelete='CASCADE'))
    team: Mapped["Team"] = relationship(back_populates='projects', foreign_keys=[team_id])

    tasks: Mapped['Task'] = relationship(back_populates='project')

    members: Mapped[list['User']] = relationship('User', secondary=member_project_association, back_populates='projects')

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    description: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    start_at: Mapped[datetime|None]
    due_on: Mapped[datetime|None]
    completed_at: Mapped[datetime|None]
    color: Mapped[str]
    created_at: Mapped[datetime]
    last_modified: Mapped[datetime|None]

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))
    project: Mapped[Project] = relationship(Project, back_populates='tasks')

    members: Mapped[list['User']] = relationship('User', secondary=member_tasks_association, back_populates='tasks')

    created_by_id: Mapped[int|None] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    created_by: Mapped[Optional['User']] = relationship(back_populates='tasks_created', foreign_keys=[created_by_id])

    parent_id: Mapped[int|None] = mapped_column(ForeignKey('tasks.id'))
    parent = relationship('Task', remote_side=[id], backref='subtasks')

class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    created_at: Mapped[datetime]
    last_modified: Mapped[datetime|None]

class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(StringEncryptedType(String, DB_ENCRYPTION_KEY, AesEngine, 'pkcs5'))
    color: Mapped[str]
    created_at: Mapped[datetime]
    last_modified: Mapped[datetime|None]