from svuchatbot_mogodb.client import get_client
from svuchatbot_config.database import db_connection_params
import email
from email.parser import BytesParser, Parser
import email
from email.parser import BytesParser, Parser
from email.policy import default
from os import listdir, getcwd, walk
from os.path import isfile, join, dirname, abspath, basename
from svuchatbot_mogodb.client import get_client
import os
from svuchatbot_config.database import db_connection_params
from bs4 import BeautifulSoup
from langdetect import detect
from aspose import email, util

def read_intents(lang='arabic', collection_name='arabic_intents'):
    db_client = get_client()
    db = db_client[db_connection_params['db']]
    col = db[collection_name]
    documents = [document for document in col.find({})]
    return documents


class email_analyser():
    def __init__(self, row_email):
        self.row_email = row_email

    def parse_header(self):
        pass


def fetch():
    emails_folder_path = os.path.join(os.curdir, '..', "data")
    target_emails_path = [(emails_folder_path, fp) for fp in listdir(emails_folder_path)]
    return target_emails_path


def email_to_db(_email, db, col, file_name):
    if not _email.get_content_type().startswith('application') and not _email.get_content_type().endswith('report'):
        if _email.get_content_type().startswith("multipart"):
            email_as_dict = {key: value for key, value in _email.items()}
            # # email_as_dict['payload'] = email.get_payload()
            email_as_dict["file_name"] = file_name
            email_as_dict["Content-Type"] = _email.get_content_type()
            # col.insert_one(email_as_dict)
            # db['multipart'].insert_one(email_as_dict)
            for p in _email.get_payload():
                # email_to_db(p, db, col, file_name)
                if p.get_content_type()=="text/plain":
                    email_as_dict["payload"] = p.get_payload()
            if email_as_dict.get("payload") is not None:
                col.insert_one(email_as_dict)
        else:

            email_as_dict = {key: value for key, value in _email.items()}
            email_as_dict['payload'] = _email.get_payload()
            email_as_dict["file_name"] = file_name
            email_as_dict["Content-Type"] = _email.get_content_type()
            if _email.get_content_type() == "text/html":
                email_as_dict['payload'] = BeautifulSoup(_email.get_payload(), 'html.parser').get_text()
            col.insert_one(email_as_dict)


def insert_emails_into_db(collection_name = 'mails'):
    mails = dict()
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db[collection_name]
    all_types = set()
    for x, y in fetch():
        mp = join(x, y)
        with open(mp, 'rb') as fp:
            email = BytesParser(policy=default).parse(fp)
            if not email.get_content_type().startswith("application") and not email.get_content_type().endswith(
                    'report'):
                email_to_db(email, db, col, y)


#         all_types.add(email.get_content_type())
#         if email.get_content_type().startswith("multipart"):
#             for p in email.get_payload():
#                 all_types.add(p.get_content_type())
# print(all_types)
#         print(email.get_content_type())
#         if email.get_content_type()=='multipart/report':
#            for p in email.get_payload():
#                if p.get_content_type()=="text/plain":
#                    print(p.get_payload())
#                print("**************")
#         if email.get_content_type()=='multipart/alternative':
#             for p in email.get_payload():
#                 if p.get_content_type()=="text/plain":
#                     print(p.get_payload())
#         if email.get_content_type() == "":
#             email_as_dict = {key: value for key,value in email.items()}
#             email_as_dict['paylod'] = email.get_payload()
#             email_as_dict["file_name"] = mp
#
#             col.insert_one(email_as_dict)
#             print(email.is_multipart())
#

def find_pairs(from_col,to_col):
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db[from_col]
    replies_emails = [e for e  in col.find({"In-Reply-To": {"$exists": True}},["Message-ID","In-Reply-To", "References", "From", "To", "payload",'file_name'])]
    start_emails = [e for e in col.find({"In-Reply-To": {"$exists": False}},["Message-ID", "From", "To", "payload",'file_name'])]
    conversation = [
        {"q_from": s["From"],
         "q_to": s["To"],
         "q_content" : s["payload"],
         "q_file_name" : s["file_name"],
         "a_from" : r["From"],
         "a_to" : r["To"],
         "a_content" : r["payload"],
         "a_file_name":r["file_name"]}
        for s in start_emails
        for r in replies_emails
        if s["Message-ID"]==r["In-Reply-To"]]

    print(len({e["Message-ID"]: e for e in replies_emails }))
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
        print("file name of p1 : " ,c["q_file_name"],"\n")
        print("From : ",c["q_from"],"\n")
        print("question : ", c["q_content"],"\n")
        print("/*","\n")
        print("file name of p2 : " ,c["a_file_name"],"\n")
        print("From : ",c["a_from"],"\n")
        print("answer : ",c["a_content"])
        print("***********")
    db[to_col].insert_many(conversation)
    # return to_col


def fields_based_filter(collection,
                        available_fields=['Message-ID', 'From', 'To', 'Subject', 'Reply-To', 'payload', 'Content-Type',
                                          'Content-Language',"In-Reply-To",'References','file_name']):
    return [e for e in collection.find({}, available_fields)]


def language_based_filter(documents, available_lang='ar'):
    return [e for e in documents if detect(e['payload']) == available_lang]


def device_based_filter(documents, excluded_field="X-Android-Message-ID"):
    return [e for e in documents if excluded_field not in e.keys()]


def filtering(from_col,to_col):
    # delete check conent languafe for english or english and arabic
    # delete all emails from andriod
    # create pairs of Qustion and answer
    # delete multiple replay

    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    col = db[from_col]
    documents = fields_based_filter(col)
    documents = language_based_filter(documents)
    documents = device_based_filter(documents)

    db[to_col].insert_many(documents)
def parse_multipart_emails():
    ##  not to use
    db_client = get_client()
    db_name = db_connection_params['db']
    db = db_client[db_name]
    db.drop_collection("multipart_collection")
    db.drop_collection("single_part_collection")
    multipart_col = db['multipart_collection']
    single_part_col = db['single_part_collection']
    for x, y in fetch():
        mp = join(x, y)
        with open(mp, 'rb') as fp:
            m_email = BytesParser(policy=default).parse(fp)
            if m_email.get_content_type().startswith("multipart"):
                email_as_dict = {key: value for key, value in m_email.items()}
                email_as_dict["file_name"] = mp
                email_as_dict["Content-Type"] = m_email.get_content_type()
                email_as_dict["sub_email_ids"] = [p["Message-ID"] for p in m_email.get_payload()]
                # multipart_col.insert_one(email_as_dict)
                for p in m_email.get_payload():
                    singlepart_email = {key: value for key, value in p.items()}
                    singlepart_email["file_name"] = mp
                    singlepart_email["Content-Type"] = p.get_content_type()
                    singlepart_email["parent_id"] = m_email['Message-ID']
                    if not p.is_multipart():
                        singlepart_email["payload"] = p.get_content()
                    single_part_col.insert_one(singlepart_email)


def fetch_from_pst(file_name="info@svuonline.org.pst"):
    dataDir = os.path.join(os.curdir, '..', "data")

    personalStorage = PersonalStorage.from_file(dataDir + file_name)

    folderInfoCollection = personalStorage.root_folder.get_sub_folders()

    for folderInfo in folderInfoCollection:
        print("Folder: " + folderInfo.display_name)
        print("Total Items: " + str(folderInfo.content_count))
        print("Total Unread Items: " + str(folderInfo.content_unread_count))
        print("----------------------")
