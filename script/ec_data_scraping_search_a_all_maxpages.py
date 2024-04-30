
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
import time
from lxml import etree
import re

from webdriver_manager.chrome import ChromeDriverManager

username = os.getlogin()
print(username)

state_name='Orissa'
directory_name='Orissa'

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\KML\\"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chromeOptions)

#manually navigate to the page and search for "a"
# get the system username

directory = "C:/Users/"+username+"/Dropbox/Environment_Clearance"
os.chdir(directory)

base_url='https://environmentclearance.nic.in/'  
##Get the url under "Track Proposal"
url = 'https://environmentclearance.nic.in/proposal_status_state.aspx?pid=ClosedEC&statename=Orissa'


driver.get(url)
time.sleep(5)

     
### Select the EC Radio Button   
try:
   next_button = WebDriverWait(driver, 10).until(
       EC.element_to_be_clickable((By.XPATH, "//*[(@id = 'ctl00_ContentPlaceHolder1_RadioButtonList1_1')]"))
   )
   next_button.click()
except StaleElementReferenceException:
    print("Click_Exception1")
    pass
except WebDriverException:
    print("Click_Exception2")
    pass

### Enter Text "a"
try:
   text_area= WebDriverWait(driver, 10).until(
       EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_textbox2"))
   )
   text_area.send_keys('a')
except StaleElementReferenceException:
    print("Click_Exception1")
    pass
except WebDriverException:
    print("Click_Exception2")
    pass


### Search
try:
   search_button= WebDriverWait(driver, 10).until(
       EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btn"))
   )
   search_button.click()
except StaleElementReferenceException:
    print("Click_Exception1")
    pass
except WebDriverException:
    print("Click_Exception2")
    pass

# On the first page, click on next set of pages button
try:
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*/table[@id='ctl00_ContentPlaceHolder1_grdevents']/tbody/tr[12]/td/table/tbody/tr/td[11]/a"))
    )
    next_button.click()
    #time.sleep(5)
except:
        print("Next Set Page Button Not Found (...)")
        pass



while True:
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*/table[@id='ctl00_ContentPlaceHolder1_grdevents']/tbody/tr[12]/td/table/tbody/tr/td[12]/a"))
        )
        next_button.click()
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        dom = etree.HTML(str(soup))

        last_page_in_set = dom.xpath("//*[@id='ctl00_ContentPlaceHolder1_grdevents']/tbody/tr[12]/td/table/tbody/tr/td[11]/a")[0].text
        print(last_page_in_set)
    except:
        print("Next Set Page Button Not Found (...)")
        time.sleep(3600)
        break

# keep the webdriver window open
