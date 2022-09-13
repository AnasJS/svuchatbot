from svuchatbot_training.train import train_intents
from src.svuchatbot_helper.data_repository import bag_of_words
from src.svuchatbot_preprocess import read_intents
import numpy
from time import sleep
import random


def chat():
    #todo remove words && data
    data = read_intents()
    model , words,labels = train_intents()
    print("Hi, How can i help you ?")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        if results[results_index] > 0.8:
            for tg in data:
                if tg['tag'] == tag:
                    responses = tg['responses']
            sleep(3)
            Bot = random.choice(responses)
            print(Bot)
        else:
            print("I don't understand!")