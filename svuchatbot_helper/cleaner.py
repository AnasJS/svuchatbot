import re
import os


class StringCleaner:
    def __init__(self, text):
        self.text = text

    def drop_new_line(self):
        self.text = re.sub(os.linesep, " ", self.text)
        self.text = re.sub("\r\n", " ", self.text)
        self.text = re.sub("\n", " ", self.text)
        self.text = re.sub("\t", " ", self.text)
        return self

    def drop_special_characters(self):
        self.text = re.sub(r"[-._!#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]", " ", self.text)
        return self

    def drop_special_word(self, word):
        self.text = re.sub(word, " ", self.text)
        return self

    def drop_meta_data_of_message(self):
        self.text = re.sub(
            ".+\@[a-z]+.[a-z]+\) sent a message using the contact form at https://svuonline.org/en/contact-us.",
            " ", self.text)
        self.text = re.sub("تم الإرسال من .*\r?\n?.*", " ", self.text)
        return self

    def drop_many_spaces(self):
        self.text = re.sub(" {2,}", " ", self.text)
        return self
