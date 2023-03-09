#-*- coding: utf-8 -*-
import os
import sys
import json
import urllib.request
from settings import *
from datetime import date

import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format

class NaverSearchAPI():
    def __init__(self):
        # Import client details, intialize keywordGroups with None
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.keywordGroups = []
        self.url = "https://openapi.naver.com/v1/datalab/search"

    def add_keyword_group(self, group_dict):
        keyword_group = {
            # Up to 5 groups, 20 keywords...
            # Might have to call this function multiple times
            'groupName': group_dict['groupName'],
            'keywords': group_dict['keywords'] 
        }
        self.keywordGroups.append(keyword_group)
    
    def get_data(self, startDate, endDate, timeUnit, ages, gender, device):
        # Apply given data to params
        params = json.dumps({
            "startDate": startDate,
            "endDate": endDate,
            "timeUnit": timeUnit,
            "keywordGroups": self.keywordGroups,
            "device": device,
            "ages": ages,
            "gender": gender
        }, ensure_ascii=False)
        
        # Below code is from NaverAPI 
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=params.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            result = json.loads(response.read())
            # JSON SAMPLE
            # {
            #     'startDate': '2020-01-01', 
            #     'endDate': '2020-01-03', 
            #     'timeUnit': 'date', 
            #     'results': [{
            #         'title': '애플', 
            #         'keywords': ['애플', 'Apple', 'AAPL'], 
            #         'data': [{
            #                 'period': '2020-01-01', 'ratio': 4.61406}, 
            #                 {'period': '2020-01-02', 'ratio': 5.23919}, 
            #                 {'period': '2020-01-03', 'ratio': 5.04305}]}, 
            #                 {
            #         'title': '아마존', 
            #         'keywords': ['아마존', 'Amazon', 'AMZN'], 
            #         'data': [{
            #                 'period': '2020-01-01', 'ratio': 2.17676}, 
            #                 {'period': '2020-01-02', 'ratio': 2.6676}, 
            #                 ...
            df = pd.json_normalize(result, 
                                   record_path=["results", "data"],
                                   meta=[["results","title"]]
                                    )
            # The above result shows
            #        period  ratio results.title
            # 0  2020-01-01   4.61            애플
            # 1  2020-01-02   5.24            애플
            # 3  2020-01-01   2.18           아마존
            # 4  2020-01-02   2.67           아마존
            # 6  2020-01-01  89.66            구글
            # 7  2020-01-02 100.00            구글

            # Pivot is needed for a structure of 
            # results.title     구글  아마존   애플
            # period                        
            # 2020-01-01     89.66 2.18 4.61
            # 2020-01-02    100.00 2.67 5.24

            df = df.pivot(index='period', columns='results.title', values='ratio')
        else:
            print("Error Code:" + rescode)
        return df
