from svuchatbot_mogodb.client import get_collection
from datetime import datetime

col = get_collection("chatbot", "Mails-1")
for item in col.find():
        try:
            sent = item["From"].split("From: ")[1]
            item.update({"From": sent})
            col.replace_one({"_id": item["_id"]}, item)
        except:
            print(item["_id"])
