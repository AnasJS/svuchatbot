from pprint import pprint

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.ner import NERecognizer

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client
from svuchatbot_preprocess.bag_of_word import nltk_based_accumulate_clean_phrases
from svuchatbot_preprocess.morphology_analysis import camel_based_morphology_analysing
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
def extract_entities_for_sentence(sent):
    ner = NERecognizer.pretrained()
    labels = []

    for label in list(zip(sent, ner.predict_sentence(sent))):
        if not label[1].startswith('O'):
            labels.append(label)


    return labels


def extract_entities_from_emails():                                              
    sentences = nltk_based_accumulate_clean_phrases()
    #todo enhancment entities extraction based on morphological analyser
    # sentences = [camel_based_morphology_analysing(sent)[0]["stem"] for sent in sentences]
    entities = []
    for sent in sentences:
        labels = extract_entities_for_sentence(sent)
        entities.append({'Labels': labels})

    return entities
col = "mails_with_key_word"
db_client = get_client()
db_name = db_connection_params['db']
db = db_client[db_name]
collection = db[col]
documents = [d for d in collection.find()]
res = extract_entities_from_emails()
new_collection = [{**d, **r} for (d, r) in zip(documents, res)]
db["mails_with_key_word_and_entities"].insert_many(new_collection)