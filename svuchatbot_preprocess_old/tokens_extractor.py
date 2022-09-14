from langdetect import detect
from nltk.tokenize import word_tokenize
from camel_tools.tokenizers.word import simple_word_tokenize
from src.svuchatbot_mogodb import get_collection
from src.svuchatbot_preprocess import Extractor


class TokensExtractor(Extractor):
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
            item.update({"tokens": TokensExtractor.camle_based_tokenize_for_sentence(item[self.field_name])})
            cursor.collection.replace_one({"_id": item["_id"]}, item)
