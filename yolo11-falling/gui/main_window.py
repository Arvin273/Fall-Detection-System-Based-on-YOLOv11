from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QMessageBox, QStatusBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QCloseEvent

from utils.constants import WINDOW_TITLE, ICON_PATH
from utils.styles import MAIN_WINDOW_STYLE, TAB_STYLE, STATUSBAR_STYLE
from utils.utils import center_window

from modules.home_widget import HomeWidget
from modules.image_widget import ImageWidget
from modules.video_widget import VideoWidget
from modules.config_widget import ConfigWidget

class MainWindow(QMainWindow):
    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        self.init_ui()
        
    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))  # 使用logo.png作为图标
        self.resize(900, 650)
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(TAB_STYLE)
        
        # 添加各个功能页面
        self.home_widget = HomeWidget(self.detector)
        self.image_widget = ImageWidget(self.detector)
        self.video_widget = VideoWidget(self.detector)
        self.config_widget = ConfigWidget(self.detector)
        
        self.tab_widget.addTab(self.home_widget, "主页")
        self.tab_widget.addTab(self.image_widget, "图片检测")
        self.tab_widget.addTab(self.video_widget, "视频检测")
        self.tab_widget.addTab(self.config_widget, "配置信息")
        
        # 设置标签页图标
        self.tab_widget.setTabIcon(0, QIcon(ICON_PATH))
        self.tab_widget.setTabIcon(1, QIcon(ICON_PATH))
        self.tab_widget.setTabIcon(2, QIcon(ICON_PATH))
        self.tab_widget.setTabIcon(3, QIcon(ICON_PATH))
        
        # 设置中央部件
        self.setCentralWidget(self.tab_widget)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(STATUSBAR_STYLE)
        self.status_bar.showMessage("系统就绪")
        self.setStatusBar(self.status_bar)
        
        # 将窗口居中显示
        center_window(self)
    
    def closeEvent(self, event: QCloseEvent):
        """关闭窗口时的确认"""
        reply = QMessageBox.question(
            self, "确认退出", "确定要退出系统吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 停止视频检测
            if hasattr(self.video_widget, 'stop_detection'):
                self.video_widget.stop_detection()
            event.accept()
        else:
            event.ignore() 