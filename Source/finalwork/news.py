# 作者: 112121931 林智鴻
# 描述: 自由時報區域新聞爬虫程式

import requests
from bs4 import BeautifulSoup
import ipywidgets as widgets
import pandas as pd
from IPython.core.display import HTML

# 定義地點選項
locations = {
    '臺北市': 'https://news.ltn.com.tw/list/breakingnews/Taipei',
    '新北市': 'https://news.ltn.com.tw/list/breakingnews/NewTaipei',
    '桃園市': 'https://news.ltn.com.tw/list/breakingnews/Taoyuan',
    '臺中市': 'https://news.ltn.com.tw/list/breakingnews/Taichung',
    '臺南市': 'https://news.ltn.com.tw/list/breakingnews/Tainan',
    '高雄市': 'https://news.ltn.com.tw/list/breakingnews/Kaohsiung',
    '基隆市': 'https://news.ltn.com.tw/list/breakingnews/Keelung',
    '新竹市': 'https://news.ltn.com.tw/list/breakingnews/Hsinchu',
    '嘉義市': 'https://news.ltn.com.tw/list/breakingnews/Chiayi',
    '新竹縣': 'https://news.ltn.com.tw/list/breakingnews/HsinchuCounty',
    '苗栗縣': 'https://news.ltn.com.tw/list/breakingnews/Miaoli',
    '彰化縣': 'https://news.ltn.com.tw/list/breakingnews/Changhua',
    '南投縣': 'https://news.ltn.com.tw/list/breakingnews/Nantou',
    '雲林縣': 'https://news.ltn.com.tw/list/breakingnews/Yunlin',
    '嘉義縣': 'https://news.ltn.com.tw/list/breakingnews/ChiayiCounty',
    '屏東縣': 'https://news.ltn.com.tw/list/breakingnews/Pingtung',
    '宜蘭縣': 'https://news.ltn.com.tw/list/breakingnews/Yilan',
    '花蓮縣': 'https://news.ltn.com.tw/list/breakingnews/Hualien',
    '臺東縣': 'https://news.ltn.com.tw/list/breakingnews/Taitung',
    '澎湖縣': 'https://news.ltn.com.tw/list/breakingnews/Penghu',
    '金門縣': 'https://news.ltn.com.tw/list/breakingnews/Kinmen',
    '連江縣': 'https://news.ltn.com.tw/list/breakingnews/Matsu'
}

# 創建地點選擇下拉選單
location_dropdown = widgets.Dropdown(
    options=locations,
    description='選擇地點:',
    disabled=False,
)

# 創建新聞標題下拉選單
news_dropdown = widgets.Dropdown(
    options=[],
    description='新聞標題:',
    disabled=False,
)

# 顯示新聞內容
def display_news_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([p.text.strip() for p in paragraphs if '爆' not in p.text and '為達最佳瀏覽效果' not in p.text])
    return f"<h2>{news_dropdown.label}</h2><p>{content}</p>"

# 更新新聞標題選項
def query_news_list(location):
    url = locations[location]

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('a', class_='tit')

    # 提取標題和鏈接
    data = [(headline.text.strip(), headline.attrs['href']) for headline in headlines[:10]]
    print(data)
    # 使用 pandas 生成 HTML 表格
    df = pd.DataFrame(data, columns=['標題', '鏈接'])
    table_html = df.to_html(escape=False, render_links=True, classes='table table-striped')
    print(table_html)
    # 顯示表格
    return table_html
'''
def query_news_list(location):
    url = locations[location]
    return display_news_content(url)
'''    