from datetime import datetime
from os.path import join

import yaml
import os
from numpy import unique
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from src.svuchatbot_mogodb.client import get_collection
import pandas as pd
from src.svuchatbot_helper.cleaner import StringCleaner
from sklearn.preprocessing import StandardScaler
from src.svuchatbot_const.db.definitions import Definitions as DB_DEFINITIONS
from src.svuchatbot_helper.read_specializations import get_specializations
import numpy as np


class MyKmeans:
    def __init__(self, source, field_name, n_clusters, intent_file_name, utter_file_name, n_gram=1,
                 specializations_from_questions=True, specializations_from_answers=True):
        # self.model = AffinityPropagation(damping=0.9)
        self.columns = []
        self.intent_file_name = intent_file_name
        self.utter_file_name = utter_file_name
        self.model = KMeans(n_clusters=n_clusters)
        self.mails_col_name = source[0][1]
        self.mails_db_name = source[0][0]
        self.BOW_col_name = source[1][1]
        self.BOW_db_name = source[1][0]
        self.field_name = field_name
        self.X = None
        self.cleaner = StringCleaner("")
        if os.path.exists(self.utter_file_name):
            os.remove(self.utter_file_name)
        if os.path.exists(self.intent_file_name):
            os.remove(self.intent_file_name)
        self.n_gram = n_gram
        self.specializations_from_questions = specializations_from_questions
        self.specializations_from_answers = specializations_from_answers

    def fetch_specializations(self):
        col = get_collection(self.mails_db_name, self.mails_col_name)

        cursor = col.find({},
                          {
                              DB_DEFINITIONS.SPECIALWORDSFIELDNAMEFROMANSWER: 1,
                              DB_DEFINITIONS.SPECIALWORDSFIELDNAMEFROMANSWER: 1,
                          })
        specializations = get_specializations()
        spec_nikname = specializations["name0"].values.tolist()
        res = []
        for item in cursor:
            sw = np.zeros(len(spec_nikname)).reshape((1, -1))
            sw_df = pd.DataFrame(np.append(item["_id"], sw).reshape(1, -1), columns=["_id"] + spec_nikname)
            if self.specializations_from_answers:
                for spw in item[DB_DEFINITIONS.SPECIALWORDSFIELDNAMEFROMANSWER]:
                    sw_df[spw[0]] += 1
            if self.specializations_from_questions:
                for spw in item[DB_DEFINITIONS.SPECIALWORDSFIELDNAMEFROMQUESTION]:
                    sw_df[spw[0]] += 1
            res.append(sw_df.values.ravel())
        # container = np.array(res).reshape(col.count_documents({}), len(spec_nikname)+1)
        df = pd.DataFrame(res, columns=["_id"] + spec_nikname).set_index("_id")
        return df

    def fetch(self):
        dfs = []
        if self.specializations_from_answers or self.specializations_from_questions:
            spw_df = self.fetch_specializations()
            print(spw_df)
            dfs.append(spw_df)
        for i in range(1, self.n_gram + 1):
            bow_col = get_collection(self.BOW_db_name, "{}-Gram".format(i))
            dfs.append(pd.DataFrame(bow_col.find({})).set_index("_id"))
        self.df_X = pd.concat(dfs, axis=1, join='inner').reset_index()
        columns = self.df_X.columns.tolist()
        columns.remove("_id")
        self.X = self.df_X[columns].values
        self.columns = columns
        print(self.df_X.head(5))
        print(self.columns)

    def fetch_old(self):
        if self.n_gram == 1:
            bow_col = get_collection(self.BOW_db_name, self.BOW_col_name)
            self.df_X = pd.DataFrame(bow_col.find({}))
            if self.specializations_from_answers or self.specializations_from_questions:
                spw_df = get_specializations()
                self.df_X = pd.concat(
                    [
                        self.df_X.set_index("_id"),
                        spw_df.set_index("_id")
                    ],
                    axis=1, join='inner').reset_index()
            columns = self.df_X.columns.tolist()
            columns.remove("_id")
            self.X = self.df_X[columns].values
            self.columns = columns
        elif self.n_gram > 1:
            dfs = []
            # df3 = pd.concat([df1.set_index("_id"), df2.set_index("_id")], axis=1, join='inner').reset_index()
            if self.specializations_from_answers or self.specializations_from_questions:
                spw_df = get_specializations()
                dfs.append(spw_df)
            for i in range(1, self.n_gram + 1):
                bow_col = get_collection(self.BOW_db_name, "{}-Gram".format(i))
                dfs.append(pd.DataFrame(bow_col.find({})).set_index("_id"))
            self.df_X = pd.concat(dfs, axis=1, join='inner').reset_index()
            columns = self.df_X.columns.tolist()
            columns.remove("_id")
            self.X = self.df_X[columns].values
            self.columns = columns

    def standardization(self):
        scaler = StandardScaler()
        self.segmentation_std = scaler.fit_transform(self.df_X[self.columns])

    def calculate_pca(self):
        self.segmentation_std = self.df_X[self.columns]
        self.pca = PCA()
        print(self.segmentation_std)
        self.pca.fit(self.segmentation_std)
        plt.figure(figsize=(10, 8))
        plt.plot(range(len(self.pca.explained_variance_ratio_)),
                 self.pca.explained_variance_ratio_.cumsum(),
                 )
        plt.title("Explained Variance by Components")
        plt.xlabel("Number of Components")
        plt.ylabel("Cumulative Explained Variance")
        plt.show()
        self.feature_number = int(input("Enter the number of components"))
        self.pca = PCA(n_components=self.feature_number)
        self.pca.fit(self.segmentation_std)
        self.pca_scores = self.pca.transform(self.segmentation_std)
        print(self.pca_scores)

    def kmeans_with_pca_fit(self):
        wcss = []
        for i in range(10, 200, 5):
            kmeans_pca = KMeans(n_clusters=i, init="k-means++", random_state=420)
            kmeans_pca.fit(self.pca_scores)
            wcss.append(kmeans_pca.inertia_)
        plt.figure(figsize=(10, 8))
        plt.plot(range(10, 200, 5), wcss)
        plt.title("k-means with PCA clustering")
        plt.xlabel("Number of clusters")
        plt.ylabel("wcss")
        plt.show()
        self.k_means_clusters = int(input("Enter number of cluster"))
        self.model = KMeans(n_clusters=self.k_means_clusters, init="k-means++", random_state=42)
        self.model.fit(self.pca_scores)
        self.df_X["tag"] = self.model.labels_

    def update_db(self):
        col = get_collection(self.mails_db_name, self.mails_col_name)
        cursor = col.find({})
        # df_X_new = self.df_X.copy(deep=True)
        # df_X_new = df_X_new.set_index("_id")
        # df_X_new = df_X_new["tag"]
        df_X_new  = pd.DataFrame()
        df_X_new["_id"] = self.df_X["_id"]
        df_X_new["tag"] = self.df_X["tag"]
        df_X_new = df_X_new.set_index("_id")

        mails_df = pd.DataFrame(cursor).set_index("_id")
        res_df = pd.merge(mails_df, df_X_new, left_index=True, right_index=True)
        err_msg = f"update db after k-means clustering : There is an error in shape " \
                  f"{res_df.shape}, {mails_df.shape}, {df_X_new.shape}"
        assert res_df.shape[0] == mails_df.shape[0] == df_X_new.shape[0], err_msg
        col.delete_many({})
        col.insert_many([iloc.to_dict() for iloc in res_df.reset_index().iloc])

    def kmeans_fit(self):
        wcss = []
        for i in range(10, 200, 5):
            kmeans = KMeans(n_clusters=i, init="k-means++", random_state=420)
            kmeans.fit(self.df_X[self.columns])
            wcss.append(kmeans.inertia_)
        plt.figure(figsize=(10, 8))
        plt.plot(range(10, 200, 5), wcss)
        plt.title("k-means with PCA clustering")
        plt.xlabel("Number of clusters")
        plt.ylabel("wcss")
        plt.show()
        self.k_means_clusters = int(input("Enter number of cluster"))
        self.model = KMeans(n_clusters=self.k_means_clusters, init="k-means++", random_state=42)
        self.model.fit(self.pca_scores)
        self.df_X["tag"] = self.model.labels_

    def fit(self):
        self.model.fit(self.X)
        self.df_X["tag"] = self.model.labels_
        print(self.model.get_feature_names_out())
        print(self.model.score(self.X))

    def to_yaml(self):
        clusters = unique(self.model.labels_)
        intent_dict = {}
        utter_dict = {}
        mails_col = get_collection(self.mails_db_name, self.mails_col_name)
        for cluster in clusters:
            ids = self.df_X[self.df_X["tag"] == cluster]["_id"]
            intent = []
            utter = []
            for id in ids:
                self.cleaner.text = mails_col.find_one({"_id": id}, {"_id": 0, "body": 1})["body"]
                self.cleaner.drop_new_line(). \
                    drop_meta_data_of_message(). \
                    drop_special_word("Original Message"). \
                    drop_special_characters(). \
                    drop_many_spaces()
                intent.append(
                    self.cleaner.text
                )
                self.cleaner.text = mails_col.find_one({"_id": id}, {"_id": 0, "replay-message": 1})["replay-message"]
                self.cleaner.drop_new_line(). \
                    drop_special_characters(). \
                    drop_meta_data_of_message(). \
                    drop_special_word("Original Message"). \
                    drop_many_spaces()
                utter.append(
                    self.cleaner.text
                )
            intent_dict[cluster.__str__()] = intent
            utter_dict[cluster.__str__()] = utter
        for k, v in intent_dict.items():
            print(k)
            for vv in v:
                print(f"\t{vv}")
        for k, v in utter_dict.items():
            print(k)
            for vv in v:
                print(f"\t{vv}")
        name = f'result_rasa_{datetime.now()}'.replace(':',"_").replace('.',"_").replace('-','_').replace(' ','__')
        name = join("result", name)
        os.mkdir(name)
        yaml.dump(intent_dict, open(join(name, self.intent_file_name), "wt"), allow_unicode=True)
        yaml.dump(utter_dict, open(join(name, self.utter_file_name), "wt"), allow_unicode=True)
