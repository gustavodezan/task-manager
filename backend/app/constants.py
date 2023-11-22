description = """
Task Manager API

## Users
You will be able to:

* **Read your current user**
* **Update your current user**
"""

from dotenv import dotenv_values

config = dotenv_values(".env")

ACCESS_TOKEN_EXPIRE_TIME = int(config["ACCESS_TOKEN_EXPIRE_MINUTES"])
DB_ENCRYPTION_KEY = config['DB_ENCRYPTION_KEY']
SECRET_KEY = config['SECRET_KEY'] # token_key
IS_PROD = config["IS_PROD"] == "True"
AUTH_ON = config["AUTH_ON"] == "True"
DATABASE_URL = config['DATABASE_URL']