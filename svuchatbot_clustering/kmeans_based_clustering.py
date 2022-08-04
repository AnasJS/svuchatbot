import numpy as np
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import AffinityPropagation
from matplotlib import pyplot
from svuchatbot_mogodb.client import get_collection
import pandas as pd

class MyKmeans:
    def __init__(self, source, field_name):
        self.model = AffinityPropagation(damping=0.9)
        self.mails_col_name = source[0][1]
        self.mails_db_name = source[0][0]
        self.BOW_col_name = source[1][1]
        self.BOW_db_name = source[1][0]
        self.field_name = field_name
        self.X = None

    def fit(self):
        bow_col = get_collection("Bag-Of-Words", "3-Gram")
        self.df_X = pd.DataFrame(bow_col.find({}))
        columns = self.df_X.columns.tolist()
        columns.remove("_id")
        self.df_X = self.df_X[columns]
        self.X = self.df_X.values
        self.model.fit(self.X)

    def predict(self):
        yhat = self.model.predict(self.X.tolist())
        clusters = unique(yhat)
        mails = [item[self.field_name] for item in get_collection(self.mails_db_name, self.mails_col_name).find({}, [self.field_name])]
        for cluster in clusters:
            row_ix = where(yhat == cluster)
            # print(len(row_ix))
            if len(row_ix[0]) > 1:
                for i in row_ix[0]:
                    print(mails[i])
                    # print("v")
                print("****************************************************************************")


k = MyKmeans(source=(("chatbot","Sent-Mails-After-Parsing"), ("Bag-Of-Words", "3-Gram")),
             field_name="replay-message")
k.fit()
k.predict()