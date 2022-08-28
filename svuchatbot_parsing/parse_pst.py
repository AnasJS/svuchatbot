from svuchatbot_mogodb.client import SingletonClient
from nltk import RegexpParser, line_tokenize, RegexpTagger
from nltk.tree.tree import Tree


class PSTParser:
    def __init__(self, from_col, to_col, from_db="PST", to_db="PST"):
        self.from_col = from_col
        self.from_db = from_db
        self.to_col = to_col
        self.to_db = to_db
        self.set_grammar()

    def set_grammar(self):
        self.patterns = [
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
            (r'\t*>* *-----Original Message-----', 'EN_ORIGINALMESSAGE'),
            (r'\t*>* *-------- الرسالة الأصلية --------', 'AR_ORIGINALMESSAGE'),
            (r'\t*>* *---------- الرسالة المعاد توجيهها ----------', 'AR_FORWORDEDMESSAGE'),
            (r'\t*>* *---------- Forwarded message ----------', 'EN_FORWORDEDMESSAGE'),
            # (r'---- info كتب ----', 'AR_InfoWrite'),
            (r'\t*>* *---- info كتب ----', 'AR_InfoWrite'),
            (r'.+', 'Content'),

        ]
        #

        self.grammar = '''
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

    def parse(self):
        client = SingletonClient()
        db = client[self.from_db]
        col = db[self.from_col]
        db_to = client[self.to_db]
        col_to = db_to[self.to_col]

        regexp_tagger = RegexpTagger(self.patterns)
        cp = RegexpParser(self.grammar)
        for document in col.find():
            try:
                line_tokens = line_tokenize(document["content"])
                regexp_tags = regexp_tagger.tag(line_tokens)
                col_to.insert_one(self.parse_message(regexp_tags, cp))
            except Exception as e:
                # exception_type, exception_object, exception_traceback = sys.exc_info()
                # filename = exception_traceback.tb_frame.f_code.co_filename
                # line_number = exception_traceback.tb_lineno
                # print("document['content']")
                # print(document["content"])
                # # print("Message : ", regexp_tags, line_number, e)

                print(e)

    def parse_message(self, message, cp):
        # print(content)
        result = cp.parse(message)
        payload = result[0]
        # try:
        assert payload.__class__ is Tree, "Invalid parsing"
        assert len(payload) == 2, "There is more than one replay"
        assert payload[0].__class__ is Tree and payload[0].label() == "Body", "There isn't any replay"
        replay_message = self.parse_body(payload[0], tag="replay-message")
        inbox_email = self.parse_email(payload[1])
        return {**replay_message, **inbox_email}
        # except Exception as e:
        #     exception_type, exception_object, exception_traceback = sys.exc_info()
        #     # filename = exception_traceback.tb_frame.f_code.co_filename
        #     line_number = exception_traceback.tb_lineno
        #     print("Message : ",message,line_number, e)

    def parse_email(self, email):
        assert email.__class__ is Tree and (email.label() == "Email" or email.label() == "ShortEmail"), "Invalid parsing inbox email"
        if email.label() == "Email" :
            header = self.parse_header(email[0])
            body = self.parse_body(email[1])
            return {**header, **body}
        elif email.label() == "ShortEmail":
            header = {}
            body = self.parse_body(email[1])
            return {**header, **body}


    def parse_body(self, body, tag="body"):
        assert body.__class__ is Tree and body.label() == "Body", "Invalid parsing body"
        return {tag: "\n".join([c[0] for c in body])}

    def parse_header(self, header):
        assert header.__class__ is Tree and header.label() == "Header" \
               and len(header) in [4, 5, 6, 7], "Invalid parsing header : \n\t{}".format(header)
        # if header[0].label() == "ORIGINALMESSAGE" or header[0].label() == "FORWORDEDMESSAGE":
        from_ = self.parse_from(header)
        sent = self.parse_sent(header)
        to = self.parse_to(header)
        cc = self.parse_cc(header)
        bcc = self.parse_bcc(header)
        date = self.parse_date(header)
        subject = self.parse_subject(header)
        # if len(header) == 4:
        #     cc = {"cc": ""}
        #     subject = self.parse_subject(header[3])
        # else:
        #     cc = self.parse_cc(header[3])
        #     subject = self.parse_subject(header[4])
        return {**from_, **sent, **to, **cc, **bcc, **date, **subject}

    def parse_from(self, header):
        for item in header:
            if item.label() == "From":
                return {"From": item[0][0]}
                break
        # assert from_.__class__ is Tree and from_.label() == "From", "Invalid parsing From"
        # return {"From": from_[0][0]}
        return {}

    def parse_subject(self, header):
        for item in header:
            if item.label() == "Subject":
                return {"Subject": item[0][0]}
                break
        return {}
        # assert subject.__class__ is Tree and subject.label() == "Subject", "Invalid parsing subject"
        # return {"Subject": subject[0][0]}

    def parse_sent(self, header):
        for item in header:
            if item.label() == "Sent":
                return {"Sent": item[0][0]}
                break
        return {}
        # assert sent.__class__ is Tree and sent.label() == "Sent", "Invalid parsing sent"
        # return {"Sent": sent[0][0]}

    def parse_date(self, header):
        for item in header:
            if item.label() == "Date":
                return {"Date": item[0][0]}
                break
        return {}

    def parse_to(self, header):
        for item in header:
            if item.label() == "To":
                return {"To": item[0][0]}
                break
        return {}
        # assert to.__class__ is Tree and to.label() == "To", "Invalid parsing To"
        # return {"To": "\n".join([c[0] for c in to])}

    def parse_cc(self, header):
        for item in header:
            if item.label() == "CC":
                return {"CC": item[0][0]}
                break
        return {}
        # assert cc.__class__ is Tree and cc.label() == "CC", "Invalid parsing CC"
        # return {"CC": "\n".join([c[0] for c in cc])}

    def parse_bcc(self, header):
        for item in header:
            if item.label() == "BCC":
                return {"BCC": item[0][0]}
                break
        return {}

# parse("Sent Items", None)
