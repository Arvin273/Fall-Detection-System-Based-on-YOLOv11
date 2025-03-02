# 系统常量定义

# 窗口标题
WINDOW_TITLE = "基于YOLOv11的摔倒检测系统"

# 欢迎语
WELCOME_SENTENCE = "欢迎使用基于YOLOv11的摔倒检测系统"

# 资源路径
ICON_PATH = "resources/images/logo.png"
DEFAULT_LEFT_IMAGE = "resources/images/default_left.jpg"
DEFAULT_RIGHT_IMAGE = "resources/images/default_right.jpg"
DEFAULT_CONFIG_IMAGE = "resources/images/config.png"
DEFAULT_HOME_IMAGE = "resources/images/home.jpg"

# 登录信息
USERNAME = "123"
PASSWORD = "123"

# 记录保存路径
RECORD_PATH = "resources/records"
IMAGE_RECORD_PATH = f"{RECORD_PATH}/images"
VIDEO_RECORD_PATH = f"{RECORD_PATH}/videos"
TMP_PATH = "resources/tmp"

# 默认模型路径
DEFAULT_MODEL_PATH = "../../runs/yolo11/train/weights/best.pt"

# 路径常量
import os
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_PATH = os.path.join(BASE_PATH, "resources")

# 确保资源目录存在
os.makedirs(RESOURCES_PATH, exist_ok=True)
os.makedirs(os.path.join(RESOURCES_PATH, "images"), exist_ok=True)
os.makedirs(os.path.join(RESOURCES_PATH, "weights"), exist_ok=True)

# 记录路径
RECORD_PATH = os.path.join(RESOURCES_PATH, "records")
IMAGE_RECORD_PATH = os.path.join(RECORD_PATH, "images")
VIDEO_RECORD_PATH = os.path.join(RECORD_PATH, "videos")

# 确保记录目录存在
os.makedirs(RECORD_PATH, exist_ok=True)
os.makedirs(IMAGE_RECORD_PATH, exist_ok=True)
os.makedirs(VIDEO_RECORD_PATH, exist_ok=True)

# 临时文件路径
TMP_PATH = os.path.join(RESOURCES_PATH, "tmp")
os.makedirs(TMP_PATH, exist_ok=True)

# 模型路径
WEIGHTS_PATH = os.path.join(RESOURCES_PATH, "weights", "best.pt")