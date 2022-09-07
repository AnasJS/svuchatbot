from svuchatbot_mogodb.client import get_collection
from langdetect import detect
import numpy as np
import pandas as pd


class Filter:
    def __init__(self, source: tuple, target: tuple):
        self.s_db_name, self.s_col_name = source
        self.t_db_name, self.t_col_name = target
        self.s_col = get_collection(self.s_db_name, self.s_col_name)
        self.t_col = get_collection(self.t_db_name, self.t_col_name)
        if source != target:
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

    def finding_incomprehensible_words(self):
        cursor = self.t_col.find({"root": {"$in": [""]}})
        words = []
        for item in cursor:
            tokens = np.asarray(item["simple-tokens"])
            roots = np.asarray(item["root"])
            for i in np.where(roots=="")[0].tolist():
                try:
                    if 0 < i < tokens.shape[0]-1:
                        words.append((tokens[i-1], tokens[i], tokens[i+1]))
                    elif i==0 :
                        words.append(("", tokens[i], tokens[i+1]))
                    elif i==tokens.shape[0]-1:
                        words.append((tokens[i - 1], tokens[i], ""))
                except Exception as e:
                    print(i)
                    print(tokens.shape[0])
                    print(tokens)
                    print(roots)
                    print(e)
                    print("*********************************")
        df = pd.DataFrame(words, columns=["word0", "word1", "word2"])
        df.to_csv("incomprehensible_words.csv")
        return self



