import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import os
import shutil
import tempfile


def load_model(model_path):
    """
    加载训练好的YOLO模型
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件不存在: {model_path}")

        print(f"正在加载模型: {model_path}")

        # 方法1: 优先使用ultralytics YOLO类加载（推荐）
        try:
            from ultralytics import YOLO
            model = YOLO(model_path)
            print("成功使用YOLO类加载模型")
            return model
        except ImportError:
            print("未安装ultralytics，请安装: pip install ultralytics")
            raise ImportError("需要安装ultralytics库")
        except Exception as yolo_error:
            print(f"YOLO类加载失败: {yolo_error}")
            raise Exception(f"YOLO模型加载失败: {yolo_error}")

    except Exception as e:
        print(f"模型加载失败: {str(e)}")
        raise Exception(f"无法加载模型 {model_path}: {str(e)}")


def preprocess_image(image_path, size=(640, 640)):
    """
    预处理图像用于YOLO模型输入
    对于ultralytics YOLO，通常直接传入图像路径或PIL图像
    """
    try:
        # 对于ultralytics YOLO，直接返回图像路径和原始尺寸
        if any(ord(char) > 127 for char in image_path):
            # 处理中文路径 - 复制到临时文件
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"temp_image_{os.getpid()}.jpg")
            shutil.copy2(image_path, temp_path)
            image_path = temp_path

        # 获取原始图像尺寸
        with Image.open(image_path) as img:
            orig_width, orig_height = img.size

        print(f"图像预处理完成: {orig_width}x{orig_height}")
        return image_path, (orig_width, orig_height)

    except Exception as e:
        print(f"图像预处理失败: {str(e)}")
        raise Exception(f"无法预处理图像 {image_path}: {str(e)}")


def postprocess_results(results, orig_size, confidence_threshold=0.25):
    """
    后处理YOLO模型输出
    """
    try:
        detections = []

        # 处理ultralytics YOLO的Results对象
        if hasattr(results, 'boxes') and results.boxes is not None:
            boxes = results.boxes

            for i in range(len(boxes)):
                # 获取置信度
                conf = float(boxes.conf[i])

                if conf >= confidence_threshold:
                    # 获取边界框坐标 (xyxy格式)
                    coords = boxes.xyxy[i].cpu().numpy()
                    x1, y1, x2, y2 = coords

                    # 获取类别ID
                    class_id = int(boxes.cls[i])

                    # 计算宽度和高度
                    width = max(1, int(x2 - x1))
                    height = max(1, int(y2 - y1))

                    detections.append({
                        'bbox': {
                            'x': int(x1),
                            'y': int(y1),
                            'width': width,
                            'height': height
                        },
                        'confidence': conf,
                        'class': class_id
                    })

        print(f"后处理完成，检测到 {len(detections)} 个目标")
        return detections

    except Exception as e:
        print(f"后处理失败: {str(e)}")
        return []


def get_model_info(model):
    """
    获取模型信息用于调试
    """
    try:
        info = {
            'type': type(model).__name__,
            'device': 'cpu'
        }

        # 获取类别信息
        if hasattr(model, 'names'):
            info['classes'] = model.names
        elif hasattr(model, 'model') and hasattr(model.model, 'names'):
            info['classes'] = model.model.names

        return info
    except Exception as e:
        return {'type': 'unknown', 'error': str(e)}


def detect_objects(model_path, image_path, confidence_threshold=0.25):
    """
    完整的目标检测流程
    """
    try:
        # 加载模型
        model = load_model(model_path)

        # 获取模型信息
        model_info = get_model_info(model)
        print(f"模型信息: {model_info}")

        # 预处理图像
        processed_image_path, orig_size = preprocess_image(image_path)

        # 使用YOLO模型进行预测
        results = model.predict(processed_image_path, conf=confidence_threshold, verbose=False)

        # 后处理结果
        if results and len(results) > 0:
            detections = postprocess_results(results[0], orig_size, confidence_threshold)
        else:
            detections = []

        # 清理临时文件
        if processed_image_path != image_path and os.path.exists(processed_image_path):
            try:
                os.remove(processed_image_path)
            except:
                pass

        return detections

    except Exception as e:
        print(f"检测过程失败: {str(e)}")
        raise