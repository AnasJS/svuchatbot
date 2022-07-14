from pymongo import MongoClient
from svuchatbot_config.database import get_db_uri
def get_client():
    return MongoClient(get_db_uri())