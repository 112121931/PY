from flask import Flask, render_template, request, render_template_string
from weather import  get_weather_map
from realestate import query_real_estate, download_and_extract_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    option = request.form.get('option')
    location = request.form.get('location')
    min_price = int(request.form.get('min_price_slider'))
    max_price = int(request.form.get('max_price_slider'))

    result = ""
    if option == "download_real_estate":
        download_and_extract_data()
        result = f"實價登錄資訊下載完成"
    elif option == 'weather':
        # 這裡可以加入查詢天氣的邏輯
        result = get_weather_map()._repr_html_()
    elif option == 'real_estate':
        # 這裡可以加入查詢實價登錄的邏輯
        result = query_real_estate(location, min_price, max_price)
    else:
        result = "無效的選項"

    return render_template_string(result)

if __name__ == '__main__':    
    app.run(debug=True)
