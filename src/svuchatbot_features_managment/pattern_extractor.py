from src.svuchatbot_helper.weight_for_tokens import get_weights_tokens
from src.svuchatbot_preprocess.extractor import Extractor
from src.svuchatbot_mogodb.client import get_collection, SingletonClient
import numpy as np


class PatternExtractor(Extractor):
    def __init__(self, source, field_name, n_cores, target, threshold=0.5, n_gram=3, prefix=None):
        super().__init__(source, field_name, n_cores)
        self.t_db_name, self.t_col_name = target
        self.n_gram = n_gram
        self.threshold = threshold
        if prefix:
            self.prefix = prefix + "-"
        else:
            self.prefix = ""
        df_important_words = get_weights_tokens((self.prefix+"TF-IDF", "1-Gram"), 1)
        df_important_words = df_important_words[df_important_words["max weight"] > threshold]
        self.important_words = df_important_words["word"].values

        self._reset_db()

    def _reset_db(self):
        # col = get_collection(self.t_db_name, self.t_col_name)
        # for item in col.find():
        #     try:
        #         item.pop(self.prefix+"root_pattern")
        #     except:
        #         pass
        #     try:
        #         item.pop(self.prefix+"lex_pattern")
        #     except:
        #         pass
        #     try:
        #         item.pop(self.prefix+"token_pattern")
        #     except:
        #         pass
        #     try:
        #         item.pop(self.prefix+"pos_pattern")
        #     except:
        #         pass
        #     col.replace_one({"_id": item["_id"]}, item)
        client = SingletonClient()
        client.drop_database(self.t_db_name)
        print("finish clean")

    def __get_indexes(self, order, max_length):
        if order in range(max_length) and self.n_gram + 1 < max_length:
            prefix = [i for i in range(order - self.n_gram, order) if i > -1]
            suffix = [i for i in range(order + 1, order + self.n_gram + 1) if i < max_length]
            indexes = prefix + [order] + suffix
            return indexes[0], indexes[-1] + 1
        else:

            return 0,max_length

    def do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        t_col = get_collection(self.t_db_name, self.t_col_name)
        cursor = col.find({"_id": {"$in": ids}})
        for item in cursor:
            token_arr = np.array(item[self.field_name])
            important_tokens = np.intersect1d(self.important_words, token_arr)
            important_tokens_indexes = {token: np.where(np.array(item[self.field_name]) == token)
                                        for token in important_tokens}
            if important_tokens_indexes == {}:
                print(str(item["_id"])+" : doesnt have important token")
                print(token_arr)
            for token, indexes in important_tokens_indexes.items():
                for index in indexes[0]:
                    res = self.__get_indexes(index, len(item[self.field_name]))
                    if res:
                        s, e = res
                        t_col.insert_one({
                            "token": token,
                            "root_pattern": item["root"][s:e],
                            "pos_pattern": item["pos"][s:e],
                            "lex_pattern": item["lex"][s:e],
                            "token_pattern": item[self.field_name][s:e],
                            "email_id": item["_id"]})
                    else:
                        print("there is an error")
