import numpy as np
import yaml
import os
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import KMeans
from matplotlib import pyplot
from svuchatbot_mogodb.client import get_collection
import pandas as pd
from nltk.tokenize import sent_tokenize
from svuchatbot_helper.cleaner import StringCleaner


class MyKmeans:
    def __init__(self, source, field_name):
        # self.model = AffinityPropagation(damping=0.9)
        self.model = KMeans(n_clusters=25)
        self.mails_col_name = source[0][1]
        self.mails_db_name = source[0][0]
        self.BOW_col_name = source[1][1]
        self.BOW_db_name = source[1][0]
        self.field_name = field_name
        self.X = None
        self.cleaner = StringCleaner("")

    def fit(self):
        bow_col = get_collection(self.BOW_db_name, self.BOW_col_name)
        self.df_X = pd.DataFrame(bow_col.find({}))
        columns = self.df_X.columns.tolist()
        columns.remove("_id")
        self.X = self.df_X[columns].values
        self.model.fit(self.X)
        self.df_X["tag"] = self.model.labels_

    def to_yaml(self):
        clusters = unique(self.model.labels_)
        intent_dict = {}
        utter_dict = {}
        mails_col = get_collection(self.mails_db_name, self.mails_col_name)
        # mails_df = pd.DataFrame(mails)
        for cluster in clusters:
            ids = self.df_X[self.df_X["tag"] == cluster]["_id"]
            intent = []
            utter = []
            for id in ids:
                self.cleaner.text = mails_col.find_one({"_id": id}, {"_id": 0, "body": 1})["body"]
                self.cleaner.drop_new_line().\
                    drop_meta_data_of_message().\
                    drop_special_word("Original Message").\
                    drop_special_characters().\
                    drop_many_spaces()
                intent.append(
                    # mails_col.find_one({"_id":id}, {"_id":0, "body":1})["body"].replace("\r\n", "")
                    self.cleaner.text
                )
                self.cleaner.text = mails_col.find_one({"_id": id}, {"_id": 0, "replay-message": 1})["replay-message"]
                self.cleaner.drop_new_line().\
                    drop_special_characters(). \
                    drop_meta_data_of_message(). \
                    drop_special_word("Original Message").\
                    drop_many_spaces()
                utter.append(
                    self.cleaner.text
                    # mails_col.find_one({"_id": id}, {"_id": 0, "replay-message": 1})["replay-message"].replace("\r\n","")
                )
            # print(len(row_ix))
            # if len(row_ix[0]) > 0:
            intent_dict[cluster.__str__()] = intent
            utter_dict[cluster.__str__()] = utter
            # print(cluster.__str__())
        if os.path.exists("kutter.yml"):
            os.remove("kutter.yml")
        if os.path.exists("kintent.yml"):
            os.remove("kintent.yml")
        yaml.dump(intent_dict, open("kintent.yml", "wt"), allow_unicode=True)
        yaml.dump(utter_dict, open("kutter.yml", "wt"), allow_unicode=True)



