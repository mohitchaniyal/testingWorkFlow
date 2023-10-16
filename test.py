import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pandas as pd
import os

class MarketInsight:
    
    def __init__(self):
        self.__agencies = os.getenv('AGENCIES').split(",")
        self.__url=os.getenv('URL')
        self.__markets=os.getenv('MARKETS').split(",")
        
    def __get_data(self):
        try:
            master=pd.DataFrame()
            for agency in self.__agencies:
                for market in self.__markets:
                    resp=requests.get(f"{self.__url}/{market}/{agency}")
                    data=soup(resp.content)
                    df=pd.read_html(str(data.find('table',{"class":"dataTable"})))[0]
                    df["Agency"]=agency
                    df["Market"]=market
                    df["RequestDate"]=datetime.now()
                    master=pd.concat([master,df],ignore_index=True)
            return {"success":True,"data":master}
        except Exception as e:
            return {"success":False,"message":f"error in {self.__get_data.__name__} : {e}"}
        
    def __filter_data(self,data):
        try :
            top_50_bse=data[(data["Agency"]=="bse") & (data["Market"]=="gainers")].sort_values("% Change",ascending=False)[:50].reset_index(drop=True)
            top_50_nse=data[(data["Agency"]=="nse") & (data["Market"]=="gainers")].sort_values("% Change",ascending=False)[:50].reset_index(drop=True)
            return {"success":True,"data":(top_50_bse,top_50_nse)}
        except Exception as e:
            return {"success":False,"message":f"error in {self.__filter_data.__name__} : {e}"}
        
    def __load_to_file(self,data):
        try:    
            total=""
            for top_50 in data:
                output=f"## {top_50['Agency'].iloc[0].upper()} TOP 50 {top_50['Market'].iloc[0].upper()}\n"
                output+="|S.No"
                top_50=top_50[['Company', 'Group', 'Prev Close (Rs)', 'Current Price (Rs)', '% Change', 'RequestDate']]
                for col in top_50.columns:
                        output+=f"|{col}"
                else :
                            output+="|\n"
                for col in top_50.columns:
                    output+="| :--------"
                else :
                    output+="|:--------|\n"
                output+=top_50.to_csv(header=None,na_rep="NA").replace(",","|").replace("\r","")
                output+="\n"
                total+=output
            print(total)
            return {"success":True}
        
        except Exception as e:
            return {"success":False,"message":f"error in {self.__load_to_file.__name__} : {e}"}
        
                
    def _process_data(self):
        get_data_resp=self.__get_data()
        
        if not get_data_resp["success"]:
            return get_data_resp
        
        data=get_data_resp["data"]
        
        filter_data_resp=self.__filter_data(data)
        
        if not filter_data_resp["success"]:
            return filter_data_resp
        
        filtered_data=filter_data_resp["data"]
        
        load_to_file_resp=self.__load_to_file(filtered_data)
        if not load_to_file_resp["success"]:
            return load_to_file_resp
        return {"success":True}
    
    @classmethod
    def pipline_handler(cls):
        resp=cls()._process_data()
        # print(resp)
        
MarketInsight.pipline_handler()       
