'''
# 作者: 112121931 林智鴻
# 描述: 主程式，以Flask框架建構主頁面與整合各子功能
'''

import os
from flask import Flask, render_template, request, render_template_string
from weather import  get_weather_map
from realestate import query_real_estate, download_and_extract_data
from realestatemap import query_real_estate_map
from news import query_news_list
from bubbles import print_bubbles

# 設置工作目錄
if os.getcwd().find('finalwork') == -1 :
    os.chdir(f'{os.getcwd()}\\Source\\finalwork')
    print(os.getcwd())  # 查看當前工作目錄

app = Flask(__name__)

@app.route('/')
def index():
    '''
    主畫面
    '''
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    '''
    查詢，處理query的POST訊息
    '''
    option = request.form.get('option')
    location = request.form.get('location')
    min_price = int(request.form.get('min_price_slider'))
    max_price = int(request.form.get('max_price_slider'))

    result = ""
    if option == "download_real_estate":
        download_and_extract_data()
        result = "實價登錄資訊下載完成"
    elif option == 'weather':
        result = get_weather_map()
    elif option == 'real_estate':
        result = query_real_estate(location, min_price, max_price)
    elif option == 'real_estate_map':
        result = query_real_estate_map(location, min_price, max_price)
    elif option == "news":
        return query_news_list(location)
    elif option == "bubbles":
        result = print_bubbles(location, min_price, max_price)
    else:
        result = "無效的選項"

    return render_template_string(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
