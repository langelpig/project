#台北市大安區youbike站點即時狀態地圖

import folium
import urllib.request as request
import json
import os # 導入 os 模組處理路徑

# 1. 抓取最新資料
src = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
with request.urlopen(src) as response:
    data = json.load(response)

# 2. 設定地圖中心點
m = folium.Map(location=[25.0263, 121.5434], zoom_start=14, control_scale=True)

# 3. 處理資料並加入標記
for d in data:
    if d['sarea'] == '大安區':
        name = d['sna'].replace("YouBike2.0_", "")
        lat, lng = d['latitude'], d['longitude']
        rent = d['available_rent_bikes']
        return_slots = d['available_return_bikes']
        
        # 決定顏色邏輯
        if rent == 0:
            color = 'red'
            icon = 'info-sign'
        elif rent < 5:
            color = 'orange'
            icon = 'warning-sign'
        else:
            color = 'green'
            icon = 'ok-sign'
            
        # 建立彈出視窗內容
        popup_text = f"""
        <div style="font-family: Microsoft JhengHei; width: 150px;">
            <h4>{name}</h4>
            <p><b>可借車輛:</b> <span style="color:{color}; font-size:16px;">{rent}</span></p>
            <p><b>可還空位:</b> {return_slots}</p>
            <hr>
            <small>更新時間: {d['updateTime']}</small>
        </div>
        """
        
        folium.Marker(
            location=[lat, lng],
            popup=folium.Popup(popup_text, max_width=200),
            tooltip=name,
            icon=folium.Icon(color=color, icon=icon)
        ).add_to(m)

# 4. 儲存路徑修正
# 取得目前程式檔案所在的資料夾路徑，並確保檔案存在那裡
current_dir = os.path.dirname(os.path.abspath(__file__))
map_file = os.path.join(current_dir, "daan_youbike_map.html")

# 執行存檔
m.save(map_file)

print(f"地圖已生成！檔案已儲存至：{map_file}")