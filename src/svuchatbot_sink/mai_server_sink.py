#todo

from email.parser import BytesParser
from email.policy import default
from os import listdir
from os.path import join
from src.svuchatbot_mogodb.client import get_collection
from bs4 import BeautifulSoup


class MailsSinker:
    def __init__(self, d_path, target):
        self.d_path = d_path
        self.db_name = target[0]
        self.col_name = target[0]

    def __fetch(self):
        target_emails_path = [fp for fp in listdir(self.d_path)]
        return target_emails_path

    @staticmethod
    def __email_to_db(_email, col, file_name=""):
        if not _email.get_content_type().startswith('application') and not _email.get_content_type().endswith('report'):
            if _email.get_content_type().startswith("multipart"):
                email_as_dict = {key: value for key, value in _email.items()}
                # email_as_dict["file_name"] = file_name
                # email_as_dict["Content-Type"] = _email.get_content_type()
                for p in _email.get_payload():
                    if p.get_content_type() == "text/plain":
                        email_as_dict["body"] = p.get_payload()
                if email_as_dict.get("body") is not None:
                    col.insert_one(email_as_dict)
            else:
                email_as_dict = {key: value for key, value in _email.items()}
                email_as_dict['body'] = _email.get_payload()
                # email_as_dict["file_name"] = file_name
                # email_as_dict["Content-Type"] = _email.get_content_type()
                if _email.get_content_type() == "text/html":
                    email_as_dict['body'] = BeautifulSoup(_email.get_payload(), 'html.parser').get_text()
                col.insert_one(email_as_dict)

    def insert_emails_into_db(self):
        mails = dict()
        col = get_collection(self.db_name, self.col_name)
        all_types = set()
        for f in self.__fetch():
            mp = join(self.d_path, f)
            with open(mp, 'rb') as fp:
                _email = BytesParser(policy=default).parse(fp)
                if not _email.get_content_type().startswith("application") and not _email.get_content_type().endswith(
                        'report'):
                    MailsSinker.__email_to_db(_email, col, file_name=f)

    def find_replies(self):
        col = get_collection(self.db_name, self.col_name)
        replies_emails = [e for e in col.find({"In-Reply-To": {"$exists": True}},
                                              ["References", "body"])]
        start_emails = [e for e in col.find({"In-Reply-To": {"$exists": False}},
                                            ["Message-ID", "From", "To", "body", 'file_name'])]
        conversation = [
            {"q_from": s["From"],
             "q_to": s["To"],
             "q_content": s["payload"],
             "q_file_name": s["file_name"],
             "a_from": r["From"],
             "a_to": r["To"],
             "a_content": r["payload"],
             "a_file_name": r["file_name"]}
            for s in start_emails
            for r in replies_emails
            if s["Message-ID"] == r["In-Reply-To"]]

        print(len({e["Message-ID"]: e for e in replies_emails}))
        print(len({e["Message-ID"]: e for e in start_emails}))
        # refs = {d["Message-ID"]: d["Message-ID", "In-Reply-To", "From", "To", "Payload"] for d in
        #         col.find({"In-Reply-To": {"$exists": True}},
        #                  ["Message-ID", "Subject", "In-Reply-To", "From", "To", "Payload"])}
        # ids = {d["Message-ID"]: d["Message-ID", "In-Reply-To", "From", "To", "Payload"] for d in
        #        col.find({"Message-ID": {"$exists": True}}, ["Message-ID", "Subject", "From", "To", "Payload"])}
        # # refs = [d["In-Reply-To"] for d in documents]
        # print(ids.keys())
        # print(refs.keys())
        # res1 = [id for id in ids if id in refs]
        # res2 = [ref for ref in refs if ref in ids]
        # print(len(res1))
        # print(len(res2))
        print(len(conversation))
        for c in conversation:
            print("file name of p1 : ", c["q_file_name"], "\n")
            print("From : ", c["q_from"], "\n")
            print("question : ", c["q_content"], "\n")
            print("/*", "\n")
            print("file name of p2 : ", c["a_file_name"], "\n")
            print("From : ", c["a_from"], "\n")
            print("answer : ", c["a_content"])
            print("***********")
        db[to_col].insert_many(conversation)
        # return to_col


