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
import warnings

from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore", category=DeprecationWarning)

#######################################################################################################

state_name='Telangana'
directory_name='Telangana'

#######################################################################################################

#driver = webdriver.Chrome(ChromeDriverManager().install())

username = os.getlogin()
print(username)

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:\\Users\\"+username+"\\Dropbox\\agnihotri_gupta\\Environment_Clearance\\"+directory_name+"\\KML\\"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chromeOptions)
url = 'https://environmentclearance.nic.in/proposal_status_state.aspx?pid=ClosedEC&statename='+state_name


#manually navigate to the page and search for "a"
# get the system username

directory = "C:/Users/"+username+"/Dropbox/agnihotri_gupta/Environment_Clearance"
os.chdir(directory)

##Name of State
##Make sure you create directory

unique_proposals=pd.read_csv(directory+'/'+directory_name+'/'+directory_name+'_ec_complete_unique.csv')

print(f'Number of Proposals: {len(unique_proposals)}')

unique_proposals['Form_Type']=" "
'''
print(unique_proposals)

print(unique_proposals)
print('BEFORE DUPLICATES REMOVED')
print(len(unique_proposals))



# Remove all rows with duplicate proposal numbers
unique_proposals.drop_duplicates(subset=['Proposal.No.'], inplace=True)
unique_proposals.reset_index(drop=True, inplace=True)
print('AFTER DUPLICATES REMOVED')
print(len(unique_proposals))
'''


## DATAFRAMES FOR STORING DATA
data_ec_closed = [] # Main page data
data_ec_timeline = [] # Timeline data
data_ec_form = [] # Detail form data - 1,2,Parivesh, Parivesh 2, Missing data
data_ec_formtype = [] # Form type data


## FUNCTION DEFINITIONS FOR SCRAPING MAIN PAGE AND DIFFERENT FORM TYPES

