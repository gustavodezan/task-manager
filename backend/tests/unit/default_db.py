from app.dependencies import GetDBs
from app.database import get_db

dbs = GetDBs(get_db())

def close_db():
    get_db().mongodb_client.close()