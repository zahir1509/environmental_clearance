# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:40:31 2016



The steps are as follows
1. Navigate to the page where you search for the proposal manually and then
search for "a"
"""

import os
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class EnvironmentClearance:
    """
        This class will be used to extract the data pased on proposal number
    """

    def __int__(self):
        """
            Initialization method used to initilize the base functionality and variable declaration
        :return:
        """
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        # manually navigate to the page and search for "a"
        self.directory = "C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance"
        os.chdir(self.directory)

        # Name of State
        # Make sure you create directory
        self.state_name = 'Orissa'
        self.directory_name = 'Orissa'
        self.base_directory_path = 'C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/'
        self.unique_proposals = pd.read_csv(
            f'{self.base_directory_path}{self.directory}/{self.directory_name}_ec_complete_unique.csv')

    def next_button(self):
        """
            This function is used to click on the next
        :return:
        """
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[(@id = 'ctl00_ContentPlaceHolder1_RadioButtonList1_1')]"))
            )
            next_button.click()
        except StaleElementReferenceException:
            print("Click_Exception1")
            pass
        except WebDriverException:
            print("Click_Exception2")
            pass

    def next_delete_button(self):
        """
            This function is used to click on the delete next button
        :return:
        """
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_grdevents_ctl02_lnkDelete"))
            )
            next_button.click()
        except StaleElementReferenceException:
            print("Click_Exception1")
            pass
        except WebDriverException:
            print("Click_Exception2")
            pass

    def search_proposal(self, proposal_number):
        """
            This function is used to search based on proposal by clicking on the search button
        :param proposal_number:
        :return:
        """
        try:
            text_area = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_textbox2"))
            )
            text_area.send_keys(self.unique_proposals['Proposal.No.'][proposal_number])
        except StaleElementReferenceException:
            print("Click_Exception1")
            pass
        except WebDriverException:
            print("Click_Exception2")
            pass

    def perform_search(self):
        """
            This function is used to perform the search
        :return:
        """
        try:
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btn"))
            )
            search_button.click()
        except StaleElementReferenceException:
            print("Click_Exception1")
            pass
        except WebDriverException:
            print("Click_Exception2")
            pass

    def parse_html(self):
        """
            This function will extarct the data from the html
        :return:
        """
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        dom = etree.HTML(str(soup))

        # Proposal Number
        proposal_number = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_std")]')[0].text

        file_number = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_fn")]')[0].text

        state = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_stdname1")]')[0].text
        district = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lbldis1")]')[0].text
        tehsil = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_lblvill1")]')[0].text

        span = soup.find("span", id="ctl00_ContentPlaceHolder1_GridView1_ctl02_datehtml")
        a = re.search('^(Date of.*)(Date of.*)', span.text).group(1)
        b = re.search('^(Date of.*)(Date of.*)', span.text).group(2)

        category = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_dst")]')[0].text

        # Company Proponent
        company = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_uag")]')[0].text
        # data_ec_closed_df['Company'].append(company)

        # Current Status
        status = dom.xpath('//*[(@id = "ctl00_ContentPlaceHolder1_GridView1_ctl02_Label1")]')[0].text

        return proposal_number, file_number, state, district, tehsil, a, b, category, company, status

    def get_dataframe(self, data_ec_closed):
        """
            This function will convert the raw data into dataframe
        :param data_ec_closed:
        :return:
        """
        data_ec_closed_df = pd.DataFrame(data_ec_closed)
        data_ec_closed_df.columns = ['Proposal', 'File_No', 'State', 'District', 'Tehsil', 'Date_1', 'Date_2',
                                     'Category',
                                     'Company', 'Status']
        return data_ec_closed_df

    def main(self):
        """
        This is used to perform the whole operations on the class or it's a driver function
        :return:
        """
        # Get the url under "Track Proposal"
        url = 'https://environmentclearance.nic.in/proposal_status_state.aspx?pid=ClosedEC&statename=' + self.state_name

        data_ec_closed = []

        # exception proposal = 1695 Odisha
        for proposal_number in range(0, len(self.unique_proposals['Proposal.No.'])):
            print(proposal_number)
            self.driver.get(url)
            time.sleep(1)
            
            # Select the EC Radio Button
            self.next_button()

            # Enter Proposal Number
            self.search_proposal(proposal_number)
            # Search
            self.perform_search()
            time.sleep(1)

            self.next_delete_button()

            # parse html
            proposal_number, file_number, state, district, tehsil, a, b, category, company, status = self.parse_html()
            data_ec_closed.append(
                [proposal_number, file_number, state, district, tehsil, a, b, category, company, status])

        # Convert into Dataframe
        data_ec_closed_df = self.get_dataframe(data_ec_closed)
        # write to Dropbox
        csvfile = f"{self.base_directory_path}{self.directory_name}/{self.directory_name}'_ec_additional_data.csv"
        data_ec_closed_df.to_csv(csvfile, encoding='utf-8-sig')
