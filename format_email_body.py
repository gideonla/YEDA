import re

class FormatBody:
    def __init__(self, template_email, title="[TITLE]", last_name="[LAST_NAME]", pi_name="[PI_NAME]", company_name="[COMPANY_NAME]", tech_desc="[TECH_DESC]"):
        self.template_email = template_email
        self.title = title
        self.last_name = last_name
        self.pi_name = pi_name
        self.company_name = company_name
        self.tech_desc = tech_desc
        self.modified = open(self.template_email).read()
        self.modified = self.modified.replace("[TITLE]", self.title)
        self.modified = self.modified.replace("[LAST_NAME]", self.last_name)
        self.modified = self.modified.replace("[PI_NAME]", self.pi_name)
        self.modified = self.modified.replace("[TECH_DESC]", self.tech_desc)
        self.unmodified = self.modified

    def ends_with_s(self):
        last_character =self.company_name[-1:]
        if last_character.lower() =="s":
            return 0
        return 1
    def add_title(self,title):
        self.modified = self.modified.replace("[TITLE]",title)
    def add_company_name(self,company_name):
        self.company_name = company_name
        self.change_company_name()
    def change_last_name(self,last_name):
        self.modified = self.modified.replace("[LAST_NAME]",last_name)
    def change_pi_name(self,pi_name):
        self.modified = self.modified.replace("[PI_NAME]",pi_name)

    def change_company_name(self):
        if self.ends_with_s():
            self.company_name = self.company_name+"\'s"
        else:
            self.company_name = self.company_name + "\'"

        self.modified = self.modified.replace("[COMPANY_NAME]",self.company_name)


    def change_tech_desc(self,tech_desc):
        self.modified = self.modified.replace("[TECH_DESC]",tech_desc)


    def make_html(self):
        re.sub(' +', ' ', self.modified)
        self.modified = self.modified.replace("\n","<br>")
        return self.modified

    def init(self): #return template to starting status
        self.modified = self.unmodified

    def check_placeholders(self):
        """ Make sure that all the place holder strings are in place
                """
        if ( self.title=="" or self.last_name=="" or self.pi_name=="" or self.company_name=="" or self.tech_desc=="" ):
            raise ValueError('One of the place holder strings is empty')
        if (self.modified.find('[')>=0 or self.modified.find(']')>=0):
            raise ValueError('One of the place holders in the template email was not replaced')



if __name__ == "__main__":
    format_body=FormatBody("/home/gideon/YEDA/template_email",title="bla",last_name="bla1",pi_name="bla2",company_name="bla3s",tech_desc='bla4')
    format_body.check_placeholders()
    format_body.make_html()
    print (format_body.modified)