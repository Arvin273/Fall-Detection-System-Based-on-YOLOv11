import os
import sys
import subprocess

def check_dependencies():
    """检查必要的依赖是否已安装"""
    try:
        import PySide6
        import cv2
        import numpy
        import torch
        import ultralytics
        return True
    except ImportError:
        return False

def main():
    """主函数"""
    # 检查依赖
    if not check_dependencies():
        print("缺少必要的依赖，正在安装...")
        subprocess.check_call([sys.executable, "install_dependencies.py"])
    
    # 启动系统
    print("启动摔倒检测系统...")
    subprocess.check_call([sys.executable, "main.py"])

if __name__ == "__main__":
    main() 