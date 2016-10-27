from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import mechanize
import cookielib
import clipboard
import time, random, string
import pandas as pd

# 6:40

class Amcat:
    def __init__(self, uname, password, url):
        self.uname = uname
        self.password = password
        self.url = url

        # selenium
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.http.phishy-userpass-length', 255)
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get(self.url)
        self.driver = driver

    def startAutomata(self):
        # close webcam test window
        self.driver.find_element_by_class_name('close').click()

        # login
        uname = self.driver.find_element_by_name('txtUserName')
        password = self.driver.find_element_by_name('txtPassword')
        uname.send_keys(self.uname)
        password.send_keys(self.password)
        loginBtn = self.driver.find_element_by_id('btnLogin')
        loginBtn.click()

        # accept disclaimer
        disclaimerChkBox = self.driver.find_element_by_id('disclaimerAccepted')
        disclaimerChkBox.click()
        self.driver.find_element_by_id('startButtonEnable').click()

        #self.__fillAmazonForm()
        self.__fillNameEmailForm()

        # Modules display: click on start button (created by js)
        self.driver.execute_script("javaScript: saveNStartTest('SaveTest','?mode=f');")

        # Test directions
        self.driver.find_element_by_id('tdNext').click()

        #Module direction
        self.driver.find_element_by_id('tdNext').click()

        # demo start popup
        self.driver.find_element_by_id('moduleDemoPopupStart').click()
        #endDemoAnimation();
        self.driver.execute_script("javaScript: endDemoAnimation();")

    def __fillNameEmailForm(self):
        self.driver.find_element_by_id('candidateName').send_keys('dummy')
        self.driver.find_element_by_id('email_id').send_keys('dummy@dummy.com')
        self.driver.find_element_by_id('submitRegTemp').click()


    def __fillAmazonForm(self):
        # fill amazon form
        self.driver.find_element_by_id('rdoGenderMale').click()
        self.driver.find_element_by_xpath("//select[@id='txtEthnicity']/option[text()='Asian']").click()
        self.driver.find_element_by_id('submitRegTemp').click()

    def fetchQuestionData(self):
        #selectBox = self.driver.find_element_by_id('sdropIDLang')
        #selectBox.find_element_by_tag_name('li')

        data = []
        for langID in [1,2,3,4,6]:
            self.driver.execute_script('javascript: return getLangQuestion(' + str(langID) + ');')
            lang_data = self.fetchLanguageData()
            lang_data['lang'] = langID
            data.append(lang_data)
            time.sleep(2)
        return data

    def fetchLanguageData(self):
        data = {}
        data['directions'] = self.driver.find_element_by_id('directionsDiv').text
        data['qStatement'] = self.driver.find_element_by_id('questionStatementDiv').text
        #defaultCode = self.driver.find_element_by_id('directionsDiv').text not working

        # Move to test case tab
        try:
            time.sleep(5)
            self.driver.find_element_by_id('tab2ID').click()
            self.driver.find_element_by_id('tab2ID').click()
            time.sleep(1)
            self.driver.find_element_by_id('tab1ID').click()
            self.driver.find_element_by_id('tab1ID').click()
            time.sleep(1)
            self.driver.find_element_by_id('tab2ID').click()
            self.driver.find_element_by_id('tab2ID').click()
            time.sleep(1)
            self.driver.find_element_by_id('tab1ID').click()
            self.driver.find_element_by_id('tab1ID').click()
        except:
            pass
        data['tcTab'] = self.driver.find_element_by_id('tab2').text
        return data

    def nextQuestion(self):
        self.driver.find_element_by_id('nextQuestionID').click()


if __name__ == '__main__':
    uname = 'amazon_demo'
    password = 'amazon_demo'
    url = 'https://takeamcat2.aspiringminds.com/login.php?cid=2328&sp=1'
    a = Amcat(uname, password, url)

    Result = []
    a.startAutomata()
    for quesNo in range(1, 2):
        ques_data = a.fetchQuestionData()
        if ques_data != "":
            for lang_data in ques_data:
                lang_data['sid'] = quesNo
        Result = Result + ques_data
        a.nextQuestion()
        time.sleep(3)
    DF = pd.DataFrame(Result)

    pass

