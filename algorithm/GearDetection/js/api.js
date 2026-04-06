/**
 * 齿轮缺陷检测系统 API 交互模块
 */

// API基础URL
const API_BASE_URL = 'http://127.0.0.1:5000';

/**
 * 检查API服务状态
 * @returns {Promise<boolean>} API是否可用
 */
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch (error) {
        console.error('API状态检查失败:', error);
        return false;
    }
}

/**
 * 上传图像并进行缺陷检测
 * @param {File} imageFile - 要检测的图像文件
 * @param {number} confidenceThreshold - 置信度阈值 (0.0-1.0)
 * @returns {Promise<Object>} 检测结果
 */
async function detectDefects(imageFile, confidenceThreshold = 0.25) {
    try {
        // 创建FormData对象
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('confidence', confidenceThreshold);

        // 发送请求
        const response = await fetch(`${API_BASE_URL}/detect`, {
            method: 'POST',
            body: formData
        });

        // 检查响应状态
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `API调用失败: ${response.status}`);
        }

        // 解析响应数据
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('检测API调用错误:', error);
        throw error;
    }
}

/**
 * 获取上传图像的URL
 * @param {string} filename - 图像文件名
 * @returns {string} 图像URL
 */
function getImageUrl(filename) {
    return `${API_BASE_URL}/uploads/${filename}`;
}

// 导出API函数
window.gearApi = {
    checkApiStatus,
    detectDefects,
    getImageUrl
};