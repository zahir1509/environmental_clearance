import requests
from pprint import pprint
from tqdm import tqdm
import random
import pandas as pd
import matplotlib.pyplot as plt

# List of project rows will be stored in this
projects = []
possible_headers = [
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 "
                      "(KHTML, like Gecko) Version/13.1.1 Safari/605.1.15"
    },
    {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    },
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    },
]
current_viewstate = "scSllP3FYjNW12aUazc9H2DqCp%2FQlAbLk8JKE5ddwZP8A0kW2FDOJZ35pJbI%2FvIfNGaSa0%2BkZ%2Byw8erC1O3dlK0O99tY%2FyYLG%2BYQPq5VrjP0vc44bFTt%2FwQ1z74d62nALigvyN8CsR3LT5VAoezunKqECIoi19f4tsCjJeJfPFxlOJPhlIcKiTXt7%2BZNvgjIFUs78xngpgh2rFwmAwwsn3CoSav8w5hhzNpcGC45iKI%2FKmSdzy1LteoHytimKTc11UbbeVt1CjHEVNIoXxWdPtNY72Af9XOq%2BpiaLepzZgYtQX67PCC1hCJCxPjTYNcHNiIvLk6wfXNjoHI1izMCCHWJPzTW6ENUSzBzcWWwYhMGRv%2FbTPGEOjHQY8fYVzn2NdrAK2k%2FLs1xde8LSW9S3d7R%2F8WuoIHlF4RuOabMP2AD2zRvwaJsQ4ZCyUDdI%2BwSqS%2B05y8%2FyWTxevh4Ldamv2zZJVEj5x1d08BVSVPicRtyrKc8JlViAFr%2FV1FiGRbNrN037Rv3svQYyFp0PyWJpGvKK2d6RDdFkHrUbRBbMhTH3D9Za6DjnAQ4Ngi4TN%2BT82pSxQKsLN5hydQyeBTk9oZStASsS5mFDjtcWWgt4DtnZhihJ%2BbTzxc8cVxHEH739MuMdl%2BGv5nBU7qZYrdsrWIx7%2FGkwdXPmpiP26oOO3j76Yomr%2BdgMzf5bwgDAIJeCxs0CnO2HtOxmrR92d1otQ%3D%3D"
current_validation = "y8vnE0j3n4hGnfyMLccq1W%2B%2BaYXuCJ9AtpIcUDkTx5N%2F0V%2FtLIBqmdpiOwJcsme5uIafxdSoC%2FBH8J8VnhZ3LnrSuZIwhjG736ZGwROmD4DjPYIDhT5MT6eBrqPgxoxki70zNvd1eb3ieQ7pBCbKPdYW2yH3xLRBh5kG%2BtIDZ7bi6BWHk639aG2%2FoXoMZrP2KgsjaYyjRPNuGHYjGcpu9%2B1kj%2BCZqUBDChHTVQB5ipAOygprejzoySO6KC%2BphFk7veuhUQPkWzScppvKpLPfs%2B80qufWKP2KWJskDsUFbng%3D"


# Send a request as the frontend asking for one html page worth of data
def grab_project_docs(state_name, project_num, pid):
    global current_viewstate, current_validation
    base_url = "https://environmentclearance.nic.in/TrackState_proposal.aspx?type=EC&statename="
    url = f"{base_url}{state_name}&pno={project_num}&pid={pid}"

    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://environmentclearance.nic.in",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": url,
        "Cookie": "ASP.NET_SessionId = 0czkxyx411fdbinxpsfxpi3c; acopendivids = Email, Campa, support, livestat, commitee, Links; acgroupswithpersist = nada",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
    }

    # Try sending the request and report if there is an error
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # note that parse_project_numbers_html must be called immediately afterwards so that the viewstate value
            # can be extracted from this response html and updated in the global variable current_viewstate
            current_viewstate = response.text.split('id="__VIEWSTATE" value="')[1].split('" />')[0].replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")
            current_validation = response.text.split('id="__EVENTVALIDATION" value="')[1].split('" />')[0].replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")
            # print(response.text.split("pid=")[1].split('" id=')[0])
            print(response.text)
            return response.text
        else:
            print(f"Error: {response.status_code}")
            return

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    state = "West Bengal"
    filename = f'../{state.replace(" ", "_")}/scraped_projects.csv'

    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        # grab_project_docs(state.replace(" ", "+"), row[2], row[7])
        pass

    grab_project_docs(state.replace(" ", "+"), "SIA/WB/IND/18439/2015", "")
