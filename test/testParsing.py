import re

from bson import ObjectId

from svuchatbot_mogodb.client import SingletonClient
from nltk import RegexpParser, line_tokenize, RegexpTagger
from nltk.tree.tree import Tree
patterns = [
            (r'\t*(> ?)* *From: ?.*', "from"),
            (r'\t*(> ?)* *FROM: ?.*', "from"),
            (r'\t*(> ?)* *To: ?.*', "to"),
            (r'\t*(> ?)* *TO: ?.*', "to"),
            (r'\t*(> ?)* *Subject: ?.*', 'subject'),
            (r'\t*(> ?)* *SUBJECT: ?.*', 'subject'),
            (r'\t*(> ?)* *Sent: ?.*', 'sent'),
            (r'\t*(> ?)* *SENT: ?.*', 'sent'),
            (r'\t*(> ?)* *Date: ?.*', 'date'),
            (r'\t*(> ?)* *DATE: ?.*', 'date'),
            (r'\t*(> ?)* *Cc: ?.*', 'cc'),
            (r'\t*(> ?)* *CC: ?.*', 'cc'),
            (r'\t*(> ?)* *BCC: ?.*', 'bcc'),
            (r'\t*(> ?)* *Bcc: ?.*', 'bcc'),
            (r'\t*(> ?)* *المرسل|من: ?.*', "ar_from"),
            (r'\t*(> ?)* *إلى|: ?.*', "ar_to"),
            (r'\t*(> ?)* *الموضوع: ?.*', 'ar_subject'),
            (r'\t*(> ?)* *تم الإرسال: ?.*', 'ar_sent'),
            (r'\t*(> ?)* *التاريخ: ?.*', 'ar_date'),
            (r'\t*(> ?)* *نسخة: ?.*', 'ar_cc'),
            (r'\t*(> ?)* *-+ ?Original [mM]essage ?-+', 'EN_ORIGINALMESSAGE'),
            (r'\t*(> ?)* *-+ ?Originalnachricht ?-+', 'GE_ORIGINALMESSAGE'),
            (r'\t*(> ?)* *-+ ?الرسالة الأساسية ?-+', 'AR_ORIGINALMESSAGE'),
            (r'\t*(> ?)* *-+ ?الرسالة الأصلية ?-+', 'AR_ORIGINALMESSAGE'),
            (r'\t*(> ?)* *-+ ?الرسالة المعاد توجيهها ?-+', 'AR_FORWORDEDMESSAGE'),
            (r'\t*(> ?)* *-+ ?الرسالة المُعاد توجيهها ?-+', 'AR_FORWORDEDMESSAGE'),
            (r'\t*(> ?)* *-+ ?رسالة مُعاد توجيهها ?-+', 'AR_FORWORDEDMESSAGE'),
            (r'\t*(> ?)* *-+ ?Forwarded [Mm]essage ?-+', 'EN_FORWORDEDMESSAGE'),
            # (r'---- info كتب ----', 'AR_InfoWrite'),
            (r'\t*(> ?)* *-+ ?info كتب ?-+', 'AR_InfoWrite'),
            (r'\t*(> ?)* * ?.*[Ss]ent a message using.*', 'SENTFROM'),
            (r'\t*(> ?)* * ?.*مرسل من','AR_SENTFROM'),
            (r'\t*(> ?)* * ?.*مُرسل من','AR_SENTFROM'),
            (r'\t*(> ?)* * ?.*أُرسلت من','AR_SENTFROM'),
            (r'\t*(> ?)* * ?.*[sS]ent [Ff]rom.*','SENTUSING'),
            (r'.+', 'Content'),
        ]
grammar = '''
        ORIGINALMESSAGE: {<EN_ORIGINALMESSAGE|AR_ORIGINALMESSAGE|GE_ORIGINALMESSAGE>}
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
a='''يرجى إرسال ايميل لمنسق البرنامج من خلال العناوين الموجودة على الموقع ضمن
اتصل بنا ومن ثم الاتثال بالجامعة

 

From: soso ta [mailto:soso92.ta@hotmail.com] 
Sent: Wednesday, January 10, 2018 1:48 PM
To: info
Subject: رد: RE: [Website feedback] هاام

 

سجلت بالمفاضله ترقيه معهد تقاني احصائي اقتصاد 
ولم يظهر اسمي بين المقبولين معدلي 74.14 
الاسم اسراء نادر التلا 
والاوراق كامله 

‫مُرسل من هاتف Sony Xperia™‎ الذكي الخاص بي

‏

----‏ info كتب ----

ماهو سؤالك 

-----Original message-----
From: ohaidar@svuonline.org [mailto:ohaidar@svuonline.org] On Behalf Of
SVU
Sent: Tuesday, January 09, 2018 10:53 PM
To: info@svuonline.org
Subject: [Website feedback] هاام

