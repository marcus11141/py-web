#############################################匯入模組##############################################
import requests
import openai


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
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        # 目前天氣API的網址前半段
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"
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
        return f"{self.icon_url}{icon_code}@2x.png"

    def get_weather_summary(self, city_name):
        info = self.get_current_weather(city_name)

        if "weather" in info and "main" in info:
            return {
                "city_name": info.get("name", city_name),
                "temerature_celsius": round(info["main"]["temp"], 2),
                "description": info["weather"][0]["description"],
                "icon_code": info["weather"][0]["icon"],
            }

        return None  # 沒有拿到主要天氣資料

    def get_icon(self, icon_code):
        # 抓取天氣圖示的主要資料
        icon_url = self.get_icon_url(icon_code)
        response = requests.get(icon_url)
        if response.status_code == 200:
            return response.content  # 回傳圖片的二進位資料
        return None  # 圖片下載失敗

    def get_forecast(self, city_name):
        send_url = (
            f"{self.forecast_url}appid={self.api_key}&q={city_name}"
            f"&units={self.unit}&lang={self.lang}"
        )
        response = requests.get(send_url)
        response.raise_for_status()
        return response.json()

    def get_forecast_summary(self, city_name, count=10):
        """查詢未來天氣預報, 並整理成更容易使用的摘要清單"""
        # 這裡和get_weather_summary()得想法一樣
        # 先把API回傳的原始資料整理好, 再交給主程式使用
        # 這樣Discord Bot 或 GUI 程式不用每次自己拆很多層字典
        forecast_count = max(0, count)

        try:
            info = self.get_forecast(city_name)
        except requests.HTTPError as error:
            response = error.response
            if response is not None and response.status_code == 404:
                return None  # 找不到城市
            raise  # 其他HTTP錯誤繼續往外丟
        if "city" not in info or "list" not in info:
            return None  # 沒有拿到預報資料

        city_label = info["city"].get("name", city_name)
        forecast_summary = []

        for forecast in info["list"][:forecast_count]:
            forecast_summary.append(
                {
                    "city_name": city_label,
                    "date_time": forecast["dt_txt"],
                    "temperature_celsius": round(forecast["main"]["temp"], 2),
                    "description": forecast["weather"][0]["description"],
                    "icon_code": forecast["weather"][0]["icon"],
                }
            )
        print(f"已整理 {len(forecast_summary)} 筆 {city_label} 的天氣預報資料")
        return forecast_summary


class AIAssistant:
    """把 OpenAI 的查詢流程整理成可重複使用的工具類別"""

    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def ask(
        self,
        system_prompt,
        user_message,
        history_messages=None,
        temperature=0.2,
        model="gpt-4o",
    ):
        if not self.api_key:
            return None, "尚未設定OPENAI_API_KEY, 請先在 .env檔裡設定。"

        if history_messages is None:
            history_messages = []

        messages = (
            [{"role": "system", "content": system_prompt}]
            + history_messages
            + [{"role": "user", "content": user_message}]
        )

        print("== 傳給 OpenAI 的訊息 ==")
        for msg in messages:
            print(f"{msg['role']}: {msg['content']}")
        print("=============================")

        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            assistant_message = response.choices[0].message.content

            return assistant_message, None

        except Exception as e:
            return None, f"發生錯誤: {e}"
