from svuchatbot_preprocess.fetching import read_intents

def read_intents_arabic():
    for d in read_intents():
        print(d)
        # assert type(d) ,str