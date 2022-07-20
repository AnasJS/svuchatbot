import camel_tools

# import the dediacritization tool
# from camel_tools.utils.dediac import dediac_ar
# print(dediac_ar("الحَمدُ للًَهِ" ))

from nltk.corpus import stopwords
from pprint import pprint
# from svuchatbot_preprocess.bag_of_word import camel_based_bag,nltk_based_bag
from nltk.corpus import stopwords
import arabicstopwords.arabicstopwords as stp

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client


def nltk_based_filter_stopwords_for_sentence(sent):
    return [w for w in sent if w not in stopwords.words('arabic')]


def arabic_stopwords_based_filter_stopwords_for_sentence(sent):
    arabic_stopwords = stp.stopwords_list()
    return [w for w in sent if w not in arabic_stopwords]


def remove_stop_words(from_col, to_col):
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db[from_col]
    documents = [d for d in col.find()]
    for item in documents:
        item["cleaned_tokens"] = arabic_stopwords_based_filter_stopwords_for_sentence(item["tokens"])
    db[to_col].insert_many(documents)
    return documents

#
# def nltk_based_filter_stopwords():
#     n_fdist = nltk_based_bag()
#     arabic_stopwords = stopwords.words('arabic')
#     return {k:v for k,v in n_fdist.items() if k not in arabic_stopwords}
#
#
# def arabic_stopwords_based_filter_stopwords():
#     n_fdist = camel_based_bag()
#     arabic_stopwords = stp.stopwords_list()
#     return {k:v for k,v in n_fdist.items() if k not in arabic_stopwords}


# nltk_based_filter_stopwords()
# import nltk
# pprint(arabic_stopwords_based_filter_stopwords().keys())
# nltk.download('stopwords')

