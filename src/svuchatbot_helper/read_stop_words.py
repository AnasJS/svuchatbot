from os import curdir, getcwd, pardir
from os.path import join,dirname,abspath,basename
import numpy as np


def stopwords(path):
    # path = join(__package__, pardir,"assets", "our_stop_words_v2.txt")
    f = open(path)
    stop_words = f.readlines()
    stop_words = np.array([s.strip() for s in stop_words])
    return stop_words

# stopwords()
