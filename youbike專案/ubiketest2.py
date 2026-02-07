#這段程式碼會持續監控大安區的 YouBike 站點狀態，每分鐘更新一次圖表，顯示可借車輛比例最高的前 15 個站點。按 Ctrl+C 可以停止監控。

import pandas as pd
import matplotlib.pyplot as plt
import urllib.request as request
import json
import time

# 解決中文亂碼
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False 

# 開啟互動模式
plt.ion() 

print("開始監控大安區 YouBike 狀態... (按 Ctrl+C 結束)")

try:
    while True:
        # 1. 抓取最新資料
        src = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
        with request.urlopen(src) as response:
            data = json.load(response)

        # 2. 資料處理
        daan_list = []
        for d in data:
            if d['sarea'] == '大安區':
                rent = d['available_rent_bikes']
                return_slots = d['available_return_bikes']
                total = rent + return_slots
                daan_list.append({
                    '站點': d['sna'].replace("YouBike2.0_", ""),
                    '比例': (rent / total * 100) if total > 0 else 0
                })

        df = pd.DataFrame(daan_list).sort_values(by='比例', ascending=False).head(15)

        # 3. 繪圖
        plt.clf() # 清除上一秒的圖表
        bars = plt.barh(df['站點'], df['比例'], color='mediumaquamarine')
        
        plt.xlabel('可借車輛比例 (%)')
        plt.title(f'大安區 YouBike 即時狀態 (更新時間: {time.strftime("%H:%M:%S")})')
        plt.xlim(0, 110) # 固定 X 軸範圍，才不會縮放跳動
        plt.gca().invert_yaxis()

        # 標註百分比文字
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center')

        plt.pause(60) # 暫停 60 秒後進行下一次抓取

except KeyboardInterrupt:
    print("監控已停止")