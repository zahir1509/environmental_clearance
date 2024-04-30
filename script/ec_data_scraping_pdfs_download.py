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
unique_proposals = unique_proposals.drop_duplicates(subset=['Proposal.No.'], keep='first')
print('AFTER DUPLICATES REMOVED')
print(len(unique_proposals))

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
'''
def download_wait(directory, timeout=5, nfiles=1):
    
    # Wait for downloads to finish with a specified timeout.

    # Args
    # directory : str
    #    The path to the folder where the files will be downloaded.
    # timeout : int
    #    How many seconds to wait until timing out.
    # nfiles : int, defaults to None
    #    If provided, also wait for the expected number of files.

    
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            time.sleep(1)
            dl_wait = False
            files = os.listdir(directory)
            if nfiles and len(files) != nfiles:
                dl_wait = True

            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True

            seconds += 1
        return seconds
'''

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

def get_last_filename_and_rename(save_folder, new_filename): # Returns to one parent folder
    files = glob.glob(save_folder + '/*')
    max_file = max(files, key=os.path.getctime)
    filename = max_file.split("/")[-1].split(".")[0]
    new_path = max_file.replace(filename, new_filename)
    os.rename(max_file, new_path)
    return new_path

def get_last_pdf_and_rename(save_folder, new_filename):
    pdf_files = glob.glob(os.path.join(save_folder, '*.pdf'))

    if not pdf_files:
        return None  # No PDF files in the folder

    latest_pdf = max(pdf_files, key=os.path.getctime)
    filename = os.path.basename(latest_pdf).split(".")[0]
    new_path = os.path.join(save_folder, new_filename + os.path.splitext(latest_pdf)[1])

    try:
        os.replace(latest_pdf, new_path)
    except Exception as e:
        print(f"Error during file renaming: {e}")
        return None

    return new_path


def get_last_pdf_and_rename_p(save_folder, new_filename): # Saves to one parent above
    pdf_files = glob.glob(save_folder+'/*.pdf')
    pdf_files = [file for file in pdf_files if os.path.basename(file) == "DownloadPfdFile.pdf"]
    if not pdf_files:
        return None  # No PDF files in the folder
    latest_pdf = max(pdf_files, key=os.path.getctime)
    filename = latest_pdf.split("/")[-1].split(".")[0]
    new_path = latest_pdf.replace(filename, new_filename)

    os.replace(latest_pdf, new_path) # change to os.rename if not working
    return new_path
