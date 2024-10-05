from flask import Flask, render_template, request
import requests
import folium

app = Flask(__name__)

API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
API_KEY = "CWA-D5B056EA-33C1-4099-9FE8-C6282F14A951"

# 台灣縣市經緯度資料 (請自行補充完整資料)
county_data = {
    "臺北市": [25.04776, 121.5170],
    "新北市": [25.0120, 121.4624],
    "桃園市": [24.9932, 121.3005],
    "臺中市": [24.1465, 120.6840],
    "臺南市": [23.0011, 120.2037],
    "高雄市": [22.6203, 120.3100],
    "基隆市": [25.1330, 121.7418],
    "新竹市": [24.8038, 120.9690],
    "嘉義市": [23.4824, 120.4333],
    "新竹縣": [24.8038, 121.0000],  # 估計經緯度
    "苗栗縣": [24.5682, 120.8208],
    "彰化縣": [24.0694, 120.5400],
    "南投縣": [23.9000, 120.8000],  # 估計經緯度
    "雲林縣": [23.7000, 120.4500],  # 估計經緯度
    "嘉義縣": [23.5000, 120.3500],  # 估計經緯度
    "屏東縣": [22.6700, 120.5000],  # 估計經緯度
    "宜蘭縣": [24.7500, 121.7500],  # 估計經緯度
    "花蓮縣": [23.9800, 121.5800],  # 估計經緯度
    "臺東縣": [22.7500, 121.1000],  # 估計經緯度
    "澎湖縣": [23.5700, 119.6000],  # 估計經緯度
    "金門縣": [24.4500, 118.3500],  # 估計經緯度
    "連江縣": [26.1500, 119.9500]   # 估計經緯度
    }

# 查詢天氣
def get_weather(city):
    params = {
        "Authorization": API_KEY,
        "locationName": city
    }
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'records' in data and 'location' in data['records']:
            location_data = data['records']['location']
            for location in location_data:
                if location['locationName'] == city:
                    weather_elements = location['weatherElement']
                    weather_description = weather_elements[0]['time'][0]['parameter']['parameterName']
                    max_temp = weather_elements[4]['time'][0]['parameter']['parameterName']
                    min_temp = weather_elements[2]['time'][0]['parameter']['parameterName']
                    return f"{city} 的天氣狀況：{weather_description}\n最高溫度：{max_temp}°C\n最低溫度：{min_temp}°C"
        else:
            return f"無法取得 {city} 的天氣資料。"
    else:
        return "API 請求失敗，請稍後再試。"
    
@app.route('/')
def home():
    # 創建地圖
    m = folium.Map(location=[23.6978, 120.9605], zoom_start=8)

    # 添加標記
    
    
    for county, coords in county_data.items():
        folium.Marker(
        location=coords,
        popup=county,
        tooltip=get_weather(county)
    ).add_to(m)

    # 將地圖保存為HTML文件
    m.save('templates/map.html')
    
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
