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
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException

import time
from lxml import etree
import re
import csv

from webdriver_manager.chrome import ChromeDriverManager

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

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

##Name of State
##Make sure you create directory

unique_proposals=pd.read_csv(directory+'/'+directory_name+'/'+directory_name+'_ec_complete_unique.csv')

print(unique_proposals)
base_url='https://environmentclearance.nic.in/'  
##Get the url under "Track Proposal"
url = 'https://environmentclearance.nic.in/proposal_status_state.aspx?pid=ClosedEC&statename='+state_name

data_ec_formtype=[]

#data_ec_closed_df = pd.DataFrame(columns=['Proposal','File_No','State','District','Tehsil','Category','Company','Status'])
#pd.DataFrame()
#data_ec_closed_df.columns=['Proposal','File_No','State','District','Tehsil','Category','Company','Status']
#
links_documents_df=[]
links_proposal_df=[]
same_page = False
#exception proposal = 1695 Odisha 
for proposal_number in range(1,len(unique_proposals['Proposal.No.'])): 
    print(proposal_number)                     
    driver.get(url)
    time.sleep(1)
    
         
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
    
    
    ### Enter Proposal Number
    try:
       text_area= WebDriverWait(driver, 10).until(
           EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_textbox2"))
           )
       text_area.send_keys(unique_proposals['Proposal.No.'][proposal_number])
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
    
    time.sleep(1)
    
        
    try:
       next_button = WebDriverWait(driver, 10).until(
           EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_grdevents_ctl02_lnkDelete"))
       )
       next_button.click()
    except StaleElementReferenceException:
        print("Click_Exception1")
        pass
    except WebDriverException:
        print("Click_Exception2")
        pass
    

    if "parivesh.nic.in" in driver.current_url:
        formtype = 'Parivesh-2'
        print(unique_proposals['Proposal.No.'][proposal_number] + " Parivesh-2")
        data_ec_formtype.append([unique_proposals['Proposal.No.'][proposal_number], formtype])
        same_page = True
        
    else:
    
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        
        #soup = BeautifulSoup(driver.page_source,  "html.parser")
        
        table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1"})
        
        #headers = [header.text for header in table.find_all('th')]
        
        dom = etree.HTML(str(soup))
        proposal_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text

        # Get Form1 data

        EC2 = driver.find_element_by_xpath("//a/img[contains(@src,'images/ecreport1.jpg')]")
        EC2.click()

            
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        #time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        dom = etree.HTML(str(soup))

        #formtype = driver.find_element_by_xpath("//div[@id='qq']/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/u").text

        try: #form2
            formtype = driver.find_element_by_xpath("//div[@id='qq']/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/u").text
            print(proposal_number, formtype)
            #data_ec_formtype.append([proposal_number, formtype])
            
        except: #form1
            try:
                formtype = driver.find_element_by_xpath("//div[@id='qq']/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/b/u").text
                print(proposal_number, formtype)
                #data_ec_formtype.append([proposal_number, formtype])

            except: #parivesh
                try:
                    if "parivesh.nic.in" in driver.current_url:
                        formtype = 'Parivesh'
                        print(proposal_number, formtype)
                        #data_ec_formtype.append([proposal_number, formtype])
                    else:
                        formtype = 'Missing'
                        print(proposal_number, formtype)
                except:
                        formtype = 'Missing'
                        print(proposal_number, formtype)
                        data_ec_formtype.append([proposal_number, formtype])


        data_ec_formtype.append([proposal_number, formtype])


    data_ec_formtype_df=pd.DataFrame(data_ec_formtype)
    data_ec_formtype_df.columns = ['Proposal','FormType']
    csvfile = directory+'/'+directory_name+'/'+directory_name+'_ec_formtype'+'.csv'
    data_ec_formtype_df.to_csv(csvfile,encoding='utf-8-sig')



    if same_page == False:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        same_page = False




##Convert into Dataframe 
#links_ec_closed_df=pd.DataFrame(links_documents_df)
#links_ec_closed_df_pid=pd.DataFrame(links_proposal_df)

##write to Dropbox
#csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_ec_complete_links'+'.csv'
#links_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')

#csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_ec_complete_links_pid'+'.csv'
#links_ec_closed_df_pid.to_csv(csvfile,encoding='utf-8-sig')