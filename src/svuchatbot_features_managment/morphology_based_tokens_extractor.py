from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer

from src.svuchatbot_preprocess.tokens_extractor import TokensExtractor


class MorphologyBasedTokensExtractor(TokensExtractor):
    def _tokenizer(self):
        mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
        TokensExtractor.msa_d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='d3tok', split=True)
        return TokensExtractor.camel_morphological_based_tokenize_for_sentence
