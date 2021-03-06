import nltk
import numpy

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client
from svuchatbot_repository.stemmers import snowball_stemmer


def get_intents_data(lang='arabic'):
    # pickle_name = "arabic_data.pickle"
    # stemmer
    # try:
    #     with open("arabic_data.pickle", "rb") as f:
    #         words, labels, training, output = pickle.load(f)
    # except:
    #     words = []
    #     labels = []
    #     docs_x = []
    #     docs_y = []
    #     for intent in data["intents"]:
    #         for pattern in intent["patterns"]:
    #             wrds = nltk.word_tokenize(pattern)
    #             words.extend(wrds)
    #             docs_x.append(wrds)
    #             docs_y.append(intent["tag"])
    #
    #         if intent["tag"] not in labels:
    #             labels.append(intent["tag"])
    #
    #     words = [stemmer.stem(w) for w in words if w != "?"]
    #     words = sorted(list(set(words)))
    #
    #     labels = sorted(labels)
    #
    #     training = []
    #     output = []
    #
    #     out_empty = [0 for _ in range(len(labels))]
    #
    #     for x, doc in enumerate(docs_x):
    #         bag = []
    #
    #         wrds = [stemmer.stem(w) for w in doc]
    #
    #         for w in words:
    #             if w in wrds:
    #                 bag.append(1)
    #             else:
    #                 bag.append(0)
    #
    #         output_row = out_empty[:]
    #         output_row[labels.index(docs_y[x])] = 1
    #
    #         training.append(bag)
    #         output.append(output_row)
    #
    #     training = numpy.array(training)
    #     output = numpy.array(output)
    #
    #     with open("data.pickle", "wb") as f:
    #         pickle.dump((words, labels, training, output), f)

    pass


def bag_of_words(s, words):
    # todo replace stemmer
    stemmer = snowball_stemmer()
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def bag_of_words_from_mails():
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db['analysed']
    mails = col.find({'payload'})