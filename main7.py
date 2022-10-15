from os import cpu_count
from src.svuchatbot_const.db.definitions import Definitions as DB_Definitions
from src.root import PreProcess, Steps, FeaturesExtraction, EmailsClustering, Exporter
from src.svuchatbot_features_managment.key_words_extractor import KeyWordExtractors, Definitions


def main():
    pp = PreProcess()
    pp.transform([
        Steps.READPSTFILE,
        Steps.Delete_Diac,
        Steps.PARSEEMAILS,
        Steps.SHORTENINIGSPACES,
        Steps.REMOVENONARABICANSWERS,
        Steps.REMOVENONARABICQUESTIONS,
        Steps.REMOVEEMPTYQUESTION,
        Steps.REMOVEDUPLICATEDQUESTIONS, #173 emails
        Steps.REMOVEEMAILSCONTAINSQUESTIONINREPLAY,
        Steps.DROPEMOJIS,
        Steps.CORRECTWORDS,
        Steps.REMOVEFORWARDEDEMAILS,
        # todo replace more than space with one space
        Steps.DROPSENTENCES,
        # Steps.REMOVEFORWARDEDEMAILS,
        Steps.REMOVEEMAILSRELATEDTOCORONA,
        Steps.PARSEFROMFIELD,
        Steps.PARSETOFIELD,
        Steps.PARSESUBJECTFIELD,
        Steps.PARSECCFIELD,
        Steps.PARSEBCCFIELD,
        Steps.PARSEDATEFIELD,
    ])

    pp.run()


    for i in range(1, 3):
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
        elif 1 < i <= 3:
            kwe.set_pipe([
                Definitions.BAGOFWORDSEXTRACION,
                Definitions.FEATURESSETUP,
                Definitions.TFIDFEXTRACTION,
            ])
        kwe.work()
    #
    FE = FeaturesExtraction()
    FE.transform([
        Steps.EXTRACTSIMPLETOKENSFROMANSWER,
        Steps.EXTRACTSIMPLETOKENSFROMQUESTION,
        # Steps.EXTRACTSENTIMENTFROMQUESTIONS,
        # Steps.EXTRACTENTITIESFROMANSWERS,
        #
        #
        Steps.EXTRACTSPECIALWORDSFROMQUESTION,
        Steps.REPLACESPECIALWORDSFROMQUESTION,
        Steps.EXTRACTSPECIALWORDSFROMANSWER,
        Steps.REPLACESPECIALWORDSFROMANSWER,
        Steps.EXTRACTMORPHOLOGICALFEATURES,
        Steps.NORMALIZEQUESTIONTOKEN,
        Steps.NORMALIZEANSWERTOKEN,
        # Steps.EXTRACTMORPHOLOGICALPATTERNS,
        Steps.ExtractShortQuestion
    ])
    FE.run()

    ec = EmailsClustering()
    ec.transform(
        [
            Steps.KMEANSBASEDCLUSTERING,
        ]
    )
    ec.run()

    e = Exporter()
    e.transform(
        [
            Steps.Export_Questions_To_File,
            Steps.Export_Collections
        ]
    )
    e.run()




if __name__ == '__main__':


    # mp.set_start_method('spwan')
    main()
