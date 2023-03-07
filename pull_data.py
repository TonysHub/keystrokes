import os
import sys
import urllib.request
from settings import *

url = "https://openapi.naver.com/v1/datalab/search"
body = "{\"startDate\":\"2017-01-01\",\"endDate\":\"2017-04-30\",\"timeUnit\":\"month\", \
        \"keywordGroups\":[{\"groupName\":\"한글\",\"keywords\":[\"한글\",\"korean\"]}, \
        {\"groupName\":\"영어\",\"keywords\":[\"영어\",\"english\"]}],\"device\":\"pc\",\"ages\":[\"1\",\"2\"],\"gender\":\"f\"}"

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
