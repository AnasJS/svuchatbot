from src.svuchatbot_parsing.parse_pst import PSTParser

print("*********************************** start fetching mails *********************************")
# insert_emails_into_db("mails")
pstp = PSTParser("Sent Items", "Sent-Mails-After-Parsing-7", from_db="PST", to_db="chatbot")
pstp.parse()