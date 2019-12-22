# Used to make requests
import urllib.request
from bs4 import BeautifulSoup
import pdb
import re
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from difflib import SequenceMatcher
from googleapiclient.discovery import build
from google_sheets_handler import *
import argparse
import re
from gspread import Cell
from bs4 import BeautifulSoup
import re

def strip_special_charechters(name):
    name = re.sub('[\ -/]', '', name)
    return name


def clean_company_name(company_name):
    # if self.ends_with_s():
    #     company_name = company_name+"\'s"
    # else:
    #     company_name = company_name + "\'"

    # In the next code block I remove ("inc","AG", "limited", etc...)

    company_name = re.sub(', Inc(.*)?', '', company_name)
    company_name = re.sub(' Inc(.*)?', '', company_name)
    company_name = re.sub(', LLC(.*)?', '', company_name)
    company_name = re.sub(' Corporation', '', company_name)
    company_name = re.sub(' INC.', '', company_name)
    company_name = re.sub(' Co., Ltd.', '', company_name)
    company_name = re.sub(' AG', '', company_name)
    company_name = re.sub(' International(.*)?', '', company_name)
    company_name = re.sub(' Ltd(.*)?', '', company_name)
    company_name = re.sub(' B.V(.*)?', '', company_name)
    company_name = re.sub(' S.A(.*)?', '', company_name)
    company_name = re.sub(' Biotechnolog(.*)?', '', company_name)
    return company_name

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def parse_args():
    """"""
    desc = 'Search using google API'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-companies_to_interest_in_tech', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet hash number, found in the browser address line', required=0, dest='cit')
    parser.add_argument('-master_company_list', metavar='1QhN0gVxELRtKb3ElGAeGQbK5s4zsEVV0lUCSMAzdccI',
                        help='The google sheet hash number, found in the browser address line', required=0, dest='cl')
    return parser.parse_args()


