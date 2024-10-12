import base64
import io
from IPython.display import display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager, rcParams
import matplotlib as mpl
import matplotlib.font_manager as fm
from realestate import read_city_data, city_files

zh_font = fm.FontProperties(fname='C:\\Windows\\Fonts\\NotoSansCJKtc-Black.otf')


# 設定中文字體
rcParams['font.sans-serif'] = ['Source Han Serif TW VF']  # 確保安裝了相應的字體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

def query_real_estate(city, min_price, max_price):

    if city not in city_files:
        print(f"抱歉，目前不支援 {city} 的資料查詢")
        return

    # 讀取資料
    file_name = city_files[city]
    df = read_city_data(file_name)
    if df is None:
        return

    # 篩選價格範圍
    filtered_df = df[(df['總價元'] >= min_price * 10000) & (df['總價元'] <= max_price * 10000)]

    # 返回篩選後的結果
    return filtered_df

# 繪製泡泡圖的函數
def plot_bubble_chart(df, city):
    # 清理數據：移除缺失或無效的數據
    df = df.dropna(subset=['總價元', '建物移轉總面積平方公尺', '鄉鎮市區'])

    # 按區域分組，計算每個區域的交易總數
    area_count = df['鄉鎮市區'].value_counts()

    # 將每個房屋的區域交易總數作為泡泡大小
    df['泡泡大小'] = df['鄉鎮市區'].apply(lambda x: area_count.get(x, 0))

    # 繪製泡泡圖
    plt.figure(figsize=(12, 8))

    # 使用不同顏色繪製每個區域的泡泡
    unique_areas = df['鄉鎮市區'].unique()
    colors = plt.colormaps.get_cmap('tab20') #, len(unique_areas))  # 使用 'tab20' 顏色映射

    color_map = {area: colors(i) for i, area in enumerate(unique_areas)}

    for area in unique_areas:
        area_data = df[df['鄉鎮市區'] == area]
        plt.scatter(
            area_data['建物移轉總面積平方公尺'],  # x軸：建物面積
            area_data['總價元'],          # y軸：總價
            s=area_data['泡泡大小'] * 10,     # 泡泡大小：區域交易總數
            alpha=0.5,
            color=color_map[area],         #區域多寡
            label=area
        )

    # 設定圖表標題與軸標籤
    plt.title(f"{city} 各區域房屋交易數據", fontproperties=zh_font)
    plt.xlabel('建物移轉總面積 (平方公尺)', fontproperties=zh_font)
    plt.ylabel('總價 (元)', fontproperties=zh_font)

    # 添加圖例
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1), title="區域", 
               title_fontproperties=zh_font, prop=zh_font)

    # 顯示圖表
    plt.tight_layout()
    #plt.show()

     # 將圖片保存到記憶體中
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    # 將圖片轉換為 base64 編碼的字符串
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return img_base64

    # 繪製顏色比照圖
    #plot_color_legend(color_map)

# 繪製顏色比照圖
def plot_color_legend(color_map):
    """
    繪製顏色比照圖
    """
    fig, ax = plt.subplots(figsize=(12, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    for i, (area, color) in enumerate(color_map.items()):
        rect = patches.Rectangle((0.1 * i, 0.5), 0.1, 0.4, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        plt.text(0.1 * i + 0.05, 0.5, area, va='center', ha='center', fontsize=10, fontproperties=zh_font)

    plt.show()

# 房屋查詢按鈕事件
def print_bubbles(city, min_price, max_price):
    # 查詢房屋資料
    filtered_df = query_real_estate(city, min_price, max_price)
    print(filtered_df)

    # 確認 df 不為空
    if filtered_df is not None and not filtered_df.empty:
        # 繪製泡泡圖
        #return plot_bubble_chart(filtered_df, city)
        img_base64 = plot_bubble_chart(filtered_df, city)
        img_tag = f'<img src="data:image/png;base64,{img_base64}" alt="Bubble Chart">'
        return img_tag
    else:
        print(f"沒有符合價格範圍 {min_price} - {max_price} 萬元的交易資料。")