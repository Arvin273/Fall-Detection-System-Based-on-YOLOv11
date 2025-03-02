import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFormLayout, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QFont, QIcon

from utils.constants import USERNAME, PASSWORD, ICON_PATH, WELCOME_SENTENCE, WINDOW_TITLE
from utils.styles import LOGIN_WINDOW_STYLE, BUTTON_STYLE, TITLE_STYLE, INPUT_STYLE, CARD_STYLE
from main_window import MainWindow
from utils.utils import center_window

class LoginWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle(f"{WINDOW_TITLE} - 登录")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(400, 300)
        self.setStyleSheet(LOGIN_WINDOW_STYLE)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 创建一个垂直布局用于居中内容
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        
        # 标题
        title_label = QLabel("摔倒检测系统登录")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(TITLE_STYLE)
        
        # 登录表单
        login_frame = QFrame()
        login_frame.setStyleSheet(CARD_STYLE)
        login_layout = QVBoxLayout(login_frame)
        login_layout.setContentsMargins(20, 20, 20, 20)
        
        # 自定义标签样式 - 移除边框
        label_style = "QLabel { font-size: 14px; color: #2c3e50; background: transparent; border: none; }"
        
        # 用户名输入
        username_layout = QHBoxLayout()
        username_label = QLabel("用户名:")
        username_label.setStyleSheet(label_style)
        username_label.setFixedWidth(60)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setStyleSheet(INPUT_STYLE)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # 密码输入
        password_layout = QHBoxLayout()
        password_label = QLabel("密码:")
        password_label.setStyleSheet(label_style)
        password_label.setFixedWidth(60)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(INPUT_STYLE)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # 登录按钮
        login_btn = QPushButton("登录")
        login_btn.setStyleSheet(BUTTON_STYLE)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.login)
        
        # 添加组件到登录布局
        login_layout.addLayout(username_layout)
        login_layout.addLayout(password_layout)
        # 添加间隔
        login_layout.addSpacing(15)
        login_layout.addWidget(login_btn)
        
        # 添加组件到居中布局
        center_layout.addWidget(title_label)
        center_layout.addWidget(login_frame)
        
        # 添加居中布局到主布局
        main_layout.addStretch(1)
        main_layout.addLayout(center_layout)
        main_layout.addStretch(1)
        
        # 将窗口居中显示
        center_window(self)
        
    def login(self):
        """登录验证"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        # 简单的验证逻辑，实际应用中应该使用更安全的方式
        if username == "admin" and password == "admin":
            self.hide()
            self.main_window.show()
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误！") 

    def closeEvent(self, event):
        """关闭窗口时退出程序"""
        # 确保程序完全退出
        import sys
        sys.exit(0)