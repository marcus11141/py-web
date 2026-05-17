#############################################匯入模組##############################################
import requests


#############################################定義類別##############################################
# 這份類別可以看成是把第一次實作天氣功能時的主程式流程拆開整理。
# 原本查天氣、取圖示代碼、組圖示網址、下載圖片都寫在同一段；
# 現在改成一個方法只負責一件事，比較容易看出每個功能各自都在做什麼。
class WeatherAPI:
    """把 Openweather 的查詢流程整理成可重複使用的工具類別"""

    def __init__(self, api_key, lang="zh_tw"):
        # __init_ () 專門負責準備共用設定。
        # 這樣就不用像早期把所有設定都直接寫在主程式裡那樣，
        # 現在查詢時都重新主動處理API金鑰、單位、語言、單位、網址前半段
        self.api_key = api_key  # api_key 是天氣網站辨認身分用的金鑰
        self.unit = "metric"
        self.lang = lang
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        # 目前天氣API的網址前半段
        self.icon_url = "https://openweathermap.org/img/wn/"
        # 天氣圖示網址前半段

    def get_current_weather(self, city_name):
        send_url = (
            f"{self.base_url}appid={self.api_key}&q={city_name}"
            f"&units={self.unit}&lang={self.lang}"
        )
        response = requests.get(send_url)
        return response.json()  # 轉成python字典

    def get_icon_url(self, icon_code):
        # 組出天氣圖示網址
        return f"{self.icon_base_url}{icon_code}@2x.png"
