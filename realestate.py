import os
import zipfile
import requests
import pandas as pd
import folium
import re
from geopy.geocoders import Nominatim

# 實價登錄資料 URL
ZIP_URL = "https://plvr.land.moi.gov.tw//Download?type=zip&fileName=lvr_landcsv.zip"
DATA_DIR = "real_estate_data"
ZIP_FILE_PATH = os.path.join(DATA_DIR, "lvr_landcsv.zip")

# 台灣各主要城市名稱與檔案對應
city_files = {
    '臺北市': 'a_lvr_land_a.csv',
    '新北市': 'f_lvr_land_a.csv',
    '桃園市': 'h_lvr_land_a.csv',
    '臺中市': 'b_lvr_land_a.csv',
    '臺南市': 'd_lvr_land_a.csv',
    '高雄市': 'e_lvr_land_a.csv',
    '基隆市': 'c_lvr_land_a.csv',
    '宜蘭縣': 'g_lvr_land_a.csv',
    '嘉義市': 'i_lvr_land_a.csv',
    '新竹縣': 'j_lvr_land_a.csv',
    '苗栗縣': 'k_lvr_land_a.csv',
    '南投縣': 'm_lvr_land_a.csv',
    '彰化縣': 'n_lvr_land_a.csv',
    '新竹市': 'o_lvr_land_a.csv',
    '雲林縣': 'p_lvr_land_a.csv',
    '嘉義縣': 'q_lvr_land_a.csv',
    '屏東縣': 't_lvr_land_a.csv',
    '花蓮縣': 'u_lvr_land_a.csv',
    '台東縣': 'v_lvr_land_a.csv',
    '金門縣': 'w_lvr_land_a.csv',
    '澎湖縣': 'x_lvr_land_a.csv',
}

def download_and_extract_data():
    '''
    下載並解壓縮實價登錄資料
    '''
    # 確保實價登錄資料夾存在
    if not os.path.exists(DATA_DIR):
        print(f"建立{DATA_DIR}資料夾")
        os.makedirs(DATA_DIR)

    print("下載實價登錄資料中...")
    response = requests.get(ZIP_URL, timeout=30)
    with open(ZIP_FILE_PATH, "wb") as zip_file:
        zip_file.write(response.content)
    print("解壓縮資料...")
    with zipfile.ZipFile(ZIP_FILE_PATH, "r") as zip_ref:
        zip_ref.extractall(DATA_DIR)
    print("下載並解壓縮完成。")

def read_city_data(file_name):
    '''
    讀取指定城市的 CSV 資料
    '''
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
        if df['總價元'].dtype not in {'int64', 'float64'}:
            df['總價元'] = pd.to_numeric(df['總價元'], errors='coerce')
        print(f"成功讀取 {file_name} 資料")
        return df

    print(f"找不到 {file_name} 的資料")
    return None

def generate_google_maps_link(address):
    '''
    生成 Google Maps 連結
    '''
    return f"https://www.google.com/maps/search/?api=1&query={address}"

def query_real_estate(city, min_price, max_price):
    '''
    查詢指定城市的房屋交易資料
    '''
    if city not in city_files:
        return f"抱歉，目前不支援 {city} 的資料查詢"

    # 讀取資料
    file_name = city_files[city]
    df = read_city_data(file_name)
    if df is None:
        return f"抱歉，{city} 的 {file_name} 資料檔案不存在，請執行『下載實價登錄資訊』"

    # 將 "土地位置建物門牌" 欄位內容替換為 Google Maps 連結
    df['土地位置建物門牌'] = df['土地位置建物門牌'].apply(
        lambda x: f'<a href="{generate_google_maps_link(x)}" target="_blank">{x}</a>')

    # 將總價元轉換為帶千分位的格式
    df['總價'] = df['總價元'].apply(lambda x: f'{x:,.0f}' if pd.notnull(x) else '')

    # 將單價元平方公尺轉換為帶千分位的格式
    if '單價元平方公尺' in df.columns:
        df['單價元平方公尺'] = pd.to_numeric(df['單價元平方公尺'], errors='coerce')
        df['單價元平方公尺'] = df['單價元平方公尺'].apply(lambda x: f'{x:,.0f}' if pd.notnull(x) else '')

    # 篩選價格範圍
    filtered_df = df[(df['總價元'] >= min_price * 1000000) & (df['總價元'] <= max_price * 1000000)]

    # 顯示篩選後的結果
    if not filtered_df.empty:
        # 自訂 CSS 樣式讓總價欄位靠右對齊
        table_html = filtered_df[['鄉鎮市區', '土地位置建物門牌', '總價', '單價元平方公尺']].to_html(
            escape=False, render_links=True, classes='table table-striped', index=False)

        # 加入自訂樣式讓總價欄位靠右對齊
        th_style = """
        <style>
            th, td { text-align: center; }
            td:nth-child(3) { text-align: right; } /* 讓第三欄總價靠右對齊 */
            td:nth-child(4) { text-align: right; } /* 讓第四欄單價靠右對齊 */
        </style>
        """

        # 加入 Bootstrap 樣式與列印按鈕
        bs_link = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
        bs_html = f"<link href=\"{bs_link}\" rel=\"stylesheet\">{th_style}{table_html}"
        
        # 加入列印按鈕和JavaScript
        bs_html += """
        <div class="text-center mt-4">
            <button onclick="window.print()" class="btn btn-primary">列印結果</button>
        </div>
        <script>
            function printResult() {
                window.print();
            }
        </script>
        """

        print("篩選到的結果已生成。")
        return bs_html

    print(f"沒有符合價格範圍 {min_price} - {max_price} 佰萬元的交易資料。")
    return f"沒有符合價格範圍 {min_price} - {max_price} 佰萬元的交易資料。"

