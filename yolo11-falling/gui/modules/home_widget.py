from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont, QIcon

from utils.constants import WELCOME_SENTENCE, DEFAULT_HOME_IMAGE, RECORD_PATH, IMAGE_RECORD_PATH, VIDEO_RECORD_PATH
from utils.styles import (
    TITLE_STYLE, SUBTITLE_STYLE, BUTTON_STYLE, CARD_STYLE
)
import os

class HomeWidget(QWidget):
    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 30, 20, 20)  # 增大边距，特别是顶部
        main_layout.setSpacing(20)  # 增大间距
        
        # 欢迎标题
        welcome_label = QLabel(WELCOME_SENTENCE)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet(TITLE_STYLE + "QLabel { font-size: 24px; }")  # 增大字体
        
        # 当前模型信息
        model_frame = QFrame()
        model_frame.setStyleSheet(CARD_STYLE)
        model_layout = QVBoxLayout(model_frame)
        model_layout.setContentsMargins(20, 20, 20, 20)  # 增大内边距
        
        model_title = QLabel("模型信息")
        model_title.setStyleSheet(SUBTITLE_STYLE + "QLabel { font-size: 18px; }")  # 增大字体
        model_title.setAlignment(Qt.AlignCenter)
        
        self.model_path_label = QLabel(f"当前模型: {self.detector.model_path}")
        self.model_path_label.setWordWrap(True)
        self.model_path_label.setAlignment(Qt.AlignCenter)
        self.model_path_label.setStyleSheet("QLabel { font-size: 16px; padding: 10px; }")  # 增大字体
        
        model_layout.addWidget(model_title)
        model_layout.addWidget(self.model_path_label)
        
        # 按钮区域
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)  # 设置按钮居中
        buttons_layout.setSpacing(30)  # 增大按钮间距
        
        # 切换模型按钮
        change_model_btn = QPushButton("切换模型")
        change_model_btn.setStyleSheet(BUTTON_STYLE + "QPushButton { font-size: 16px; padding: 12px 20px; }")  # 增大按钮
        change_model_btn.setCursor(Qt.PointingHandCursor)
        change_model_btn.clicked.connect(self.change_model)
        change_model_btn.setFixedWidth(180)  # 增大按钮宽度
        
        # 查看历史记录按钮
        view_history_btn = QPushButton("查看历史记录")
        view_history_btn.setStyleSheet(BUTTON_STYLE + "QPushButton { font-size: 16px; padding: 12px 20px; }")  # 增大按钮
        view_history_btn.setCursor(Qt.PointingHandCursor)
        view_history_btn.clicked.connect(self.view_history)
        view_history_btn.setFixedWidth(180)  # 增大按钮宽度
        
        buttons_layout.addWidget(change_model_btn)
        buttons_layout.addWidget(view_history_btn)
        
        # 添加组件到主布局，向上移动内容
        main_layout.addWidget(welcome_label)
        main_layout.addSpacing(30)  # 标题和模型信息之间增加间距
        main_layout.addWidget(model_frame)
        main_layout.addSpacing(30)  # 模型信息和按钮之间增加间距
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch(1)  # 底部添加弹性空间，使内容向上移动
        
        # 设置主布局
        self.setLayout(main_layout)
    
    def change_model(self):
        """切换模型"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择模型文件", "", "模型文件 (*.pt)"
        )
        
        if file_path:
            if self.detector.update_model(file_path):
                self.model_path_label.setText(f"当前模型: {file_path}")
                QMessageBox.information(self, "成功", "模型切换成功！")
            else:
                QMessageBox.warning(self, "错误", "模型加载失败！")
    
    def view_history(self):
        """查看历史记录"""
        try:
            if os.path.exists(RECORD_PATH):
                os.startfile(RECORD_PATH)
            else:
                # 如果目录不存在，尝试创建它
                os.makedirs(RECORD_PATH, exist_ok=True)
                os.makedirs(IMAGE_RECORD_PATH, exist_ok=True)
                os.makedirs(VIDEO_RECORD_PATH, exist_ok=True)
                
                # 再次尝试打开
                os.startfile(RECORD_PATH)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法打开历史记录目录: {str(e)}") 