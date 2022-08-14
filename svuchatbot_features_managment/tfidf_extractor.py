from sklearn.feature_extraction.text import TfidfTransformer
from svuchatbot_mogodb.client import get_collection
import pandas as pd
import numpy as np


class TFIDFExtractor:
    def __init__(self, bag_of_words, ngram, feature_names, tfidf_db_name="TF-IDF", weights_db_name="Weights"):
        self.ngram = ngram
        self.bag_of_words = bag_of_words
        self.feature_names = feature_names
        self.tfidf_db_name = tfidf_db_name
        self.weights_db_name = weights_db_name

    def work(self):
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(self.bag_of_words)
        df_tfidf = pd.DataFrame(tfidf.todense(), columns=self.feature_names)
        col_tfidf = get_collection(self.tfidf_db_name, self.ngram)
        word_cnts = np.asarray(
            self.bag_of_words.sum(axis=0)).ravel().tolist()  # for each word in column, sum all row counts
        df_cnts = pd.DataFrame({'word': self.feature_names, 'count': word_cnts})
        df_cnts = df_cnts.sort_values('count', ascending=False)

        # Build word weights as a list and sort them
        weights = np.asarray(tfidf.mean(axis=0)).ravel().tolist()
        df_weights = pd.DataFrame({'word': self.feature_names, 'weight': weights})
        df_weights = df_weights.sort_values('weight', ascending=False)

        df_weights = df_weights.merge(df_cnts, on='word', how='left')
        df_weights = df_weights[['word', 'count', 'weight']]
        col_tfidf.insert_many([iloc.to_dict() for iloc in df_tfidf.iloc])
        col = get_collection(self.weights_db_name, self.ngram)
        col.insert_many([iloc.to_dict() for iloc in df_weights.iloc])
