> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** هي أداة سطر أوامر (CLI) مبنية بلغة بايثون ومصممة لإنشاء صور بانورامية سلسة بزاوية 360 درجة متساوية المستطيلات باستخدام قدرات الإنشاء المتقدم متعدد الوسائط وتحسين التلقين (prompt) الخاصة بـ Google Gemini.

من خلال التطبيق التلقائي لعلامات التنسيق الصحيحة رياضيًا والمنطق المكاني (السمت/النظير)، تساعد هذه الأداة في إنشاء أصول عالية الجودة جاهزة للاستخدام في تخطيط الواقع الافتراضي (VR) أو عارضات الـ 360 درجة.

## ✨ الميزات

- **حلقة تحسين التلقين (Prompt Enhancement Loop)**: تحول مطالبات المستخدم البسيطة (مثل، "مدينة سيبربانك في الليل") إلى مطالبات دقيقة وجاهزة للواقع الافتراضي (VR) تحتوي على مواصفات السمت (zenith)، النظير (nadir)، والأفق (horizon).
- **التحقق التلقائي من الجودة والتحسين**: يقوم نموذج اللغة الكبير (LLM) المدمج الخاص بضمان الجودة بفحص الصور المنشأة للتأكد من أنها تبدو كصور بانورامية صحيحة. إذا فشلت المحاولة، فإنه يعيد تغذية الملاحظات إلى المولد ويستخدم الصورة المرفوضة كأساس لـ **تحسين الصورة إلى صورة (img2img)** في المحاولة التالية.
- **الدمج السلس المشروط**: بعد الإنشاء الناجح، تحلل الأداة الصورة بحثًا عن أي خطوط فاصلة (seams) عمودية في الخلف. إذا تم اكتشاف خط فاصل حاد، فإنها تستخدم تلقائيًا الرسم الداخلي بالذكاء الاصطناعي (AI inpainting) ودمج ألفا (alpha-blending) لإصلاحه، مما يضمن التفافًا سلسًا ومثاليًا بزاوية 360 درجة.
- **دعم المراجع متعددة الوسائط**: يمكنك تقديم صور محلية لتوجيه عملية الإنشاء (نقل النمط، أو تضمين الشخصيات، أو التخطيطات الأساسية).
- **جاهز للعمل على Docker**: سهولة النشر والتشغيل في بيئة معزولة باستخدام Docker Compose.

## 🛠️ المتطلبات الأساسية

- **Python 3.12+** (إذا كنت تقوم بالتشغيل محليًا)
- **Docker** و **Docker Compose** (موصى بهما للعزل)
- **مفتاح واجهة برمجة تطبيقات Google Cloud (API Key)** مع إمكانية الوصول إلى نماذج Gemini (بما في ذلك قدرات إنشاء الصور).

## 🚀 التثبيت والإعداد

### 1. استنساخ المستودع
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. تكوين البيئة
انسخ ملف البيئة التجريبي وأضف مفتاح API الخاص بك.
```bash
cp .env.example .env
```
افتح `.env` وعيِّن المتغيرات الخاصة بك:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. التشغيل باستخدام Docker (موصى به)

بناء صورة Docker:
```bash
docker-compose build
```

تشغيل الأمر الافتراضي:
```bash
docker-compose up
```

### 4. التشغيل محليًا

إنشاء بيئة افتراضية:
```bash
python -m venv venv
source venv/bin/activate
```

تثبيت التبعيات:
```bash
pip install -r requirements.txt
```

## 💡 الاستخدام

### استخدام واجهة سطر الأوامر (CLI) محليًا

قم بتشغيل السكربت `main.py` وقدم التلقين (prompt):

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**استخدام الصور المرجعية:**
إذا كنت تريد تمرير صورة كسياق للنمط أو المحتوى، فاستخدم العلامة `--image-refs`.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
يمكنك تمرير صور مرجعية متعددة عن طريق تكرار العلامة:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### استخدام Docker Compose

إذا كنت ترغب في تشغيل أوامر CLI معينة باستخدام Docker، يمكنك تنفيذ:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(تأكد من إمكانية الوصول إلى أي مسارات مرجعية داخل الحاوية، عادةً عن طريق عمل mount لها أو وضعها في دليل مشروعك).*

## 🏗️ البنية (Architecture)

يتكون المشروع من ثلاثة مكونات رئيسية تحت `app/core`:
1. **PromptEnhancer** (مُحسِّن التلقين): يتواصل مع النموذج النصي (`TEXT_MODEL_NAME`) لتوسيع الأوصاف القصيرة للمستخدمين إلى مطالبات VR مفصلة.
2. **GenAIClient**: يغلف حزمة تطوير البرمجيات `google-genai` (SDK) للتعامل مع تحليل المخرجات المنظمة، وإنشاء الصور متعددة الوسائط (`IMAGE_MODEL_NAME`)، والفحص المرئي لضمان الجودة (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: المنسق الذي يربط محاولات التحسين، والإنشاء، والتحقق معًا في حلقة واحدة متماسكة.

## 🧪 التطوير والاختبار

تم كتابة اختبارات الوحدة (Unit tests) باستخدام `pytest` و `pytest-mock`. يهدف المشروع إلى تحقيق تغطية اختبار بنسبة 100%.

**باستخدام Docker (موصى به):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**باستخدام بيئة بايثون المحلية:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 الترخيص

هذا المشروع مرخص بموجب ترخيص MIT - راجع ملف [LICENSE](LICENSE) للحصول على التفاصيل.