from src.svuchatbot_const.db.definitions import Definitions
from src.svuchatbot_mogodb.client import get_collection
import pandas as pd
col = get_collection(Definitions.PARSSEDEMAILSDBNAME, Definitions.PARSSEDEMAILSCOLLECTIONNAME)
res = []
for item in col.find({"questions":{"$ne":[]}}):

    for q in item["questions"]:
        res.append({
            "id": item["_id"],
            "intent": item["tag"],
            "answer": item["replay-message"],
            "question": q,
            "email": item["body"]

        })
# df = pd.DataFrame(res, columns=["id", "intent", "answer", "question", "email"])
df = pd.DataFrame(res)
df.to_csv("q&a.csv")

res=[]
for item in col.find({"questions": []}):
    res.append({
        "id": item["_id"],
        "intent": item["tag"],
        "answer": item["replay-message"],
        "question": "",
        "email": item["body"]

    })
# df = pd.DataFrame(res, columns=["id", "intent", "answer", "question", "email"])
df = pd.DataFrame(res)
df.to_csv("empty_q&a.csv")
