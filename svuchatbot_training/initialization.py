import numpy

from src.svuchatbot_preprocess import read_intents
from src.svuchatbot_preprocess import stem_conllection


def init_intents():
    words, labels, docs_x, docs_y, stemmer = stem_conllection(read_intents())
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    return training, output, words, labels
