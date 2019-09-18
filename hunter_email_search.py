from pyhunter import PyHunter
import argparse
import os
import pdb
from google_sheets_handler import *


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

    parser.add_argument('-company_domain_mapping', metavar='02e8e18aa60c165820184fd59f39851154e1874e',
                        help='a google sheet with a map from company name to domain',
                        required=0, dest='company_domain_mapping', type=str)

    parser.add_argument('-google_sheet', metavar='02e8e18aa60c165820184fd59f39851154e1874e',
                        help='hash number of google sheet',
                        required=0, dest='google_sheet', type=str)

    return parser.parse_args()


class email_search:
    def __init__(self,query,google_sheet,google_sheet_domain_map=""):
        self.query=query
        self.hunter = PyHunter('02e8e18aa60c165820184fd59f39851154e1874e')
        self.name_domain_dict={}
        self.email_template = {}
        self.GS=GoogleSheets(google_sheet, 0)
        self.GSDM = GoogleSheets(google_sheet_domain_map, general_WS=1)
        if self.GSDM:
            self.companies = self.GSDM.wks.col_values(2)
            self.domains = self.GSDM.wks.col_values(1)

    def get_patterns_using_hunter(self,single_query):
        pattern=self.hunter.domain_search(single_query)["pattern"]
        pdb.set_trace()
        print (single_query,pattern)

    def find_domain_from_company_name(self,name):
        row_num = self.GS.get_row_by_name(name)
        company = self.GS.companies[row_num-1]
        index=find_most_similar_item_in_list(company,self.companies)
        if index<0:
            ValueError("Did not find company name")
            return
        return self.domains[index]

    def get_patterns_using_hunter(self,single_query):
        pattern=self.hunter.domain_search(single_query)["pattern"]
        pdb.set_trace()
        print (single_query,pattern)

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
        first = re.sub(r'\s+', '',name.split(" ")[0])
        last = re.sub(r'\s+', '',name.split(" ")[1])
        domains.append(first[0]+last+"@"+domain)
        domains.append(first+ last + "@" + domain)
        domains.append(last + "@" + domain)
        domains.append(last + first[0] + "@" + domain)
        domains.append(first + "@" + domain)
        domains.append(first+last[0] + "@" + domain)
        domains.append(first +"."+ last + "@" + domain)
        domains.append(first + "_" + last + "@" + domain)
        self.email_template.update( {name: domains})

    def update_google_sheet_w_emails(self,name):
        row_num=self.GS.get_row_by_name(name)
        emails=self.email_template.get(name)
        #pdb.set_trace()
        self.GS.update_emails(row_num,emails)

    def make_list_of_names_from_google_sheet(self):
        first_names=self.GS.get_first_names()
        last_names = self.GS.get_last_names()
        names=[]
        for index in range(0,len(first_names)):
            first=first_names[index].rstrip()
            last = last_names[index].rstrip()
            names.append(first+" "+last)
        return names

    def get_domain_by_name(self, name):
        #print(name)
        #pdb.set_trace()
        return self.name_domain_dict.get(name)

    def search_hunter_email_by_name(self,name,domain):
        print(name)
        pdb.set_trace()
        first=name.split(" ")[0]
        last = name.split(" ")[1]
        email, confidence_score = self.hunter.email_finder(domain, first_name=first, last_name=last)
        print (name, email, confidence_score)

        #pdb.set_trace()

    def split_input_into_names_and_domains(self):
        with open(self.query) as f:
            for line in f:
                (key, val) = line.split("\|")
                self.name_domain_dict[key] = val.rstrip()

    def search_mutliple_queries(self):
        for key, value in self.name_domain_dict.items():
            self.search_email_by_name(key,value)



if __name__ == "__main__":
    args=parse_args()
    ES=email_search(args.query,args.google_sheet,args.company_domain_mapping)

    #ES.split_input_into_names_and_domains()
    names=ES.make_list_of_names_from_google_sheet()
    for name in names:
        domain=""
        try:
            domain=ES.find_domain_from_company_name(name)
        except:
            print ("did not find domain for: "+name)
            continue
        if not domain:
            print("did not find domain for: " + name)
            continue
        #pdb.set_trace()
        ES.guess_emails_from_name(name, domain)
        ES.update_google_sheet_w_emails(name)
