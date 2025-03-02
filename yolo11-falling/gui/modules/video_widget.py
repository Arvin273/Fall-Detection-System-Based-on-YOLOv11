from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

import cv2
import threading
import time
import os

from utils.constants import DEFAULT_LEFT_IMAGE
from utils.styles import (
    TITLE_STYLE, SUBTITLE_STYLE, BUTTON_STYLE, DANGER_BUTTON_STYLE, 
    CARD_STYLE, RESULT_LABEL_STYLE
)
from utils.utils import cv2_to_qpixmap, save_record_video_frame

class VideoWidget(QWidget):
    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        
        # 视频相关变量
        self.cap = None
        self.is_webcam = True
        self.video_source = 0
        self.is_running = False
        self.frame_count = 0
        self.save_interval = 30  # 每30帧保存一次
        
        # 创建定时器用于更新视频帧
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)  # 减小边距
        main_layout.setSpacing(5)  # 减小间距
        
        # 视频显示和结果区域
        content_layout = QHBoxLayout()
        content_layout.setSpacing(5)  # 减小间距
        
        # 视频显示区域
        video_frame = QFrame()
        video_frame.setStyleSheet(CARD_STYLE)
        video_layout = QVBoxLayout(video_frame)
        video_layout.setContentsMargins(3, 3, 3, 3)  # 减小内边距
        
        video_title = QLabel("实时视频")
        video_title.setStyleSheet(SUBTITLE_STYLE + "QLabel { font-size: 14px; }")
        video_title.setAlignment(Qt.AlignCenter)
        video_title.setMaximumHeight(20)  # 减小高度
        
        self.video_display = QLabel()
        self.video_display.setPixmap(QPixmap(DEFAULT_LEFT_IMAGE).scaled(
            640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation  # 增大视频尺寸
        ))
        self.video_display.setAlignment(Qt.AlignCenter)
        self.video_display.setMinimumSize(640, 480)  # 增大最小尺寸
        
        video_layout.addWidget(video_title)
        video_layout.addWidget(self.video_display)
        
        # 右侧区域
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)  # 减小间距
        
        # 检测结果文本
        result_frame = QFrame()
        result_frame.setStyleSheet(CARD_STYLE)
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(3, 3, 3, 3)  # 减小内边距
        
        result_title = QLabel("检测统计")
        result_title.setStyleSheet(SUBTITLE_STYLE)
        result_title.setAlignment(Qt.AlignCenter)
        result_title.setMaximumHeight(20)  # 减小高度
        
        self.result_label = QLabel("当前检测结果: 等待检测")
        self.result_label.setStyleSheet("QLabel { font-size: 14px; }")
        self.result_label.setAlignment(Qt.AlignCenter)
        
        result_layout.addWidget(result_title)
        result_layout.addWidget(self.result_label)
        
        # 按钮区域
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet(CARD_STYLE)
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(3, 3, 3, 3)  # 减小内边距
        
        # 摄像头检测按钮
        self.webcam_btn = QPushButton("摄像头实时检测")
        self.webcam_btn.setStyleSheet(BUTTON_STYLE)
        self.webcam_btn.setCursor(Qt.PointingHandCursor)
        self.webcam_btn.clicked.connect(self.start_webcam)
        
        # 视频文件检测按钮
        self.video_file_btn = QPushButton("视频文件检测")
        self.video_file_btn.setStyleSheet(BUTTON_STYLE)
        self.video_file_btn.setCursor(Qt.PointingHandCursor)
        self.video_file_btn.clicked.connect(self.open_video_file)
        
        # 停止检测按钮
        self.stop_btn = QPushButton("停止检测")
        self.stop_btn.setStyleSheet(DANGER_BUTTON_STYLE)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.clicked.connect(self.stop_detection)
        self.stop_btn.setEnabled(False)
        
        buttons_layout.addWidget(self.webcam_btn)
        buttons_layout.addWidget(self.video_file_btn)
        buttons_layout.addWidget(self.stop_btn)
        
        right_layout.addWidget(result_frame)
        right_layout.addWidget(buttons_frame)
        
        content_layout.addWidget(video_frame, 8)  # 增加视频区域比例为8
        content_layout.addLayout(right_layout, 2)  # 减小右侧区域比例为2
        
        # 添加组件到主布局
        main_layout.addLayout(content_layout)
        
        # 设置主布局
        self.setLayout(main_layout)
    
    def start_webcam(self):
        """启动摄像头检测"""
        if self.is_running:
            return
        
        try:
            self.is_webcam = True
            self.video_source = 0
            self.cap = cv2.VideoCapture(self.video_source)
            
            if not self.cap.isOpened():
                QMessageBox.warning(self, "错误", "无法打开摄像头")
                return
            
            self.is_running = True
            self.webcam_btn.setEnabled(False)
            self.video_file_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            
            # 启动定时器
            self.timer.start(30)  # 约33fps
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"摄像头启动失败: {str(e)}")
    
    def open_video_file(self):
        """打开视频文件"""
        if self.is_running:
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择视频文件", "", "视频文件 (*.mp4 *.avi *.mov *.mkv)"
        )
        
        if file_path:
            try:
                self.is_webcam = False
                self.video_source = file_path
                self.cap = cv2.VideoCapture(self.video_source)
                
                if not self.cap.isOpened():
                    QMessageBox.warning(self, "错误", "无法打开视频文件")
                    return
                
                self.is_running = True
                self.webcam_btn.setEnabled(False)
                self.video_file_btn.setEnabled(False)
                self.stop_btn.setEnabled(True)
                
                # 启动定时器
                self.timer.start(30)  # 约33fps
                
            except Exception as e:
                QMessageBox.warning(self, "错误", f"视频文件打开失败: {str(e)}")
    
    def update_frame(self):
        """更新视频帧"""
        if not self.is_running or not self.cap:
            return
        
        ret, frame = self.cap.read()
        
        if not ret:
            # 视频结束
            if not self.is_webcam:
                self.stop_detection()
                QMessageBox.information(self, "完成", "视频检测完成")
            return
        
        try:
            # 处理帧
            use_tracking = self.detector.is_tracking if hasattr(self.detector, 'is_tracking') else False
            tracker_type = self.detector.tracker_type if hasattr(self.detector, 'tracker_type') else None
            
            result_frame, result_info = self.detector.process_video_frame(
                frame, use_tracking, tracker_type
            )
            
            if result_frame is not None:
                # 显示处理后的帧
                pixmap = cv2_to_qpixmap(result_frame, 640)  # 增大视频尺寸
                self.video_display.setPixmap(pixmap)
                
                # 更新检测结果
                self.result_label.setText(f"当前检测结果:\n{result_info}")
                
                # 保存记录
                self.frame_count += 1
                if self.frame_count % self.save_interval == 0:
                    save_record_video_frame(result_frame)
            
        except Exception as e:
            print(f"帧处理错误: {str(e)}")
    
    def stop_detection(self):
        """停止检测"""
        self.is_running = False
        self.timer.stop()
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # 重置UI
        self.webcam_btn.setEnabled(True)
        self.video_file_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.video_display.setPixmap(QPixmap(DEFAULT_LEFT_IMAGE).scaled(
            640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation  # 增大视频尺寸
        ))
        self.result_label.setText("当前检测结果: 等待检测")
        self.frame_count = 0
    
    def closeEvent(self, event):
        """关闭窗口时释放资源"""
        self.stop_detection()
        super().closeEvent(event) 