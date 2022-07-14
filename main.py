from svuchatbot_config.database import get_db_uri, db_connection_params
from svuchatbot_mogodb.client import get_client
# print(get_db_uri())
print(db_connection_params)
c = get_db_uri()
cc = get_client()