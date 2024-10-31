import subprocess
import sys

# 确保安装 Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.common.by import By
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.common.by import By

import time

# 设置 Edge WebDriver 的路径
edge_driver_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe'  # 替换为你自己的路径

# 创建 Edge 浏览器的服务对象
service = Service(edge_driver_path)
service.start()

# 创建 Edge 浏览器实例
driver = webdriver.Edge(service=service)

# 打开 Bing 搜索页面
driver.get("https://www.bing.com")

# 找到搜索框并输入“你好”
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("你好")

# 提交搜索
search_box.submit()

# 等待几秒钟以查看结果
time.sleep(5)

# 关闭浏览器
driver.quit()
