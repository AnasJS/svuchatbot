import re

from bson import ObjectId

from src.svuchatbot_mogodb import SingletonClient
from nltk import RegexpParser, line_tokenize, RegexpTagger

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
    (r'\t*(> ?)* *-+ ?.*info كتب.* ?-+', 'AR_InfoWrite'),
    (r'.*info <info@svuonline.org> كتب.*', 'AR_InfoWrite'),
    (r'.*جاء من.*بتاريخ.*', 'AR_InfoWrite'),
    (r'.*كتب/كتبت svu.*', 'AR_InfoWrite'),
    (r'info (<info@svuonline.org)?.*', 'AR_InfoWrite'),
    (r'.*تمت كتابة ما يلي بواسطة.*', 'AR_InfoWrite'),
    (r'.*wrote:.*', 'AR_InfoWrite'),
    (
    r'On (Mon|Tue|Wed|Thu|Fri|Sat|Sun), [0-9]{1,2} (Jan|Mar|Feb|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4} [0-9]{2}:[0-9]{2}.*',
    'AR_InfoWrite'),
(r'في (السبت|الأحد|الاثنين|الثلاثاء|الأربعاء|الخميس|الجمعة)، [٠-٩]{1,2} (يناير|فبراير|مارس|أبريل|إبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر)،? [٠-٩]{4} [٠-٩]{1,2}:[٠-٩]{1,2}.*', 'AR_InfoWrite'),


    (r'.*كتب:.*', 'AR_InfoWrite'),
    (r'\t*(> ?)* *-+ ?.*[Ss]ent a message using.*', 'SENTFROM'),
    (r'\t*(> ?)* *-+ ?.*مرسل من', 'AR_SENTFROM'),
    (r'\t*(> ?)* *-+ ?.*مُرسل من', 'AR_SENTFROM'),
    (r'\t*(> ?)* *-+ ?.*أُرسلت من', 'AR_SENTFROM'),
    (r'\t*(> ?)* *-+ ?.*[sS]ent [Ff]rom.*', 'SENTUSING'),
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
                   ShortEmail: {<AR_InfoWrite>+<Body>}
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
f='''الزملاء الأعزاء
يرجى الاطلاع
وشكرا جزيلا 

 

From: Fansah Hamo [mailto:fansahhamo.2018@gmail.com] 
Sent: Monday, December 17, 2018 9:30 PM
To: info
Subject: Re: [Website feedback] كشف علامات الدبلوم التأهيل التربوي للعام
الدراسي ٢٠١٠

 

السلام عليكم  انا السيدة فنسة محمود حمو حاولت الدخول في حسابي ولكن لم
انجح في ذلك لانني كنت أتذكر ان كلمة المرور هو رقمي الوطني ولكن لم أتمكن
من الدخول   ، أرجو منكم مساعدتي .

ولكم كل الشكر والتقدير 

 

في الأحد، ١٦ ديسمبر، ٢٠١٨ ١٠:٤١، كتب info <info@svuonli ne.org>:

	يجب أن تقومي بالدخول إلى حسابك الجامعي وتقديم الطلب من حسابك 
	
	-----Original Message-----
	From: portal@svuonline.org [mailto:portal@svuonline.org] On
Behalf Of SVU
	Sent: Thursday, December 13, 2018 10:45 PM
	To: info@svuonline.org
	Subject: [Website feedback] كشف علامات الدبلوم التأهيل التربوي
للعام الدراسي ٢٠١٠
	
	فنسة محمود حمو (fansahhamo.2018@gmail.com) sent a message using
the contact form at https://svuonline.org/en/node/120.
	
	السلام عليكم :انا السيدة فنسة محمود حمو
	اريد الحصول على كشف علامات شهادة الدبلوم التأهيل التربوي  . علما
بأنني درست الدبلوم التأهيل التربوي للعام الدراسي ٢٠٠٨-٢٠٠٩ استنادا إلى
قرار الجامعة الافتراضية رقم ٤٦١ تاريخ ١٣/١٠/٢٠١٠
	الاسم فنسة حمو     اسم الاب محمود   اسم الأم
	كولي
	الجنسية  ع.س    درجة الدبلوم التأهيل
	التربوي
	قسم تاريخ    بمرتبة جيد جدا
	ومعدل قدره ٧.،٨٢ سبعون درجة واثنان وثمانون جزءا بالمائة بنتيجة
امتحانات  الفصل الدراسي الدورة التكميلية الأولى دمشق في 22/11/1431هجري
الموافق ل 30/10/2010 ولكم جزيل الشكر

'''
g='''يرجى التواصل مع قسم الدعم التقني على العنوان التالي:

support@svuonline.org <mailto:support@svuonline.org>  

 

 

From: Ehab Alsaeed94 [mailto:ehabalsaeed129@gmail.com] 
Sent: Sunday, October 6, 2019 12:49 PM
To: info <info@svuonline.org>
Subject: Re: مفاضله ماجستير خريف 2019

 

ماعم يعطيني خيارات للبرنامج التي ترغب التسجيل بها؟؟ 

 

في الأحد، ٦ أكتوبر، ٢٠١٩ ١:٤٩ ص، كتب Ehab Alsaeed94
<ehabalsaeed129@gmail.com <mailto:ehabalsaeed129@gmail.com> >:

	علمآ انا عم سجل كرمال قدم ع مفاضلة الماجستير

	يعني عم قدم ل امتحان اللغة 

	 

	في الأحد، ٦ أكتوبر، ٢٠١٩ ١:٤٧ ص، كتب Ehab Alsaeed94
<ehabalsaeed129@gmail.com <mailto:ehabalsaeed129@gmail.com> >:

		عم سجل عم يطلب مني البرنامج الذي ارغب التسجيل فيه ومافي
خيارات

		شو اعمل؟ بعد أذنك 🌹

		 

		في الخميس، ٣ أكتوبر، ٢٠١٩ ٨:٥٧ ص، كتب info
<info@svuonline.org <mailto:info@svuonline.org> >:

			ينتهي التسجيل 7/10/2019

			 

			From: Ehab Alsaeed94
[mailto:ehabalsaeed129@gmail.com <mailto:ehabalsaeed129@gmail.com> ] 
			Sent: Thursday, October 03, 2019 8:22 AM
			To: info@svuonline.org
<mailto:info@svuonline.org> 
			Subject: مفاضله ماجستير خريف 2019

			 

			أنا متخرج كلية تربية معلم صف

			ل أيمت فيي قدم ع مفاضلة الماجستير؟ 

'''
h='''يجب التواصل بهذا الخصوص مع منسق البرنامج الخاص بك عن طريق إرسال ايميل 

 

From: sajedah hejazy [mailto:damasrose94@gmail.com] 
Sent: Monday, July 22, 2019 11:54 AM
To: info <info@svuonline.org>
Subject: Re: [Website feedback] بخصوص استكمال التسجيل

 

شكرا ل ردك انا سجلت ب مفاضلة الخريف الماضي ...هل علي اعادة التسجيل
الكترونيا مع العلم انه حسابي ف الجامعه لقيته شغال واكتف هل اعيد التسجيل
الاكتروني ام فقط استكمل التسجيل وادفع الرسوم 

 

في الاثنين، ٢٢ يوليو، ٢٠١٩ ٩:٤١ ص، كتب info <info@svuonline.org
<mailto:info@svuonline.org> >:

	هل قمتي بالتسجيل على مفاضلة الربيع 2019؟ وما هي الأوراق التي لم
تقومي بتسليمها؟! 
	
	-----Original Message-----
	From: portal@svuonline.org <mailto:portal@svuonline.org>
[mailto:portal@svuonline.org <mailto:portal@svuonline.org> ] On Behalf
Of SVU
	Sent: Sunday, July 21, 2019 11:08 PM
	To: info@svuonline.org <mailto:info@svuonline.org> 
	Subject: [Website feedback] بخصوص استكمال التسجيل
	
	ساجدة حجازي (damasrose94@gmail.com
<mailto:damasrose94@gmail.com> ) sent a message using the contact form
at https://svuonline.org/en/node/120.
	
	تحية طيبة وبعد
	انا سجلت بالمفاضلة الااولى الكترونيا
	وطلعلي اعلام، وكنت ناوية استكمل التسجيل
	بس لاني ساكنة بمصر بعتت الورق عسوريا بس
	للاسف وصلوا بعد اخر يوم للتسجيل بيوم وكان التسجيل قد انتهى انا
محتارة هل استكمل خطوات التسجيل بتسليم الوررق او عيد التسجيل من اول جديد
وادخل المفاضلة.
	شكر جدا

'''
i= '''يمكنك التسجيل على المفاضلة المقبلة بالشهر الثالث
بحال كان المعدل الحاصلة عليه في الثانوية 50% وما فوق يمكنك التسجيل على
الإجازة بالإعلام أو إجازة بالحقوق 

 

From: رافي روري [mailto:rarore924@gmail.com] 
Sent: Sunday, February 03, 2019 12:50 PM
To: Info@svuonline.org
Subject: Re: مساعدة

 

 

في الأحد، ٣ فبراير ٢٠١٩ ٥:٤١ ص، كتب رافي روري <rarore924@gmail.com>:

	مرحبا 

	انا حاصلة على شهادة البكلوريا الادبي (قديمة )بمعدل 139 علامة 

	بحثت في موقع الجامعة عن امكانية التسجيل وفي اي فرع ولم استطع
الوصول هل بامكانكم المساعدة وشكرا 

'''
line_tokens = line_tokenize(re.sub('[\u202b\u200f\u202a\u202b]','',i))
# line_tokens = line_tokenize(document["content"])
regexp_tags = regexp_tagger.tag(line_tokens)
for rt in regexp_tags:
    print(rt)
print("***********************")
result = cp.parse(regexp_tags)
# result.pretty_print()
# result.draw()
a="-------- Original message --------"