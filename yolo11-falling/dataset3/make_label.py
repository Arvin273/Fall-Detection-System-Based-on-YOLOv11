import json
import os

# 定义类别到索引的映射
class_to_id = {"standing": 1,
               "falling": 0}  # 根据实际情况修改

def convert_to_yolo_format(json_data):
    """
    将 JSON 数据转换为 YOLOv8 标注格式
    """
    yolo_annotations = []
    image_width = json_data["imageWidth"]
    image_height = json_data["imageHeight"]

    for shape in json_data["shapes"]:
        label = shape["label"]
        points = shape["points"]
        class_id = class_to_id.get(label, -1)  # 获取类别索引，如果未定义则返回 -1

        if class_id == -1:
            print(f"Warning: 类别 '{label}' 未定义，跳过该标注。")
            continue

        # 提取边界框的左上角和右下角坐标
        x_min, y_min = points[0]
        x_max, y_max = points[1]

        # 计算中心坐标、宽度和高度
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min

        # 归一化
        x_center /= image_width
        y_center /= image_height
        width /= image_width
        height /= image_height

        # 添加到 YOLO 格式标注
        yolo_annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")

    return yolo_annotations

def save_yolo_annotation(yolo_annotations, output_path):
    """
    将 YOLOv8 标注保存到 .txt 文件
    """
    with open(output_path, "w") as f:
        for annotation in yolo_annotations:
            f.write(annotation + "\n")

def process_json_file(json_file_path, output_dir):
    """
    处理单个 JSON 文件并生成 YOLOv8 标注文件
    """
    # 读取 JSON 文件
    with open(json_file_path, "r") as f:
        json_data = json.load(f)

    # 转换为 YOLOv8 格式
    yolo_annotations = convert_to_yolo_format(json_data)

    # 生成输出文件路径
    image_name = os.path.splitext(os.path.basename(json_data["imagePath"]))[0]
    output_path = os.path.join(output_dir, f"{image_name}.txt")

    # 保存标注文件
    save_yolo_annotation(yolo_annotations, output_path)
    print(f"标注文件已保存到: {output_path}")

def batch_process_json_files(json_folder, output_dir):
    """
    批量处理文件夹中的所有 JSON 文件
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历文件夹中的所有 JSON 文件
    for json_file in os.listdir(json_folder):
        if json_file.endswith(".json"):
            json_file_path = os.path.join(json_folder, json_file)
            process_json_file(json_file_path, output_dir)

# 示例用法
if __name__ == "__main__":
    json_folder = "images/train_label_json"  # 替换为包含 JSON 文件的文件夹路径
    output_dir = "labels/train"  # 替换为输出目录路径

    # 批量处理 JSON 文件
    batch_process_json_files(json_folder, output_dir)