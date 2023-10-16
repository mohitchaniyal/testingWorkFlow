import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
import os

agencies = os.getenv('AGENCIES').split(",")
url=os.getenv('URL')
markets=os.getenv('MARKETS').split(",")
print(agencies,url,markets)

master=pd.DataFrame()
for agency in agencies:
    for market in markets:
        resp=requests.get(f"{url}/{market}/{agency}")
        data=soup(resp.content)
        df=pd.read_html(str(data.find('table',{"class":"dataTable"})))[0]
        df["Agency"]=agency
        df["Market"]=market
        df["RequestDate"]=datetime.now().date().strftime('%Y-%m-%d')
        master=pd.concat([master,df],ignore_index=True)
print(master.iloc[0])
