/**
 * 齿轮缺陷检测系统 演示模块
 * 用于在没有后端API的情况下提供演示功能
 */

// 演示模式标志
const DEMO_MODE = false;

// 演示用的缺陷类别定义
const DEMO_DEFECT_CLASSES = {
    '0': {
        'name': '点蚀',
        'description': '齿轮表面出现的小点状腐蚀或损伤',
        'color': '#FF3B30'  // 红色
    },
    '1': {
        'name': '剥落',
        'description': '齿轮表面材料脱落形成的缺陷',
        'color': '#FF9500'  // 橙色
    },
    '2': {
        'name': '压伤',
        'description': '由外力挤压导致的齿轮表面凹陷',
        'color': '#4CD964'  // 绿色
    },
    '3': {
        'name': '擦伤',
        'description': '齿轮表面的线状磨损痕迹',
        'color': '#007AFF'  // 蓝色
    }
};

// 演示用的检测结果
const DEMO_DETECTION_RESULTS = {
    'gear_sample_1.jpg': [
        { class: 0, confidence: 0.92, bbox: { x: 150, y: 120, width: 60, height: 40 } },
        { class: 0, confidence: 0.85, bbox: { x: 320, y: 220, width: 45, height: 35 } },
        { class: 2, confidence: 0.78, bbox: { x: 400, y: 180, width: 70, height: 50 } }
    ],
    'gear_sample_2.jpg': [
        { class: 1, confidence: 0.88, bbox: { x: 200, y: 150, width: 80, height: 60 } },
        { class: 3, confidence: 0.76, bbox: { x: 350, y: 200, width: 120, height: 30 } }
    ],
    'gear_sample_3.jpg': [
        { class: 0, confidence: 0.81, bbox: { x: 180, y: 140, width: 50, height: 40 } },
        { class: 1, confidence: 0.79, bbox: { x: 280, y: 190, width: 65, height: 55 } },
        { class: 2, confidence: 0.83, bbox: { x: 380, y: 220, width: 70, height: 60 } },
        { class: 3, confidence: 0.75, bbox: { x: 450, y: 150, width: 90, height: 40 } }
    ]
};

/**
 * 模拟API状态检查
 * @returns {Promise<boolean>} 模拟的API状态
 */
async function demoCheckApiStatus() {
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 800));
    return true;
}

/**
 * 模拟缺陷检测过程
 * @param {File} imageFile - 图像文件
 * @param {number} confidenceThreshold - 置信度阈值
 * @returns {Promise<Object>} 模拟的检测结果
 */
async function demoDetectDefects(imageFile, confidenceThreshold = 0.25) {
    // 模拟处理延迟
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 获取文件名，用于查找演示结果
    const filename = imageFile.name.toLowerCase();
    let detections = [];
    
    // 查找匹配的演示结果，如果没有则生成随机结果
    for (const [demoName, demoResults] of Object.entries(DEMO_DETECTION_RESULTS)) {
        if (filename.includes(demoName.split('_')[1].split('.')[0])) {
            detections = demoResults.filter(d => d.confidence >= confidenceThreshold);
            break;
        }
    }
    
    // 如果没有匹配的演示结果，生成随机结果
    if (detections.length === 0) {
        const numDetections = Math.floor(Math.random() * 5) + 1; // 1-5个检测结果
        
        for (let i = 0; i < numDetections; i++) {
            const classId = Math.floor(Math.random() * 4); // 0-3的缺陷类别
            const confidence = Math.random() * 0.5 + 0.5; // 0.5-1.0的置信度
            
            if (confidence >= confidenceThreshold) {
                detections.push({
                    class: classId,
                    confidence: confidence,
                    bbox: {
                        x: Math.floor(Math.random() * 400) + 100,
                        y: Math.floor(Math.random() * 300) + 100,
                        width: Math.floor(Math.random() * 80) + 40,
                        height: Math.floor(Math.random() * 60) + 30
                    }
                });
            }
        }
    }
    
    // 统计各类缺陷数量
    const defect_counts = {};
    for (let i = 0; i < 4; i++) {
        defect_counts[i] = 0;
    }
    
    detections.forEach(detection => {
        defect_counts[detection.class]++;
    });
    
    // 构建结果对象
    return {
        detections: detections,
        defect_classes: DEMO_DEFECT_CLASSES,
        defect_counts: defect_counts,
        total_defects: detections.length,
        inference_time: (Math.random() * 0.5 + 0.2).toFixed(3), // 0.2-0.7秒的推理时间
        filename: imageFile.name,
        upload_time: Math.floor(Date.now() / 1000),
        image_size: { width: 800, height: 600 }
    };
}

/**
 * 初始化演示模式
 * 如果启用了演示模式，将替换API函数为演示函数
 */
function initDemoMode() {
    if (DEMO_MODE && window.gearApi) {
        console.log('启用演示模式 - API调用将被模拟');
        
        // 替换API函数
        window.gearApi.checkApiStatus = demoCheckApiStatus;
        window.gearApi.detectDefects = demoDetectDefects;
        window.gearApi.getImageUrl = (filename) => URL.createObjectURL(window.lastUploadedImage);
        
        // 存储最后上传的图像，用于演示模式下显示
        window.lastUploadedImage = null;
        
        // 修改原始的handleImageUpload函数以保存图像
        const originalHandleImageUpload = window.imageHandler.handleImageUpload;
        window.imageHandler.handleImageUpload = async (file) => {
            window.lastUploadedImage = file;
            return originalHandleImageUpload(file);
        };
    }
}

// 在页面加载完成后初始化演示模式
document.addEventListener('DOMContentLoaded', function() {
    initDemoMode();
});

// 导出演示函数
window.demoModule = {
    initDemoMode,
    DEMO_MODE,
    DEMO_DEFECT_CLASSES
};