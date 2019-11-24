from google_sheets_handler import *
from format_email_body import *
from EmailBuilder import *
import argparse
import pdb
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename





def parse_args():
    """"""
    desc = 'Automatically send emails using google sheets as a database'
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('-cshn','--company_sheet_hash_number', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet of the companies to send email hash number, found in the browser address line', required=1,dest='cshn')
    parser.add_argument('-mshn','--master_sheet_hash_number', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet hash number, found in the browser address line', required=1,dest='mshn')
    parser.add_argument('-general_email_message_template', help='Path to email template text file (when appraoching first time)',required=1)
    parser.add_argument('-private_email_message_template', help='Path to email template text file (when appraoching second time)', required=1)
    parser.add_argument('-pi_name', help='Name of PI', required=1)
    parser.add_argument('-desc', help='Description of technology', required=1)
    parser.add_argument('-cc', help='Who to send cc email to', default="jacob.fierer@weizmann.ac.il, Orly.Savion@weizmann.ac.il  ")
    parser.add_argument('-bcc', help='Who to send bcc email to', default="magic.yeda@weizmann.ac.il")
    parser.add_argument('-email_subject', help='Email subject line', default="",required=1)
    parser.add_argument('-attachments', nargs='+', help='list of files to attach to email')
    parser.add_argument("--send", type=str2bool, nargs='?',const=True, default=False, help="If false save email to drafts and don't send")





    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    GS = GoogleSheets(args.cshn,0) #create the google sheet object that holds the email list for the current campaign
    GS_master= GoogleSheets(args.mshn,1) #this object holds the google sheet for the master list (where all the company list live)
    for i in range(GS.number_of_chosen_emails()):
        company,last_name,title,emails,first_name=GS.iterate_sheet()
        email_list=emails.split(",")
        email_replied=GS_master.check_if_replied(email_list[0]) #if this email has been contacted before (as marked in the master list) return appropriate boolean.
        if email_replied:
            format_body = FormatBody(args.private_email_message_template, pi_name=args.pi_name, tech_desc=args.desc)
            format_body.change_first_name(first_name)
        else:
            format_body = FormatBody(args.general_email_message_template, pi_name=args.pi_name, tech_desc=args.desc)
        print (company,last_name,title,email_list[0])
        format_body.add_company_name(company)
        format_body.change_last_name(last_name)
        format_body.add_title(title)
        format_body.check_placeholders()
        email_list.append(args.bcc)
        #email_list.append("glapidoth@gmail.com")
        msg = MIMEMultipart()
        body = MIMEText(format_body.get_body(),'html')
        msg.attach(body)
        msg['From'] = 'Dr. Gideon Lapidoth - YEDA R&D<gideon.lapidoth@weizmann.ac.il>'
        msg['To'] = ''
        msg['Cc'] = args.cc
        msg['Bcc'] = args.bcc+","+emails+',glapidoth@gmail.com'
        msg['Subject'] = args.email_subject
        try:
            for f in args.attachments:
                with open(f, "rb") as fil:
                    part = MIMEApplication(fil.read(),Name=basename(f))
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)
        except:
            print ("no files to attach")
        server = smtplib.SMTP('localhost')
        pdb.set_trace()
        rcpts = (msg['Cc']+","+msg['To']+","+msg['Bcc']).split(',')
        print (rcpts)
        print ("sending to",last_name,"at",company)
        server.sendmail('gideon.lapidoth@weizmann.ac.il', rcpts, msg.as_string())
        pdb.set_trace()
        GS_master.update_contacted(email_list[0])
        format_body.init()




