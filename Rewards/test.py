import subprocess

def ping_ip(ip):
    try:
        result = subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        if result.returncode == 0:
            print(f"{ip} is occupied.")
        else:
            print(f"{ip} is not occupied.")
    except subprocess.TimeoutExpired:
        print(f"Ping to {ip} timed out.")

if __name__ == "__main__":
    ip_list = ['192.168.4.84', '192.168.4.1', '10.0.0.1']
    for ip in ip_list:
        ping_ip(ip)