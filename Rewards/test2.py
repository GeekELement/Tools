import random
import time
import pyautogui
import subprocess
import os
import pygetwindow as gw

def start_automation():
    repeat_count = 30  # 每个浏览器执行的搜索次数
    edge_index = 1  # 从 Edge1 开始

    while True:
        edge_path = f"C:\\Apps\\Edge\\Edge{edge_index}\\Edge{edge_index}.lnk"
        if not os.path.exists(edge_path):
            print(f"路径 {edge_path} 不存在，停止自动化。")
            break

        # 打开浏览器
        open_with_shortcut(edge_path)
        time.sleep(5)  # 等待浏览器完全打开

        # 获取初始Edge窗口列表
        initial_windows = gw.getWindowsWithTitle('Microsoft Edge')

        # 打开30个新窗口
        for _ in range(repeat_count):
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(2)

        # 获取所有Edge窗口
        all_windows = gw.getWindowsWithTitle('Microsoft Edge')

        # 获取新增的窗口
        new_windows = all_windows[len(initial_windows):]

        # 在每个新窗口中进行搜索
        for window in new_windows:
            window.activate()
            time.sleep(1)
            random_number = random.randint(100000, 999999)
            pyautogui.typewrite(str(random_number))
            pyautogui.press('enter')
            time.sleep(2)

        # 关闭当前浏览器实例
        kill_browser_with_taskkill("msedge.exe")
        time.sleep(2)  # 等待进程关闭

        edge_index += 1  # 切换到下一个浏览器实例

def open_with_shortcut(path):
    os.startfile(path)

def kill_browser_with_taskkill(process_name):
    subprocess.call(["taskkill", "/IM", process_name, "/F"])

if __name__ == '__main__':
    start_automation()