from abc import ABC
from copy import copy, deepcopy
from camel_tools.sentiment import SentimentAnalyzer
from svuchatbot_preprocess.extractor import Extractor
from svuchatbot_mogodb.client import get_collection


class SentimentExtractor(Extractor):
    @staticmethod
    def camel_based_sentiment_analyser_for_sentence(sent, sa):
        # print(sa.predict(sent))
        return sa.predict(sent)[0]

    def _do(self, ids):
        # sa = copy(self.sa)
        sa = deepcopy(SentimentAnalyzer.pretrained())
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        # print(len(ids))
        # print(id(sa))
        for item in cursor:
            try:
                item.update({self.field_name+"_sentiments": SentimentExtractor.camel_based_sentiment_analyser_for_sentence(
                    item[self.field_name], sa)})
                cursor.collection.replace_one({"_id": item["_id"]}, item)
            except Exception as e:
                print("item : {} \n exception: {}".format(item, e))