اسراء نادر التلا (soso92.ta@hotmail.com) sent a message using the
contact form at https://svuonline.org/en/node/120.

ليش مافي رد نهائيا

'''
b = '''يرجى إرسال ايميل بهذا الخصوص لمنسق برنامج الاقتصاد على العنوان التالي:
bsce_coor@svuonline.org 

-----Original Message-----
From: rani_94321@svuonline.org [mailto:rani_94321@svuonline.org] 
Sent: Tuesday, January 23, 2018 9:54 PM
To: info@svuonline.org
Subject: Fwd: طلب معادلة مواد عن طريق كشف العلامات من معهد علوم مالية و مصرفية للطالب الجديد راني شيا F17



-------- الرسالة الأساسية --------
الموضوع: طلب معادلة مواد عن طريق كشف العلامات من معهد علوم  مالية و مصرفية للطالب الجديد راني شيا F17
التاريخ: 2018-01-23 21:36
المرسل: rani_94321@svuonline.org
المستقبل: bsce_coor@svuonline.org

طلب معادلة مواد عن طريق كشف العلامات من معهد علوم  مالية و مصرفية للطالب الجديد راني شيا F17 لقد دفعت مبلغ 5 مواد مع رسوم الجامعة ورسوم الامتحانات الرجاء معادلة موادي لكي استطيع الدخول سنة ثانية تجارة واقتصاد في جامعتكم المحترمة
----------------------------------
HASAN ABI SHAKAA
Director of Educational Services Department GSM   : +90 531 335 53 00
Telephone: +90 212 508 81 06
Facebook  : SamaTurk.edu
www.edu.samaturk.com.tr <http://www.samaturk.com.tr/> 
hasan@samaturk.com.tr <mailto:tarek@samaturk.com.tr> 
Telegram : edusamaturk
'''
c='''
يرجى إرسال ايميل لمنسق البرنامج من خلال العناوين الموجودة على الموقع ضمن
اتصل بنا ومن ثم الاتثال بالجامعة

 

From: soso ta [mailto:soso92.ta@hotmail.com] 
Sent: Wednesday, January 10, 2018 1:48 PM
To: info
Subject: رد: RE: [Website feedback] هاام

 

سجلت بالمفاضله ترقيه معهد تقاني احصائي اقتصاد 
ولم يظهر اسمي بين المقبولين معدلي 74.14 
الاسم اسراء نادر التلا 
والاوراق كامله 

‫مُرسل من هاتف Sony Xperia™‎ الذكي الخاص بي

‏

----‏ info كتب ----

ماهو سؤالك 

-----Original Message-----
From: ohaidar@svuonline.org [mailto:ohaidar@svuonline.org] On Behalf Of
SVU
Sent: Tuesday, January 09, 2018 10:53 PM
To: info@svuonline.org
Subject: [Website feedback] هاام

اسراء نادر التلا (soso92.ta@hotmail.com) sent a message using the
contact form at https://svuonline.org/en/node/120.

ليش مافي رد نهائيا

'''
d='''يرجى إرسال ايميل لمنسق البرنامج من خلال العناوين الموجودة على الموقع ضمن
اتصل بنا ومن ثم الاتثال بالجامعة

 

From: soso ta [mailto:soso92.ta@hotmail.com] 
Sent: Wednesday, January 10, 2018 1:48 PM
To: info
Subject: رد: RE: [Website feedback] هاام

 

سجلت بالمفاضله ترقيه معهد تقاني احصائي اقتصاد 
ولم يظهر اسمي بين المقبولين معدلي 74.14 
الاسم اسراء نادر التلا 
والاوراق كامله 

‫مُرسل من هاتف Sony Xperia™‎ الذكي الخاص بي

‏

----‏ info كتب ----

ماهو سؤالك 

-----Original Message-----
From: ohaidar@svuonline.org [mailto:ohaidar@svuonline.org] On Behalf Of
SVU
Sent: Tuesday, January 09, 2018 10:53 PM
To: info@svuonline.org
Subject: [Website feedback] هاام

اسراء نادر التلا (soso92.ta@hotmail.com) sent a message using the
contact form at https://svuonline.org/en/node/120.

ليش مافي رد نهائيا
'''
e = '''claude chahood (cchahood@gmail.com) sent a message using the contact form at https://svuonline.org/en/contact-us.
الرجاء تدقيق طلبي
رقمي الجامعي هو 97729'''
line_tokens = line_tokenize(re.sub('[\u202b\u200f\u202a\u202b]','',e))
# line_tokens = line_tokenize(document["content"])
regexp_tags = regexp_tagger.tag(line_tokens)
for rt in regexp_tags:
    print(rt)
print("***********************")
result = cp.parse(regexp_tags)
result.pretty_print()
result.draw()
a="-------- Original message --------"