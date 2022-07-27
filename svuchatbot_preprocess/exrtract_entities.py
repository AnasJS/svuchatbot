from pprint import pprint
import pandas as pd

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.ner import NERecognizer

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client
from svuchatbot_preprocess.bag_of_word import nltk_based_accumulate_clean_phrases
from svuchatbot_preprocess.morphology_analysis import camel_based_morphology_analysing
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer


def extract_entities_for_sentence(sent, ner):
    return [(word,label) for word,label in zip(sent,ner.predict_sentence(sent)) if not label.startswith("O") ]


def extract_entities(from_col="mails",to_col="entities", from_db="chatbot", to_db="chatbot"):
    db_client = get_client()
    # db_name = db_connection_params['db']
    db_from = db_client[from_db]
    db_to = db_client[to_db]
    col = db_from[from_col]
    documents = [d for d in col.find()]
    # print(len(documents))
    ner = NERecognizer.pretrained()
    for item in documents:

        item["entities"] = extract_entities_for_sentence(item["cleaned_tokens"], ner)
        # print(item["entities"])
    # print("///////////////////////////end///////////////////////////////")
    db_to[to_col].insert_many(documents)
    return documents


def extract_entities_from_emails(from_col="mails", to_col="mails_with_extracted_entities"):
    items = nltk_based_accumulate_clean_phrases(from_col)
    #todo enhancment entities extraction based on morphological analyser
    # sentences = [camel_based_morphology_analysing(sent)[0]["stem"] for sent in sentences]
    entities = []
    for item in items:
        item['labels']  = extract_entities_for_sentence(item['payload'])
    return items
# # col = "mails_with_key_word"
# # db_client = get_client()
# # db_name = db_connection_params['db']
# # db = db_client[db_name]
# # collection = db[col]
# # documents = [d for d in collection.find()]
# res = extract_entities_from_emails(col = "mails")
# df = pd.DataFrame(res)
# print(df)
# # new_collection = [{**d, **r} for (d, r) in zip(documents, res)]
# # db["mails_with_key_word_and_entities"].insert_many(new_collection)