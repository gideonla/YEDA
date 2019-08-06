from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import pdb
from selenium.webdriver.firefox.options import Options
import time
options = Options()
options.headless = True



class linkedin_user:
    def __init__(self, link:str):
        self.browser = webdriver.Firefox(options=options)
        self.browser.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
        username = self.browser.find_element_by_name('session_key')
        username.send_keys("glapidoth@gmail.com")
        passwd = self.browser.find_element_by_name('session_password')
        passwd.send_keys("C71fB6u9S6Tb")
        button = self.browser.find_element_by_xpath('/html/body/div/main/div/form/div[3]/button')
        button.click()
        self.link=link
        self.browser.get(link)

    def set_link(self,link:str):
        self.browser.get(link)

    def finish(self):
        self.browser.close()

    def get_user_name(self):
        # get name from linkedin profile
        name = self.browser.find_element_by_xpath(
            '/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[1]/li[1]').text
        return name

    def get_user_proffesion(self):
        # get current occupation from linkedin profile
        prof = self.browser.find_element_by_xpath(
            '/html/body/div[5]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/h2').text
        return prof

    def get_user_company(self):
        current_company=self.browser.find_element_by_xpath('//*[@id="ember100"]').text
        return current_company
''
#search=browser.find_element_by_xpath(/html/body/header/div/form/div/div/div/artdeco-typeahead-deprecated/artdeco-typeahead-deprecated-input/input')
#search.send_keys("glapidoth@gmail.com")
#search.send_keys(Keys.RETURN)



if __name__ == "__main__":
    link = sys.argv[1]
   # # wks = gc.open('Companies to interest in technology').sheet1
    time1 = time.time()
    LU = linkedin_user(link)
    print(LU.get_user_name())
    print(LU.get_user_company())
    print (LU.get_user_proffesion())
    time2 = time.time()
    print (time2-time1)

    LU.finish()