from selenium import webdriver
from google_sheets_handler import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import pdb
from selenium.webdriver.firefox.options import Options
import time
import re
options = Options()
options.headless = False
from googlesearch import search
from scraper import *
import resource
import argparse


class CustomValueError(ValueError):
 def __init__(self, arg):
  self.strerror = arg
  self.args = {arg}


def parse_args():
    """"""
    desc = 'Search linkedin for user information'
    parser = argparse.ArgumentParser(description = desc)

    parser.add_argument('-google_sheet', metavar='02e8e18aa60c165820184fd59f39851154e1874e',
                        help='This is the google sheet of the companies to interest in tech',
                        required=0, dest='google_sheet',type=str)

    return parser.parse_args()
class linkedin_user:
    def __init__(self, link:str = "", google_sheet:str=""):
        self.GS=GoogleSheets(google_sheet)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        #self.browser = webdriver.Chrome(chrome_options=options,executable_path='/home/gideon/YEDA/chromedriver')
        self.browser = webdriver.Firefox()
        self.browser.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
        username = self.browser.find_element_by_name('session_key')
        username.send_keys("bla123123@yahoo.com")
        passwd = self.browser.find_element_by_name('session_password')
        passwd.send_keys("nelsonmandela")
        button = self.browser.find_element_by_xpath('/html/body/div/main/div/form/div[3]/button')
        button.click()
        self.link=link
        self.linkedin_data=''
        self.page_data='' #this will hold the raw HTML text for searching other relevant terms

        if google_sheet:
            #self.GS=GoogleSheets(google_sheet)
            index=self.GS.get_coulmn_number_by_value("linkedin")
            self.linkedin_links=self.GS.wks.col_values(index)
            self.titels=self.GS.get_titles()


    def get_user_by_link(self,link:str):
        """
        Gets user information using link
        :param link: linkedin user link
        :return: null
        """
        self.browser.get(link)

        #pdb.set_trace()
    def set_link(self,link:str):
        self.browser.get(link)
        time.sleep(1)
        self.page_data =self.browser.page_source

    def finish(self):
        self.browser.close()

    def get_user_name(self):
        # get name from linkedin profile
        counter=0
        self.linkedin_data=""
        data_line_num=0
        while data_line_num<=6:
            try:
                time.sleep(1)
               # pdb.set_trace()

                self.linkedin_data = self.browser.find_elements_by_xpath("//div[starts-with(@id,'ember')]")[data_line_num].text.splitlines()
                find_string = [self.linkedin_data.index(i) for i in self.linkedin_data if 'More' in i]
                #pdb.set_trace()
                if len(find_string)==0:
                    raise CustomValueError("Did not find More")
                #self.linkedin_daa =self.browser.find_element_by_xpath("/html/body/main/div[1]/section/section[1]/div[2]").text
                #self.linkedin_data =self.linkedin_data.splitlines()
                if []==self.linkedin_data:

                    raise CustomValueError("Did not find user data on linkedin")
                for i, line in enumerate(self.linkedin_data):

                    if re.search("More", line):
                        print ("YES")
                        return (self.linkedin_data[i+1])
                #pdb.set_trace()
                return name
            except Exception as e:
                data_line_num+=1
                print(str(e))
                #self.linkedin_data = self.browser.find_element_by_xpath("/html/body/main/section[1]/section/section[1]/div/div").text
                #self.linkedin_data = self.linkedin_data.splitlines()
                #return (self.linkedin_data[0])
                continue
            break



    def get_user_proffesion(self):
        # get current occupation from linkedin profile
        try:
            for i, line in enumerate(self.linkedin_data):
                #pdb.set_trace()
                if re.search("account", line,re.IGNORECASE):
                    return (self.linkedin_data[i + 1])
        except Exception as e:
            print("Did not find name in Linkedin page")

        #for num,i in enumerate(prof):
       # print (prof[6].text)
        #pdb.set_trace()
       # return prof[6].text

    def get_user_company(self):
       # current_company=self.browser.find_element_by_xpath('/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/h2').text
        #return current_company
        # get current occupation from linkedin profile
        #return (self.browser.find_element_by_xpath("/html/body/main/div[1]/section/section[1]/div[2]/div/div[2]/div[1]/a/span").text)
        #pdb.set_trace()
        try:
            for i, line in enumerate(self.linkedin_data):
                if re.search("company", line,re.IGNORECASE):
                    return (self.linkedin_data[i + 1])
        except Exception as e:
            print("Did not find company name on page")

    def find_user_by_name(self,name:str):
        search_box = self.browser.find_element_by_xpath("/html/body/header/div/form/div/div/div/div/div[1]/div/input")
        search_box.clear()

        search_box.send_keys("\""+name+"\"")
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        #pdb.set_trace()
        try:
            link = LU.browser.find_elements_by_class_name("name")[0]
            link.click()
            return True
        except Exception as e:
            print ("Did not find user: "+name)
            return False

    def get_user_title(self):
        dr=self.page_data.find("Dr.")
        phd1 = self.page_data.find("PhD")
        phd2 = self.page_data.find("Ph.D.")
        scd1 = self.page_data.find("Sc.D.")
        scd2 = self.page_data.find("D.Sc.")
        MD = self.page_data.find("M.D.")
        if (dr>0) or(phd1>0) or(phd2>0) or(scd1>0) or(scd2>0) or(MD>0):
            return "Dr."

    def find_user_link_in_google(self,name:str):
        name=name.rstrip()
        first_name=name.split(' ')[0]
        last_name = name.split(' ')[-1]
        additional_query_strings=  " AND (hebrew OR Weizmann OR technion OR bgu OR bar-ilan)"
        query = "linkedin AND "+name+additional_query_strings
        links=search_using_selenium(query)
        #pdb.set_trace()
        #links=search_in_search_engine(query,"duckduckgo")
        for link in (links):
            if not re.search("linkedin", link, re.IGNORECASE):
                continue
            if not re.search(first_name, link, re.IGNORECASE):
                continue
            if re.search(last_name, link, re.IGNORECASE):

                link=link.replace(" › ","/in/")

                print(link)
                self.get_user_by_link(link)
                return True

        print("Did not find user: " + name)
        return False

''
#search=browser.find_element_by_xpath(/html/body/header/div/form/div/div/div/artdeco-typeahead-deprecated/artdeco-typeahead-deprecated-input/input')
#search.send_keys("glapidoth@gmail.com")
#search.send_keys(Keys.RETURN)



if __name__ == "__main__":
    args=parse_args()
    LU = linkedin_user(google_sheet=args.google_sheet)
    title_coulmn_num=LU.GS.col_num_map.get("titles")
    pdb.set_trace()
    for num,link in enumerate (LU.linkedin_links):
        pdb.set_trace()
        if link.find("http")<0:
            continue
        if LU.titels[num]:
            continue
        LU.set_link(link)
        title=LU.get_user_title()
        LU.GS.wks.update_cell(num+1,title_coulmn_num,title)


    #
    # with open(name, "r") as ifile:
    #     for line in ifile:
    #         mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    #         print ("Memory usage is: {0} KB".format(mem))
    #
    #        # pdb.set_trace()
    #
    #         if not LU.find_user_link_in_google(line):
    #            # pdb.set_trace()
    #             continue
    #
    #
    #         try:
    #             print(LU.get_user_name()+"|",LU.get_user_company()+"|",LU.get_user_proffesion())
    #
    #         except Exception as e:
    #             print(str(e))
    #             continue

    LU.finish()

import pdb

import pdb


