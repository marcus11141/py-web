#######################匯入模組#######################
# 匯入 ttkbootstrap 模組，這個美化版 tkinter 元件在 adv-02/prj-04-ttk_GUI.py 已經介紹過
from ttkbootstrap import *

# 匯入 sys、os 模組，用來設定工作目錄
import sys
import os

# 匯入 filedialog，用來開啟檔案選擇視窗
from tkinter import filedialog

# 匯入 PIL 模組，用來讀取與顯示圖片
from PIL import Image, ImageTk

#######################設定工作目錄########################
# 工作目錄的設定方式在 adv-01/prj-08-loadmage.py 已經介紹過
os.chdir(sys.path[0])


#######################定義函數########################
def open_file():
    global file_path

    # askopenfilename() 會跳出檔案選擇視窗，回傳使用者選到的完整路徑
    file_path = filedialog.askopenfilename(initialdir=sys.path[0])
    if file_path == "":  # 如果使用者按了「取消」，就不繼續往下執行
        return
    label2.config(text=file_path)  # 顯示檔名


def show_image():  # 顯示圖片
    global file_path
    image = Image.open(file_path)  # 打開圖片檔案
    # 調整圖片大小，讓它適合畫布的大小
    # Image.LANCZOS 是一種縮放魔法✨，就像把大象照片縮小放進相框時，
    # 它會很仔細地把顏色混合好，讓圖片縮小後還是清楚好看，不會變得模糊或鋸齒狀
    image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
    # 轉換成tkinter可以用的格式
    photo = ImageTk.PhotoImage(image)
    # 在畫布上顯示圖片，圖片的左上角會對齊畫布的左上角
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo  # 保留圖片，避免被垃圾回收機制回收


#######################建立視窗########################
window = Tk()  # 建立視窗
window.title("My GUI")  # 設定視窗標題

#######################設定字型########################
# option_add() 設定預設字型的概念在 adv-02/prj-04-ttk_GUI.py 已經介紹過
font_size = 20
window.option_add("*font", ("Helvetica", font_size))

#######################設定主題########################
# Style 與按鈕樣式的設定在 adv-02/prj-04-ttk_GUI.py 已經介紹過
style = Style(theme="minty")
style.configure("my.TButton", font=("Helvetica", font_size))

#######################建立標籤########################
label = Label(window, text="選擇檔案:")
label.grid(row=0, column=0, sticky="E")

label2 = Label(window, text="無")
label2.grid(row=0, column=1, sticky="E")

#######################建立按鈕########################
# Button 搭配 grid 的寫法在 adv-02/prj-04-ttk_GUI.py 已經介紹過
button = Button(window, text="瀏覽", command=open_file, style="my.TButton")
button.grid(row=0, column=2, sticky="W")

button2 = Button(window, text="顯示", command=show_image, style="my.TButton")
button2.grid(row=1, column=0, columnspan=3, sticky="EW")

#######################建立畫布########################
# Canvas 的建立方式在 adv-01/prj-07-canvas.py 已經介紹過
canvas = Canvas(window, width=600, height=600)
canvas.grid(row=2, column=0, columnspan=3)

#######################運行應用程式########################
window.mainloop()
