from svuchatbot_preprocess.filter import Filter
#
# f = Filter(source=("chatbot", "Sent-Mails-After-Parsing"),
#            target=("chatbot", "Mails"))
# f.exclude_emails_containing_word("replay-message", "الزملاء")
#
# f2 = Filter(source=("chatbot", "Mails"),
#            target=("chatbot", "Mails-1"))
# f2.exclude_emails_writen_in_foreign_language("replay-message")

# f = Filter(source=("chatbot", "Mails-1"),
#            target=("chatbot", "Mails-2"))
# f.exclude_emails_containing_word("replay-message", "الزميل")

f = Filter(source=("chatbot", "Mails-2"),
           target=("chatbot", "Mails-3"))
f.exclude_emails_containing_word("replay-message", "الزميلة")