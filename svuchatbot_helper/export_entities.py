from svuchatbot_mogodb.client import get_collection
col = get_collection("chatbot", "Sent-Mails-After-Parsing")
mails = list(col.find())
import pandas as pd
df = pd.DataFrame(mails)
df1 = pd.DataFrame([{"word":i[0], "tag":i[1]} for e in df["entities"] for i in e])
df2 = df1.drop_duplicates(ignore_index=True)
df2.to_csv("entities.csv")

