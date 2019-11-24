import argparse
import os
import pdb
from google_sheets_handler import *
import unidecode
from socket import *
import dns.resolver
import socket
import smtplib
from gspread.models import *



def eval_input(input:str):
    if os.path.isfile(input):
        with open(input) as f:
            lineList = f.readlines()
        return lineList
    else:
        return [input]

def parse_args():
    """"""
    desc = 'search for company eamils'
    parser = argparse.ArgumentParser(description = desc)

    parser.add_argument('-query', metavar='intel.com',
                        help='main query argument, can be either company domain or file with list of domains',
                        required=0, dest='query',type=str)

    parser.add_argument('-company_domain_mapping', metavar='1bM3hNok_drvXoOS4LvnyAvOcGoliQscNs7p59_ETUrU',
                        help='a google sheet with a map from company name to domain',
                        required=0, dest='company_domain_mapping', type=str)

    parser.add_argument('-google_sheet', metavar='02e8e18aa60c165820184fd59f39851154e1874e',
                        help='hash number of google sheet',
                        required=0, dest='google_sheet', type=str)

    return parser.parse_args()


class email_search:
    def __init__(self,query,google_sheet):
        self.query=query
        self.name_domain_dict={}
        self.email_template = {}
        self.GS=GoogleSheets(google_sheet, 0)
        self.names=[]


    def remove_accents(self,name):
        '''
        Remove special accents letter and replace with regular letters.
        :param name:
        :return: unaccented_string
        '''
        unaccented_string = unidecode.unidecode(name)
        return unaccented_string

    def clean_domain_name(self,domain):
        domain = domain.replace("http://", "")
        domain = domain.replace("https://", "")
        domain = re.sub("/.*", '', domain)
        domain=domain.rstrip('.')
        domain = domain.replace("www.", "")
        return domain

    def find_domain_from_company_name(self,name):
        row_num = self.GS.get_row_by_name(name)
        company = self.GS.companies[row_num-1]
        index=find_most_similar_item_in_list(company,self.companies)
        if index<0:
            ValueError("Did not find company name")
            return
        return self.domains[index]



    def clean_name(self,name):
        '''
        some name have weird characters that I need to clean out
        :param name:
        :return:
        '''
        name = re.sub(",.*",'',name)
        name = re.sub(" PhD",'',name)
        name = re.sub(" Ph.D.", '', name)
        name = re.sub("'",'', name)
        name = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", name)
        name = re.sub("\(",'', name)
        name = re.sub("\)", '', name)
        name = re.sub("'", '', name)
        return name

    def guess_emails_from_name(self,name,domain):
        '''
        rst_initial last	jdoe@celgene.com	36.2%
        first last	janedoe@celgene.com	24.9%
        last	doe@celgene.com	10.7%
        last first_initial	doej@celgene.com	9.6%
        first	jane@celgene.com	9.0%
        first last_initial	janed@celgene.com	9.0%
        first '-' last	jane-doe@celgene.com	0.6%
        :param name:
        :param domain:
        :return:
        '''
        domains=[]
        orig_name=name
        name=self.clean_name(name)
        first = re.sub(r'\s+', '',name.split(" ")[0])
        first = self.remove_accents(first)
        last="".join(name.split(" ")[1:])
        last = re.sub(r'\s+', '',last)
        last = self.remove_accents(last)
        if not first:
            print (name+" does not have first name, can't create email")
            return
        if not last:
            print (name+" does not have last name, can't create email")
            pdb.set_trace()
            return
        domains.append(first[0]+last+"@"+domain)
        domains.append(first+ last + "@" + domain)
        domains.append(last + "@" + domain)
        domains.append(last + first[0] + "@" + domain)
        domains.append(first + "@" + domain)
        domains.append(first+last[0] + "@" + domain)
        domains.append(first +"."+ last + "@" + domain)
        domains.append(first + "_" + last + "@" + domain)
        self.email_template.update( {orig_name: domains})

    #def check_email_address(self):


    def update_google_sheet_w_emails(self):
        cell_list=[]
        col = self.GS.col_num_map.get("emails")
        email_colmn =  self.GS.get_emails()
        name =  self.GS.get_first_names()
        email_colmn_padding = [''] * (len(name) - len(email_colmn))
        email_colmn.extend(email_colmn_padding)
        for key in self.email_template:
            print (key)
            row=find_most_similar_item_in_list(key, self.names)
            if email_colmn[row]: #if email exist then skip
                continue
            #pdb.set_trace()
            cell_list.append(Cell(row+2, col, ",".join(self.email_template.get(key))))
            pdb.set_trace()
        pdb.set_trace()
        self.GS.wks.update_cells(cell_list)




    def make_list_of_names_from_google_sheet(self):
        first_names=self.GS.get_first_names()
        first_names.pop(0)
        last_names = self.GS.get_last_names()
        last_names.pop(0)

        for index in range(0,len(first_names)):
            first=first_names[index].rstrip()
            last = last_names[index].rstrip()
            self.names.append(first+" "+last)


    def get_domain_by_name(self, name):
        #print(name)
        #pdb.set_trace()
        return self.name_domain_dict.get(name)



        #pdb.set_trace()

    def split_input_into_names_and_domains(self):
        with open(self.query) as f:
            for line in f:
                (key, val) = line.split("\|")
                self.name_domain_dict[key] = val.rstrip()

    def search_mutliple_queries(self):
        for key, value in self.name_domain_dict.items():
            self.search_email_by_name(key,value)

    def generate_emails(self):
        '''
        This function guesses the emails adress and add them to the google_sheet
        :return:
        '''
        # ES.split_input_into_names_and_domains()
        #pdb.set_trace()
        self.make_list_of_names_from_google_sheet()
        domain_list = self.GS.get_website()
        domain_list.pop(0)
        email_list = self.GS.get_emails()
        email_list.pop(0)
        email_list_padding = ['0'] * (len(self.names) - len(email_list))
        email_list.extend(email_list_padding)
        for index_name in range(0, len(self.names)):
            if "@" in email_list[index_name]:
                continue #if email address already there skip
            print (self.names[index_name].encode('utf-8'))
            domain = self.clean_domain_name(domain_list[index_name])
            self.guess_emails_from_name(self.names[index_name], domain)
            pdb.set_trace()

            # print(ES.email_template[name])

        ES.update_google_sheet_w_emails()

    def telnet_protocol(self,domain,email):
        # Get local server hostname
        host = socket.gethostname()

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(domain)
        server.helo(host)
        server.mail('me@domain.com')
        code, message = server.rcpt(str(email))
        #pdb.set_trace()
        server.quit()
        if code==250:
            return email
        else:
            return ''




    def check_emails(self):
        col = self.GS.col_num_map.get("emails")
        domain_list = self.GS.get_website()
        domain_list.pop(0)
        email_list = self.GS.get_emails()
        chosen_list = self.GS.get_chosen()
        chosen_list.pop(0)
        email_list.pop(0)
        name_list = self.GS.get_first_names()
        name_list.pop(0)
        last_name_list = self.GS.get_last_names()
        last_name_list.pop(0)
        for index_name in range(0, len(domain_list)):
            if not chosen_list[index_name]:
                continue
            domain = self.clean_domain_name(domain_list[index_name])
            answers = dns.resolver.query(domain, 'MX')
            new_domain = str(answers[0].exchange)
            emails=email_list[index_name].split(",")
            new_email=''
            for email in emails:
                #pdb.set_trace()
                new_email=new_email+","+self.telnet_protocol(new_domain,email)
            valid_email=False
            for char in new_email:
                if char.isalnum():
                    valid_email= True
                    self.GS.wks.update_cell(index_name + 2, col,new_email)
                    break
            if not valid_email:
                print (name_list[index_name],last_name_list[index_name],"does not have a valid email")

if __name__ == "__main__":
    args=parse_args()
    ES=email_search(args.query,args.google_sheet)
    ES.generate_emails()
    #ES.check_emails()


