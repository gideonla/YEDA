from O365 import Account, FileSystemTokenBackend
from format_email_body import *
import pdb
class EmailBuilder:
    credentials = ('4dca8325-3be8-42aa-80d8-be291da5c1ea', 'myewtg3_3tbls-fq?0?whRJGfdLyO65b')
    token_backend = FileSystemTokenBackend(token_path='/home/gideon/YEDA', token_filename='o365_token.txt')
    account = Account(credentials, token_backend=token_backend)

    def __init__(self, to_email=None,cc=None,bcc=None,subject=None, body=None, attachments=None):
        self.message = self.account.new_message()
        self.message.subject =subject
        self.message.to.add(to_email)
        self.message.cc.add(cc)
        self.message.bcc.add(bcc)
        self.message.body = body
        self.attach(attachments)


    def set_subject(self,subject):
        self.message.subject=subject

    def set_to(self,to):
        self.message.to.add(to)

    def set_body(self,body):
        self.message.body = body

    def send(self):
        self.message.send()

    def save_draft(self):
        self.message.save_draft()

    def attach(self,attachments:list ):
        if not attachments:
            return
        for i in attachments:
            self.message.attachments.add(i)

    def search_inbox(self,email:str ):
        mailbox = self.account.mailbox()

        inbox = mailbox.inbox_folder()
        query = inbox.new_query()

        query=query.on_attribute('from').contains(email)
        messages = inbox.get_messages(limit=25, query=query)

        for message in messages:
            #pdb.set_trace()
            i=(message.sender.address)
            if i :
                return True
        return False

    def search_sent(self,email:str ):
        mailbox = self.account.mailbox()

        sent = mailbox.sent_folder()
        query = sent.new_query()

        query = sent.q().search(email)
        messages = sent.get_messages(limit=25, query=query)
        #pdb.set_trace()
        for message in messages:
            if (message.to[0].address):
                return True
        return False


if __name__ == "__main__":
    #format_body = FormatBody("/home/gideon/YEDA/template_email", title="bla", last_name="bla1", pi_name="bla2",
    #                         company_name="bla3s", tech_desc='bla4')
    #n = EmailBuilder(to_email="glapidoth@gmail.com",bcc="gideon.lapidoth@weizmann.ac.il",subject="NEW",body=format_body.make_html(),attachments=["/home/gideon/YEDA/varified_emails2"])
    #pdb.set_trace()
    #n.send()
    email = EmailBuilder()
    if email.search_sent("james@ingredientech.com"):
        print ("yes")


