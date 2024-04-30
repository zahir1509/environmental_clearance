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

import time
from lxml import etree
import re
import csv
import shutil

from webdriver_manager.chrome import ChromeDriverManager

import warnings

#suppress depecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

username = os.getlogin()
print(username)

state_name='Orissa'
directory_name='Orissa'

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\PDF\\",
         "plugins.always_open_pdf_externally": True}
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
print('BEFORE DUPLICATES REMOVED')
print(len(unique_proposals))

# Remove all rows with duplicate proposal numbers
#unique_proposals.drop_duplicates(subset=['Proposal.No.'], keep='first', inplace=True)
unique_proposals.drop_duplicates(subset=['Proposal.No.'], inplace=True)
unique_proposals.reset_index(drop=True, inplace=True)
print('AFTER DUPLICATES REMOVED')
print(len(unique_proposals))

#print(f"Rows 153 to 157 in dataframe: {unique_proposals[153:158]}")

base_url='https://environmentclearance.nic.in/'  
##Get the url under "Track Proposal"
url = 'https://environmentclearance.nic.in/proposal_status_state.aspx?pid=ClosedEC&statename='+state_name

data_ec_closed=[]

data_ec_form2=[]

data_ec_timeline = []
#data_ec_closed_df = pd.DataFrame(columns=['Proposal','File_No','State','District','Tehsil','Category','Company','Status'])
#pd.DataFrame()
#data_ec_closed_df.columns=['Proposal','File_No','State','District','Tehsil','Category','Company','Status']
#
links_documents_df=[]
links_proposal_df=[]


def download_wait(directory, timeout=30, nfiles=1):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.pdf'):
                dl_wait = False

        seconds += 1
    return seconds


#exception proposal = 1695 Odisha 

# exception 38,97,105,112,155 Odisha - duplicates - fixed now
# SCRAPED UNTIL 655
for proposal_number in range(655,len(unique_proposals['Proposal.No.'])): 
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


    
    
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    
    #soup = BeautifulSoup(driver.page_source,  "html.parser")
    
    #table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1"})
    
    #headers = [header.text for header in table.find_all('th')]
    
    dom = etree.HTML(str(soup))
    
    try:

        #Proposal Number 
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text)
        proposal_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text


        # Replace '/' in proposal number with '_'
        proposal_number_dir = proposal_number.replace('/','_')
        
        # Create a directory by the name of the proposal number
        directory_pdf_root = "C:/Users/"+username+"/Dropbox/Environment_Clearance/"+directory_name+"/PDF"
        if not os.path.exists(directory_pdf_root+'/'+proposal_number_dir):
            os.makedirs(directory_pdf_root+'/'+proposal_number_dir)
        
        # Set the download directory to the proposal number directory
        #prefs = {"download.default_directory" : directory_pdf_root+'/'+proposal_number_dir}
        download_path = directory_pdf_root+'/'+proposal_number_dir
        #download_path_temp = directory_pdf_root+'/'+proposal_number_dir+'/temp'
        #params = { 'behavior': 'allow', 'downloadPath': download_path }
        #driver.execute_cdp_cmd('Page.setDownloadBehavior', {
        #    'behavior': 'allow', 'downloadPath':  "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\PDF\\"+proposal_number_dir+'\\temp'
        #    })    

        time.sleep(1)
        
        # FOR EIA
        try:
            download_path_EIA = download_path+'/EIA'
            
            # EIA report
            # Download the pdf file open
            # Will happen by default since the chrome settings are set to open pdf externally and not embed
            EIA = driver.find_element_by_xpath("//a/img[contains(@src,'images/eia.png')]")
            os.makedirs(download_path_EIA)
            driver.execute_cdp_cmd('Page.setDownloadBehavior', {
            'behavior': 'allow', 'downloadPath':  "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\PDF\\"+proposal_number_dir+'\\EIA'
            })    
            EIA.click()
            print(f"Downloading EIA for {proposal_number}")
            time.sleep(1)
            download_wait(download_path_EIA)
            
        
        except:
            pass


        try:
            #Risk Asssessment Report
            download_path_RISK = download_path+'/RISK'
            
            RISK = driver.find_element_by_xpath("//a/img[contains(@src,'images/Risk.gif')]")
            os.makedirs(download_path_RISK)
            driver.execute_cdp_cmd('Page.setDownloadBehavior', {
            'behavior': 'allow', 'downloadPath':  "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\PDF\\"+proposal_number_dir+'\\RISK'
            })     
            RISK.click()
            print(f"Downloading Risk Assessment Report for {proposal_number}")
            time.sleep(1)
            download_wait(download_path_RISK)
            
        except:
            pass

        try:
            download_path_ADD = download_path+'/ADD'
            
            ADD = driver.find_element_by_xpath("//a/img[contains(@src,'images/add.png')]")
            os.makedirs(download_path_ADD)
            driver.execute_cdp_cmd('Page.setDownloadBehavior', {
            'behavior': 'allow', 'downloadPath':  "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\PDF\\"+proposal_number_dir+'\\ADD'
            })    
            ADD.click()
            print(f"Downloading Additional Information for {proposal_number}")
            time.sleep(1)
            download_wait(download_path_ADD)
            
        except:
            pass

        
        try:
            download_path_COVER = download_path+'/COVER'
            
            COVER = driver.find_element_by_xpath("//a/img[contains(@src,'images/coverletter1.jpg')]")
            os.makedirs(download_path_COVER)
            driver.execute_cdp_cmd('Page.setDownloadBehavior', {
            'behavior': 'allow', 'downloadPath':  "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\PDF\\"+proposal_number_dir+'\\COVER'
            })    
            COVER.click()
            print(f"Downloading Cover Letter for {proposal_number}")
            time.sleep(1)
            download_wait(download_path_COVER)
            
        except:
            pass

        

        try:
            download_path_REJECT = download_path+'/REJECT'
            
            REJECT = driver.find_element_by_xpath("//a/img[contains(@src,'images/rejected.png')]")
            os.makedirs(download_path_REJECT)
            driver.execute_cdp_cmd('Page.setDownloadBehavior', {
            'behavior': 'allow', 'downloadPath':  "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\PDF\\"+proposal_number_dir+'\\REJECT'
            })    
            REJECT.click()
            print(f"Downloading Rejection Letter for {proposal_number}")
            time.sleep(1)
            download_wait(download_path_REJECT)
        
        except:
            pass


    except:
        print(f"PAGE ERROR - Check if Parivesh \n Proposal Number: {unique_proposals['Proposal.No.'][proposal_number]}")
        pass
