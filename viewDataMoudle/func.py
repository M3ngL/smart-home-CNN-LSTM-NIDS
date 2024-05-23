
import subprocess
import tkinter as tk

def help():
    subprocess.Popen(['notepad.exe', 'help.txt'])

def getFlow():
    script_path = "Design/dataProcess/main.py"
    subprocess.call(["python", script_path])


def clear_window(window):
    for widget in window.winfo_children():
        if not isinstance(widget, tk.Menu):  # 检查是否是菜单
            widget.destroy()
