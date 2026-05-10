#######################匯入模組#######################
# 匯入 ttkbootstrap 模組，提供較美觀的 tkinter 元件
from ttkbootstrap import *

# 匯入 sys、os 模組，用來設定工作目錄
import sys
import os
import requests

#######################設定工作目錄########################
# 將工作目錄切換到目前程式所在的資料夾，方便讀取相關檔案
os.chdir(sys.path[0])


#######################定義函數########################
def on_switch_change():
    # 當 Checkbutton 狀態改變時，將目前布林值顯示在標籤上
    check_label.config(text="溫度單位(c/f)")


API_KEY = "892da2f13edf3c7f382637760e72d224"

# OpenWeather 目前天氣資料的 API 網址
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


# 查詢結果顯示語言（zh_tw = 繁體中文）
LANG = "zh_tw"

# 天氣圖標的基礎網址
ICON_BASE_URL = "https://openweathermap.org/img/wn/"

#######################建立視窗########################
# 建立主視窗
window = Tk()

# 設定視窗標題
window.title("天氣查詢")

#######################設定字型########################
# 設定全域預設字型大小
font_size = 20

# 設定所有元件的預設字型
window.option_add("*font", ("Helvetica", font_size))

#######################設定主題########################
# 設定視窗主題樣式
style = Style(theme="minty")

# 設定按鈕與 Checkbutton 的字型樣式
style.configure("my.TButton", font=("Helvetica", font_size))
style.configure("my.TCheckbutton", font=("Helvetica", font_size))

label = Label(window, text="描述:?")
label.grid(row=1, column=3)
label1 = Label(window, text="溫度:?")
label1.grid(row=1, column=2)
entry = Entry(window, width=30)
entry.grid(row=0, column=2)


def show_result():
    entry_text = entry.get()
    # 在這裡可以添加獲取天氣資訊的邏輯，例如使用 requests 發送 API 請求並更新 label 的內容
    send_url = f"{BASE_URL}appid={API_KEY}&q={entry_text}&lang={LANG}"

    # 印出這次發送的請求網址
    print(f"發送的 URL：{send_url}")

    # 這裡用 requests.get() 取得資料，再用 response.json() 轉成字典；基本流程可參考 adv-03/prj-03-get_request.py
    response = requests.get(send_url)
    info = response.json()

    if "weather" in info and "main" in info:
        # 取得目前溫度、天氣描述與圖標代碼
        current_temperature = info["main"]["temp"]
        weather_description = info["weather"][0]["description"]
        icon_code = info["weather"][0]["icon"]

        # 在終端機顯示查詢結果
        print(f"城市：{entry_text}")
        label1.config(text=f"溫度: {current_temperature}")
        label.config(text=f"描述: {weather_description}")
        # 根據圖標代碼組合圖標下載網址
        icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"

        # 印出圖標網址並發送下載請求
        print(f"下載天氣圖標：{icon_url}")
        icon_response = requests.get(icon_url)

    if check_type.get():
        UNITS = "metric"
    else:
        UNITS = "imperial"


button = Button(window, text="獲得天氣資訊", command=show_result)
button.grid(row=0, column=3)
#######################建立變數########################
# BooleanVar 是 tkinter / ttk 用來和元件同步的布林變數
check_type = BooleanVar()

# 預設為勾選狀態
check_type.set(True)

label2 = Label(window, text="請輸入城市名稱")
label2.grid(row=0, column=0)
#######################建立標籤########################
# 建立標籤，顯示目前 Checkbutton 對應的布林值
check_label = Label(window, text="溫度單位(c/f)")

# 將標籤放到視窗中的指定位置
check_label.grid(row=2, column=2)

#######################建立Checkbutton########################
# Checkbutton 會和 check_type 綁在一起
# 勾選時存 True，取消勾選時存 False，並在狀態改變時呼叫 on_switch_change
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
)
# 將 Checkbutton 放到視窗中的指定位置
check.grid(row=2, column=1)

#######################運行應用程式########################
# 開始執行主迴圈，等待使用者操作
window.mainloop()