def scrape_main_page():
    main_page_url = driver.current_url
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    dom = etree.HTML(str(soup))

    proposal_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text
    file_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_fn")]')[0].text
    proposal_name = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label2")]')[0].text
    state=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_stdname1")]')[0].text
    district=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lbldis1")]')[0].text
    tehsil=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lblvill1")]')[0].text
    
    date_table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml"})
    span = soup.find("span", id="ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml")
    a= re.search('^(Date of.*)(Date of.*)',span.text).group(1)
    b= re.search('^(Date of.*)(Date of.*)',span.text).group(2)
    
    category=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_dst")]')[0].text
    company=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_uag")]')[0].text
    status=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label1")]')[0].text

    anchor_tag = soup.find('a', title='Timeline')
    timeline_found=0
    # Check if the anchor tag exists
    if anchor_tag:
        # Get the href attribute
        href = anchor_tag.get('href')
        timeline_link='https://environmentclearance.nic.in/'+href
        timeline_found=1
        
    else:
        print("Anchor tag with the specified title not found.")
        timeline_link=''
        timeline_found=0
 

    print(f"Proposal Number: {proposal_number}, \nFile Number: {file_number}, \nProposal Name: {proposal_name}, \nState: {state}, \nDistrict: {district}, \nTehsil: {tehsil}, \nDate_1: {a}, \nDate_2: {b}, \nCategory: {category}, \nCompany: {company}, \nStatus: {status}")
    data_ec_closed.append([proposal_number,file_number,proposal_name,state,district,tehsil,a,b,category,company,status,main_page_url,timeline_link])

    data_ec_closed_df=pd.DataFrame(data_ec_closed)
    data_ec_closed_df.columns=['Proposal.No.','File_No','Proposal Name','State','District','Tehsil','Date_1','Date_2','Category','Company','Status','Link','Timeline']
    ##write to Dropbox
    csvfile = directory+'/'+directory_name+'/'+directory_name+'_ec_maindata'+'.csv'
    data_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')

    if timeline_found == 1:
  
        driver.get(timeline_link)

        #time.sleep(2)
    
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        dom = etree.HTML(str(soup))
    
        print('..............TIMELINE DATA..............')

        proposal_number_tl = dom.xpath('//*[@id="plblproposal_no"]')[0].text
        project_name2 = dom.xpath('//*[@id="plblnameofproject"]')[0].text
        project_sector = dom.xpath('//*[@id="plblsector"]')[0].text
        date_submission = dom.xpath('//*[@id="plbldateofsum"]')[0].text
        submitted_by_proponent = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[1]')[0].text
        query_shortcoming_SEIAA = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[2]')[0].text
        resubmission1 = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[3]')[0].text
        accepted_date_SEIAA = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[4]')[0].text
        query_shortcoming_SEAC = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[5]')[0].text
        resubmission2 = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[6]')[0].text
        accepted_date_SEAC = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[7]')[0].text
        forwarded_date_SEIAA = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[8]')[0].text
        EC_letter_uploaded = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[9]')[0].text
        timeline_current_url = driver.current_url

        print(f"Proposal Number: {proposal_number_tl}, \nProject Name: {project_name2}, \nProject Sector: {project_sector}, \nDate of Submission: {date_submission}, \nSubmitted by Proponent: {submitted_by_proponent}, \nQuery for Shortcoming(if any) by SEIAA: {query_shortcoming_SEIAA}, \nResubmission of Proposal by Proponent 1: {resubmission1}, \nAccepted by SEIAA and forwarded to SEAC: {accepted_date_SEIAA}, \nQuery for Shortcoming(if any) by SEAC: {query_shortcoming_SEAC}, \nResubmission of Proposal by Proponent 2: {resubmission2}, \nAccepted by SEAC: {accepted_date_SEAC}, \nForwarded to SEIAA for EC: {forwarded_date_SEIAA}, \nEC Letter Uploaded On/EC Granted: {EC_letter_uploaded}")
        data_ec_timeline.append([proposal_number_tl,project_name2,project_sector,date_submission,submitted_by_proponent,query_shortcoming_SEIAA,resubmission1,accepted_date_SEIAA,query_shortcoming_SEAC,resubmission2,accepted_date_SEAC,forwarded_date_SEIAA,EC_letter_uploaded,timeline_current_url])
        data_ec_timeline_df=pd.DataFrame(data_ec_timeline)
        data_ec_timeline_df.columns = ['Proposal Number','Project Name','Project Sector','Date of Submission','Submitted by Proponent','Query for Shortcoming(if any) by SEIAA','Resubmission of Proposal by Proponent 1','Accepted by SEIAA and forwarded to SEAC','Query for Shortcoming(if any) by SEAC','Resubmission of Proposal by Proponent 2','Accepted by SEAC','Forwarded to SEIAA for EC','EC Letter Uploaded On/EC Granted','Link']
    
        csvfile_timeline = directory+'/'+directory_name+'/'+directory_name+'_ec_timelinedata'+'.csv'
        data_ec_timeline_df.to_csv(csvfile_timeline,encoding='utf-8-sig')
        
    else:
       
       proposal_number_tl = proposal_number
       project_name2 = proposal_name
       project_sector = ''
       date_submission = ''
       submitted_by_proponent =''
       query_shortcoming_SEIAA = ''
       resubmission1 = ''
       accepted_date_SEIAA = ''
       query_shortcoming_SEAC = ''
       resubmission2 = ''
       accepted_date_SEAC = ''
       forwarded_date_SEIAA = ''
       EC_letter_uploaded = ''
       timeline_current_url = ''
    
       print(f"Proposal Number: {proposal_number_tl}, \nProject Name: {project_name2}, \nProject Sector: {project_sector}, \nDate of Submission: {date_submission}, \nSubmitted by Proponent: {submitted_by_proponent}, \nQuery for Shortcoming(if any) by SEIAA: {query_shortcoming_SEIAA}, \nResubmission of Proposal by Proponent 1: {resubmission1}, \nAccepted by SEIAA and forwarded to SEAC: {accepted_date_SEIAA}, \nQuery for Shortcoming(if any) by SEAC: {query_shortcoming_SEAC}, \nResubmission of Proposal by Proponent 2: {resubmission2}, \nAccepted by SEAC: {accepted_date_SEAC}, \nForwarded to SEIAA for EC: {forwarded_date_SEIAA}, \nEC Letter Uploaded On/EC Granted: {EC_letter_uploaded}")
       data_ec_timeline.append([proposal_number_tl,project_name2,project_sector,date_submission,submitted_by_proponent,query_shortcoming_SEIAA,resubmission1,accepted_date_SEIAA,query_shortcoming_SEAC,resubmission2,accepted_date_SEAC,forwarded_date_SEIAA,EC_letter_uploaded,timeline_current_url])
       data_ec_timeline_df=pd.DataFrame(data_ec_timeline)
       data_ec_timeline_df.columns = ['Proposal Number','Project Name','Project Sector','Date of Submission','Submitted by Proponent','Query for Shortcoming(if any) by SEIAA','Resubmission of Proposal by Proponent 1','Accepted by SEIAA and forwarded to SEAC','Query for Shortcoming(if any) by SEAC','Resubmission of Proposal by Proponent 2','Accepted by SEAC','Forwarded to SEIAA for EC','EC Letter Uploaded On/EC Granted','Link']
    
       csvfile_timeline = directory+'/'+directory_name+'/'+directory_name+'_ec_timelinedata'+'.csv'
       data_ec_timeline_df.to_csv(csvfile_timeline,encoding='utf-8-sig')


for proposal_number in range(0, len(unique_proposals['Proposal.No.'])):
    print('----------------------------------------------------------')
    print(f'Index: {proposal_number}')
    print(f'Proposal Number: {unique_proposals["Proposal.No."][proposal_number]}')
    #current_formtype = unique_proposals['FormType'][proposal_number]
    driver.get(url)

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
    
    #time.sleep(1)
    
    ### Click on more information to go to main page
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
    
    #time.sleep(1)
    
    if "parivesh.nic.in" in driver.current_url:
     formtype = 'Parivesh-2'
     unique_proposals['Form_Type'][proposal_number] = " Parivesh-2"
     print(formtype)   
           
    else:
   
        # For Main Page
        scrape_main_page()
    
        # For Timeline Data
        #scrape_timeline_data()



csvfile = directory+'/'+directory_name+'/'+directory_name+'_ec_complete_unique_formtype.csv'
unique_proposals.to_csv(csvfile,encoding='utf-8-sig')
    
        