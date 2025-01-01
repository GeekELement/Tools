import asyncio
from aio_ping import ping

async def ping_ip(ip, timeout=0.5):
    try:
        result = await ping(ip, timeout=timeout)
        if result:
            print(f"{ip} is occupied.")
        else:
            print(f"{ip} is not occupied.")
    except Exception as e:
        print(f"Error pinging {ip}: {e}")

async def main(ips):
    tasks = [ping_ip(ip) for ip in ips]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    ip_list = ['8.8.8.8', '192.168.4.1', '10.0.0.1']  # 替换为你要检测的IP列表
    asyncio.run(main(ip_list))