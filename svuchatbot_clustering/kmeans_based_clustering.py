import yaml
import os
from numpy import unique
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from svuchatbot_mogodb.client import get_collection
import pandas as pd
from svuchatbot_helper.cleaner import StringCleaner
from sklearn.preprocessing import StandardScaler

class MyKmeans:
    def __init__(self, source, field_name, n_clusters, intent_file_name, utter_file_name, n_gram):
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

    def fetch(self):
        bow_col = get_collection(self.BOW_db_name, self.BOW_col_name)
        self.df_X = pd.DataFrame(bow_col.find({}))
        columns = self.df_X.columns.tolist()
        columns.remove("_id")
        self.X = self.df_X[columns].values
        self.columns = columns

    def standardization(self):
        scaler = StandardScaler()
        self.segmentation_std = scaler.fit_transform(self.df_X[self.columns])

    def calculate_pca(self):
        self.pca = PCA()
        self.pca.fit(self.segmentation_std)
        plt.figure(figsize=(10,8))
        plt.plot(range(len(self.pca.explained_variance_ratio_)),
                 self.pca.explained_variance_ratio_.cumsum(),
                 )
        plt.title("Explained Variance by Components")
        plt.xlabel("Number of Components")
        plt.ylabel("Cumulative Explained Variance")
        plt.show()
        self.feature_number = int(input("Enter the number of feature"))
        self.pca = PCA(n_components= self.feature_number)
        self.pca.fit(self.segmentation_std)
        self.pca_scores = self.pca.transform(self.segmentation_std)

    def kmeans_fit(self):
        wcss = []
        for i in range(10,200, 5):
            kmeans_pca = KMeans(n_clusters= i, init="k-means++", random_state=420)
            kmeans_pca.fit(self.pca_scores)
            wcss.append(kmeans_pca.inertia_)
        plt.figure(figsize=(10,8))
        plt.plot(range(10,200,5), wcss)
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

        yaml.dump(intent_dict, open(self.intent_file_name, "wt"), allow_unicode=True)
        yaml.dump(utter_dict, open(self.utter_file_name, "wt"), allow_unicode=True)
