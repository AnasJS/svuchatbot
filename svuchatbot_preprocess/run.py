from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import SingletonClient
from svuchatbot_preprocess.Methodology import extract_key_words
from svuchatbot_preprocess.exrtract_entities import extract_entities_from_emails,extract_entities
from svuchatbot_preprocess.fetching import insert_emails_into_db,filtering,find_pairs
from svuchatbot_preprocess.sentiment_analyser import camel_based_sentiment_analyser
from svuchatbot_preprocess.stopwords import remove_stop_words
from svuchatbot_preprocess.tokenizer import tokenize
from svuchatbot_preprocess.parse_pst import parse

print("*********************************** start fetching mails *********************************")
# insert_emails_into_db("mails")
# parse("Sent Items", "Sent-Mails-After-Parsing", from_db="PST", to_db="chatbot")
db_client = SingletonClient()
db_name = db_connection_params['db']
db = db_client[db_name]
print("*********************************** start filtering mails *********************************")
# filtering(from_col="Sent-Mails-After-Parsing", to_col="filterd_mails",filters=["language"], from_db="chatbot", to_db="chatbot")
# print("*********************************** start building conversation *********************************")
# find_pairs(from_col="filterd_mails", to_col="conversation", from_db="chatbot), to_db="chatbot
print("*********************************** start tokenizing mails *********************************")
tokenize(from_col="Sent-Mails-After-Parsing",to_col="tokenized_mails", from_db="chatbot", to_db="chatbot", field_name="body")
print("*********************************** start cleaning tokenized mails *********************************")
remove_stop_words(from_col="tokenized_mails", to_col="cleaned_tokenized_mails", from_db="chatbot", to_db="chatbot")
print("*********************************** start extracting entities *********************************")
extract_entities(from_col="cleaned_tokenized_mails", to_col="mails_and_entities", from_db="chatbot", to_db="chatbot")
print("*********************************** start extracting sentiments *********************************")
camel_based_sentiment_analyser(from_col="mails_and_entities", to_col="mails_and_sentiments", from_db="chatbot", to_db="chatbot",field_name="body")
# print("*********************************** start calculate tfidf *********************************")
# extract_key_words(from_col = "mails_and_sentiments", to_col="tfidf", from_db="chatbot", to_db="chatbot")






