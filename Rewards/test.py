import random
import time
import pyautogui
import subprocess
import os

# 定义 Edge 和 Edge2 的路径
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 原始 Edge 浏览器路径
edge2_shortcut_path = r"C:\Apps\Edge\Edge2\Edge2.lnk"  # 替换为快捷方式路径

# 重复 Edge 打开次数
repeat_count_edge = 30  # 根据需要设置次数

# 重复 Edge2 打开次数
repeat_count_edge2 = 30  # 根据需要设置次数

# 使用 os.startfile() 打开快捷方式
def open_with_shortcut(path):
    os.startfile(path)  # 使用 os.startfile() 启动快捷方式

# 使用 taskkill 强制关闭浏览器进程
def kill_browser_with_taskkill(process_name):
    subprocess.call(["taskkill", "/IM", process_name, "/F"])  # 通过进程名称强制关闭进程

for _ in range(repeat_count_edge):
    # 使用 Edge 浏览器打开
    edge_process = subprocess.Popen(edge_path)  # 通过命令行启动浏览器并获取进程对象

    # 等待 Edge 打开
    time.sleep(2)  # 根据需要调整时间

    # 生成一个六位数的随机数
    random_number = random.randint(100000, 999999)

    # 等待一段时间，确保浏览器完全加载
    time.sleep(1)  # 等待浏览器完全加载

    # 在输入框中输入随机数
    pyautogui.typewrite(str(random_number))

    # 模拟按下 Enter
    pyautogui.press('enter')

    # 等待搜索结果加载
    time.sleep(3)  # 根据需要调整时间

    # 关闭 Edge 浏览器进程
    kill_browser_with_taskkill("msedge.exe")  # 使用 taskkill 强制关闭浏览器进程
    
    # 等待任务被彻底关闭
    time.sleep(3)  # 增加等待时间以确保浏览器完全关闭

# 切换浏览器间隙    
time.sleep(5)
#change ip
for _ in range(repeat_count_edge2):
    # 使用 os.startfile() 打开 Edge2 快捷方式
    open_with_shortcut(edge2_shortcut_path)  # 使用 os.startfile() 启动快捷方式

    # 等待 Edge2 打开
    time.sleep(3)  # 根据需要调整时间

    # 生成一个六位数的随机数
    random_number = random.randint(100000, 999999)

    # 等待一段时间，确保浏览器完全加载
    time.sleep(1)  # 等待浏览器完全加载

    # 在输入框中输入随机数
    pyautogui.typewrite(str(random_number))

    # 模拟按下 Enter
    pyautogui.press('enter')

    # 等待搜索结果加载
    time.sleep(3)  # 根据需要调整时间

    # 关闭 Edge2 浏览器进程
    kill_browser_with_taskkill("msedge.exe")  # 使用 taskkill 强制关闭浏览器进程
    
    # 等待任务被彻底关闭
    time.sleep(5)  # 增加等待时间以确保浏览器完全关闭
