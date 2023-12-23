import configparser
import os
# import pyautogui
# import asyncio
# import websockets
# import pystray
# from PIL import Image
import win32gui
import win32api
import win32process
# import time

WM_INPUTLANGCHANGEREQUEST = 0x0050  # win32api const


def isWorkInThisProgram():
    string = "Jut.su"

    hwnd = win32gui.GetForegroundWindow()

    title = win32gui.GetWindowText(hwnd)

    index = title.find(string)

    if index != -1:
        return True
    else:
        return False


def cL(layout_id=0):
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle,
                                  WM_INPUTLANGCHANGEREQUEST,
                                  0,
                                  layout_id)
    if result == 0:
        return True
    else:
        return result


def get_l():
    window_handle = win32gui.GetForegroundWindow()
    thread_id = win32process.GetWindowThreadProcessId(window_handle)[0]
    layout_id = win32api.GetKeyboardLayout(thread_id)
    return layout_id


start_l = get_l()

if (start_l != 67699721):
    cL(67699721)

# Get the current working directory
current_dir = os.getcwd()

# Construct the path to the main.pyw file
main_file_path = os.path.join(current_dir, "p2.pyw")


# Открываем конфигурационный файл
config = configparser.ConfigParser()
config.read("config.ini")

# Получаем доступ к разделу lang
lang = config["lang"]

# Устанавливаем новое значение параметра base.lang
lang["base.lang"] = str(start_l)

with open('config.ini', 'w') as configfile:    # save
    config.write(configfile)


# Open the main.pyw file
# os.system(f'\"{main_file_path}\" exit')
os.system(f'start "" "{main_file_path}" exit')
