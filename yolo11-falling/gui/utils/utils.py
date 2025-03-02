import os
import shutil
import time
import cv2
from PySide6.QtGui import QPixmap, QImage
import numpy as np
from utils.constants import TMP_PATH, IMAGE_RECORD_PATH, VIDEO_RECORD_PATH

def ensure_dir(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)

# 初始化必要的目录
ensure_dir(TMP_PATH)
ensure_dir(IMAGE_RECORD_PATH)
ensure_dir(VIDEO_RECORD_PATH)

def cv2_to_qpixmap(cv_img, target_size=None):
    """将OpenCV图像转换为QPixmap"""
    # 转换颜色空间从BGR到RGB
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
    # 如果需要调整大小
    if target_size:
        height, width = cv_img.shape[:2]
        # 计算缩放比例
        scale = min(target_size / height, target_size / width)
        # 调整大小
        rgb_image = cv2.resize(rgb_image, (0, 0), fx=scale, fy=scale)
    
    # 创建QImage
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    
    # 转换为QPixmap
    return QPixmap.fromImage(qt_image)

def save_temp_image(image, filename):
    """保存临时图像"""
    ensure_dir(TMP_PATH)
    filepath = os.path.join(TMP_PATH, filename)
    cv2.imwrite(filepath, image)
    return filepath

def save_record_image(image, prefix="img"):
    """保存记录图像"""
    ensure_dir(IMAGE_RECORD_PATH)
    time_str = time.strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{prefix}_{time_str}.jpg"
    filepath = os.path.join(IMAGE_RECORD_PATH, filename)
    cv2.imwrite(filepath, image)
    return filepath

def save_record_video_frame(image, prefix="vid"):
    """保存视频帧记录"""
    ensure_dir(VIDEO_RECORD_PATH)
    time_str = time.strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{prefix}_{time_str}.jpg"
    filepath = os.path.join(VIDEO_RECORD_PATH, filename)
    cv2.imwrite(filepath, image)
    return filepath

def copy_file_to_temp(file_path, new_name=None):
    """复制文件到临时目录"""
    ensure_dir(TMP_PATH)
    if new_name is None:
        _, ext = os.path.splitext(file_path)
        new_name = f"temp_{int(time.time())}{ext}"
    
    dest_path = os.path.join(TMP_PATH, new_name)
    shutil.copy(file_path, dest_path)
    return dest_path

def format_detection_results(result):
    """格式化检测结果为可读文本"""
    result_names = result.names
    result_nums = [0] * len(result_names)
    
    # 获取类别ID列表
    try:
        cls_ids = list(result.boxes.cls.cpu().numpy())
        for cls_id in cls_ids:
            result_nums[int(cls_id)] += 1
    except:
        return "检测失败，未找到目标"
    
    # 格式化结果
    result_info = ""
    for idx_cls, cls_num in enumerate(result_nums):
        if cls_num > 0:
            result_info += f"{result_names[idx_cls]}: {cls_num}\n"
    
    return result_info if result_info else "未检测到目标"

def center_window(window):
    """将窗口居中显示在屏幕上，并向上偏移"""
    from PySide6.QtWidgets import QApplication
    screen_geometry = QApplication.primaryScreen().geometry()
    window_geometry = window.frameGeometry()
    center_point = screen_geometry.center()
    # 向上偏移窗口位置（偏移屏幕高度的15%）
    center_point.setY(center_point.y() - int(screen_geometry.height() * 0.08))
    center_point.setX(center_point.x() - 20)
    window_geometry.moveCenter(center_point)
    window.move(window_geometry.topLeft())