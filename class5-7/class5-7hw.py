#######################匯入模組#######################
# 匯入 requests 套件，用來發送 API 請求
import requests

# 匯入 os、sys 模組，用來設定工作目錄
import os
import sys

from ttkbootstrap import *

from tkinter import filedialog

Windows = Tk()
Windows.title("天氣查詢")
#######################定義常數########################
# OpenWeather API 金鑰
API_KEY = "892da2f13edf3c7f382637760e72d224"

# OpenWeather 目前天氣資料的 API 網址
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# 查詢時使用的溫度單位（metric = 攝氏）
UNITS = "metric"

# 查詢結果顯示語言（zh_tw = 繁體中文）
LANG = "zh_tw"

# 天氣圖標的基礎網址
ICON_BASE_URL = "https://openweathermap.org/img/wn/"

#######################匯入模組#######################
# 匯入 ttkbootstrap 模組，這個美化版 tkinter 元件在 adv-02/prj-04-ttk_GUI.py 已經介紹過
from ttkbootstrap import *

#######################主程式########################
# 將工作目錄切換到目前程式所在的資料夾
os.chdir(sys.path[0])

canvas = Canvas(Windows, width=600, height=600, bg="white")
while True:
    # 讓使用者輸入想查詢天氣的城市名稱
    city_name = input("請輸入城市名稱：")

    # 組合查詢天氣資料的 API URL
    send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"

    # 印出這次發送的請求網址
    print(f"發送的 URL：{send_url}")

    # 這裡用 requests.get() 取得資料，再用 response.json() 轉成字典；基本流程可參考 adv-03/prj-03-get_request.py
    response = requests.get(send_url)
    info = response.json()

    # 如果成功取得 weather 與 main 欄位，就顯示天氣資訊並下載圖標
    if "weather" in info and "main" in info:
        # 取得目前溫度、天氣描述與圖標代碼
        current_temperature = info["main"]["temp"]
        weather_description = info["weather"][0]["description"]
        icon_code = info["weather"][0]["icon"]

        # 在終端機顯示查詢結果
        print(f"城市：{city_name}")
        print(f"溫度：{current_temperature}°C")
        print(f"描述：{weather_description}")
