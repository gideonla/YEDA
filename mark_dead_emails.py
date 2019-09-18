from google_sheets_handler import *
from format_email_body import *
from EmailBuilder import *
import argparse
import pdb
import time
from gspread import Cell


def parse_args():
    """"""
    desc = 'Delete dead email from google sheet'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-mshn', '--master_sheet_hash_number', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet hash number, found in the browser address line', required=1, dest='mshn')
    return parser.parse_args()


if __name__ == "__main__":
    start = time.time()
    args = parse_args()
    GS_master = GoogleSheets(args.mshn,
                             1)  # this object holds the google sheet for the master list (where all the company list live)
    email_coulmn =GS_master.col_num_map.get("emails")
    EMAIL = EmailBuilder()
    email_list = GS_master.get_emails()
    replied = GS_master.get_replied()
    replied.pop(0)
    email_list.pop(0)  # this is to skip the title of the coulmn
    replies_padding=['0']*(len(email_list)-len(replied))
    replied.extend(replies_padding)
    cell_list=[]
    for index in range(len(email_list)):
        #pdb.set_trace()
        if str2bool(replied[index]):
            continue
        if not any(c.isalpha() for c in email_list[index]):  # if email cell is empty then skip
            continue
        current_email_list=[x.lower() for x in email_list[index].split(",")]
        tmp_current_email_list =current_email_list

        for email_str in current_email_list:
            if "@" not in email_str:
                continue
            print(email_str)
            found = EMAIL.get_dead_email(email_str)
            #pdb.set_trace()
            live_emails=set(tmp_current_email_list).difference(found)
            tmp_current_email_list=list(live_emails)
            #print(tmp_current_email_list)
        #pdb.set_trace()
        live_emails = ','.join(tmp_current_email_list)
        cell_list.append(Cell(index+2,email_coulmn,live_emails))
        #pdb.set_trace()
    GS_master.wks.update_cells(cell_list)
    end = time.time()
    print(" Total run time: " + str(end - start) + " seconds")
