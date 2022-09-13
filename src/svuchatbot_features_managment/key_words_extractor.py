from datetime import datetime

import pandas as pd

from src.svuchatbot_mogodb.client import SingletonClient, get_collection
from src.svuchatbot_preprocess.cleand_tokens_extractor import Elector

from src.svuchatbot_preprocess.special_words_extractor import SpecialWordExtraction
from src.svuchatbot_preprocess.bag_of_words_extractor import BagOfWordsExtractor
from src.svuchatbot_preprocess.orthographic_normalization import Normalizer
from src.svuchatbot_features_managment.simple_tokens_extractor import SimpleTokensExtractor
from src.svuchatbot_features_managment.morphology_based_tokens_extractor import MorphologyBasedTokensExtractor
from src.svuchatbot_features_managment.tfidf_extractor import TFIDFExtractor
from src.svuchatbot_const.db.definitions import Definitions as DB_Definitions


class Definitions:
    SIMPLETOKENIZATION = "simple_tokenization"
    MORPHOLOGICALTOKENIZATION = "morphological_tokenization"
    NORMALIZATION = "normalization"
    STOPWORDSREMOVING = "remove_stopwords"
    BAGOFWORDSEXTRACION = "bag_of_words_extraction"
    FEATURESSETUP = "setup_features_names"
    TFIDFEXTRACTION = "tfidf_extraction"
    SPECIALWORDSEXTRACTION = "special_words_extraction"


