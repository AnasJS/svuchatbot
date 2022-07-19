from camel_tools.sentiment import SentimentAnalyzer

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client
from svuchatbot_preprocess.bag_of_word import nltk_based_accumulate_clean_phrases


def camel_based_sentiment_analyser_for_sentence(sent):
    sa = SentimentAnalyzer.pretrained()
    # print(sa.predict(sent))
    return sa.predict(sent)[0]


def camel_based_sentiment_analyser():
    sentences = nltk_based_accumulate_clean_phrases()
    sentences = [" ".join(sent) for sent in sentences]
    #todo enhancment entities extraction based on morphological analyser
    # sentences = [camel_based_morphology_analysing(sent)[0]["stem"] for sent in sentences]
    sentiments = []
    for sent in sentences:
        sentiment = camel_based_sentiment_analyser_for_sentence(sent)
        sentiments.append({'sentiments': sentiment})

col = "mails_with_key_word_and_entities"
db_client = get_client()
db_name = db_connection_params['db']
db = db_client[db_name]
collection = db[col]
documents = [d for d in collection.find()]
res = camel_based_sentiment_analyser()
new_collection = [{**d, **r} for (d, r) in zip(documents, res)]
db["mails_with_key_word_and_entities_and_sentiments"].insert_many(new_collection)



# print(camel_based_sentiment_analyser())