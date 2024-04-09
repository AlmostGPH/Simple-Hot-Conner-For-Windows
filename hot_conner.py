import tkinter as tk
import time
import pyautogui
import os
import threading
import sys
from pystray import MenuItem as item, Icon as icon
from PIL import Image
from tkinter import PhotoImage

pyautogui.FAILSAFE = False  # 禁用鼠标移动到屏幕左上角时的异常检测

SETTINGS_FILE = "settings.txt"

def save_settings(wait_time, check_interval):
    with open(SETTINGS_FILE, "w") as file:
        file.write(str(wait_time) + "\n")
        file.write(str(check_interval) + "\n")


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default_settings = (0.3, 0.1)
        #save_settings(*default_settings)
        return default_settings
    else:
        try:
            with open(SETTINGS_FILE, "r") as file:
                settings = file.readlines()
                return float(settings[0].strip()), float(settings[1].strip())
        except Exception as e:
            print("读取设置失败:", e)
            return 0.3, 0.1


def set_startup(enable_startup):
    if enable_startup:
        # 设置开机运行
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "MouseMonitor"
        exe_path = os.path.abspath(sys.argv[0])  # 替换为你的可执行文件路径

        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            print("设置开机自启动成功")
        except Exception as e:
            print("设置开机自启动失败:", e)
    else:
        # 取消开机运行
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "MouseMonitor"

        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, app_name)
            winreg.CloseKey(key)
            print("取消开机自启动成功")
        except Exception as e:
            print("取消开机自启动失败:", e)


def start_monitoring(wait_time, check_interval):
    try:
        while True:
            x, y = pyautogui.position()
            if x <= 10 and y <= 10:
                pyautogui.hotkey('win', 'tab')
                time.sleep(wait_time)
                while True:
                    x, y = pyautogui.position()
                    if x > 10 or y > 10:
                        break
                    time.sleep(check_interval)
            time.sleep(0.005)
    except KeyboardInterrupt:
        print("The procedure has been completed")


def save_and_start(root, entry_wait_time, entry_check_interval):
    wait_time = float(entry_wait_time.get())
    check_interval = float(entry_check_interval.get())
    save_settings(wait_time, check_interval)
    root.destroy()  # 关闭图形界面
    start_thread = threading.Thread(target=start_monitoring, args=(wait_time, check_interval))
    start_thread.daemon = True
    start_thread.start()

def start_program():
    wait_time, check_interval = load_settings()
    start_thread = threading.Thread(target=start_monitoring, args=(wait_time, check_interval))
    start_thread.daemon = True
    start_thread.start()


def stop_program(icon, item):
    os._exit(0)

root = tk.Tk()
root.withdraw()

def main():
    wait_time, check_interval = load_settings()
    # 使用默认设置开始监控
    start_program()
    
    def open_settings(icon, item):
        # 获取图标路径
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            bundle_dir = sys._MEIPASS
        else:
            # we are running in a normal Python environment
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(bundle_dir, 'fire-alt.png')
        dockicon = os.path.join(bundle_dir, 'icon.ico')
        window_icon = PhotoImage(file=icon_path)
        settings_window = tk.Toplevel()
        # 设置任务栏图标

        settings_window.iconbitmap(dockicon)

        settings_window.iconphoto(False, window_icon)   
        settings_window.title("鼠标监控器设置")
        settings_window.geometry("400x200")

        wait_time, check_interval = load_settings()

        label1 = tk.Label(settings_window, text="等待时间（秒）:")
        label1.pack()
        entry_wait_time = tk.Entry(settings_window)
        entry_wait_time.insert(0, str(wait_time))
        entry_wait_time.pack()

        label2 = tk.Label(settings_window, text="检测间隔（秒）:")
        label2.pack()
        entry_check_interval = tk.Entry(settings_window)
        entry_check_interval.insert(0, str(check_interval))
        entry_check_interval.pack()

        def save_and_start_thread():
            save_and_start(settings_window, entry_wait_time, entry_check_interval)

        button = tk.Button(settings_window, text="保存并开始", command=save_and_start_thread)
        button.pack()

        startup_var = tk.BooleanVar()
        startup_checkbox = tk.Checkbutton(settings_window, text="开机自启动", variable=startup_var, command=lambda: set_startup(startup_var.get()))
        startup_checkbox.pack()

        # 启动图形界面的事件循环
        settings_window.mainloop()

    # 获取图标路径
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(bundle_dir, 'icon.ico')

    # 创建系统托盘图标
    #icon_image = Image.open("icon.ico")
    icon_image = Image.open(icon_path)

    menu = (item('设置', open_settings), item('退出', stop_program),)
    icon_obj = icon('MouseMonitor', icon_image, menu=menu)
    icon_obj.run()

    


if __name__ == "__main__":
    main()
