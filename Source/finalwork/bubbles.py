# 作者: L
# 描述: 繪制泡泡圖
import base64
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm
import matplotlib
from realestate import query_real_estate  # 引入資料查詢函數

matplotlib.use('Agg')

# 設定中文字體
rcParams['axes.unicode_minus'] = False
font_path = os.path.abspath('fonts/NotoSansCJKtc-Black.otf')
zh_font = fm.FontProperties(fname=font_path)

def calculate_values(df):
    """計算單價元平方公尺，並移除無效數據"""
    df['單價元平方公尺'] = df['總價元'] / df['建物移轉總面積平方公尺']
    df = df.dropna(subset=['總價元', '建物移轉總面積平方公尺', '鄉鎮市區'])
    return df

def plot_bubble_chart(df, city):
    """繪製泡泡圖"""
    df = calculate_values(df)  # 使用計算後的值
    area_count = df['鄉鎮市區'].value_counts()
    df['泡泡大小'] = df['鄉鎮市區'].apply(lambda x: area_count.get(x, 0))

    plt.figure(figsize=(11, 7))
    unique_areas = df['鄉鎮市區'].unique()
    colors = plt.cm.tab20
    color_map = {area: colors(i / len(unique_areas)) for i, area in enumerate(unique_areas)}

    for area in unique_areas:
        area_data = df[df['鄉鎮市區'] == area]
        plt.scatter(
            area_data['建物移轉總面積平方公尺'],
            area_data['單價元平方公尺'],
            s=area_data['泡泡大小'] * 10,
            alpha=0.5,
            color=color_map[area],
            label=area
        )

    plt.title(f"{city} 各區域房屋交易單價", fontproperties=zh_font)
    plt.xlabel('建物移轉總面積 (平方公尺)', fontproperties=zh_font)
    plt.ylabel('單價 (元/平方公尺)', fontproperties=zh_font)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1), title="區域", title_fontproperties=zh_font, prop=zh_font)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

def print_bubbles(location, min_price, max_price):
    """查詢並生成泡泡圖"""
    df = query_real_estate(location, min_price, max_price)
    
    if not isinstance(df, pd.DataFrame):
        print("查詢結果不是 DataFrame。")  # 除錯訊息
        raise ValueError("查詢結果不是 DataFrame。")
    
    if df.empty:
        print("查詢結果為空")  # 除錯訊息
        return "沒有符合條件的資料。"

    image_base64 = plot_bubble_chart(df, location)
    return f"<img src='data:image/png;base64,{image_base64}'/>"
