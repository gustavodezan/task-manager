description = """
Task Manager API

## Users
You will be able to:

* **Read your current user**
* **Update your current user**
"""

from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

ACCESS_TOKEN_EXPIRE_TIME = int(config["ACCESS_TOKEN_EXPIRE_MINUTES"])
IS_PROD = config["IS_PROD"] == "True"
AUTH_ON = config["AUTH_ON"] == "True"