from svuchatbot_mogodb.client import get_collection
import numpy as np

def add_tag(source=("chatbot", "PatternsFrequency"), mails=("chatbot", "Mails-3")):
    col_name, db_name = source
    col = get_collection(col_name, db_name)
    # *********************************************************************************
    documents = list(col.find())
    p_tags = set([item["pos_pattern_frequency"] for item in documents])
    print(f'pos tags : {len(p_tags)}')
    l_tags = set([item["lex_pattern_frequency"] for item in documents])
    print(f'lex tags : {len(l_tags)}')
    r_tags = set([item["root_pattern_frequency"] for item in documents])
    print(f'root tags : {len(r_tags)}')
    t_tags = set([item["token_pattern_frequency"] for item in documents])
    print(f'token tags : {len(t_tags)}')
    lex_root_tags = set([(
        # item["pos_pattern_frequency"],
        item["lex_pattern_frequency"],
        item["root_pattern_frequency"],
        # item["token_pattern_frequency"]
                     ) for item in documents])
    print(f'lex root tags : {len(lex_root_tags)}')
    p_t_tags = set([(
        item["pos_pattern_frequency"],
        # item["lex_pattern_frequency"],
        # item["root_pattern_frequency"],
        item["token_pattern_frequency"]
                     ) for item in documents])
    print(f'pos token tags : {len(p_t_tags)}')
    p_r_tags = set([(
        item["pos_pattern_frequency"],
        # item["lex_pattern_frequency"],
        item["root_pattern_frequency"],
        # item["token_pattern_frequency"]
                     ) for item in documents])
    print(f'pos root tags : {len(p_r_tags)}')
    p_l_tags = set([(
        item["pos_pattern_frequency"],
        item["lex_pattern_frequency"],
        # item["root_pattern_frequency"],
        # item["token_pattern_frequency"]
                     ) for item in documents])
    print(f'pos lex tags : {len(p_l_tags)}')
    l_t_tags = set([(
        # item["pos_pattern_frequency"],
        item["lex_pattern_frequency"],
        # item["root_pattern_frequency"],
        item["token_pattern_frequency"]
                     ) for item in documents])
    print(f'lex token tags : {len(l_t_tags)}')
    r_t_tags = set([(
        # item["pos_pattern_frequency"],
        # item["lex_pattern_frequency"],
        item["root_pattern_frequency"],
        item["token_pattern_frequency"]
                     ) for item in documents])
    print(f'root token tags : {len(r_t_tags)}')
    all_tags = set([(
        item["pos_pattern_frequency"],
        item["lex_pattern_frequency"],
        item["root_pattern_frequency"],
        item["token_pattern_frequency"]
                     ) for item in documents])
    print(f'all tags : {len(all_tags)}')
    tags = ["pos", "lex", "root", "token"]
    all_argmax_tags = set([
        (
            tags[np.argmax((
        item["pos_pattern_frequency"],
        item["lex_pattern_frequency"],
        item["root_pattern_frequency"],
        item["token_pattern_frequency"]
                     ))],
         np.max((
             item["pos_pattern_frequency"],
             item["lex_pattern_frequency"],
             item["root_pattern_frequency"],
             item["token_pattern_frequency"]
         ))
        )for item in documents])
    print(f'all_argmax_tags tags : {sorted(all_argmax_tags)}')
    # **********************************************************************************
    cursor = col.find()
    for item in cursor:
        item.update({"tag":    (
            str(np.max((
        item["pos_pattern_frequency"],
        item["lex_pattern_frequency"],
        item["root_pattern_frequency"],
        item["token_pattern_frequency"]
                     ))),
         tags[np.argmax((
             item["pos_pattern_frequency"],
             item["lex_pattern_frequency"],
             item["root_pattern_frequency"],
             item["token_pattern_frequency"]
         ))] )})
        col.replace_one({"_id": item["_id"]}, item)

    # **********************************************************************************
    # target = ("ClustersMails", "1-Gram")
    # mails = ("chatbot", "Mails-3")
    m_col = get_collection(mails[0], mails[1])
    # t_col = get_collection(target[0], target[1])
    for item in m_col.find():
        item.update({"tag": None})
        m_col.replace_one({"_id": item["_id"]}, item)
        try:
            email_id = item["_id"]
            # print(email_id)
            rows_tags = [tuple(r["tag"]) for r in col.find({"email_id": email_id},{"tag":1})]
            # print(rows_tags)
            max_tag = max(rows_tags)
            item.update({"tag": max_tag})
            m_col.replace_one({"_id": item["_id"]}, item)
        except Exception as e:
            print(item["_id"], e)
