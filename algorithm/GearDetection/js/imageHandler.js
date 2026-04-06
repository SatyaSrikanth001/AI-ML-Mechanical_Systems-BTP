/**
 * 齿轮缺陷检测系统 图像处理模块
 */

/**
 * 处理图像上传
 * @param {File} file - 上传的图像文件
 * @returns {Promise<Object>} 包含图像URL和文件信息的对象
 */
function handleImageUpload(file) {
    return new Promise((resolve, reject) => {
        // 检查文件类型
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            reject(new Error('不支持的文件类型，请上传JPG或PNG图像'));
            return;
        }

        // 检查文件大小 (限制为16MB)
        const maxSize = 16 * 1024 * 1024; // 16MB
        if (file.size > maxSize) {
            reject(new Error('文件过大，请上传小于16MB的图像'));
            return;
        }

        // 读取文件为DataURL
        const reader = new FileReader();
        reader.onload = (e) => {
            resolve({
                file: file,
                url: e.target.result,
                name: file.name
            });
        };
        reader.onerror = () => {
            reject(new Error('文件读取失败'));
        };
        reader.readAsDataURL(file);
    });
}

/**
 * 在Canvas上绘制检测结果
 * @param {HTMLCanvasElement} canvas - 目标Canvas元素
 * @param {string} imageUrl - 图像URL
 * @param {Array} detections - 检测结果数组
 * @param {Object} defectClasses - 缺陷类别定义
 */
function drawDetectionResults(canvas, imageUrl, detections, defectClasses) {
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const img = new Image();

    img.onload = () => {
        // 设置Canvas尺寸与图像一致
        canvas.width = img.width;
        canvas.height = img.height;
        
        // 绘制原始图像
        ctx.drawImage(img, 0, 0);

        // 绘制检测框
        detections.forEach((detection) => {
            const { bbox, class: classId, confidence } = detection;
            const defectInfo = defectClasses[classId];

            // 设置边框样式
            ctx.strokeStyle = defectInfo.color;
            ctx.lineWidth = 3;
            ctx.fillStyle = defectInfo.color;
            ctx.font = '16px Arial';

            // 绘制边界框
            ctx.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height);

            // 绘制标签背景
            const label = `${defectInfo.name} ${(confidence * 100).toFixed(1)}%`;
            const textMetrics = ctx.measureText(label);
            const textWidth = textMetrics.width;
            const textHeight = 20;

            ctx.fillRect(bbox.x, bbox.y - textHeight - 5, textWidth + 10, textHeight + 5);
            
            // 绘制标签文本
            ctx.fillStyle = 'white';
            ctx.fillText(label, bbox.x + 5, bbox.y - 8);
        });
    };

    img.src = imageUrl;
}

/**
 * 下载Canvas内容为图像
 * @param {HTMLCanvasElement} canvas - 源Canvas元素
 * @param {string} filename - 下载文件名
 */
function downloadCanvasImage(canvas, filename = 'detection_result') {
    if (!canvas) return;

    // 创建下载链接
    const link = document.createElement('a');
    link.download = `${filename}_${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
}

// 导出函数
window.imageHandler = {
    handleImageUpload,
    drawDetectionResults,
    downloadCanvasImage
};