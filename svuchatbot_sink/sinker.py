from abc import ABC, abstractmethod
import pypff
import os
import time
from svuchatbot_preprocess.extractor import Extractor
from svuchatbot_mogodb.client import get_collection
from multiprocessing import Process


class Sinker(ABC):
    def __init__(self, f_path, db_name, n_cores):
        self.path = f_path
        self.db_name = db_name
        self.n_cores = n_cores

    def _range(self, order, length):
        r = int(length / self.n_cores)
        start = order * r
        if order == self.n_cores - 1:
            end = length
        else:
            end = start + r
        return start, end

    def _work(self):
        # folder = parent.get_sub_folder(folder_index)
        messages_count = self._length()
        processes = []
        for i in range(self.n_cores):
            s, e = self._range(i, messages_count)
            p = Process(target=self.__do, args=())
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

    @abstractmethod
    def _do(self, **args):
        pass

    @abstractmethod
    def _length(self):
        pass

    @abstractmethod
    def _do_args(self):
        return
