from camel_tools.sentiment import SentimentAnalyzer

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client
from svuchatbot_preprocess.bag_of_word import nltk_based_accumulate_clean_phrases


def camel_based_sentiment_analyser_for_sentence(sent,sa):
    # print(sa.predict(sent))
    return sa.predict(sent)[0]


def camel_based_sentiment_analyser(from_col='mails' , to_col="mails_and_sentiments"):
    # items = nltk_based_accumulate_clean_phrases(from_col)
    # sentences = {message_id: " ".join(payload) for message_id,payload in sentences.items()}
    #todo enhancment entities extraction based on morphological analyser
    # sentences = [camel_based_morphology_analysing(sent)[0]["stem"] for sent in sentences]
    # sentiments = []
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    collection = db[from_col]
    documents = [d for d in collection.find()]
    sa = SentimentAnalyzer.pretrained()
    for item in documents:
        item["sentiments"] = camel_based_sentiment_analyser_for_sentence(item["payload"],sa)
        # sentiment = camel_based_sentiment_analyser_for_sentence(sent)
        # sentiments.append({'sentiments': sentiment})
    db[to_col].insert_many(documents)
    return documents

# col = "mails"
# db_client = get_client()
# db_name = db_connection_params['db']
# db = db_client[db_name]
# collection = db[col]
# documents = {d['Message-ID']:d for d in collection.find()}
# res = camel_based_sentiment_analyser(col="mails")
# # print(len(documents))
# new_collection = [{**d, **r} for (d, r) in zip(documents, res)]
# print(res)
# print(new_collection)
# db["mails_with_key_word_and_entities_and_sentiments"].insert_many(new_collection)



# print(camel_based_sentiment_analyser())