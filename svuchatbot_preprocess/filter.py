from svuchatbot_mogodb.client import get_collection
from langdetect import detect

class Filter:
    def __init__(self, source: tuple, target: tuple):
        self.s_db, self.s_col = source
        self.t_db, self.t_col = target

    def exclude_emails_containing_word(self, field, word):
        col = get_collection(self.s_db, self.s_col)
        cursor = col.find({field:{"$not":{"$regex" : word}}})
        t_col = get_collection(self.t_db, self.t_col)
        t_col.insert_many(cursor)

    def exclude_emails_writen_in_foreign_language(self, field):
        col = get_collection(self.s_db, self.s_col)
        cursor = col.find()
        mails = []
        for item in cursor:

            try:
                if detect(item[field]) == 'ar':
                    mails.append(item)
            except:
                print("item: ", item[field])
        t_col = get_collection(self.t_db, self.t_col)
        t_col.insert_many(mails)

