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
from lxml import etree
import re

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

#manually navigate to the page and search for "a"
directory = "C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance"
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


data_ec_closed=[]

#data_ec_closed_df = pd.DataFrame(columns=['Proposal','File_No','State','District','Tehsil','Category','Company','Status'])
#pd.DataFrame()
#data_ec_closed_df.columns=['Proposal','File_No','State','District','Tehsil','Category','Company','Status']
#
links_documents_df=[]
links_proposal_df=[]

#links_documents_df=pd.DataFrame(columns=['Link','Proposal'])
for index in ['02','03','04','05','06','07','08','09','10','11']: 
    print(index)
    
    try:
       next_button = WebDriverWait(driver, 10).until(
           EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_grdevents_ctl%s_lnkDelete" % index))
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
    
    table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1"})
    
    #headers = [header.text for header in table.find_all('th')]
    
    dom = etree.HTML(str(soup))
    
    #Proposal Number 
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text)
    proposal_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text
    #data_ec_closed_df['Proposal'].append(proposal_number)
    
    #File Number //*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_fn")]
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_fn")]')[0].text)
    file_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_fn")]')[0].text
    #data_ec_closed_df['File_No'].append(file_number)
    
    
    #State Name//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_stdname1")]
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_stdname1")]')[0].text)
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lbldis1")]')[0].text)
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lblvill1")]')[0].text)
    state=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_stdname1")]')[0].text
    district=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lbldis1")]')[0].text
    tehsil=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lblvill1")]')[0].text
    
    #data_ec_closed_df['State'].append(state)
    #data_ec_closed_df['District'].append(district)
    #data_ec_closed_df['Tehsil'].append(tehsil)
    
    #Date ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml
    date_table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml"})
    span = soup.find("span", id="ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml")
    a= re.search('^(Date of.*)(Date of.*)',span.text).group(1)
    b= re.search('^(Date of.*)(Date of.*)',span.text).group(2)
    
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml")]')[0].text)
    
    #Categiry //*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_dst")]
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_dst")]')[0].text)
    category=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_dst")]')[0].text
    #data_ec_closed_df['Category'].append(category)
    
    #Company Proponent 
    #//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_uag")]
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_uag")]')[0].text)
    company=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_uag")]')[0].text
    #data_ec_closed_df['Company'].append(company)
    
    #Current Status
    #//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label1")]
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label1")]')[0].text)
    status=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label1")]')[0].text
    #data_ec_closed_df['Status'].append(status)
    data_ec_closed.append([proposal_number,file_number,state,district,tehsil,a,b,category,company,status])
    
    links_documents = []
    for link in table.find_all('a', href=True):
        href = link.get("href")
        if href is not None:
            links_documents.append(href)
           
    
    links_documents_df.append(links_documents)
    
    links_proposal_df.append([proposal_number]*len(links_documents))
    
    driver.back()

##Loop across all pages 
##manually checked that there are 266 pages. Should be a better way to do this
for page_number in range(2,266): 
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
    
    #links_documents_df=pd.DataFrame(columns=['Link','Proposal'])
    for index in ['02','03','04','05','06','07','08','09','10','11']: 
        print(index)
        
        try:
           next_button = WebDriverWait(driver, 10).until(
               EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_grdevents_ctl%s_lnkDelete" % index))
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
        
        table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1"})
        
        #headers = [header.text for header in table.find_all('th')]
        
        dom = etree.HTML(str(soup))
        
        #Proposal Number 
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text)
        proposal_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text
        #data_ec_closed_df['Proposal'].append(proposal_number)
        
        #File Number //*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_fn")]
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_fn")]')[0].text)
        file_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_fn")]')[0].text
        #data_ec_closed_df['File_No'].append(file_number)
        
        
        #State Name//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_stdname1")]
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_stdname1")]')[0].text)
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lbldis1")]')[0].text)
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lblvill1")]')[0].text)
        state=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_stdname1")]')[0].text
        district=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lbldis1")]')[0].text
        tehsil=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lblvill1")]')[0].text
        
        #data_ec_closed_df['State'].append(state)
        #data_ec_closed_df['District'].append(district)
        #data_ec_closed_df['Tehsil'].append(tehsil)
        
        #Date ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml
        date_table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml"})
        span = soup.find("span", id="ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml")
        a= re.search('^(Date of.*)(Date of.*)',span.text).group(1)
        b= re.search('^(Date of.*)(Date of.*)',span.text).group(2)
        
        
        #Categiry //*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_dst")]
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_dst")]')[0].text)
        category=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_dst")]')[0].text
        #data_ec_closed_df['Category'].append(category)
        
        #Company Proponent 
        #//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_uag")]
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_uag")]')[0].text)
        company=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_uag")]')[0].text
        #data_ec_closed_df['Company'].append(company)
        
        #Current Status
        #//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label1")]
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label1")]')[0].text)
        status=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label1")]')[0].text
        
        #UID
        uid=str(page_number)+str(index)
        
        #data_ec_closed_df['Status'].append(status)
        data_ec_closed.append([uid,proposal_number,file_number,state,district,tehsil,a,b,category,company,status])
        
        links_documents = []
        for link in table.find_all('a', href=True):
            href = link.get("href")
            if href is not None:
                links_documents.append(href)
               
        
        links_documents_df.append(links_documents)
        
        links_proposal_df.append([proposal_number]*len(links_documents))
        
        driver.back()
    
    
    
    
    

    
##Convert into Dataframe 
data_ec_closed_df=pd.DataFrame(data_ec_closed)
data_ec_closed_df.columns=['UID','Proposal','File_No','State','District','Tehsil','Date_1','Date_2','Category','Company','Status']
##write to Dropbox
csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_ec_complete_data'+'.csv'
data_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')

##Convert into Dataframe 
links_ec_closed_df=pd.DataFrame(links_documents_df)
links_ec_closed_df_pid=pd.DataFrame(links_proposal_df)

##write to Dropbox
csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_ec_complete_links'+'.csv'
links_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')

csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_ec_complete_links_pid'+'.csv'
links_ec_closed_df_pid.to_csv(csvfile,encoding='utf-8-sig')