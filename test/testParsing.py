from bson import ObjectId

from svuchatbot_mogodb.client import SingletonClient
from nltk import RegexpParser, line_tokenize, RegexpTagger
from nltk.tree.tree import Tree
patterns = [
            (r'\t*>* *From: ?.*', "from"),
            (r'\t*>* *To: ?.*', "to"),
            (r'\t*>* *Subject: ?.*', 'subject'),
            (r'\t*>* *Sent: ?.*', 'sent'),
            (r'\t*>* *Date: ?.*', 'date'),
            (r'\t*>* *Cc: ?.*', 'cc'),
            (r'\t*>* *Bcc: ?.*', 'bcc'),
            (r'\t*>* *المرسل|من: ?.*', "ar_from"),
            (r'\t*>* *إلى|: ?.*', "ar_to"),
            (r'\t*الموضوع>* *: ?.*', 'ar_subject'),
            (r'\t*>* *تم الإرسال: ?.*', 'ar_sent'),
            (r'\t*>* *التاريخ: ?.*', 'ar_date'),
            (r'\t*>* *نسخة: ?.*', 'ar_cc'),
            (r'\t*>* *-+ ?Original Message ?-+', 'EN_ORIGINALMESSAGE'),
            (r'\t*>* *-+ ?الرسالة الأصلية ?-+', 'AR_ORIGINALMESSAGE'),
            (r'\t*>* *-+ ?الرسالة المعاد توجيهها ?-+', 'AR_FORWORDEDMESSAGE'),
            (r'\t*>* *-+ ?Forwarded message ?-+', 'EN_FORWORDEDMESSAGE'),
            # (r'---- info كتب ----', 'AR_InfoWrite'),
            (r'\t*>* *-+ ?info كتب ?-+', 'AR_InfoWrite'),
            (r'.+', 'Content'),
        ]
grammar = '''
            ORIGINALMESSAGE: {<EN_ORIGINALMESSAGE|AR_ORIGINALMESSAGE>}
            FORWORDEDMESSAGE: {<AR_FORWORDEDMESSAGE|EN_FORWORDEDMESSAGE>}
            From: {<from|ar_from>}
            Sent: {<sent|ar_sent>}
            Date: {<date|ar_date>}
            Subject: {<subject|ar_subject>}
            To: {<to|ar_to><Content>*}
            CC: {<cc|ar_cc><Content>*}
            BCC: {<bcc><Content>*}
            Header: {<ORIGINALMESSAGE|FORWORDEDMESSAGE>?<From><Sent>?<To><CC>?<BCC>?<Date>?<Subject>}
            Body: {<Content>+}
            Email: {<Header><Body>?}
            ShortEmail: {<AR_InfoWrite><Body>}
            Payload: {<Body><Email|ShortEmail>+}
            '''
client = SingletonClient()
db = client["PST"]
col = db["Sent Items"]
document = col.find_one({"_id": ObjectId('62d96508f02a7ff6a29fc0ef')})
regexp_tagger = RegexpTagger(patterns)
cp = RegexpParser(grammar)
line_tokens = line_tokenize(document["content"])
regexp_tags = regexp_tagger.tag(line_tokens)
for rt in regexp_tags:
    print(rt)
print("***********************")
result = cp.parse(regexp_tags)
result.pretty_print()