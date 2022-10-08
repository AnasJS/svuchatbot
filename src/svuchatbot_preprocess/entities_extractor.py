from src.svuchatbot_mogodb.client import get_collection
from src.svuchatbot_preprocess.extractor import Extractor
from camel_tools.ner import NERecognizer


class EntitiesExtractor(Extractor):
    @staticmethod
    def extract_entities_for_sentence(sent, ner):
        return [(word, label) for word, label in zip(sent, ner.predict_sentence(sent)) if not label.startswith("O")]

    def do(self, ids):
        # documents = [d for d in self.col.find()]
        # print(len(documents))
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        ner = NERecognizer.pretrained()
        # cursor = col.find({"_id": {"$in": ids}})
        if type(self.field_name) is list:
            for item in cursor:
                tmp = set([w for field in self.field_name for w in item[field]])
                item["entities"] = EntitiesExtractor.extract_entities_for_sentence(tmp, ner)
                cursor.collection.replace_one({"_id": item["_id"]}, item)
        else:
            for item in cursor:
                item["entities"] = EntitiesExtractor.extract_entities_for_sentence(item[self.field_name], ner)
                cursor.collection.replace_one({"_id": item["_id"]}, item)
