from src.svuchatbot_mogodb.client import get_collection
from src.svuchatbot_preprocess.extractor import Extractor


class SimpleWorker(Extractor):
    def __init__(self, source, field_name, n_cores, do, args=None, fltr={}):
        super().__init__(source, field_name, n_cores)
        self.doo = do
        self.filter = fltr
        if args:
            pass

    def do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}, **self.filter})
        for item in cursor:
            self.doo(self.field_name, item, col)
