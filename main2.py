# from svuchatbot_mogodb import SingletonClient
# #
# #
# c = SingletonClient()
# # print(c.a)
# c2 = SingletonClient()
# # c2.a = 6
# # print(c.a)
from os import cpu_count
# from svuchatbot_preprocess.tokenizer import work
from svuchatbot_preprocess.tokens_extractor import TokensExtractor
# from svuchatbot_preprocess.tokenizer import Tokenizer
# from_col="Sent-Mails-After-Parsing",to_col="tokenized_mails", from_db="chatbot", to_db="chatbot", field_name="body"
# t = Tokenizer(("chatbot", "Sent-Mails-After-Parsing"), ("chatbot","tokenized_mails_1"), field="body")
# work(("chatbot", "Sent-Mails-After-Parsing"), ("chatbot","tokenized_mails_1"))

# tokenizer = TokensExtractor(("chatbot", "Sent-Mails-After-Parsing"), "body", cpu_count())
# tokenizer.work()
#
# from svuchatbot_preprocess.clead_tokens_extractor import Elector
# elect = Elector(("chatbot", "Sent-Mails-After-Parsing"), "tokens", cpu_count())
# elect.work()


from svuchatbot_sink.pst_sink import PST
pst_sink = PST("/home/dell/works/svuchatbot/data/info@svuonline.org.pst", "PST1", 8)
pst_sink.sink()


