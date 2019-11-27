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
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-mshn', '--master_sheet_hash_number', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet hash number, found in the browser address line', required=1, dest='mshn')
    parser.add_argument('-Yeda_num', metavar='1633', help='The YEDA reference number', required=0, dest='Yeda_num',default="")

    return parser.parse_args()


if __name__ == "__main__":
    start = time.time()
    args = parse_args()
    GS_master = GoogleSheets(args.mshn,
                             1)  # this object holds the google sheet for the master list (where all the company list live)

    EMAIL = EmailBuilder()
    email_list = GS_master.get_emails()
    contacted = GS_master.get_contacted()
    contacted_date_coulmn = GS_master.col_num_map.get("Date contacted")
    contacted_coulmn = GS_master.col_num_map.get("contacted")
    contacted.pop(0)
    email_list.pop(0)  # this is to skip the title of the coulmn
    contacted_padding = ['0'] * (len(email_list) - len(contacted))
    contacted.extend(contacted_padding)
    found=False
    cell_list,cell_list_dates = [],[]

    for index in range(len(email_list)):
        print (index)
        #pdb.set_trace()
        if str2bool(contacted[index]):
            continue
        if not any(c.isalpha() for c in email_list[index]):  # if email cell is empty then skip
            continue
        for email_str in email_list[index].split(","):
            if "@" not in email_str:
                continue
            found = EMAIL.search_sent(email_str,args.Yeda_num) or found
        #pdb.set_trace()
        if found:
            pdb.set_trace()
            #print(email_str)
            cell_list.append(Cell(index + 2, contacted_coulmn, 1))
            cell_list_dates.append(Cell(index + 2, contacted_date_coulmn, found))
        else:
            cell_list.append(Cell(index + 2, contacted_coulmn, 0))
        found = False
    #pdb.set_trace()
    GS_master.wks.update_cells(cell_list)
    end = time.time()
    print(" Total run time: " + str(end - start) + " seconds")
