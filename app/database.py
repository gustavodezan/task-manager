from deta import Deta
import os
from pathlib import Path
from dotenv import load_dotenv

# Project name: njudh
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
deta = Deta(os.getenv("DATABASE_KEY"))

user_db = deta.Base('users')
team_db = deta.Base('teams')
project_db = deta.Base('projects')
task_db = deta.Base('tasks')
tag_db = deta.Base('tags')