def clean_address(address):
    # 定義阿拉伯數字、中文數字和全形數字的集合
    arabic_digits = '0123456789'
    chinese_digits = '一二三四五六七八九十'
    fullwidth_digits = '０１２３４５６７８９'

    # 創建正則表達式來匹配這些數字後跟“弄”或“樓”的部分
    pattern = f'[{arabic_digits}{chinese_digits}{fullwidth_digits}]+弄|[{arabic_digits}{chinese_digits}{fullwidth_digits}]+號|[{arabic_digits}{chinese_digits}{fullwidth_digits}]+樓'
    
    # 使用正則表達式進行替換
    cleaned_address = re.sub(pattern, '', address)
    return cleaned_address

def generate_link(lat, lon):
    base_url = "https://www.twipcam.com/api/v1/query-cam-list-by-coordinate"
    link = f"{base_url}?lat={lat}&lon={lon}"
    return link

def get_coordinates(location):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(location)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None
    
def query_real_estate_map(city, min_price, max_price):
    '''
    查詢指定城市的房屋交易資料地圖
    '''
    if city not in city_files:
        return f"抱歉，目前不支援 {city} 的資料查詢"

    # 讀取資料
    file_name = city_files[city]
    df = read_city_data(file_name)
    if df is None:
        return f"抱歉，{city} 的 {file_name} 資料檔案不存在，請執行『下載實價登錄資訊』"

    # 將 "土地位置建物門牌" 欄位內容替換為 Google Maps 連結
    df['土地位置建物門牌'] = df['土地位置建物門牌'].apply(
        lambda x: f'<a href="{generate_google_maps_link(x)}" target="_blank">{x}</a>')

    # 將總價元轉換為帶千分位的格式
    df['總價'] = df['總價元'].apply(lambda x: f'{x:,.0f}' if pd.notnull(x) else '')

    # 將單價元平方公尺轉換為帶千分位的格式
    if '單價元平方公尺' in df.columns:
        df['單價元平方公尺'] = pd.to_numeric(df['單價元平方公尺'], errors='coerce')
        df['單價元平方公尺'] = df['單價元平方公尺'].apply(lambda x: f'{x:,.0f}' if pd.notnull(x) else '')

    # 篩選價格範圍
    filtered_df = df[(df['總價元'] >= min_price * 1000000) & (df['總價元'] <= max_price * 1000000)]

    # 顯示篩選後的結果
    if not filtered_df.empty:
        # 自訂 CSS 樣式讓總價欄位靠右對齊
        table_html = filtered_df[['鄉鎮市區', '土地位置建物門牌', '總價', '單價元平方公尺']].to_html(
            escape=False, render_links=True, classes='table table-striped', index=False)

    m = folium.Map(location=[23.6978, 120.9605], zoom_start=8)

    # 添加標記
    for 土地位置建物門牌 in filtered_df.items():
        folium.Marker(
        location=get_coordinates(土地位置建物門牌),
        popup=city,
        tooltip=''
    ).add_to(m)

    # 使用 branca.element.Element 來獲取 HTML 表示
    map_html = m.get_root().render()

    return map_html

