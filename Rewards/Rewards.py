import random
import time
import pyautogui
import subprocess
import os

def start_automation():
    repeat_count = 3  # 每个浏览器执行的搜索次数

    edge_index = 1  # 从 Edge1 开始
    while True:
        edge_path = f"C:\\Edge\\Edge{edge_index}\\Edge{edge_index}.lnk"
        if not os.path.exists(edge_path):
            print(f"路径 {edge_path} 不存在，停止自动化。")
            break

        # 打开浏览器
        open_with_shortcut(edge_path)
        time.sleep(2)  # 等待浏览器完全打开

        # 执行30次搜索
        for _ in range(repeat_count):
            random_number = random.randint(100000, 999999)
            # 输入随机数并搜索
            pyautogui.typewrite(str(random_number))
            pyautogui.press('enter')
            time.sleep(2)  # 等待搜索结果加载

            # 如果还没有完成30次，则新开标签页
            if _ < repeat_count - 1:
                pyautogui.hotkey('ctrl', 't')
                time.sleep(2)  # 等待新标签页加载

        # 30次搜索完成后关闭浏览器
        kill_browser_with_taskkill("msedge.exe")
        time.sleep(2)  # 等待进程关闭

        edge_index += 1  # 切换到下一个浏览器实例

def open_with_shortcut(path):
    os.startfile(path)

def kill_browser_with_taskkill(process_name):
    subprocess.call(["taskkill", "/IM", process_name, "/F"])

if __name__ == '__main__':
    start_automation()