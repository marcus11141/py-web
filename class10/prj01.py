##################################模組####################################
# asyncio是python內建的非同步工具
# 可以把它想成 任務小管家 :如果某件事需要等網路回應，他可以先去處理其他事情，不會讓種個程式傻傻卡住
import os
import asyncio
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


# @bot.event 這種寫法叫裝飾器，
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


def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))
    # 如果這份檔案室直接執行，
    # 就呼叫main() 啟動機器人!


if __name__ == "__main__":
    main()  # 正式啟動程式
