from svuchatbot_mogodb.client import get_client
from svuchatbot_config.database import db_connection_params


def read_intents(lang='arabic',collection_name='arabic_intents'):

    db_client = get_client()
    db = db_client[db_connection_params['db']]
    col = db[collection_name]
    documents = [document for document in col.find({}) ]
    return documents


