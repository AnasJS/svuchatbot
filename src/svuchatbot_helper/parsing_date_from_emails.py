from src.svuchatbot_mogodb.client import get_collection
from datetime import datetime

col = get_collection("chatbot", "Mails-1")
for item in col.find():
    if type(item["Sent"]) == str:
        try:
            sent = item["Sent"].split("Sent: ")[1]
            # print(sent)
            dt = datetime.strptime(sent, '%A, %B %d, %Y %I:%M %p')
            # print(dt)
            item.update({"Sent": dt})
            col.replace_one({"_id": item["_id"]}, item)
        except:
            print(item["_id"])
    #
# mails = list()
# import pandas as pd
# df = pd.DataFrame(mails)
# df1 = pd.DataFrame([{"word":i[0], "tag":i[1]} for e in df["entities"] for i in e])
# df2 = df1.drop_duplicates(ignore_index=True)
# df2.to_csv("entities.csv")
