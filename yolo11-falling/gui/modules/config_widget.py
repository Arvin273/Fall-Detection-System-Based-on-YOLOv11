from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFormLayout, QMessageBox, QFrame, QCheckBox,
    QComboBox, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QDoubleValidator, QIntValidator

from utils.constants import DEFAULT_CONFIG_IMAGE
from utils.styles import (
    TITLE_STYLE, SUBTITLE_STYLE, BUTTON_STYLE, CARD_STYLE,
    INPUT_STYLE, CHECKBOX_STYLE, COMBOBOX_STYLE, SUCCESS_BUTTON_STYLE, SWITCH_STYLE
)

class ConfigWidget(QWidget):
    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)  # 减小边距
        main_layout.setSpacing(5)  # 减小间距
        
        # 配置表单
        config_frame = QFrame()
        config_frame.setStyleSheet(CARD_STYLE)
        config_layout = QFormLayout(config_frame)  # 使用表单布局
        config_layout.setContentsMargins(15, 15, 15, 15)
        config_layout.setSpacing(15)
        config_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)  # 允许字段扩展
        config_layout.setLabelAlignment(Qt.AlignLeft)  # 标签左对齐
        
        # 自定义标签样式 - 移除边框
        label_style = "QLabel { font-size: 14px; color: #2c3e50; background: transparent; border: none; }"
        
        # 显示大小配置
        output_size_label = QLabel("系统图像显示大小:")
        output_size_label.setStyleSheet(label_style)
        self.output_size_input = QLineEdit(str(480))
        self.output_size_input.setStyleSheet(INPUT_STYLE)
        self.output_size_input.setValidator(QIntValidator(100, 1000))
        config_layout.addRow(output_size_label, self.output_size_input)
        
        # 摄像头源配置
        vid_source_label = QLabel("摄像头源地址:")
        vid_source_label.setStyleSheet(label_style)
        self.vid_source_input = QLineEdit("0")
        self.vid_source_input.setStyleSheet(INPUT_STYLE)
        config_layout.addRow(vid_source_label, self.vid_source_input)
        
        # 视频帧保存间隔
        vid_gap_label = QLabel("视频帧保存间隔:")
        vid_gap_label.setStyleSheet(label_style)
        self.vid_gap_input = QLineEdit("30")
        self.vid_gap_input.setStyleSheet(INPUT_STYLE)
        self.vid_gap_input.setValidator(QIntValidator(1, 100))
        config_layout.addRow(vid_gap_label, self.vid_gap_input)
        
        # 置信度阈值
        conf_thres_label = QLabel("检测模型置信度阈值:")
        conf_thres_label.setStyleSheet(label_style)
        self.conf_thres_input = QLineEdit(str(self.detector.conf_thres))
        self.conf_thres_input.setStyleSheet(INPUT_STYLE)
        self.conf_thres_input.setValidator(QDoubleValidator(0.01, 1.0, 2))
        config_layout.addRow(conf_thres_label, self.conf_thres_input)
        
        # IOU阈值
        iou_thres_label = QLabel("检测模型IOU阈值:")
        iou_thres_label.setStyleSheet(label_style)
        self.iou_thres_input = QLineEdit(str(self.detector.iou_thres))
        self.iou_thres_input.setStyleSheet(INPUT_STYLE)
        self.iou_thres_input.setValidator(QDoubleValidator(0.01, 1.0, 2))
        config_layout.addRow(iou_thres_label, self.iou_thres_input)
        
        # 保存txt选项
        save_txt_label = QLabel("推理时是否保存txt文件:")
        save_txt_label.setStyleSheet(label_style)
        self.save_txt_checkbox = QCheckBox()
        self.save_txt_checkbox.setChecked(self.detector.save_txt)
        self.save_txt_checkbox.setStyleSheet(SWITCH_STYLE)
        config_layout.addRow(save_txt_label, self.save_txt_checkbox)
        
        # 保存置信度选项
        save_conf_label = QLabel("推理时是否保存置信度:")
        save_conf_label.setStyleSheet(label_style)
        self.save_conf_checkbox = QCheckBox()
        self.save_conf_checkbox.setChecked(self.detector.save_conf)
        self.save_conf_checkbox.setStyleSheet(SWITCH_STYLE)
        config_layout.addRow(save_conf_label, self.save_conf_checkbox)
        
        # 保存切片文件选项
        save_crop_label = QLabel("推理时是否保存切片文件:")
        save_crop_label.setStyleSheet(label_style)
        self.save_crop_checkbox = QCheckBox()
        self.save_crop_checkbox.setChecked(self.detector.save_crop)
        self.save_crop_checkbox.setStyleSheet(SWITCH_STYLE)
        config_layout.addRow(save_crop_label, self.save_crop_checkbox)
        
        # 追踪配置
        track_label = QLabel("追踪配置:")
        track_label.setStyleSheet(label_style)
        self.track_combobox = QComboBox()
        self.track_combobox.addItems(["不开启追踪", "bytetrack", "botsort"])
        self.track_combobox.setCurrentText("不开启追踪" if not self.detector.is_tracking else self.detector.tracker_type)
        self.track_combobox.setStyleSheet(COMBOBOX_STYLE)
        config_layout.addRow(track_label, self.track_combobox)
        
        # 保存按钮
        save_btn = QPushButton("保存配置信息")
        save_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_config)
        
        # 添加组件到主布局
        main_layout.addWidget(config_frame)
        main_layout.addWidget(save_btn)
        
        # 设置主布局
        self.setLayout(main_layout)
    
    def save_config(self):
        """保存配置信息"""
        try:
            # 更新检测器配置
            self.detector.conf_thres = float(self.conf_thres_input.text())
            self.detector.iou_thres = float(self.iou_thres_input.text())
            self.detector.save_txt = self.save_txt_checkbox.isChecked()
            self.detector.save_conf = self.save_conf_checkbox.isChecked()
            self.detector.save_crop = self.save_crop_checkbox.isChecked()
            
            # 更新追踪配置
            track_option = self.track_combobox.currentText()
            self.detector.is_tracking = track_option != "不开启追踪"
            self.detector.tracker_type = track_option if self.detector.is_tracking else None
            
            # 更新其他配置
            output_size = int(self.output_size_input.text())
            vid_source = self.vid_source_input.text()
            vid_gap = int(self.vid_gap_input.text())
            
            # 这些配置需要传递给视频检测模块
            # 可以通过信号槽机制或者直接引用实现
            
            QMessageBox.information(self, "成功", "配置保存成功")
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"配置保存失败: {str(e)}") 