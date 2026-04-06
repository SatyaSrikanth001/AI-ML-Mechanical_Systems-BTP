

Chinese (Simplified) - Detected

Hindi

Tamil

Punjabi (Gurmukhi)

English

Limburgish

Telugu
# 齿轮缺陷检测系统

## 项目概述

齿轮缺陷检测系统是一个基于深度学习的Web应用，用于自动识别和分析齿轮表面的常见缺陷。系统采用YOLO目标检测模型，能够检测包括点蚀、剥落、压伤和擦伤在内的多种齿轮缺陷类型。

## 系统特点

- **高精度检测**：基于训练好的YOLO模型，提供高精度的缺陷识别
- **用户友好界面**：直观的Web界面，支持图像上传和结果可视化
- **实时分析**：快速处理上传图像并显示检测结果
- **结果导出**：支持检测结果图像的下载和保存
- **参数调整**：允许用户调整检测置信度阈值

## 目录结构

```
├── index.html                # 项目主页面
├── home.html                 # 检测应用主界面
├── css/                      # 样式文件
│   └── styles.css            # 主样式表
├── js/                       # JavaScript脚本
│   ├── api.js                # API交互模块
│   └── imageHandler.js       # 图像处理模块
├── img/                      # 图像资源
├── model/                    # 模型文件
│   └── model_loader.py       # 模型加载器
├── api/                      # 后端API
│   ├── app.py                # Flask应用主文件
│   └── config.py             # API配置文件
├── uploads/                  # 上传图像存储目录
├── docs/                     # 文档
│   └── 使用说明.md            # 使用指南
└── requirements.txt          # Python依赖包列表
```

## 技术栈

- **前端**：HTML, CSS, JavaScript, React (CDN加载)
- **后端**：Python, Flask
- **深度学习**：PyTorch, YOLO

## 快速开始

### 环境准备

1. 确保已安装Python 3.7+
2. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
3. 将训练好的模型文件（.pt格式）放入`model`目录，并命名为`best.pt`

### 启动服务

1. 启动后端API服务：
   ```
   python api/app.py
   ```
2. 在浏览器中打开前端页面：
   ```
   http://localhost:5000
   ```
   或直接打开`index.html`文件

## 使用流程

1. 在首页点击"进入应用"按钮
2. 在应用页面上传齿轮图像
3. 调整检测参数（可选）
4. 点击"开始检测"按钮
5. 查看检测结果和统计信息
6. 下载结果图像（可选）

## 注意事项

- 确保API服务正常运行，检查页面上的API状态指示器
- 上传图像应清晰可见，光照充足
- 支持的图像格式：JPG, PNG
- 最大上传文件大小：16MB

## 开发者信息

