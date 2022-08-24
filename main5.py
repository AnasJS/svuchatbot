import os

# from svuchatbot_clustering.kmeans_based_clustering import MyKmeans
from svuchatbot_clustering.kmeans_based_clustering import MyKmeans
from svuchatbot_features_managment.key_words_extractor import KeyWordExtractors, Definitions
#
# for i in range(1, 6):
#     kwe = KeyWordExtractors(
#         source=("chatbot", "Mails-3"),
#         cpu_count=os.cpu_count(),
#         field_name="replay-message",
#         min_weight=0.01,
#         ngram="{}-Gram".format(i),
#         normalize=True,
#         # prefix="simple",
#         reset_db=(i == 1)
#     )
#     if i == 1:
#         kwe.set_pipe([
#             Definitions.SIMPLETOKENIZATION,
#             Definitions.STOPWORDSREMOVING,
#             Definitions.MORPHOLOGICALTOKENIZATION,
#             Definitions.STOPWORDSREMOVING,
#             Definitions.NORMALIZATION,
#             Definitions.STOPWORDSREMOVING,
#             Definitions.BAGOFWORDSEXTRACION
#         ])
#     else:
#         kwe.set_pipe([
#             Definitions.BAGOFWORDSEXTRACION
#         ])
#     kwe.work()

k = MyKmeans(source=(("chatbot", "Mails-3"), ("Bag-Of-Words", "1-Gram")),
             field_name="replay-message",
             n_clusters=30,
             utter_file_name="results/kmeans_with_pca_5_gram/utter.yml",
             intent_file_name="results/kmeans_with_pca_5_gram/intent.yml",
             n_gram=5)
k.fetch()
# k.standardization()
k.calculate_pca()
k.kmeans_with_pca_fit()
# k.fit()
k.to_yaml()
