import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from utils.detector import Detector
from utils.constants import DEFAULT_MODEL_PATH
from main_window import MainWindow
from login_window import LoginWindow

from utils.constants import ICON_PATH

# 确保资源目录存在
os.makedirs("resources/images", exist_ok=True)

def main():
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON_PATH))
    
    # 初始化检测器
    detector = Detector(DEFAULT_MODEL_PATH)
    
    # 创建主窗口
    main_window = MainWindow(detector)
    
    # 创建登录窗口，并传入主窗口实例
    login_window = LoginWindow(main_window)
    login_window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 