本系统基于您训练的YOLO模型构建，支持四种齿轮缺陷类型的自动识别。
# Chǐlún quēxiàn jiǎncè xìtǒng ## xiàngmù gàishù chǐlún quēxiàn jiǎncè xìtǒng shì yīgè jīyú shēndù xuéxí de Web yìngyòng, yòng yú zìdòng shìbié hé fēnxī chǐlún biǎomiàn de chángjiàn quēxiàn. Xìtǒng cǎiyòng YOLO mùbiāo jiǎncè móxíng, nénggòu jiǎncè bāokuò diǎn shí, bōluò, yā shāng hé cā shāng zài nèi de duō zhǒng chǐlún quēxiàn lèixíng. ## Xìtǒng tèdiǎn - **gāo jīngdù jiǎncè**: Jīyú xùnliàn hǎo de YOLO móxíng, tígōng gāo jīngdù de quēxiàn shìbié - **yònghù yǒuhǎo jièmiàn**: Zhíguān de Web jièmiàn, zhīchí túxiàng shàngchuán hé jiéguǒ kěshìhuà - **shíshí fēnxī**: Kuàisù chǔlǐ shàngchuán túxiàng bìng xiǎnshì jiǎncè jiéguǒ - **jiéguǒ dǎochū**: Zhīchí jiǎncè jiéguǒ túxiàng de xiàzài hé bǎocún - **cānshù tiáozhěng**: Yǔnxǔ yònghù tiáozhěng jiǎncè zhìxìn dù yùzhí ## mùlù jiégòu ``` ├── index.Html # xiàngmù zhǔyèmiàn ├── home.Html # jiǎncè yìngyòng zhǔ jièmiàn ├── css/ # yàngshì wénjiàn ￨ └── styles.Css # zhǔ yàngshì biǎo ├── js/ # JavaScript jiǎoběn ￨ ├── api.Js # API jiāohù mókuài ￨ └── imageHandler.Js # túxiàng chǔlǐ mókuài ├── img/ # túxiàng zīyuán ├── model/ # móxíng wénjiàn ￨ └── model_loader.Py # móxíng jiāzài qì ├── api/ # hòu duān API ￨ ├── app.Py # Flask yìngyòng zhǔ wénjiàn ￨ └── config.Py # API pèizhì wénjiàn ├── uploads/ # shàngchuán túxiàng cúnchú mùlù ├── docs/ # wéndàng ￨ └── shǐyòng shuōmíng.Md # shǐyòng zhǐnán └── requirements.Txt # Python yīlài bāo lièbiǎo ``` ## jìshù zhàn - **qiánduān**:HTML, CSS, JavaScript, React (CDN jiāzài) - **hòu duān**:Python, Flask - **shēndù xuéxí**:PyTorch, YOLO ## kuàisù kāishǐ ### huánjìng zhǔnbèi 1. Quèbǎo yǐ ānzhuāng Python 3.7+ 2. Ānzhuāng yīlài bāo: ``` Pip install -r requirements.Txt ``` 3. Jiāng xùnliàn hǎo de móxíng wénjiàn (.Pt géshì) fàng rù `model`mùlù, bìng mìngmíng wèi `best.Pt` ### qǐdòng fúwù 1. Qǐdòng hòu duān API fúwù: ``` Python api/app.Py ``` 2. Zài liúlǎn qì zhōng dǎkāi qiánduān yèmiàn: ``` Http://Localhost:5000 ``` Huò zhíjiē dǎkāi `index.Html`wénjiàn ## shǐyòng liúchéng 1. Zài shǒuyè diǎnjī"jìnrù yìngyòng"ànniǔ 2. Zài yìngyòng yèmiàn shàngchuán chǐlún túxiàng 3. Tiáozhěng jiǎncè cānshù (kě xuǎn) 4. Diǎnjī"kāishǐ jiǎncè"ànniǔ 5. Chákàn jiǎncè jiéguǒ hé tǒngjì xìnxī 6. Xiàzài jiéguǒ túxiàng (kě xuǎn) ## zhùyì shìxiàng - quèbǎo API fúwù zhèngcháng yùnxíng, jiǎnchá yè miàn shàng de API zhuàngtài zhǐshì qì - shàngchuán túxiàng yīng qīngxī kějiàn, guāngzhào chōngzú - zhīchí de túxiàng géshì:JPG, PNG - zuìdà shàngchuán wénjiàn dàxiǎo:16MB ## kāifā zhě xìnxī běn xìtǒng jīyú nín xùnliàn de YOLO móxíng gòujiàn, zhīchí sì zhǒng chǐlún quēxiàn lèixíng de zìdòng shìbié.
Show more
1,569
# Gear Defect Detection System

## Project Overview

The Gear Defect Detection System is a deep learning-based web application designed to automatically identify and analyze common defects on gear surfaces. The system utilizes the YOLO object detection model to detect various types of gear defects, including pitting, spalling, indentation, and abrasion. ## System Features

- **High-Precision Detection**: Based on a pre-trained YOLO model, providing high-accuracy defect recognition.
- **User-Friendly Interface**: An intuitive web interface supporting image uploads and result visualization.
- **Real-time Analysis**: Rapidly processes uploaded images and displays detection results.
- **Result Export**: Supports downloading and saving images containing detection results.
- **Parameter Adjustment**: Allows users to adjust the detection confidence threshold.

## Directory Structure

```
├── index.html                # Project main page
├── home.html                 # Main interface for the detection application
├── css/                      # Stylesheet files
│   └── styles.css            # Main stylesheet
├── js/                       # JavaScript scripts
│   ├── api.js                # API interaction module
│   └── imageHandler.js       # Image processing module
├── img/                      # Image assets
├── model/                    # Model files
│   └── model_loader.py       # Model loader
├── api/                      # Backend API
│   ├── app.py                # Main Flask application file
│   └── config.py             # API configuration file
├── uploads/                  # Directory for storing uploaded images
├── docs/                     # Documentation
│   └── 使用说明.md            # User Guide
└── requirements.txt          # List of Python dependencies
```

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript, React (loaded via CDN)
- **Backend**: Python, Flask
- **Deep Learning**: PyTorch, YOLO

## Quick Start

### Environment Setup

1. Ensure that Python 3.7+ is installed.
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Place the pre-trained model file (in `.pt` format) into the `model` directory and name it `best.pt`.

### Launching the Service

1. Start the backend API service:
```
python api/app.py
```
2. Open the frontend page in your browser:
```
http://localhost:5000
```
Alternatively, open the `index.html` file directly.

## Usage Workflow

1. Click the "Enter Application" button on the homepage.
2. Upload a gear image on the application page.
3. Adjust detection parameters (optional).
4. Click the "Start Detection" button
5. View detection results and statistics
6. Download result images (Optional)

## Important Notes

- Ensure the API service is operational; check the API status indicator on the page
- Uploaded images should be clear, visible, and well-lit
- Supported image formats: JPG, PNG
- Maximum upload file size: 16MB

## Developer Information

This system is built upon your trained YOLO model and supports the automatic detection of four types of gear defects.
Send feedback

