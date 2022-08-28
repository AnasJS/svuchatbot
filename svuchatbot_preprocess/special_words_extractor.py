from svuchatbot_preprocess.extractor import Extractor
from svuchatbot_preprocess.tokens_extractor import TokensExtractor
import pandas as pd
import os
class SpecialWordExtraction(TokensExtractor):
    # def __init__(self, source, field_name, n_cores,f_path= None, target=None, n_gram=1):
    #     super().__init__(source, field_name, n_cores)


    def _tokenizer(self):
        f_path = os.path.join( os.getcwd(), 'data', "Specializations_of_the_Syrian_Virtual_University.csv" )
        df = pd.read_csv(f_path, names=["name0", "name1", "name2", "name3"])
        df = df.applymap(str.strip)
        TokensExtractor.special_words_dict = {column: item["name0"] for item in df.iloc for column in item}
        TokensExtractor.special_words = df.values.ravel().tolist()
        return SpecialWordExtraction.special_words_tokenize_for_sentence
