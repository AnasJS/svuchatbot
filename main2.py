# from svuchatbot_mogodb import SingletonClient
# #
# #
# c = SingletonClient()
# # print(c.a)
# c2 = SingletonClient()
# # c2.a = 6
# # print(c.a)
import os
# from svuchatbot_preprocess.tokenizer import work
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

# from svuchatbot_preprocess.sentiment_extractor import SentimentExtractor
# se = SentimentExtractor(("chatbot", "cleaned_tokenized_mails"), "tokens", 8)
# se.work()

# from svuchatbot_sink.pst_sink import PST
# pst_sink = PST("/home/dell/works/svuchatbot/data/info@svuonline.org.pst", "PST1", 8)
# pst_sink.sink()

# from svuchatbot_preprocess.bag_of_words_extractor import BagOfWordsExtractor
# bow_replies = BagOfWordsExtractor(("chatbot", "cleaned_tokenized_mails"), field_name="replay-message")
# bow = BagOfWordsExtractor(("chatbot", "cleaned_tokenized_mails"), field_name="cleaned_tokens", n_cores=8, n_gram=2,
#                           target=("chatbot", "2_gram_bagOfWords"))
# bow.work()

# from svuchatbot_features_managment.key_words_extractor import KeyWordExtractors
#
# kwe = KeyWordExtractors(("chatbot", "cleaned_tokenized_mails"), field_name="body")
# kwe.work()
# **************************************************************************************************

# tokenizer = TokensExtractor(("chatbot", "Sent-Mails-After-Parsing"), "replay-message", cpu_count(),
#                             target=("chatbot", "tokenized-reply"))
# tokenizer.work()

# from svuchatbot_preprocess.bag_of_words_extractor import BagOfWordsExtractor
# bow_replies = BagOfWordsExtractor(("chatbot", "Sent-Mails-After-Parsing"), field_name="tokenized-reply", n_cores=8,
#                                   target=("Bag-Of-Words", "1_gram_bagOfWords_reply"))
# bow_replies2 = BagOfWordsExtractor(("chatbot", "Sent-Mails-After-Parsing"), field_name="tokenized-reply", n_cores=8, n_gram=2,
#                           target=("Bag-Of-Words", "2_gram_bagOfWords_reply"))
#
# bow_replies3 = BagOfWordsExtractor(("chatbot", "Sent-Mails-After-Parsing"), field_name="tokenized-reply", n_cores=8,
#                                    n_gram=3, target=("Bag-Of-Words", "3_gram_bagOfWords_reply"))
# bow_replies4 = BagOfWordsExtractor(("chatbot", "Sent-Mails-After-Parsing"), field_name="tokenized-reply", n_cores=8,
#                                    n_gram=4, target=("Bag-Of-Words", "4_gram_bagOfWords_reply"))
# bow_replies5 = BagOfWordsExtractor(("chatbot", "Sent-Mails-After-Parsing"), field_name="tokenized-reply", n_cores=8,
#                                    n_gram=5, target=("Bag-Of-Words", "5_gram_bagOfWords_reply"))
# bow_replies6 = BagOfWordsExtractor(("chatbot", "Sent-Mails-After-Parsing"), field_name="tokenized-reply", n_cores=8,
#                                    n_gram=6, target=("Bag-Of-Words", "6_gram_bagOfWords_reply"))
# bow_replies.work()
# bow_replies2.work()
# bow_replies3.work()
# bow_replies4.work()
# bow_replies5.work()
# bow_replies6.work()
# ***********************************************************************************************
# from svuchatbot_features_managment.features_extractor import FeaturesExtractor
# fe = FeaturesExtractor(source=("Bag-Of-Words", "1_gram_bagOfWords_reply"), n_cores=4, field_name="",
#                        target=("Most-Important-Tokens","1_gram"), min_freq=50 )
# fe.work()
# fe = FeaturesExtractor(source=("Bag-Of-Words", "2_gram_bagOfWords_reply"), n_cores=4, field_name="",
#                        target=("Most-Important-Tokens","2_gram"), min_freq=50 )
# fe.work()
# fe = FeaturesExtractor(source=("Bag-Of-Words", "3_gram_bagOfWords_reply"), n_cores=4, field_name="",
#                        target=("Most-Important-Tokens","3_gram"), min_freq=50 )
# fe.work()
# fe = FeaturesExtractor(source=("Bag-Of-Words", "4_gram_bagOfWords_reply"), n_cores=4, field_name="",
#                        target=("Most-Important-Tokens","4_gram"), min_freq=50 )
# fe.work()
# fe = FeaturesExtractor(source=("Bag-Of-Words", "5_gram_bagOfWords_reply"), n_cores=4, field_name="",
#                        target=("Most-Important-Tokens","5_gram"), min_freq=50 )
# fe.work()
# ***********************************************************************************************
# from svuchatbot_mogodb.client import get_collection, SingletonClient
# col = get_collection("chatbot", "Mails-1")
# for item in col.find():
#     # item["tokens"] = None
#     try:
#         item.pop("tokenized-reply")
#     except:
#         pass
#     try:
#         item.pop("tokens")
#     except:
#         pass
#     try:
#         item.pop("cleaned_tokens")
#     except:
#         pass
#     col.replace_one({"_id": item["_id"]}, item)
# client = SingletonClient()
# client.drop_database("TF-IDF")
# client.drop_database("Weights")
# client.drop_database("Bag-Of-Words")
# ***********************************************************************************************
from src.svuchatbot_features_managment import KeyWordExtractors

for i in range(1, 2):
    kwe = KeyWordExtractors(
        source=("chatbot", "Mails-3"),
        cpu_count=os.cpu_count(),
        field_name="replay-message",
        min_weight=0.01,
        ngram="{}-Gram".format(i),
        normalize=True,
        # prefix="simple"
    )
    kwe.work()
# rbbowe = RootBasedBagOfWordsExtractor(
#     source=("chatbot", "Mails-1"),
#     cpu_count=os.cpu_count(),
#     field_name="replay-message",
#     min_weight=0.01,
#     ngram="{}-Gram".format(1),
#     normalize=True,
#     prefix="simple1"
# )
# rbbowe.work()

# from svuchatbot_helper.weight_for_tokens import get_weights_tokens
# for i in range(1, 6):
#     get_weights_tokens(source=("TF-IDF", "{}-Gram".format(i)), n=i)

# # ***********************************************************************************************
# tokenizer = TokensExtractor(("chatbot", "Mails-1"), "replay-message", cpu_count())
# tokenizer.work()
#
# from svuchatbot_preprocess.cleand_tokens_extractor import Elector
# elect = Elector(("chatbot", "Mails-1"), "tokens", cpu_count())
# elect.work()
#
# from svuchatbot_preprocess.entities_extractor import EntitiesExtractor
# ee = EntitiesExtractor(source=("chatbot", "Sent-Mails-After-Parsing"),
#                        field_name="tokens",
#                        n_cores=cpu_count()
#                        )
# ee.work()
