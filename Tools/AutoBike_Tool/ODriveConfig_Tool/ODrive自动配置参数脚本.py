import pyautogui
import time
import keyboard  # 需要安装 keyboard 模块: pip install keyboard

# 等待几秒让你有时间切换到终端窗口
time.sleep(5)

# 配置参数命令列表
commands = [
    "odrv0.erase_configuration()",
    "odrv0.config.brake_resistance = 0.47",
    "odrv0.config.dc_bus_overvoltage_trip_level = 56",
    "odrv0.config.dc_max_positive_current = 120",
    "odrv0.config.dc_max_negative_current = -30",
    "odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT",
    "odrv0.axis0.motor.config.pole_pairs = 14",
    "odrv0.axis0.motor.config.calibration_current = 10",
    "odrv0.axis0.motor.config.current_lim = 120",
    "odrv0.axis0.motor.config.current_lim_margin = 8",
    "odrv0.axis0.encoder.config.mode = ENCODER_MODE_INCREMENTAL",
    "odrv0.axis0.encoder.config.cpr = 8192",
    "odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL",
    "odrv0.axis0.controller.config.vel_limit = 50",
    "odrv0.axis0.controller.config.vel_limit_tolerance = 2",
    "odrv0.axis0.controller.config.vel_gain = 0.45",  # kp
    "odrv0.axis0.controller.config.vel_integrator_gain = 0.2",  # ki
    "odrv0.axis0.controller.config.input_mode = INPUT_MODE_VEL_RAMP",
    "odrv0.axis0.controller.config.vel_ramp_rate = 50",
    "odrv0.axis1.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT",
    "odrv0.axis1.motor.config.pole_pairs = 14",
    "odrv0.axis1.motor.config.calibration_current = 10",
    "odrv0.axis1.motor.config.current_lim = 120",
    "odrv0.axis1.motor.config.current_lim_margin = 8",
    "odrv0.axis1.encoder.config.mode = ENCODER_MODE_INCREMENTAL",
    "odrv0.axis1.encoder.config.cpr = 8192",
    "odrv0.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL",
    "odrv0.axis1.controller.config.vel_limit = 50",
    "odrv0.axis1.controller.config.vel_limit_tolerance = 2",
    "odrv0.axis1.controller.config.vel_gain = 0.45",  # kp
    "odrv0.axis1.controller.config.vel_integrator_gain = 0.2",  # ki
    "odrv0.axis1.controller.config.input_mode = INPUT_MODE_VEL_RAMP",
    "odrv0.axis1.controller.config.vel_ramp_rate = 50",
    "odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE",
    "odrv0.axis0.error",
    "odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL",
    "odrv0.axis0.motor.config.pre_calibrated = True",
    "odrv0.axis0.config.startup_encoder_offset_calibration = True",
    "odrv0.axis0.config.startup_closed_loop_control = True",
    "odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE",
    "odrv0.axis1.error",
    "odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL",
    "odrv0.axis1.motor.config.pre_calibrated = True",
    "odrv0.axis1.config.startup_encoder_offset_calibration = True",
    "odrv0.axis1.config.startup_closed_loop_control = True",
    "odrv0.config.enable_uart = True",
    "odrv0.config.uart_baudrate = 460800",
    "odrv0.axis0.requested_state = AXIS_STATE_IDLE",
    "odrv0.axis1.requested_state = AXIS_STATE_IDLE",
    "odrv0.save_configuration()",
    "odrv0.reboot()"
]

# 逐行输入命令并执行
try:
    for command in commands:
        if keyboard.is_pressed('q'):  # 检查是否按下 'q' 键
            print("脚本被用户终止")
            break
        pyautogui.write(command)  # 输入命令
        pyautogui.press('enter')  # 模拟回车
        time.sleep(0.5)  # 每次输入后稍等一下，防止过快
except KeyboardInterrupt:
    print("脚本已中断")
