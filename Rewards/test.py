import random
import time
import pyautogui
import subprocess
import os

# 定义 Edge 浏览器的路径
edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",  # Edge
    r"C:\Apps\Edge\Edge2\Edge2.lnk",  # Edge2
    r"C:\Apps\Edge\Edge3\Edge3.lnk"   # Edge3
    # 可以继续添加更多的 Edge 浏览器路径，如 Edge4
]

# 每个浏览器的打开次数
repeat_count = 3  # 每个浏览器的搜索次数

# 设置 IP 地址的函数
def set_ip(interface, base_ip, subnet_mask, gateway):
    try:
        subprocess.run(["netsh", "interface", "ip", "set", "address",
                        f"name={interface}", "static", base_ip, subnet_mask, gateway],
                       check=True)
        print(f"IP 地址已设置为 {base_ip}")
    except subprocess.CalledProcessError as e:
        print(f"设置 IP 地址失败: {e}")

# 使用 os.startfile() 打开快捷方式
def open_with_shortcut(path):
    os.startfile(path)

# 使用 taskkill 强制关闭浏览器进程
def kill_browser_with_taskkill(process_name):
    subprocess.call(["taskkill", "/IM", process_name, "/F"])

# 主程序
if __name__ == "__main__":
    base_ip = 85  # 起始 IP 地址的末尾数字
    subnet_mask = "255.255.255.0"
    gateway = "192.168.4.1"

    for i, edge_path in enumerate(edge_paths):
        # 设置新的 IP 地址
        current_ip = f"192.168.4.{base_ip + i}"  # 例如，85, 86, 87...
        set_ip("以太网", current_ip, subnet_mask, gateway)  # 设置新的 IP 地址
        time.sleep(5)  # 等待 IP 地址切换生效

        for _ in range(repeat_count):
            # 打开浏览器并输入随机数
            if edge_path.endswith('.lnk'):
                open_with_shortcut(edge_path)  # 打开快捷方式
            else:
                edge_process = subprocess.Popen(edge_path)  # 启动浏览器
            time.sleep(2)  # 等待浏览器打开

            random_number = random.randint(100000, 999999)  # 生成一个六位数的随机数
            time.sleep(1)  # 等待浏览器完全加载

            pyautogui.typewrite(str(random_number))  # 输入随机数
            pyautogui.press('enter')  # 模拟按下 Enter
            time.sleep(2)  # 等待搜索结果加载

            kill_browser_with_taskkill("msedge.exe")  # 关闭浏览器进程
            time.sleep(2)  # 等待进程完全关闭

        # 完成所有搜索后再切换 IP 地址
        print(f"完成 {edge_path} 的所有搜索，准备切换到下一个 IP 地址。")
