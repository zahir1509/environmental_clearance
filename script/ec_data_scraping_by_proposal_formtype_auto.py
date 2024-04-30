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

state_name='Orissa'
directory_name='Orissa'

#######################################################################################################

#driver = webdriver.Chrome(ChromeDriverManager().install())

username = os.getlogin()
print(username)

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\KML\\"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chromeOptions)
url = 'https://environmentclearance.nic.in/proposal_status_state.aspx?pid=ClosedEC&statename='+state_name


#manually navigate to the page and search for "a"
# get the system username

directory = "C:/Users/"+username+"/Dropbox/Environment_Clearance"
os.chdir(directory)

##Name of State
##Make sure you create directory

unique_proposals=pd.read_csv(directory+'/'+directory_name+'/'+directory_name+'_ec_complete_unique.csv')

print(f'Number of Proposals: {len(unique_proposals)}')

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

    print(f"Proposal Number: {proposal_number}, \nFile Number: {file_number}, \nProposal Name: {proposal_name}, \nState: {state}, \nDistrict: {district}, \nTehsil: {tehsil}, \nDate_1: {a}, \nDate_2: {b}, \nCategory: {category}, \nCompany: {company}, \nStatus: {status}")
    data_ec_closed.append([proposal_number,file_number,proposal_name,state,district,tehsil,a,b,category,company,status,main_page_url])

    data_ec_closed_df=pd.DataFrame(data_ec_closed)
    data_ec_closed_df.columns=['Proposal.No.','File_No','Proposal Name','State','District','Tehsil','Date_1','Date_2','Category','Company','Status','Link']
    ##write to Dropbox
    csvfile = directory+'/'+directory_name+'/'+directory_name+'_ec_maindata'+'.csv'
    data_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')

