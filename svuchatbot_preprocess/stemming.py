from svuchatbot_repository.stemmers import snowball_stemmer
import nltk


def stem_conllection(data):
    words = []
    docs_x = []
    docs_y = []
    labels = []
    stemmer = snowball_stemmer()
    for intent in data:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)
    return words, labels, docs_x, docs_y, stemmer
