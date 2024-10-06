import os
from flask import Flask, render_template, request, jsonify, render_template_string
import requests
from weather import get_weather, get_weather_map
from realestate import query_real_estate, download_and_extract_data

app = Flask(__name__)

@app.route('/map')
def map_view():    
    m = get_weather_map()
    return render_template('map.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    option = request.form.get('option')
    location = request.form.get('location')
    result = ""
    if option == "download_real_estate":
        download_and_extract_data()
        result = f"實價登錄資訊下載完成"
    elif option == 'weather':
        # 這裡可以加入查詢天氣的邏輯
        result = f"<iframe id=\"result_frame\" src=\"/map\" width=\"100%\" height=\"100%\"></iframe>"
    elif option == 'real_estate':
        # 這裡可以加入查詢實價登錄的邏輯
        result = f"查詢 {location} 的實價登錄資訊"
    else:
        result = "無效的選項"

    
    return render_template_string(result)

if __name__ == '__main__':    
    app.run(debug=True)
