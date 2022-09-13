from src.svuchatbot_preprocess.extractor import Extractor
from camel_tools.utils.normalize import normalize_alef_ar, normalize_alef_maksura_ar, normalize_teh_marbuta_ar
from src.svuchatbot_mogodb.client import get_collection


class Normalizer(Extractor):
    def __init__(self, source, field_name, n_cores, word=False):
        super().__init__(source, field_name, n_cores)
        self.word = word

    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        if not self.word:
            for item in cursor:
                sent = normalize_teh_marbuta_ar(item[self.field_name])
                sent = normalize_alef_ar(sent)
                sent = normalize_alef_maksura_ar(sent)
                item.update({self.field_name: sent})
                cursor.collection.replace_one({"_id": item["_id"]}, item)
        else:
            for item in cursor:
                words = item[self.field_name]
                words = [normalize_teh_marbuta_ar(w) for w in words]
                words = [normalize_alef_ar(w) for w in words]
                words = [normalize_alef_maksura_ar(w) for w in words]
                item.update({self.field_name: words})
                cursor.collection.replace_one({"_id": item["_id"]}, item)