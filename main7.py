from os import cpu_count
from svuchatbot_const.db.definitions import Definitions as DB_Definitions
from root import PreProcess, Steps, FeaturesExtraction
from svuchatbot_features_managment.key_words_extractor import KeyWordExtractors, Definitions


def main():
    pp = PreProcess(steps=[
        Steps.READPSTFILE,
        Steps.PARSEEMAILS,
        Steps.REMOVENONARABICANSWERS,
        Steps.REMOVENONARABICQUESTIONS,
        Steps.REMOVEEMPTYQUESTION,
        Steps.REMOVEDUPLICATEDQUESTIONS, #173 emails
        Steps.CORRECTSENTENCES,
        Steps.DROPSENTENCES,
        Steps.REMOVEFORWARDEDEMAILS,
        Steps.REMOVEEMAILSRELATEDTOCORONA,
        Steps.PARSEFROMFIELD,
        Steps.PARSETOFIELD,
        Steps.PARSESUBJECTFIELD,
        Steps.PARSECCFIELD,
        Steps.PARSEBCCFIELD,
        Steps.PARSEDATEFIELD,

    ])
    #
    #
    # pp.run()


    for i in range(1, 6):
        kwe = KeyWordExtractors(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            cpu_count=cpu_count(),
            field_name=DB_Definitions.ANSWERFIELDNAME,
            min_weight=0.01,
            ngram="{}-Gram".format(i),
            normalize=True,
            # prefix="simple",
            reset_db=(i == 1)
        )
        if i == 1:
            kwe.set_pipe([
                Definitions.SIMPLETOKENIZATION,
                Definitions.STOPWORDSREMOVING,
                Definitions.MORPHOLOGICALTOKENIZATION,
                Definitions.STOPWORDSREMOVING,
                Definitions.NORMALIZATION,
                Definitions.STOPWORDSREMOVING,
                Definitions.BAGOFWORDSEXTRACION,
                Definitions.FEATURESSETUP,
                Definitions.TFIDFEXTRACTION,
                Definitions.SPECIALWORDSEXTRACTION

            ])
        elif 1 < i <= 5:
            kwe.set_pipe([
                Definitions.BAGOFWORDSEXTRACION,
                Definitions.FEATURESSETUP,
                Definitions.TFIDFEXTRACTION,
            ])
        kwe.work()

    # FE = FeaturesExtraction(steps=[
    #     Steps.EXTRACTSIMPLETOKENSFROMANSWER,
    #     Steps.EXTRACTSIMPLETOKENSFROMQUESTION,
    #     Steps.EXTRACTSENTIMENTFROMQUESTIONS,
    #     Steps.EXTRACTENTITIESFROMANSWERS
    # ])
    # FE.run()


if __name__ == '__main__':
    main()
