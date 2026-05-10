##################################模組####################################
# asyncio是python內建的非同步工具
# 可以把它想成 任務小管家 :如果某件事需要等網路回應，他可以先去處理其他事情，不會讓種個程式傻傻卡住
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
