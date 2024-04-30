# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:40:31 2016

@author: anustubh

The steps are as follows
1. Navigate to the page where you search for the proposal manually and then
search for "a"
"""

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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

username = os.getlogin()
print(username)


##Name of State
##Make sure you create directory
# example Uttar%20Pradesh
state_name='Haryana'
#When there is a space add _ example Uttar_Pradesh
directory_name='Haryana'

lenovo=1

if lenovo:
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "C:\\Users\\"+username+"\\Dropbox\\agnihotri_gupta\\Environment_Clearance\\"+directory_name+"\\KML\\"}
    chromeOptions.add_experimental_option("prefs",prefs)
    service = Service(executable_path='C:/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chromeOptions)

else:
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless') #Dont put headless on for some time. Once code is sorted, then do headless. 
    prefs = {"download.default_directory" : "C:\\Users\\"+username+"\\Dropbox\\agnihotri_gupta\\Environment_Clearance\\"+directory_name+"\\KML\\",
             "profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chromeOptions)




directory = "C:/Users/"+username+"/Dropbox/agnihotri_gupta/Environment_Clearance"
os.chdir(directory)

base_url='https://environmentclearance.nic.in/'  


for attempt in range(1,6): 
    #Cycle Through Website 4 times 
    print('Attempt is')
    print(attempt)
    
    ##Get the url under "Track Proposal"
    url = 'https://environmentclearance.nic.in/proposal_status_state.aspx?pid=ClosedEC&statename='+state_name
    
    
    driver.get(url)
    time.sleep(5)
    
    ##Max Page Number +1 How many pages show up when you search for 'a' in EC track proposal 
    max_page_number=105
    
    
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
    
    
    
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    
    soup = BeautifulSoup(driver.page_source,  "html.parser")
    
    table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_grdevents"})
    
    headers = [header.text for header in table.find_all('th')]
    
    rows = table.findAll('tr')
      
    data_ec_closed= []
     
    for row in rows:
         cols = row.find_all('td')
         #cols = [ele.text.split() for ele in cols]
         cols = [ele.text.encode('utf-8').strip() for ele in cols]
         data_ec_closed.append([ele.decode() for ele in cols]) 
    
    
    data_ec_closed_df = pd.DataFrame(data_ec_closed)
    #Remove rows that have more than 8 null values 
    data_ec_closed_df['Null_Values']=data_ec_closed_df.notnull().sum(axis=1)
    data_ec_closed_df = data_ec_closed_df.drop(data_ec_closed_df[data_ec_closed_df.Null_Values != 8].index)
    
    ##Loop across all pages 
    ##manually checked that there are 266 pages. Should be a better way to do this
    for page_number in range(2,max_page_number): 
        print(page_number)
        
        try:
           next_button = WebDriverWait(driver, 10).until(
               EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'Page$%d')]" % page_number))
           )
           next_button.click()
        except StaleElementReferenceException:
            print("Click_Exception1")
            pass
        except WebDriverException:
            print("Click_Exception2")
            pass
        
        time.sleep(.5)
        
        soup = BeautifulSoup(driver.page_source,  "html.parser")
          
        table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_grdevents"})
        
        rows = table.findAll('tr')
          
        data_ec_closed_temp= []
         
        for row in rows:
             cols = row.find_all('td')
             #cols = [ele.text.split() for ele in cols]
             cols = [ele.text.encode('utf-8').strip() for ele in cols]
             data_ec_closed_temp.append([ele.decode() for ele in cols]) 
    
    
        data_ec_closed_temp = pd.DataFrame(data_ec_closed_temp)
        
        
        data_ec_closed_temp['Null_Values']=data_ec_closed_temp.notnull().sum(axis=1)
        
        data_ec_closed_temp = data_ec_closed_temp.drop(data_ec_closed_temp[data_ec_closed_temp.Null_Values != 8].index)
    
        data_ec_closed_df=pd.concat([data_ec_closed_df,data_ec_closed_temp])
        
        
    ##Remove columns 

    data_ec_closed_df.drop(data_ec_closed_df.columns[[8,9,10,11,12]], axis = 1, inplace = True)
    
    data_ec_closed_df.drop(data_ec_closed_df.columns[[8]], axis = 1, inplace = True)

    ##Add headers 
    data_ec_closed_df.columns = headers
    
    
    ##write 
    if lenovo:
        csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/'+directory_name+ '/'+ state_name+'_ec_complete_'+str(attempt)+'.csv'
        data_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')
    else:
        csvfile = 'C:/Users/agnihotri/Dropbox/agnihotri_gupta/Environment_Clearance/'+directory_name+'/'+directory_name+'_ec_complete_'+str(attempt)+'.csv'
        data_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')