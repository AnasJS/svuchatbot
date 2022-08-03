from abc import ABC, abstractmethod
from multiprocessing import Process
import time
from svuchatbot_mogodb.client import SingletonClient
from svuchatbot_mogodb.client import get_collection


class Extractor(ABC):
    def __init__(self, source, field_name, n_cores, based_on="rows", consecutive=False):
        self.consecutive = consecutive
        self.db_name = source[0]
        self.col_name = source[1]
        self.field_name = field_name
        self.n_cores = n_cores
        self.col = get_collection(self.db_name, self.col_name)
        self.based_on = based_on

    @abstractmethod
    def _do(self, ids):
        pass

    def _range(self, order, length):
        r = int(length / self.n_cores)
        start = order * r
        if order == self.n_cores - 1:
            end = length
        else:
            end = start + r
        return start, end

    @staticmethod
    def __ids(col):
        return [item["_id"] for item in col.find({}, ["_id"])]

    @staticmethod
    def __columns(col, columns):
        return list(col.find({}, columns))

    def __config_process(self, col, order, target):
        if self.based_on == "rows":
            ids = Extractor.__ids(col)
            s, e = self._range(order, len(ids))
            p = Process(target=target, args=(ids[s:e],))
        elif self.based_on == "columns":
            columns_name = list(col.find_one({}).keys())[1:]
            s, e = self._range(order, len(columns_name))
            # print(columns_name)
            # columns = Extractor.__columns(columns=columns_name[s:e])
            p = Process(target=target, args=(columns_name[s:e],))
        else:
            raise Exception("based on should be 'rows' or 'columns'")
        p.start()
        return p

    def __workflow(self, col, do):
        if not self.consecutive:
            processes = []
            for i in range(self.n_cores):
                p = self.__config_process(col, i, do)
                processes.append(p)
            for p in processes:
                p.join()
        else:
            for i in range(self.n_cores):
                p = self.__config_process(col, i, do)
                p.join()

    def work(self, do=None):
        startTime = time.time()
        client = SingletonClient()
        f_col = client[self.db_name][self.col_name]
        # n_cores = os.cpu_count()
        field = "body"
        if do is None:
            do = self._do
        self.__workflow(f_col, do)
        endTime = time.time()
        workTime = endTime - startTime
        print("The job took " + str(workTime) + " seconds to complete")



