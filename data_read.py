# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 10:39:41 2020

@author: 59654
"""
import dbfread
import os
import pandas as pd
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import itertools
#读取dbf文件
def readDbfFile(filename):
    table = dbfread.DBF(filename, encoding='UTF-8')
    df = pd.DataFrame(iter(table))
    return df
#读取csv文件
def readCsvFile(filename):
    csv_data = pd.read_csv(filename)
    return csv_data
#保存图片
def save_fig(fig_id, tight_layout=True):
    path = os.path.join("images",  fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)
#平滑函数   
def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
#绘图函数
def pltxy(dataf):
    mpl.rc('axes', labelsize=14)
    mpl.rc('xtick', labelsize=12)
    mpl.rc('ytick', labelsize=12)
    X = dataf['time_s']
    y = dataf['count1']
    max_x =  dataf['time_s'].max()
    max_y = y.max()
    plt.figure(figsize=(20,15))
    plt.plot(X, smooth(y,15), "b.",linestyle = '-')
    plt.xlabel("$x_1$", fontsize=36)
    plt.ylabel("$y$", rotation=0, fontsize=36)
    plt.axis([0, max_x, 0, max_y])
    save_fig(dataf['date_time'].max())
    plt.show()



def getdata():
    wea_level_temp = {'天气':['晴','晴~多云','多云~晴','多云','多云~阴','阴~多云','阴','小雨~多云','阴~小雨','小雨','大雨~小雨'],'wea_level':[1,2,3,4,5,6,7,8,9,10,11]}
    wea_level = pd.DataFrame(wea_level_temp)
    # 读取天气节假日数据
    Data_PATH = os.path.join("Data", "杭州.csv")
    data_wea_t1 = readCsvFile(Data_PATH)
    
    # 读取数据中的日期信息
    dt = data_wea_t1['日期'].apply(lambda x:datetime.strptime(x, '%Y/%m/%d'))
    data_wea_t1['month']  = dt.map(lambda x: x.month)
    data_wea_t1['day']  = dt.map(lambda x: x.day)
    data_wea = pd.merge(left=data_wea_t1, right=wea_level, how='left', on=['天气'])    
    
    
    
    # 读取卡口流量数据
    Data_PATH = os.path.join("Data", "kktj_oau94mwxa1.dbf")
    df = readDbfFile(Data_PATH)
    

    
    # 转换小时分钟为每日的绝对分钟时间
    df['time_h'] = (df['time1'] - df['time1']%100)/100
    df['time_mi'] = df['time1']%100
    df['time_s'] = df['time_h']*60 + df['time_mi']
    # 读取日期信息与天气节假日匹配
    dt = df['date_time'].apply(lambda x:datetime.strptime(x, '%m%d'))
    df['month']  = dt.map(lambda x: x.month)
    df['day']  = dt.map(lambda x: x.day)
    df.sort_values('time_s',inplace=True,ascending=True)
    
    # 绘制每日的流量统计折线图
    #for date in df['date_time'].unique():
    #    data_temp = df[df['date_time']== date]
    #    pltxy(data_temp)
    pack = np.arange(0,1445,5)
    pack1 = pd.DataFrame(pack,columns=['time_s'])
    mmdd = data_wea[['day','month']]
    pack1['value']=1
    mmdd['value']=1
    data1 = pd.merge(mmdd,pack1,how='left',on=['value'])
    del data1['value']
    new_data = pd.merge(left=data1, right=df, how='left', on=['month','day','time_s'])    
    new_data1 = pd.merge(left=new_data, right=data_wea, how='left', on=['month','day'])
    new_data1 = new_data1[['count1','month','day','time_s','最高气温','最低气温','天气','空气质量指数','节日属性','wea_level']]
    new_data1['count1'].fillna(0, inplace=True)
    new_data1 = new_data1.dropna(axis=0,how='any') #drop all rows that have any NaN value
    return new_data1
kk = getdata()
count_all = kk['count1'].sum()
tianqi = kk['天气'].unique()
tongji ={}
for wea in tianqi:
    aa = {}
    count = kk[kk['天气'] == wea]
    count_wea = count['count1'].mean()
    day_num = count['count1'].count()
    aa[wea] = count_wea,day_num
    tongji.update(aa)
sum = 0
for a in tongji:
    sum +=tongji.get(a)[1]
    