# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:40:31 2016

@author: anustubh
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxProfile
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
import csv
import time
import re

#from indic_transliteration import sanscript
#from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
#from transliterate import detect_language, translit, get_available_language_codes

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

#manually login
directory = "C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance"
os.chdir(directory)
#path_to_chromedriver = "C:/Users/anust/Documents/Download_Driver/chromedriver.exe"
#chromeOptions = webdriver.ChromeOptions()
#prefs = {"download.default_directory" : "C:/Users/anust/Downloads"}
#chromeOptions.add_experimental_option("prefs",prefs)
base_url='https://environmentclearance.nic.in/'  
url = 'https://environmentclearance.nic.in/online_track_proposal_state.aspx?role=1bBxLm4fi0IhYZ3iSjTUTC4AAor4+1Di6YcIT7OLhZw=&type=ZHv5PQmmkflHpFD1goMtPQ==&status=BOII5FUynjpl5RZJJ8nW1g==&statename=Orissa'

#payload = {'_EVENTTARGET': 'ctl00$ContentPlaceHolder1$GridView1', '_EVENTARGUMENT': 'Page$2'}
#response = requests.post(url, data=payload)
#print(response.content)

#driver = webdriver.Chrome(executable_path = path_to_chromedriver,port=0,chrome_options=chromeOptions, service_args=None, desired_capabilities=None, service_log_path=None)

driver.get(url)
time.sleep(5)

page_number=1

html = driver.page_source
soup = BeautifulSoup(html,'lxml')

soup = BeautifulSoup(driver.page_source,  "html.parser")

#table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1"})

table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_tbl"})


headers = [header.text for header in table.find_all('th')]

# create empty lists to store the table data and URLs
data = []
urls = []
links_documents = []
links_id= []
links_timeline = []
counter=0
# loop through each row in the table
for row in table.find_all('tr'):
    print(counter)
    counter=counter+1
    
    if len(row)==11:
        # create an empty list to store the row data
        print('Inside Main if')
        print(len(row))
        row_data = []
        if len(row.find_all('td'))==30:
            ##Proposal
            proposal_string = row.find_all('td')[1].text.strip().replace("\n", "").replace("\r", "")
            proposal_no = re.search(r'Proposal No\s*:\s*(.*)File No.*$', proposal_string).group(1)
            row_data.append(proposal_no)  
            file_no = re.search(r'^.*File No\s*:\s*(.*)Proposal Name.*$', proposal_string).group(1)
            row_data.append(file_no)  
            proposal_name= re.search(r'^.*Proposal Name\s*:\s*(.*)$', proposal_string).group(1)
            row_data.append(proposal_name)  
            ##Location
            ##Start with Proposal Details
            location_string = row.find_all('td')[11].text.strip().replace("\n", "").replace("\r", "")
            state = re.search(r'State\s*:\s*(.*)District.*$', location_string).group(1)
            row_data.append(state)  
            district = re.search(r'^.*District\s*:\s*(.*)Tehsil.*$', location_string).group(1)
            row_data.append(district)  
            tehsil= re.search(r'^.*Tehsil\s*:\s*(.*)$', location_string).group(1)
            row_data.append(tehsil)   
            ##Important Dates
            date_submission_string = row.find_all('td')[21].text.strip().replace("\n", "").replace("\r", "")
            date_submission= re.search(r'^Date of Submission \s*:\s*(.*)$', date_submission_string).group(1)
            row_data.append(date_submission) 
            row_data.append(" TOR Not Granted Yet") 
            ##Category
            category_string = row.find_all('td')[25].text.strip().replace("\n", "").replace("\r", "")
            row_data.append(category_string) 
            ##Company Proponent
            company_proponent=row.find_all('td')[26].text.strip().replace("\n", "").replace("\r", "")
            row_data.append(company_proponent) 
            ##Status 
            status=row.find_all('td')[27].text.strip().replace("\n", "").replace("\r", "")
            row_data.append(status) 
            for link in row.find_all('td')[28].find_all("a"):
                href = link.get("href")
                if href is not None:
                    links_documents.append(href)
                    links_id.append(proposal_no)
            for link in row.find_all('td')[29].find_all("a"):
                 href = link.get("href")
                 if href is not None:
                     links_timeline.append(href)
        
        elif len(row.find_all('td'))==33:
             proposal_string = row.find_all('td')[1].text.strip().replace("\n", "").replace("\r", "")
             proposal_no = re.search(r'Proposal No\s*:\s*(.*)File No.*$', proposal_string).group(1)
             row_data.append(proposal_no)  
             file_no = re.search(r'^.*File No\s*:\s*(.*)Proposal Name.*$', proposal_string).group(1)
             row_data.append(file_no)  
             proposal_name= re.search(r'^.*Proposal Name\s*:\s*(.*)$', proposal_string).group(1)
             row_data.append(proposal_name)  
             ##Location
             ##Start with Proposal Details
             location_string = row.find_all('td')[11].text.strip().replace("\n", "").replace("\r", "")
             state = re.search(r'State\s*:\s*(.*)District.*$', location_string).group(1)
             row_data.append(state)  
             district = re.search(r'^.*District\s*:\s*(.*)Tehsil.*$', location_string).group(1)
             row_data.append(district)  
             tehsil= re.search(r'^.*Tehsil\s*:\s*(.*)$', location_string).group(1)
             row_data.append(tehsil)   
             ##Important Dates
             date_submission_string = row.find_all('td')[21].text.strip().replace("\n", "").replace("\r", "")
             date_submission= re.search(r'^Date of Submission \s*:\s*(.*)Date of TOR Granted.*$', date_submission_string).group(1)
             row_data.append(date_submission) 
             tor_granted= re.search(r'.*Date of TOR Granted \s*:\s*(.*)$', date_submission_string).group(1)
             row_data.append(tor_granted) 
             ##Category
             category_string = row.find_all('td')[28].text.strip().replace("\n", "").replace("\r", "")
             row_data.append(category_string) 
             ##Company Proponent
             company_proponent=row.find_all('td')[29].text.strip().replace("\n", "").replace("\r", "")
             row_data.append(company_proponent) 
             ##Status 
             status=row.find_all('td')[30].text.strip().replace("\n", "").replace("\r", "")
             row_data.append(status) 
             for link in row.find_all('td')[31].find_all("a"):
                 href = link.get("href")
                 if href is not None:
                     links_documents.append(href)
                     links_id.append(proposal_no)
             for link in row.find_all('td')[32].find_all("a"):
                  href = link.get("href")
                  if href is not None:
                      links_timeline.append(href)
        data.append(row_data)
         
    elif len(row)!=11:
        print("Not in Main if")
        



