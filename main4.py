# from svuchatbot_features_managment.features_extractor import FeaturesExtractor
# from svuchatbot_features_managment.simple_tokens_extractor import SimpleTokensExtractor
# from os import cpu_count
# ste = SimpleTokensExtractor(source=("chatbot", "Mails-1"),
#                             target=("", "simple-tokens"),
#                             field_name="replay-message",
#                             n_cores=cpu_count())
# ste.work()
# pose = FeaturesExtractor(source=("chatbot", "Mails-1"),
#                     field_name="simple-tokens",
#                     n_cores=cpu_count()
#                     )
# pose.work()
# ***************************************************************************************
# from os import cpu_count
# from svuchatbot_features_managment.root_based_bag_of_words_extractor import RootBasedBagOfWordsExtractor
# rbbowe = RootBasedBagOfWordsExtractor(
#     source=("chatbot", "Mails-1"),
#     field_name="replay-message",
#     cpu_count=cpu_count(),
#     prefix="simple3",
#     min_weight=0.5
# )
# rbbowe.work()
#
# from svuchatbot_helper.weight_for_tokens import get_weights_tokens
# get_weights_tokens(source=("simple3-TF-IDF", "1-Gram"), n=1)
# ******************************************************************************************
from os import cpu_count
from svuchatbot_features_managment.pattern_extractor import PatternExtractor
pe = PatternExtractor(source=("chatbot", "Mails-1"),
                      target=("Patterns", "1-Gram"),
                      threshold=0.5,
                      n_gram=3,
                      n_cores=cpu_count(),
                      field_name="simple3-tokens")
pe.work()
