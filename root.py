from datetime import datetime

from svuchatbot_preprocess.filter import Filter
from svuchatbot_preprocess.simple_worker import SimpleWorker
from svuchatbot_sink.pst_sink import PST
from os import cpu_count
from svuchatbot_parsing.parse_pst import PSTParser
from svuchatbot_mogodb.client import get_collection
from datetime import datetime
from os.path import join
from os import pardir, curdir
from svuchatbot_const.db.definitions import Definitions as DB_Definitions


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
    REMOVEDUBLICATEDQUESTIONS = ""
    REMOVEFORWORDEDEMAILS = ""
    REMOVEGREETINGSENTINCESESFROMQUESTIONS = ""


class PreProcess:
    def __init__(self,  steps):


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
        Steps.REMOVENONARABICQUESTIONS: "remove_non_arabic_questions",
        Steps.REMOVENONARABICANSWERS: "remove_non_arabic_answers",
        Steps.REMOVEEMAILSRELATEDTOCORONA: "remove_corona_emails",
        Steps.REMOVEDUBLICATEDQUESTIONS: "",
        Steps.REMOVEFORWORDEDEMAILS: "",
        Steps.REMOVEGREETINGSENTINCESESFROMQUESTIONS: "",
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
                         to_db=DB_Definitions.PARSSEDEMAILSDBNAME)
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
        f = Filter(source=("chatbot", "Sent-Mails-After-Parsing"),
                    target=("chatbot", "Sent-Mails-After-Parsing"))
        f.exclude_emails_writen_in_foreign_language("body")

    @staticmethod
    def remove_non_arabic_answers():
        f = Filter(source=("chatbot", "Sent-Mails-After-Parsing"),
                    target=("chatbot", "Sent-Mails-After-Parsing"))
        f.exclude_emails_writen_in_foreign_language("replay-message")

    @staticmethod
    def remove_corona_emails():
        f = Filter(source=("chatbot", "Sent-Mails-After-Parsing"),
                   target=("chatbot", "Sent-Mails-After-Parsing"))
        f.exclude_emails_containing_word("body", "كورونا"). \
            exclude_emails_containing_word("replay-message", "كورونا")
