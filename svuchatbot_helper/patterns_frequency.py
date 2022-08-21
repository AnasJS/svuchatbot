from svuchatbot_mogodb.client import get_collection
import pandas as pd


def get_pattern_freq(source):
    col = get_collection(source[0], source[1])

    # counter = pd.Series(items).value_counts()
    fields = ["pos_pattern", "lex_pattern", "root_pattern","token_pattern"]
    fields_req = {}
    for field in fields:
        items = [item[field] for item in col.find({}, {field: 1, "_id": 0})]
        fields_req[field] = pd.Series(items).value_counts().sort_values(axis=0, ascending=False)

    m_col = get_collection("chatbot", "Mails-3")
    t_col = get_collection("chatbot", "PatternsFrequency")
    for item in col.find():
        for field in fields:
            for k,v in fields_req[field].items():
                if k == item[field]:
                    item.update({field+"_frequency": v})
                    break
        _email = m_col.find_one({"_id": item["email_id"]}, {"replay-message":1, "body":1})
        item.update({"replay-message": _email["replay-message"]})
        item.update({"question-message": _email["body"]})
        t_col.insert_one(item)
    return fields_req
# get_freq(("Patterns", "1-Gram"), "pos_pattern")
# get_freq(("Patterns", "1-Gram"), "lex_pattern")
# get_freq(("Patterns", "1-Gram"), "root_pattern")

