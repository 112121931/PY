from flask import Flask, render_template, request
import requests
import folium
from cities import get_cities  
from weather import get_weather

app = Flask(__name__)
    
@app.route('/')
def home():
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

if __name__ == '__main__':
    app.run(debug=True)