class google_search:
    def __init__(self,google_sheet1='',google_sheet2=''):
        self.previous_links = set()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        # self.browser = webdriver.Chrome(chrome_options=options,executable_path='/home/gideon/YEDA/chromedriver')

        self.my_api_key = "AIzaSyDGwfHLWYo5-kITkD0YD7LEg0f0yD4jTqs"
        self.my_cse_id = "010801457502507310290:vqjegg6emhv"
        self.google_sheet1 =GoogleSheets(google_sheet1,0)
        if not (google_sheet2==''):
            self.google_sheet2 = GoogleSheets(google_sheet2, 0)

    def linkedin_login(self):
        self.browser = webdriver.Firefox()
        self.browser.get('https://www.linkedin.com/login?trk=gulsest_homepage-basic_nav-header-signin')
        username = self.browser.find_element_by_name('session_key')
        username.send_keys("bla123123@yahoo.com")
        passwd = self.browser.find_element_by_name('session_password')
        passwd.send_keys("nelsonmandela")
        button = self.browser.find_element_by_xpath('/html/body/div/main/div/form/div[3]/button')
        button.click()

    def google_search(self):
        try:
            url = 'https://www.google.com/search?q=gideon+lapidoth'

            # now, with the below headers, we defined ourselves as a simpleton who is
            # still using internet explorer.
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = resp.read()
            urllist = re.findall(r"""<\s*a\s*href=["']([^=]+)["']""", respData.decode("utf-8"))
            print(urllist)

        except Exception as e:
            print(str(e))

    def duckduck_search(self, single_query):
        url = 'https://www.duckduckgo.com/'
        self.browser.get(url)
        # pdb.set_trace()
        search_bar = self.browser.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        search_bar.send_keys("site:linkedin.com AND " + single_query + " AND about")
        search_bar.send_keys(Keys.RETURN)  # hit return after you enter search text
        time.sleep(1)  # sleep for 2 seconds so you can see the results
        linkedin_urls = self.browser.find_elements_by_xpath("//a[@class='result__a']")
        if len(linkedin_urls) == 0:
            return
        for result in linkedin_urls:
            if "company" in (result.get_attribute("href")):
                break
        time.sleep(2)
        if result in self.previous_links:
            return
        else:
            link = result.get_attribute("href")
            self.previous_links.add(result)  # keep memeory of visited links so not to waste time
        if "company" in link:
            result.click()
            print(single_query, "|", self.get_company_data_from_linkedin_when_logged_in())

    def get_company_data_from_linkedin_NOT_logged_in(self):
        time.sleep(2)
        # pdb.set_trace()

        overview, website, industry, name = "", "", "", ""
        try:
            data = self.browser.find_element_by_class_name('about-us').text.splitlines()
        except:
            pdb.set_trace()
            self.browser.find_element_by_class_name(
                "show-more-less-state__label.organization-page__label.show-more-less-state__label-more").click()
            data = self.browser.find_element_by_class_name('about').text.splitlines()
        try:
            for num, dat in enumerate(data):
                if website and industry:
                    break
                if re.search("Industr", str(dat)):
                    industry = str(data[num + 1])
                if re.search("Website", str(dat)):
                    website = str(data[num + 1])
        except:
            return name, overview, website, industry
        # pdb.set_trace()
        # website = website[2:-1]
        # industry = industry[2:-1]
        return website, industry

    def google_search_API(self, search_term, **kwargs):
        service = build("customsearch", "v1", developerKey=self.my_api_key)
        params = {
            'q': '<query>',
            'cx': '<cse reference>',
            'num': 10,
            'start': 1
        }
        res = service.cse().list(q=search_term, cx=self.my_cse_id, start=2).execute()
        return res

    def get_company_data_from_linkedin_when_logged_in(self,url):
        self.browser.get(url)
        time.sleep(2)
        # for num,data in enumerate(browser.find_elements_by_xpath("//div[starts-with(@id,'ember')]")):
        #    print (num,data.text)
        content = self.browser.find_element_by_class_name('mb3')
        pdb.set_trace()
        overview, website, industry, name = "", "", "", ""
        data=content.text.encode('utf-8').splitlines()
        for num, dat in enumerate(data):
            try:
                if re.search("Industry", str(dat)):
                    industry = str(data[num + 1])
                if re.search("Website", str(dat)):
                    website = str(data[num + 1])
            except:
                return website, industry

        return website, industry

    def search_using_selenium(self, single_query):
        url = 'https://www.google.com/'
        self.browser.get(url)
        search = self.browser.find_element_by_name('q')
        search.send_keys("site:linkedin.com AND " + single_query + " AND about")
        search.send_keys(Keys.RETURN)  # hit return after you enter search text
        time.sleep(1)  # sleep for 2 seconds so you can see the results
        linkedin_urls = self.browser.find_elements_by_class_name('iUh30')

        if len(linkedin_urls) == 0:
            return
        if linkedin_urls[0] in self.previous_links:
            return
        else:
            link = linkedin_urls[0].text
            self.previous_links.add(linkedin_urls[0])  # keep memeory of visited links so not to waste time
        if "company" in link:
            link = link.replace(" › ", "/")
            linkedin_urls[0].click()
            print(single_query, "|", self.get_company_data_from_linkedin_when_logged_in())

    def get_company_linkedin_about_page(self):
        company_name = self.google_sheet1.get_company_names()
        company_name.pop(0)
        for i in company_name:
            cleancompanyname=clean_company_name(i.rstrip())
            res = self.google_search_API("site:linkedin.com/company AND " + "\"" + cleancompanyname + "\"")
            if int(res.get('searchInformation').get('totalResults')) == 0:
                continue
            #print(cleancompanyname)
            minres = min(100, len(res.get('items')))
            for num in range(minres):  # if API result is not in first 5 results then continue
                #pdb.set_trace()
                link = res.get('items')[num].get('link')
                name=""
                if "about" in link:
                    name=link.split("/")[-2]
                else:
                    name = link.split("/")[-1]
                print (name,cleancompanyname)
                clean_name = strip_special_charechters(name).lower()
                cleancompanyname = strip_special_charechters(cleancompanyname).lower()
                similarity_score=similar(clean_name,cleancompanyname)
                if similarity_score>0.8:
                    if "about" in link:
                        print(i.rstrip(), "|", link)
                    else:
                        print(i.rstrip(), "|", link + "/about/")
                    break

    def search_company_with_keywords(self, search_string):
        '''
            This function uses google to search the key words (e.g. antibody)
            within the company website and returns the number of results google gets.
            The logic being that if no results are found then the company is irrelevant
            :param self:
            :return:
            '''
        companies_contacted = self.google_sheet2.get_company_names()
        emails_of_preivously_contacted_people = self.google_sheet2.get_emails()
        companies_to_contact_list = self.google_sheet1.get_company_names()
        # pdb.set_trace()
        cell_list=[]
        website_list = self.google_sheet1.get_website()
        website_list.pop(0)  # remove coloumn header
        google_search_results = self.google_sheet1.get_results()
        google_search_results.pop(0)
        google_search_results_padding = ['0'] * (len(website_list) - len(google_search_results))
        google_search_results.extend(google_search_results_padding)
        google_results_column = self.google_sheet1.col_num_map["results"]

        for i,link in enumerate(website_list):
            if not google_search_results[i]=="0" and (not google_search_results[i]==""):
                continue
            print ("site:" + website_list[i].rstrip()+search_string)
            res = google_search.google_search_API(
                "site:" + website_list[i].rstrip() + search_string)
            pdb.set_trace()
            print(website_list[i].rstrip(), int(res.get('searchInformation').get('totalResults')))
            cell_list.append(Cell(i + 2, google_results_column, int(res.get('searchInformation').get('totalResults'))))
        self.google_sheet1.wks.update_cells(cell_list)


    #def find_company_

    def find_people_on_linkedin_using_google(self,search_string):
        companies_contacted=self.google_sheet2.get_company_names()
        emails_of_preivously_contacted_people = self.google_sheet2.get_emails()
        companies_to_contact_list = self.google_sheet1.get_company_names()
        website_of_companies_to_contact = self.google_sheet1.get_website()
        website_of_companies_to_contact.pop(0)
        companies_to_contact_list.pop(0)  # remove coloumn header
        results = self.google_sheet1.get_results() #results is a coulmn with the number of hits I get searching the company webbsite with the relevant keywords
        results.pop(0)  # remove coloumn header
        results_padding = ['0'] * (len(companies_to_contact_list) - len(results))
        results.extend(results_padding)
        for i in range(len(website_of_companies_to_contact)):
            searched_emails=[s for s in emails_of_preivously_contacted_people if website_of_companies_to_contact[i] in s]
            if len(searched_emails) >0:
                print ("company %s already contacted,extract emails from master list"%(website_of_companies_to_contact[i]))
                continue
            cleancompanyname=clean_company_name(companies_to_contact_list[i])
            res = google_search.google_search_API(cleancompanyname +" AND "+search_string)
            #pdb.set_trace()
            try:
                if int(res.get('searchInformation').get('totalResults')) == 0:
                    continue
            except:
                continue
            minres = min(1000, len(res.get('items')))
            count = 0
            for num in range(minres):  # if API result is not in first 5 results then continue
                #pdb.set_trace()
                link = res.get('items')[num].get('link')
                if (not ("linkedin" in link)) or ("company" in link) or ("jobs" in link):
                    continue
                # pdb.set_trace()
                try:
                    desc = res.get('items')[num].get('title')
                    desc = re.split('–|-', desc)

                    name = desc[0].split(" ")
                    title = desc[1].replace(' ...', '')
                except:
                    continue  # I usually have an error when the description is poorly formatted
                print(link ,"|",website_of_companies_to_contact[i] ,"|", companies_to_contact_list[i], "|", "|", name[0], "|", " ".join(name[1:]).lstrip(), "|", title)
                count += 1
                if (count == 5):
                    break

    def find_person_title_on_google(self):
        # pdb.set_trace()
        linkedin_list = google_sheet.get_linkedin()
        linkedin_list.pop(0)  # remove column header
        title = google_sheet.get_titles()
        title.pop(0)  # remove column header
        first_name = google_sheet.get_first_names()
        last_name = google_sheet.get_last_names()
        company_list = google_sheet.get_company_names()
        company_list.pop(0)
        first_name.pop(0)
        last_name.pop(0)
        title_column = google_sheet.col_num_map["titles"]
        title_padding = [''] * (len(linkedin_list) - len(title))
        title.extend(title_padding)
        cell_list = []
        for i in range(len(linkedin_list)):
            name = first_name[i] + " " + last_name[i]
            print(name + " AND " + company_list[i] + " AND Dr.  -linkedin")
            # pdb.set_trace()
            try:
                if title[i]:  # if cell already has a value then skip
                    continue
            except:
                pdb.set_trace()
            res = google_search.google_search_API(name + " AND " + company_list[i] + " AND Dr.  -linkedin")
            if int(res.get('searchInformation').get('totalResults')) == 0:
                continue
            minres = min(9, int(res.get('searchInformation').get('totalResults')))
            for num in range(minres):
                # pdb.set_trace()
                soup = BeautifulSoup(res.get('items')[num]["htmlSnippet"], "html").get_text()
                if ("Dr. " + name in res.get('items')[num]["title"]) or ("Dr. " + name in soup):
                    cell_list.append(Cell(i + 2, title_column, "Dr."))
                    break
                elif (last_name[i] + ", Ph.D" in res.get('items')[num]["title"]) or (
                        last_name[i] + ", Ph.D" in soup):
                    cell_list.append(Cell(i + 2, title_column, "Dr."))
                    break

        google_sheet.wks.update_cells(cell_list)

