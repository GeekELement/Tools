import requests
import time

def get_ip_location(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        response.raise_for_status()  # 当HTTP请求返回不成功的状态码时引发HTTPError
        return response.json()
    except requests.RequestException as e:
        print("网络错误:", e)
        return None

def get_current_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException as e:
        print("网络错误:", e)
        return None

def display_location_info(ip_address, location_data):
    if location_data:
        print("IP地址的位置信息:", ip_address)
        fields = ["ip", "hostname", "city", "region", "country", "loc", "org"]
        for field in fields:
            print(f"{field.capitalize()}: {location_data.get(field, 'N/A')}")
    else:
        print("无法获取位置信息。")

if __name__ == "__main__":
    if True:
        ip_address = get_current_ip()
        if ip_address:
            location_data = get_ip_location(ip_address)
            display_location_info(ip_address, location_data)
        else:
            print("无法获取当前IP地址。")
        print("----------------------------------------------------------------")
        time.sleep(1)  # 等待1秒
