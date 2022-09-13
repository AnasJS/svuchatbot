from src.svuchatbot_config import db_connection_params
from src.svuchatbot_mogodb import SingletonClient
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from collections import Counter
from langdetect import detect
from src.svuchatbot_preprocess.tokens_extractor import TokensExtractor
# from src.svuchatbot_preprocess import nltk_based_filter_stopwords_for_sentence
from camel_tools.tokenizers.word import simple_word_tokenize


def nltk_based_bag():
    db_client = SingletonClient()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db['mails']
    fdist = FreqDist()
    bag = []
    for d in col.find({}, ['payload']):
        for sent in sent_tokenize(d['payload']):
            for word in word_tokenize(sent):
                try:
                    if detect(word) == 'ar':
                        bag.append(word)
                        fdist[word] += 1
                except:
                    # print(word)
                    pass

    # for word in bag:
    #     fdist[word]+=1

    print(len(fdist))
    return fdist


def camel_based_bag():
    db_client = SingletonClient()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db['mails']
    bag = []
    for d in col.find({}, ['payload']):
        for t in simple_word_tokenize(d['payload']):
            try:
                if detect(t) == 'ar':
                    bag.append(t)
            except:
                # print(t)
                pass
    fdist = Counter(bag)
    print(len(fdist))
    # print(bag)
    return fdist


def nltk_based_accumulation_words():
    return " ".join(list(nltk_based_bag().keys()))


def camel_based_accumulation_words():
    return " ".join(list(camel_based_bag().keys()))


def accumulate_phrases(col="analysed"):
    db_client = SingletonClient()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db[col]
    # return {d['Message-ID']: d['payload'] for d in col.find({}, ['Message-ID', 'payload'])}
    return [item for item in col.find({}, ['Message-ID', 'payload'])]


def nltk_based_accumulate_clean_phrases(col="analysed"):
    sents = accumulate_phrases(col=col)
    tokenised_sentences = sents.copy()
    for item in tokenised_sentences:
        item["tokens"]= TokensExtractor.nltk_based_tokenize_for_sentence(item["payload"])
        item["cleaned_tokens"]=TokensExtractor.nltk_based_filter_stopwords_for_sentence(item["tokens"])
        # {message_id:nltk_based_tokenize_for_sentence(payload) for message_id,payload in sents.items()}
        # cleand_tokenized_sentences = {message_id: nltk_based_filter_stopwords_for_sentence(tokens) for message_id,tokens in tokenised_sentences.items()}
    return tokenised_sentences
#
# fd1 = nltk_based_bag()
# fd2 = camel_based_bag()
#
# fd1l= set([k for k in fd1.keys()])
# fd2l = set([k for k in fd2.keys()])
# print(fd2l-fd1l)
#

#
# print(nltk_based_accumulation_mails())
# print(camel_based_accumulation_mails())
# res = nltk_based_accumulate_clean_phrases()
# pprint(res)
# print(len(res))