class KeyWordExtractors:
    def __init__(self, source, min_weight, field_name, cpu_count, ngram="1-Gram",
                 normalize=False, prefix=None, reset_db=True):
        # super().__init__(source, field_name, n_cores)
        self.source = source
        self.db_name, self.col_name = self.source
        # self.bow_col_name = source[0][1]
        # self.bow_db_name = source[0][0]
        # self.mit_col_name = source[1][1]
        # self.mit_db_name = source[1][0]
        # self.tfidf_col_name = target[0][1]
        # self.tfidf_db_name = target[0][0]
        # self.mibow_col_name = target[1][1]
        # self.mibow_db_name = target[1][0]
        # self.mif_col_name = target[2][1]
        # self.mif_db_name = target[2][0]
        self.ngram = ngram
        self.min_weight = min_weight
        #
        self.cpu_count = cpu_count
        self.field_name = field_name
        self.normalize = normalize
        if prefix:
            self.prefix = prefix+"-"
        else:
            self.prefix = ""
        if reset_db:
            self._reset_db()
        self.pipe_dict = {
            Definitions.SIMPLETOKENIZATION: self._simple_tokenize,
            Definitions.MORPHOLOGICALTOKENIZATION: self._morphological_tokenize,
            Definitions.NORMALIZATION: self._correction,
            Definitions.STOPWORDSREMOVING: self._election,
            Definitions.BAGOFWORDSEXTRACION: self._extract_bag_of_word,
            Definitions.FEATURESSETUP: self._setup_features_names,
            Definitions.TFIDFEXTRACTION: self._tfidf,
            Definitions.SPECIALWORDSEXTRACTION: self._special_words_extraction
        }
        self.pipe = []

    def _reset_db(self):
        col = get_collection(self.db_name, self.col_name)
        for item in col.find():
            try:
                item.pop(self.prefix+DB_Definitions.TOKENSFIELDNAME)
            except:
                pass
            col.replace_one({"_id": item["_id"]}, item)
        client = SingletonClient()
        client.drop_database(self.prefix+DB_Definitions.TFIDFDBNAME)
        client.drop_database(self.prefix+DB_Definitions.WEIGHTSDBNAME)
        client.drop_database(self.prefix+DB_Definitions.BAGOFWORDSDBNAME)

    def _correction(self):
        if self.normalize:
            n = Normalizer(source=(self.source[0], self.source[1]), n_cores= self.cpu_count,
                           field_name=self.prefix+DB_Definitions.TOKENSFIELDNAME, word=True)
            n.work()
            # e = Elector(source=self.source, field_name=self.prefix+"tokens", n_cores=self.cpu_count)
            # e.work()

    def _simple_tokenize(self):
        col = get_collection(self.source[0], self.source[1])
        if not self.prefix+DB_Definitions.TOKENSFIELDNAME in col.find_one().keys():
            te = SimpleTokensExtractor(self.source, self.field_name, self.cpu_count, target=("", self.prefix+DB_Definitions.TOKENSFIELDNAME))
            te.work()
            # e = Elector(source=self.source, field_name="tokens", n_cores=self.cpu_count)
            # e.work()
            # te = TokensExtractor(self.source, "tokens", self.cpu_count, target=("", "tokens"), type="morphological")
            # te.work()

    def _morphological_tokenize(self):
        col = get_collection(self.source[0], self.source[1])
        # if not self.prefix + "tokens" in col.find_one().keys():
        te = MorphologyBasedTokensExtractor(self.source, self.prefix + DB_Definitions.TOKENSFIELDNAME, self.cpu_count,
                                   target=("", self.prefix + DB_Definitions.TOKENSFIELDNAME))
        te.work()

    def _election(self):
        e = Elector(source=self.source, field_name=self.prefix+DB_Definitions.TOKENSFIELDNAME, n_cores=self.cpu_count)
        e.work()

    def _extract_bag_of_word(self):
        boe = BagOfWordsExtractor(self.source, field_name=self.prefix+DB_Definitions.TOKENSFIELDNAME, n_cores=self.cpu_count,
                                  target=(self.prefix+DB_Definitions.BAGOFWORDSDBNAME, self.ngram), n_gram=int(self.ngram[0]))
        boe.work()

    def _special_words_extraction(self):
        swe = SpecialWordExtraction(self.source, field_name= self.field_name, n_cores=self.cpu_count,
                                  target=("", self.prefix+DB_Definitions.SPECIALWORDSFIELDNAME))
        swe.work()

    def _setup_features_names(self):
        bow_col = get_collection(self.prefix+DB_Definitions.BAGOFWORDSDBNAME, self.ngram)
        bow = bow_col.find({})
        bow = list(bow)
        feature_names = list(bow_col.find_one().keys())
        feature_names.remove("_id")
        self.feature_names = feature_names
        self.df_bag_of_words = pd.DataFrame(bow)[self.feature_names]
        self.bag_of_words = self.df_bag_of_words.values
        return bow

    def _tfidf(self):
        tfidf = TFIDFExtractor(self.bag_of_words,
                               self.ngram,
                               self.feature_names,
                               tfidf_db_name=self.prefix+DB_Definitions.TFIDFDBNAME,
                               weights_db_name=self.prefix+DB_Definitions.WEIGHTSDBNAME)
        tfidf.work()
        # transformer = TfidfTransformer()
        # tfidf = transformer.fit_transform(self.bag_of_words)
        # df_tfidf = pd.DataFrame(tfidf.todense(), columns=self.feature_names)
        # col_tfidf = get_collection("TF-IDF", self.ngram)
        # # col_tfidf.insert_many([{k:v for k,v in zip(self.feature_names, row.tolist())} for row in tfidf.toarray()])
        # # Find most popular words and highest weights
        # word_cnts = np.asarray(self.bag_of_words.sum(axis=0)).ravel().tolist()  # for each word in column, sum all row counts
        # df_cnts = pd.DataFrame({'word': self.feature_names, 'count': word_cnts})
        # df_cnts = df_cnts.sort_values('count', ascending=False)
        #
        # # Build word weights as a list and sort them
        # weights = np.asarray(tfidf.mean(axis=0)).ravel().tolist()
        # df_weights = pd.DataFrame({'word': self.feature_names, 'weight': weights})
        # df_weights = df_weights.sort_values('weight', ascending=False)
        #
        # df_weights = df_weights.merge(df_cnts, on='word', how='left')
        # df_weights = df_weights[['word', 'count', 'weight']]
        # # df_weights = df_weights[df_weights['weight'] > self.min_weight]
        # # df_tfidf = df_tfidf[df_weights['word']]
        # col_tfidf.insert_many([iloc.to_dict() for iloc in df_tfidf.iloc])
        # # col_tfidf.insert_many([{k:v for k,v in zip(self.feature_names, row.tolist())} for row in tfidf.toarray()])
        # col = get_collection("Weights", self.ngram)
        # col.insert_many([iloc.to_dict() for iloc in df_weights.iloc])

    def get_pipe(self):
        return self.pipe_dict.keys()

    def set_pipe(self, pipe):
        for step in pipe:
            if step in self.pipe_dict.keys():
                self.pipe.append(self.pipe_dict[step])

    def work(self):
        if self.pipe is None or self.pipe == []:
            print("Start extracting tokens")
            self._simple_tokenize()
            # self._election()
            # self._morphological_tokenize()
            print("start Normalizing")
            # self._correction()
            # self._election()
            print("start extract bag of words")
            self._extract_bag_of_word()
            print("start create vector of counter")
            self._setup_features_names()
            print("start calculate tfidf")
            self._tfidf()
        else:
            for step in self.pipe:
                print(f"******************** start step {step.__name__} at {datetime.now().time()} ********************")
                step()



