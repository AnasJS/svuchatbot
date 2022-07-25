from langdetect import detect
from nltk.tokenize import sent_tokenize, word_tokenize
from camel_tools.tokenizers.word import simple_word_tokenize

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client


def nltk_based_tokenize_for_sentence(sent):
    res = []
    for word in word_tokenize(sent):
        try:
            if detect(word) == 'ar':
                res.append(word)
        except:
            pass
    return res


def camle_based_tokenize_for_sentence(sent):
    res = []
    for word in simple_word_tokenize(sent):
        try:
            if detect(word) == 'ar':
                res.append(word)
        except:
            pass

    return res


def tokenize(from_col, to_col, from_db="chatbot", to_db="chatbot", field_name="payload"):
    db_client = get_client()
    # db_name = db_connection_params['db']
    db_from = db_client[from_db]
    db_to = db_client[to_db]
    col = db_from[from_col]
    documents = [d for d in col.find()]
    for item in documents:
        item["tokens"] = camle_based_tokenize_for_sentence(item[field_name])
    db_to[to_col].insert_many(documents)
    return  documents
