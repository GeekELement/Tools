import random
import time
import pyautogui
import subprocess
import os
import psutil  # 用来处理进程操作

# 定义 Edge 和 Edge2 的路径
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 原始 Edge 浏览器路径
edge2_shortcut_path = r"C:\Apps\Edge\Edge2\Edge2.lnk"  # 替换为快捷方式路径

# 重复 Edge 打开次数
repeat_count_edge = 30  # 根据需要设置次数

# 重复 Edge2 打开次数
repeat_count_edge2 = 10  # 根据需要设置次数

# 通过进程名称查找并结束浏览器进程
def kill_browser_by_name(process_name):
    # 获取所有进程
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            # 如果进程名称是 msedge.exe
            if proc.info['name'].lower() == process_name.lower():
                print(f"准备终止进程: {proc.info['name']} PID: {proc.info['pid']}")
                
                # 递归获取所有子进程并终止
                for child_proc in proc.children(recursive=True):
                    print(f"终止子进程: {child_proc.info['name']} PID: {child_proc.info['pid']}")
                    child_proc.terminate()  # 尝试正常终止子进程
                    child_proc.wait(timeout=5)  # 等待子进程退出，设置一个最大等待时间
                    if child_proc.is_running():  # 如果子进程仍在运行，强制终止
                        child_proc.kill()
                        print(f"强制终止子进程: {child_proc.info['name']} PID: {child_proc.info['pid']}")
                
                # 终止主进程
                proc.terminate()  # 尝试正常终止主进程
                proc.wait(timeout=5)  # 等待进程正常退出，设置一个最大等待时间
                if proc.is_running():  # 如果进程仍在运行，强制终止
                    proc.kill()
                    print(f"强制终止进程: {proc.info['name']} PID: {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

# 使用 os.startfile() 打开快捷方式
def open_with_shortcut(path):
    os.startfile(path)  # 使用 os.startfile() 启动快捷方式

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
    edge_process.terminate()  # 使用 terminate() 来结束进程
    edge_process.wait(timeout=5)  # 等待进程正常退出，设置一个最大等待时间
    if edge_process.poll() is None:  # 如果进程仍在运行，强制终止
        edge_process.kill()
        print("强制终止原始 Edge 进程")
    
    # 等待任务被彻底关闭
    time.sleep(3)  # 增加等待时间以确保浏览器完全关闭

# 切换浏览器间隙    
time.sleep(5)

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
    kill_browser_by_name('msedge.exe')  # 使用 psutil 查找并结束 Edge 浏览器进程
    
    # 等待任务被彻底关闭
    time.sleep(5)  # 增加等待时间以确保浏览器完全关闭
