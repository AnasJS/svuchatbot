from pymongo import MongoClient
from svuchatbot_config.database import get_db_uri


class SingletonClient(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClient, cls).__new__(cls)
            cls.instance.client = MongoClient(get_db_uri())
        return cls.instance.client
