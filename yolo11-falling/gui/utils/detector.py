import torch
import cv2
import numpy as np
import time
from ultralytics import YOLO
from collections import defaultdict
from utils.utils import save_record_image, save_record_video_frame, format_detection_results

class Detector:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.load_model(model_path)
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.save_txt = False
        self.save_conf = False
        self.save_crop = False
        self.track_history = defaultdict(lambda: [])
        self.is_tracking = False
        self.tracker_type = None
        
    @torch.no_grad()
    def load_model(self, weights):
        """加载YOLO模型"""
        try:
            model = YOLO(weights)
            return model
        except Exception as e:
            print(f"模型加载失败: {e}")
            return None
    
    def update_model(self, model_path):
        """更新模型"""
        self.model_path = model_path
        self.model = self.load_model(model_path)
        return self.model is not None
    
    def detect_image(self, image_path):
        """检测单张图像"""
        if self.model is None:
            return None, "模型未加载"
        
        try:
            results = self.model(
                image_path, 
                conf=self.conf_thres, 
                iou=self.iou_thres, 
                save_txt=self.save_txt, 
                save_conf=self.save_conf, 
                save_crop=self.save_crop
            )
            
            result = results[0]
            img_array = result.plot()
            
            # 保存记录
            save_record_image(img_array)
            
            # 格式化结果
            result_info = format_detection_results(result)
            
            return img_array, result_info
        except Exception as e:
            print(f"图像检测失败: {e}")
            return None, f"检测失败: {str(e)}"
    
    def process_video_frame(self, frame, use_tracking=False, tracker_type=None):
        """处理视频帧"""
        if self.model is None:
            return None, "模型未加载"
        
        try:
            if use_tracking and tracker_type:
                results = self.model.track(
                    frame, 
                    conf=self.conf_thres, 
                    iou=self.iou_thres, 
                    save_txt=self.save_txt,
                    save_conf=self.save_conf, 
                    save_crop=self.save_crop, 
                    tracker=tracker_type, 
                    persist=True
                )
                
                result = results[0]
                img_array = result.plot()
                
                # 绘制跟踪轨迹
                try:
                    boxes = results[0].boxes.xywh.cpu()
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    
                    for box, track_id in zip(boxes, track_ids):
                        x, y, w, h = box
                        track = self.track_history[track_id]
                        track.append((float(x), float(y)))
                        if len(track) > 30:
                            track.pop(0)
                        
                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(img_array, [points], isClosed=False, color=(0, 0, 230), thickness=3)
                except:
                    pass
            else:
                results = self.model(
                    frame, 
                    conf=self.conf_thres, 
                    iou=self.iou_thres, 
                    save_txt=self.save_txt,
                    save_conf=self.save_conf, 
                    save_crop=self.save_crop
                )
                
                result = results[0]
                img_array = result.plot()
            
            # 格式化结果
            result_info = format_detection_results(result)
            
            return img_array, result_info
        except Exception as e:
            print(f"视频帧处理失败: {e}")
            return None, f"处理失败: {str(e)}"
