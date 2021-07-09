# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:27:53 2020

@author: 59654
"""
import dbfread
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import get_weather

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


# 读取dbf文件
def readDbfFile(filename):
    table = dbfread.DBF(filename, encoding='UTF-8')
    df = pd.DataFrame(iter(table))
    return df


# 读取csv文件
def readCsvFile(filename):
    csv_data = pd.read_csv(filename)
    return csv_data


# 保存图片
def save_fig(fig_id, month, day, tight_layout=True):
    path = os.path.join("images", "x" + str(month) + "-" + str(day) + "x.png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)


# 平滑函数
def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


# 绘图函数
def pltxy(dataf, month, day):
    mpl.rc('axes', labelsize=14)
    mpl.rc('xtick', labelsize=12)
    mpl.rc('ytick', labelsize=12)
    X = dataf['time_min']
    y = dataf['count1']
    max_x = dataf['time_min'].max()
    max_y = dataf['count1'].max()
    plt.figure(figsize=(20, 15))
    plt.plot(X, y, "b.", linestyle='-')
    plt.xlabel("$x_1$", fontsize=36)
    plt.ylabel("$y$", rotation=0, fontsize=36)
    plt.axis([0, max_x, 0, max_y])
    save_fig(dataf['day'].max(), month, day)
    plt.show()


def getdata():
    # wea_level_temp = {'天气':['晴','晴~多云','多云~晴','多云','多云~阴','阴~多云','阴','小雨~多云','阴~小雨','小雨','大雨~小雨'],'wea_level':[1,2,3,4,5,6,7,8,9,10,11]}
    # wea_level = pd.DataFrame(wea_level_temp)
    # 读取天气节假日数据
    Data_PATH = os.path.join("Data", "杭州.csv")
    data_wea_t1 = readCsvFile(Data_PATH)
    # data_wea_t1 = get_weather.getweather(1,8)
    # data_wea_t1 = get_weather.getweather_onemonth(8)
    # 读取数据中的日期信息
    dt = data_wea_t1['日期'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d'))
    data_wea_t1['month'] = dt.map(lambda x: x.month)
    data_wea_t1['day'] = dt.map(lambda x: x.day)
    # data_wea = pd.merge(left=data_wea_t1, right=wea_level, how='left', on=['天气'])    
    data_wea = data_wea_t1

    # 读取卡口流量数据
    Data_PATH = os.path.join("Data", "kktj_oau94mwxa1_2019_1_9_60.dbf")
    df = readDbfFile(Data_PATH)

    # 转换小时分钟为每日的绝对分钟时间
    df['time_h'] = df['time_h'].astype(float)
    df['time_min'] = df['time_h'] * 60 + df['time_s']

    # 读取日期信息与天气节假日匹配
    dt = df['date_time'].apply(lambda x: datetime.strptime(x, '%m%d'))
    df['month'] = dt.map(lambda x: x.month)
    df['day'] = dt.map(lambda x: x.day)
    df.sort_values('time_s', inplace=True, ascending=True)
    df.sort_values(by=["month", "day", "time_h", "time_s"], ascending=[True, True, True, True], inplace=True)
    # 绘制每日的流量统计折线图
    # for date in df['date_time'].unique():
    #    data_temp = df[df['date_time']== date]
    #    pltxy(data_temp)
    pack = np.arange(0, 1445, 60)
    pack1 = pd.DataFrame(pack, columns=['time_min'])
    mmdd = data_wea[['day', 'month']]
    pack1['value'] = 1
    mmdd['value'] = 1
    data1 = pd.merge(mmdd, pack1, how='left', on=['value'])
    del data1['value']
    new_data = pd.merge(left=data1, right=df, how='left', on=['month', 'day', 'time_min'])
    new_data1 = pd.merge(left=new_data, right=data_wea, how='left', on=['month', 'day'])
    # new_data1 = new_data1[['time_h','count1','month','day','time_s','time_min','最高气温','最低气温','天气','空气质量指数','节日属性',
    # 'wea_level']]
    new_data1 = new_data1[['time_h', 'count1', 'month', 'day', 'time_s', 'time_min', '最高气温', '最低气温', '天气', '空气质量指数']]

    new_data1['count1'].fillna(0, inplace=True)
    new_data1 = new_data1.dropna(axis=0, how='any')  # drop all rows that have any NaN value
    # 平滑数据
    y = new_data1['count1']
    new_data1['count1'] = smooth(y, 3)
    wrong_data = [1, 22, 23, 24, 6, 25, 26]
    # wrong_data = []
    # ture_data = [14,15,16,17,18,19,20]
    new_data = new_data1.drop(new_data1[(new_data1['day'].isin(wrong_data)) & (new_data1['month'] == 8)].index)
    new_data = new_data.drop(new_data1[(new_data1['day'].isin([29, 30, 31])) & (new_data1['month'] == 7)].index)
    # new_data = new_data1[new_data1['day'].isin(ture_data)]
    # print(new_data['day'].unique())
    # 绘制每日的流量统计折线图
    # for month in new_data['month'].unique():
    #     for date in new_data['day'].unique():
    #         data_temp = new_data[(new_data['day']== date)&(new_data['month']== month)]
    #         if(not data_temp.empty):
    #             pltxy(data_temp,month,date)
    return new_data
# kk = getdata()
# count_all = kk['count1'].sum()
# tianqi = kk['天气'].unique()
# tongji ={}
# for wea in tianqi:
#     aa = {}
#     count = kk[kk['天气'] == wea]
#     count_wea = count['count1'].mean()
#     day_num = count['count1'].count()
#     aa[wea] = count_wea,day_num
#     tongji.update(aa)
# sum = 0
# for a in tongji:
#     sum +=tongji.get(a)[1]
#
if __name__ == '__main__':
    data = getdata()