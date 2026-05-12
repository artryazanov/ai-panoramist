> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** เป็นเครื่องมือ Python CLI ที่ออกแบบมาเพื่อสร้างภาพพาโนรามา 360 องศาแบบ equirectangular ที่ไร้รอยต่อ โดยใช้ความสามารถในการสร้างแบบหลายโมดัล (multimodal) ขั้นสูงและการปรับปรุงคำสั่ง (prompt-enhancement) ของ Google Gemini

ด้วยการใช้เครื่องหมายการจัดรูปแบบและตรรกะเชิงพื้นที่ (จุดจอมฟ้า/จุดต่ำสุด) ที่ถูกต้องตามหลักคณิตศาสตร์โดยอัตโนมัติ เครื่องมือนี้ช่วยให้สามารถสร้างเนื้อหาคุณภาพสูงที่พร้อมใช้งานสำหรับการแมป VR หรือเครื่องมือดูภาพแบบ 360 องศาได้

## ✨ คุณสมบัติ

- **Prompt Enhancement Loop**: แปลงคำสั่งง่ายๆ ของผู้ใช้ (เช่น "เมืองไซเบอร์พังค์ในตอนกลางคืน") ให้เป็นคำสั่งที่พร้อมใช้งานสำหรับ VR อย่างสมบูรณ์แบบ ซึ่งประกอบด้วยข้อกำหนดเกี่ยวกับจุดจอมฟ้า (zenith) จุดต่ำสุด (nadir) และเส้นขอบฟ้า
- **Automated QA Validation & Refinement**: ระบบ LLM QA ที่มาพร้อมกับตัวเครื่องมือจะตรวจสอบภาพที่สร้างขึ้นเพื่อให้แน่ใจว่าดูเหมือนภาพพาโนรามาที่ถูกต้อง หากการพยายามสร้างล้มเหลว ระบบจะส่งคำวิจารณ์กลับไปยังตัวสร้างภาพ และใช้ภาพที่ถูกปฏิเสธเป็นพื้นฐานสำหรับ **การปรับแต่งแบบ img2img (img2img refinement)** ในการพยายามครั้งต่อไป
- **Conditional Seamless Blending**: หลังจากสร้างภาพสำเร็จ เครื่องมือจะวิเคราะห์ภาพเพื่อหารอยต่อแนวตั้งด้านหลัง หากตรวจพบรอยต่อที่ชัดเจน ระบบจะใช้ AI inpainting และ alpha-blending ในการซ่อมแซมโดยอัตโนมัติ เพื่อให้มั่นใจได้ถึงการห่อหุ้มแบบ 360 องศาที่ไร้รอยต่ออย่างสมบูรณ์
- **Multimodal Reference Support**: สามารถระบุภาพในเครื่องเพื่อเป็นแนวทางในการสร้างภาพได้ (การถ่ายโอนสไตล์ การรวมตัวละคร หรือเค้าโครงพื้นฐาน)
- **Docker Ready**: ง่ายต่อการปรับใช้และรันในสภาพแวดล้อมที่แยกต่างหากโดยใช้ Docker Compose

## 🛠️ ข้อกำหนดเบื้องต้น

- **Python 3.12+** (หากรันในเครื่องของคุณเอง)
- **Docker** และ **Docker Compose** (แนะนำเพื่อให้ทำงานในสภาพแวดล้อมที่แยกต่างหาก)
- **Google Cloud API Key** ที่มีสิทธิ์การเข้าถึงโมเดล Gemini (รวมถึงความสามารถในการสร้างภาพ)

## 🚀 การติดตั้งและการตั้งค่า

### 1. โคลน Repository
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. กำหนดค่าสภาพแวดล้อม
คัดลอกไฟล์ตัวอย่างสภาพแวดล้อม (environment file) และเพิ่ม API key ของคุณ
```bash
cp .env.example .env
```
เปิด `.env` และตั้งค่าตัวแปรของคุณ:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. การรันด้วย Docker (แนะนำ)

สร้าง Docker image:
```bash
docker-compose build
```

รันคำสั่งเริ่มต้น:
```bash
docker-compose up
```

### 4. การรันในเครื่อง (Locally)

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

### การใช้งานผ่าน CLI ในเครื่อง

รันสคริปต์ `main.py` และระบุคำสั่ง (prompt):

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**การใช้ภาพอ้างอิง:**
หากคุณต้องการส่งภาพอ้างอิงเพื่อกำหนดสไตล์หรือบริบทของเนื้อหา ให้ใช้แฟล็ก `--image-refs`

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
คุณสามารถระบุภาพอ้างอิงหลายภาพได้โดยการใช้แฟล็กซ้ำ:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### การใช้งาน Docker Compose

หากคุณต้องการรันคำสั่ง CLI เฉพาะด้วย Docker คุณสามารถรัน:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(ตรวจสอบให้แน่ใจว่า path อ้างอิงใดๆ สามารถเข้าถึงได้ภายในคอนเทนเนอร์ ซึ่งโดยปกติแล้วทำได้โดยการเมาท์ (mounting) หรือวางไว้ในไดเรกทอรีโปรเจกต์ของคุณ)*

## 🏗️ สถาปัตยกรรม (Architecture)

โปรเจกต์นี้ประกอบด้วยส่วนประกอบหลัก 3 ส่วนภายใต้ `app/core`:
1. **PromptEnhancer**: สื่อสารกับโมเดลข้อความ (`TEXT_MODEL_NAME`) เพื่อขยายคำอธิบายสั้นๆ ของผู้ใช้ให้เป็นคำสั่ง VR ที่มีรายละเอียด
2. **GenAIClient**: ทำหน้าที่ครอบ (Wrap) SDK `google-genai` เพื่อจัดการกับการแยกวิเคราะห์โครงสร้างข้อมูลเอาต์พุต, การสร้างภาพแบบ multimodal (`IMAGE_MODEL_NAME`), และการตรวจสอบด้วยภาพของ QA (`VALIDATOR_MODEL_NAME`)
3. **Panoramist**: ตัวควบคุมการทำงาน (Orchestrator) ที่เชื่อมโยงการปรับปรุงคำสั่ง, การสร้างภาพ, และการทดลองทำซ้ำเพื่อตรวจสอบ ให้เป็นวงจรการทำงานเดียวกันอย่างสมบูรณ์

## 🧪 การพัฒนาและการทดสอบ

Unit tests เขียนขึ้นโดยใช้ `pytest` และ `pytest-mock` โปรเจกต์นี้ตั้งเป้าหมายเพื่อให้ครอบคลุมการทดสอบ (test coverage) แบบ 100%

**การใช้ Docker (แนะนำ):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**การใช้ Python Environment ในเครื่อง:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 สัญญาอนุญาต (License)

โปรเจกต์นี้อยู่ภายใต้สัญญาอนุญาต MIT - ดูรายละเอียดเพิ่มเติมได้ในไฟล์ [LICENSE](LICENSE)