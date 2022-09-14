from src.svuchatbot_config import db_connection_params
from src.svuchatbot_mogodb import SingletonClient
from src.svuchatbot_preprocess_old.extract_entities import extract_entities
from src.svuchatbot_preprocess.tokens_extractor import  TokensExtractor #camel_based_sentiment_analyser
from src.svuchatbot_preprocess import remove_stop_words
from src.svuchatbot_preprocess import tokenize

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
TokensExtractor.camel_based_sentiment_analyser(from_col="mails_and_entities", to_col="mails_and_sentiments", from_db="chatbot", to_db="chatbot",field_name="body")
# print("*********************************** start calculate tfidf *********************************")
# extract_key_words(from_col = "mails_and_sentiments", to_col="tfidf", from_db="chatbot", to_db="chatbot")






