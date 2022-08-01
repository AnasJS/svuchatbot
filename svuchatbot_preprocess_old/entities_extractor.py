from svuchatbot_preprocess.extractor import Extractor
from camel_tools.ner import NERecognizer


class EntitiesExtractor(Extractor):
    @staticmethod
    def extract_entities_for_sentence(sent, ner):
        return [(word, label) for word, label in zip(sent, ner.predict_sentence(sent)) if not label.startswith("O")]

    def _do(self, ids):
        documents = [d for d in self.col.find()]
        # print(len(documents))
        ner = NERecognizer.pretrained()
        cursor = self.col.find({"_id": {"$in": ids}})
        for item in cursor:
            item.update({"entities": EntitiesExtractor.extract_entities_for_sentence(item[self.field_name], ner)})
            cursor.collection.replace_one({"_id": item["_id"]}, item)
