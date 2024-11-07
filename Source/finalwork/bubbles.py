# 作者: L
# 描述: 繪制泡泡圖
import base64
import io
import os
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib import rcParams
import matplotlib.font_manager as fm
from realestate import read_city_data
from cities import get_city_files

# 設定字體路徑
font_path = os.path.abspath('fonts/NotoSansCJKtc-Black.otf')
zh_font = fm.FontProperties(fname=font_path)

# 設定中文字體
rcParams['font.sans-serif'] = ['Source Han Serif TW VF']  # 確保安裝了相應的字體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

#資料預處理
def query_real_estate(city, min_price, max_price):
    if city not in get_city_files():
        print(f"抱歉，目前不支援 {city} 的資料查詢")
        return

    # 讀取資料
    file_name = get_city_files()[city]
    df = read_city_data(file_name)
    if df is None:
        return

    # 篩選價格範圍
    filtered_df = df[(df['總價元'] >= min_price * 1000000) & (df['總價元'] <= max_price * 1000000)]

    # 返回篩選後的結果
    return filtered_df

# 繪製泡泡圖的函數
def plot_bubble_chart(df, city):
    # 清理數據：移除缺失或無效的數據
    df = df.dropna(subset=['總價元', '建物移轉總面積平方公尺', '鄉鎮市區'])

    # 確保總價元和建物移轉總面積平方公尺是數字類型，並過濾出大於 0 的值
    df['總價元'] = pd.to_numeric(df['總價元'], errors='coerce')
    df['建物移轉總面積平方公尺'] = pd.to_numeric(df['建物移轉總面積平方公尺'], errors='coerce')
    df = df[(df['總價元'] > 0) & (df['建物移轉總面積平方公尺'] > 0)].dropna(subset=['總價元', '建物移轉總面積平方公尺'])

    # 計算單價元平方公尺和面積轉換為坪
    df['單價元平方公尺'] = df['總價元'] / df['建物移轉總面積平方公尺']
    df['建物移轉總面積坪'] = df['建物移轉總面積平方公尺'] / 3.3058  # 轉換為坪

    # 按區域分組，計算每個區域的交易總數
    area_count = df['鄉鎮市區'].value_counts()
    df['泡泡大小'] = df['鄉鎮市區'].apply(lambda x: area_count.get(x, 0))

    # 使用 Plotly 繪製互動式泡泡圖
    fig = px.scatter(
        df,
        x='建物移轉總面積坪',           # X 軸：建物移轉總面積（坪）
        y='單價元平方公尺',            # Y 軸：每坪單價
        size='泡泡大小',               # 泡泡大小：交易量
        color='鄉鎮市區',               # 顏色代表不同的區域
        hover_name='鄉鎮市區',          # 滑鼠懸停顯示區域名稱
        title=f"{city} 各區域房屋交易數據",
        labels={'建物移轉總面積坪': '建物移轉總面積 (坪)', '單價元平方公尺': '單價 (元/平方公尺)'}
    )

    # 調整圖例以便可以點選篩選
    fig.update_layout(
        legend_title_text='區域',
        title_font=dict(size=20)
    )

    # 將圖表轉換為 base64 圖片，以便在網頁中顯示
    img = io.BytesIO()
    fig.write_image(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return img_base64

# 繪製泡泡圖
def print_bubbles(city, min_price, max_price):    
    filtered_df = query_real_estate(city, min_price, max_price)
    
    # 確認 df 不為空
    if filtered_df is not None and not filtered_df.empty:        
        # 繪製泡泡圖
        img_base64 = plot_bubble_chart(filtered_df, city)
        img_tag = f'<img src="data:image/png;base64,{img_base64}" alt="Bubble Chart">'
        return img_tag
    else:
        print(f"沒有符合價格範圍 {min_price} - {max_price} 萬元的交易資料。")
