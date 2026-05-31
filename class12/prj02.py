import requests

API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
UNITS = "metric"
LANG = "zh_tw"

city_name = "Taipei"
send_url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
print(f"發送的URL:{send_url}")
response = requests.get(send_url)
response.raise_for_status()
info = response.json()

if "city" in info:
    for forecast in info["list"]:
        date_time = forecast["dt_txt"]
        temperature = forecast["main"]["temp"]
        weather_description = forecast["weather"][0]["description"]
        print(f"{date_time}: {weather_description}, 溫度: {temperature}°C")
else:
    print("找不到該城市")
