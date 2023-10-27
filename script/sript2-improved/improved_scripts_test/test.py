url = 'https://environmentclearance.nic.in/TrackState_proposal.aspx?type=EC&status=EC_new&statename=Orissa&pno=SIA/OR/MIS/146514/2020&pid=95022'


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

driver = webdriver.Chrome('C:/chromedriver.exe')

driver.get(url)

EC2 = driver.find_element_by_xpath("//a/img[contains(@src,'images/ecreport1.jpg')]")
EC2.click()



time.sleep(1)
driver.switch_to.window(driver.window_handles[1])

time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
dom = etree.HTML(str(soup))
text1 = dom.xpath("//div[@id='qq']/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/table[1]/tbody/tr[2]/td/table[@class='myTable']/tbody/tr/td[2]/table/tbody/tr[4]/td[2]")[0].text
print(text1)
driver.close()
driver.switch_to.window(driver.window_handles[0])
