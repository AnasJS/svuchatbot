from src.svuchatbot_clustering.simple import add_tag
from src.svuchatbot_features_managment.features_extractor import MorphologicalFeaturesExtractor
from src.svuchatbot_features_managment.pattern_extractor import PatternExtractor
from src.svuchatbot_features_managment.simple_tokens_extractor import SimpleTokensExtractor
from src.svuchatbot_helper.cleaner import StringCleaner
from src.svuchatbot_helper.patterns_frequency import get_pattern_freq
from src.svuchatbot_preprocess.filter import Filter
from src.svuchatbot_preprocess.orthographic_normalization import Normalizer
from src.svuchatbot_preprocess.sentiment_extractor import SentimentExtractor
from src.svuchatbot_preprocess.entities_extractor import EntitiesExtractor
from src.svuchatbot_preprocess.simple_worker import SimpleWorker
from src.svuchatbot_preprocess.special_words_extractor import SpecialWordExtraction
from src.svuchatbot_preprocess.special_words_replacment import SpecialWordsReplacement
from src.svuchatbot_sink.pst_sink import PST
from os import cpu_count, curdir, pardir, mkdir, system
from src.svuchatbot_parsing.parse_pst import PSTParser
from src.svuchatbot_mogodb.client import get_collection
from datetime import datetime
from os.path import join
import pandas as pd
import re
from src.svuchatbot_clustering.kmeans_based_clustering import MyKmeans
from abc import ABC, abstractmethod
from src.svuchatbot_const.db.definitions import Definitions as DB_Definitions
from src.svuchatbot_features_managment.key_words_extractor import KeyWordExtractors, Definitions
from src.svuchatbot_helper.utils import get_project_root
from emoji import emoji_list
import pandas as pd
from src.svuchatbot_const.db.definitions import Definitions
from src.svuchatbot_mogodb.client import get_collection
import pandas as pd
from datetime import datetime
from camel_tools.utils.dediac import dediac_ar



def strip(word):
    return word.strip()


class Steps:
    READPSTFILE = "read_pst_file"
    PARSEEMAILS = "parse_emails"
    PARSEFROMFIELD = "parse_from"
    PARSETOFIELD = "parse_to"
    PARSESENTFIELD = "parse_sent"
    PARSESUBJECTFIELD = "parse_subject"
    PARSEDATEFIELD = "parse_date"
    PARSECCFIELD = "parse_cc"
    PARSEBCCFIELD = "parse_bcc"
    REMOVENONARABICQUESTIONS = "remove_non_arabic_questions"
    REMOVENONARABICANSWERS = "remove_non_arabic_answers"
    REMOVEEMAILSRELATEDTOCORONA = "remove_corona_emails"
    EXTRACTSIMPLETOKENSFROMANSWER = "extract_answer_simple_tokens"
    EXTRACTSIMPLETOKENSFROMQUESTION = "extract_question_simple_tokens"
    EXTRACTSENTIMENTFROMQUESTIONS = "extract_sentiment_from_questions"
    EXTRACTENTITIESFROMANSWERS = "extract_entities_from_answers"
    REMOVEDUPLICATEDQUESTIONS = "remove_duplicated_questions"
    REMOVEFORWARDEDEMAILS = "remove_forwarded_emails"
    REMOVEGREETINGSENTINCESESFROMQUESTIONS = ""
    REMOVEEMPTYQUESTION = "remove_empty_questions"
    CORRECTWORDS = "correct_words"
    DROPSENTENCES = "drop_sentences"
    REPLACESPECIALWORDS = "replace_special_words"
    EXTRACTSPECIALWORDS = "extract_special_words"
    REPLACESPECIALWORDSFROMQUESTION = "replace_special_words_from_question"
    EXTRACTSPECIALWORDSFROMQUESTION = "extract_special_words_from_question"
    EXTRACTMORPHOLOGICALFEATURES = "extract_morphological_features"
    EXTRACTMORPHOLOGICALPATTERNS = "extract_morphological_patterns"
    REPLACESPECIALWORDSFROMANSWER = "replace_special_words_from_answer"
    EXTRACTSPECIALWORDSFROMANSWER = "extract_special_words_from_answer"
    KMEANSBASEDCLUSTERING = "split_emails_based_on_kmeans_clustering"
    REMOVEEMAILSCONTAINSQUESTIONINREPLAY = "remove_emails_contain_question_in_replay"
    SHORTENINIGSPACES = "shortening_spaces"
    DROPEMOJIS = "drop_emojis"
    ExtractShortQuestion = "extract_short_question"
    NORMALIZEANSWERTOKEN = "normalize_answer_token"
    NORMALIZEQUESTIONTOKEN = "normalize_question_token"
    Export_Questions_To_File = "Export_Questions_To_File"
    Export_Collections = "export_collections"
    Delete_Diac = "delete_diac"

    #


