
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arabic_reshaper
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer

from sklearn.metrics.pairwise import cosine_similarity

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import SingletonClient, get_collection
from svuchatbot_preprocess.extractor import Extractor
from arabicstopwords.arabicstopwords import stopwords_list

class KeyWordExtractors():
    def __init__(self, source, target, min_weight, ngram="1-Gram"):
        # super().__init__(source, field_name, n_cores)
        self.bow_col_name = source[0][1]
        self.bow_db_name = source[0][0]
        self.mit_col_name = source[1][1]
        self.mit_db_name = source[1][0]
        self.tfidf_col_name = target[0][1]
        self.tfidf_db_name = target[0][0]
        self.mibow_col_name = target[1][1]
        self.mibow_db_name = target[1][0]
        self.mif_col_name = target[2][1]
        self.mif_db_name = target[2][0]
        self.ngram = ngram
        self.min_weight = min_weight
        #
        # self.field_name = field_name


    def __most_important_bag_of_words(self):
        bow_col = get_collection(self.bow_db_name, self.bow_col_name)
        mit_col = get_collection(self.mit_db_name, self.mit_col_name)
        mibow_col = get_collection(self.mibow_db_name, self.ngram)
        mit = [item['word'] for item in mit_col.find({}, ['word'])]
        # self.feature_names = np.asarray(mit)
        bow = bow_col.find({})
        # bow = bow_col.find({}, mit)
        mibow = list(bow)
        mibow_col.insert_many(mibow)
        feature_names = list(bow_col.find_one().keys())
        feature_names.remove("_id")
        self.feature_names = feature_names
        # return mibow_col
        self.df_bag_of_words = pd.DataFrame(mibow)[self.feature_names]
        self.bag_of_words = self.df_bag_of_words.values
        return mibow

    def __tfidf(self):
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(self.bag_of_words)
        df_tfidf = pd.DataFrame(tfidf.todense(), columns=self.feature_names)
        col_tfidf = get_collection(self.tfidf_db_name, self.ngram)
        # col_tfidf.insert_many([{k:v for k,v in zip(self.feature_names, row.tolist())} for row in tfidf.toarray()])
        # Find most popular words and highest weights
        word_cnts = np.asarray(self.bag_of_words.sum(axis=0)).ravel().tolist()  # for each word in column, sum all row counts
        df_cnts = pd.DataFrame({'word': self.feature_names, 'count': word_cnts})
        df_cnts = df_cnts.sort_values('count', ascending=False)

        # Build word weights as a list and sort them
        weights = np.asarray(tfidf.mean(axis=0)).ravel().tolist()
        df_weights = pd.DataFrame({'word': self.feature_names, 'weight': weights})
        df_weights = df_weights.sort_values('weight', ascending=False)

        df_weights = df_weights.merge(df_cnts, on='word', how='left')
        df_weights = df_weights[['word', 'count', 'weight']]
        df_weights = df_weights[df_weights['weight'] > self.min_weight]
        df_tfidf = df_tfidf[df_weights['word']]
        col_tfidf.insert_many([iloc.to_dict() for iloc in df_tfidf.iloc])
        # col_tfidf.insert_many([{k:v for k,v in zip(self.feature_names, row.tolist())} for row in tfidf.toarray()])
        col = get_collection(self.mif_db_name, self.ngram)
        col.insert_many([iloc.to_dict() for iloc in df_weights.iloc])


    def _do(self, items ):
        pass

    def build_vectorizer(self, sentences, vocab=None, min_df=0.0, max_df=1.0,
                         ngram_range=(1, 1)):  # for a 2-gram use: ngram_range=(1,2)
        '''
        Build the tf-idf vectorizer:
        1. Build the count_vectorizer from the input sentences.
        2. Transform count_vectorizer to bag-of-words.
        3. Fit the transform to the bag-of-words.

        Note:
        Alternatively we can do this directly with 'TfidfVectorizer' instead of using 'CountVectorizer' followed by 'TfidfTransformer'

        Return:
        cvec, feature_names, df_bag_of_words, tfidf, df_weights, cos_sim, samp_dist
        '''

        # Build count vectorizer
        count_vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, vocabulary=vocab,
                                           ngram_range=(1,3), stop_words=stopwords_list())
        # stop_words='english, max_features=N_FEATURES
        cvec = count_vectorizer.fit(sentences)

        # Get feature names
        feature_names = cvec.get_feature_names()
        # Get bag-of-words and analyze
        bag_of_words = cvec.transform(sentences)
        df_bag_of_words = pd.DataFrame(bag_of_words.todense(), columns=feature_names)

        # Transform bag_of_words into tf-idf matrix
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(bag_of_words)

        # Find most popular words and highest weights
        word_cnts = np.asarray(bag_of_words.sum(axis=0)).ravel().tolist()  # for each word in column, sum all row counts
        df_cnts = pd.DataFrame({'word': feature_names, 'count': word_cnts})
        df_cnts = df_cnts.sort_values('count', ascending=False)

        # Build word weights as a list and sort them
        weights = np.asarray(tfidf.mean(axis=0)).ravel().tolist()
        df_weights = pd.DataFrame({'word': feature_names, 'weight': weights})
        df_weights = df_weights.sort_values('weight', ascending=False)

        df_weights = df_weights.merge(df_cnts, on='word', how='left')
        df_weights = df_weights[['word', 'count', 'weight']]

        # Cosine similarity of sentences
        cos_sim = cosine_similarity(tfidf, tfidf)

        # Distance matrix of sentences
        samp_dist = 1 - cos_sim

        return cvec, feature_names, df_bag_of_words, tfidf, df_weights, cos_sim, samp_dist

    def work(self):
        print("start create vector of counter")
        self.__most_important_bag_of_words()
        print("start calculate tfidf")
        self.__tfidf()

    def __work(self):
        mibow = self.__most_important_bag_of_words()
        df_bag_of_words = pd.DataFrame(mibow)
        cvec, feature_names, df_bag_of_words, tfidf, df_weights, cos_sim, samp_dist = self.build_vectorizer(
            [item[self.field_name] for item in get_collection(self.db_name, self.col_name).find({},[self.field_name])])

        df_tfidf = pd.DataFrame(tfidf.todense(), columns=feature_names)
        # res = {message_id:tf_idf_row for message_id,tf_idf_row in zip(sentences.keys(), df_tfidf.iloc)}
        col = get_collection(self.db_name, self.col_name)
        sentences = [item[self.field_name] for item in col.find({}, [self.field_name])][:10]
        print("%d dummy sentences:" % len(sentences))
        print("---")
        print("%d feature_names (each feature represents a distinct word):" % len(feature_names))
        print(feature_names)
        print("---")
        print("df_tfidf[%d,%d]:" % (len(sentences), len(feature_names)))
        print(df_tfidf.to_string())
        print("---")
        print("df_weights:")
        print(df_weights)
        print("---")
        print("cos_sim[%d,%d] (a square matrix of length and width = len(sentences)):" % (len(sentences), len(sentences)))
        print(cos_sim)
        print("df_bag_of_words[%d,%d]:" % (len(sentences), len(feature_names)))
        print(df_bag_of_words)
