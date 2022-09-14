from src.svuchatbot_mogodb.client import get_collection

col = get_collection("chatbot", "Mails-1")
for item in col.find():
        try:
            sent = item["To"].split("To: ")[1]
            item.update({"To": sent})
            col.replace_one({"_id": item["_id"]}, item)
        except:
            print(item["_id"])
