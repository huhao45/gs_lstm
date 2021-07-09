# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 17:10:58 2020

@author: 59654
"""

import requests
import json
import pandas as pd
import  re
from bs4 import BeautifulSoup

def geturl(month):
    m = '%02d'%month
    url = "http://tianqi.2345.com/t/wea_history/js/2020"+m+"/58457_2020"+m+".js"
    return url

def getweather(month_start,month_end):
    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36' #http头大小写不敏感
    headers['accept'] = '*/*'
    headers['Connection'] = 'keep-alive'
    headers['Pragma'] = 'no-cache'

#url = "http://tianqi.2345.com/t/wea_history/js/202005/58457_202005.js"   #  58457  代表杭州
    result = []
    for month in range(month_start,month_end+1):
        url = geturl(month)
        res = requests.get(url)
        data=json.dumps(res.text, indent=2,ensure_ascii=False)
        #print(data[17:])

        b=res.text.split('[')
        c=b[1].replace('"','')
        f=re.findall(r'\{(.*?)\}', str(c))
        # tianqi=[]
        for i in f[:-1]:
            i={i.replace("'",'')}
            xx= re.sub("[A-Za-z\!\%\[\]\,\。]", " ", str(i))
            yy=xx.split(' ')
            #print(yy)
            # tianqi.append([data[24:26], yy[3][1:], yy[10][1:-1], yy[17][1:-1], yy[24][1:], yy[34][1:],yy[41][1:], yy[45][1:],yy[53][1:]])
            result.append([data[24:26], yy[3][1:], yy[10][1:-1], yy[17][1:-1], yy[24][1:], yy[34][1:],yy[41][1:], yy[45][1:],yy[53][1:]])
        #print(tianqi)
        # print('日期	最高气温	最低气温	天气	风向风力	空气质量指数')
        # print(tianqi)
    weather=pd.DataFrame(result)
    weather.columns=['城市',"日期","最高气温","最低气温","天气","风向",'风力','空气质量指数','空气质量']
    return weather

def getweathercsv(month_start,month_end):
    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36' #http头大小写不敏感
    headers['accept'] = '*/*'
    headers['Connection'] = 'keep-alive'
    headers['Pragma'] = 'no-cache'

#url = "http://tianqi.2345.com/t/wea_history/js/202005/58457_202005.js"   #  58457  代表杭州
    result = []
    for month in range(month_start,month_end+1):
        url = geturl(month)
        res = requests.get(url)
        data=json.dumps(res.text, indent=2,ensure_ascii=False)
        #print(data[17:])

        b=res.text.split('[')
        c=b[1].replace('"','')
        f=re.findall(r'\{(.*?)\}', str(c))
        # tianqi=[]
        for i in f[:-1]:
            i={i.replace("'",'')}
            xx= re.sub("[A-Za-z\!\%\[\]\,\。]", " ", str(i))
            yy=xx.split(' ')
            #print(yy)
            # tianqi.append([data[24:26], yy[3][1:], yy[10][1:-1], yy[17][1:-1], yy[24][1:], yy[34][1:],yy[41][1:], yy[45][1:],yy[53][1:]])
            result.append([data[24:26], yy[3][1:], yy[10][1:-1], yy[17][1:-1], yy[24][1:], yy[34][1:],yy[41][1:], yy[45][1:],yy[53][1:]])
        #print(tianqi)
        # print('日期	最高气温	最低气温	天气	风向风力	空气质量指数')
        # print(tianqi)
    weather=pd.DataFrame(result)
    weather.columns=['城市',"日期","最高气温","最低气温","天气","风向",'风力','空气质量指数','空气质量']
    weather.to_csv(str(data[24:26])+str(month_start)+'月_'+str(month_end)+'月.csv',encoding="utf_8_sig")
    
# getweather(1,8)
def getweather_onemonth(month):
    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36' #http头大小写不敏感
    headers['accept'] = '*/*'
    headers['Connection'] = 'keep-alive'
    headers['Pragma'] = 'no-cache'

#     url = "http://tianqi.2345.com/t/wea_history/js/202005/58457_202005.js"   #  58457  代表杭州
    result = []
    
    url = geturl(month)
    res = requests.get(url)
    data=json.dumps(res.text, indent=2,ensure_ascii=False)
    #print(data[17:])

    b=res.text.split('[')
    c=b[1].replace('"','')
    f=re.findall(r'\{(.*?)\}', str(c))
    # tianqi=[]
    for i in f[:-1]:
        i={i.replace("'",'')}
        xx= re.sub("[A-Za-z\!\%\[\]\,\。]", " ", str(i))
        yy=xx.split(' ')
        #print(yy)
        # tianqi.append([data[24:26], yy[3][1:], yy[10][1:-1], yy[17][1:-1], yy[24][1:], yy[34][1:],yy[41][1:], yy[45][1:],yy[53][1:]])
        result.append([data[24:26], yy[3][1:], yy[10][1:-1], yy[17][1:-1], yy[24][1:], yy[34][1:],yy[41][1:], yy[45][1:],yy[53][1:]])
    #print(tianqi)
    # print('日期	最高气温	最低气温	天气	风向风力	空气质量指数')
    # print(tianqi)
    weather=pd.DataFrame(result)
    weather.columns=['城市',"日期","最高气温","最低气温","天气","风向",'风力','空气质量指数','空气质量']
    return weather