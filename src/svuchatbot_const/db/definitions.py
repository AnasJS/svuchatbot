class Definitions :
    #DB
    PSTDBNAME = "PST"
    PARSSEDEMAILSDBNAME = "SVU"
    FAILEDPARSSEDEMAILSDBNAME = "SVU_Failed"
    TFIDFDBNAME = "TF-IDF"
    WEIGHTSDBNAME = "Weights"
    BAGOFWORDSDBNAME = "Bag-Of-Words"
    PATTERNSDBNAME = "Patterns"
    ANALYSIS = "Analysis"



    #Collections
    SENTCOLLECTIONNAME = "Sent"
    PARSSEDEMAILSCOLLECTIONNAME = "Sent-Mails-After-Parsing"
    FAILEDPARSSEDEMAILSCOLLECTIONNAME = "Sent-Mails-Failed-Parsing"
    PATTERNSCOLLECTIONNAME = "1-Gram"
    PATTERNSFREQUENCYCOLLECTIONNAME = "PatternsFrequency"
    BAGOFWORDSCOLLECTIONNAME1GRAM = "1-Gram"
    BAGOFWORDSCOLLECTIONNAME2GRAM = "2-Gram"
    BAGOFWORDSCOLLECTIONNAME3GRAM = "3-Gram"
    BAGOFWORDSCOLLECTIONNAME4GRAM = "4-Gram"
    BAGOFWORDSCOLLECTIONNAME5GRAM = "5-Gram"
    AnalysisCollection = "analysis"


    #Fields
    TOKENSFIELDNAME = "tokens"
    SIMPLETOKENSFIELDNAME = "simple-tokens"
    QUESTIONSIMPLETOKENSFIELDNAME = "question-simple-tokens"
    ANSWERSIMPLETOKENSFIELDNAME = "answer-simple-tokens"
    QUESTIONFIELDNAME = "body"
    ANSWERFIELDNAME = "replay-message"
    SPECIALWORDSFIELDNAME = "special-words"
    SPECIALWORDSFIELDNAMEFROMQUESTION = "special-words-question"
    SPECIALWORDSFIELDNAMEFROMANSWER = "special-words-answer"
    count_non_arabic_questions = "count_non_arabic_questions"
    count_non_arabic_answers = "count_non_arabic_answers"
    count_corona_emails = "count_corona_emails"
    count_duplicated_questions = "count_duplicated_questions"
    count_forwarded_emails = "count_forwarded_emails"
    count_empty_questions = "count_empty_questions"
    count_emails_contain_question_in_replay = "count_emails_contain_question_in_replay"
    content_field_name = "content"
