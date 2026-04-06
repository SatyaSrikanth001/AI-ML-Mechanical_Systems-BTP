# 齿轮缺陷检测API配置文件

import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 模型配置
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'best_v8n_20ep.pt')  # 模型文件路径
MODEL_INPUT_SIZE = (640, 640)  # 模型输入尺寸

# 上传文件配置
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # 上传文件保存目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # 允许的文件扩展名
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传文件大小（16MB）

# 缺陷类别定义
DEFECT_CLASSES = {
    0: {"name": "点蚀", "english": "pitting", "color": "#ff4757", "description": "表面点状腐蚀或磨损"},
    1: {"name": "剥落", "english": "spalling", "color": "#ff6b35", "description": "表面材料剥落脱落"},
    2: {"name": "压伤", "english": "indentation", "color": "#f0932b", "description": "受压产生的凹陷变形"},
    3: {"name": "擦伤", "english": "scratching", "color": "#6c5ce7", "description": "表面划痕或擦痕"}
}

# API服务配置
API_HOST = '127.0.0.1'  # API服务主机
API_PORT = 5000  # API服务端口
DEBUG_MODE = True  # 是否启用调试模式