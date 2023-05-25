from dotenv import dotenv_values
from pymongo import MongoClient


config = dotenv_values(".env")

class Database:
    def __init__(self):
        self.mongodb_client: MongoClient = MongoClient(config["CHATDB_URL"])
        self.core = self.mongodb_client[config["CHAT_DB_NAME"]]
        self.rooms = self.core["rooms"]

    def Close(self):
        print("Closing connection")
        self.mongodb_client.close()

db = Database()

def get_db():
    return db
# mongodb_client: MongoClient = MongoClient(config["CHATDB_URL"])
# database = mongodb_client[config["CHAT_DB_NAME"]]
