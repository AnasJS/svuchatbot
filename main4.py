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

from src.svuchatbot_clustering.simple import add_tag
from src.svuchatbot_features_managment import PatternExtractor
from src.svuchatbot_generator.intentions_generator import IntentionsGenerator
from src.svuchatbot_helper import get_pattern_freq

pe = PatternExtractor(source=("chatbot", "Mails-3"),
                      target=("Patterns", "1-Gram"),
                      threshold=0.3,
                      n_gram=3,
                      n_cores=cpu_count(),
                      field_name="simple-tokens")
pe.work()
from src.svuchatbot_mogodb import get_collection
col = get_collection("Patterns", "1-Gram")
emails_ids = set([item["email_id"] for item in col.find({},{"email_id":1,"_id":0})])
col = get_collection("chatbot","Mails-3")
ids = set([item["_id"] for item in col.find({},{"_id":1})])
message = f'There is an error in PatternExtractor,{len(emails_ids)}!={len(ids)}'
assert len(emails_ids)==len(ids), message
freq = get_pattern_freq(("Patterns", "1-Gram"))
col = get_collection("chatbot", "PatternsFrequency")
emails_ids = set([item["email_id"] for item in col.find({},{"email_id":1,"_id":0})])
# print(len(freq))
assert len(emails_ids)==len(ids), "There is an error in get_pattern_freq"
add_tag()


ig = IntentionsGenerator(("chatbot","Mails-3"))
ig.work()
