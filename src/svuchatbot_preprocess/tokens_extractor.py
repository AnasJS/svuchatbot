from abc import ABC, abstractmethod

from langdetect import detect
from nltk.tokenize import word_tokenize
from camel_tools.tokenizers.word import simple_word_tokenize
from src.svuchatbot_mogodb.client import get_collection
from src.svuchatbot_preprocess.extractor import Extractor
import re


class TokensExtractor(Extractor, ABC):
    def __init__(self, source, field_name, n_cores, target=None, type_="simple"):
        super().__init__(source, field_name, n_cores)
        self.type = type_
        if target is None:
            self.t_col_name = "tokens"
        else:
            self.t_col_name = target[1]

    @staticmethod
    def nltk_based_tokenize_for_sentence(sent):
        res = []
        for word in word_tokenize(sent):
            try:
                if detect(word) == 'ar':
                    res.append(word)
            except:
                pass
        return res

    @staticmethod
    def camel_simple_based_tokenize_for_sentence(sent):
        res = []
        for word in simple_word_tokenize(sent):
            try:
                if detect(word) == 'ar':
                    res.append(word)
            except:
                pass
        return res

    @staticmethod
    def special_words_tokenize_for_sentence(sent):
        res = set()
        for word in TokensExtractor.special_words:
            try:
                for w in re.findall(word, sent):
                    res.add((TokensExtractor.special_words_dict[w], w))
            except:
                pass
        return list(res)

    @staticmethod
    def camel_morphological_based_tokenize_for_sentence(tokens):
        msa_bw_tok = [w for w in TokensExtractor.msa_d3_tokenizer.tokenize(tokens)
                      if not w.startswith("+")
                      and not w.endswith("+")]
        return msa_bw_tok

    @abstractmethod
    def _tokenizer(self):
        pass

    def do(self, ids):
        col = get_collection(self.db_name, self.col_name)
        cursor = col.find({"_id": {"$in": ids}})
        # if self.type == "simple":
        #     tokenizer = TokensExtractor.camel_simple_based_tokenize_for_sentence
        # elif self.type == "morphological":
        #     tokenizer = TokensExtractor.camel_morphological_based_tokenize_for_sentence
        #     mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
        #     TokensExtractor.msa_d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='d3tok', split=True)
        # msa_bw_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='bwtok', split=True)
        # path1 = join(__package__, pardir, "assets", "our_stop_words_v2.txt")
        # path2 = join(__package__, pardir, "assets", "useless_words.txt")
        # ostp = np.append(o_stopwords(path1), o_stopwords(path2))
        tokenizer = self._tokenizer()
        for item in cursor:
            tokens = tokenizer(item[self.field_name])
            item.update({self.t_col_name: tokens})
            cursor.collection.replace_one({"_id": item["_id"]}, item)
