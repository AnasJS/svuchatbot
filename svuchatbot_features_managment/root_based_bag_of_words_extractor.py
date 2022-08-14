# from sklearn.feature_extraction.text import TfidfTransformer
#
# from svuchatbot_features_managment.features_extractor import MorphologicalFeaturesExtractor
from svuchatbot_features_managment.key_words_extractor import KeyWordExtractors
# from svuchatbot_features_managment.simple_tokens_extractor import SimpleTokensExtractor
from svuchatbot_mogodb.client import get_collection, SingletonClient
from svuchatbot_preprocess.bag_of_words_extractor import BagOfWordsExtractor
from svuchatbot_features_managment.features_extractor import MorphologicalFeaturesExtractor
# import numpy as np
# import pandas as pd


class RootBasedBagOfWordsExtractor(KeyWordExtractors):

    def _reset_db(self):
        # super(RootBasedBagOfWordsExtractor, self).__reset_db()
        col = get_collection(self.db_name, self.col_name)
        for item in col.find():
            try:
                item.pop(self.prefix + "tokens")
            except:
                pass
            try:
                item.pop("root")
            except:
                pass
            try:
                item.pop("prc0")
            except:
                pass
            try:
                item.pop("prc1")
            except:
                pass
            try:
                item.pop("prc2")
            except:
                pass
            try:
                item.pop("prc3")
            except:
                pass
            try:
                item.pop("pos")
            except:
                pass
            try:
                item.pop("lex")
            except:
                pass
            col.replace_one({"_id": item["_id"]}, item)
        client = SingletonClient()
        client.drop_database(self.prefix + "TF-IDF")
        client.drop_database(self.prefix + "Weights")
        client.drop_database(self.prefix + "Bag-Of-Words")

    def __extract_morphological_features(self):
        mfe = MorphologicalFeaturesExtractor(source=self.source,
                                             n_cores=self.cpu_count,
                                             field_name=self.prefix+"tokens")
        mfe.work()

    def __extract_bag_of_word(self):
        boe = BagOfWordsExtractor(self.source, field_name="lex", n_cores=self.cpu_count,
                                  target=(self.prefix+"Bag-Of-Words", self.ngram), n_gram=1)
        boe.work()

    def work(self):
        print("Start extracting tokens")
        self._simple_tokenize()
        print("start extract morphological features")
        self.__extract_morphological_features()
        print("start extract bag of words")
        self.__extract_bag_of_word()
        print("start create vector of counter")
        self._setup_features_names()
        print("start calculate tfidf")
        self._tfidf()
