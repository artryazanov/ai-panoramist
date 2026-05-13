> 🌐 **ภาษา:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** คือเครื่องมือ CLI ของ Python ที่ออกแบบมาเพื่อสร้างภาพพาโนรามา 360 องศาแบบ equirectangular ที่ไร้รอยต่อ โดยอาศัยความสามารถในการสร้างผลลัพธ์แบบ Multimodal ขั้นสูงและการปรับปรุงคำสั่ง (prompt-enhancement) ของ Google Gemini

ด้วยการใช้มาร์กเกอร์จัดรูปแบบและตรรกะเชิงพื้นที่ (จุดสูงสุด/จุดต่ำสุด หรือ zenith/nadir) ที่ถูกต้องตามหลักคณิตศาสตร์โดยอัตโนมัติ เครื่องมือนี้ช่วยให้สามารถสร้างภาพคุณภาพสูงที่พร้อมสำหรับนำไปใช้งานในการทำ VR mapping หรือโปรแกรมสำหรับดูภาพ 360 องศาได้ทันที

## 🖼️ ตัวอย่าง

![Cyberpunk Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/cyberpunk_example.jpg)
![Beach Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/beach_example.jpg)

> [!NOTE]
> ภาพพาโนรามาที่สร้างขึ้นอาจไม่ได้สมบูรณ์แบบทางคณิตศาสตร์ทั้งหมด อาจมีความผิดเพี้ยนเล็กน้อยหรือมีร่องรอยของการผสมภาพ (blending artifacts) อยู่บ้าง แต่ภาพรวมของผลลัพธ์ที่ได้ก็ยังคงน่าประทับใจเป็นอย่างมาก!

## ✨ คุณสมบัติ

- **วงจรการปรับปรุงคำสั่ง (Prompt Enhancement Loop)**: แปลงคำสั่งง่ายๆ ของผู้ใช้ (เช่น "เมืองไซเบอร์พังก์ยามค่ำคืน") ให้เป็นคำสั่งที่มีความละเอียดพร้อมสำหรับ VR ซึ่งรวมถึงข้อกำหนดเรื่องจุดสูงสุด (zenith) จุดต่ำสุด (nadir) และเส้นขอบฟ้า (horizon)
- **การตรวจสอบความถูกต้องและปรับปรุงอัตโนมัติ (Automated QA Validation & Refinement)**: ระบบตรวจสอบ QA ด้วย LLM ในตัวจะตรวจสอบภาพที่สร้างขึ้นเพื่อให้แน่ใจว่าดูเหมือนภาพพาโนรามาจริงๆ หากการสร้างภาพเกิดข้อผิดพลาด ระบบจะส่งข้อเสนอแนะกลับไปยังตัวสร้างเพื่อแก้ไขและสร้างภาพพาโนรามาที่ถูกต้องออกมาในการพยายามครั้งถัดไป
- **การผสมภาพไร้รอยต่อแบบมีเงื่อนไข (Conditional Seamless Blending)**: หลังจากการสร้างภาพเสร็จสมบูรณ์ เครื่องมือจะวิเคราะห์หาเส้นรอยต่อแนวตั้งที่ด้านหลังของภาพ หากพบรอยต่อที่เห็นได้ชัด ระบบจะนำเทคนิค AI inpainting และ alpha-blending มาซ่อมแซมโดยอัตโนมัติ เพื่อให้ภาพหมุนรอบทิศทาง 360 องศาได้อย่างไร้รอยต่อโดยสมบูรณ์
- **รองรับการอ้างอิงแบบ Multimodal**: สามารถส่งไฟล์รูปภาพภายในเครื่องเพื่อใช้เป็นแนวทางชี้นำการสร้างภาพ (ทั้งการถ่ายโอนสไตล์ภาพ การเพิ่มตัวละคร หรือการวางโครงสร้างฐาน) ได้
- **พร้อมใช้งานบน Docker**: ติดตั้งใช้งานและรันบนสภาพแวดล้อมที่ถูกแยกเป็นสัดส่วนได้อย่างง่ายดายผ่าน Docker Compose

