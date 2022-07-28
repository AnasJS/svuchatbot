from abc import ABC, abstractmethod
from multiprocessing import Process
import time
from svuchatbot_mogodb.client import SingletonClient


class Extractor(ABC):
    def __init__(self, source, field_name, n_cores):
        self.db_name = source[0]
        self.col_name = source[1]
        self.field_name = field_name
        self.n_cores = n_cores

    @abstractmethod
    def _do(self, ids):
        pass

    def __range(self, order, length):
        r = int(length / self.n_cores)
        start = order * r
        if order == self.n_cores - 1:
            end = length
        else:
            end = start + r
        return start, end

    def work(self):
        startTime = time.time()
        client = SingletonClient()
        f_col = client[self.db_name][self.col_name]
        # n_cores = os.cpu_count()
        field = "body"
        processes = []
        ids = [item["_id"] for item in f_col.find({}, ["_id"])]
        for i in range(self.n_cores):
            s, e = self.__range(i, f_col.count_documents({}))
            p = Process(target=self._do, args=(ids[s:e],))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        endTime = time.time()
        workTime = endTime - startTime
        print("The job took " + str(workTime) + " seconds to complete")
