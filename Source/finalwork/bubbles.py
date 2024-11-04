# 作者: L
# 描述: 繪制泡泡圖
import base64
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import rcParams
import matplotlib.font_manager as fm
import matplotlib
from realestate import query_real_estate, city_files  # 導入 realestate.py 中的查詢函數和 city_files 字典
matplotlib.use('Agg')  # 避免在無視窗環境中出現錯誤

# 設定中文字體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# 設定字體路徑
font_path = os.path.abspath('fonts/NotoSansCJKtc-Black.otf')
zh_font = fm.FontProperties(fname=font_path)

def plot_bubble_chart(df, city):
    '''
    繪製汽泡圖
    '''
    # 清理數據：移除缺失或無效的數據
    df = df.dropna(subset=['總價元', '建物移轉總面積平方公尺', '鄉鎮市區'])

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
            area_data['總價元'],
            s=area_data['泡泡大小'] * 10,
            alpha=0.5,
            color=color_map[area],
            label=area
        )

    plt.title(f"{city} 各區域房屋交易數據", fontproperties=zh_font)
    plt.xlabel('建物移轉總面積 (平方公尺)', fontproperties=zh_font)
    plt.ylabel('總價 (元)', fontproperties=zh_font)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1), title="區域", title_fontproperties=zh_font, prop=zh_font)

    # 保存圖表到記憶體
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    # 圖片轉換為 base64 編碼的字符串
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return img_base64

def print_bubbles(city, min_price, max_price):
    '''
    查詢實價登錄資料與繪圖
    '''
    filtered_df = query_real_estate(city, min_price, max_price)  # 使用 realestate.py 的查詢函數
    if isinstance(filtered_df, pd.DataFrame) and not filtered_df.empty:
        img_base64 = plot_bubble_chart(filtered_df, city)
        img_tag = f'<img src="data:image/png;base64,{img_base64}" alt="Bubble Chart">'
        return img_tag

    return f"沒有符合價格範圍 {min_price} - {max_price} 萬元的交易資料。"