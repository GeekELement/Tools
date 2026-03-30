# YOLO AI 工具集 - 全局配置文件
# 所有脚本共享的配置参数

# ==================== 路径配置 ====================

# 数据集路径
DATA_PATH = "C:\\Files\\Projects\\3D_Print_Error_Detection\\3D-printing-defects-database\\data.yaml"

# 输出目录根目录
OUTPUT_ROOT = "OUTPUT"

# ==================== 模型配置 ====================

# 预训练模型选择
# YOLOv26 系列: "yolov26n.pt", "yolov26s.pt", "yolov26m.pt", "yolov26l.pt", "yolov26x.pt"
# YOLOv8 系列: "yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt"
MODEL = "yolov26n.pt"

# ==================== 训练配置 ====================

# 训练参数
EPOCHS = 200          # 训练轮数
BATCH_SIZE = 16       # 批次大小
IMAGE_SIZE = 640      # 输入图片尺寸
DEVICE = "0"          # 训练设备: "0" (GPU), "cpu", "0,1,2,3" (多GPU)

# 优化器和学习率
OPTIMIZER = "SGD"     # 优化器: "SGD", "Adam", "AdamW"
LEARNING_RATE = 0.01  # 初始学习率

# 数据增强
DEGREES = 0.0         # 随机旋转角度
TRANSLATE = 0.1       # 随机平移
SCALE = 0.5           # 随机缩放
HSV_H = 0.015         # HSV 色调增强
HSV_S = 0.7           # HSV 饱和度增强
HSV_V = 0.4           # HSV 亮度增强
FLIPUD = 0.0          # 上下翻转概率
FLIPLR = 0.5          # 左右翻转概率
MOSAIC = 1.0          # Mosaic 增强概率
MIXUP = 0.0           # Mixup 增强概率

# 早停和保存
PATIENCE = 50         # 早停耐心值（多少轮不提升就停止）
SAVE_PERIOD = 10      # 每多少轮保存一次检查点

# 其他训练选项
WORKERS = 8           # 数据加载线程数
SEED = 0              # 随机种子（0表示随机）
CACHE = True          # 是否缓存数据集到内存
PRETRAINED = True     # 是否使用预训练权重

# 训练输出目录
TRAIN_OUTPUT_DIR = f"{OUTPUT_ROOT}/train"  # 训练输出目录
EXIST_OK = False      # False: 如果目录存在则创建新目录, True: 覆盖

# ==================== 量化导出配置 ====================

# 导出格式: "engine" (TensorRT) 或 "onnx"
FORMAT = "onnx"

# 量化类型: "int8", "fp16", 或 "fp32" (不量化)
QUANTIZE = "fp16"

# 量化设备
QUANTIZE_DEVICE = "0"  # "0" (GPU), "cpu"

# TensorRT 工作空间 (GB)，仅 TensorRT 有效
WORKSPACE = 4

# ==================== 自定义模型名称 ====================

# 是否启用自定义输出模型名称
USE_CUSTOM_NAME = False

# 自定义模型名称（仅在 USE_CUSTOM_NAME = True 时有效）
CUSTOM_MODEL_NAME = "my_model.pt"
