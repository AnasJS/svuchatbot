from svuchatbot_mogodb.client import get_collection
from langdetect import detect

class Filter:
    def __init__(self, source: tuple, target: tuple):
        self.s_db_name, self.s_col_name = source
        self.t_db_name, self.t_col_name = target
        self.s_col = get_collection(self.s_db_name, self.s_col_name)
        self.t_col = get_collection(self.t_db_name, self.t_col_name)
        self.t_col.delete_many({})
        self.t_col.insert_many(self.s_col.find({}))

    def exclude_emails_containing_word(self, field, word):
        self.t_col.delete_many({field: {"$regex": word}})
        return self


    def exclude_emails_writen_in_foreign_language(self, field):
        cursor = self.t_col.find()
        # mails = []
        for item in cursor:
            try:
                if detect(item[field]) == 'ar':
                    self.t_col.delete_one({"_id": item["_id"]})
                    # mails.append(item)
            except:
                print("item: ", item[field])



