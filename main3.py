from src.svuchatbot_preprocess import Filter
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

# f = Filter(source=("chatbot", "Mails-2"),
#            target=("chatbot", "Mails-3"))
# f.exclude_emails_containing_word("replay-message", "الزميلة")

f = Filter(source=("chatbot", "Mails-3"),
           target=("chatbot", "Mails-4"))
f.exclude_emails_containing_word("replay-message", "؟").\
      exclude_emails_containing_word("body", "كورونا").\
      exclude_emails_containing_word("replay-message", "كورونا").\
      exclude_emails_containing_word("replay-message", "يرجى الاطلاع وشكرا").\
      finding_incomprehensible_words()
