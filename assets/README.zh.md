> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** 是一款 Python 命令行（CLI）工具，旨在利用 Google Gemini 先进的多模态生成和提示词增强功能，生成无缝的等距柱状投影（equirectangular）360 度全景图。

通过自动应用数学上正确的格式标记和空间逻辑（天顶/天底），该工具有助于生成高质量的资产，可直接用于 VR 映射或 360 度全景查看器。

## ✨ 功能特性

- **提示词增强循环**：将简单的用户提示词（例如：“夜晚的赛博朋克城市”）转换为严格的适用于 VR 的提示词，包含天顶（zenith）、天底（nadir）和地平线（horizon）规范。
- **自动化的 QA 验证与改进**：内置的 LLM QA 会检查生成的图像，以确保它们看起来像标准的全景图。如果尝试失败，它会将批评意见反馈给生成器，并以此被拒绝的图像作为基础，在下一次尝试中进行 **图生图（img2img）改进**。
- **条件性无缝融合**：生成成功后，该工具会分析图像是否存在垂直后接缝。如果检测到严重的接缝，它会自动使用 AI 内画（inpainting）和 Alpha 混合（alpha-blending）对其进行修复，确保完美的无缝 360 度环绕。
- **多模态参考支持**：提供本地图像以指导生成（风格迁移、角色包含或基础布局）。
- **支持 Docker**：使用 Docker Compose，在隔离环境中轻松部署和运行。

## 🛠️ 前置要求

- **Python 3.12+**（如果要在本地运行）
- **Docker** & **Docker Compose**（推荐用于环境隔离）
- **Google Cloud API 密钥**，需要具备访问 Gemini 模型（包括图像生成功能）的权限。

## 🚀 安装与设置

### 1. 克隆仓库
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. 配置环境
复制示例环境文件并添加您的 API 密钥。
```bash
cp .env.example .env
```
打开 `.env` 文件并设置您的变量：
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. 使用 Docker 运行（推荐）

构建 Docker 镜像：
```bash
docker-compose build
```

运行默认命令：
```bash
docker-compose up
```

### 4. 在本地运行

创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate
```

安装依赖：
```bash
pip install -r requirements.txt
```

## 💡 使用方法

### 在本地使用 CLI

运行 `main.py` 脚本并提供提示词：

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**使用参考图像：**
如果您想传递图像以获取风格或内容上下文，请使用 `--image-refs` 标志。

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
您可以通过重复该标志来传递多张参考图像：
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### 使用 Docker Compose

如果您想使用 Docker 运行特定的 CLI 命令，您可以执行：

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(请确保容器内可以访问任何参考路径，通常可以通过挂载或将其放置在项目目录中来实现)。*

## 🏗️ 架构

该项目由 `app/core` 下的三个主要组件组成：
1. **PromptEnhancer（提示词增强器）**：与文本模型（`TEXT_MODEL_NAME`）通信，将简短的用户描述扩展为详细的 VR 提示词。
2. **GenAIClient（GenAI 客户端）**：封装了 `google-genai` SDK，以处理结构化输出解析、多模态图像生成（`IMAGE_MODEL_NAME`）和 QA 视觉检查（`VALIDATOR_MODEL_NAME`）。
3. **Panoramist（全景图生成器）**：协调器，将增强、生成和验证重试整合到一个有凝聚力的循环中。

## 🧪 开发与测试

单元测试使用 `pytest` 和 `pytest-mock` 编写。项目旨在实现 100% 的测试覆盖率。

**使用 Docker（推荐）：**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**使用本地 Python 环境：**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 许可证

本项目基于 MIT 许可证开源 - 详情请查看 [LICENSE](LICENSE) 文件。