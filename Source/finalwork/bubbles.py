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

matplotlib.use('Agg')  # 避免在無視窗環境中出現錯誤

# 設定中文字體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# 設定字體路徑
font_path = os.path.abspath('fonts/NotoSansCJKtc-Black.otf')
zh_font = fm.FontProperties(fname=font_path)

def calculate_values(df):
    # 計算 '單價元平方公尺' 並篩選無效數據
    df['單價元平方公尺'] = df['總價元'] / df['建物移轉總面積平方公尺']
    df = df.dropna(subset=['總價元', '建物移轉總面積平方公尺', '鄉鎮市區'])
    return df

def plot_bubble_chart(df, city):
    # 清理數據：移除缺失或無效的數據
    df = df.dropna(subset=['總價元', '建物移轉總面積平方公尺', '鄉鎮市區'])
    
    # 計算單價
    df['單價元平方公尺'] = df['總價元'] / df['建物移轉總面積平方公尺']

    # 按區域分組，計算每個區域的交易總數
    area_count = df['鄉鎮市區'].value_counts()
    df['泡泡大小'] = df['鄉鎮市區'].apply(lambda x: area_count.get(x, 0))

    # 繪製泡泡圖
    plt.figure(figsize=(11, 7))  # 寬,高

    unique_areas = df['鄉鎮市區'].unique()
    colors = plt.cm.tab20  # 使用 'tab20' 顏色映射
    color_map = {area: colors(i / len(unique_areas)) for i, area in enumerate(unique_areas)}

    for area in unique_areas:
        area_data = df[df['鄉鎮市區'] == area]
        plt.scatter(
            area_data['建物移轉總面積平方公尺'],
            area_data['單價元平方公尺'],  # 改為單價
            s=area_data['泡泡大小'] * 10,
            alpha=0.5,
            color=color_map[area],
            label=area
        )

    plt.title(f"{city} 各區域房屋交易單價", fontproperties=zh_font)
    plt.xlabel('建物移轉總面積 (平方公尺)', fontproperties=zh_font)
    plt.ylabel('單價 (元/平方公尺)', fontproperties=zh_font)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1), title="區域", title_fontproperties=zh_font, prop=zh_font)

    # 保存圖表到記憶體
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    # 圖片轉換為 base64 編碼的字符串
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return img_base64

def print_bubbles(city, df):
    '''
    使用資料繪製泡泡圖
    '''
    if not df.empty:
        img_base64 = plot_bubble_chart(df, city)
        img_tag = f'<img src="data:image/png;base64,{img_base64}" alt="Bubble Chart">'
        return img_tag

    return "沒有可用的交易資料。"
