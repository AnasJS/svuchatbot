import time

from svuchatbot_mogodb import SingletonClient
from svuchatbot_mogodb.client import get_collection
from svuchatbot_preprocess.extractor import Extractor
from multiprocessing import Manager, Process
from collections import Counter
from copy import copy, deepcopy
from pprint import pprint

class BagOfWordsExtractor(Extractor):
    def __init__(self, source, field_name, n_cores):
        super().__init__(source, field_name, n_cores)
        self.bag = Manager().list()
        self.bag_dict = Manager().dict()

    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}}, ["_id",self.field_name])
        for item in cursor:
            self.bag += item[self.field_name]
            self.bag_dict[item["_id"]] = Counter(item[self.field_name])

    def _do_after(self, ids):
        col = get_collection(self.db_name, "bag_of_words")
        bag_dict = deepcopy(self.bag_dict)
        bag = deepcopy(self.bag)
        for item_id in ids:
            item_bag = bag_dict[item_id]
            temp = {k: 0 for k in bag}
            temp["_id"] = item_id
            temp = {**temp, **item_bag}
            col.insert_one(temp)

    def work(self, do=None):
        super().work()
        super().work(do=self._do_after)





