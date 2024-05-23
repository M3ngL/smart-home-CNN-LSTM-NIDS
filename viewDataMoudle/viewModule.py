import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from func import clear_window

def viewGraphData(illegal_count, normal_count, window):
    # 创建一个Frame用于放置图像
    frame = tk.Frame(window, bg="lightgray", width=300, height=150)  # 框架大小
    frame.pack(side=tk.LEFT, anchor=tk.SW)

    plt.ion() #开启interactive mode 成功的关键函数
    plt.figure(1)
    plot_x = []
    plot_y1, plot_y2 = [], []

    plt.clf() #清空画布上的所有内容
    plot_x_now = time.time()
    timestamp_in_seconds = plot_x_now
    # 转换为struct_time对象
    current_time = time.gmtime(timestamp_in_seconds)
    # 使用strftime进行格式化
    formatted_time = time.strftime("%H:%M:%S", current_time)
    plot_x.append(formatted_time)#模拟数据增量流入，保存历史数据

    plot_y1.append(illegal_count)
    plot_y2.append(normal_count)
    
    

    fig = Figure(figsize=(6,4))
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    ax.plot(plot_x,plot_y1,'-r', label='Data Set 1')
    ax.plot(plot_x,plot_y2,'-b', label='Data Set 2')

    ax.legend()

    # 添加标题和轴标签
    ax.title('Two Lines on One Plot')
    ax.xlabel('X-axis Label')
    ax.ylabel('Y-axis Label')

def viewTableData(window):
    clear_window(window)
    file_path = 'output.csv'
    df = pd.read_csv(file_path)
    df.fillna(0, inplace=True)
    text = tk.Text(window, wrap=tk.WORD)
    text.pack(expand=True, fill='both')
    text.configure(wrap='none')
    # 将 DataFrame 转换为格式化的字符串，并插入到 Text 组件中
    text.insert(tk.END, df.to_string(index=False))