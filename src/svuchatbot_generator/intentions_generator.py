from src.svuchatbot_mogodb.client import get_collection


class IntentionsGenerator:
    def __init__(self, source):
        self.source = source
        self.tags_intentions={}
        self.tags_utter = {}

    def work(self):
        col = get_collection(self.source[0], self.source[1])
        documents = list(col.find())
        for item in documents:
            intentions = self.tags_intentions.get(str(tuple(item["tag"])), [])
            intentions.append(item["body"])
            self.tags_intentions[str(tuple(item["tag"]))] = intentions
            utters = self.tags_utter.get(str(tuple(item["tag"])), [])
            utters.append(item["replay-message"])
            self.tags_utter[str(tuple(item["tag"]))] = utters
        # df_intent = pd.DataFrame(self.tags_intentions)
        # df_intent.to_json("intent.json")
        # json.dump(self.tags_intentions, open("intent.json","wt"))
        # json.dump(self.tags_intentions, open("utter.json","wt"))
        # print(json.dumps(self.tags_intentions ))
        # print(json.dumps(self.tags_intentions))
        # df_utter = pd.DataFrame(self.tags_intentions)
        # df_utter.to_json("utter.json")
        import yaml
        import os
        if os.path.exists("intent.yml"):
            os.remove("intent.yml")
        if os.path.exists("utter.yml"):
            os.remove("utter.yml")
        yaml.dump(self.tags_intentions, open("intent.yml","wt"),  allow_unicode=True)
        yaml.dump(self.tags_utter, open("utter.yml", "wt"),  allow_unicode=True)
