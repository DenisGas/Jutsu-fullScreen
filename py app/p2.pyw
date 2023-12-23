import configparser
import os
import pyautogui
import asyncio
import websockets
import pystray
from PIL import Image
import win32gui
import win32api
# import win32process
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


# def get_l():
#     window_handle = win32gui.GetForegroundWindow()
#     thread_id = win32process.GetWindowThreadProcessId(window_handle)[0]
#     layout_id = win32api.GetKeyboardLayout(thread_id)
#     return layout_id


config = configparser.ConfigParser()
config.read("config.ini")

# Получаем значение параметра base.lang
base_lang = config["lang"]["base.lang"]
print(base_lang)
cL(int(base_lang))


def on_tray_exit(icon, item):
    global exit_flag
    exit_flag = True
    icon.stop()


async def press_f():
    print("ff")
    pyautogui.press('f')


async def echo(websocket, path):
    print(f"Подключен клиент {websocket.remote_address}")

    async for message in websocket:
        print(f"Получено сообщение от клиента: {message}")

        if message == "fullscreen":
            work = isWorkInThisProgram()
            if work == True:
                await press_f()
                print("Переход в полноэкранный режим")

        await websocket.send("fullscreen")


# Создание и настройка трей-иконки
image = Image.open("ico.png")
menu = (
    pystray.MenuItem('Выход', on_tray_exit),
)
icon = pystray.Icon("Jut.su FullScreen", image, "Jut.su Full-Screen", menu)

# Функция для запуска трей-приложения


def run_tray():
    icon.run()


# Запуск асинхронного WebSocket-сервера
start_server = websockets.serve(echo, "localhost", 8765)  # Порт 8765

# Запуск асинхронного трей-приложения
tray_task = asyncio.get_event_loop().run_in_executor(None, run_tray)

# Запуск основного цикла программы


async def main():
    global exit_flag
    while not exit_flag:
        await asyncio.sleep(1)

print("Program Start")


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(tray_task)
asyncio.get_event_loop().run_until_complete(main())
