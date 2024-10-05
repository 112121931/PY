from flask import Flask, render_template, request, jsonify
import requests
import folium
from cities import get_cities  
from weather import get_weather
from realestate import query_real_estate, download_and_extract_data

app = Flask(__name__)
    
@app.route('/map')
def map_view():
    # 創建地圖
    m = folium.Map(location=[23.6978, 120.9605], zoom_start=8)

    # 添加標記
    
    
    for city, coords in get_cities().items():
        folium.Marker(
        location=coords,
        popup=city,
        tooltip=get_weather(city)
    ).add_to(m)

    # 將地圖保存為HTML文件
    m.save('templates/map.html')
    
    return render_template('map.html')

@app.route('/refresh_map', methods=['POST'])
def refresh_map():
    # 重新生成地圖並返回成功消息
    map_view()
    return jsonify({"message": "Map refreshed successfully"})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    download_and_extract_data()
    app.run(debug=True)
