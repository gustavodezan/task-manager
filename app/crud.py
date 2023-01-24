from app.database import user_db, team_db, project_db, task_db, tag_db

from utils.encryption import encrypt, decrypt_user, decrypt_user_preview

# User
def get_user(key: str):
    """Get user by id"""
    return decrypt_user(user_db.get(key))

def get_user_raw(key:str):
    return user_db.get(key)

def get_users_raw():
    return user_db.fetch().items

def fetch_users(query: dict):
    return user_db.fetch(query).items

def create_user(user: dict):
    """Create new team"""
    return user_db.insert(user)


# Tags
def get_tag(key: str):
    """Get tag by id"""
    return tag_db.get(key)

def create_tag(tag: dict):
    return tag_db.insert(tag)


# Tasks
def get_task(key: str):
    """Get tasks by id"""
    return task_db.get(key)

def create_tasks(task: dict):
    return task_db.insert(task)


# Projects
def get_projects(key: str):
    """Get projects by id"""
    return project_db.get(key)

def create_projects(project: dict):
    return project_db.insert(project)


# Team
def get_team(key: str):
    """Get team by id"""
    return team_db.get(key)

def create_team(team: dict):
    """Create new team"""
    return team_db.insert(team)

def update_team(team: dict):
    """Update team"""
    return team_db.put(team)