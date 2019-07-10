import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import pdb
from difflib import SequenceMatcher
from collections import OrderedDict


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_most_similar_item_in_list(item,list):
    max_val=0.5
    max_position=-1
    for i in range(0,len(list)):
        if (similar(item, list[i]) > max_val):
            max_val=similar(item, list[i])
            max_position=i
    return max_position

class GoogleSheets:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('YEDA-7f7ce62ed162.json', SCOPES)
    gc = gspread.authorize(creds)
    

    def __init__(self, sheet_hash, master_list:bool):
        self.master_list=master_list
        self.wks = GoogleSheets.gc.open_by_key(sheet_hash).sheet1
        self.sheet_name=GoogleSheets.gc.open_by_key(sheet_hash).title
        self.map_col_header_to_col_num()
        self.counter=0

    def map_col_header_to_col_num(self):
        """ This function will map the header title numbers (e.g. "Company name")
            to a fixed order as specified in the variable "key_values".
            I assume that the title of the
            columns are the first row of the sheet
        """
        header_values = [x.lower() for x in self.wks.row_values(1)]
        key_values =[x.lower() for x in ["Company Name","title","first","Last Name","E-Mail","chosen","contacted","replied"]]
        c=[]
        #c=[i for i, item in enumerate(header_values) find_most_similar_item_in_list(item.lower(),key_values)]
        for item in key_values:
            c.append(find_most_similar_item_in_list(item.lower(),header_values))
        try:
            self.companies = self.wks.col_values(c[0]+1)
        except:
            sys.exit("google sheet -"+self.sheet_name+"- does not have \"companies\" column")
        try:
            self.titles = self.wks.col_values(c[1]+1)
        except:
            sys.exit("google sheet -"+self.sheet_name+"- does not have \"titles\" column")
        try:
            self.first_name= self.wks.col_values(c[2]+1)
        except:
            sys.exit("google sheet -"+self.sheet_name+"- does not have \"first name\" column")
        try:
            self.last_names = self.wks.col_values(c[3]+1)
        except:
            sys.exit("google sheet -"+self.sheet_name+"- does not have \"last names\" column")
        try:
            self.emails = self.wks.col_values(c[4]+1)
        except:
            sys.exit("google sheet -"+self.sheet_name+"- does not have \"emails\" column")
        try:
            self.chosen = self.wks.col_values(c[5]+1)
        except:
            sys.exit("google sheet -"+self.sheet_name+"- does not have \"chosen\" column")
        if self.master_list:
            try:
                self.contacted = self.wks.col_values(c[6] + 1)
            except:
                sys.exit("google sheet -"+self.sheet_name+"- does not have \"contacted\" column")
            try:
                self.replied = self.wks.col_values(c[7] + 1)
            except:
                sys.exit("google sheet -"+self.sheet_name+"- does not have \"replied\" column")




    def get_company_names(self):
        return self.companies

    def get_last_names(self):
        return self.last_names

    def get_titles(self):
        return self.titles

    def get_emails(self):
        return self.emails

    def get_chosen(self):
        return self.chosen

    def iterate_sheet(self):
        while self.counter<len(self.chosen):
            if self.chosen[self.counter] == '1':
                self.counter = self.counter + 1
                return  self.get_company_names()[self.counter-1], self.get_last_names()[self.counter-1],self.get_titles()[self.counter-1],self.get_emails()[self.counter-1]

            self.counter=self.counter+1

    def number_of_chosen_emails(self):
        return self.chosen.count("1")







if __name__ == "__main__":
    google_sheet = sys.argv[1]
   # # wks = gc.open('Companies to interest in technology').sheet1
    GS = GoogleSheets(google_sheet)
   #
   # # for num, c in enumerate(GS.get_chosen(), start=0):
   #  #    if c=='1':
   #   #       print("{},{},{},{},{}".format(num,GS.get_company_names()[num],GS.get_last_names()[num],GS.get_titles()[num],GS.get_emails()[num]))
   #  print (GS.number_of_chosen_emails())
   #  for i in range(GS.number_of_chosen_emails()):
   #      print (GS.iterate_sheet())
    print (GS.emails)
