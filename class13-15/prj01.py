##################################模組####################################
# asyncio是python內建的非同步工具
# 可以把它想成 任務小管家 :如果某件事需要等網路回應，他可以先去處理其他事情，不會讓種個程式傻傻卡住
import os
import asyncio
import requests
from myfunction.myfunction import WeatherAPI, AIAssistant
import discord  # pip install -U discord.py :這個套件負責跟discord溝通
from dotenv import (
    load_dotenv,
)  # pip install python-dotenv :這個套件負責讀取 .env 檔案裡的環境變數

##################################初始化####################################
load_dotenv()  # 讀取 .env 檔，讓程式可以拿到DC_BOT_TOKEN這類設定資料
# event loop  #可以想成 非同步任務的轉盤
# 哪個工作先做，哪個工作要等一下，會由這個轉盤幫忙安排
# python 3.10 + 在主程式裡不一定會先自動準備好這個轉盤，所以我們先建立一個給discord使用
asyncio.set_event_loop(asyncio.new_event_loop())

# 建立一個新的 event loop，給 Discrod 使用

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

weather_api = WeatherAPI(os.getenv("OPENWEATHER_API_KEY"))
ai_assistant = AIAssistant(os.getenv("OPENAI_API_KEY"))


def build_weather_embed(weather_summary):
    """根據天氣摘要資料，建立一個Discord Embed物件"""
    embed = discord.Embed(
        title=f"{weather_summary['city_name']} 的當前天氣",
        description=f"描述: {weather_summary['description']}",
        color=discord.Color.from_str("#1E90FF"),
    )

    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])
    embed.set_thumbnail(url=icon_url)

    embed.add_field(
        name="溫度", value=f"{weather_summary['temerature_celsius']} °C", inline=False
    )
    return embed


def build_forecast_embeds(forecast_summary):
    """把未來多筆預報資料排成 Discord 卡片清單。"""
    # forecast_summary 裡每一筆都是同一座城市、不同時間點的天氣資料。
    # 這個函式會把它們一筆一筆做成卡片，最後回傳一個清單。
    embeds = []
    for forecast in forecast_summary:
        # 這裡每跑一次迴圈，就建立一張新的預報卡片。
        embed = discord.Embed(
            title=f"{forecast['city_name']} 天氣預報 - {forecast['date_time']}",
            description=f"描述：{forecast['description']}",
            color=discord.Colour.from_str("#1E90FF"),
        )
        # forecast 的 icon_code 也是 WeatherAPI 整理好的資料，可以直接拿來組圖示網址
        icon_url = weather_api.get_icon_url(forecast["icon_code"])
        embed.set_thumbnail(url=icon_url)
        embed.add_field(
            name="溫度",
            value=f"{forecast['temperature_celsius']}°C",
            inline=False,  # 單獨一行顯示，卡片內容會比較整齊
        )
        embeds.append(embed)

    return embeds


# @bot.event 這種寫法叫裝飾器
# 可以把它想成下面函式貼上一張事件管理員標籤。
# def 是一般函式，通常會照順序一路做完。
# async def 是可以搭配 await 的函式；
# 遇到需要等一下的工作時，
# 它可以先暫停，等事情完成後再回來繼續做。
@bot.event
async def on_ready():
    print(f"{bot.user} 已經上線了！")  # 登入成功提示
    # await 等這件事完成後再繼續往下
    # return : 直接結束函式
    # tree.sync() : 把slash指令送去Discord登記
    await tree.sync()


@bot.event
async def on_message(message):
    # message 就是一則剛剛出現在頻道裡的訊息
    if message.author == bot.user:  # 如果是自己說的，就不回應
        return  # return : 直接結束函式
    if message.content == "hello":  # 如果訊息內容是hello
        # send() 需要經過網路送回Discord，要用await等它送完
        await message.channel.send("hey!")  # 回應hey!


@tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    """輸入/hello，機器人會回應hey!"""
    # interaction 就是這次使用指令時送來的資料包，
    # 裡面包含是誰按的、在哪裡按的、指令相關資訊
    await interaction.response.send_message("Hey!")
    # 把Hey! 回傳給使用者


@tree.command(name="weather", description="取得當前天氣資訊")
async def weather(
    interaction: discord.Interaction,
    city: str,
    forecast: bool = False,
    ai: bool = False,
):
    """輸入/weather [城市名稱]，機器人會回應該城市的天氣資訊"""
    await interaction.response.defer()  # 告訴Discord我們正在處理，避免超時
    city = city.strip()  # 去除前後空白

    if not weather_api.api_key:
        await interaction.followup.send(
            "尚未設定WEATHER_API_KEY, 請先在 .env檔裡設定。"
        )
        return
    try:
        if not forecast:
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send(f"找不到 ***{city}*** 的天氣資訊")
                return
            embed = build_weather_embed(weather_summary)
            await interaction.followup.send(embed=embed)
            return

        if not ai:
            forecast_summary = weather_api.get_forecast_summary(city)
            if forecast_summary is None:
                await interaction.followup.send(f"找不到 ***{city}*** 的天氣預報資訊")
                return
            embeds = build_forecast_embeds(forecast_summary)
            await interaction.followup.send(embeds=embeds[:10])
            # Discord限制一次最多只能送10張卡片
            return
        raw_forecast = weather_api.get_forecast(city)
    except (requests.RequestException, KeyError) as e:
        await interaction.followup.send("目前無法取得天氣資訊，請稍後再試。")
        return

    analysis, error = ai_assistant.ask(
        system_prompt="你是一個天氣分析師，請根據提供的天氣預報資料，整理出未來幾天的天氣趨勢、溫度變化和重要天氣事件。",
        user_message=f"請分析以下天氣預報資料:\n{raw_forecast}",
    )
    if error:
        await interaction.followup.send(f"分析天氣資料時發生錯誤: {error}")
    else:
        await interaction.followup.send(f"**{city}** 的天氣分析結果:\n{analysis}")


def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))
    # 如果這份檔案室直接執行，
    # 就呼叫main() 啟動機器人!


if __name__ == "__main__":
    main()  # 正式啟動程式
