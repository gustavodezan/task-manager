from dotenv import dotenv_values
from pymongo import MongoClient


config = dotenv_values(".env")

class Database:
    def __init__(self):
        self.mongodb_client: MongoClient = MongoClient(config["TASKDB_URL"])
        self.core = self.mongodb_client[config["TASK_DB_NAME"]]
        self.manager = self.core["manager"]
        self.user = self.core["user"]
        self.team = self.core["team"]
        print("Connected to the MongoDB database!")

    def Close(self):
        print("Closing connection")
        self.mongodb_client.close()

db = Database()

def get_db():
    return db
# mongodb_client: MongoClient = MongoClient(config["CHATDB_URL"])
# database = mongodb_client[config["CHAT_DB_NAME"]]
