from src.svuchatbot_const.db.definitions import Definitions as DB_Definitions
from src.svuchatbot_mogodb.client import get_collection

col = get_collection(DB_Definitions.PARSSEDEMAILSDBNAME, DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME)
for item in col.find():

    try:
        # item.pop(DB_Definitions.SIMPLETOKENSFIELDNAME)
        item.pop(DB_Definitions.QUESTIONSIMPLETOKENSFIELDNAME)
        item.pop(DB_Definitions.ANSWERSIMPLETOKENSFIELDNAME)
        col.replace_one({"_id": item["_id"]}, item)
    except:
        pass