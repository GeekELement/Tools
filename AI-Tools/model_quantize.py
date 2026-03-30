import subprocess
import sys
from pathlib import Path

# 导入配置文件
from config import (
    FORMAT, QUANTIZE, QUANTIZE_DEVICE as DEVICE, WORKSPACE,
    DATA_PATH, TRAIN_OUTPUT_DIR
)

# YOLO 模型导出脚本
# 所有配置参数请在 config.py 中修改

# ==================== 用户配置区域 ====================

# 模型路径（默认从训练输出目录读取，也可修改为其他路径）
MODEL_PATH = str(Path(TRAIN_OUTPUT_DIR) / "weights" / "best.pt")

# ==================== 自动配置 ====================

# 根据参数自动设置
int8 = QUANTIZE == "int8"
half = QUANTIZE == "fp16"
use_gpu = DEVICE != "cpu"

# 验证配置
if FORMAT == "engine" and not use_gpu:
    print("错误: TensorRT (engine) 格式只能在 GPU 上运行，请设置 QUANTIZE_DEVICE='0'")
    sys.exit(1)

if int8 and half:
    print("错误: 不能同时启用 INT8 和 FP16，请修改 QUANTIZE 参数")
    sys.exit(1)

# 显示配置信息
print(f"导出配置:")
print(f"  格式: {FORMAT}")
print(f"  量化: {QUANTIZE.upper() if int8 or half else '无'}")
print(f"  设备: {'GPU ' + DEVICE if use_gpu else 'CPU'}")
print()

# 构建命令
cmd = [
    "yolo", "export",
    f"model={MODEL_PATH}",
    f"format={FORMAT}",
    f"device={DEVICE}",
    "imgsz=640",
    "batch=1",
    "verbose=True",
]

if int8:
    cmd.append("int8=True")
    cmd.append(f"data={DATA_PATH}")
if half:
    cmd.append("half=True")
if FORMAT == "engine" and WORKSPACE:
    cmd.append(f"workspace={WORKSPACE}")

print(f"执行命令: {' '.join(cmd)}")
print()

result = subprocess.run(cmd, capture_output=False)
sys.exit(result.returncode)
