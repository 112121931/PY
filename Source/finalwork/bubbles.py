# 作者: L
# 描述: 繪制泡泡圖
# bubbles.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    colors = plt.cm.get_cmap('tab20', len(unique_areas))
    color_map = {area: colors(i) for i, area in enumerate(unique_areas)}
    
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
    
    plt.title(f"{city} 各區域房屋交易數據")
    plt.xlabel('建物移轉總面積 (平方公尺)')
    plt.ylabel('總價 (元)')
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1), title="區域")
    plt.tight_layout()
    plt.show()

    # 繪製顏色比照圖
    plot_color_legend(color_map)

# 繪製顏色比照圖
def plot_color_legend(color_map):
    fig, ax = plt.subplots(figsize=(12, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    for i, (area, color) in enumerate(color_map.items()):
        rect = patches.Rectangle((0.1 * i, 0.5), 0.1, 0.4, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        plt.text(0.1 * i + 0.05, 0.5, area, va='center', ha='center', fontsize=10)
    
    plt.show()
