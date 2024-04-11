# Simple-Hot-Conner-For-Windows
An application that enables Windows the same feature hot-conner that MacOS has.

Very envious of MacOS and Kde's hot corner feature, so wrote one for windows

![show](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHN2M3EzM3hkdTNyc2s1aGU0OG4zOXptc2R3amgxdzh1bmppdmN3aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/quSHP1w9T3UJshDnQS/giphy-downsized-large.gif)

If you want to build it by yourself, clone this repository and execute those commands:

```
pip install tk
pip install pyautogui
pip install pystray
pip install pillow
pip install pyinstaller
pyinstaller -F -w -i icon.ico --add-data 'icon.ico;.' --add-data 'fire-alt.png;.' hot_conner.py
```
then your exe will appears in a dictionary named 'dist' **or you can just download the latest release.**

When you building, use [**UPX**](https://github.com/upx/upx/tree/v3.96) will makes your exe smaller, run command as follow:

```
pyinstaller -F -w -i icon.ico --add-data 'icon.ico;.' --add-data 'fire-alt.png;.' hot_conner.py --upx-dir your/path/to/upx
```
