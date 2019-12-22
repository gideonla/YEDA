## YEDA

These are an assortment of scripts I've written to automate marketing campaigns for YEDA (Weizmann institute of science TTO).

Some of the functionalities:

 -   Automatic email sending (using either Azure API or sendmail)
    
 -   Automatic reply notification (whether or not a contact has replied)
    
 -   Email tracking
    
 -   Database management using google sheets API

**Use examples:**

 - Sending emails:

  

    python EmailSender.py  **-cshn** 1OjadEyidSldkGdxXmDUVw_3UU9nF0f2bywzbX9SRikcY **-mshn** 1cTW4WqGTfdSBG5ZKI76XldEXthr2MU_Pzw9lIDqm-4o0 **-general_email_message_template**  \<template_email.txt\>  **-private_email_message_template**  \<personal_template_email>r **-pi_name** "Prof. Michael Fainzilber" **-desc** "a method for inhibiting importin to treat psychiatric stress and other disorders" **--send** 0 **-email_subject** "A Novel Method for Treating Psychiatric Disorders [1875]" **-attachments** \<FILES>

  

 - cshn : The hash number of the google sheet with the companies for the current email campaign.

-  mshn : The hash number of the google sheet with the “master list” of companies

-  general_email_message_template - the file with the email template

-  private_email_message_template - The file with the private message

-  pi_name - string

-  desc - The short description of the the technology. This will go into the body of the email.

-  send - 1 = send  0= save draft

-  email_subject - string