class Workflow(ABC):
    def __init__(self):
        self.steps_dict = {}
        self.steps = []
        self.set_available_methods()

    def transform(self, steps):
        for step in steps:
            if step in self.steps_dict.keys():
                self.steps.append(self.steps_dict[step])

    def run(self):
        for step in self.steps:
            print("\t\t\t/\t\t\t\t****\t\t\t\t\\\n")
            print("\t\t/\t\t\t\t****************\t\t\t\\\n")
            print("\t/\t\t\t******************************\t\t\t\\\n")
            print(f'/\t\t Step:  {step.__name__}\t\t\t\t\t\t\t\t\\')
            print(f'\\\t\t starts now at {datetime.now()}\t\t/')
            print("\t\t\n\\\t\t\t******************************\t\t\t/\n")
            print("\t\t\\\t\t\t\t****************\t\t\t/\n")
            print("\t\t\t\\\t\t\t\t****\t\t\t\t/\n")
            step()

    @abstractmethod
    def set_available_methods(self):
        self.steps_dict = {}


class PreProcess(Workflow):
    def set_available_methods(self):
        self.steps_dict = {
            Steps.READPSTFILE: self.read_pst_file,
            Steps.Delete_Diac: self.delete_diac,
            Steps.PARSEEMAILS: self.parse_emails,
            Steps.PARSEFROMFIELD: self.parse_from,
            Steps.PARSETOFIELD: self.parse_to,
            Steps.PARSESUBJECTFIELD: self.parse_subject,
            Steps.PARSEDATEFIELD: self.parse_date,
            Steps.PARSECCFIELD: self.parse_cc,
            Steps.PARSEBCCFIELD: self.parse_bcc,
            Steps.REMOVENONARABICQUESTIONS: self.remove_non_arabic_questions,
            Steps.REMOVENONARABICANSWERS: self.remove_non_arabic_answers,
            Steps.REMOVEEMAILSRELATEDTOCORONA: self.remove_corona_emails,
            Steps.REMOVEFORWARDEDEMAILS: self.remove_forwarded_emails,
            Steps.REMOVEEMPTYQUESTION: self.remove_empty_questions,
            Steps.REMOVEDUPLICATEDQUESTIONS: self.remove_duplicated_questions,
            Steps.REMOVEGREETINGSENTINCESESFROMQUESTIONS: "",
            Steps.CORRECTWORDS: self.correct_words,
            Steps.DROPSENTENCES: self.drop_sentences,
            Steps.REMOVEEMAILSCONTAINSQUESTIONINREPLAY: self.remove_emails_contain_question_in_replay,
            Steps.SHORTENINIGSPACES: self.shortening_spaces,
            Steps.DROPEMOJIS: self.drop_emojis,


        }

    @staticmethod
    def read_pst_file():
        # p = join(get_project_root(), 'data', 'info@svuonline.org.pst')
        p = join(get_project_root(), 'assets', 'bait_coor@svuonline.org.pst')
        pst_sink = PST(p, DB_Definitions.PSTDBNAME, 1)
        pst_sink.sink()

    @staticmethod
    def delete_diac():
        def __do(field_name, item, col):
            item[field_name] = dediac_ar(item[field_name])
            col.replace_one({"_id": item["_id"]}, item)

        sw = SimpleWorker(source=(DB_Definitions.PSTDBNAME,
                                  DB_Definitions.SENTCOLLECTIONNAME),
                          field_name=DB_Definitions.content_field_name,
                          n_cores=cpu_count(),
                          do=__do)
        sw.work()


    @staticmethod
    def parse_emails():
        pstp = PSTParser(DB_Definitions.SENTCOLLECTIONNAME,
                         DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME,
                         from_db=DB_Definitions.PSTDBNAME,
                         to_db=DB_Definitions.PARSSEDEMAILSDBNAME,
                         update=True)
        pstp.parse()
        a_col = get_collection(DB_Definitions.ANALYSIS, DB_Definitions.AnalysisCollection)
        a_col.delete_many({})
        col = get_collection(DB_Definitions.PARSSEDEMAILSDBNAME, DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME)

        count = col.find({})
        count = [d for d in count]
        count = len(count)
        a_col.insert_one({"filter name": "Parsed Emails", "count": count, "data": datetime.now()})

    @staticmethod
    def __template_parser(key, do=None, cpus=cpu_count()):
        if do is None:
            def do(k, i, c):
                if key in i.keys():
                    if type(i[key]) == str:
                        try:
                            data = i[k].split(f"{k}: ")[1]
                            i.update({f"{k}": data})
                            c.replace_one({"_id": i["_id"]}, i)
                        except:
                            print(i["_id"])

        sw = SimpleWorker((DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME), key, cpus, do)
        sw.work()

    @staticmethod
    def parse_date():
        def do(k, i, c):
            if key in i.keys():
                if type(i[key]) == str:
                    try:
                        data = i[k].split(f"{k}: ")[1]
                        dt = datetime.strptime(data, '%A, %B %d, %Y %I:%M %p')
                        i.update({f"{k}": dt})
                        c.replace_one({"_id": i["_id"]}, i)
                    except:
                        print(i["_id"])

        keys = ["Sent", "Date"]
        for key in keys:
            PreProcess.__template_parser(key, do=do)

    @staticmethod
    def parse_from():
        PreProcess.__template_parser("From")

    @staticmethod
    def parse_to():
        PreProcess.__template_parser("To")

    @staticmethod
    def parse_subject():
        PreProcess.__template_parser("Subject")

    @staticmethod
    def parse_sent():
        PreProcess.__template_parser("Sent")

    @staticmethod
    def parse_cc():
        PreProcess.__template_parser("Cc")

    @staticmethod
    def parse_bcc():
        PreProcess.__template_parser("Bcc")

    @staticmethod
    def remove_non_arabic_questions():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        f.exclude_emails_writen_in_foreign_language(DB_Definitions.QUESTIONFIELDNAME)

    @staticmethod
    def remove_empty_questions():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        f.exclude_empty_emails(DB_Definitions.QUESTIONFIELDNAME)

    @staticmethod
    def remove_non_arabic_answers():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        f.exclude_emails_writen_in_foreign_language(DB_Definitions.ANSWERFIELDNAME)

    @staticmethod
    def remove_corona_emails():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        f.exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "كورونا"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "كورونا")

    @staticmethod
    def remove_forwarded_emails():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        f.exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "الزملاء", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "الزميل", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "الزميلة", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "يرجى الاطلاع", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "يرجى الاطلاع و شكرا", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "يرجى الرد و شكرا", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "الزملاء", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "الزميل", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "الزميلة", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "يرجى الاطلاع", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "يرجى الاطلاع و شكرا", name="forwarded_emails"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "يرجى الرد و شكرا", name="forwarded_emails")

    @staticmethod
    def remove_duplicated_questions():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        f.exclude_duplicated(DB_Definitions.QUESTIONFIELDNAME)

    @staticmethod
    def drop_sentences():
        fpath = join(get_project_root(), "assets", "sentence_to_remove.txt")
        file = open(fpath, "rt")
        sents = [f"^{sent.strip()}|\W{sent.strip()}\W" for sent in file.readlines()]
        reps = [" " for i in sents]

        # def __do(field, item, col):
        #         text = item[field]
        #         for sent, rep in zip(sents, reps):
        #             text = re.sub(sent, rep, text)
        #         item[field] = text
        #         col.replace_one({"_id": item["_id"]}, item)
        # sw = SimpleWorker(
        #     source=(DB_Definitions.PARSSEDEMAILSDBNAME,
        #             DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
        #     n_cores=cpu_count(),
        #     field_name=DB_Definitions.QUESTIONFIELDNAME,
        #     do=__do
        # )
        # sw.work()
        # sw.field_name = DB_Definitions.ANSWERFIELDNAME
        # sw.work()

        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))

        f.correct_sentences(DB_Definitions.QUESTIONFIELDNAME, sents, reps). \
            correct_sentences(DB_Definitions.ANSWERFIELDNAME, sents, reps)

    @staticmethod
    def correct_words():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        fpath = join(get_project_root(), "assets", "Correct_Words.csv")
        df = pd.read_csv(fpath, header=None)
        # sents = " " + df[0].apply(strip) + " "
        tmp = df[0].apply(strip)
        sents = "^"+tmp+"|\W+"+tmp+"\W+"
        reps = " " + df[1] + " "
        f.correct_sentences(DB_Definitions.QUESTIONFIELDNAME, sents, reps). \
            correct_sentences(DB_Definitions.ANSWERFIELDNAME, sents, reps)

    @staticmethod
    def remove_emails_contain_question_in_replay():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        f.exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "؟", name="emails_contain_question_in_replay"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "يرجى توضيح المطلوب", name="emails_contain_question_in_replay")
        # exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "?")

    @staticmethod
    def shortening_spaces():
        def __do(field_name, item, col):
            item[field_name] = re.sub("  +", " ", item[field_name])
            col.replace_one({"_id": item["_id"]}, item)

        sw = SimpleWorker(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                  DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                          field_name=DB_Definitions.ANSWERFIELDNAME,
                          n_cores=cpu_count(),
                          do=__do)
        sw.work()
        sw = SimpleWorker(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                  DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                          field_name=DB_Definitions.QUESTIONFIELDNAME,
                          n_cores=cpu_count(),
                          do=__do)
        sw.work()

    @staticmethod
    def drop_emojis():
        def __doo(fld, itm, col):
            # pass
            print(len(emoji_list(itm[fld])))
            if len(emoji_list(itm[fld])) > 0:
                print(itm[fld])
                res = emoji_list(itm[fld])
                res.reverse()
                for e in res:
                    itm[fld] = itm[fld][:e["match_start"]] + itm[fld][e["match_end"]:]
                print(itm[fld])
            #     print("********************************************************************************************")
            col.replace_one({"_id": itm["_id"]}, itm)

        sw = SimpleWorker((DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                          DB_Definitions.QUESTIONFIELDNAME,
                          cpu_count(),
                          __doo
                          )
        sw.work()


class FeaturesExtraction(Workflow):
    def set_available_methods(self):
        self.steps_dict = {
            Steps.EXTRACTSIMPLETOKENSFROMANSWER: self.extract_answer_simple_tokens,
            Steps.EXTRACTSIMPLETOKENSFROMQUESTION: self.extract_question_simple_tokens,
            Steps.EXTRACTSENTIMENTFROMQUESTIONS: self.extract_sentiment_from_questions,
            Steps.EXTRACTENTITIESFROMANSWERS: self.extract_entities_from_answers,
            Steps.EXTRACTSPECIALWORDSFROMQUESTION: self.extract_special_words_from_question,
            Steps.REPLACESPECIALWORDSFROMQUESTION: self.replace_special_words_from_question,
            Steps.REPLACESPECIALWORDSFROMANSWER: self.replace_special_words_from_answer,
            Steps.EXTRACTSPECIALWORDSFROMANSWER: self.extract_special_words_from_answer,
            Steps.EXTRACTMORPHOLOGICALFEATURES: self.extract_morphological_features,
            Steps.EXTRACTMORPHOLOGICALPATTERNS: self.extract_morphological_patterns,
            Steps.ExtractShortQuestion: self.extract_short_question,
            Steps.NORMALIZEQUESTIONTOKEN: self.normalize_question_token,
            Steps.NORMALIZEANSWERTOKEN: self.normalize_answer_token

        }

    @staticmethod
    def extract_question_simple_tokens():
        ste = SimpleTokensExtractor(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            field_name=DB_Definitions.QUESTIONFIELDNAME,
            n_cores=cpu_count(),
            target=("", DB_Definitions.QUESTIONSIMPLETOKENSFIELDNAME))
        ste.work()

    @staticmethod
    def normalize_question_token():
        n = Normalizer(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            n_cores=cpu_count(),
            field_name=DB_Definitions.QUESTIONSIMPLETOKENSFIELDNAME,
            word=True)
        n.work()

    @staticmethod
    def normalize_answer_token():
        n = Normalizer(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            n_cores=cpu_count(),
            field_name=DB_Definitions.ANSWERSIMPLETOKENSFIELDNAME,
            word=True)
        n.work()

    @staticmethod
    def extract_answer_simple_tokens():
        ste = SimpleTokensExtractor(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            field_name=DB_Definitions.ANSWERFIELDNAME,
            n_cores=cpu_count(),
            target=("", DB_Definitions.ANSWERSIMPLETOKENSFIELDNAME))
        ste.work()

    @staticmethod
    def extract_sentiment_from_questions():
        se = SentimentExtractor((DB_Definitions.PARSSEDEMAILSDBNAME,
                                 DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                                DB_Definitions.QUESTIONSIMPLETOKENSFIELDNAME, cpu_count())
        se.work()

    @staticmethod
    def extract_entities_from_answers():
        ee = EntitiesExtractor(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                       DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                               field_name=[DB_Definitions.QUESTIONSIMPLETOKENSFIELDNAME,
                                           DB_Definitions.ANSWERSIMPLETOKENSFIELDNAME],
                               n_cores=cpu_count()
                               )
        ee.work()

    @staticmethod
    def extract_special_words_from_question():
        swe = SpecialWordExtraction(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                            DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                                    field_name=DB_Definitions.QUESTIONFIELDNAME,
                                    n_cores=cpu_count(),
                                    target=("", DB_Definitions.SPECIALWORDSFIELDNAMEFROMQUESTION),
                                    )
        swe.work()

    @staticmethod
    def replace_special_words_from_question():
        swr = SpecialWordsReplacement(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            field_name=DB_Definitions.QUESTIONFIELDNAME,
            n_cores=cpu_count(),
            from_field_name=DB_Definitions.SPECIALWORDSFIELDNAMEFROMQUESTION
        )
        swr.work()

    @staticmethod
    def extract_special_words_from_answer():
        swe = SpecialWordExtraction(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                            DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                                    field_name=DB_Definitions.ANSWERFIELDNAME,
                                    n_cores=cpu_count(),
                                    target=("", DB_Definitions.SPECIALWORDSFIELDNAMEFROMANSWER),
                                    )
        swe.work()

    @staticmethod
    def replace_special_words_from_answer():
        swr = SpecialWordsReplacement(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            field_name=DB_Definitions.ANSWERFIELDNAME,
            n_cores=cpu_count(),
            from_field_name=DB_Definitions.SPECIALWORDSFIELDNAMEFROMANSWER
        )
        swr.work()

    @staticmethod
    def extract_morphological_features():
        mfe = MorphologicalFeaturesExtractor(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                                     DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                                             n_cores=cpu_count(),
                                             field_name=DB_Definitions.ANSWERSIMPLETOKENSFIELDNAME)
        mfe.work()

    @staticmethod
    def extract_morphological_patterns():
        pe = PatternExtractor(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                      DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                              target=(DB_Definitions.PATTERNSDBNAME,
                                      DB_Definitions.PATTERNSCOLLECTIONNAME),
                              threshold=0.0,
                              n_gram=1,
                              n_cores=cpu_count(),
                              field_name=DB_Definitions.ANSWERSIMPLETOKENSFIELDNAME)
        pe.work()

        col = get_collection(DB_Definitions.PATTERNSDBNAME,
                             DB_Definitions.PATTERNSCOLLECTIONNAME)
        emails_ids = set([item["email_id"] for item in col.find({}, {"email_id": 1, "_id": 0})])
        col = get_collection(DB_Definitions.PARSSEDEMAILSDBNAME,
                             DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME)
        ids = set([item["_id"] for item in col.find({}, {"_id": 1})])
        message = f'There is an error in PatternExtractor,{len(emails_ids)}!={len(ids)}'
        assert len(emails_ids) == len(ids), message
        freq = get_pattern_freq((DB_Definitions.PATTERNSDBNAME,
                                 DB_Definitions.PATTERNSCOLLECTIONNAME))
        col = get_collection(DB_Definitions.PATTERNSDBNAME,
                             DB_Definitions.PATTERNSFREQUENCYCOLLECTIONNAME)
        emails_ids = set([item["email_id"] for item in col.find({}, {"email_id": 1, "_id": 0})])
        # print(len(freq))
        assert len(emails_ids) == len(ids), "There is an error in get_pattern_freq"
        add_tag()

    @staticmethod
    def extract_short_question():
        df = pd.read_csv(join(get_project_root(), 'assets', 'questions_words.csv'), names=['qw'])
        question_words = df["qw"].tolist()

        def __doo(fld, itm, col):
            res = []
            word_ptrn = '\w+'
            ques_mark = '?'
            dot_mark = '.'
            for qw in question_words:
                ptrn = f'^{qw} [\w+ *]+ ?[.؟]?|\W{qw} [\w+ *]+ ?[.؟]?'

                # ptrn = qw + " [\w* ]*؟?.?"
                tmp = re.sub('\n', ' ', itm[fld])
                res += re.findall(ptrn, tmp)
            itm["questions"] = res
            col.replace_one({"_id": itm["_id"]}, itm)

        sw = SimpleWorker(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            field_name=DB_Definitions.QUESTIONFIELDNAME,
            n_cores=cpu_count(),
            do=__doo)
        sw.work()


class EmailsClustering(Workflow):
    def set_available_methods(self):
        self.steps_dict = {
            Steps.KMEANSBASEDCLUSTERING: self.split_emails_based_on_kmeans_clustering,
        }

    @staticmethod
    def split_emails_based_on_kmeans_clustering():
        k = MyKmeans(
            source=(
                (DB_Definitions.PARSSEDEMAILSDBNAME,
                 DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                (DB_Definitions.BAGOFWORDSDBNAME,
                 DB_Definitions.BAGOFWORDSCOLLECTIONNAME1GRAM)),
            field_name=DB_Definitions.ANSWERFIELDNAME,
            n_clusters=30,
            utter_file_name=f"utter__{datetime.now().strftime('%m_%d_%Y__%H_%M_%S')}.yml",
            intent_file_name=f"intent__{datetime.now().strftime('%m_%d_%Y__%H_%M_%S')}.yml",
            n_gram=1,
            # specializations_from_answers=False,
            specializations_from_questions=False
        )
        k.fetch()
        # k.standardization()
        k.calculate_pca()
        k.kmeans_with_pca_fit()
        # k.fit()
        k.to_yaml()
        k.update_db()


class Exporter(Workflow):
    def set_available_methods(self):
        self.steps_dict = {
            Steps.Export_Questions_To_File: self.export_questions_to_file,
            Steps.Export_Collections: self.export_collections
        }


    @staticmethod
    def export_questions_to_file():
        col = get_collection(Definitions.PARSSEDEMAILSDBNAME,
                             Definitions.PARSSEDEMAILSCOLLECTIONNAME)
        res = []
        name = f'result_questions_{datetime.now()}'.replace(':', "_").replace('.', "_").replace('-', '_').replace(' ', '__')
        name = join("result", name)
        mkdir(name)
        for item in col.find({"questions": {"$ne": []}}):

            for q in item["questions"]:
                res.append({
                    "id": item["_id"],
                    "intent": item["tag"],
                    "answer": item["replay-message"],
                    "question": q,
                    "email": item["body"]

                })
        # df = pd.DataFrame(res, columns=["id", "intent", "answer", "question", "email"])
        df = pd.DataFrame(res)
        df.to_csv(join(name, "q$a.csv"))

        res = []
        for item in col.find({"questions": []}):
            res.append({
                "id": item["_id"],
                "intent": item["tag"],
                "answer": item["replay-message"],
                "question": "",
                "email": item["body"]

            })
        # df = pd.DataFrame(res, columns=["id", "intent", "answer", "question", "email"])
        df = pd.DataFrame(res)
        df.to_csv(join(name, "empty_q&a.csv"))

    @staticmethod
    def export_collections():
        collections = [
            (DB_Definitions.ANALYSIS, DB_Definitions.AnalysisCollection),
            (DB_Definitions.BAGOFWORDSDBNAME, DB_Definitions.BAGOFWORDSCOLLECTIONNAME1GRAM),
            (DB_Definitions.BAGOFWORDSDBNAME, DB_Definitions.BAGOFWORDSCOLLECTIONNAME2GRAM),
            (DB_Definitions.PARSSEDEMAILSDBNAME, DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            (DB_Definitions.PSTDBNAME, DB_Definitions.SENTCOLLECTIONNAME),
            (DB_Definitions.TFIDFDBNAME, DB_Definitions.BAGOFWORDSCOLLECTIONNAME1GRAM),
            (DB_Definitions.WEIGHTSDBNAME, DB_Definitions.BAGOFWORDSCOLLECTIONNAME1GRAM),
            (DB_Definitions.FAILEDPARSSEDEMAILSDBNAME, DB_Definitions.FAILEDPARSSEDEMAILSCOLLECTIONNAME)
        ]
        name = f'result_Database_{datetime.now()}'.replace(':',"_").replace('.',"_").replace('-','_').replace(' ','__')
        name = join("result", name)
        mkdir(name)

        for db, col in collections:
            tmp = join(name, f"{db}_{col}")
            cmd = f"mongoexport --collection={col} --db={db} --out={tmp}.csv"
            system(cmd)

