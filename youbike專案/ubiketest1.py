#台北市大安區大安區 YouBike 站點可用車輛比例分析 (前30名)

import pandas as pd
import matplotlib.pyplot as plt
import urllib.request as request
import json

# 1. 抓取資料
src = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
with request.urlopen(src) as response:
    data = json.load(response)

# 2. 篩選大安區資料並計算比例
daan_list = []
for d in data:
    if d['sarea'] == '大安區':
        rent = d['available_rent_bikes']
        return_slots = d['available_return_bikes']
        total = rent + return_slots
        
        daan_list.append({
            '站點名稱': d['sna'].replace("YouBike2.0_", ""), # 去掉前綴讓圖表乾淨點
            '可借車數': rent,
            '比例': (rent / total * 100) if total > 0 else 0
        })

df = pd.DataFrame(daan_list)
df = df.sort_values(by='比例', ascending=False).head(30) # 取前 30 個站點避免圖表太擠

# 3. 繪圖設定 (解決中文亂碼問題)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False 

plt.figure(figsize=(12, 8))
bars = plt.barh(df['站點名稱'], df['比例'], color='skyblue')

# 加入標籤與標題
plt.xlabel('可借車輛比例 (%)')
plt.title('大安區 YouBike 站點可用車輛比例 (前30名)', fontsize=16)
plt.gca().invert_yaxis() # 讓比例最高的在上面

# 在條形圖末端標示百分比
for bar in bars:
    width = bar.get_width()
    plt.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center')

plt.tight_layout()
plt.show()