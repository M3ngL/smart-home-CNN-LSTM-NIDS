# main.py
import tkinter as tk

import numpy as np
from tkinter import messagebox

import threading
import pystray
from pystray import MenuItem, Menu
from PIL import Image
from art import *

from runModel import run
from func import help, getFlow, clear_window
from viewModule import viewGraphData, viewTableData
from importModule import importModel,importData,importdefaultModel
from judgeModule import judgeFlow
from loggingModule import catLog, enterLog, ProduceLog


def AutoDetectionPart():
    global defaultmodel
    defaultmodel = importdefaultModel()
    while not stop_event.is_set():
        getFlow()
        judgeFlow(defaultmodel)

def AutoDetection():
    global thread
    thread = threading.Thread(target=AutoDetectionPart)
    thread.start()

def closeAuto():
    global thread
    if thread is not None and thread.is_alive():
        stop_event.set()  # 设置停止事件
        # 等待子线程结束
        thread.join()
    else:
        print("Warn! There is no thread")


# showinfo("Info","加载模型中...请稍等")


# 导入模型
# defaultmodel = importdefaultModel()


# 实例化object
window = tk.Tk()
window.iconbitmap('icon.ico')

'''
后台运行部分
'''
def quit_window(icon:pystray.Icon):
    icon.stop()
    window.destroy()
def show_window():
    window.deiconify()
def on_exit():
    window.withdraw()
menu = (
    MenuItem('显示', show_window, default=True), 
    Menu.SEPARATOR, 
    MenuItem('退出', quit_window)
    )
image = Image.open("icon.png")
icon = pystray.Icon("icon", image, "Smart-Home-NIDS", menu)
window.protocol('WM_DELETE_WINDOW', on_exit)
threading.Thread(target=icon.run, daemon=True).start()

stop_event = threading.Event()
'''
主页显示
'''
# 设定窗口的大小
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
Width = 980  # 窗口大小值
Hight = 580
# 计算中心坐标
cen_x = (sw - Width) // 2
cen_y = (sh - Hight) // 2
# 设置窗口大小并居中
window.geometry('%dx%d+%d+%d' % (Width, Hight, cen_x, cen_y))
# window.geometry('1280x680+290+120')
window.configure(bg='white')
# 窗口名字
window.title('智能家居网络入侵检测系统')
# 界面欢迎页

l = tk.Label(window, text=text2art('Smart Home NIDS'),bg='white')
l.pack()


'''
菜单部分
'''
# 创建菜单栏
menubar = tk.Menu(window)

# 菜单分类
menu1 = tk.Menu(menubar, tearoff=0)
menu2 = tk.Menu(menubar, tearoff=0)
menu3 = tk.Menu(menubar, tearoff=0)
menu4 = tk.Menu(menubar, tearoff=0)

# 菜单命名为文件
menubar.add_cascade(label='文件', menu=menu2)
# 第二级菜单
submenu = tk.Menu(menu2) 
# 导入选项
menu2.add_cascade(label='导入文件', menu=submenu)
# Run项
menu2.add_command(label='运行', command=run)
menu2.add_separator()    # 添加一条分隔线
menu2.add_command(label='退出系统', command=window.quit)
# 第三级菜单
thirdmenu = tk.Menu(submenu)
submenu.add_command(label='模型', command=importModel)
submenu.add_command(label='数据集', command=importData)
# 菜单命名为工具
menubar.add_cascade(label='工具', menu=menu1)
menu1.add_command(label='抓取流量', command=getFlow)
menu1.add_command(label='判断流量', command=lambda: judgeFlow(defaultmodel))
menu1.add_command(label='展示流量', command=lambda: viewTableData(window))
menu1.add_command(label='自动化', command=AutoDetection)
menu1.add_command(label='关闭自动化', command=closeAuto)
menu3.add_command(label='历史日志', command=catLog)
# 菜单命名为查看
menubar.add_cascade(label='查看', menu=menu3)
# 菜单命名为窗口
menubar.add_cascade(label='窗口', menu=menu4)
menu4.add_command(label='生成新窗口', command=lambda: clear_window(window))
# 菜单命名为帮助
menubar.add_command(label='帮助', command=help)


# 菜单栏menubar显示
window.config(menu=menubar)


# 主窗口显示
window.mainloop()