df = pd.DataFrame(data)
df.columns = ['proposal_no','file_no','proposal_name','state','district','tehsil','date_submission','tor_approval','project_category','company_proponent','status']
df=df[1:]
csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_tor_'+str(page_number)+'.csv'
df.to_csv(csvfile,encoding='utf-8-sig')

links_documents_df=pd.DataFrame(links_documents)
links_documents_df['id']=links_id
links_documents_df['absolute_path']=base_url+links_documents_df[0]
csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_tor_document_links_'+str(page_number)+'.csv'
links_documents_df.to_csv(csvfile,encoding='utf-8-sig')

links_timeline_df=pd.DataFrame(links_timeline)
links_timeline_df['absolute_path']=base_url+links_timeline_df[0]
csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_tor_timeline_links_'+str(page_number)+'.csv'
links_timeline_df.to_csv(csvfile,encoding='utf-8-sig')

#Click onnext page 
for page_number in range(12,24): 
    print('Page Number is',page_number)
    time.sleep(20)
   

      
   
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



    time.sleep(20)


   #Get all links 
    
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    
    soup = BeautifulSoup(driver.page_source,  "html.parser")
    
    #table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1"})
    
    table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_tbl"})
    
    
    headers = [header.text for header in table.find_all('th')]
    
    # create empty lists to store the table data and URLs
    data = []
    urls = []
    links_documents = []
    links_id= []
    links_timeline = []
    counter=0
    # loop through each row in the table
    for row in table.find_all('tr'):
        print(counter)
        counter=counter+1
        
        if len(row)==11:
            # create an empty list to store the row data
            print('Inside Main if')
            print(len(row))
            row_data = []
            if len(row.find_all('td'))==30:
                ##Proposal
                proposal_string = row.find_all('td')[1].text.strip().replace("\n", "").replace("\r", "")
                proposal_no = re.search(r'Proposal No\s*:\s*(.*)File No.*$', proposal_string).group(1)
                row_data.append(proposal_no)  
                file_no = re.search(r'^.*File No\s*:\s*(.*)Proposal Name.*$', proposal_string).group(1)
                row_data.append(file_no)  
                proposal_name= re.search(r'^.*Proposal Name\s*:\s*(.*)$', proposal_string).group(1)
                row_data.append(proposal_name)  
                ##Location
                ##Start with Proposal Details
                location_string = row.find_all('td')[11].text.strip().replace("\n", "").replace("\r", "")
                state = re.search(r'State\s*:\s*(.*)District.*$', location_string).group(1)
                row_data.append(state)  
                district = re.search(r'^.*District\s*:\s*(.*)Tehsil.*$', location_string).group(1)
                row_data.append(district)  
                tehsil= re.search(r'^.*Tehsil\s*:\s*(.*)$', location_string).group(1)
                row_data.append(tehsil)   
                ##Important Dates
                date_submission_string = row.find_all('td')[21].text.strip().replace("\n", "").replace("\r", "")
                date_submission= re.search(r'^Date of Submission \s*:\s*(.*)$', date_submission_string).group(1)
                row_data.append(date_submission) 
                row_data.append(" TOR Not Granted Yet") 
                ##Category
                category_string = row.find_all('td')[25].text.strip().replace("\n", "").replace("\r", "")
                row_data.append(category_string) 
                ##Company Proponent
                company_proponent=row.find_all('td')[26].text.strip().replace("\n", "").replace("\r", "")
                row_data.append(company_proponent) 
                ##Status 
                status=row.find_all('td')[27].text.strip().replace("\n", "").replace("\r", "")
                row_data.append(status) 
                for link in row.find_all('td')[28].find_all("a"):
                    href = link.get("href")
                    if href is not None:
                        links_documents.append(href)
                        links_id.append(proposal_no)
                for link in row.find_all('td')[29].find_all("a"):
                     href = link.get("href")
                     if href is not None:
                         links_timeline.append(href)
            
            elif len(row.find_all('td'))==33:
                 proposal_string = row.find_all('td')[1].text.strip().replace("\n", "").replace("\r", "")
                 proposal_no = re.search(r'Proposal No\s*:\s*(.*)File No.*$', proposal_string).group(1)
                 row_data.append(proposal_no)  
                 file_no = re.search(r'^.*File No\s*:\s*(.*)Proposal Name.*$', proposal_string).group(1)
                 row_data.append(file_no)  
                 proposal_name= re.search(r'^.*Proposal Name\s*:\s*(.*)$', proposal_string).group(1)
                 row_data.append(proposal_name)  
                 ##Location
                 ##Start with Proposal Details
                 location_string = row.find_all('td')[11].text.strip().replace("\n", "").replace("\r", "")
                 state = re.search(r'State\s*:\s*(.*)District.*$', location_string).group(1)
                 row_data.append(state)  
                 district = re.search(r'^.*District\s*:\s*(.*)Tehsil.*$', location_string).group(1)
                 row_data.append(district)  
                 tehsil= re.search(r'^.*Tehsil\s*:\s*(.*)$', location_string).group(1)
                 row_data.append(tehsil)   
                 ##Important Dates
                 date_submission_string = row.find_all('td')[21].text.strip().replace("\n", "").replace("\r", "")
                 date_submission= re.search(r'^Date of Submission \s*:\s*(.*)Date of TOR Granted.*$', date_submission_string).group(1)
                 row_data.append(date_submission) 
                 tor_granted= re.search(r'.*Date of TOR Granted \s*:\s*(.*)$', date_submission_string).group(1)
                 row_data.append(tor_granted) 
                 ##Category
                 category_string = row.find_all('td')[28].text.strip().replace("\n", "").replace("\r", "")
                 row_data.append(category_string) 
                 ##Company Proponent
                 company_proponent=row.find_all('td')[29].text.strip().replace("\n", "").replace("\r", "")
                 row_data.append(company_proponent) 
                 ##Status 
                 status=row.find_all('td')[30].text.strip().replace("\n", "").replace("\r", "")
                 row_data.append(status) 
                 for link in row.find_all('td')[31].find_all("a"):
                     href = link.get("href")
                     if href is not None:
                         links_documents.append(href)
                         links_id.append(proposal_no)
                 for link in row.find_all('td')[32].find_all("a"):
                      href = link.get("href")
                      if href is not None:
                          links_timeline.append(href)
            data.append(row_data)
             
        elif len(row)!=11:
            print("Not in Main if")
            
    
    
    
    df = pd.DataFrame(data)
    df.columns = ['proposal_no','file_no','proposal_name','state','district','tehsil','date_submission','tor_approval','project_category','company_proponent','status']
    df=df[1:]
    csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_tor_'+str(page_number)+'.csv'
    df.to_csv(csvfile,encoding='utf-8-sig')
   
    links_documents_df=pd.DataFrame(links_documents)
    links_documents_df['id']=links_id
    links_documents_df['absolute_path']=base_url+links_documents_df[0]
    csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_tor_document_links_'+str(page_number)+'.csv'
    links_documents_df.to_csv(csvfile,encoding='utf-8-sig')

    links_timeline_df=pd.DataFrame(links_timeline)
    links_timeline_df['absolute_path']=base_url+links_timeline_df[0]
    csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_tor_timeline_links_'+str(page_number)+'.csv'
    links_timeline_df.to_csv(csvfile,encoding='utf-8-sig')
    
    
    driver.get(url)
    print('Getting the url again')
    time.sleep(10)