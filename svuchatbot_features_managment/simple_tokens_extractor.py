from svuchatbot_preprocess.extractor import Extractor
from svuchatbot_mogodb.client import get_collection
from svuchatbot_preprocess.tokens_extractor import TokensExtractor


class SimpleTokensExtractor(TokensExtractor):
    def _tokenizer(self):
        return TokensExtractor.camel_simple_based_tokenize_for_sentence
    # def _do(self, ids):
    #     col = get_collection(self.db_name, self.col_name)
    #     cursor = col.find({"_id": {"$in": ids}})
    #     tokenizer = TokensExtractor.camel_simple_based_tokenize_for_sentence
    #     for item in cursor:
    #         tokens = tokenizer(item[self.field_name])
    #         item.update({self.t_col_name: tokens})
    #         cursor.collection.replace_one({"_id": item["_id"]}, item)
