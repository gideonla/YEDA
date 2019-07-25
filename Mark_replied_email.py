from google_sheets_handler import *
from format_email_body import *
from EmailBuilder import *
import argparse
import pdb
import time



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
    EMAIL=EmailBuilder()
    email_list=GS_master.get_emails()
    email_list.pop(0)
    for email in email_list:
        print (email)
        if email=="":
            continue
        found=EMAIL.search_inbox(email)
        if found:
            print (email)
            GS_master.update_replied(email)
    end = time.time()
    print(" Total run time: "+end - start+" seconds")
