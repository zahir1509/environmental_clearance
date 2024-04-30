# -*- coding: utf-8 -*-
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
############ THIS ONLY GETS FORM 2 DATA #####################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################

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

username = os.getlogin()
print(username)

state_name='Orissa'
directory_name='Orissa'

#chromeOptions = webdriver.ChromeOptions()
#prefs = {"download.default_directory" : "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\KML\\"}
#chromeOptions.add_experimental_option("prefs",prefs)

#driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chromeOptions)
#driver = webdriver.Chrome(ChromeDriverManager().install())

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:\\Users\\"+username+"\\Dropbox\\Environment_Clearance\\"+directory_name+"\\KML\\"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=chromeOptions)

#manually navigate to the page and search for "a"
# get the system username

directory = "C:/Users/"+username+"/Dropbox/agnihotri_gupta/Environment_Clearance"
os.chdir(directory)

##Name of State
##Make sure you create directory

unique_proposals=pd.read_csv(directory+'/'+directory_name+'/'+directory_name+'_ec_complete_unique.csv')


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

#exception proposal = 1695 Odisha 
for proposal_number in range(484,len(unique_proposals['Proposal.No.'])): 
    skip_form = False
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
    

    # Main Try Block if non-Parivesh (acknowledgment)

    try:    
        main_page_url = driver.current_url
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
        print(dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label2")]')[0].text)
        proposal_name = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label2")]')[0].text
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
        data_ec_closed.append([proposal_number,file_number,proposal_name,state,district,tehsil,a,b,category,company,status,main_page_url])
        
        #links_documents = []
        #for link in table.find_all('a', href=True):
        #    href = link.get("href")
        #    if href is not None:
        #        links_documents.append(href)
            
        
        #links_documents_df.append(links_documents)
        
        #links_proposal_df.append([proposal_number]*len(links_documents))

    except:
        print('Exception - Main Page')
        proposal_number = unique_proposals['Proposal.No.'][proposal_number]
        data_ec_closed.append([proposal_number,'','','','','','','','','','',''])
        skip_form = True




    
        ##Convert into Dataframe 
    data_ec_closed_df=pd.DataFrame(data_ec_closed)
    data_ec_closed_df.columns=['Proposal','File_No','Proposal Name','State','District','Tehsil','Date_1','Date_2','Category','Company','Status','Link']
    ##write to Dropbox
    csvfile = directory+'/'+directory_name+'/'+directory_name+'_ec_maindata'+'.csv'
    data_ec_closed_df.to_csv(csvfile,encoding='utf-8-sig')










    if skip_form == False:
    # Get Timeline data
 
        timeline_icon = driver.find_element_by_xpath("//a/img[contains(@src,'images/tme.png')]")
        timeline_icon.click()

        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        dom = etree.HTML(str(soup))

        print('--------------------timeline---------------------')

        proposal_number3 = dom.xpath('//*[@id="plblproposal_no"]')[0].text
        print(proposal_number3)
        project_name2 = dom.xpath('//*[@id="plblnameofproject"]')[0].text
        print(project_name2)
        project_sector = dom.xpath('//*[@id="plblsector"]')[0].text
        print(project_sector)
        date_submission = dom.xpath('//*[@id="plbldateofsum"]')[0].text
        print(date_submission)

        submitted_by_proponent = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[1]')[0].text
        print(submitted_by_proponent)
        query_shortcoming_SEIAA = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[2]')[0].text
        print(query_shortcoming_SEIAA)
        resubmission1 = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[3]')[0].text
        print(resubmission1)
        accepted_date_SEIAA = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[4]')[0].text
        print(accepted_date_SEIAA)
        query_shortcoming_SEAC = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[5]')[0].text
        print(query_shortcoming_SEAC)
        resubmission2 = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[6]')[0].text
        print(resubmission2)
        accepted_date_SEAC = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[7]')[0].text
        print(accepted_date_SEAC)
        forwarded_date_SEIAA = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[8]')[0].text
        print(forwarded_date_SEIAA)
        EC_letter_uploaded = dom.xpath('//*[@id="detailHTML"]/table/tbody/tr[2]/td[9]')[0].text
        print(EC_letter_uploaded)

        data_ec_timeline.append([proposal_number3,project_name2,project_sector,date_submission,submitted_by_proponent,query_shortcoming_SEIAA,resubmission1,accepted_date_SEIAA,query_shortcoming_SEAC,resubmission2,accepted_date_SEAC,forwarded_date_SEIAA,EC_letter_uploaded])
        data_ec_timeline_df=pd.DataFrame(data_ec_timeline)
        data_ec_timeline_df.columns = ['Proposal Number','Project Name','Project Sector','Date of Submission','Submitted by Proponent','Query for Shortcoming(if any) by SEIAA','Resubmission of Proposal by Proponent 1','Accepted by SEIAA and forwarded to SEAC','Query for Shortcoming(if any) by SEAC','Resubmission of Proposal by Proponent 2','Accepted by SEAC','Forwarded to SEIAA for EC','EC Letter Uploaded On/EC Granted']

        csvfile3 = directory+'/'+directory_name+'/'+directory_name+'_ec_timelinedata'+'.csv'
        data_ec_timeline_df.to_csv(csvfile3,encoding='utf-8-sig')
        

        driver.close()
        driver.switch_to.window(driver.window_handles[0])












        # Get Form1 data

        EC2 = driver.find_element_by_xpath("//a/img[contains(@src,'images/ecreport1.jpg')]")
        EC2.click()

            
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        dom = etree.HTML(str(soup))

        
        print('--------------------project details---------------------')
        #target_text = "(a)Name of the project(s)"
        #table_xpath =  f"//table[.//td[contains(., '{target_text}')]]"
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

        print(name_proj, name_company, reg_address, legal_status_of_company)

        #target_text = "(a)Name of the Applicant"
        #table_xpath =  f"//table[.//td[contains(., '{target_text}')]]"

        print('--------------------name, design, contact---------------------')
        try:
                
            match_using_text = dom.xpath('//*[contains(text(), "(a)Name of the Applicant")]/../..')[0]
            # print xpath of this
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


        print(name_applicant, designation_applicant, address_applicant, pincode_applicant, email_applicant, tel_applicant)
        

        print("--------------------------------------activity--------------------------------------")

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

        print(major_activity, minor_activity, project_category, proposal_number2, master_proposal_number, EAC_concerned_proj_A, project_type)
        


        print('-------------------------location-------------------------')

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
            soi_topo_sheet_no = ''
            AMSL = ''
            nearest_hfl = ''
            seismic_zone = ''

        print(plot_no, pincode_proj, soi_topo_sheet_no, AMSL, nearest_hfl, seismic_zone)
        print(f'Lat: {from_n_degrees} {from_n_mins} {from_n_secs} {to_n_degrees} {to_n_mins} {to_n_secs}')
        print(f'Long: {from_e_degrees} {from_e_mins} {from_e_secs} {to_e_degrees} {to_e_mins} {to_e_secs}')


        # Print the XPath
        #print(f"XPath: {xpath}")
        
        print('-------------------------details of state-------------------------')

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

        print(state_name, dist_name, tehesil_name, village_name)


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

    else:

        data_ec_timeline.append([proposal_number,"","","","","","","","","","","",""])

        #data_ec_timeline.append([proposal_number3,project_name2,project_sector,date_submission,submitted_by_proponent,query_shortcoming_SEIAA,resubmission1,accepted_date_SEIAA,query_shortcoming_SEAC,resubmission2,accepted_date_SEAC,forwarded_date_SEIAA,EC_letter_uploaded])
        data_ec_timeline_df=pd.DataFrame(data_ec_timeline)
        data_ec_timeline_df.columns = ['Proposal Number','Project Name','Project Sector','Date of Submission','Submitted by Proponent','Query for Shortcoming(if any) by SEIAA','Resubmission of Proposal by Proponent 1','Accepted by SEIAA and forwarded to SEAC','Query for Shortcoming(if any) by SEAC','Resubmission of Proposal by Proponent 2','Accepted by SEAC','Forwarded to SEIAA for EC','EC Letter Uploaded On/EC Granted']

        csvfile3 = directory+'/'+directory_name+'/'+directory_name+'_ec_timelinedata'+'.csv'
        data_ec_timeline_df.to_csv(csvfile3,encoding='utf-8-sig')



        data_ec_form2.append([proposal_number,"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""])
        #data_ec_form2.append([proposal_number,name_proj,name_company,reg_address,legal_status_of_company,name_applicant,designation_applicant,address_applicant,pincode_applicant,email_applicant,tel_applicant,major_activity,minor_activity,project_category,proposal_number2,master_proposal_number,EAC_concerned_proj_A,project_type,plot_no,pincode_proj,from_n_degrees,from_n_mins,from_n_secs,to_n_degrees,to_n_mins,to_n_secs,from_e_degrees,from_e_mins,from_e_secs,to_e_degrees,to_e_mins,to_e_secs,soi_topo_sheet_no,AMSL,nearest_hfl,seismic_zone,state_name,dist_name,tehesil_name,village_name,latest_file])



        data_ec_form2_df=pd.DataFrame(data_ec_form2)
        data_ec_form2_df.columns = ['Proposal','Name of the project(s)','Name of the Company','Registered Address','Legal Status of Company','Name of the Applicant','Designation','Address','Pincode','Email','Telephone','Major Project/Activity','Minor Project/Activity','Project Category','Proposal Number','Master Proposal Number','EAC concerned Project Authority','Project Type','Plot/Survey/Khasra No.','Pincode', 'From N Degrees', 'From N Mins', 'From N Secs', 'To N Degrees', 'To N Mins', 'To N Secs', 'From E Degrees', 'From E Mins', 'From E Secs', 'To E Degrees', 'To E Mins', 'To E Secs', 'SOI/Topo Sheet No.', 'AMSL', 'Nearest HFL', 'Seismic Zone', 'State', 'District', 'Tehsil', 'Village', 'KML']
        csvfile2 = directory+'/'+directory_name+'/'+directory_name+'_ec_form2data'+'.csv'
        data_ec_form2_df.to_csv(csvfile2,encoding='utf-8-sig')
