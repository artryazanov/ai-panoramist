> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** is a Python CLI tool designed to generate seamless, equirectangular 360-degree panoramas using Google Gemini's advanced multimodal generation and prompt-enhancement capabilities.

By automatically applying the mathematically correct formatting markers and spatial logic (zenith/nadir), this tool helps generate high-quality assets ready for use in VR mapping or 360-degree viewers.

## 🖼️ Examples

![Cyberpunk Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/cyberpunk_example.jpg)
![Beach Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/beach_example.jpg)

## ✨ Features

- **Prompt Enhancement Loop**: Converts simple user prompts (e.g., "A cyberpunk city at night") into rigorous VR-ready prompts containing zenith, nadir, and horizon specifications.
- **Automated QA Validation & Refinement**: The built-in LLM QA checks generated images to ensure they look like proper panoramas. If an attempt fails, it feeds the critique back to the generator to produce a corrected panorama on the next attempt.
- **Conditional Seamless Blending**: After a successful generation, the tool analyzes the image for vertical back seams. If a severe seam is detected, it automatically uses AI inpainting and alpha-blending to repair it, ensuring a perfectly seamless 360-degree wrap-around.
- **Multimodal Reference Support**: Provide local images to guide the generation (style transfer, character inclusion, or base layouts).
- **Docker Ready**: Easy to deploy and run in an isolated environment using Docker Compose.

## 🛠️ Prerequisites

- **Python 3.12+** (if running locally)
- **Docker** & **Docker Compose** (recommended for isolation)
- **Google Cloud API Key** with access to Gemini models (including image generation capabilities).

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. Configure Environment
Copy the example environment file and add your API key.
```bash
cp .env.example .env
```
Open `.env` and set your variables:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Running with Docker (Recommended)

Build the Docker image:
```bash
docker-compose build
```

Run the default command:
```bash
docker-compose up
```

### 4. Running Locally

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## 💡 Usage

### Using the CLI Locally

Run the `main.py` script and provide a prompt:

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**Using Reference Images:**
If you want to pass an image for style or content context, use the `--image-refs` flag.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
You can pass multiple reference images by repeating the flag:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### Using Docker Compose

If you want to run specific CLI commands using Docker, you can run:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(Ensure any reference paths are accessible inside the container, typically by mounting them or placing them in your project directory).*

## 🏗️ Architecture

The project consists of three main components under `app/core`:
1. **PromptEnhancer**: Communicates with the text model (`TEXT_MODEL_NAME`) to expand short user descriptions into detailed VR prompts.
2. **GenAIClient**: Wraps the `google-genai` SDK to handle structured output parsing, multimodal image generation (`IMAGE_MODEL_NAME`), and the QA visual inspection (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: The orchestrator that ties enhancement, generation, and validation retries together into one cohesive loop.

## 🧪 Development & Testing

Unit tests are written using `pytest` and `pytest-mock`. The project aims for 100% test coverage.

**Using Docker (Recommended):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**Using Local Python Environment:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.