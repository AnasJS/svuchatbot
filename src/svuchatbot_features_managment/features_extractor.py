from src.svuchatbot_preprocess.extractor import Extractor
from src.svuchatbot_mogodb.client import get_collection
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.database import MorphologyDB


class MorphologicalFeaturesExtractor(Extractor):
    @staticmethod
    def __analyze(tokens, analyser):
        res = analyser.analyze_words(tokens)

        assert len(res) == len(tokens), "not equal"

        result = []
        for r in res:

            if len(r.analyses):
                # print(r.analyses[0])
                result.append(r.analyses[0])
            else:
                result.append({
                "root": "",
                "lex":"",
                "prc0": "",
                "prc1": "",
                "prc2": "",
                "prc3": "",
                "pos":""
                })
        return {
            "root": [r["root"] for r in result],
            "lex": [r["lex"] for r in result],
            "prc0": [r["prc0"] for r in result],
            "prc1": [r["prc1"] for r in result],
            "prc2": [r["prc2"] for r in result],
            "prc3": [r["prc3"] for r in result],
            "pos" : [r["pos"] for r in result]
        }

    def _do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        db = MorphologyDB.builtin_db()
        analyzer = Analyzer(db)

        for item in cursor:
            result = MorphologicalFeaturesExtractor.__analyze(item[self.field_name], analyzer)
            for k, v in result.items():
                item.update({k: v})
            cursor.collection.replace_one({"_id": item["_id"]}, item)


