#-*- coding: utf-8 -*-
import os
import sys
import urllib.request
from settings import *
from datetime import date

endDate = date.today().strftime("%Y-%m-%d")
url = "https://openapi.naver.com/v1/datalab/search"
body = "{\"startDate\":\"2020-01-01\",                                              \
        \"endDate\":\endDate,                                                 \
        \"timeUnit\":\"date\",                                                      \
        \"keywordGroups\":[                                                         \
            {\"groupName\":\"한글\",\"keywords\":[\"한글\",\"korean\"]},              \
            {\"groupName\":\"영어\",\"keywords\":[\"영어\",\"english\"]}],}"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",CLIENT_ID)
request.add_header("X-Naver-Client-Secret",CLIENT_SECRET)
request.add_header("Content-Type","application/json")
response = urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
