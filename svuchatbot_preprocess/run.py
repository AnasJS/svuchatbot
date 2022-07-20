from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client
from svuchatbot_preprocess.Methodology import extract_key_words
from svuchatbot_preprocess.exrtract_entities import extract_entities_from_emails,extract_entities
from svuchatbot_preprocess.fetching import insert_emails_into_db,filtering,find_pairs
from svuchatbot_preprocess.sentiment_analyser import camel_based_sentiment_analyser
from svuchatbot_preprocess.stopwords import remove_stop_words
from svuchatbot_preprocess.tokenizer import tokenize
print("*********************************** start fetching mails *********************************")
insert_emails_into_db("mails")
db_client = get_client()
db_name = db_connection_params['db']
db = db_client[db_name]
print("*********************************** start filtering mails *********************************")
filtering(from_col="mails", to_col="filterd_mails")
print("*********************************** start building conversation *********************************")
find_pairs(from_col="filterd_mails", to_col="conversation")
print("*********************************** start tokenizing mails *********************************")
tokenize(from_col="filterd_mails",to_col="tokenized_mails")
print("*********************************** start cleaning tokenized mails *********************************")
remove_stop_words(from_col="tokenized_mails", to_col="cleaned_tokenized_mails")
print("*********************************** start extracting entities *********************************")
extract_entities(from_col="cleaned_tokenized_mails", to_col="mails_and_entities")
print("*********************************** start extracting sentiments *********************************")
camel_based_sentiment_analyser(from_col="mails_and_entities", to_col="mails_and_sentiments")
print("*********************************** start calculate tfidf *********************************")
extract_key_words(from_col = "mails_and_sentiments", to_col="tfidf")






