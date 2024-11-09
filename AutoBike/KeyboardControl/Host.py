import socket
import keyboard
import time

# 主机与从机的网络配置
SERVER_IP = "192.168.2.141"  # 从机IP
SERVER_PORT = 5000

# 帧协议定义
FRAME_HEADER = 0x30
FRAME_FOOTER = 0x40
PULSE_STEP = 50
current_pulse = 1500  # 舵机中值为1500


def calculate_crc(data):
    """计算CRC校验（前三字节异或）"""
    return data[0] ^ data[1] ^ data[2]


def build_frame(pulse_value):
    """构建数据帧，确保脉冲在 500 到 2500 之间"""
    pulse_value = max(500, min(2500, pulse_value))
    data = [
        FRAME_HEADER,
        pulse_value & 0xFF,  # 低字节
        (pulse_value >> 8) & 0xFF,  # 高字节
    ]
    crc = calculate_crc(data)
    frame = data + [crc, FRAME_FOOTER]
    return bytearray(frame)


def send_pulse(sock, pulse_value):
    """发送脉冲数据帧到从机"""
    frame = build_frame(pulse_value)
    sock.sendto(frame, (SERVER_IP, SERVER_PORT))
    print("发送数据帧:", [hex(x) for x in frame], "脉冲值:", pulse_value)


def main():
    global current_pulse
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # 发送舵机初始中值
        send_pulse(sock, current_pulse)

        print("主机端已启动，按 'A' 增加脉冲，'D' 减少脉冲，Ctrl+C 退出。")
        while True:
            # 监听键盘事件
            event = keyboard.read_event()
            if event.event_type == "down":
                if event.name == "a":
                    current_pulse += PULSE_STEP
                    send_pulse(sock, current_pulse)
                    time.sleep(0.1)  # 控制发送速率，避免连发
                elif event.name == "d":
                    current_pulse -= PULSE_STEP
                    send_pulse(sock, current_pulse)
                    time.sleep(0.1)  # 控制发送速率，避免连发


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("程序已退出")
