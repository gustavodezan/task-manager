from app.database import user_db, team_db, project_db, task_db, tag_db
import app.schemas as schemas
from utils.encryption import encrypt, decrypt_user, decrypt_user_preview

# User
class User:
    def get(key: str):
        """Get user by id"""
        return decrypt_user(user_db.get(key))

    def get_raw(key:str):
        return user_db.get(key)

    def get_users_raw():
        return user_db.fetch().items

    def fetch(query: dict):
        return user_db.fetch(query).items

    def create(user: dict):
        """Create new team"""
        return user_db.insert(user)


# Tags
class Tags:
    def get(key: str):
        """Get tag by id"""
        return tag_db.get(key)

    def create(tag: dict):
        return tag_db.insert(tag)


# Tasks
class Task:
    def get(key: str):
        """Get tasks by id"""
        return task_db.get(key)

    def create(task: dict):
        return task_db.insert(task)


# Projects
class Project:
    def get(key: str):
        """Get projects by id"""
        return project_db.get(key)

    def fetch(query: dict):
        return project_db.fetch(query).items

    def create(project: dict):
        return project_db.insert(project)


# Team
class Team:
    def get(self, key: str):
        """Get team by id"""
        return team_db.get(key)

    def fetch(query: str):
        return team_db.fetch(query).items

    def create(team: dict):
        """Create new team"""
        return team_db.insert(team)

    def update(team: dict):
        """Update team"""
        return team_db.put(team)