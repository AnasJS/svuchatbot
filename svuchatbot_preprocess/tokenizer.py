from langdetect import detect
from nltk.tokenize import sent_tokenize, word_tokenize
from camel_tools.tokenizers.word import simple_word_tokenize
from multiprocessing import Pool, Manager, Process, Queue
import time
import os
from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import SingletonClient, get_collection
from svuchatbot_preprocess.extractor import Extractor


def nltk_based_tokenize_for_sentence(sent):
    res = []
    for word in word_tokenize(sent):
        try:
            if detect(word) == 'ar':
                res.append(word)
        except:
            pass
    return res


def camle_based_tokenize_for_sentence(sent):
    res = []
    for word in simple_word_tokenize(sent):
        try:
            if detect(word) == 'ar':
                res.append(word)
        except:
            pass

    return res


def tokenize(from_col, to_col, from_db="chatbot", to_db="chatbot", field_name="payload"):
    db_client = SingletonClient()
    # db_name = db_connection_params['db']
    db_from = db_client[from_db]
    db_to = db_client[to_db]
    col = db_from[from_col]
    documents = [d for d in col.find()]
    for item in documents:
        item["tokens"] = camle_based_tokenize_for_sentence(item[field_name])
    db_to[to_col].insert_many(documents)
    return documents


#
# class Tokenizer:
#     def __init__(self, source, target, field="payload", n_cores=4):
#         self.client = SingletonClient()
#         self.f_col = self.client[source[0]][source[1]]
#         self.t_col = self.client[target[0]][target[1]]
#         self.field = field
#         self.manager = Manager()
#         self.n_cores = n_cores
#
#     def __fetch(self):
#         self.documents = self.manager.list([d for d in self.f_col.find()])
#
#     def __do(self, order):
#         r = int(len(self.documents) / self.n_cores)
#         start = order*r
#         if order == self.n_cores-1:
#             end = len(self.documents)
#         else:
#             end = start + r -1
#         for i in range(start, end):
#             self.documents[i]["tokens"] = camle_based_tokenize_for_sentence(self.documents[i][self.field])
#
#     def work(self):
#         self.__fetch()
#         pool = Pool(processes=self.n_cores)
#         pool.map(self.__do, (0, 1, 2, 3))


# def do(documents, n_process, order, field, q):
#     r = int(len(documents) / n_process)
#     start = order * r
#     if order == n_process - 1:
#         end = len(documents)
#     else:
#         end = start + r
#     print("order: ", order, "start", start, "end", end)
#     docs = list(documents[start:end])
#     for item in docs:
#         # print(type(item))
#         # print(item)
#         item["tokens"] = camle_based_tokenize_for_sentence(item[field])
#         # print(item["tokens"])
#     q.put(docs)

# def fetch(self, manager, f_col):
#     documents = manager.list([d for d in f_col.find()])
#     return documents

# class Tokenizer:
#     def __init__(self, source, field_name, n_cores):
#         self.db_name = source[0]
#         self.col_name = source[1]
#         self.field_name = field_name
#         self.n_cores = n_cores
#
#     def _do(self, ids):
#         col = get_collection(self.db_name, self.col_name)
#         cursor = col.find({"_id": {"$in": ids}})
#         for item in cursor:
#             item.update({"tokens": camle_based_tokenize_for_sentence(item[self.field_name])})
#             cursor.collection.replace_one({"_id": item["_id"]}, item)
#
#     def __range(self, order, length):
#         r = int(length / self.n_cores)
#         start = order * r
#         if order == self.n_cores - 1:
#             end = length
#         else:
#             end = start + r
#         return start, end
#
#     def work(self):
#         startTime = time.time()
#         client = SingletonClient()
#         f_col = client[self.db_name][self.col_name]
#         # n_cores = os.cpu_count()
#         field = "body"
#         processes = []
#         ids = [item["_id"] for item in f_col.find({}, ["_id"])]
#         for i in range(self.n_cores):
#             s, e = self.__range(i, f_col.count_documents({}))
#             p = Process(target=self._do, args=(ids[s:e],))
#             p.start()
#             processes.append(p)
#         for p in processes:
#             p.join()
#         endTime = time.time()
#         workTime = endTime - startTime
#         print("The job took " + str(workTime) + " seconds to complete")


class Tokenizer(Extractor):
    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        for item in cursor:
            item.update({"tokens": camle_based_tokenize_for_sentence(item[self.field_name])})
            cursor.collection.replace_one({"_id": item["_id"]}, item)
