#######################匯入模組#######################
# 匯入 tkinter 模組
from tkinter import *

# 匯入 PIL 模組，這一課改用 Pillow 載入圖片
from PIL import Image, ImageTk

# pip install pillow
import sys
import os

#######################設定工作目錄########################
# 工作目錄的設定方式在 adv-01/prj-08-loadmage.py 已經介紹過
os.chdir(sys.path[0])


#######################定義函數########################
# event.keysym 可以告訴我們使用者剛剛按了哪一顆鍵
def move_circle(event):
    # 取得按下的按鍵名稱
    key = event.keysym

    # 印出按鍵名稱，方便在終端機觀察事件有沒有正確觸發
    print(key)

    # 方向鍵控制圓形，WASD 控制矩形
    if key == "Right":
        canvas.move(circle, 10, 0)
    elif key == "Left":
        canvas.move(circle, -10, 0)
    elif key == "Up":
        canvas.move(circle, 0, -10)
    elif key == "Down":
        canvas.move(circle, 0, 10)
    elif key == "d":
        canvas.move(rect, 10, 0)
    elif key == "a":
        canvas.move(rect, -10, 0)
    elif key == "w":
        canvas.move(rect, 0, -10)
    elif key == "s":
        canvas.move(rect, 0, 10)


#######################創建主視窗#######################
# 創建主視窗
windows = Tk()

# 設定主視窗標題
windows.title("My first GUI")

#######################創建畫布#######################
# Canvas 的建立方式在 adv-01/prj-07-canvas.py 已經介紹過
canvas = Canvas(windows, width=600, height=600, bg="white")

# 將畫布加入主視窗中
canvas.pack()

#######################設定視窗圖片########################
# 設定視窗圖片
windows.iconbitmap("crocodile2.ico")

#######################載入圖片########################
# 在 adv-01/prj-08-loadmage.py 介紹的是 tkinter 內建的 PhotoImage，這一課改用 Pillow
# 好處：
#   1. 支援幾乎所有格式（JPG、PNG、BMP、WebP、TIFF 等）
#   2. 可在顯示前對圖片做處理（縮放、裁切、旋轉、濾鏡等）
image = Image.open("crocodile2.png")

# 將 PIL Image 物件轉換成 tkinter 可顯示的 PhotoImage 物件
img = ImageTk.PhotoImage(image)

#######################顯示圖片########################
# create_image() 的顯示方式在 adv-01/prj-08-loadmage.py 已經介紹過，這裡把圖片中心點放在畫布的 (300, 300)
my_img = canvas.create_image(300, 300, image=img)
#######################畫圖形########################
# Canvas 畫圖指令的座標都是以畫布左上角為基準
# 在畫布上畫一個圓形，起始位置為 (250,150)，結束位置為 (300,200)，填充顏色為紅色
circle = canvas.create_oval(250, 150, 300, 200, fill="red")

# 在畫布上畫一個矩形，起始位置為 (220,400)，結束位置為 (340,430)，填充顏色為藍色
rect = canvas.create_rectangle(220, 400, 340, 430, fill="blue")

# 在畫布上顯示一段文字，位置為 (300,100)，文字為 Corcodile，顏色為黑色，字型為 Arial，大小為 30
msg = canvas.create_text(300, 100, text="Corcodile", fill="black", font=("Arial", 30))
#######################綁定按鍵事件########################
# bind_all("<Key>", ...) 會讓視窗收到鍵盤輸入時呼叫 move_circle
canvas.bind_all("<Key>", move_circle)
#######################運行應用程式#######################
# 開始執行主迴圈，等待用戶操作
windows.mainloop()
