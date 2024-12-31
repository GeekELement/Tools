import subprocess

def set_ip(interface, ip_address, subnet_mask, gateway):
    try:
        # 设置 IP 地址
        subprocess.run(["netsh", "interface", "ip", "set", "address", 
                        f"name={interface}", "static", ip_address, subnet_mask, gateway],
                       check=True)
        print(f"IP 地址已设置为 {ip_address}")
    except subprocess.CalledProcessError as e:
        print(f"设置 IP 地址失败: {e}")

# 示例使用
set_ip("以太网", "192.168.4.85", "255.255.255.0", "192.168.4.1")
