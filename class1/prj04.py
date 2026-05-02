#######################匯入模組#######################
# ttkbootstrap 是美化版的 tkinter 元件庫
from ttkbootstrap import *  # pip install ttkbootstrap -U

# 匯入 sys、os 模組，用來設定工作目錄
import sys
import os

#######################設定工作目錄########################
# 工作目錄的設定方式在 adv-01/prj-08-loadmage.py 已經介紹過
os.chdir(sys.path[0])


#######################定義函數########################
def test():
    print("test")


#######################建立視窗########################
window = Tk()  # 建立視窗
window.title("My GUI")  # 設定視窗標題

#######################設定字型########################
# option_add() 設定預設字型的概念在 adv-01/prj-06-text_color.py 已經介紹過
font_size = 20
window.option_add("*font", ("Helvetica", font_size))

#######################設定主題########################
# Style 可以直接套用現成主題來美化介面
style = Style(theme="vapor")

# "my.TButton" 的命名邏輯：
# 就像幫東西貼標籤一樣，分成兩個部分，用「.」隔開：
#   前半段 "my"    → 自己取的名字，可以換成任何名字，例如 "big"、"red"
#   後半段 "TButton" → 固定寫法，代表「按鈕」這種元件
#                      T 是 Ttk（一種按鈕工具箱）的縮寫
#                      就像「T恤」的T一樣，是品牌名稱的開頭
# 常見元件的後半段寫法：
#   按鈕 → TButton  標籤 → TLabel  輸入框 → TEntry
style.configure("my.TButton", font=("Helvetica", font_size))  # 設定按鈕字型

#######################建立標籤########################
# grid 用 row / column 排列元件位置，sticky 可控制靠左靠右或橫向撐開
label = Label(window, text="hello world")
label.grid(row=0, column=0, sticky="E")  # sticky="E"靠右對齊

#######################建立按鈕########################
button = Button(window, text="瀏覽", command=test, style="my.TButton")  # 設定按鈕樣式
button.grid(row=0, column=1, sticky="W")
button2 = Button(window, text="顯示", command=test, style="my.TButton")  # 設定按鈕樣式
button2.grid(row=1, column=0, columnspan=2, sticky="EW")

#######################運行應用程式########################
window.mainloop()
