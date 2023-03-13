#-*- coding: utf-8 -*-
import os
import sys
import time
import json
import random
import requests
import signaturehelper
from settings import *
from datetime import date

import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format

class naverSearchAPI():
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.keywordGroups = []
        self.url = "https://openapi.naver.com/v1/datalab/search"

    def add_keyword_group(self, group_dict):
        keyword_group = {
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
        
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "Content-Type": "application/json",
        }
        response = requests.post(self.url, headers=headers, data=params.encode("utf-8"))
        rescode = response.status_code

        if(rescode==200):
            result = response.json()
            df = pd.json_normalize(result, 
                        record_path=["results", "data"],
                        meta=[["results","title"]]
                        )
            df = df.pivot(index='period', columns='results.title', values='ratio')
        else:
            print("Error Code:" + rescode)
        return df
    
    '''JSON SAMPLE - saved for future reference
    {
        'startDate': '2020-01-01', 
        'endDate': '2020-01-03', 
        'timeUnit': 'date', 
        'results': [{
            'title': '애플', 
            'keywords': ['애플', 'Apple', 'AAPL'], 
            'data': [{
                    'period': '2020-01-01', 'ratio': 4.61406}, 
                    {'period': '2020-01-02', 'ratio': 5.23919}, 
                    {'period': '2020-01-03', 'ratio': 5.04305}]}, 
                    {
            'title': '아마존', 
            'keywords': ['아마존', 'Amazon', 'AMZN'], 
            'data': [{
                    'period': '2020-01-01', 'ratio': 2.17676}, 
                    {'period': '2020-01-02', 'ratio': 2.6676}, 
                    ...

    The above result shows
            period  ratio results.title
    0  2020-01-01   4.61            애플
    1  2020-01-02   5.24            애플
    3  2020-01-01   2.18           아마존
    4  2020-01-02   2.67           아마존
    6  2020-01-01  89.66            구글
    7  2020-01-02 100.00            구글

    Pivot is needed for a structure of 
    results.title     구글  아마존   애플
    period                        
    2020-01-01     89.66 2.18 4.61
    2020-01-02    100.00 2.67 5.24'''
            
class naverAdsAPI():
    def __init__(self):
        self.base_url = 'https://api.searchad.naver.com'
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.customer_id = CUSTOMER_ID

    def get_header(self, method, uri):
        timestamp = str(round(time.time() * 1000))
        signature = signaturehelper.Signature.generate(timestamp, method, uri, self.secret_key)
        return {'Content-Type': 'application/json; charset=UTF-8', 
                'X-Timestamp': timestamp, 'X-API-KEY': self.api_key, 
                'X-Customer': str(self.customer_id), 'X-Signature': signature}

    def get_keywords(self, keyword):
        uri = '/keywordstool'
        method = 'GET'
        r = requests.get(self.base_url + uri+'?hintKeywords={}&showDetail=1'.format(keyword),
                         headers=self.get_header(method, uri))
        if r.status_code == 200:
            df = pd.DataFrame(r.json()['keywordList'])
            df.rename({'compIdx':'경쟁정도',
                       'monthlyAveMobileClkCnt':'월평균클릭수_모바일',
                       'monthlyAveMobileCtr':'월평균클릭률_모바일',
                       'monthlyAvePcClkCnt':'월평균클릭수_PC',
                       'monthlyAvePcCtr':'월평균클릭률_PC', 
                       'monthlyMobileQcCnt':'월간검색수_모바일',
                       'monthlyPcQcCnt': '월간검색수_PC',
                       'plAvgDepth':'월평균노출광고수', 
                       'relKeyword':'키워드'},axis=1,inplace=True)
            return df
        else:
            print("Error Code:", r.status_code)

    def get_avg_bid(self):
        uri = '/estimate/average-position-bid/keyword'
        method = 'POST'
        r = requests.post(self.base_url + uri, json={'device': 'PC', 'items': [{'key': '제주여행', 'position': 1}, 
                                                                               {'key': '게스트하우스', 'position': 1}, 
                                                                               {'key': '자전거여행', 'position': 1}]}, 
                                                    headers=self.get_header(method, uri))
        if r.status_code == 200:
            df = pd.DataFrame(r.json()['estimate'])
            df.rename({'bid': '광고_단가',
                       'keyword': '키워드',
                       'position': '광고_노출_순위'}, axis=1, inplace=True)
            return df
        else:
            print("Error Code:", r.status_code )

class naverShoppingAPI():
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
    
    def get_comparison_data(self, startDate, endDate, timeUnit, category, ages, gender, device):
        url = "https://openapi.naver.com/v1/datalab/shopping/categories"
        params = json.dumps({
            "startDate": startDate,
            "endDate": endDate,
            "timeUnit": timeUnit,
            "category": category,
            "keyword": self.keyword,
            "keyword.name": "",
            "keyword.param": [],
            "device": device,
            "ages": ages,
            "gender": gender
        }, ensure_ascii=False)
        
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, data=params.encode("utf-8"))
        rescode = response.status_code

    def get_gender_data(self, startDate, endDate, timeUnit, category, ages, gender, device):
        url = "https://openapi.naver.com/v1/datalab/shopping/category/keyword/gender"
        params = json.dumps({
            "startDate": startDate,
            "endDate": endDate,
            "timeUnit": timeUnit,
            "category": category,
            "keyword": self.keyword,
            "keyword.name": "",
            "keyword.param": [],
            "device": device,
            "ages": ages,
            "gender": gender
        }, ensure_ascii=False)
        
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, data=params.encode("utf-8"))
        rescode = response.status_code

    def get_age_data(self, startDate, endDate, timeUnit, category, ages, gender, device):
        url = "https://openapi.naver.com/v1/datalab/shopping/category/keyword/age"
        params = json.dumps({
            "startDate": startDate,
            "endDate": endDate,
            "timeUnit": timeUnit,
            "category": category,
            "keyword": self.keyword,
            "keyword.name": "",
            "keyword.param": [],
            "device": device,
            "ages": ages,
            "gender": gender
        }, ensure_ascii=False)
        
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, data=params.encode("utf-8"))
        rescode = response.status_code

