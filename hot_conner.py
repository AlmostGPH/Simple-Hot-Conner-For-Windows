import tkinter as tk
import time
import pyautogui
import os
import sys
import threading
from pystray import MenuItem as item, Icon as icon
from PIL import Image

pyautogui.FAILSAFE = False  # 禁用鼠标移动到屏幕左上角时的异常检测

SETTINGS_FILE = "settings.txt"


# 指定所需的权限，例如读取和写入权限
# 格式为三位数，每位表示所有者、所属组和其他用户的权限
# 4表示读取权限，2表示写入权限，1表示执行权限
# 例如，'0600' 表示所有者有读写权限，所属组和其他用户没有权限
permissions = 0o600

try:
    # 修改文件权限
    os.chmod(SETTINGS_FILE, permissions)
    print("文件权限修改成功")
except OSError:
    print("修改文件权限时出错")


def convert_png_to_ico(png_path, ico_path):
    img = Image.open(png_path)
    img.save(ico_path, format="ICO")


# 将 "icon.png" 转换为 "icon.ico"
# convert_png_to_ico(r"E:\STUDY\study_tmp\try2\fire-alt.png", "icon.ico")

ICON_PATH = "icon.ico"  # 图标路径


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default_settings = (0.3, 0.1)
        save_settings(*default_settings)
        return default_settings
    else:
        try:
            with open(SETTINGS_FILE, "r") as file:
                settings = file.readlines()
                return float(settings[0].strip()), float(settings[1].strip())
        except Exception as e:
            print("读取设置失败:", e)
            return 0.3, 0.1


def save_settings(wait_time, check_interval):
    with open(SETTINGS_FILE, "w") as file:
        file.write(str(wait_time) + "\n")
        file.write(str(check_interval) + "\n")


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

def stop_program(icon, item):
    os._exit(0)


def main():
    wait_time, check_interval = load_settings()

    root = tk.Tk()
    root.title("鼠标监控器设置")
    root.geometry("400x200")

    label1 = tk.Label(root, text="等待时间（秒）:")
    label1.pack()
    entry_wait_time = tk.Entry(root)
    entry_wait_time.insert(0, str(wait_time))
    entry_wait_time.pack()

    label2 = tk.Label(root, text="检测间隔（秒）:")
    label2.pack()
    entry_check_interval = tk.Entry(root)
    entry_check_interval.insert(0, str(check_interval))
    entry_check_interval.pack()

    button = tk.Button(root, text="保存并开始", command=lambda: save_and_start(root, entry_wait_time, entry_check_interval))
    button.pack()

    startup_var = tk.BooleanVar()
    startup_checkbox = tk.Checkbutton(root, text="开机自启动", variable=startup_var, command=lambda: set_startup(startup_var.get()))
    startup_checkbox.pack()

    root.mainloop()

    # 创建系统托盘图标
    icon_image = Image.open(ICON_PATH)
    menu = (item('退出', stop_program),)
    icon_obj = icon('MouseMonitor', icon_image, menu=menu)
    icon_obj.run()

if __name__ == "__main__":
    main()

