import csv
import json
import demjson
import requests
import datetime
import time


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


start = datetime.datetime(2019, 1, 1, 0, 0, 0)
end = datetime.datetime(2020, 12, 31, 0, 0, 0)
result = []
for i in date_range(start, end):
    # print(i.strftime('%Y%m%d'))
    URL = "http://tool.bitefu.net/jiari/"
    url = URL + "?d=" + i.strftime('%Y%m%d') + "&info=1"
    res = requests.get(url)
    data = json.dumps(res.text, ensure_ascii=False)
    jsona = demjson.decode(res.text)
    # print(i.strftime('%Y%m%d'),jsona)
    time.sleep(1)
    csv_list = [[] * 6] * len(jsona)
    s = []
    j = 0
    # 判断道路名称是否为空，为空不做记录
    s.append(jsona['day'])
    s.append(jsona['status'])
    s.append(jsona['type'])
    s.append(jsona['typename'])
    s.append(jsona['unixtime'])
    s.append(jsona['nonglicn'])
    s.append(jsona['nongli'])
    s.append(jsona['shengxiao'])
    s.append(jsona['jieqi'])
    s.append(jsona['weekcn'])
    s.append(jsona['week1'])
    s.append(jsona['week3'])
    s.append(jsona['daynum'])
    s.append(jsona['weeknum'])
    result.append(s)
    print(s)
# 将数据写入csv
data_list = ['day', 'status', 'type', 'typename', 'unixtime', 'nonglicn', 'nongli', 'shengxiao', 'jieqi', 'weekcn', 'week1', 'week3', 'daynum', 'weeknum']
fp_csv = open('tt.csv', 'w', newline='', encoding='utf-8-sig')
writer = csv.writer(fp_csv)
# 写入表头标题
writer.writerow(data_list)
# 写入表内容
writer.writerows(result)
print(result)
fp_csv.close()