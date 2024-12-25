# filepath: /w:/MyProjects/WeChatWarning/lab.py
import time
from threading import Thread, Event
import pygetwindow as gw
from wxauto import WeChat
import tkinter as tk
from tkinter import messagebox
import win32gui
import pystray
from PIL import Image, ImageDraw
import sys
import re

# 读取警告列表
def read_warning_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content.split('\n')

try:
    warningList = read_warning_list('warningList.txt')
except FileNotFoundError:
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    root.attributes('-topmost', True)  # 将窗口置于最前
    messagebox.showwarning("错误","文件【warningList.txt】不存在")
    sys.exit(1)  # 终止程序

keepGoing = True
wx = WeChat()
lastWarnedChat = None  # 用于跟踪上一次打印的联系人

def create_image():
    # 生成一个图标
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=(255, 0, 0))
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=(0, 255, 0))
    return image

def on_exit(icon, item):
    icon.stop()
    global keepGoing
    keepGoing = False

def check_wechat():
    global lastWarnedChat
    while keepGoing:
        hwnd = win32gui.GetForegroundWindow()
        frontTitle = win32gui.GetWindowText(hwnd)
        if frontTitle == "微信": # 检测微信是否在前台
            wechat_window = gw.getWindowsWithTitle('微信')
            if len(wechat_window) > 0:
                wechat_window = wechat_window[0]
                if wechat_window.isMinimized or not wechat_window.visible:
                    lastWarnedChat = None  # 重置 lastWarnedChat
                    time.sleep(1)  # 暂停检测,等待窗口恢复
                    continue
                if wechat_window.isActive:
                    # 获取微信窗口对象
                    currentChat = wx.CurrentChat()  # 当前聊天窗口名称
                    if currentChat:
                        currentChat=re.sub(r'\s?\(.*\)$', '', currentChat) # 正则表达去除最后括号中的内容
                        if currentChat != lastWarnedChat:
                            lastWarnedChat = None  # 重置 lastWarnedChat
                        if currentChat in warningList and currentChat != lastWarnedChat:  # 判断是否在警告列表中且不同于上一次打印的联系人
                            root = tk.Tk()
                            root.withdraw()  # 隐藏主窗口
                            root.attributes('-topmost', True)  # 将窗口置于最前
                            messagebox.showwarning("警告", f"当前会话【{currentChat}】在警告列表中!")
                            lastWarnedChat = currentChat  # 更新上一次打印的联系人
        else:
            lastWarnedChat = None
        time.sleep(1)  # 暂停检测,等待窗口恢复

icon = pystray.Icon("WeChatWarning", title="WeChatWarning")
icon.icon = create_image()
icon.menu = pystray.Menu(pystray.MenuItem("退出", on_exit))

Thread(target=check_wechat).start()
icon.run()