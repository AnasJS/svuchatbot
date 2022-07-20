from pprint import pprint

import wordcloud

import nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arabic_reshaper
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer

from sklearn.metrics.pairwise import cosine_similarity

from svuchatbot_config import db_connection_params
from svuchatbot_mogodb.client import get_client
from svuchatbot_preprocess.bag_of_word import accumulate_phrases
from sklearn.cluster import KMeans
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from svuchatbot_preprocess.bag_of_word import nltk_based_accumulate_clean_phrases

def build_vectorizer(sentences, vocab=None, min_df=0.0, max_df=1.0,
                     ngram_range=(1, 1)):  # for a 2-gram use: ngram_range=(1,2)
    '''
    Build the tf-idf vectorizer:
    1. Build the count_vectorizer from the input sentences.
    2. Transform count_vectorizer to bag-of-words.
    3. Fit the transform to the bag-of-words.

    Note:
    Alternatively we can do this directly with 'TfidfVectorizer' instead of using 'CountVectorizer' followed by 'TfidfTransformer'

    Return:
    cvec, feature_names, df_bag_of_words, tfidf, df_weights, cos_sim, samp_dist
    '''

    # Build count vectorizer
    count_vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, vocabulary=vocab,
                                       ngram_range=(1, 1))  # stop_words='english, max_features=N_FEATURES
    cvec = count_vectorizer.fit(sentences)

    # Get feature names
    feature_names = cvec.get_feature_names()
    print
    # Get bag-of-words and analyze
    bag_of_words = cvec.transform(sentences)
    df_bag_of_words = pd.DataFrame(bag_of_words.todense(), columns=feature_names)

    # Transform bag_of_words into tf-idf matrix
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(bag_of_words)

    # Find most popular words and highest weights
    word_cnts = np.asarray(bag_of_words.sum(axis=0)).ravel().tolist()  # for each word in column, sum all row counts
    df_cnts = pd.DataFrame({'word': feature_names, 'count': word_cnts})
    df_cnts = df_cnts.sort_values('count', ascending=False)

    # Build word weights as a list and sort them
    weights = np.asarray(tfidf.mean(axis=0)).ravel().tolist()
    df_weights = pd.DataFrame({'word': feature_names, 'weight': weights})
    df_weights = df_weights.sort_values('weight', ascending=False)

    df_weights = df_weights.merge(df_cnts, on='word', how='left')
    df_weights = df_weights[['word', 'count', 'weight']]

    # Cosine similarity of sentences
    cos_sim = cosine_similarity(tfidf, tfidf)

    # Distance matrix of sentences
    samp_dist = 1 - cos_sim

    return cvec, feature_names, df_bag_of_words, tfidf, df_weights, cos_sim, samp_dist

def extract_key_words(from_col= "mails_from_files",to_col="tf-idf"):
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    collection = db[from_col]
    sentences = [d["payload"] for d in collection.find()]

    cvec, feature_names, df_bag_of_words, tfidf, df_weights, cos_sim, samp_dist = build_vectorizer(sentences)

    df_tfidf = pd.DataFrame(tfidf.todense(), columns=feature_names)
    # res = {message_id:tf_idf_row for message_id,tf_idf_row in zip(sentences.keys(), df_tfidf.iloc)}

    print("%d dummy sentences:" % len(sentences))
    print(sentences)
    print("---")
    print("%d feature_names (each feature represents a distinct word):" % len(feature_names))
    print(feature_names)
    print("---")
    print("df_tfidf[%d,%d]:" % (len(sentences), len(feature_names)))
    print(df_tfidf.to_string())
    print("---")
    print("df_weights:")
    print(df_weights)
    print("---")
    print("cos_sim[%d,%d] (a square matrix of length and width = len(sentences)):" % (len(sentences), len(sentences)))
    print(cos_sim)
    print("df_bag_of_words[%d,%d]:" % (len(sentences), len(feature_names)))
    print(df_bag_of_words)
    "/************************** insert into db **********************************/"
    # db_client = get_client()
    # db_name = db_connection_params['db']
    # db = db_client[db_name]
    # collection = db[col]
    # documents = [d for d in collection.find()]
    # res=[]
    # for cs in cos_sim:
    #     res_r=[]
    #     for i in range(len(cs)):
    #         if cs[i]>0.5:
    #             res_r.append(feature_names[i])
    #     res.append({"key_words" :res_r})
    # res = []
    # for r in df_tfidf.iloc:
    #     res_r = []
    #     for c in df_tfidf.columns:
    #         if r[c] > 0.1:
    #             res_r.append(c)
    #     res.append({"key_words" :res_r})
    #
    # new_collection = [{**d, **r} for (d,r) in zip(documents,res)]
    # db["mails_with_key_word"].insert_many(new_collection)


    document = {
        # "cvec" : cvec ,
     "feature_names" : feature_names ,
     # "df_bag_of_words" : df_bag_of_words.to_dict() ,
     # "tfidf" : df_tfidf.to_dict() ,
     # "df_weights" : df_weights.to_dict() ,
     # "cos_sim" : cos_sim ,
     # "samp_dist" : samp_dist
    }
    db[to_col].insert_one(document)

    collection = db[from_col]
    messages_ids = [d["Message-ID"] for d in collection.find({},["Message-ID"])]
    m_db = db_client["Methodology"]
    col = m_db["TF-IDF"]
    for id,item in zip(messages_ids,df_tfidf.iloc):
        item=item.to_dict()
        item["Message-ID"] = id
        col.insert_one(dict(item))

    col = m_db["Bag-Of-Words"]
    for item in df_bag_of_words.iloc:
        col.insert_one(item.to_dict())

    col = m_db["Weights"]
    for item in df_weights.iloc:
        col.insert_one(item.to_dict())


    col = m_db["COS_SIN"]
    for id,item in zip(messages_ids,cos_sim):
        col.insert_one({"Messag-ID":id,"cos_sin":list(item)})

#
# extract_key_words()
# extract_key_words(col="analysed")








