'''
This file will hold functions that are used by all the classes 
'''
import re
from google_sheets_handler import *
import argparse
import pdb
from search_google import *
from fuzzywuzzy import process
from fuzzywuzzy import fuzz



def parse_args():
    """"""
    desc = 'Automatically send emails using google sheets as a database'
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('-google_sheet',metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='google sheet hash number, found in the browser address line', required=0,dest='gs')
    parser.add_argument('-filename', metavar='bla.csv',
                        help='CSV file', required=0,dest='fn')
    return parser.parse_args()

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def clean_company_name(company_name:str):
    # if ends_with_s():
    #     company_name = company_name+"\'s"
    # else:
    #     company_name = company_name + "\'"

    # In the next code block I remove ("inc","AG", "limited", etc...)
    company_name = re.sub(', Inc(.*)?', '', company_name)
    company_name = re.sub(' Inc(.*)?', '', company_name)
    company_name = re.sub(', LLC(.*)?', '', company_name,flags=re.IGNORECASE)
    company_name = re.sub(' LLC(.*)?', '', company_name,flags=re.IGNORECASE)
    company_name = re.sub(' L.L.C.(.*)?', '', company_name,flags=re.IGNORECASE)
    company_name = re.sub(' Corporation', '', company_name)
    company_name = re.sub(' INC.', '', company_name)
    company_name = re.sub(' Co., Ltd.', '', company_name)
    company_name = re.sub(' AG', '', company_name,flags=re.IGNORECASE)
    company_name = re.sub(' International(.*)?', '', company_name)
    company_name = re.sub(' Ltd(.*)?', '', company_name)
    company_name = re.sub(' B.V(.*)?', '', company_name)
    company_name = re.sub(' S.A(.*)?', '', company_name)
    company_name = re.sub(' gmbh(.*)?', '', company_name,flags=re.IGNORECASE)
    company_name = re.sub(' company(.*)?', '', company_name, flags=re.IGNORECASE)
    company_name = re.sub(' &(.*)?', '', company_name, flags=re.IGNORECASE)
    return company_name

def validate_company_name_using_google_search(company_name:str,google_search_obj):
    known_websties=['www.sec.gov','www.investopedia.com','wiktionary.org','www.uspto.gov','www.cdc.gov','www.bloomberg.com','https://fdazilla.com','chemicalbook.com','wikipedia','yahoo.com','justia.com','pharmaoffer.com','freepatentsonline.com','twitter','nytimes.com','wsj.com','linkedin.com']
    res = google_search_obj.google_search_API(company_name)
    links=set()
    for num,i in enumerate(res.get('items')):
        if num>9:
            break
        if fuzz.token_set_ratio(company_name, i.get('title')) >70 or fuzz.token_set_ratio(company_name, i.get('snippet')) >70:
            found=False
            for link in known_websties:
                if link in i.get('link'):
                    found=True
            if found:
                continue
            print (i.get('link'))
            if "http://" in i.get('link') or "https://" in i.get('link'):
                links.add(i.get('link').rsplit('/')[2])
            else:
                links.add(i.get('link').rsplit('/')[0])

    #print (company_name)
    print (links)
    pdb.set_trace()
    Ratios = process.extract(company_name, list(links))
    top_link=process.extractOne(company_name, list(links))[0]
    top_link_score = process.extractOne(company_name, list(links))[1]
    print(company_name,"|",top_link,"|",top_link_score)
    pdb.set_trace()


if __name__ == '__main__':
    args = parse_args()
    print(args.gs)
    if args.gs is not None:
        google_search_obj=google_search(args.gs)
        clean_company_list=set()
        GS = GoogleSheets(args.gs, 0)
        company_list=GS.get_company_names()
        company_list.pop(0)
        for i in company_list:
            if 'univ' in i.lower() or 'center' in i.lower() or 'hospital' in i.lower():
                continue
            if isEnglish(i):
                clean_company_list.add(clean_company_name(i))
                validate_company_name_using_google_search(clean_company_name(i),google_search_obj)
        pdb.set_trace()
        print (clean_company_list)


