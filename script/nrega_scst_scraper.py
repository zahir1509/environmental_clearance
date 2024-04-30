import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint
from tqdm import tqdm

base_url = "https://nreganarep.nic.in/netnrega/state_html/"
state_codes = {"ANDAMAN AND NICOBAR": "01", "ANDHRA PRADESH": "02",
               "ARUNACHAL PRADESH": "03", "ASSAM": "04", "BIHAR": "05", "CHHATTISGARH": "33", "DN HAVELI AND DD": "07",
               "GOA": "10", "GUJARAT": "11", "HARYANA": "12", "HIMACHAL PRADESH": "13", "JAMMU AND KASHMIR": "14",
               "JHARKHAND": "34", "KARNATAKA": "15", "KERALA": "16", "LADAKH": "37", "LAKSHADWEEP": "19",
               "MADHYA PRADESH": "17", "MAHARASHTRA": "18", "MANIPUR": "20", "MEGHALAYA": "21", "MIZORAM": "22",
               "NAGALAND": "23", "ODISHA": "24", "PUDUCHERRY": "25", "PUNJAB": "26", "RAJASTHAN": "27", "SIKKIM": "28",
               "TAMIL NADU": "29", "TELANGANA": "36", "TRIPURA": "30", "UTTAR PRADESH": "31", "UTTARAKHAND": "35",
               "WEST BENGAL": "32"}


# scrape the district pages for district names and block page links
def grab_districts(session, state, year):
    resolution = "s".upper()
    state_name = state.upper().replace(" ", "%20")
    state_code = state_codes[state.upper()]
    url = f"https://nreganarep.nic.in/netnrega/state_html/empstatusnewall_scst.aspx?page={resolution}&lflag=eng&state_name={state_name}&state_code={state_code}&fin_year={year}&source=national&Digest=LXFrYfDbR23q8Uao8A8mOA"
    response = session.get(url)

    districts = []

    soup = BeautifulSoup(response.content, 'html.parser')
    target_table = None
    for table in soup.find_all('table'):
        if "HH issued jobcards" in str(table):
            target_table = table
            break

    for row in target_table.find_all('tr'):
        cells = row.find_all('td')
        second_column = cells[1].find('a')
        if second_column:
            link_text = second_column.get_text(strip=True)
            href_link = second_column['href']
            districts.append((link_text, href_link))

    return districts


# scrape the block pages for district names and panchayat page links
def grab_blocks(session, district):
    url = base_url + district[1]
    response = session.get(url)

    blocks = []

    soup = BeautifulSoup(response.content, 'html.parser')
    target_table = None
    for table in soup.find_all('table'):
        if "HH issued jobcards" in str(table):
            target_table = table
            break

    for row in target_table.find_all('tr'):
        cells = row.find_all('td')
        second_column = cells[1].find('a')
        if second_column:
            link_text = second_column.get_text(strip=True)
            href_link = second_column['href']
            blocks.append((link_text, href_link))

    return blocks


# scrape the panchayat pages for the numbers
def grab_panchayats(session, district, block):
    url = base_url + block[1]
    response = session.get(url)

    panchayats = []

    soup = BeautifulSoup(response.content, 'html.parser')
    target_table = None
    for table in soup.find_all('table'):
        if "HH issued jobcards" in str(table):
            target_table = table
            break

    for row in target_table.find_all('tr')[4:-1]:
        panchayat = [district[0], block[0]]
        cells = row.find_all('td')
        for i in range(1, 20):
            column_text = cells[i].get_text(strip=True)
            panchayat.append(column_text)
        panchayats.append(panchayat)

    return panchayats


# create the final dataframe
def grab_data(state, year):
    data = []

    with requests.Session() as session:

        districts = grab_districts(session, state, year)

        for district in tqdm(districts):
            blocks = grab_blocks(session, district)

            for block in blocks:
                panchayats = grab_panchayats(session, district, block)
                data += panchayats

    return data


if __name__ == "__main__":
    state = "Andhra Pradesh"
    start_year = 2014
    end_year = 2015

    # Placing the below code inside this loop should allow every state to be scraped in one run
    # for state in state_codes.keys():

    for year in range(start_year, end_year):

        df = pd.DataFrame(grab_data(state, str(year)+"-"+str(year+1)))
        df.columns = ["District", "Block", "Panchayat", "SCs HH issued jobcards", "STs HH issued jobcards", "Others HH issued jobcards", "Total HH issued jobcards", "SCs Provided Employment", "STs Provided Employment", "Others Provided Employment", "Total Provided Employment", "Women EMP Provided", "SCs Persondays generated", "STs Persondays generated", "Others Persondays generated", "Total Persondays generated", "Women Persondays generated", "SCs Families Completed 100 Days", "STs Families Completed 100 Days", "Others Families Completed 100 Days", "Total Families Completed 100 Days"]

        filename = f'../mnrega/{state.replace(" ", "_")}/mnrega_scst_{str(year)+"-"+str(year+1)}.csv'

        # create the folder if none exists
        foldername = "/".join(filename.split("/")[:-1])
        if not os.path.exists(foldername):
            os.mkdir(foldername)

        df.to_csv(filename, index=True)
