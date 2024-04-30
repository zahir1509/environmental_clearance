import os
import requests
import pandas as pd
from pprint import pprint
from tqdm import tqdm
import math

tqdm.pandas()

links = pd.read_csv('../Orissa/Odisha_ec_complete_links.csv')
pids = pd.read_csv('../Orissa/Odisha_ec_complete_links_pid.csv')
df = pd.merge(pids[["Unnamed: 0", "0"]], links, on="Unnamed: 0")
df.rename({"Unnamed: 0": "index", "0_x": "pid", "0_y": "0"}, axis=1, inplace=True)

base_url = "https://environmentclearance.nic.in"
output_directory = '../Orissa/pdfs/'


def download_pdfs(project, column_name):

    pdf = f"{output_directory}{project['pid'].replace('/', '+')}_{column_name}.pdf"

    if type(project[column_name]) != str or str(project[column_name]) == "NaN" or os.path.isfile(pdf):
        return

    if project[column_name].startswith("http://") or project[column_name].startswith("https://"):
        link = project[column_name]
    elif project[column_name].startswith("../"):
        link = base_url + project[column_name][2:]
    elif project[column_name].startswith("state/") or project[column_name].startswith("timeline.aspx"):
        link = base_url + "/" + project[column_name]
    else:
        link = base_url + project[column_name]

    try:
        response = requests.get(link, verify=False) if project[column_name].startswith("http://") else requests.get(link)
        if response.status_code == 200:
            with open(pdf, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download PDF from: {link}")
    except Exception as e:
        print(f"Failed to download PDF from: {link}, error: {e}")


for column in range(0, int(list(df.columns)[-1])+1):
    df.progress_apply(download_pdfs, axis=1, args=(str(column),))
