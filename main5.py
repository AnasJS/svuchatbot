from svuchatbot_clustering.kmeans_based_clustering import MyKmeans

k = MyKmeans(source=(("chatbot", "Mails-3"), ("Bag-Of-Words", "1-Gram")),
             field_name="replay-message")
k.fit()
k.to_yaml()