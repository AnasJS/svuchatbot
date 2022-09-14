from src.svuchatbot_preprocess.extractor import Extractor
from src.svuchatbot_mogodb.client import get_collection
from nltk.corpus import stopwords
import arabicstopwords.arabicstopwords as stp


class Elector(Extractor):
    @staticmethod
    def nltk_based_filter_stopwords_for_sentence(sent):
        return [w for w in sent if w not in stopwords.words('arabic')]

    @staticmethod
    def arabic_stopwords_based_filter_stopwords_for_sentence(sent):
        arabic_stopwords = stp.stopwords_list()
        return [w for w in sent if w not in arabic_stopwords]

    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        for item in cursor:
            item.update({"cleaned_tokens": Elector.arabic_stopwords_based_filter_stopwords_for_sentence(item[self.field_name])})
            cursor.collection.replace_one({"_id": item["_id"]}, item)
