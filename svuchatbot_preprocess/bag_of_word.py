from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.probability import FreqDist
from collections import Counter
from langdetect import detect
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_alef_bw
from camel_tools.utils.normalize import normalize_alef_hsb

from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_alef_ar

from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import normalize_alef_maksura_ar
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_teh_marbuta_ar
from camel_tools.utils.normalize import normalize_unicode
from camel_tools.tokenizers.word import simple_word_tokenize
def nltk_based_bag():
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db['analysed']
    fdist = FreqDist()
    bag = []
    for d in col.find({},['payload']):
        for sent in sent_tokenize(d['payload']):
            for word in word_tokenize(sent):
                try:
                    if detect(word)=='ar':
                        bag.append(word)
                        fdist[word] += 1
                except:
                    print(word)

    # for word in bag:
    #     fdist[word]+=1


    print(len(fdist))
    return fdist


def camel_based_bag():
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db['analysed']
    bag = []
    for d in col.find({}, ['payload']):
        for t in simple_word_tokenize(d['payload']):
            try:
                if detect(t)=='ar':
                    bag.append(t)
            except:
                print(t)
    fdist = Counter(bag)
    print(len(fdist))
    # print(bag)
    return fdist
#
# fd1 = nltk_based_bag()
# fd2 = camel_based_bag()
#
# fd1l= set([k for k in fd1.keys()])
# fd2l = set([k for k in fd2.keys()])
# print(fd2l-fd1l)
#
