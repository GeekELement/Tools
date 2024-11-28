import random
import time
import pyautogui
import subprocess

# 定义 Edge 和 Chrome 的路径
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Bing 搜索引擎的 URL
bing_url = "https://www.bing.com"

# 重复 Edge 打开次数
repeat_count_edge = 30  # 根据需要设置次数

# 重复 Chrome 打开次数
repeat_count_chrome = 10  # 根据需要设置次数

for _ in range(repeat_count_edge):
    # 使用 Edge 浏览器打开
    subprocess.Popen(edge_path)  # 直接通过命令行打开浏览器

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

    # 关闭 Edge 浏览器窗口
    subprocess.call(["taskkill", "/IM", "msedge.exe", "/F"])
    
    # 等待任务被彻底关闭
    time.sleep(3)  # 增加等待时间以确保浏览器完全关闭

# 切换浏览器间隙    
time.sleep(5)

for _ in range(repeat_count_chrome):
    # 使用 Chrome 浏览器打开 Bing
    subprocess.Popen([chrome_path, bing_url])  # 直接通过命令行打开浏览器并指定 URL

    # 等待 Chrome 打开
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

    # 关闭 Chrome 浏览器窗口
    subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    
    # 等待任务被彻底关闭
    time.sleep(5)  # 增加等待时间以确保浏览器完全关闭
