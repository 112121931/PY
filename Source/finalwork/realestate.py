'''
# 作者: 112120900 鄭怡婷
# 描述: 於不動產成交案件，實際資料供應系統下載實價登錄資訊檔案
#       查詢實價登入資訊與結合google map，查詢地點
'''

import os
import zipfile
import requests
import pandas as pd

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

def download_and_extract_data():
    '''
    # 下載並解壓縮實價登錄資料
    '''
    # 確保實價登錄資料夾存在
    if not os.path.exists(DATA_DIR):
        print(f"建立{DATA_DIR}資料匣")
        os.makedirs(DATA_DIR)

    print("下載實價登錄資料中...")
    response = requests.get(ZIP_URL, timeout=30)
    with open(ZIP_FILE_PATH, "wb") as zip_file:
        zip_file.write(response.content)
    print("解壓縮資料...")
    with zipfile.ZipFile(ZIP_FILE_PATH, "r") as zip_ref:
        zip_ref.extractall(DATA_DIR)

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


def generate_google_maps_link(address):
    '''
    # 生成 Google Maps 連結
    '''
    return f"https://www.google.com/maps/search/?api=1&query={address}"

def query_real_estate(city, min_price, max_price):
    '''
    # 查詢指定城市的房屋交易資料
    '''
    if city not in city_files:
        return f"抱歉，目前不支援 {city} 的資料查詢"

    # 讀取資料
    file_name = city_files[city]
    df = read_city_data(file_name)
    if df is None:
        return f"抱歉，{city} 的{file_name} 資料檔案不存在，請執行『下載實價登錄資訊』"

    # 將 "土地位置建物門牌" 欄位內容替換為 Google Maps 連結
    df['土地位置建物門牌'] = df['土地位置建物門牌'].apply(
        lambda x: f'<a href="{generate_google_maps_link(x)}" target="_blank">{x}</a>')

    # 篩選價格範圍
    filtered_df = df[(df['總價元'] >= min_price * 1000000) & (df['總價元'] <= max_price * 1000000)]

    # 顯示篩選後的結果
    if not filtered_df.empty:
        print("符合條件的房屋交易資料：")
        table_html = filtered_df[['鄉鎮市區', '土地位置建物門牌', '總價元', '單價元平方公尺']].to_html(
            escape=False, render_links=True, classes='table table-striped')

        bootstrap_link = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
        bootstrap_html = f"<link href=\"{bootstrap_link}\" rel=\"stylesheet\">{table_html}"

        # 顯示表格
        return bootstrap_html

    return f"沒有符合價格範圍 {min_price} - {max_price} 佰萬元的交易資料。"
