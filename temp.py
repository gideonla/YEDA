from google_sheets_handler import *
from format_email_body import *
from EmailBuilder import *
import argparse
import pdb

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_args():
    """"""
    desc = 'Automatically send emails using google sheets as a database'
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('-cshn','--company_sheet_hash_number', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet of the companies to send email hash number, found in the browser address line', required=1,dest='cshn')
    parser.add_argument('-mshn','--master_sheet_hash_number', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet hash number, found in the browser address line', required=1)
    parser.add_argument('-email_message_template', help='Path to email template text file',required=1)
    parser.add_argument('-pi_name', help='Name of PI', required=1)
    parser.add_argument('-desc', help='Description of technology', required=1)
    parser.add_argument('-cc', help='Who to send cc email to', default="jacob.fierer@weizmann.ac.il")
    parser.add_argument('-bcc', help='Who to send bcc email to', default="magic.yeda@weizmann.ac.il")
    parser.add_argument('-email_subject', help='Email subject line', default="",required=1)
    parser.add_argument('-attachments', nargs='+', help='list of files to attach to email')
    parser.add_argument("--send", type=str2bool, nargs='?',const=True, default=False, help="If false save email to drafts and don't send")





    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    GS = GoogleSheets(args.cshn,0) #create the google sheet object that holds the email list
    format_body = FormatBody(args.email_message_template, pi_name=args.pi_name,tech_desc=args.desc)
    for i in range(GS.number_of_chosen_emails()):
        company,last_name,title,email=GS.iterate_sheet()
        print (company,last_name,title,email)
        format_body.add_company_name(company)
        format_body.change_last_name(last_name)
        format_body.add_title(title)
        format_body.check_placeholders()
        n = EmailBuilder(to_email=email, bcc=args.bcc,cc=args.cc, subject=args.email_subject,body=format_body.make_html(),attachments=args.attachments)

        if (args.send):
            n.send()
        else:
            print ("saving draft")
            n.save_draft()
        format_body.init()




