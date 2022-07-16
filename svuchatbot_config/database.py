import os
import yaml
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(ROOT_DIR, 'database.yml')
db_connection_params = {}

with open(path, 'r') as f:
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    for x in docs:
        for k, v in x.items():
            db_connection_params[k] = v
    # Todo remove env
    env = 'dev'
    db_connection_params = db_connection_params[env]

# print('#############################b_connection_params : {}*****'.format(db_connection_params))

def get_db_uri():
    # db_connection_params = get_params_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.yml'))

    # override(db_connection_params[environment], "FabSight_DB_%s_" % environment.upper())
    uri = '{host}:{port}/'.format(**db_connection_params)  # mongodb://
    if ('username' in db_connection_params) and ('password' in db_connection_params):
        uri = ("{username}:{password}@" + uri).format(**db_connection_params)
    db_connection = {k: v for k, v in db_connection_params.items() if
                     k not in ['db', 'host', 'username', 'password', 'port']}
    if db_connection:
        uri += "?"
        for (k, v) in db_connection.items():
            uri += k + "=" + str(v).lower() + "&"
        uri = uri[:-1]
    uri = "mongodb://" + uri
    print(uri)
    return uri