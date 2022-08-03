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
#
# tokenizer = TokensExtractor(("chatbot", "Sent-Mails-After-Parsing"), "replay-message", cpu_count(),
#                             target=("chatbot", "tokenized-reply"))
# tokenizer.work()
#
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

from svuchatbot_features_managment.key_words_extractor import KeyWordExtractors

kwe = KeyWordExtractors(
    source=[
        ("Bag-Of-Words", "1_gram_bagOfWords_reply"),
        ("Most-Important-Tokens", "1_gram")],
    target=[
        ("TF-IDF", "1-Gram"),
        ("Count-Vectors", "1-Gram"),
        ("Weights", "1-Gram")
    ],
    min_weight=0.01,
    ngram="1-Gram")
kwe.work()
