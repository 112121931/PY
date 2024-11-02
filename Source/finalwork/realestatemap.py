'''
# 作者: 112121931 林智鴻
# 描述: 於不動產成交案件，實際資料供應系統下載實價登錄資訊檔案
#       查詢實價登入資訊與結合google map，查詢地點
'''

import os
import zipfile
import requests
import pandas as pd
import folium
import re
from geopy.geocoders import Nominatim
import pickle
#from geopy.geocoders import Photon

# 實價登錄資料 URL
ZIP_URL = "https://plvr.land.moi.gov.tw//Download?type=zip&fileName=lvr_landcsv.zip"
DATA_DIR = "real_estate_data"
ZIP_FILE_PATH = os.path.join(DATA_DIR, "lvr_landcsv.zip")

# 台灣各主要城市名稱
city_names = [
    '臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市',
    '基隆市', '新竹市', '嘉義市', '新竹縣', '苗栗縣', '彰化縣',
    '南投縣', '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣',
    '臺東縣', '澎湖縣', '金門縣', '連江縣'
]

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

def read_city_data(file_name):
    '''
    # 讀取指定城市的 CSV 資料
    '''
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
        if df['總價元'].dtype not in {'int64', 'float64'}:
            df['總價元'] = pd.to_numeric(df['總價元'], errors='coerce')
        return df

    print(f"找不到 {file_name} 的資料")
    return None

def clean_address(address):
    print(address)
    # 定義阿拉伯數字、中文數字和全形數字的集合
    arabic_digits = '0123456789'
    chinese_digits = '一二三四五六七八九十'
    fullwidth_digits = '０１２３４５６７８９'

    # 創建正則表達式來匹配這些數字後跟“弄”或“樓”的部分
    pattern = f'[{arabic_digits}{chinese_digits}{fullwidth_digits}]+弄|[{arabic_digits}{chinese_digits}{fullwidth_digits}]+號|[{arabic_digits}{chinese_digits}{fullwidth_digits}]+樓'
    
    # 使用正則表達式進行替換
    cleaned_address = re.sub(pattern, '', address)
    # 去除 '之' (含) 以後的資料
    cleaned_address = re.sub(r'之.*$', '', cleaned_address)
    
    print(cleaned_address)
    return cleaned_address

def get_coordinates(location):
    '''
    查詢座標資訊
    '''
    cache_file = os.path.join(DATA_DIR, 'location_cache.pkl')
    
    # 嘗試從暫存檔中讀取座標資訊
    try:
        with open(cache_file, 'rb') as f:
            location_cache = pickle.load(f)
    except FileNotFoundError:
        location_cache = {}

    # 如果暫存檔中已有該地點的座標，則直接返回
    if location in location_cache:
        return location_cache[location]

    # 否則，使用 geolocator 查詢座標
    geolocator = Nominatim(user_agent="realestatemap")
    location_obj = geolocator.geocode(location, timeout=10)
    
    if location_obj:
        coordinates = (location_obj.latitude, location_obj.longitude)
    else:
        coordinates = None

    # 將查詢結果存入暫存檔
    location_cache[location] = coordinates
    with open(cache_file, 'wb') as f:
        pickle.dump(location_cache, f)

    return coordinates
    
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
    count = 0
    for index, row in filtered_df.iterrows():
        if count >= 10:
            break
        location = get_coordinates(clean_address(row['土地位置建物門牌']))
        if location != None:
            folium.Marker(
            location= location,
            popup=row['鄉鎮市區'],
            tooltip=row['土地位置建物門牌']
            ).add_to(m)
            count += 1

    # 使用 branca.element.Element 來獲取 HTML 表示
    map_html = m.get_root().render()

    return map_html

