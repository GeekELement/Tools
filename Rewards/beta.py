import sys
import random
import time
import pyautogui
import subprocess
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import re

# 定义 Edge 浏览器的路径
edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",  # Edge
    r"C:\Apps\Edge\Edge2\Edge2.lnk",  # Edge2
    r"C:\Apps\Edge\Edge3\Edge3.lnk"   # Edge3
]

class BrowserAutomationApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Browser Automation Settings')
        
        # 创建输入框和标签
        self.repeat_count_label = QtWidgets.QLabel('搜索重复次数:')
        self.repeat_count_input = QtWidgets.QLineEdit(self)

        self.start_ip_label = QtWidgets.QLabel('起始 IP 最后一个段:')
        self.start_ip_input = QtWidgets.QLineEdit(self)

        # 创建按钮
        self.start_button = QtWidgets.QPushButton('开始自动化', self)
        self.start_button.clicked.connect(self.start_automation)

        # 创建作者标签
        self.author_label = QtWidgets.QLabel('作者: 耑木菌', self)
        self.author_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # 布局设置
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.repeat_count_label)
        layout.addWidget(self.repeat_count_input)
        layout.addWidget(self.start_ip_label)
        layout.addWidget(self.start_ip_input)
        layout.addWidget(self.start_button)
        layout.addStretch()  # 添加伸缩空间，使作者标签靠下
        layout.addWidget(self.author_label)

        self.setLayout(layout)

    def start_automation(self):
        # 获取用户输入
        repeat_count = int(self.repeat_count_input.text())
        start_ip_last = self.start_ip_input.text().strip()
        
        # 验证输入是否为有效的整数，并在0到255之间
        if not start_ip_last.isdigit() or not (0 <= int(start_ip_last) <= 255):
            print("起始 IP 最后一个段格式不正确，请输入0到255之间的整数")
            return

        # 定义前三个段
        base_ip_prefix = "192.168.4"

        subnet_mask = "255.255.255.0"

        for i, edge_path in enumerate(edge_paths):
            # 计算当前 IP 的最后一个段
            current_last = int(start_ip_last) + i
            # 确保最后一个段不超过255
            if current_last > 255:
                print("IP 地址最后一个段超过255，停止执行")
                break
            # 组合完整的 IP 地址
            current_ip = f"{base_ip_prefix}.{current_last}"
            self.set_ip("以太网", current_ip, subnet_mask)  # 设置新的 IP 地址
            time.sleep(5)  # 等待 IP 地址切换生效

            for _ in range(repeat_count):
                # 打开浏览器并输入随机数
                if edge_path.endswith('.lnk'):
                    self.open_with_shortcut(edge_path)  # 打开快捷方式
                else:
                    edge_process = subprocess.Popen(edge_path)  # 启动浏览器
                time.sleep(2)  # 等待浏览器打开

                random_number = random.randint(100000, 999999)  # 生成一个六位数的随机数
                time.sleep(1)  # 等待浏览器完全加载

                pyautogui.typewrite(str(random_number))  # 输入随机数
                pyautogui.press('enter')  # 模拟按下 Enter
                time.sleep(2)  # 等待搜索结果加载

                self.kill_browser_with_taskkill("msedge.exe")  # 关闭浏览器进程
                time.sleep(2)  # 等待进程完全关闭

            # 完成所有搜索后再切换 IP 地址
            print(f"完成 {edge_path} 的所有搜索，准备切换到下一个 IP 地址。")

    def set_ip(self, interface, base_ip, subnet_mask):
        gateway = self.get_gateway(interface)
        if gateway:
            try:
                # 禁用 netsh 命令的输出
                subprocess.run(["netsh", "interface", "ip", "set", "address",
                                f"name={interface}", "static", base_ip, subnet_mask, gateway],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"IP 地址已设置为 {base_ip}，网关为 {gateway}")
            except subprocess.CalledProcessError as e:
                print(f"设置 IP 地址失败: {e}")
        else:
            print("无法获取当前网关，无法设置IP地址")

    def get_gateway(self, interface):
        # 捕获输出而不显示
        result = subprocess.run(["netsh", "interface", "ip", "show", "address", interface],
                                capture_output=True, text=True, encoding='utf-8')
        output = result.stdout
        # 查找“默认网关”后的IP地址
        match = re.search(r'默认网关\s*:\s*(\d+\.\d+\.\d+\.\d+)', output)
        if match:
            return match.group(1)
        else:
            return None

    def open_with_shortcut(self, path):
        os.startfile(path)

    def kill_browser_with_taskkill(self, process_name):
        subprocess.call(["taskkill", "/IM", process_name, "/F"])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BrowserAutomationApp()
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec_())