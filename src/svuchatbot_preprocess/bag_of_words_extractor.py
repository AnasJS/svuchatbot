from src.svuchatbot_mogodb.client import get_collection
from src.svuchatbot_preprocess.extractor import Extractor
from multiprocessing import Manager
from collections import Counter
from copy import deepcopy
import multiprocessing as mp


class BagOfWordsExtractor(Extractor):
    def __init__(self, source, field_name, n_cores,  target=None, n_gram=1):
        super().__init__(source, field_name, n_cores)
        self.bag = Manager().list()
        self.bag_dict = Manager().dict()
        self.n_gram = n_gram
        if target is None:
            self.t_db_name = source[0]
            self.t_col_name = "bag_of_words"
        else:
            self.t_db_name= target[0]
            self.t_col_name = target[1]

    def __inject_words(self, item_id, words):
        self.bag += words
        self.bag_dict[item_id] = Counter(words)

    def do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}}, ["_id", self.field_name])
        if self.n_gram == 1:
            for item in cursor:
                words = item[self.field_name]
                # self.bag += words
                # self.bag_dict[item["_id"]] = Counter(words)
                self.__inject_words(item["_id"], words)
        elif self.n_gram > 1:
            for item in cursor:
                words = [" ".join([item[self.field_name][j] for j in range(i, i+self.n_gram)])
                         for i in range(len(item[self.field_name])-self.n_gram)]
                self.__inject_words(item["_id"], words)

    def _do_after(self, ids):
        col = get_collection(self.t_db_name, self.t_col_name)
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
        # for _, v in self.bag_dict.items():
        #     pprint(v)
        super().work(do=self._do_after)
