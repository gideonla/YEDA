from google_sheets_handler import *
from format_email_body import *
from EmailBuilder import *
import argparse
import pdb
import time
from gspread import Cell



def parse_args():
    """"""
    desc = 'Will search inbox'
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('-mshn','--master_sheet_hash_number', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet hash number, found in the browser address line', required=1,dest='mshn')
    return parser.parse_args()

if __name__ == "__main__":
    start = time.time()
    args = parse_args()
    GS_master = GoogleSheets(args.mshn,
                             1)  # this object holds the google sheet for the master list (where all the company list live)
    EMAIL = EmailBuilder()
    email_list = GS_master.get_emails()
    replied = GS_master.get_replied()
    replied_coulmn = GS_master.col_num_map.get("replied")
    replied.pop(0)
    email_list.pop(0)  # this is to skip the title of the coulmn
    contacted_padding = ['0'] * (len(email_list) - len(replied))
    replied.extend(contacted_padding)
    found = False
    cell_list = []
    for index in range(len(email_list)):
        print(index)
        # pdb.set_trace()
        if str2bool(replied[index]):
            continue
        if not any(c.isalpha() for c in email_list[index]):  # if email cell is empty then skip
            continue
        for email_str in email_list[index].split(","):
            if "@" not in email_str:
                continue
            found = EMAIL.search_inbox(email_str) or found
            #pdb.set_trace()
        if found:
            print(email_str)
        cell_list.append(Cell(index + 2, replied_coulmn, int(found)))
        found=False
    pdb.set_trace()
    GS_master.wks.update_cells(cell_list)
    end = time.time()
    print(" Total run time: " + str(end - start) + " seconds")
