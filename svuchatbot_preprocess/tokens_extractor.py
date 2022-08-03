from langdetect import detect
from nltk.tokenize import sent_tokenize, word_tokenize
from camel_tools.tokenizers.word import simple_word_tokenize
from svuchatbot_mogodb.client import get_collection
from svuchatbot_preprocess.extractor import Extractor


class TokensExtractor(Extractor):
    def __init__(self, source, field_name, n_cores, target= None):
        super().__init__(source, field_name, n_cores)
        if target is None:
            self.t_col_name = "tokens"
        else:
            self.t_col_name = target[1]

    @staticmethod
    def nltk_based_tokenize_for_sentence(sent):
        res = []
        for word in word_tokenize(sent):
            try:
                if detect(word) == 'ar':
                    res.append(word)
            except:
                pass
        return res

    @staticmethod
    def camle_based_tokenize_for_sentence(sent):
        res = []
        for word in simple_word_tokenize(sent):
            try:
                if detect(word) == 'ar':
                    res.append(word)
            except:
                pass
        return res

    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        for item in cursor:
            item.update({self.t_col_name: TokensExtractor.camle_based_tokenize_for_sentence(item[self.field_name])})
            cursor.collection.replace_one({"_id": item["_id"]}, item)