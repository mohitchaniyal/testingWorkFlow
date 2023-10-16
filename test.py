import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd

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
