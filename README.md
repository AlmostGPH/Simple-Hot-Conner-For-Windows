# Simple-Hot-Conner-For-Windows
An application that enables Windows the same feature hot-conner that MacOS has.

Very envious of MacOS and Kde's hot corner feature, so wrote one for windows

If you want to build it by yourself, clone this repository and execute those commands:

```
pip install tk
pip install pyautogui
pip install pystray
pip install pillow
pip install pyinstaller
pyinstaller -F -w -i icon.ico --add-data 'icon.ico;.' --add-data 'fire-alt.png;.' hot_conner.py
```
then your exe will appeared in a dictionary named 'dist'
