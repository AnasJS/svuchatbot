
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arabic_reshaper
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer

from sklearn.metrics.pairwise import cosine_similarity

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import SingletonClient, get_collection
from svuchatbot_preprocess.cleand_tokens_extractor import Elector
from svuchatbot_preprocess.extractor import Extractor
from arabicstopwords.arabicstopwords import stopwords_list

from svuchatbot_preprocess.tokens_extractor import TokensExtractor
from svuchatbot_preprocess.bag_of_words_extractor import BagOfWordsExtractor

class KeyWordExtractors():
    def __init__(self, source, min_weight, field_name, cpu_count, ngram="1-Gram"):
        # super().__init__(source, field_name, n_cores)
        self.source = source
        # self.bow_col_name = source[0][1]
        # self.bow_db_name = source[0][0]
        # self.mit_col_name = source[1][1]
        # self.mit_db_name = source[1][0]
        # self.tfidf_col_name = target[0][1]
        # self.tfidf_db_name = target[0][0]
        # self.mibow_col_name = target[1][1]
        # self.mibow_db_name = target[1][0]
        # self.mif_col_name = target[2][1]
        # self.mif_db_name = target[2][0]
        self.ngram = ngram
        self.min_weight = min_weight
        #
        self.cpu_count = cpu_count
        self.field_name = field_name

    def __tokenize(self):
        te = TokensExtractor(self.source, self.field_name, self.cpu_count, target=("", "tokens"))
        te.work()
        e = Elector(source=self.source, field_name="tokens", n_cores=self.cpu_count)
        e.work()

    def __extract_bag_of_word(self):
        boe = BagOfWordsExtractor(self.source, field_name="tokens", n_cores=self.cpu_count,
                                  target=("Bag-Of-Words", self.ngram), n_gram=int(self.ngram[0]))
        boe.work()

    def __most_important_bag_of_words(self):
        bow_col = get_collection("Bag-Of-Words", self.ngram)
        bow = bow_col.find({})
        bow = list(bow)
        feature_names = list(bow_col.find_one().keys())
        feature_names.remove("_id")
        self.feature_names = feature_names
        self.df_bag_of_words = pd.DataFrame(bow)[self.feature_names]
        self.bag_of_words = self.df_bag_of_words.values
        return bow

    def __tfidf(self):
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(self.bag_of_words)
        df_tfidf = pd.DataFrame(tfidf.todense(), columns=self.feature_names)
        col_tfidf = get_collection("TF-IDF", self.ngram)
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
        # df_weights = df_weights[df_weights['weight'] > self.min_weight]
        # df_tfidf = df_tfidf[df_weights['word']]
        col_tfidf.insert_many([iloc.to_dict() for iloc in df_tfidf.iloc])
        # col_tfidf.insert_many([{k:v for k,v in zip(self.feature_names, row.tolist())} for row in tfidf.toarray()])
        col = get_collection("Weights", self.ngram)
        col.insert_many([iloc.to_dict() for iloc in df_weights.iloc])

    def work(self):
        print("Start extracting tokens")
        self.__tokenize()
        print("start extract bag of words")
        self.__extract_bag_of_word()
        print("start create vector of counter")
        self.__most_important_bag_of_words()
        print("start calculate tfidf")
        self.__tfidf()

