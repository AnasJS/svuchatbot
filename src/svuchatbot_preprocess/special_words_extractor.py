from src.svuchatbot_preprocess.tokens_extractor import TokensExtractor
import pandas as pd
import os
from src.svuchatbot_helper.read_specializations import get_specializations


class SpecialWordExtraction(TokensExtractor):
    # def __init__(self, source, field_name, n_cores, target=None, replace=False):
    #     super().__init__(source, field_name, n_cores, target)
        # TokensExtractor.replace_special_words = replace

    def _tokenizer(self):
        df = get_specializations()
        TokensExtractor.special_words_dict = {column: item["name0"] for item in df.iloc for column in item}
        TokensExtractor.special_words = df.values.ravel().tolist()
        return SpecialWordExtraction.special_words_tokenize_for_sentence
