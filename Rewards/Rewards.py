import os
import random
import string
import subprocess
import time

import pyautogui


def start_automation():
    repeat_count = 25
    edge_index = 1

    while True:
        edge_path = f"C:\\Edge\\Edge{edge_index}\\Edge{edge_index}.lnk"
        if not os.path.exists(edge_path):
            print(f"路径 {edge_path} 不存在，停止自动化。")
            break

        open_with_shortcut(edge_path)
        time.sleep(2)

        for attempt in range(repeat_count):
            random_text = generate_random_text(6)
            search_with_clipboard(random_text)
            time.sleep(2)

            if attempt < repeat_count - 1:
                pyautogui.hotkey("ctrl", "t")
                time.sleep(2)

        kill_browser_with_taskkill("msedge.exe")
        time.sleep(2)
        edge_index += 1


def open_with_shortcut(path):
    os.startfile(path)


def generate_random_text(length):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def search_with_clipboard(text):
    pyautogui.hotkey("ctrl", "l")
    time.sleep(random.uniform(0.1, 0.3))
    type_text_with_random_delay(text)
    pyautogui.press("enter")
    time.sleep(random.uniform(0.1, 0.3))
    pyautogui.press("enter")


def type_text_with_random_delay(text):
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(0, 0.5))


def kill_browser_with_taskkill(process_name):
    subprocess.call(["taskkill", "/IM", process_name, "/F"])


if __name__ == "__main__":
    start_automation()
