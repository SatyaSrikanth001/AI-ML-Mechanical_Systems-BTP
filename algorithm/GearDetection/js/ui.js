/**
 * 齿轮缺陷检测系统 UI交互模块
 */

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化UI组件
    initUI();
});

/**
 * 初始化UI组件和交互
 */
function initUI() {
    // 添加页面加载动画
    addPageLoadAnimation();
    
    // 初始化工具提示
    initTooltips();
    
    // 初始化滑块组件
    initSliders();
    
    // 添加响应式导航菜单
    setupResponsiveNav();
}

/**
 * 添加页面加载动画
 */
function addPageLoadAnimation() {
    // 添加页面元素的淡入效果
    const fadeElements = document.querySelectorAll('.header, .card');
    
    fadeElements.forEach((element, index) => {
        // 设置初始透明度为0
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        // 延迟显示元素
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100 + (index * 150)); // 错开动画时间
    });
}

/**
 * 初始化工具提示
 */
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        // 创建工具提示元素
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = element.getAttribute('data-tooltip');
        
        // 鼠标悬停显示工具提示
        element.addEventListener('mouseenter', () => {
            document.body.appendChild(tooltip);
            positionTooltip(tooltip, element);
            
            setTimeout(() => {
                tooltip.style.opacity = '1';
                tooltip.style.transform = 'translateY(0)';
            }, 10);
        });
        
        // 鼠标离开隐藏工具提示
        element.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translateY(10px)';
            
            setTimeout(() => {
                if (tooltip.parentNode) {
                    document.body.removeChild(tooltip);
                }
            }, 300);
        });
    });
}

/**
 * 定位工具提示
 * @param {HTMLElement} tooltip - 工具提示元素
 * @param {HTMLElement} element - 触发元素
 */
function positionTooltip(tooltip, element) {
    const rect = element.getBoundingClientRect();
    const tooltipHeight = tooltip.offsetHeight;
    
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltipHeight - 10 + 'px';
}

/**
 * 初始化滑块组件
 */
function initSliders() {
    const sliders = document.querySelectorAll('input[type="range"]');
    
    sliders.forEach(slider => {
        // 创建或获取值显示元素
        let valueDisplay = document.querySelector(`#${slider.id}-value`);
        
        if (!valueDisplay && slider.hasAttribute('data-show-value')) {
            valueDisplay = document.createElement('span');
            valueDisplay.id = `${slider.id}-value`;
            valueDisplay.className = 'slider-value';
            slider.parentNode.appendChild(valueDisplay);
        }
        
        // 更新滑块值显示
        if (valueDisplay) {
            updateSliderValue(slider, valueDisplay);
            
            slider.addEventListener('input', () => {
                updateSliderValue(slider, valueDisplay);
            });
        }
    });
}

/**
 * 更新滑块值显示
 * @param {HTMLElement} slider - 滑块元素
 * @param {HTMLElement} valueDisplay - 值显示元素
 */
function updateSliderValue(slider, valueDisplay) {
    const value = slider.value;
    const min = slider.min || 0;
    const max = slider.max || 100;
    const percentage = ((value - min) / (max - min)) * 100;
    
    // 更新值显示
    if (slider.hasAttribute('data-value-format')) {
        const format = slider.getAttribute('data-value-format');
        valueDisplay.textContent = format.replace('{value}', value);
    } else {
        valueDisplay.textContent = value;
    }
    
    // 更新滑块填充样式
    slider.style.background = `linear-gradient(to right, var(--primary-color) 0%, var(--primary-color) ${percentage}%, #e2e8f0 ${percentage}%, #e2e8f0 100%)`;
}

/**
 * 设置响应式导航菜单
 */
function setupResponsiveNav() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('nav-open');
            navToggle.classList.toggle('nav-toggle-active');
        });
        
        // 点击导航链接后关闭菜单
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('nav-open');
                navToggle.classList.remove('nav-toggle-active');
            });
        });
    }
}

// 导出UI函数
window.ui = {
    initUI,
    addPageLoadAnimation,
    initTooltips,
    initSliders
};