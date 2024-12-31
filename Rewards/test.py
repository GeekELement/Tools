import sys
import random
import time
import pyautogui
import subprocess
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt  # 添加这一行

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

        self.gateway_label = QtWidgets.QLabel('默认网关:')
        self.gateway_input = QtWidgets.QLineEdit(self)

        self.start_ip_label = QtWidgets.QLabel('起始 IP:')
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
        layout.addWidget(self.gateway_label)
        layout.addWidget(self.gateway_input)
        layout.addWidget(self.start_ip_label)
        layout.addWidget(self.start_ip_input)
        layout.addWidget(self.start_button)
        layout.addStretch()  # 添加伸缩空间，使作者标签靠下
        layout.addWidget(self.author_label)

        self.setLayout(layout)

    def start_automation(self):
        # 获取用户输入
        repeat_count = int(self.repeat_count_input.text())
        gateway = self.gateway_input.text()
        start_ip = int(self.start_ip_input.text().split('.')[-1])  # 获取最后一个数字

        subnet_mask = "255.255.255.0"

        for i, edge_path in enumerate(edge_paths):
            # 设置新的 IP 地址
            current_ip = f"192.168.4.{start_ip + i}"  # 例如，85, 86, 87...
            self.set_ip("以太网", current_ip, subnet_mask, gateway)  # 设置新的 IP 地址
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

    def set_ip(self, interface, base_ip, subnet_mask, gateway):
        try:
            subprocess.run(["netsh", "interface", "ip", "set", "address",
                            f"name={interface}", "static", base_ip, subnet_mask, gateway],
                           check=True)
            print(f"IP 地址已设置为 {base_ip}")
        except subprocess.CalledProcessError as e:
            print(f"设置 IP 地址失败: {e}")

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
