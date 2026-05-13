> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** คือเครื่องมือ Python CLI ที่ออกแบบมาเพื่อสร้างภาพพาโนรามา 360 องศาแบบ equirectangular ที่ไร้รอยต่อ โดยใช้ความสามารถในการสร้างภาพแบบหลายโหมด (multimodal) ขั้นสูงและการปรับปรุงพรอมต์ (prompt-enhancement) ของ Google Gemini

ด้วยการใส่เครื่องหมายการจัดรูปแบบที่ถูกต้องตามหลักคณิตศาสตร์และตรรกะเชิงพื้นที่ (จุดจอมฟ้า/จุดจอมดิน) โดยอัตโนมัติ เครื่องมือนี้จะช่วยสร้างแอสเซตคุณภาพสูงที่พร้อมใช้งานสำหรับการทำแผนที่ VR หรือโปรแกรมดูภาพ 360 องศา

## 🖼️ ตัวอย่าง

![Cyberpunk Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/cyberpunk_example.jpg)
![Beach Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/beach_example.jpg)

## ✨ คุณสมบัติ

- **Prompt Enhancement Loop**: แปลงพรอมต์ง่ายๆ จากผู้ใช้ (เช่น "เมืองไซเบอร์พังก์ตอนกลางคืน") ให้เป็นพรอมต์ที่พร้อมสำหรับ VR อย่างละเอียด ซึ่งประกอบด้วยข้อกำหนดของจุดเหนือศีรษะ (zenith) จุดใต้เท้า (nadir) และเส้นขอบฟ้า (horizon)
- **Automated QA Validation & Refinement**: ระบบ QA ของ LLM ที่มาในตัวจะตรวจสอบภาพที่สร้างขึ้นเพื่อให้แน่ใจว่าดูเหมือนภาพพาโนรามาที่ถูกต้อง หากการสร้างล้มเหลว ระบบจะส่งคำวิจารณ์กลับไปยังตัวสร้างเพื่อสร้างภาพพาโนรามาที่แก้ไขแล้วในครั้งต่อไป
- **Conditional Seamless Blending**: หลังจากการสร้างสำเร็จ เครื่องมือจะวิเคราะห์ภาพเพื่อหารอยต่อแนวตั้งด้านหลัง หากตรวจพบรอยต่อที่ชัดเจน ระบบจะใช้ AI inpainting และ alpha-blending เพื่อซ่อมแซมโดยอัตโนมัติ เพื่อให้ได้ภาพ 360 องศาที่เชื่อมต่อกันอย่างแนบเนียนไร้รอยต่ออย่างสมบูรณ์แบบ
- **Multimodal Reference Support**: สามารถให้ภาพจากเครื่องของคุณเพื่อใช้เป็นแนวทางในการสร้าง (เช่น การถ่ายทอดสไตล์ การแทรกตัวละคร หรือเลย์เอาต์พื้นฐาน)
- **Docker Ready**: ปรับใช้และเรียกใช้งานในสภาพแวดล้อมแบบแยกส่วนได้ง่ายโดยใช้ Docker Compose

## 🛠️ สิ่งที่ต้องมีเบื้องต้น

- **Python 3.12+** (หากรันบนเครื่องของคุณเอง)
- **Docker** และ **Docker Compose** (แนะนำสำหรับการแยกสภาพแวดล้อม)
- **Google Cloud API Key** ที่สามารถเข้าถึงโมเดลของ Gemini ได้ (รวมถึงความสามารถในการสร้างภาพ)

## 🚀 การติดตั้งและการตั้งค่า

### 1. โคลน Repository
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. กำหนดค่า Environment
คัดลอกไฟล์ environment ตัวอย่างแล้วเพิ่ม API key ของคุณ
```bash
cp .env.example .env
```
เปิดไฟล์ `.env` และตั้งค่าตัวแปรของคุณ:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. การรันด้วย Docker (แนะนำ)

สร้าง (Build) Docker image:
```bash
docker-compose build
```

รันคำสั่งเริ่มต้น:
```bash
docker-compose up
```

### 4. การรันบนเครื่องของคุณเอง (Locally)

สร้าง virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

## 💡 การใช้งาน

### การใช้งาน CLI บนเครื่องของคุณเอง

รันสคริปต์ `main.py` และระบุพรอมต์:

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**การใช้ภาพอ้างอิง (Reference Images):**
หากคุณต้องการส่งภาพเพื่อใช้เป็นบริบทสำหรับสไตล์หรือเนื้อหา ให้ใช้แฟล็ก `--image-refs`

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
คุณสามารถส่งภาพอ้างอิงหลายภาพได้โดยใส่แฟล็กซ้ำ:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### การใช้งาน Docker Compose

หากคุณต้องการรันคำสั่ง CLI ที่เฉพาะเจาะจงโดยใช้ Docker คุณสามารถรัน:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(ตรวจสอบให้แน่ใจว่า path อ้างอิงใดๆ สามารถเข้าถึงได้ภายในคอนเทนเนอร์ โดยปกติจะทำได้ผ่านการเมาท์ (mounting) หรือการวางไว้ในไดเรกทอรีโปรเจกต์ของคุณ)*

## 🏗️ สถาปัตยกรรม (Architecture)

โปรเจกต์นี้ประกอบด้วยส่วนประกอบหลัก 3 ส่วนภายใต้ `app/core`:
1. **PromptEnhancer**: สื่อสารกับโมเดลข้อความ (`TEXT_MODEL_NAME`) เพื่อขยายคำอธิบายสั้นๆ ของผู้ใช้ให้เป็นพรอมต์ VR ที่มีรายละเอียด
2. **GenAIClient**: ครอบการทำงานของ SDK `google-genai` เพื่อจัดการการแยกวิเคราะห์เอาต์พุตที่มีโครงสร้าง การสร้างภาพแบบ multimodal (`IMAGE_MODEL_NAME`) และการตรวจสอบภาพด้วย QA (`VALIDATOR_MODEL_NAME`)
3. **Panoramist**: ตัวควบคุมที่เชื่อมโยงกระบวนการปรับปรุง การสร้าง และการตรวจสอบความถูกต้องซ้ำให้เป็นลูปเดียวกันที่สอดคล้องกัน

## 🧪 การพัฒนาและการทดสอบ

Unit tests ถูกเขียนขึ้นโดยใช้ `pytest` และ `pytest-mock` โปรเจกต์นี้ตั้งเป้าหมายไว้ที่ test coverage 100%

**การใช้ Docker (แนะนำ):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**การใช้ Local Python Environment:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 ไลเซนส์ (License)

โปรเจกต์นี้ได้รับอนุญาตภายใต้ MIT License - ดูรายละเอียดเพิ่มเติมได้ที่ไฟล์ [LICENSE](LICENSE)