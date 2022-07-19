import camel_tools

# import the dediacritization tool
# from camel_tools.utils.dediac import dediac_ar
# print(dediac_ar("الحَمدُ للًَهِ" ))

from nltk.corpus import stopwords

from svuchatbot_preprocess.bag_of_word import camel_based_bag,nltk_based_bag
from nltk.corpus import stopwords
def nltk_based_filter_stopwords():
    n_fdist = nltk_based_bag()
    c_fdsit = camel_based_bag()
    arabic_stopwords = stopwords.words('arabic')
    res = {k:v for k,v in n_fdist.items() if k not in arabic_stopwords}
    print("hgjfkdlshgjfkdlsljghjfkdsldkfjghjfkdls;aslkfjghjfkdlsldkfjghjfkdls;lkfjgfkdls;lkfjkdls;a")
    print(res)
    print(len(res))

nltk_based_filter_stopwords()
# import nltk
# nltk.download('stopwords')