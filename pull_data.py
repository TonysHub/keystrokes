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

class NaverOpenAPI():
    def __init__(self, client_id, client_secret):
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
    
    def get_data(self, endDate, startDate, timeUnit, ages, gender, device):
        # apply given data to params
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
            print(result)
        else:
            print("Error Code:" + rescode)
