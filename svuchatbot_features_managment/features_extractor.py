from svuchatbot_mogodb.client import get_collection
import pandas as pd
import numpy as np

from svuchatbot_preprocess.extractor import Extractor


class FeaturesExtractor(Extractor):
    def __init__(self, source, field_name, n_cores, target, min_freq):
        super().__init__(source, field_name, n_cores, based_on="columns", consecutive=True)
        self.s_db_name = self.db_name
        self.s_col_names = self.col_name
        self.min_freq = min_freq
        self.t_db_name = target[0]
        self.t_col_name = target[1]

    def _do(self, features):
        col = get_collection(self.s_db_name, self.col_name)
        cursor = col.find({}, features)
        bag_of_words_df = pd.DataFrame(list(cursor))[features]
        feature_names = bag_of_words_df.columns
        # bag_of_words_df = bag_of_words_df[feature_names]
        word_cnts = np.asarray(
            bag_of_words_df.sum(axis=0)).ravel().tolist()  # for each word in column, sum all row counts
        # print("word_cnts")
        # print(word_cnts)
        df_cnts = pd.DataFrame({'word': bag_of_words_df.columns, 'count': word_cnts})
        df_cnts = df_cnts.sort_values('count', ascending=False)
        most_frequent_tokens_df = df_cnts[df_cnts['count'] > self.min_freq]
        t_col = get_collection(self.t_db_name, self.t_col_name)
        res = [iloc.to_dict() for iloc in most_frequent_tokens_df.iloc]
        try:
            t_col.insert_many(res)
        except:
            print(res)




    # def most_frequent_tokens(self, min_freq):
    #     result = []
    #     for col_name in self.s_col_names:
    #         col = get_collection(self.s_db_name, col_name)
    #         cursor = col.find({})
    #         bag_of_words_df = pd.DataFrame(list(cursor))
    #         feature_names = bag_of_words_df.columns[1:]
    #         bag_of_words_df = bag_of_words_df[feature_names]
    #         result.append(bag_of_words_df)
    #     bag_of_all_words_df = pd.concat(result, axis=1)
    #     word_cnts = np.asarray(
    #         bag_of_all_words_df.sum(axis=0)).ravel().tolist()  # for each word in column, sum all row counts
    #     df_cnts = pd.DataFrame({'word': bag_of_all_words_df.columns, 'count': word_cnts})
    #     df_cnts = df_cnts.sort_values('count', ascending=False)
    #     return df_cnts[df_cnts["count"] > min_freq]

