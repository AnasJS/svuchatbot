from svuchatbot_preprocess.extractor import Extractor
from svuchatbot_mogodb.client import get_collection
from nltk.corpus import stopwords
import arabicstopwords.arabicstopwords as stp
from svuchatbot_helper.read_stop_words import stopwords as o_stopwords
import numpy as np
from os import pardir
from os.path import join


class Elector(Extractor):
    @staticmethod
    def nltk_based_filter_stopwords_for_sentence(sent):
        return [w for w in sent if w not in stopwords.words('arabic')]

    @staticmethod
    def arabic_stopwords_based_filter_stopwords_for_sentence(sent):
        arabic_stopwords = stp.stopwords_list()
        return [w for w in sent if w not in arabic_stopwords]

    @staticmethod
    def filter_stopwords_for_sentence(sent, ostp):
        return [w for w in sent if w not in ostp]

    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        path1 = join(__package__, pardir, "assets", "our_stop_words_v2.txt")
        path2 = join(__package__, pardir, "assets", "useless_words.txt")

        ostp = np.append(o_stopwords(path1), o_stopwords(path2))

        for item in cursor:
            cleaned_tokens = Elector.filter_stopwords_for_sentence(item[self.field_name], ostp)
            # cleaned_tokens = Elector.arabic_stopwords_based_filter_stopwords_for_sentence(item[self.field_name])
            item.update({"tokens": cleaned_tokens})
            cursor.collection.replace_one({"_id": item["_id"]}, item)
