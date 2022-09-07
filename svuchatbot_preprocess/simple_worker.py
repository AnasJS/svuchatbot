from svuchatbot_mogodb.client import get_collection
from svuchatbot_preprocess.extractor import Extractor


class SimpleWorker(Extractor):
    def __init__(self, source, field_name, n_cores, do):
        super().__init__(source, field_name, n_cores)
        self.do = do

    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        for item in cursor:
            self.do(self.field_name, item, col)
