from src.svuchatbot_mogodb.client import get_collection
from src.svuchatbot_preprocess.extractor import Extractor
import re


class SpecialWordsReplacement(Extractor):
    def __init__(self, source, field_name, n_cores, from_field_name,
                 from_field_pattern_index=1, from_field_replacement_index=0):
        super().__init__(source, field_name, n_cores)
        self.from_field_name = from_field_name
        self.from_field_pattern_index = from_field_pattern_index
        self.from_field_replacement_index = from_field_replacement_index

    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        filter = {
            "_id": {"$in": ids},
            self.from_field_name: {
                "$exists": 1,
                "$not": {"$size": 0}
            }
        }
        cursor = col.find(filter)
        for item in cursor:
            for special_word in item[self.from_field_name]:
                item[self.field_name] = re.sub(
                    special_word[self.from_field_pattern_index],
                    special_word[self.from_field_replacement_index],
                    item[self.field_name]
                )
            col.replace_one({"_id": item["_id"]}, item)

