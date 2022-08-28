from svuchatbot_parsing.parse_pst import PSTParser

print("*********************************** start fetching mails *********************************")
# insert_emails_into_db("mails")
pstp = PSTParser("Sent Items", "Sent-Mails-After-Parsing-2", from_db="PST", to_db="chatbot")
pstp.parse()