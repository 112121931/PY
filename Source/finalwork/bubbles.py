# 作者: L
# 描述: 繪制泡泡圖
import os
import base64
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams
import matplotlib.font_manager as fm
import matplotlib
from realestate import read_city_data, city_files
matplotlib.use('Agg')  # 避免在無視窗環境中出現錯誤

# 設定字體路徑
font_path = os.path.abspath('fonts/NotoSansCJKtc-Black.otf')
zh_font = fm.FontProperties(fname=font_path)

# 設定中文字體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

def query_real_estate(city, min_price, max_price):
    '''
    讀取實價登錄資料
    '''
    if city not in city_files:
        print(f"抱歉，目前不支援 {city} 的資料查詢")
        return None
    
    # 讀取城市資料
    df = read_city_data(city)
    
    # 檢查是否成功讀取資料
    if df is None:
        print(f"無法讀取 {city} 的資料，請確認資料是否存在")
        return None
    
    # 篩選價格範圍
    filtered_df = df[(df['總價元'] >= min_price * 10000) & (df['總價元'] <= max_price * 10000)]
    
    return filtered_df


# 繪製泡泡圖的函數
def plot_bubble_chart(df, city):
    '''
    繪製汽泡圖
    '''
    area_count = df['鄉鎮市區'].value_counts()
    df['泡泡大小'] = df['鄉鎮市區'].apply(lambda x: area_count.get(x, 0))

    plt.figure(figsize=(12, 8))

    unique_areas = df['鄉鎮市區'].unique()
    colors = plt.cm.tab20
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
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

def plot_color_legend(color_map):
    """
    繪製顏色比照圖
    """
    _, ax = plt.subplots(figsize=(12, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    for i, (area, color) in enumerate(color_map.items()):
        rect = patches.Rectangle((0.1 * i, 0.5), 0.1, 0.4, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        plt.text(0.1 * i + 0.05, 0.5, area, va='center', ha='center', fontsize=10, fontproperties=zh_font)

    plt.show()

def print_bubbles(city, min_price, max_price):
    '''
    查詢實價登錄資料與繪圖
    '''
    filtered_df = query_real_estate(city, min_price, max_price)
    
    # 確認 df 不為空
    if filtered_df is not None and not filtered_df.empty:
        img_base64 = plot_bubble_chart(filtered_df, city)
        img_tag = f'<img src="data:image/png;base64,{img_base64}" alt="Bubble Chart">'
        return img_tag
    else:
        return "查無符合條件的資料或資料無法讀取"

