from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from utils.constants import DEFAULT_LEFT_IMAGE, DEFAULT_RIGHT_IMAGE
from utils.styles import (
    TITLE_STYLE, SUBTITLE_STYLE, BUTTON_STYLE, SUCCESS_BUTTON_STYLE, 
    CARD_STYLE, RESULT_LABEL_STYLE
)
from utils.utils import cv2_to_qpixmap, copy_file_to_temp

class ImageWidget(QWidget):
    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        self.image_path = None
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)  # 减小边距
        main_layout.setSpacing(5)  # 减小间距
        
        # 图像显示区域
        images_layout = QHBoxLayout()
        images_layout.setSpacing(5)  # 减小间距
        
        # 左侧原始图像
        left_frame = QFrame()
        left_frame.setStyleSheet(CARD_STYLE)
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(3, 3, 3, 3)  # 减小内边距
        
        left_title = QLabel("原始图像")
        left_title.setStyleSheet(SUBTITLE_STYLE + "QLabel { font-size: 14px; }")
        left_title.setAlignment(Qt.AlignCenter)
        left_title.setMaximumHeight(20)  # 减小高度
        
        self.left_image = QLabel()
        self.left_image.setPixmap(QPixmap(DEFAULT_LEFT_IMAGE).scaled(
            500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation  # 增大图像尺寸
        ))
        self.left_image.setAlignment(Qt.AlignCenter)
        
        left_layout.addWidget(left_title)
        left_layout.addWidget(self.left_image)
        
        # 右侧检测结果图像
        right_frame = QFrame()
        right_frame.setStyleSheet(CARD_STYLE)
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(3, 3, 3, 3)  # 减小内边距
        
        right_title = QLabel("检测结果")
        right_title.setStyleSheet(SUBTITLE_STYLE + "QLabel { font-size: 14px; }")
        right_title.setAlignment(Qt.AlignCenter)
        right_title.setMaximumHeight(20)  # 减小高度
        
        self.right_image = QLabel()
        self.right_image.setPixmap(QPixmap(DEFAULT_RIGHT_IMAGE).scaled(
            500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation  # 增大图像尺寸
        ))
        self.right_image.setAlignment(Qt.AlignCenter)
        
        right_layout.addWidget(right_title)
        right_layout.addWidget(self.right_image)
        
        images_layout.addWidget(left_frame, 5)  # 设置比例为5
        images_layout.addWidget(right_frame, 5)  # 设置比例为5
        
        # 检测结果文本和按钮区域
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(5)  # 减小间距
        
        # 检测结果文本
        result_frame = QFrame()
        result_frame.setStyleSheet(CARD_STYLE)
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(3, 3, 3, 3)  # 减小内边距
        
        result_title = QLabel("检测统计")
        result_title.setStyleSheet(SUBTITLE_STYLE)
        result_title.setAlignment(Qt.AlignCenter)
        result_title.setMaximumHeight(20)  # 减小高度
        
        self.result_label = QLabel("当前检测结果: 待检测")
        self.result_label.setStyleSheet("QLabel { font-size: 14px; }")
        self.result_label.setAlignment(Qt.AlignCenter)
        
        result_layout.addWidget(result_title)
        result_layout.addWidget(self.result_label)
        
        # 按钮区域
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet(CARD_STYLE)
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(3, 3, 3, 3)  # 减小内边距
        
        # 上传图片按钮
        upload_btn = QPushButton("上传图片")
        upload_btn.setStyleSheet(BUTTON_STYLE)
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.clicked.connect(self.upload_image)
        
        # 开始检测按钮
        detect_btn = QPushButton("开始检测")
        detect_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        detect_btn.setCursor(Qt.PointingHandCursor)
        detect_btn.clicked.connect(self.detect_image)
        
        buttons_layout.addWidget(upload_btn)
        buttons_layout.addWidget(detect_btn)
        
        bottom_layout.addWidget(result_frame, 3)  # 设置比例为3
        bottom_layout.addWidget(buttons_frame, 2)  # 设置比例为2
        
        # 添加组件到主布局
        main_layout.addLayout(images_layout, 8)  # 增加图像区域比例为8
        main_layout.addLayout(bottom_layout, 2)  # 减小底部区域比例为2
        
        # 设置主布局
        self.setLayout(main_layout)
    
    def upload_image(self):
        """上传图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.jpg *.jpeg *.png *.bmp)"
        )
        
        if file_path:
            try:
                # 复制图片到临时目录
                self.image_path = copy_file_to_temp(file_path, "input_image.jpg")
                
                # 显示原始图片，但不改变标题样式
                self.left_image.setPixmap(QPixmap(self.image_path).scaled(
                    500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation  # 增大图像尺寸
                ))
                
                # 重置右侧图像和结果
                self.right_image.setPixmap(QPixmap(DEFAULT_RIGHT_IMAGE).scaled(
                    500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation  # 增大图像尺寸
                ))
                self.result_label.setText("当前检测结果: 待检测")
                
            except Exception as e:
                QMessageBox.warning(self, "错误", f"图片加载失败: {str(e)}")
    
    def detect_image(self):
        """检测图片"""
        if not self.image_path:
            QMessageBox.warning(self, "警告", "请先上传图片")
            return
        
        try:
            # 执行检测
            result_image, result_info = self.detector.detect_image(self.image_path)
            
            if result_image is not None:
                # 显示检测结果图像
                pixmap = cv2_to_qpixmap(result_image, 500)  # 增大图像尺寸
                self.right_image.setPixmap(pixmap)
                
                # 显示检测结果文本
                self.result_label.setText(f"当前检测结果:\n{result_info}")
                
                QMessageBox.information(self, "成功", "图片检测完成")
            else:
                QMessageBox.warning(self, "错误", result_info)
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"检测失败: {str(e)}") 