'''
def get_last_filename_and_rename(save_folder, new_filename):
    files = glob.glob(save_folder + '/*')
    
    if not files:
        return None  # No files in the folder
    
    max_file = max(files, key=os.path.getctime)
    filename = os.path.basename(max_file).split(".")[0]
    new_path = os.path.join(save_folder, new_filename + os.path.splitext(max_file)[1])
    
    os.rename(max_file, new_path)
    return new_path
'''
#exception proposal = 1695 Odisha 
for proposal_number in range(48,len(unique_proposals['Proposal.No.'])): 
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
    
    table = soup.find("table",{"id":"ctl00_ContentPlaceHolder1_GridView1"})
    
    #headers = [header.text for header in table.find_all('th')]
    
    dom = etree.HTML(str(soup))
    
    #Proposal Number 
    print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text)
    proposal_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text


    # Replace '/' in proposal number with '_'
    proposal_number_dir = proposal_number.replace('/','_')
    
    # Create a directory by the name of the proposal number
    directory_pdf_root = "C:/Users/"+username+"/Dropbox/Environment_Clearance/"+directory_name+"/PDF"
    if not os.path.exists(directory_pdf_root+'/'+proposal_number_dir):
        os.makedirs(directory_pdf_root+'/'+proposal_number_dir+'/temp')
    
    # Set the download directory to the proposal number directory
    #prefs = {"download.default_directory" : directory_pdf_root+'/'+proposal_number_dir}
    download_path = directory_pdf_root+'/'+proposal_number_dir
    download_path_temp = directory_pdf_root+'/'+proposal_number_dir+'/temp'
    #params = { 'behavior': 'allow', 'downloadPath': download_path }
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {
        'behavior': 'allow', 'downloadPath':  "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\PDF\\"+proposal_number_dir+'\\temp'
        })    

    time.sleep(1)
    
    try:
        # EIA report
        # Download the pdf file open
        # Will happen by default since the chrome settings are set to open pdf externally and not embed
        EIA = driver.find_element_by_xpath("//a/img[contains(@src,'images/eia.png')]")
        EIA.click()
        time.sleep(1)
        # Wait for the download to complete 
        download_wait(download_path)
        time.sleep(2)
        # Rename the file to the proposal number_EIA.pdf
        get_last_pdf_and_rename_p(download_path_temp, proposal_number_dir+'_EIA')
        time.sleep(2)
    except:
        pass


    try:
        #Risk Asssessment Report
        
        RISK = driver.find_element_by_xpath("//a/img[contains(@src,'images/Risk.gif')]")
        RISK.click()
        time.sleep(1)
        download_wait(download_path)
        time.sleep(2)
        get_last_pdf_and_rename_p(download_path_temp, proposal_number_dir+'_RISK')
        time.sleep(2)
    except:
        pass

    try:
        ADD = driver.find_element_by_xpath("//a/img[contains(@src,'images/add.png')]")
        ADD.click()
        time.sleep(1)
        download_wait(download_path)
        time.sleep(2)
        get_last_pdf_and_rename_p(download_path_temp, proposal_number_dir+'_ADD')
        time.sleep(2)
    except:
        pass

    
    try:
        COVER = driver.find_element_by_xpath("//a/img[contains(@src,'images/coverletter1.jpg')]")
        COVER.click()
        time.sleep(1)
        download_wait(download_path)
        time.sleep(2)
        get_last_pdf_and_rename_p(download_path_temp, proposal_number_dir+'_COVER')
        time.sleep(2)
    except:
        pass

    '''
    try:
        EC_letter = driver.find_element_by_xpath("//a/img[contains(@src,'images/ec.png')]")
        EC_letter.click()
        time.sleep(1)
        download_wait(download_path)
        time.sleep(2)
        get_last_pdf_and_rename_p(download_path_temp, proposal_number_dir+'_EC')
        time.sleep(2)
    except:
        pass
    '''

    try:
        REJECT = driver.find_element_by_xpath("//a/img[contains(@src,'images/rejected.png')]")
        REJECT.click()
        time.sleep(1)
        download_wait(download_path)
        time.sleep(2)
        get_last_pdf_and_rename_p(download_path_temp, proposal_number_dir+'_REJECT')
        time.sleep(2)
    except:
        pass


    try: 
    # Delete the temp folder
        os.rmdir(download_path_temp)
    except:
        pass



    '''

    
    ##Convert into Dataframe 
    data_ec_closed_df=pd.DataFrame(data_ec_closed)
    data_ec_closed_df.columns=['Proposal','File_No','Proposal Name','State','District','Tehsil','Date_1','Date_2','Category','Company','Status']
    ##write to Dropbox
    csvfile = directory+'/'+directory_name+'/'+directory_name+'_ec_maindata'+'.csv'
    data_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')








    driver.switch_to.window(driver.window_handles[1])

    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])










    try:    
        kml_download = driver.find_element_by_xpath("//a/img[contains(@src,'images/download.png')]")
        kml_download.click()

        time.sleep(2)

        filepath = "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\KML\\"
        list_of_files = glob.glob(directory+'/'+directory_name+'/KML/*.kml') 
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)

    except:
        latest_file = ''

    data_ec_form2.append([proposal_number,name_proj,name_company,reg_address,legal_status_of_company,name_applicant,designation_applicant,address_applicant,pincode_applicant,email_applicant,tel_applicant,major_activity,minor_activity,project_category,proposal_number2,master_proposal_number,EAC_concerned_proj_A,project_type,plot_no,pincode_proj, from_n_degrees, from_n_mins, from_n_secs, to_n_degrees, to_n_mins, to_n_secs, from_e_degrees, from_e_mins, from_e_secs, to_e_degrees, to_e_mins, to_e_secs, soi_topo_sheet_no, AMSL, nearest_hfl, seismic_zone, state_name, dist_name, tehesil_name, village_name, latest_file])



    data_ec_form2_df=pd.DataFrame(data_ec_form2)
    data_ec_form2_df.columns = ['Proposal','Name of the project(s)','Name of the Company','Registered Address','Legal Status of Company','Name of the Applicant','Designation','Address','Pincode','Email','Telephone','Major Project/Activity','Minor Project/Activity','Project Category','Proposal Number','Master Proposal Number','EAC concerned Project Authority','Project Type','Plot/Survey/Khasra No.','Pincode', 'From N Degrees', 'From N Mins', 'From N Secs', 'To N Degrees', 'To N Mins', 'To N Secs', 'From E Degrees', 'From E Mins', 'From E Secs', 'To E Degrees', 'To E Mins', 'To E Secs', 'SOI/Topo Sheet No.', 'AMSL', 'Nearest HFL', 'Seismic Zone', 'State', 'District', 'Tehsil', 'Village', 'KML']
    csvfile2 = directory+'/'+directory_name+'/'+directory_name+'_ec_form2data'+'.csv'
    data_ec_form2_df.to_csv(csvfile2,encoding='utf-8-sig')


    # DOWNLOAD THE KML FILE


    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    '''


##Convert into Dataframe 
#links_ec_closed_df=pd.DataFrame(links_documents_df)
#links_ec_closed_df_pid=pd.DataFrame(links_proposal_df)

##write to Dropbox
#csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_ec_complete_links'+'.csv'
#links_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')

#csvfile = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/'+'Odisha_ec_complete_links_pid'+'.csv'
#links_ec_closed_df_pid.to_csv(csvfile,encoding='utf-8-sig')