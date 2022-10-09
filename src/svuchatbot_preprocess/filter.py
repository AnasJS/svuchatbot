from src.svuchatbot_mogodb.client import get_collection
from langdetect import detect
import numpy as np
import pandas as pd
from src.svuchatbot_const.db.definitions import Definitions as DB_Definitions
import re
from os import cpu_count

from src.svuchatbot_helper.cleaner import StringCleaner
from src.svuchatbot_preprocess.simple_worker import SimpleWorker


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

    def exclude_empty_emails(self, field):
        self.t_col.delete_many({field: ""})
        return self

    def exclude_emails_writen_in_foreign_language(self, field):
        cursor = self.t_col.find()
        # mails = []
        for item in cursor:
            try:
                if detect(item[field]) != 'ar':
                    self.t_col.delete_one({"_id": item["_id"]})
                    # mails.append(item)
            except:
                print("item: ", item[field])
        return self

    def finding_incomprehensible_words(self):
        cursor = self.t_col.find({"root": {"$in": [""]}})
        words = []
        for item in cursor:
            tokens = np.asarray(item["simple-tokens"])
            roots = np.asarray(item["root"])
            for i in np.where(roots == "")[0].tolist():
                try:
                    if 0 < i < tokens.shape[0] - 1:
                        words.append((tokens[i - 1], tokens[i], tokens[i + 1]))
                    elif i == 0:
                        words.append(("", tokens[i], tokens[i + 1]))
                    elif i == tokens.shape[0] - 1:
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

    def exclude_duplicated(self, field):
        cursor = self.t_col.find()
        df = pd.DataFrame([d for d in cursor])
        df_target = df[field]
        df.drop(df[df_target.duplicated()].index, inplace=True)
        self.t_col.delete_many({})
        self.t_col.insert_many([d.to_dict() for d in df.iloc])
        return self

    def correct_sentences_old(self, field, sents, replacements):
        cursor = self.t_col.find()

        # def __do(fld, item, col):
        #     text = item[fld]
        #     for sent, rep in zip(sents, replacements):
        #         text = re.sub(sent, rep, text)
        #     item[field] = text
        #     col.replace_one({"_id": item["_id"]}, item)
        #
        # sw = SimpleWorker(
        #     source=(DB_Definitions.PARSSEDEMAILSDBNAME,
        #             DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
        #     n_cores=cpu_count(),
        #     field_name=field,
        #     do=__do
        # )
        # sw.work()
        sc = StringCleaner("")
        for item in cursor:
            try:
                sc.text = item[field]
                for sent, rep in zip(sents, replacements):
                    sc.correct_word(sent, rep)
                    item[field] = sc.text
                    self.t_col.replace_one({"_id": item["_id"]}, item)
            except Exception as e:
                print(e, "item: ", item[field])
        return self

    def correct_sentences(self, field, sents, replacements):
        for sent, rep in zip(sents, replacements):
            # print(f"*****{sent.strip()}******")

            def __do(fld, itm, col):
                # print(itm[fld])
                itm[fld] = re.sub(sent, rep, " "+itm[fld]+" ")
                # itm[fld] = re.sub(sent.strip(), rep, itm[fld])
                # print(itm[fld])
                # print("*******************************")
                col.replace_one({"_id": itm["_id"]}, itm)
            sw = SimpleWorker((DB_Definitions.PARSSEDEMAILSDBNAME,
                               DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                              field,
                              cpu_count(),
                              __do,
                              fltr={field: {"$regex": sent.strip()}})
            sw.work()
        # sc = StringCleaner("")
        # for item in cursor:
        #     try:
        #         sc.text = item[field]
        #         for sent, rep in zip(sents, replacements):
        #             sc.correct_word(sent, rep)
        #             item[field] = sc.text
        #             self.t_col.replace_one({"_id": item["_id"]}, item)
        #     except Exception as e:
        #         print(e, "item: ", item[field])
        return self
