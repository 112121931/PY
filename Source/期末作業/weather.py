import requests

API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
API_KEY = "CWA-D5B056EA-33C1-4099-9FE8-C6282F14A951"

# 查詢天氣
def get_weather(city):
    params = {
        "Authorization": API_KEY,
        "locationName": city
    }
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'records' in data and 'location' in data['records']:
            location_data = data['records']['location']
            for location in location_data:
                if location['locationName'] == city:
                    weather_elements = location['weatherElement']
                    weather_description = weather_elements[0]['time'][0]['parameter']['parameterName']
                    max_temp = weather_elements[4]['time'][0]['parameter']['parameterName']
                    min_temp = weather_elements[2]['time'][0]['parameter']['parameterName']
                    return f"{city} 的天氣狀況：{weather_description}\n最高溫度：{max_temp}°C\n最低溫度：{min_temp}°C"
        else:
            return f"無法取得 {city} 的天氣資料。"
    else:
        return "API 請求失敗，請稍後再試。"