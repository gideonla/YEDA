import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import pdb
from difflib import SequenceMatcher
from collections import OrderedDict
import re
import time
import colorama
from colorama import Fore, Style
import warnings



def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', ''):
        return False
    else:
        raise ValueError('Boolean value expected.')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_most_similar_item_in_list(item,list,max_val=0.5):
    max_position=-1
    for i in range(0,len(list)):
        if (similar(item, list[i]) > max_val):
            max_val=similar(item, list[i])
            max_position=i
    #print (list[max_position])
    #print (max_val)
    return max_position

class GoogleSheets:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/gideon/YEDA/YEDA-7f7ce62ed162.json', SCOPES)
    gc = gspread.authorize(creds)


    def __init__(self, sheet_hash, master_list:bool=0, general_WS:bool=0):
        self.c = [] #this list will map bewtween names and the current sheet coulmn values
        self.general_WS = general_WS  # general WS means that this is not a "companies WKS"
        self.master_list=master_list
        self.wks = GoogleSheets.gc.open_by_key(sheet_hash).sheet1
        self.sheet_name=GoogleSheets.gc.open_by_key(sheet_hash).title
        self.map_col_header_to_col_num()
        self.counter=0


    def get_row_by_name(self,name):
        temp_names=[]
        for index,fname in enumerate(self.first_name):
            temp_name=self.first_name[index]+" "+self.last_names[index]
            temp_names.append(temp_name)
        return find_most_similar_item_in_list(name,temp_names)+1 # the plus 1 is becuase cells in google sheets atart at 1 and not 0

    def update_emails(self,row_num,emails):
        #pdb.set_trace()
        current_cell_value= self.wks.cell(row_num, self.c[4]+1).value
        self.wks.update_cell(row_num, self.c[4]+1, current_cell_value+","+",".join(emails))

    def get_coulmn_number_by_value(self,value):
        header_values = [x.lower() for x in self.wks.row_values(1)]
        index=find_most_similar_item_in_list(value.lower(), header_values)
        return index+1



    def map_col_header_to_col_num(self):
        """ This function will map the header title numbers (e.g. "Company name")
            to a fixed order as specified in the variable "key_values".
            I assume that the title of the
            columns are the first row of the sheet
        """
        if self.general_WS:
            return
        self.col_num_map={}
        header_values = [x.lower() for x in self.wks.row_values(1)]
        key_values =[x.lower() for x in ["Company Name","title","first","Last Name","E-Mail","chosen","contacted","replied","linkedin","website","results", "Date contacted"]]
        #c=[i for i, item in enumerate(header_values) find_most_similar_item_in_list(item.lower(),key_values)]
        for item in key_values:
            self.c.append(find_most_similar_item_in_list(item.lower(),header_values))
        try:
            self.date_contacted = self.wks.col_values(self.c[11]+1)
            self.col_num_map.update({'Date contacted': self.c[11]+1})
        except:
            warnings.warn("google sheet -"+self.sheet_name+"- does not have 'Date contacted' column")
        try:
            self.results = self.wks.col_values(self.c[10]+1)
            self.col_num_map.update({'results': self.c[10]+1})
        except:
            warnings.warn("google sheet -"+self.sheet_name+"- does not have 'results' column")

        try:
            self.website = self.wks.col_values(self.c[9]+1)
            self.col_num_map.update({'website': self.c[9]+1})
        except:
            warnings.warn("google sheet -"+self.sheet_name+"- does not have 'website' column")

        try:
            self.companies = self.wks.col_values(self.c[0]+1)
            self.col_num_map.update({'companies': self.c[0]+1})
        except:
            warnings.warn("google sheet -"+self.sheet_name+"- does not have 'companies' column")
        try:
                self.linkedin = self.wks.col_values(self.c[8] + 1)
                self.col_num_map.update({'linkedin': self.c[8] + 1})
        except:
                warnings.warn("google sheet -" + self.sheet_name + "- does not have 'linkedin' column")
        try:
            self.titles = self.wks.col_values(self.c[1]+1)
            self.col_num_map.update({'titles': self.c[1] + 1})
        except:
            warnings.warn("google sheet -"+self.sheet_name+"- does not have 'titles' column")
        try:
            self.first_name= self.wks.col_values(self.c[2]+1)
            self.col_num_map.update({'first_name': self.c[2] + 1})
        except:
            warnings.warn("google sheet -"+self.sheet_name+"- does not have 'first name' column")
        try:
            self.last_names = self.wks.col_values(self.c[3]+1)
            self.col_num_map.update({'last_names': self.c[3] + 1})
        except:
            warnings.warn("google sheet -"+self.sheet_name+"- does not have 'last names' column")
        try:
            self.emails = self.wks.col_values(self.c[4]+1)
            self.col_num_map.update({'emails': self.c[4] + 1})

        except:
            warnings.warn("google sheet -"+self.sheet_name+"- does not have 'emails' column")
        try:
            self.chosen = self.wks.col_values(self.c[5]+1)
            self.col_num_map.update({'chosen': self.c[5] + 1})
        except:
            if not self.master_list:
                warnings.warn("google sheet -"+self.sheet_name+"- does not have 'chosen' column")
        if self.master_list:
            try:
                self.contacted = self.wks.col_values(self.c[6] + 1)
                self.col_num_map.update({'contacted': self.c[6] + 1})
            except:
                warnings.warn("google sheet -"+self.sheet_name+"- does not have 'contacted' column")
            try:
                self.replied = self.wks.col_values(self.c[7] + 1)
                self.col_num_map.update({'replied': self.c[7] + 1})
            except:
                warnings.warn("google sheet -"+self.sheet_name+"- does not have 'replied' column")




    def update_contacted(self,email):
        if not email:
            return
        if not self.master_list:
            return
        email_re = re.compile(email, re.IGNORECASE)
        try:
            cell = self.wks.find(email_re)
        except gspread.exceptions.CellNotFound:
            print (Fore.RED +"Could not find "+email+" in '" +self.sheet_name+"'" )
            print(Style.RESET_ALL)
            return
        print(cell.row)
        print(email)
        # pdb.set_trace()
        self.wks.update_cell(cell.row,self.c[6]+1,1)

    def update_replied(self,email:str):
        """
        Given a cell numner in a google sheet it will mark the cell with '1'
        The purpose of this is to let me know that this person has replied to my email
        :param cell_num:
        :return: null
        """
        cell = self.wks.find(email)
        print (cell.row)
        print (email)
        #pdb.set_trace()

        self.wks.update_cell(cell.row,self.c[7]+1,1)

    def get_results(self):#results is a coulmn with the number of hits I get searching the company webbsite with the relevant keywords
        return self.results

    def get_company_names(self):
        return self.companies

    def get_last_names(self):
        return self.last_names

    def get_linkedin(self):
        return self.linkedin

    def get_website(self):
        return self.website

    def get_first_names(self):
        return self.first_name

    def get_titles(self):
        return self.titles

    def get_emails(self):
        return self.emails

    def get_contacted(self):
        return self.contacted

    def get_chosen(self):
        return self.chosen

    def get_replied(self):
        return self.replied

    def check_if_replied(self,email):
        for i, item in enumerate(self.emails):
            if (item==email):
                break
        try:
            return str2bool(self.replied[i])
        except IndexError: #if the coulmn has no values the length of the coulmn is 0. in this case I am assuming that the values are false
            return False

    def iterate_sheet(self):
        while self.counter<len(self.chosen):
            if self.chosen[self.counter] == '1':
                self.counter = self.counter + 1
                return  self.get_company_names()[self.counter-1], self.get_last_names()[self.counter-1],self.get_titles()[self.counter-1],self.get_emails()[self.counter-1],self.get_first_names()[self.counter-1]

            self.counter=self.counter+1

    def number_of_chosen_emails(self):
        if self.chosen.count("1")<1:
            raise Exception('No emails were chosen to send')
            return
        return self.chosen.count("1")

    def remove_redundant_entries(self):
        """
         Goes over the google sheet and removes double entries;
         keeping the row with more data
         :return: null
        """
        all_index_list=[]
        tmp_sheet = self.wks.get_all_values()
        for i in self.emails:
            email_re= re.compile(i, re.IGNORECASE)
            index_list=[]
            # pdb.set_trace()
            for index,j in enumerate(self.emails):
                if bool(re.search(email_re,j)):
                    index_list.append(index)
            if len(index_list)>1:
                print(i)
                double_emails=[]
                for email_row in index_list:
                    double_emails.append(tmp_sheet[email_row])
                #print(index_list)
                ind=max(enumerate(double_emails), key=lambda x: len(x[1]))[0]
                index_list.pop(ind)
                #print(index_list)
                all_index_list.append(index_list)
        flat_all_index_list=[item for sublist in all_index_list for item in sublist]
        s=set(flat_all_index_list)
        flat_all_index_list=list(s)
        flat_all_index_list.sort()
        print(flat_all_index_list)
        for i,val in enumerate(flat_all_index_list):
            self.wks.delete_row(val-i+1)


if __name__ == "__main__":
    google_sheet = sys.argv[1]
    # # wks = gc.open('Companies to interest in technology').sheet1
    GS = GoogleSheets(google_sheet,1)
    #
    # # for num, c in enumerate(GS.get_chosen(), start=0):
    #  #    if c=='1':
    #   #       print("{},{},{},{},{}".format(num,GS.get_company_names()[num],GS.get_last_names()[num],GS.get_titles()[num],GS.get_emails()[num]))
    #  print (GS.number_of_chosen_emails())
    #  for i in range(GS.number_of_chosen_emails()):
    #      print (GS.iterate_sheet())
    GS.remove_redundant_entries()
