#台北市 大安區 YouBike 使用情況分析

import urllib.request as request
import json


#公開資料 json格式
src = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
with request.urlopen(src) as response:
    data = json.load(response)
clist = []
for d in data:
    if d['sarea'] == '大安區': #篩選出大安區的站點
        clist.append(d)

for c in clist:
    print(c['mday'],  c['sna'],"可借數量:", c['available_rent_bikes'],"空位數量:", c['available_return_bikes']) #列出站點名稱、站點代號、空位數量

print("大安區共有", len(clist), "個YouBike站點")

import pandas as pd
df = pd.DataFrame(clist)
df.to_csv("youbike專案/youbike.csv", index=False, encoding="utf-8-sig") #將大安區的YouBike站點資料存成CSV檔









