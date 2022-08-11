from svuchatbot_mogodb.client import get_collection
col = get_collection("chatbot", "Sent-Mails-After-Parsing")
mails = list(col.find())
import pandas as pd

df= pd.DataFrame(mails)
print(df.shape)
df = df['replay-message']
print(df.shape)
df.drop_duplicates()
print(df.shape)
