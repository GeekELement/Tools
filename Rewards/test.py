import random
import time
import pyautogui
import subprocess
import os

# 定义 Edge 和 Edge2 的路径
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 原始 Edge 浏览器路径
edge2_shortcut_path = r"C:\Apps\Edge\Edge2\Edge2.lnk"  # 替换为快捷方式路径

# 重复 Edge 打开次数
repeat_count_edge = 3  # 根据需要设置次数

# 重复 Edge2 打开次数
repeat_count_edge2 = 3  # 根据需要设置次数

# 设置 IP 地址的函数
def set_ip(interface, ip_address, subnet_mask, gateway):
    try:
        subprocess.run(["netsh", "interface", "ip", "set", "address",
                        f"name={interface}", "static", ip_address, subnet_mask, gateway],
                       check=True)
        print(f"IP 地址已设置为 {ip_address}")
    except subprocess.CalledProcessError as e:
        print(f"设置 IP 地址失败: {e}")

# 使用 os.startfile() 打开快捷方式
def open_with_shortcut(path):
    os.startfile(path)  # 使用 os.startfile() 启动快捷方式

# 使用 taskkill 强制关闭浏览器进程
def kill_browser_with_taskkill(process_name):
    subprocess.call(["taskkill", "/IM", process_name, "/F"])  # 通过进程名称强制关闭进程

# 打开 Edge 浏览器并输入随机数
for _ in range(repeat_count_edge):
    edge_process = subprocess.Popen(edge_path)  # 通过命令行启动浏览器并获取进程对象
    time.sleep(2)  # 等待 Edge 打开

    random_number = random.randint(100000, 999999)  # 生成一个六位数的随机数
    time.sleep(1)  # 等待浏览器完全加载

    pyautogui.typewrite(str(random_number))  # 在输入框中输入随机数
    pyautogui.press('enter')  # 模拟按下 Enter
    time.sleep(3)  # 等待搜索结果加载

    kill_browser_with_taskkill("msedge.exe")  # 使用 taskkill 强制关闭浏览器进程
    time.sleep(3)  # 等待任务被彻底关闭

# 切换 IP 地址
set_ip("以太网", "192.168.4.86", "255.255.255.0", "192.168.4.1")  # 设置新的 IP 地址
time.sleep(5)  # 等待 IP 地址切换生效

# 切换浏览器间隙    
time.sleep(5)

# 打开 Edge2 浏览器并输入随机数
for _ in range(repeat_count_edge2):
    open_with_shortcut(edge2_shortcut_path)  # 使用 os.startfile() 启动快捷方式
    time.sleep(3)  # 等待 Edge2 打开

    random_number = random.randint(100000, 999999)  # 生成一个六位数的随机数
    time.sleep(1)  # 等待浏览器完全加载

    pyautogui.typewrite(str(random_number))  # 在输入框中输入随机数
    pyautogui.press('enter')  # 模拟按下 Enter
    time.sleep(3)  # 等待搜索结果加载

    kill_browser_with_taskkill("msedge.exe")  # 使用 taskkill 强制关闭浏览器进程
    time.sleep(5)  # 等待任务被彻底关闭
