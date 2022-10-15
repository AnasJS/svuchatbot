import pandas as pd
import numpy as np

from src.svuchatbot_mogodb.client import get_collection


def get_last_tokens(source, n):
    col = get_collection(source[0], source[1])
    df = pd.DataFrame(list(col.find()))
    columns = df.columns
    df = df[columns.drop("_id")]
    dfm = df.max(axis=0)
    f = open("last_{}_words_5gram".format(n), "wt")
    f.writelines(dfm.sort_values(ascending=False).tail(n).__str__())
    f.close()


def get_weights_tokens(source, n):
    col = get_collection(source[0], source[1])
    df = pd.DataFrame(list(col.find()))
    columns = df.columns
    df = df[columns.drop("_id")]
    dfm = df.max(axis=0)
    dff = pd.DataFrame(dfm.to_dict().items(), columns=["word","max weight"])
    dff = dff.sort_values('max weight', ascending=False)
    # dfm.sort_values(axis='count', ascending=False)
    dff.to_csv("tokens_{}_gram.csv".format(n, n))
    # f = open("tokens_{}_gram".format(n, n), "wt")
    # f.writelines(dfm.sort_values(ascending=False).__str__())
    # f.close()
    return dff


def get_weight_from_RTF(source):
    n_col, n_db = source
    col = get_collection(n_col, n_db)
    col_arr = np
    df = pd.DataFrame(list(col.find()))
    columns = df.columns
    df = df[columns.drop("_id")]
