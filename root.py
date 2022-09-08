from datetime import datetime

from svuchatbot_clustering.simple import add_tag
from svuchatbot_features_managment.pattern_extractor import PatternExtractor
from svuchatbot_helper.patterns_frequency import get_pattern_freq
from svuchatbot_preprocess.filter import Filter
from svuchatbot_preprocess.sentiment_extractor import SentimentExtractor
from svuchatbot_preprocess.entities_extractor import EntitiesExtractor
from svuchatbot_preprocess.simple_worker import SimpleWorker
from svuchatbot_preprocess.special_words_extractor import SpecialWordExtraction
from svuchatbot_sink.pst_sink import PST
from os import cpu_count, curdir, pardir
from svuchatbot_parsing.parse_pst import PSTParser
from svuchatbot_mogodb.client import get_collection
from datetime import datetime
from os.path import join
import pandas as pd
from svuchatbot_const.db.definitions import Definitions as DB_Definitions
from svuchatbot_features_managment.key_words_extractor import KeyWordExtractors, Definitions


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
    CORRECTSENTENCES = "correct_sentences"
    DROPSENTENCES = "drop_sentences"

    #


class PreProcess:
    def __init__(self, steps):

        self.steps_dict = {
            Steps.READPSTFILE: self.read_pst_file,
            Steps.PARSEEMAILS: self.parse_emails,
            Steps.PARSEFROMFIELD: self.parse_from,
            Steps.PARSETOFIELD: self.parse_to,
            # Steps.PARSESENTFIELD: self.parse_sent,
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
            Steps.CORRECTSENTENCES: self.correct_sentences,
            Steps.DROPSENTENCES: self.drop_sentences,
        }
        self.steps = []
        for step in steps:
            if step in self.steps_dict.keys():
                self.steps.append(self.steps_dict[step])

    def run(self):
        for step in self.steps:
            print(f'{step.__name__} start at {datetime.now()}')
            step()

    @staticmethod
    def read_pst_file():
        p = join(curdir, 'data', 'info@svuonline.org.pst')
        pst_sink = PST(p, DB_Definitions.PSTDBNAME, 1)
        pst_sink.sink()

    @staticmethod
    def parse_emails():
        pstp = PSTParser(DB_Definitions.SENTCOLLECTIONNAME,
                         DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME,
                         from_db=DB_Definitions.PSTDBNAME,
                         to_db=DB_Definitions.PARSSEDEMAILSDBNAME,
                         update=True)
        pstp.parse()

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
        f.exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "الزملاء"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "الزميل"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "الزميلة"). \
            exclude_emails_containing_word(DB_Definitions.ANSWERFIELDNAME, "يرجى الاطلاع وشكرا"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "الزملاء"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "الزميل"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "الزميلة"). \
            exclude_emails_containing_word(DB_Definitions.QUESTIONFIELDNAME, "يرجى الاطلاع وشكرا")

    @staticmethod
    def remove_duplicated_questions():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        f.exclude_duplicated(DB_Definitions.QUESTIONFIELDNAME)

    @staticmethod
    def drop_sentences():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        fpath = join(curdir, "assets", "sentence_to_remove.txt")
        file = open(fpath, "rt")
        sents = file.readlines()
        reps = ["" for i in sents]
        f.correct_sentences(DB_Definitions.QUESTIONFIELDNAME, sents, reps). \
            correct_sentences(DB_Definitions.ANSWERFIELDNAME, sents, reps)

    @staticmethod
    def correct_sentences():
        f = Filter(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                   target=(DB_Definitions.PARSSEDEMAILSDBNAME,
                           DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME))
        fpath = join(curdir, "assets", "Correct_Words.csv")
        df = pd.read_csv(fpath, header=None)
        sents = df[0]
        reps = df[1]
        f.correct_sentences(DB_Definitions.QUESTIONFIELDNAME, sents, reps). \
            correct_sentences(DB_Definitions.ANSWERFIELDNAME, sents, reps)


class FeaturesExtraction:
    def __init__(self, steps):
        self.steps_dict = {
            Steps.EXTRACTSIMPLETOKENSFROMANSWER: self.extract_answer_simple_tokens,
            Steps.EXTRACTSIMPLETOKENSFROMQUESTION: self.extract_question_simple_tokens,
            Steps.EXTRACTSENTIMENTFROMQUESTIONS: self.extract_sentiment_from_questions,
            Steps.EXTRACTENTITIESFROMANSWERS: self.extract_entities_from_answers,
        }
        self.steps = []
        for step in steps:
            if step in self.steps_dict.keys():
                self.steps.append(self.steps_dict[step])

    def run(self):
        for step in self.steps:
            print(f'{step.__name__} start at {datetime.now()}')
            step()

    @staticmethod
    def extract_question_simple_tokens():
        kwe = KeyWordExtractors(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            cpu_count=cpu_count(),
            field_name=DB_Definitions.QUESTIONFIELDNAME,
            min_weight=0.01,
            ngram="{}-Gram".format(1),
            prefix="question-simple",
            reset_db=False
        )
        kwe.set_pipe([
            Definitions.SIMPLETOKENIZATION,
            Definitions.STOPWORDSREMOVING,
        ])
        kwe.work()

    @staticmethod
    def extract_answer_simple_tokens():
        kwe = KeyWordExtractors(
            source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                    DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
            cpu_count=cpu_count(),
            field_name=DB_Definitions.ANSWERFIELDNAME,
            min_weight=0.01,
            ngram="{}-Gram".format(1),
            prefix="answer-simple",
            reset_db=False
        )
        kwe.set_pipe([
            Definitions.SIMPLETOKENIZATION,
            Definitions.STOPWORDSREMOVING,
        ])
        kwe.work()

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


    def extract_special_words(self):
        swe = SpecialWordExtraction(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                            DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                                    field_name= DB_Definitions.QUESTIONFIELDNAME,
                                    n_cores=cpu_count(),
                                    target=("", self.prefix+DB_Definitions.SPECIALWORDSFIELDNAME))
        swe.work()

    @staticmethod
    def extract_morphological_patterns():

        pe = PatternExtractor(source=(DB_Definitions.PARSSEDEMAILSDBNAME,
                                      DB_Definitions.PARSSEDEMAILSCOLLECTIONNAME),
                              target=(DB_Definitions.PATTERNSDBNAME,
                                      DB_Definitions.PATTERNSCOLLECTIONNAME),
                              threshold=0.3,
                              n_gram=3,
                              n_cores=cpu_count(),
                              field_name=DB_Definitions.SIMPLETOKENSFIELDNAME)
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
