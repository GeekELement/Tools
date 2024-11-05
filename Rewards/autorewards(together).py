import webbrowser
import random
import time
import pyautogui
import os

# 注册 Edge 浏览器
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))

# 注册 Chrome 浏览器
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# 重复edge搜索的次数
repeat_count_edge = 30  # 根据需要设置次数

# 重复chrome搜索的次数
repeat_count_chrome = 10  # 根据需要设置次数

for _ in range(repeat_count_edge):
    # 生成一个六位数的随机数
    random_number = random.randint(100000, 999999)

    # 使用 Edge 浏览器打开 Bing
    webbrowser.get('edge').open('https://www.bing.com')

    # 等待 Edge 打开
    time.sleep(3)  # 根据需要调整时间

    # 在输入框中输入随机数
    pyautogui.typewrite(str(random_number))

    # 模拟按下 Enter
    pyautogui.press('enter')

    # 等待搜索结果加载
    time.sleep(3)  # 根据需要调整时间

    # 关闭 Edge 浏览器窗口
    os.system("taskkill /IM msedge.exe /F")
    
    # 等待任务被彻底关闭
    time.sleep(3)
    

# 切换浏览器间隙    
time.sleep(3)


for _ in range(repeat_count_chrome):
    # 生成一个六位数的随机数
    random_number = random.randint(100000, 999999)

    # 使用 Chrome 浏览器打开 Bing
    webbrowser.get('chrome').open('https://www.bing.com')

    # 等待 Chrome 打开
    time.sleep(3)  # 根据需要调整时间

    # 在输入框中输入随机数
    pyautogui.typewrite(str(random_number))

    # 模拟按下 Enter
    pyautogui.press('enter')

    # 等待搜索结果加载
    time.sleep(3)  # 根据需要调整时间

    # 关闭 Chrome 浏览器窗口
    os.system("taskkill /IM chrome.exe /F")
    
    # 等待任务被彻底关闭
    time.sleep(3)