if __name__ == '__main__':
    args = parse_args()  # get user arguments
    print("select the desired option:")
    print("1:generate list of people from company name")
    print("2:Search for company linkedin about page")
    print("3:Scrape linkedin for company information")
    print("4:Search google with company name and keywords")

    input_num = int(input())
    if input_num==1:
        google_search = google_search(google_sheet1=args.cit,google_sheet2=args.cl,)  # initiate google search object
        google_search.find_people_on_linkedin_using_google('site:linkedin.com/in AND "academic collaboration" OR "Drug Development" OR "Search and Evaluation" OR "Development" OR "Alliance and Integration" OR "Licensing" OR "BD&L" OR "Opportunities" OR "biological development" OR "Innovation" OR "Emerging Technology" OR "New Ventures" OR "Commercial Strategy" OR "Director of R&D" OR "Scouting" OR "CMO" OR "CSO" OR "Business Development" -jobs')
        #" AND immunotherapy AND antibodies AND (cancer OR autoimmune)"
    if input_num == 2:
        google_search = google_search(google_sheet1=args.cit, google_sheet2=args.cl, )
        google_search.get_company_linkedin_about_page()
    if input_num==3:
        google_search = google_search(google_sheet1=args.cit, google_sheet2=args.cl, )  # initiate google search object
        google_search.linkedin_login()
        company_websites=google_search.google_sheet1.get_website()
        company_websites.pop(0)
        for website in company_websites:
            try:
                print (google_search.get_company_data_from_linkedin_when_logged_in(website))
            except:
                print("Did not find linked page:",website)
    if input_num == 4:
        google_search = google_search(google_sheet1=args.cit, google_sheet2=args.cl, )
        google_search.search_company_with_keywords(" AND \"enzyme inhibitor\"")