def scrape_timeline_data():
    timeline_icon = driver.find_element_by_xpath("//a/img[contains(@src,'images/tme.png')]")
    timeline_icon.click()

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(2)

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
    

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def scrape_form2_data():

    formtype = 'Form-2'

    EC2 = driver.find_element_by_xpath("//a/img[contains(@src,'images/ecreport1.jpg')]")
    EC2.click()

    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    dom = etree.HTML(str(soup))

    print('..............FORM 2 DATA..............')

    proposal_number1 = unique_proposals['Proposal.No.'][proposal_number]
    print(f'Proposal Number: {proposal_number1} || {formtype}')

    try:
        match_using_text = dom.xpath('//*[contains(text(), "(a)Name of the project(s)")]/../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        name_proj = match_using_text.xpath(xpath + "/tr[3]/td[2]")[0].text
        name_company = match_using_text.xpath(xpath + "/tr[4]/td[2]")[0].text
        reg_address = match_using_text.xpath(xpath + "/tr[5]/td[2]")[0].text
        legal_status_of_company = match_using_text.xpath(xpath + "/tr[6]/td[2]")[0].text

    except:
        name_proj = ''
        name_company = ''
        reg_address = ''
        legal_status_of_company = ''

    print(f"Name of the Project: {name_proj}, \nName of the Company: {name_company}, \nRegistered Address: {reg_address}, \nLegal Status of Company: {legal_status_of_company}")


    try:    
        match_using_text = dom.xpath('//*[contains(text(), "(a)Name of the Applicant")]/../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        name_applicant = match_using_text.xpath(xpath + "/tr[2]/td[2]")[0].text
        designation_applicant = match_using_text.xpath(xpath + "/tr[3]/td[2]")[0].text
        address_applicant = match_using_text.xpath(xpath + "/tr[4]/td[2]")[0].text
        pincode_applicant = match_using_text.xpath(xpath + "/tr[5]/td[2]")[0].text
        email_applicant = match_using_text.xpath(xpath + "/tr[6]/td[2]")[0].text
        tel_applicant = match_using_text.xpath(xpath + "/tr[7]/td[2]")[0].text
    except:
        name_applicant = ''
        designation_applicant = ''
        address_applicant = ''
        pincode_applicant = ''
        email_applicant = ''
        tel_applicant = ''
    
    print(f"Name of the Applicant: {name_applicant}, \nDesignation of the Applicant: {designation_applicant}, \nAddress of the Applicant: {address_applicant}, \nPincode of the Applicant: {pincode_applicant}, \nEmail of the Applicant: {email_applicant}, \nTelephone of the Applicant: {tel_applicant}")

    try:   
        match_using_text = dom.xpath('//*[contains(text(), "(a)Major Project/Activity")]/../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        major_activity = match_using_text.xpath(xpath + "/tr[2]/td[2]/b")[0].text
        minor_activity = match_using_text.xpath(xpath + "/tr[3]/td[2]/b")[0].text
        project_category = match_using_text.xpath(xpath + "/tr[4]/td[2]/b")[0].text
        proposal_number2 = match_using_text.xpath(xpath + "/tr[5]/td[2]/b")[0].text
        master_proposal_number = match_using_text.xpath(xpath + "/tr[6]/td[2]/b")[0].text
        EAC_concerned_proj_A = match_using_text.xpath(xpath + "/tr[7]/td[2]/b")[0].text
        project_type = match_using_text.xpath(xpath + "/tr[8]/td[2]/b")[0].text
    except:
        major_activity = ''
        minor_activity = ''
        project_category = ''
        proposal_number2 = ''
        master_proposal_number = ''
        EAC_concerned_proj_A = ''
        project_type = ''

    print(f"Major Project/Activity: {major_activity}, \nMinor Project/Activity: {minor_activity}, \nProject Category: {project_category}, \nProposal Number: {proposal_number2}, \nMaster Proposal Number: {master_proposal_number}, \nEAC Concerned Project A: {EAC_concerned_proj_A}, \nProject Type: {project_type}")

    try:     
        match_using_text = dom.xpath('//*[contains(text(), "(a)Plot/Survey/Khasra No.")]/../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        plot_no = match_using_text.xpath(xpath + "/tr[2]/td[2]")[0].text
        pincode_proj = match_using_text.xpath(xpath + "/tr[3]/td[2]")[0].text
        from_n_degrees = match_using_text.xpath(xpath + "/tr[6]/td[2]")[0].text
        from_n_mins = match_using_text.xpath(xpath + "/tr[7]/td[2]")[0].text
        from_n_secs = match_using_text.xpath(xpath + "/tr[8]/td[2]")[0].text
        to_n_degrees = match_using_text.xpath(xpath + "/tr[10]/td[2]")[0].text
        to_n_mins = match_using_text.xpath(xpath + "/tr[11]/td[2]")[0].text
        to_n_secs = match_using_text.xpath(xpath + "/tr[12]/td[2]")[0].text
        from_e_degrees = match_using_text.xpath(xpath + "/tr[15]/td[2]")[0].text
        from_e_mins = match_using_text.xpath(xpath + "/tr[16]/td[2]")[0].text
        from_e_secs = match_using_text.xpath(xpath + "/tr[17]/td[2]")[0].text
        to_e_degrees = match_using_text.xpath(xpath + "/tr[19]/td[2]")[0].text
        to_e_mins = match_using_text.xpath(xpath + "/tr[20]/td[2]")[0].text
        to_e_secs = match_using_text.xpath(xpath + "/tr[21]/td[2]")[0].text
        location_coordinates = from_n_degrees + '°' + from_n_mins + "'" + from_n_secs + '"' + 'N' + ' ' + from_e_degrees + '°' + from_e_mins + "'" + from_e_secs + '"' + 'E' + ' ' + to_n_degrees + '°' + to_n_mins + "'" + to_n_secs + '"' + 'N' + ' ' + to_e_degrees + '°' + to_e_mins + "'" + to_e_secs + '"' + 'E'
        soi_topo_sheet_no = match_using_text.xpath(xpath + "/tr[22]/td[2]")[0].text
        AMSL = match_using_text.xpath(xpath + "/tr[24]/td[2]")[0].text

        nearest_hfl = match_using_text.xpath(xpath + "/tr[26]/td[2]")[0].text
        seismic_zone = match_using_text.xpath(xpath + "/tr[27]/td[2]")[0].text
    
    except:
        plot_no = ''
        pincode_proj = ''
        from_n_degrees = ''
        from_n_mins = ''
        from_n_secs = ''
        to_n_degrees = ''
        to_n_mins = ''
        to_n_secs = ''
        from_e_degrees = ''
        from_e_mins = ''
        from_e_secs = ''
        to_e_degrees = ''
        to_e_mins = ''
        to_e_secs = ''
        location_coordinates = ''
        soi_topo_sheet_no = ''
        AMSL = ''
        nearest_hfl = ''
        seismic_zone = ''

    print(f"Plot/Survey/Khasra No.: {plot_no}, \nPincode of Project: {pincode_proj}, \nFrom N Degrees: {from_n_degrees}, \nFrom N Minutes: {from_n_mins}, \nFrom N Seconds: {from_n_secs}, \nTo N Degrees: {to_n_degrees}, \nTo N Minutes: {to_n_mins}, \nTo N Seconds: {to_n_secs}, \nFrom E Degrees: {from_e_degrees}, \nFrom E Minutes: {from_e_mins}, \nFrom E Seconds: {from_e_secs}, \nTo E Degrees: {to_e_degrees}, \nTo E Minutes: {to_e_mins}, \nTo E Seconds: {to_e_secs}, \nLocation: {location_coordinates}, \nSOI Topo Sheet No.: {soi_topo_sheet_no}, \nAMSL: {AMSL}, \nNearest HFL: {nearest_hfl}, \nSeismic Zone: {seismic_zone}")



    try:
        match_using_text = dom.xpath('//*[contains(text(), "Details of State(s) of the project")]/../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        state_name = match_using_text.xpath(xpath + "/tr[3]/td[2]/span")[0].text
        dist_name = match_using_text.xpath(xpath + "/tr[3]/td[3]/span")[0].text
        tehesil_name = match_using_text.xpath(xpath + "/tr[3]/td[4]")[0].text
        village_name = match_using_text.xpath(xpath + "/tr[3]/td[5]")[0].text

    except:
        state_name = ''
        dist_name = ''
        tehesil_name = ''
        village_name = ''

    print(f"State Name: {state_name}, \nDistrict Name: {dist_name}, \nTehsil Name: {tehesil_name}, \nVillage Name: {village_name}")

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

    print(f"KML File: {latest_file}")

    form2url = driver.current_url

    data_ec_form.append([proposal_number1, formtype, name_proj,name_company,reg_address,legal_status_of_company,name_applicant,designation_applicant,address_applicant,pincode_applicant,email_applicant,tel_applicant,major_activity,minor_activity,project_category,proposal_number2,master_proposal_number,EAC_concerned_proj_A,project_type,plot_no,pincode_proj,from_n_degrees,from_n_mins,from_n_secs,to_n_degrees,to_n_mins,to_n_secs,from_e_degrees,from_e_mins,from_e_secs,to_e_degrees,to_e_mins,to_e_secs,location_coordinates,soi_topo_sheet_no,AMSL,nearest_hfl,seismic_zone,state_name,dist_name,tehesil_name,village_name,latest_file,form2url])
    data_ec_form_df=pd.DataFrame(data_ec_form)
    data_ec_form_df.columns = ['Proposal.No.', 'FormType' ,'Name of the Project','Name of the Company','Registered Address','Legal Status of Company','Name of the Applicant','Designation of the Applicant','Address of the Applicant','Pincode of the Applicant','Email of the Applicant','Telephone of the Applicant','Major Project/Activity','Minor Project/Activity','Project Category','Proposal Number','Master Proposal Number','EAC Concerned Project A','Project Type','Plot/Survey/Khasra No.','Pincode of Project','From N Degrees','From N Minutes','From N Seconds','To N Degrees','To N Minutes','To N Seconds','From E Degrees','From E Minutes','From E Seconds','To E Degrees','To E Minutes','To E Seconds','Location Coordinates','SOI Topo Sheet No.','AMSL','Nearest HFL','Seismic Zone','State Name','District Name','Tehsil Name','Village Name','KML File','Link']

    csvfile_formdata = directory+'/'+directory_name+'/'+directory_name+'_ec_formdata'+'.csv'
    data_ec_form_df.to_csv(csvfile_formdata,encoding='utf-8-sig')

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def scrape_form1_data():

    formtype = 'Form-1'

    EC2 = driver.find_element_by_xpath("//a/img[contains(@src,'images/ecreport1.jpg')]")
    EC2.click()

    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    dom = etree.HTML(str(soup))

    print('..............FORM 1 DATA..............')

    proposal_number1 = unique_proposals['Proposal.No.'][proposal_number]
    print(f'Proposal Number: {proposal_number1} || {formtype}')

    try:
        match_using_text = dom.xpath('//*[contains(text(), "Project Name")]/../../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        name_proj = match_using_text.xpath(xpath + "/tr[1]/td[2]")[0].text
        name_company = match_using_text.xpath(xpath + "/tr[1]/td[4]")[0].text
        reg_address = match_using_text.xpath(xpath + "/tr[2]/td[2]")[0].text
        legal_status_of_company = match_using_text.xpath(xpath + "/tr[2]/td[4]")[0].text

    except:
        name_proj = ''
        name_company = ''
        reg_address = ''
        legal_status_of_company = ''
    
    
    print(f"Name of the Project: {name_proj}, \nName of the Company: {name_company}, \nRegistered Address: {reg_address}, \nLegal Status of Company: {legal_status_of_company}")

    try:
        match_using_text = dom.xpath('//*[contains(text(), "Name of the Applicant")]/../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        name_applicant = match_using_text.xpath(xpath + "/tr[2]/td[2]")[0].text
        designation_applicant = match_using_text.xpath(xpath + "/tr[3]/td[2]")[0].text
        address_applicant = match_using_text.xpath(xpath + "/tr[4]/td[2]")[0].text
        pincode_applicant = match_using_text.xpath(xpath + "/tr[5]/td[2]")[0].text
        email_applicant = match_using_text.xpath(xpath + "/tr[6]/td[2]")[0].text
        tel_applicant = match_using_text.xpath(xpath + "/tr[7]/td[2]")[0].text
    except:
        name_applicant = ''
        designation_applicant = ''
        address_applicant = ''
        pincode_applicant = ''
        email_applicant = ''
        tel_applicant = ''

    print(f"Name of the Applicant: {name_applicant}, \nDesignation of the Applicant: {designation_applicant}, \nAddress of the Applicant: {address_applicant}, \nPincode of the Applicant: {pincode_applicant}, \nEmail of the Applicant: {email_applicant}, \nTelephone of the Applicant: {tel_applicant}")

    try:
        match_using_text = dom.xpath('//*[contains(text(), "Major Project/Activity")]/../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        major_activity = match_using_text.xpath(xpath + "/tr[2]/td[2]/b")[0].text
        minor_activity = match_using_text.xpath(xpath + "/tr[3]/td[2]/b")[0].text
        project_category = match_using_text.xpath(xpath + "/tr[4]/td[2]/b")[0].text
        proposal_number2 = match_using_text.xpath(xpath + "/tr[5]/td[2]/b")[0].text
        master_proposal_number = match_using_text.xpath(xpath + "/tr[6]/td[2]/b")[0].text
        EAC_concerned_proj_A = match_using_text.xpath(xpath + "/tr[7]/td[2]/b")[0].text
        project_type = match_using_text.xpath(xpath + "/tr[8]/td[2]/b")[0].text
    except:
        major_activity = ''
        minor_activity = ''
        project_category = ''
        proposal_number2 = ''
        master_proposal_number = ''
        EAC_concerned_proj_A = ''
        project_type = ''

    print(f"Major Project/Activity: {major_activity}, \nMinor Project/Activity: {minor_activity}, \nProject Category: {project_category}, \nProposal Number: {proposal_number2}, \nMaster Proposal Number: {master_proposal_number}, \nEAC Concerned Project A: {EAC_concerned_proj_A}, \nProject Type: {project_type}")

    try:
        match_using_text = dom.xpath('//*[contains(text(), "Plot/Survey/Khasra No.")]/../../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        plot_no = match_using_text.xpath(xpath + "/tr[2]/td[4]")[0].text
        pincode_proj = match_using_text.xpath(xpath + "/tr[4]/td[4]")[0].text
        from_n_degrees = ""
        from_n_mins = ""
        from_n_secs = ""
        to_n_degrees = ""
        to_n_mins = ""
        to_n_secs = ""
        from_e_degrees = ""
        from_e_mins = ""
        from_e_secs = ""
        to_e_degrees = ""
        to_e_mins = ""
        to_e_secs = ""
        location_coordinates = match_using_text.xpath(xpath + "/tr[1]/td[2]")[0].text
        soi_topo_sheet_no = ""
        AMSL = ""
        nearest_hfl = ""
        seismic_zone = ""

    except:
        plot_no = ''
        pincode_proj = ''
        from_n_degrees = ''
        from_n_mins = ''
        from_n_secs = ''
        to_n_degrees = ''
        to_n_mins = ''
        to_n_secs = ''
        from_e_degrees = ''
        from_e_mins = ''
        from_e_secs = ''
        to_e_degrees = ''
        to_e_mins = ''
        to_e_secs = ''
        location_coordinates = ''
        soi_topo_sheet_no = ''
        AMSL = ''
        nearest_hfl = ''
        seismic_zone = ''

    print(f"Plot/Survey/Khasra No.: {plot_no}, \nPincode of Project: {pincode_proj}, \nFrom N Degrees: {from_n_degrees}, \nFrom N Minutes: {from_n_mins}, \nFrom N Seconds: {from_n_secs}, \nTo N Degrees: {to_n_degrees}, \nTo N Minutes: {to_n_mins}, \nTo N Seconds: {to_n_secs}, \nFrom E Degrees: {from_e_degrees}, \nFrom E Minutes: {from_e_mins}, \nFrom E Seconds: {from_e_secs}, \nTo E Degrees: {to_e_degrees}, \nTo E Minutes: {to_e_mins}, \nTo E Seconds: {to_e_secs}, \nLocation: {location_coordinates}, \nSOI Topo Sheet No.: {soi_topo_sheet_no}, \nAMSL: {AMSL}, \nNearest HFL: {nearest_hfl}, \nSeismic Zone: {seismic_zone}")

    try:
        match_using_text = dom.xpath('//*[contains(text(), "Details of State(s) of the project")]/../..')[0]
        xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
        state_name = match_using_text.xpath(xpath + "/tr[3]/td[2]/span")[0].text
        dist_name = match_using_text.xpath(xpath + "/tr[3]/td[3]/span")[0].text
        tehesil_name = match_using_text.xpath(xpath + "/tr[3]/td[4]")[0].text
        village_name = match_using_text.xpath(xpath + "/tr[3]/td[5]")[0].text
    except:
        state_name = ''
        dist_name = ''
        tehesil_name = ''
        village_name = ''

    print(f"State Name: {state_name}, \nDistrict Name: {dist_name}, \nTehsil Name: {tehesil_name}, \nVillage Name: {village_name}")

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
    
    print(f"KML File: {latest_file}")

    form1url = driver.current_url

    data_ec_form.append([proposal_number1, formtype, name_proj,name_company,reg_address,legal_status_of_company,name_applicant,designation_applicant,address_applicant,pincode_applicant,email_applicant,tel_applicant,major_activity,minor_activity,project_category,proposal_number2,master_proposal_number,EAC_concerned_proj_A,project_type,plot_no,pincode_proj,from_n_degrees,from_n_mins,from_n_secs,to_n_degrees,to_n_mins,to_n_secs,from_e_degrees,from_e_mins,from_e_secs,to_e_degrees,to_e_mins,to_e_secs,location_coordinates,soi_topo_sheet_no,AMSL,nearest_hfl,seismic_zone,state_name,dist_name,tehesil_name,village_name,latest_file,form1url])
    data_ec_form_df=pd.DataFrame(data_ec_form)
    data_ec_form_df.columns = ['Proposal.No.', 'FormType' ,'Name of the Project','Name of the Company','Registered Address','Legal Status of Company','Name of the Applicant','Designation of the Applicant','Address of the Applicant','Pincode of the Applicant','Email of the Applicant','Telephone of the Applicant','Major Project/Activity','Minor Project/Activity','Project Category','Proposal Number','Master Proposal Number','EAC Concerned Project A','Project Type','Plot/Survey/Khasra No.','Pincode of Project','From N Degrees','From N Minutes','From N Seconds','To N Degrees','To N Minutes','To N Seconds','From E Degrees','From E Minutes','From E Seconds','To E Degrees','To E Minutes','To E Seconds','Location Coordinates','SOI Topo Sheet No.','AMSL','Nearest HFL','Seismic Zone','State Name','District Name','Tehsil Name','Village Name','KML File','Link']

    csvfile_formdata = directory+'/'+directory_name+'/'+directory_name+'_ec_formdata'+'.csv'
    data_ec_form_df.to_csv(csvfile_formdata,encoding='utf-8-sig')

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def scrape_pariveshform_data():

    formtype = 'Parivesh'

    EC2 = driver.find_element_by_xpath("//a/img[contains(@src,'images/ecreport1.jpg')]")
    EC2.click()

    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    def page_respond():
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[(@id = 'ngb-nav-0')]"))
        )
    
    def page_respond2():
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='btn btn-primary mn-w-100']"))
        )
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    dom = etree.HTML(str(soup))

    print('..............PARIVESH FORM DATA..............')

    proposal_number1 = unique_proposals['Proposal.No.'][proposal_number]
    print(f'Proposal Number: {proposal_number1} || {formtype}')

    # Match using text does not work here - troubleshoot later, work with xpath for now
    '''
    match_using_text = dom.xpath('//*[contains(text(), "Project Name:")]/..')[0]
    xpath = etree.ElementTree(match_using_text).getpath(match_using_text)
    print(xpath)
    '''

    
    time.sleep(5)
    page_respond()
    print('Page Loaded')
    #name_proj = dom.xpath('//*[@id="proposal-summary-panel-1"]/div/div/div/div[1]/div//text()')
    name_proj = driver.find_element_by_xpath('//*[@id="proposal-summary-panel-1"]/div/div/div/div[1]/div/div[2]').text
    page_respond()
    name_company = driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[2]/div/div/table[1]/tbody/tr[2]/td[2]').text
    page_respond()
    reg_address = driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[2]/div/div/table[2]/tbody/tr[1]/td[2]').text
    page_respond()
    legal_status_of_company = driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[2]/div/div/table[1]/tbody/tr[1]/td[2]').text
    page_respond()
    
    name_applicant = driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[3]/div/div/table[1]/tbody/tr[1]/td[2]').text
    page_respond()
    designation_applicant =  driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[3]/div/div/table[1]/tbody/tr[2]/td[2]').text
    page_respond()
    address_applicant = driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[3]/div/div/table[2]/tbody/tr[1]/td[2]').text
    page_respond()
    pincode_applicant = driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[3]/div/div/table[2]/tbody/tr[4]/td[2]').text
    page_respond()
    email_applicant = driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[3]/div/div/table[2]/tbody/tr[5]/td[2]').text
    page_respond()
    tel_applicant = driver.find_element_by_xpath('//*[@id="caf_project"]/div/div[3]/div/div/table[2]/tbody/tr[6]/td[2]').text
    page_respond()

    major_activity = '' #page A
    minor_activity = '' #page A
    page_respond()
    project_category = driver.find_element_by_xpath('//*[@id="proposal-summary-panel-1"]/div/div/div/div[7]/div/div[2]').text
    page_respond()
    proposal_number2 = driver.find_element_by_xpath('//*[@id="proposal-summary-panel-1"]/div/div/div/div[3]/div/div[2]').text
    page_respond()
    master_proposal_number = driver.find_element_by_xpath('//*[@id="proposal-summary-panel-1"]/div/div/div/div[2]/div/div[2]').text
    page_respond()
    EAC_concerned_proj_A = ''
    page_respond()
    project_type = ''
    page_respond()

    plot_no = driver.find_element_by_xpath('//*[@id="caf_locationOfProject"]/div/div[1]/div/div/table[3]/tbody/tr/td[6]').text
    page_respond()
    pincode_proj = '' 
    page_respond()
    from_n_degrees = ''
    from_n_mins = ''
    from_n_secs = ''
    to_n_degrees = ''
    to_n_mins = ''
    to_n_secs = ''
    from_e_degrees = ''
    from_e_mins = ''
    from_e_secs = ''
    to_e_degrees = ''
    to_e_mins = ''
    to_e_secs = ''
    location_coordinates = ''
    page_respond()
    soi_topo_sheet_no = driver.find_element_by_xpath('//*[@id="caf_locationOfProject"]/div/div[1]/div/div/table[3]/tbody/tr/td[1]').text
    AMSL = ''
    nearest_hfl = ''
    seismic_zone = ''

    page_respond()
    state_name = driver.find_element_by_xpath('//*[@id="caf_locationOfProject"]/div/div[1]/div/div/table[3]/tbody/tr/td[2]').text
    page_respond()
    dist_name = driver.find_element_by_xpath('//*[@id="caf_locationOfProject"]/div/div[1]/div/div/table[3]/tbody/tr/td[3]').text
    page_respond()
    tehesil_name = driver.find_element_by_xpath('//*[@id="caf_locationOfProject"]/div/div[1]/div/div/table[3]/tbody/tr/td[4]').text
    page_respond()
    village_name = driver.find_element_by_xpath('//*[@id="caf_locationOfProject"]/div/div[1]/div/div/table[3]/tbody/tr/td[5]').text
    page_respond()

    parivesh_url = driver.current_url

    #Click on Part A
    partA = driver.find_element(By.LINK_TEXT, 'Part A')
    page_respond()
    time.sleep(1)
    page_respond()
    driver.execute_script("arguments[0].click();", partA)
    time.sleep(10)
    page_respond()

    major_activity = driver.find_element_by_xpath('//*[@id="ec_basicDetails"]/div/div[1]/div/div/div/table/tbody/tr[1]/td[2]').text
    page_respond()
    time.sleep(1)
    page_respond()
    minor_activity = driver.find_element_by_xpath('//*[@id="ec_basicDetails"]/div/div[1]/div/div/div/table/tbody/tr[1]/td[3]').text
    page_respond()

    #Click on CAF

    CAF = driver.find_element(By.LINK_TEXT, 'CAF')
    page_respond()
    time.sleep(1)
    page_respond()
    driver.execute_script("arguments[0].click();", partA)
    time.sleep(1)
    page_respond()

    print(f"Name of the Project: {name_proj}, \nName of the Company: {name_company}, \nRegistered Address: {reg_address}, \nLegal Status of Company: {legal_status_of_company}, \nName of the Applicant: {name_applicant}, \nDesignation of the Applicant: {designation_applicant}, \nAddress of the Applicant: {address_applicant}, \nPincode of the Applicant: {pincode_applicant}, \nEmail of the Applicant: {email_applicant}, \nTelephone of the Applicant: {tel_applicant}, \nMajor Project/Activity: {major_activity}, \nMinor Project/Activity: {minor_activity}, \nProject Category: {project_category}, \nProposal Number: {proposal_number2}, \nMaster Proposal Number: {master_proposal_number}, \nEAC Concerned Project A: {EAC_concerned_proj_A}, \nProject Type: {project_type}, \nPlot/Survey/Khasra No.: {plot_no}, \nPincode of Project: {pincode_proj}, \nFrom N Degrees: {from_n_degrees}, \nFrom N Minutes: {from_n_mins}, \nFrom N Seconds: {from_n_secs}, \nTo N Degrees: {to_n_degrees}, \nTo N Minutes: {to_n_mins}, \nTo N Seconds: {to_n_secs}, \nFrom E Degrees: {from_e_degrees}, \nFrom E Minutes: {from_e_mins}, \nFrom E Seconds: {from_e_secs}, \nTo E Degrees: {to_e_degrees}, \nTo E Minutes: {to_e_mins}, \nTo E Seconds: {to_e_secs}, \nLocation: {location_coordinates}, \nSOI Topo Sheet No.: {soi_topo_sheet_no}, \nAMSL: {AMSL}, \nNearest HFL: {nearest_hfl}, \nSeismic Zone: {seismic_zone}, \nState Name: {state_name}, \nDistrict Name: {dist_name}, \nTehsil Name: {tehesil_name}, \nVillage Name: {village_name}")



    preview_kml = driver.find_element_by_xpath('//*[@id="caf_locationOfProject"]/div/div[1]/div/div/table[1]/tbody/tr[1]/td[2]/app-download-file/span')
    #page_respond2()
    time.sleep(1)
    #page_respond2()
    driver.execute_script("arguments[0].click();", preview_kml)
    time.sleep(2)
    #page_respond2()
    time.sleep(2)
    download_btn_kml = driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div[2]/a')
    #page_respond2()
    time.sleep(1)
    #page_respond2()
    driver.execute_script("arguments[0].click();", download_btn_kml)
    time.sleep(2)

    filepath = "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\KML\\"
    list_of_files = glob.glob(directory+'/'+directory_name+'/KML/*.kml')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"KML File: {latest_file}")

    data_ec_form.append([proposal_number1, formtype, name_proj,name_company,reg_address,legal_status_of_company,name_applicant,designation_applicant,address_applicant,pincode_applicant,email_applicant,tel_applicant,major_activity,minor_activity,project_category,proposal_number2,master_proposal_number,EAC_concerned_proj_A,project_type,plot_no,pincode_proj,from_n_degrees,from_n_mins,from_n_secs,to_n_degrees,to_n_mins,to_n_secs,from_e_degrees,from_e_mins,from_e_secs,to_e_degrees,to_e_mins,to_e_secs,location_coordinates,soi_topo_sheet_no,AMSL,nearest_hfl,seismic_zone,state_name,dist_name,tehesil_name,village_name,latest_file,parivesh_url])
    data_ec_form_df=pd.DataFrame(data_ec_form)
    data_ec_form_df.columns = ['Proposal.No.', 'FormType' ,'Name of the Project','Name of the Company','Registered Address','Legal Status of Company','Name of the Applicant','Designation of the Applicant','Address of the Applicant','Pincode of the Applicant','Email of the Applicant','Telephone of the Applicant','Major Project/Activity','Minor Project/Activity','Project Category','Proposal Number','Master Proposal Number','EAC Concerned Project A','Project Type','Plot/Survey/Khasra No.','Pincode of Project','From N Degrees','From N Minutes','From N Seconds','To N Degrees','To N Minutes','To N Seconds','From E Degrees','From E Minutes','From E Seconds','To E Degrees','To E Minutes','To E Seconds','Location Coordinates','SOI Topo Sheet No.','AMSL','Nearest HFL','Seismic Zone','State Name','District Name','Tehsil Name','Village Name','KML File','Link']

    csvfile_formdata = directory+'/'+directory_name+'/'+directory_name+'_ec_formdata'+'.csv'
    data_ec_form_df.to_csv(csvfile_formdata,encoding='utf-8-sig')

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def scrape_missing_data():

    formtype = 'Missing'

    proposal_number1 = unique_proposals['Proposal.No.'][proposal_number]
    print(f'Proposal Number: {proposal_number1} || {formtype}')

    name_proj = ''
    name_company = ''
    reg_address = ''
    legal_status_of_company = ''
    name_applicant = ''
    designation_applicant = ''
    address_applicant = ''
    pincode_applicant = ''
    email_applicant = ''
    tel_applicant = ''
    major_activity = ''
    minor_activity = ''
    project_category = ''
    proposal_number2 = ''
    master_proposal_number = ''
    EAC_concerned_proj_A = ''
    project_type = ''
    plot_no = ''
    pincode_proj = ''
    from_n_degrees = ''
    from_n_mins = ''
    from_n_secs = ''
    to_n_degrees = ''
    to_n_mins = ''
    to_n_secs = ''
    from_e_degrees = ''
    from_e_mins = ''
    from_e_secs = ''
    to_e_degrees = ''
    to_e_mins = ''
    to_e_secs = ''
    location_coordinates = ''
    soi_topo_sheet_no = ''
    AMSL = ''
    nearest_hfl = ''
    seismic_zone = ''
    state_name = ''
    dist_name = ''
    tehesil_name = ''
    village_name = ''
    latest_file = ''
    formurl = ''

    data_ec_form.append([proposal_number1, formtype, name_proj,name_company,reg_address,legal_status_of_company,name_applicant,designation_applicant,address_applicant,pincode_applicant,email_applicant,tel_applicant,major_activity,minor_activity,project_category,proposal_number2,master_proposal_number,EAC_concerned_proj_A,project_type,plot_no,pincode_proj,from_n_degrees,from_n_mins,from_n_secs,to_n_degrees,to_n_mins,to_n_secs,from_e_degrees,from_e_mins,from_e_secs,to_e_degrees,to_e_mins,to_e_secs,location_coordinates,soi_topo_sheet_no,AMSL,nearest_hfl,seismic_zone,state_name,dist_name,tehesil_name,village_name,latest_file,formurl])
    data_ec_form_df=pd.DataFrame(data_ec_form)
    data_ec_form_df.columns = ['Proposal.No.', 'FormType' ,'Name of the Project','Name of the Company','Registered Address','Legal Status of Company','Name of the Applicant','Designation of the Applicant','Address of the Applicant','Pincode of the Applicant','Email of the Applicant','Telephone of the Applicant','Major Project/Activity','Minor Project/Activity','Project Category','Proposal Number','Master Proposal Number','EAC Concerned Project A','Project Type','Plot/Survey/Khasra No.','Pincode of Project','From N Degrees','From N Minutes','From N Seconds','To N Degrees','To N Minutes','To N Seconds','From E Degrees','From E Minutes','From E Seconds','To E Degrees','To E Minutes','To E Seconds','Location Coordinates','SOI Topo Sheet No.','AMSL','Nearest HFL','Seismic Zone','State Name','District Name','Tehsil Name','Village Name','KML File','Link']

    csvfile_formdata = directory+'/'+directory_name+'/'+directory_name+'_ec_formdata'+'.csv'
    data_ec_form_df.to_csv(csvfile_formdata,encoding='utf-8-sig')
    
def scrape_parivesh2_data(proposal_number):
    print('Scraping Parivesh2 Data')
    
    formtype = 'Parivesh-2'

    proposal_number1 = unique_proposals['Proposal.No.'][proposal_number]
    print(f'Proposal Number: {proposal_number1} || {formtype}')


    # Scrape Main Page Worth of Data

    proposal_number_main = proposal_number1
    file_number = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Label5"]').text
    proposal_name = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtprojectname"]').text
    state = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlp_state"]').text
    district = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlp_dist"]').text
    tehsil = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddl_p_tehshil"]').text
    a = ''
    b = ''
    category = ''
    company = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtppname"]').text
    status = ''
    link = driver.current_url
    print(f'Proposal Number: {proposal_number_main}, \nFile Number: {file_number}, \nProposal Name: {proposal_name}, \nState: {state}, \nDistrict: {district}, \nTehsil: {tehsil}, \nCategory: {category}, \nCompany: {company}, \nStatus: {status}')

    data_ec_closed.append([proposal_number_main, file_number, proposal_name, state, district, tehsil, a, b, category, company, status, link])
    data_ec_closed_df=pd.DataFrame(data_ec_closed)
    data_ec_closed_df.columns=['Proposal.No.','File_No','Proposal Name','State','District','Tehsil','Date_1','Date_2','Category','Company','Status','Link']

    csvfile_closed = directory+'/'+directory_name+'/'+directory_name+'_ec_maindata'+'.csv'
    data_ec_closed_df.to_csv(csvfile_closed,encoding='utf-8-sig')

    # Scrape Timeline Data

    proposal_number_tl = unique_proposals['Proposal.No.'][proposal_number]
    project_name2 = proposal_name
    project_sector = ''
    date_submission = ''
    submitted_by_proponent = ''
    query_shortcoming_SEIAA = ''
    resubmission1 = ''
    accepted_date_SEIAA = ''
    query_shortcoming_SEAC = ''
    resubmission2 = ''
    accepted_date_SEAC = ''
    forwarded_date_SEIAA = ''
    EC_letter_uploaded = ''
    timeline_current_url = link

    print(f'Proposal Number: {proposal_number_tl}, \nProject Name: {project_name2}, \nProject Sector: {project_sector}, \nDate of Submission: {date_submission}, \nSubmitted by Proponent: {submitted_by_proponent}, \nQuery/Shortcoming by SEIAA: {query_shortcoming_SEIAA}, \nResubmission: {resubmission1}, \nAccepted Date by SEIAA: {accepted_date_SEIAA}, \nQuery/Shortcoming by SEAC: {query_shortcoming_SEAC}, \nResubmission: {resubmission2}, \nAccepted Date by SEAC: {accepted_date_SEAC}, \nForwarded Date by SEIAA: {forwarded_date_SEIAA}, \nEC Letter Uploaded: {EC_letter_uploaded}, \nTimeline Current URL: {timeline_current_url}')

    data_ec_timeline.append([proposal_number_tl, project_name2, project_sector, date_submission, submitted_by_proponent, query_shortcoming_SEIAA, resubmission1, accepted_date_SEIAA, query_shortcoming_SEAC, resubmission2, accepted_date_SEAC, forwarded_date_SEIAA, EC_letter_uploaded, timeline_current_url])
    data_ec_timeline_df=pd.DataFrame(data_ec_timeline)
    data_ec_timeline_df.columns = ['Proposal Number','Project Name','Project Sector','Date of Submission','Submitted by Proponent','Query for Shortcoming(if any) by SEIAA','Resubmission of Proposal by Proponent 1','Accepted by SEIAA and forwarded to SEAC','Query for Shortcoming(if any) by SEAC','Resubmission of Proposal by Proponent 2','Accepted by SEAC','Forwarded to SEIAA for EC','EC Letter Uploaded On/EC Granted','Link']
    
    csvfile_timeline = directory+'/'+directory_name+'/'+directory_name+'_ec_timelinedata'+'.csv'
    data_ec_timeline_df.to_csv(csvfile_timeline,encoding='utf-8-sig')

    # Scrape Form 2 equivalent data

    proposal_number1 = unique_proposals['Proposal.No.'][proposal_number]
    name_proj = proposal_name
    name_company = company
    reg_address = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtaddress"]').text
    legal_status_of_company = ''

    name_applicant = company
    designation_applicant = ''
    address_applicant = reg_address
    pincode_applicant = ''
    email_applicant = ''
    tel_applicant = ''

    major_activity = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Label8"]').text
    minor_activity = ''
    project_category = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlcategory"]').text
    proposal_number2 = proposal_number_tl
    master_proposal_number = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblsingle"]').text
    EAC_concerned_proj_A = ''
    project_type = ''

    plot_no = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtplplot"]').text
    pincode_proj = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtplpincode"]').text
    from_n_degrees = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlpfromdate"]').text
    from_n_mins = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlafromminutes"]').text
    from_n_secs = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlafromsecond"]').text
    to_n_degrees = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlptodate"]').text
    to_n_mins = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlatominutes"]').text
    to_n_secs = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlatosecond"]').text
    from_e_degrees = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlpfromdate1"]').text
    from_e_mins = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlonfromminutes"]').text
    from_e_secs = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlonfromseconds"]').text
    to_e_degrees = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlptodate1"]').text
    to_e_mins = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlontominutes"]').text
    to_e_secs = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtlontosecond"]').text
    location_coordinates = from_n_degrees + '°' + from_n_mins + "'" + from_n_secs + '"' + 'N' + ' ' + from_e_degrees + '°' + from_e_mins + "'" + from_e_secs + '"' + 'E' + ' ' + to_n_degrees + '°' + to_n_mins + "'" + to_n_secs + '"' + 'N' + ' ' + to_e_degrees + '°' + to_e_mins + "'" + to_e_secs + '"' + 'E'
    soi_topo_sheet_no = ''
    AMSL = ''
    nearest_hfl = ''
    seismic_zone = ''

    state_name = state
    dist_name = district
    tehesil_name = tehsil
    village_name = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtpvillage"]').text

    print(f'Proposal Number: {proposal_number1}, \nName of the Project: {name_proj}, \nName of the Company: {name_company}, \nRegistered Address: {reg_address}, \nLegal Status of Company: {legal_status_of_company}, \nName of the Applicant: {name_applicant}, \nDesignation of the Applicant: {designation_applicant}, \nAddress of the Applicant: {address_applicant}, \nPincode of the Applicant: {pincode_applicant}, \nEmail of the Applicant: {email_applicant}, \nTelephone of the Applicant: {tel_applicant}, \nMajor Project/Activity: {major_activity}, \nMinor Project/Activity: {minor_activity}, \nProject Category: {project_category}, \nProposal Number: {proposal_number2}, \nMaster Proposal Number: {master_proposal_number}, \nEAC Concerned Project A: {EAC_concerned_proj_A}, \nProject Type: {project_type}, \nPlot/Survey/Khasra No.: {plot_no}, \nPincode of Project: {pincode_proj}, \nFrom N Degrees: {from_n_degrees}, \nFrom N Minutes: {from_n_mins}, \nFrom N Seconds: {from_n_secs}, \nTo N Degrees: {to_n_degrees}, \nTo N Minutes: {to_n_mins}, \nTo N Seconds: {to_n_secs}, \nFrom E Degrees: {from_e_degrees}, \nFrom E Minutes: {from_e_mins}, \nFrom E Seconds: {from_e_secs}, \nTo E Degrees: {to_e_degrees}, \nTo E Minutes: {to_e_mins}, \nTo E Seconds: {to_e_secs}, \nLocation: {location_coordinates}, \nSOI Topo Sheet No.: {soi_topo_sheet_no}, \nAMSL: {AMSL}, \nNearest HFL: {nearest_hfl}, \nSeismic Zone: {seismic_zone}, \nState Name: {state_name}, \nDistrict Name: {dist_name}, \nTehsil Name: {tehesil_name}, \nVillage Name: {village_name}')

    try:    
        kml_download = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_LinkButton6"]')
        kml_download.click()

        time.sleep(2)

        filepath = "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\KML\\"
        list_of_files = glob.glob(directory+'/'+directory_name+'/KML/*.kml') 
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)

    except:
        latest_file = ''

    print(f"KML File: {latest_file}")

    data_ec_form.append([proposal_number1, formtype, name_proj,name_company,reg_address,legal_status_of_company,name_applicant,designation_applicant,address_applicant,pincode_applicant,email_applicant,tel_applicant,major_activity,minor_activity,project_category,proposal_number2,master_proposal_number,EAC_concerned_proj_A,project_type,plot_no,pincode_proj,from_n_degrees,from_n_mins,from_n_secs,to_n_degrees,to_n_mins,to_n_secs,from_e_degrees,from_e_mins,from_e_secs,to_e_degrees,to_e_mins,to_e_secs,location_coordinates,soi_topo_sheet_no,AMSL,nearest_hfl,seismic_zone,state_name,dist_name,tehesil_name,village_name,latest_file,link])
    data_ec_form_df=pd.DataFrame(data_ec_form)
    data_ec_form_df.columns = ['Proposal.No.', 'FormType' ,'Name of the Project','Name of the Company','Registered Address','Legal Status of Company','Name of the Applicant','Designation of the Applicant','Address of the Applicant','Pincode of the Applicant','Email of the Applicant','Telephone of the Applicant','Major Project/Activity','Minor Project/Activity','Project Category','Proposal Number','Master Proposal Number','EAC Concerned Project A','Project Type','Plot/Survey/Khasra No.','Pincode of Project','From N Degrees','From N Minutes','From N Seconds','To N Degrees','To N Minutes','To N Seconds','From E Degrees','From E Minutes','From E Seconds','To E Degrees','To E Minutes','To E Seconds','Location Coordinates','SOI Topo Sheet No.','AMSL','Nearest HFL','Seismic Zone','State Name','District Name','Tehsil Name','Village Name','KML File','Link']

    csvfile_formdata = directory+'/'+directory_name+'/'+directory_name+'_ec_formdata'+'.csv'
    data_ec_form_df.to_csv(csvfile_formdata,encoding='utf-8-sig')

same_page = False

for proposal_number in range(621, len(unique_proposals['Proposal.No.'])):
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
    
    time.sleep(1)
    
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
    

    # CASE CHECKS FOR FORM TYPES - Parivesh 2

    if "parivesh.nic.in" in driver.current_url:
        current_formtype = 'Parivesh-2'
        print(unique_proposals['Proposal.No.'][proposal_number] + " Parivesh-2")
        data_ec_formtype.append([unique_proposals['Proposal.No.'][proposal_number], current_formtype])
        same_page = True

    else:
    
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        dom = etree.HTML(str(soup))

        proposal_number=dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text

        # Try getting form data

        EC2 = driver.find_element_by_xpath("//a/img[contains(@src,'images/ecreport1.jpg')]")
        EC2.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        dom = etree.HTML(str(soup))

        try: #form2
            current_formtype = driver.find_element_by_xpath("//div[@id='qq']/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/u").text
            print(proposal_number, current_formtype)
            #data_ec_formtype.append([proposal_number, formtype])
            
        except: #form1
            try:
                current_formtype = driver.find_element_by_xpath("//div[@id='qq']/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[1]/td/b/u").text
                print(proposal_number, current_formtype)
                #data_ec_formtype.append([proposal_number, formtype])

            except: #parivesh
                try:
                    if "parivesh.nic.in" in driver.current_url:
                        current_formtype = 'Parivesh'
                        print(proposal_number, current_formtype)
                        #data_ec_formtype.append([proposal_number, formtype])
                    else:
                        current_formtype = 'Missing'
                        print(proposal_number, current_formtype)
                except:
                        current_formtype = 'Missing'
                        print(proposal_number, current_formtype)
                        data_ec_formtype.append([proposal_number, current_formtype])


        data_ec_formtype.append([proposal_number, current_formtype])


    data_ec_formtype_df=pd.DataFrame(data_ec_formtype)
    data_ec_formtype_df.columns = ['Proposal','FormType']
    csvfile = directory+'/'+directory_name+'/'+directory_name+'_ec_formtype'+'.csv'
    data_ec_formtype_df.to_csv(csvfile,encoding='utf-8-sig')



    if same_page == False:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        same_page = False



    # CASE FOR PARIVESH 2 - ACKNOWLEDGEMENT FORM
    # This directly pops up with Form2 equivalent data - NO mainpage or timeline data

    if current_formtype == 'Parivesh-2':
        #proposal_number1 = unique_proposals['Proposal.No.'][proposal_number]
        scrape_parivesh2_data(proposal_number)
        continue

    # For other cases - Form 1,2,Parivesh,Missing
    
    # For Main Page
    scrape_main_page()

    # For Timeline Data
    scrape_timeline_data()




    # For Forms 1,2
    if current_formtype == 'Form-2':
        scrape_form2_data()
    elif current_formtype == 'Form-1':
        scrape_form1_data()
    elif current_formtype == 'Parivesh':
        scrape_pariveshform_data()
    elif current_formtype == 'Missing':
        scrape_missing_data()
    
        