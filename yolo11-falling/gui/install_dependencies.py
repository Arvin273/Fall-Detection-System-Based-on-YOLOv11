import subprocess
import sys

def install_dependencies():
    """安装必要的依赖"""
    dependencies = [
        "pyside6",
        "opencv-python",
        "numpy",
        "torch",
        "torchvision",
        "ultralytics",
        "pyyaml"
    ]
    
    print("正在安装必要的依赖...")
    for dep in dependencies:
        print(f"安装 {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    
    print("依赖安装完成！")

if __name__ == "__main__":
    install_dependencies()
