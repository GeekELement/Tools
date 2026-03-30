import subprocess
import sys
from pathlib import Path
from datetime import datetime
import shutil

# 导入配置文件
from config import (
    MODEL, DATA_PATH, EPOCHS, BATCH_SIZE, IMAGE_SIZE, DEVICE,
    OPTIMIZER, LEARNING_RATE, DEGREES, TRANSLATE, SCALE,
    HSV_H, HSV_S, HSV_V, FLIPUD, FLIPLR, MOSAIC, MIXUP,
    PATIENCE, SAVE_PERIOD, WORKERS, SEED, CACHE, PRETRAINED,
    TRAIN_OUTPUT_DIR, EXIST_OK, OUTPUT_ROOT,
    USE_CUSTOM_NAME, CUSTOM_MODEL_NAME
)

# YOLO 模型训练脚本
# 所有配置参数请在 config.py 中修改

# ==================== 自动配置 ====================

# 验证配置
if not Path(DATA_PATH).exists():
    print(f"错误: 数据配置文件不存在: {DATA_PATH}")
    sys.exit(1)

# 解析输出目录
output_path = Path(TRAIN_OUTPUT_DIR)
project = str(output_path.parent)
name = str(output_path.name)

# 构建命令
cmd = [
    "yolo", "train",
    f"model={MODEL}",
    f"data={DATA_PATH}",
    f"epochs={EPOCHS}",
    f"batch={BATCH_SIZE}",
    f"imgsz={IMAGE_SIZE}",
    f"device={DEVICE}",
    f"optimizer={OPTIMIZER}",
    f"lr0={LEARNING_RATE}",
    f"patience={PATIENCE}",
    f"save_period={SAVE_PERIOD}",
    f"workers={WORKERS}",
    f"seed={SEED}",
    f"project={project}",
    f"name={name}",
    f"exist_ok={EXIST_OK}",
]

# 添加布尔参数
if CACHE:
    cmd.append("cache=True")
if PRETRAINED:
    cmd.append("pretrained=True")

# 添加数据增强参数
cmd.extend([
    f"degrees={DEGREES}",
    f"translate={TRANSLATE}",
    f"scale={SCALE}",
    f"hsv_h={HSV_H}",
    f"hsv_s={HSV_S}",
    f"hsv_v={HSV_V}",
    f"flipud={FLIPUD}",
    f"fliplr={FLIPLR}",
    f"mosaic={MOSAIC}",
    f"mixup={MIXUP}",
])

# 显示配置信息
print("=" * 50)
print("训练配置:")
print("=" * 50)
print(f"  模型: {MODEL}")
print(f"  数据集: {DATA_PATH}")
print(f"  轮数: {EPOCHS}")
print(f"  批次大小: {BATCH_SIZE}")
print(f"  图片尺寸: {IMAGE_SIZE}")
print(f"  设备: {'GPU ' + DEVICE if DEVICE != 'cpu' else 'CPU'}")
print(f"  优化器: {OPTIMIZER}")
print(f"  学习率: {LEARNING_RATE}")
print(f"  早停耐心: {PATIENCE}")
print(f"  输出目录: {TRAIN_OUTPUT_DIR}")
print("=" * 50)
print()

# 执行训练
print(f"执行命令: {' '.join(cmd)}")
print()

result = subprocess.run(cmd, capture_output=False)

# 训练完成后，复制最佳模型到 OUTPUT 根目录（可选）
if result.returncode == 0:
    src = Path(TRAIN_OUTPUT_DIR) / "weights" / "best.pt"
    
    if USE_CUSTOM_NAME:
        # 使用自定义名称
        dst = Path(OUTPUT_ROOT) / CUSTOM_MODEL_NAME
    else:
        # 使用自动生成的名称（包含时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"{Path(MODEL).stem}_{timestamp}.pt"
        dst = Path(OUTPUT_ROOT) / model_name
    
    if src.exists():
        shutil.copy2(src, dst)
        print(f"\n模型已复制到: {dst}")

sys.exit(result.returncode)