## 🛠️ ข้อกำหนดเบื้องต้น

- **Python 3.12+** (หากเลือกรันบนเครื่องปกติ)
- **Docker** & **Docker Compose** (แนะนำสำหรับการแยกสภาพแวดล้อมให้เป็นสัดส่วน)
- **Google Cloud API Key** ที่มีสิทธิ์เข้าถึงโมเดล Gemini (รวมถึงความสามารถด้านการสร้างภาพ)

## 🚀 การติดตั้งและการตั้งค่า

### 1. โคลน Repository
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. กำหนดค่าสภาพแวดล้อม
คัดลอกไฟล์ environment ตัวอย่างแล้วเพิ่ม API key ของคุณลงไป
```bash
cp .env.example .env
```
เปิดไฟล์ `.env` และกำหนดค่าตัวแปร:
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

### 4. การรันบนเครื่องคอมพิวเตอร์ของคุณเอง (Locally)

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

### การใช้งาน CLI บนเครื่องแบบทั่วไป

รันสคริปต์ `main.py` พร้อมกำหนดคำสั่ง (prompt):

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**การใช้รูปภาพอ้างอิง:**
หากคุณต้องการส่งรูปภาพเพื่อกำหนดทิศทางของสไตล์หรือเนื้อหา ให้ใช้ flag `--image-refs`

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
คุณสามารถระบุรูปภาพอ้างอิงได้หลายๆ รูป โดยการระบุ flag นั้นซ้ำ:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### การใช้งานผ่าน Docker Compose

หากคุณต้องการรันคำสั่ง CLI บางคำสั่งผ่าน Docker สามารถรันได้ดังนี้:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(โปรดตรวจสอบให้แน่ใจว่าคอนเทนเนอร์สามารถเข้าถึง path ไฟล์อ้างอิงใดๆ ก็ตามที่คุณนำมาใช้ ซึ่งปกติจะทำโดยการเมานต์ไฟล์ หรือวางไฟล์ไว้ในไดเรกทอรีของโปรเจกต์คุณ)*

## 🏗️ สถาปัตยกรรม (Architecture)

โปรเจกต์นี้ประกอบไปด้วยส่วนสำคัญ 3 ส่วนภายใต้ `app/core`:
1. **PromptEnhancer**: ทำหน้าที่ติดต่อสื่อสารกับโมเดลภาษา (`TEXT_MODEL_NAME`) เพื่อนำคำอธิบายสั้นๆ ของผู้ใช้มาขยายความให้เป็นคำสั่งสำหรับ VR โดยละเอียด
2. **GenAIClient**: โค้ดส่วนที่ครอบการทำงานของ `google-genai` SDK ใช้จัดการการแปลงข้อมูลออกแบบมาเป็นโครงสร้าง (structured output) การสร้างภาพด้วยโมเดลภาพ (`IMAGE_MODEL_NAME`) และการตรวจสอบภาพด้วยตา (QA) ผ่านโมเดลวิเคราะห์ (`VALIDATOR_MODEL_NAME`)
3. **Panoramist**: ทำหน้าที่เสมือนศูนย์กลางควบคุมการทำงาน (Orchestrator) ที่จะคอยประสานระบบต่างๆ ทั้งการปรับปรุงข้อความ การสร้างภาพ และกระบวนการทำซ้ำเพื่อตรวจสอบความถูกต้องให้เป็นระบบที่เชื่อมต่อกันอย่างสอดคล้อง

## 🧪 การพัฒนาและการทดสอบ

Unit tests ในโปรเจกต์นี้เขียนโดยใช้ `pytest` และ `pytest-mock` ซึ่งมีเป้าหมายการครอบคลุมของเทส (test coverage) ไว้ที่ 100%

**การใช้งานผ่าน Docker (แนะนำ):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**การใช้งานผ่าน Local Python Environment:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 ลิขสิทธิ์

โปรเจกต์นี้เผยแพร่ภายใต้ลิขสิทธิ์ MIT License - สามารถดูรายละเอียดได้จากไฟล์ [LICENSE](LICENSE)