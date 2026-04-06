from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import time
import torch
from werkzeug.utils import secure_filename
from flask_cors import CORS

# 添加父目录到路径，以便导入model模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.model_loader import load_model, preprocess_image, postprocess_results

# 全局变量存储模型
model = None

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# 配置
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 模型路径
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'best_v11_120ep.pt')


def allowed_file(filename):
    """
    检查文件扩展名是否允许
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/health', methods=['GET'])
def health_check():
    """
    健康检查接口
    """
    return jsonify({'status': 'ok', 'message': 'API服务正常运行'})


@app.route('/detect', methods=['POST'])
def detect():
    """
    齿轮缺陷检测接口
    """
    global model

    # 检查是否有文件上传
    if 'image' not in request.files:
        return jsonify({'error': '没有上传图像'}), 400

    file = request.files['image']

    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'error': '未选择图像'}), 400

    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件类型'}), 400

    # 获取置信度阈值参数
    confidence_threshold = float(request.form.get('confidence', 0.25))

    # 保存上传的文件
    filename = secure_filename(f"{int(time.time())}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # 懒加载模型
        if model is None:
            print(f"正在加载模型: {MODEL_PATH}")
            model = load_model(MODEL_PATH)

        # 预处理图像
        processed_image_path, orig_size = preprocess_image(filepath)

        # 执行推理 - 使用YOLO的predict方法
        results = model.predict(processed_image_path, conf=confidence_threshold, verbose=False)

        # 后处理结果
        if results and len(results) > 0:
            detections = postprocess_results(results[0], orig_size, confidence_threshold)
        else:
            detections = []

        # 清理临时文件
        if processed_image_path != filepath and os.path.exists(processed_image_path):
            try:
                os.remove(processed_image_path)
            except:
                pass

        return jsonify({
            'status': 'success',
            'detections': detections,
            'image_path': filename
        })

    except Exception as e:
        print(f"检测失败: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

    finally:
        # 清理上传的文件（可选）
        # os.remove(filepath)
        pass


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    提供上传的图像文件
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # 检查模型文件是否存在
    if not os.path.exists(MODEL_PATH):
        print(f"错误: 模型文件不存在: {MODEL_PATH}")
        print("请确保将训练好的best.pt文件放在model目录下")
        sys.exit(1)

    print(f"模型路径: {MODEL_PATH}")
    print(f"上传目录: {app.config['UPLOAD_FOLDER']}")

    # 启动Flask应用
    app.run(debug=True, host='127.0.0.1', port=5000)