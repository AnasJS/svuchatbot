# # from rake_nltk import Rake
# from svuchatbot_preprocess.bag_of_word import camel_based_accumulation_words,accumulate_phrases
# from pprint import pprint
# def key_words_based_rake():
#     r= Rake()
#     # all_mails = camel_based_accumulation_words()
#     # r.extract_keywords_from_text(all_mails)
#     # ranked_phrases = r.get_ranked_phrases()
#     # ranked_phrases_with_score = r.get_ranked_phrases_with_scores()
#     all_phrases = accumulate_phrases()
#     r.extract_keywords_from_sentences(all_phrases)
#     ranked_phrases = r.get_ranked_phrases()
#     ranked_phrases_with_score = r.get_ranked_phrases_with_scores()
#     return (ranked_phrases,ranked_phrases_with_score)
#
# rp,rps = key_words_based_rake()
# pprint(rp)
# print("*************")
# # print(rps)