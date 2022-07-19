from langdetect import detect
from nltk.tokenize import sent_tokenize, word_tokenize
from camel_tools.tokenizers.word import simple_word_tokenize


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
