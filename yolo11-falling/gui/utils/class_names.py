import yaml
import os

def get_class_names():
    """从data.yaml文件中获取类别名称"""
    try:
        # 尝试从训练目录加载类别名称
        yaml_path = "../../data.yaml"
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                if 'names' in data:
                    return data['names']
        
        # 如果找不到，使用默认类别名称
        return ['person', 'fall']
    except Exception as e:
        print(f"加载类别名称失败: {e}")
        return ['person', 'fall']
