> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** هي أداة سطر أوامر (CLI) بلغة بايثون مُصممة لإنشاء صور بانورامية سلسة بزاوية 360 درجة متساوية المستطيلات (equirectangular) باستخدام قدرات Google Gemini المتقدمة في التوليد متعدد الوسائط وتحسين التلقين.

من خلال التطبيق التلقائي لعلامات التنسيق الصحيحة رياضيًا والمنطق المكاني (السمت/النظير - zenith/nadir)، تساعد هذه الأداة في توليد أصول عالية الجودة جاهزة للاستخدام في خرائط الواقع الافتراضي (VR) أو عارضات الـ 360 درجة.

## 🖼️ الأمثلة

![Cyberpunk Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/cyberpunk_example.jpg)
![Beach Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/beach_example.jpg)

> [!NOTE]
> الصور البانورامية المُولّدة ليست مثالية رياضيًا. قد تحتوي على تشوهات طفيفة أو عيوب في دمج الألوان، ولكن النتيجة المرئية الإجمالية تظل مثيرة للإعجاب!

## ✨ الميزات

- **حلقة تحسين التلقين (Prompt Enhancement Loop)**: تحويل مطالبات المستخدم البسيطة (مثل: "مدينة سايبربانك في الليل") إلى مطالبات دقيقة وجاهزة للواقع الافتراضي (VR) تحتوي على مواصفات السمت (zenith)، النظير (nadir)، والأفق.
- **التحقق الآلي لضمان الجودة والتحسين (Automated QA Validation & Refinement)**: يقوم نموذج اللغة الكبير (LLM) المدمج لضمان الجودة بفحص الصور المُولّدة للتأكد من أنها تبدو كصور بانورامية صحيحة. وفي حال فشل المحاولة، يقوم بتغذية الملاحظات النقدية مرة أخرى إلى المُولّد لإنتاج صورة بانورامية مُصححة في المحاولة التالية.
- **الدمج السلس المشروط (Conditional Seamless Blending)**: بعد نجاح عملية التوليد، تحلل الأداة الصورة بحثًا عن أي فواصل أو لحامات خلفية رأسية. إذا تم اكتشاف لحام واضح، فإنها تستخدم تلقائيًا تقنيات الرسم الداخلي بالذكاء الاصطناعي (AI inpainting) ودمج ألفا (alpha-blending) لإصلاحه، مما يضمن التفافًا مثاليًا وسلسًا بزاوية 360 درجة.
- **دعم المراجع متعددة الوسائط**: يمكنك توفير صور محلية لتوجيه عملية التوليد (نقل النمط، أو تضمين الشخصيات، أو التخطيطات الأساسية).
- **جاهزية Docker**: سهولة النشر والتشغيل في بيئة معزولة باستخدام Docker Compose.

## 🛠️ المتطلبات الأساسية

- **Python 3.12+** (في حال التشغيل محليًا)
- **Docker** و **Docker Compose** (يُوصى بهما للعزل)
- **مفتاح واجهة برمجة تطبيقات Google Cloud (API Key)** مع صلاحية الوصول إلى نماذج Gemini (بما في ذلك قدرات توليد الصور).

## 🚀 التثبيت والإعداد

### 1. استنساخ المستودع
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. إعداد البيئة
انسخ ملف البيئة كمثال وأضف مفتاح API الخاص بك.
```bash
cp .env.example .env
```
افتح ملف `.env` وقم بتعيين المتغيرات الخاصة بك:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. التشغيل باستخدام Docker (مُستحسن)

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

### استخدام سطر الأوامر (CLI) محليًا

قم بتشغيل سكربت `main.py` مع توفير تلقين (prompt):

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**استخدام الصور المرجعية:**
إذا كنت ترغب في تمرير صورة كسياق للنمط أو المحتوى، فاستخدم العلامة `--image-refs`.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
يمكنك تمرير صور مرجعية متعددة عن طريق تكرار العلامة:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### استخدام Docker Compose

إذا كنت ترغب في تشغيل أوامر CLI محددة باستخدام Docker، فيمكنك تشغيل:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(تأكد من إمكانية الوصول إلى أي مسارات مرجعية داخل الحاوية، عادةً عن طريق عمل mount لها أو وضعها في مجلد مشروعك).*

## 🏗️ البنية (Architecture)

يتكون المشروع من ثلاثة مكونات رئيسية ضمن `app/core`:
1. **مُحسن التلقين (PromptEnhancer)**: يتواصل مع النموذج النصي (`TEXT_MODEL_NAME`) لتوسيع وصف المستخدم القصير إلى مطالبات VR مُفصلة.
2. **عميل الذكاء الاصطناعي التوليدي (GenAIClient)**: يعمل كغلاف (Wrapper) لحزمة `google-genai` SDK للتعامل مع تحليل المخرجات المهيكلة، وتوليد الصور متعددة الوسائط (`IMAGE_MODEL_NAME`)، والفحص البصري لضمان الجودة (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: المنسق الذي يربط بين التحسين، والتوليد، ومحاولات التحقق في حلقة واحدة متماسكة.

## 🧪 التطوير والاختبار

تمت كتابة اختبارات الوحدة باستخدام `pytest` و `pytest-mock`. يهدف المشروع إلى تحقيق تغطية اختبارية بنسبة 100%.

**استخدام Docker (مُستحسن):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**استخدام بيئة بايثون المحلية:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 الترخيص

هذا المشروع مُرخص بموجب ترخيص MIT - راجع ملف [الترخيص (LICENSE)](LICENSE) للحصول على التفاصيل.