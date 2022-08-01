import sys

from svuchatbot_mogodb.client import SingletonClient
from nltk import RegexpParser, line_tokenize, RegexpTagger
from nltk.tree.tree import Tree


def parse(from_col, to_col, from_db="PST", to_db="PST"):
    client = SingletonClient()
    db = client[from_db]
    col = db[from_col]
    db_to = client[to_db]
    col_to = db_to[to_col]
    patterns = [(r'\t*From: .*', "from"), (r'\t*To: .*', "to"), (r'\t*Subject: .*', 'subject'),
                (r'\t*Sent: .*', 'sent'),
                (r'\t*Cc: .*', 'cc'), (r'.+', 'Content')]
    grammar = '''
    From: {<from>}
    Sent: {<sent>}
    Subject: {<subject>}
    To: {<to><Content>*}
    CC: {<cc><Content>*}
    Header: {<From><Sent><To><CC>?<Subject>}
    Body: {<Content>+}
    Email: {<Header><Body>?}
    Payload: {<Body><Email>+}
    '''
    regexp_tagger = RegexpTagger(patterns)
    cp = RegexpParser(grammar)
    for document in col.find():

        try:
            line_tokens = line_tokenize(document["content"])
            regexp_tags = regexp_tagger.tag(line_tokens)
            col_to.insert_one(parse_message(regexp_tags, cp))
        except Exception as e:
            # exception_type, exception_object, exception_traceback = sys.exc_info()
            # filename = exception_traceback.tb_frame.f_code.co_filename
            # line_number = exception_traceback.tb_lineno
            # print("document['content']")
            # print(document["content"])
            # # print("Message : ", regexp_tags, line_number, e)

            print(e)


def parse_message(message, cp):
    # print(content)
    result = cp.parse(message)
    payload = result[0]
    # try:
    assert payload.__class__ is Tree, "Invalid parsing"
    assert len(payload) == 2, "There is more than one replay"
    assert payload[0].__class__ is Tree and payload[0].label() == "Body", "There isn't any replay"
    replay_message = parse_body(payload[0], tag="replay-message")
    inbox_email = parse_email(payload[1])
    return {**replay_message, **inbox_email}
    # except Exception as e:
    #     exception_type, exception_object, exception_traceback = sys.exc_info()
    #     # filename = exception_traceback.tb_frame.f_code.co_filename
    #     line_number = exception_traceback.tb_lineno
    #     print("Message : ",message,line_number, e)


def parse_email(email):
    assert email.__class__ is Tree and email.label() == "Email", "Invalid parsing inbox email"
    header = parse_header(email[0])
    body = parse_body(email[1])
    return {**header, **body}


def parse_body(body, tag="body"):
    assert body.__class__ is Tree and body.label() == "Body", "Invalid parsing body"
    return {tag: "\n".join([c[0] for c in body])}


def parse_header(header):
    assert header.__class__ is Tree and header.label() == "Header" \
           and len(header) in [4, 5], "Invalid parsing header : \n\t{}".format(header)
    from_ = parse_from(header[0])
    sent = parse_sent(header[1])
    to = parse_to(header[2])
    if len(header) == 4:
        cc = {"cc": ""}
        subject = parse_subject(header[3])
    else:
        cc = parse_cc(header[3])
        subject = parse_subject(header[4])
    return {**from_, **sent, **to, **cc, **subject}


def parse_from(from_):
    assert from_.__class__ is Tree and from_.label() == "From", "Invalid parsing From"
    return {"From": from_[0][0]}


def parse_subject(subject):
    assert subject.__class__ is Tree and subject.label() == "Subject", "Invalid parsing subject"
    return {"Subject": subject[0][0]}


def parse_sent(sent):
    assert sent.__class__ is Tree and sent.label() == "Sent", "Invalid parsing sent"
    return {"Sent": sent[0][0]}


def parse_to(to):
    assert to.__class__ is Tree and to.label() == "To", "Invalid parsing To"
    return {"To": "\n".join([c[0] for c in to])}


def parse_cc(cc):
    assert cc.__class__ is Tree and cc.label() == "CC", "Invalid parsing CC"
    return {"CC": "\n".join([c[0] for c in cc])}


# parse("Sent Items", None)
