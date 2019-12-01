import re
import codecs
from utils import *


class FormatBody:
    def __init__(self, template_email, title="", last_name="", pi_name="",
                 company_name="", tech_desc=""):
        self.template_email = template_email
        self.title = title
        self.last_name = last_name
        self.pi_name = pi_name
        self.company_name = company_name
        self.tech_desc = tech_desc
        self.modified = codecs.open(self.template_email, encoding="utf-8").read()
        if not (title==""):
            self.modified = self.modified.replace("[TITLE]", self.title)
        if not (last_name == ""):
            self.modified = self.modified.replace("[LAST_NAME]", self.last_name)
        if not (pi_name == ""):
            self.modified = self.modified.replace("[PI_NAME]", self.pi_name)
        if not (tech_desc == ""):
            self.modified = self.modified.replace("[TECH_DESC]", self.tech_desc)
        self.unmodified = self.modified

    def ends_with_s(self):
        last_character = self.company_name[-1:]
        if last_character.lower() == "s":
            return 0
        return 1

    def add_title(self, title):
        self.title=title
        self.modified = self.modified.replace("[TITLE]", title)

    def add_email(self, email):
        self.modified = self.modified.replace("[EMAIL]", email)

    def add_company_name(self, company_name):
        self.company_name = company_name
        self.company_name = clean_company_name(company_name)
        self.change_company_name()

    def change_last_name(self, last_name):
        self.last_name = last_name
        self.modified = self.modified.replace("[LAST_NAME]", last_name)

    def change_pi_name(self, pi_name):
        self.pi_name = pi_name
        self.modified = self.modified.replace("[PI_NAME]", pi_name)

    def change_first_name(self, first_name):
        self.modified = self.modified.replace("[FIRST_NAME]", first_name)

    def change_company_name(self):
        self.modified = self.modified.replace("[COMPANY_NAME]", self.company_name)

    def change_tech_desc(self, tech_desc):
        self.tech_desc = tech_desc
        self.modified = self.modified.replace("[TECH_DESC]", tech_desc)

    def make_html(self):
        re.sub(' +', ' ', self.modified)
        self.modified = self.modified.replace("\n", "<br>")
        return self.modified

    def get_body(self):
        re.sub(' +', ' ', self.modified)
        return self.modified

    def init(self):  # return template to starting status
        self.modified = self.unmodified

    def check_placeholders(self):
        """ Make sure that all the place holder strings are in place
                """
        if (
                self.title == "" or self.last_name == "" or self.pi_name == "" or self.company_name == "" or self.tech_desc == ""):
            raise ValueError('One of the place holder strings is empty')
        # print (self.modified.encode(encoding='UTF-8'))
        pdb.set_trace()
        if self.modified.find('[TITLE]') >= 0:
            raise ValueError('TITLE place holder in the template email was not replaced')
        if self.modified.find('[LAST_NAME]') >= 0:
            raise ValueError('LAST_NAME place holder in the template email was not replaced')
        if self.modified.find('[PI_NAME]') >= 0:
            raise ValueError('PI_NAME place holder in the template email was not replaced')
        if self.modified.find('[COMPANY_NAME]') >= 0:
            raise ValueError('COMPANY_NAME place holder in the template email was not replaced')
        if self.modified.find('[TECH_DESC]') >= 0:
            raise ValueError('TECH_DESC place holder in the template email was not replaced')


if __name__ == "__main__":
    format_body = FormatBody("/home/gideon/YEDA/template_email", title="bla", last_name="bla1", pi_name="bla2",
                             company_name="bla3s", tech_desc='bla4')
    format_body.check_placeholders()
    format_body.make_html()
    print(format_body.modified)
