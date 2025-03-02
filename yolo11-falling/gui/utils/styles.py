# 样式定义

# 主题颜色
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#2980b9"
SUCCESS_COLOR = "#2ecc71"
WARNING_COLOR = "#f39c12"
DANGER_COLOR = "#e74c3c"
LIGHT_COLOR = "#ecf0f1"
DARK_COLOR = "#2c3e50"
BACKGROUND_COLOR = "#f5f5f5"

# 按钮样式
BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 13px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {SECONDARY_COLOR};
    }}
    QPushButton:pressed {{
        background-color: {DARK_COLOR};
    }}
    QPushButton:disabled {{
        background-color: #cccccc;
        color: #666666;
    }}
"""

SUCCESS_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {SUCCESS_COLOR};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 15px;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #27ae60;
    }}
    QPushButton:pressed {{
        background-color: #1e8449;
    }}
"""

DANGER_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {DANGER_COLOR};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 15px;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #c0392b;
    }}
    QPushButton:pressed {{
        background-color: #a93226;
    }}
"""

# 标签样式
TITLE_STYLE = f"""
    QLabel {{
        color: {DARK_COLOR};
        font-size: 18px;
        font-weight: bold;
        padding: 2px;
        margin: 0;
        max-height: 30px;
    }}
"""

SUBTITLE_STYLE = f"""
    QLabel {{
        color: {DARK_COLOR};
        font-size: 14px;
        font-weight: bold;
        padding: 2px;
        margin: 0;
        max-height: 25px;
    }}
"""

# 输入框样式
INPUT_STYLE = f"""
    QLineEdit {{
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        padding: 8px;
        background-color: white;
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border: 1px solid {PRIMARY_COLOR};
    }}
"""

# 复选框样式 - 不使用图像的简洁样式
CHECKBOX_STYLE = f"""
    QCheckBox {{
        spacing: 8px;
        font-size: 14px;
    }}
    
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        background-color: white;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {PRIMARY_COLOR};
        border: 1px solid {PRIMARY_COLOR};
    }}
    
    QCheckBox::indicator:unchecked:hover {{
        border: 1px solid {PRIMARY_COLOR};
    }}
"""

# 开关样式 - 与复选框样式相同，但使用不同名称
SWITCH_STYLE = CHECKBOX_STYLE

# 下拉框样式
COMBOBOX_STYLE = f"""
    QComboBox {{
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        padding: 8px;
        background-color: white;
        font-size: 14px;
        min-width: 150px;
    }}
    QComboBox:hover {{
        border: 1px solid {PRIMARY_COLOR};
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #bdc3c7;
    }}
"""

# 标签页样式
TAB_STYLE = f"""
    QTabWidget::pane {{
        border: 1px solid #bdc3c7;
        background-color: white;
        border-radius: 4px;
    }}
    QTabBar::tab {{
        background-color: {LIGHT_COLOR};
        color: {DARK_COLOR};
        border: 1px solid #bdc3c7;
        border-bottom: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        padding: 8px 12px;
        margin-right: 2px;
        font-size: 14px;
    }}
    QTabBar::tab:selected {{
        background-color: white;
        border-bottom: 2px solid {PRIMARY_COLOR};
    }}
    QTabBar::tab:hover {{
        background-color: white;
    }}
"""

# 主窗口样式
MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {BACKGROUND_COLOR};
    }}
    QWidget {{
        background-color: {BACKGROUND_COLOR};
    }}
"""

# 卡片样式
CARD_STYLE = f"""
    QFrame {{
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }}
"""

# 状态栏样式
STATUSBAR_STYLE = f"""
    QStatusBar {{
        background-color: {LIGHT_COLOR};
        color: {DARK_COLOR};
        font-size: 12px;
    }}
"""

# 登录窗口样式
LOGIN_WINDOW_STYLE = f"""
    QWidget {{
        background-color: white;
    }}
    QLabel {{
        font-size: 14px;
        color: {DARK_COLOR};
    }}
    QLineEdit {{
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        padding: 10px;
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border: 1px solid {PRIMARY_COLOR};
    }}
"""

# 结果显示框样式
RESULT_LABEL_STYLE = f"""
    QLabel {{
        font-size: 14px;
        padding: 5px;
    }}
"""
