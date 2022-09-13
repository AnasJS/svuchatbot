from headerparser import scan_string
from src.svuchatbot_mogodb import SingletonClient


def parse(from_col="Inbox"):
    client = SingletonClient()
    db = client["PST"]
    col = db[from_col]
    for document in col.find({}):
        try:
            headers = scan_string(document["header"])
            headers = {k:v for k,v in headers if k}
            col.update_one({"_id":document["_id"]},{"$set":headers} )
            # col.update_one({"_id":document["_id"]},{"$set":[{k:v for k,v in headers if k}]})
        except Exception as e:
            #todo delete this document 62d9634df02a7ff6a29fb8cf
            print(document["_id"])
            print(e)

parse()