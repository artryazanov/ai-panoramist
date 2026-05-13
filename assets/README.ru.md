> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** — это CLI-утилита на Python, предназначенная для генерации бесшовных эквидистантных 360-градусных панорам с использованием передовых возможностей мультимодальной генерации и улучшения промптов (подсказок) от Google Gemini.

Автоматически применяя математически точные маркеры форматирования и пространственную логику (зенит/надир), этот инструмент помогает создавать высококачественные ассеты, готовые к использованию в VR-маппинге или 360-градусных просмотрщиках.

## 🖼️ Примеры

![Cyberpunk Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/cyberpunk_example.jpg)
![Beach Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/beach_example.jpg)

> [!NOTE]
> Сгенерированные панорамы не являются математически идеальными. Они могут содержать незначительные искажения или артефакты склейки, но в целом визуальный результат всё равно выглядит весьма впечатляюще!

## ✨ Возможности

- **Цикл улучшения промптов**: Преобразует простые пользовательские запросы (например, "Киберпанк-город ночью") в строгие VR-промпты, содержащие спецификации зенита, надира и горизонта.
- **Автоматическая QA-проверка и доработка**: Встроенная LLM-проверка качества анализирует сгенерированные изображения, чтобы убедиться, что они выглядят как правильные панорамы. Если попытка неудачна, критика возвращается генератору для создания исправленной панорамы при следующей попытке.
- **Условное бесшовное смешивание**: После успешной генерации инструмент анализирует изображение на наличие вертикальных задних швов. Если обнаружен грубый шов, он автоматически использует AI-инпейнтинг и альфа-смешивание для его устранения, обеспечивая идеальное бесшовное 360-градусное замыкание.
- **Поддержка мультимодальных референсов**: Возможность передачи локальных изображений для направления генерации (перенос стиля, добавление персонажей или базовых компоновок).
- **Готовность к Docker**: Легко развернуть и запустить в изолированной среде с использованием Docker Compose.

## 🛠️ Требования

- **Python 3.12+** (при локальном запуске)
- **Docker** и **Docker Compose** (рекомендуется для изоляции)
- **Google Cloud API Key** с доступом к моделям Gemini (включая возможности генерации изображений).

## 🚀 Установка и настройка

### 1. Клонирование репозитория
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. Настройка окружения
Скопируйте пример файла окружения и добавьте свой API-ключ.
```bash
cp .env.example .env
```
Откройте `.env` и задайте ваши переменные:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Запуск с помощью Docker (Рекомендуется)

Сборка Docker-образа:
```bash
docker-compose build
```

Запуск команды по умолчанию:
```bash
docker-compose up
```

### 4. Локальный запуск

Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate
```

Установите зависимости:
```bash
pip install -r requirements.txt
```

## 💡 Использование

### Использование CLI локально

Запустите скрипт `main.py` и укажите промпт:

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**Использование референсных изображений:**
Если вы хотите передать изображение для контекста стиля или контента, используйте флаг `--image-refs`.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
Вы можете передать несколько референсных изображений, повторив этот флаг:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### Использование Docker Compose

Если вы хотите выполнять специфичные CLI-команды с помощью Docker, вы можете запустить:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(Убедитесь, что пути к референсам доступны внутри контейнера, как правило, монтируя их или помещая в каталог вашего проекта).*

## 🏗️ Архитектура

Проект состоит из трех основных компонентов в директории `app/core`:
1. **PromptEnhancer**: Взаимодействует с текстовой моделью (`TEXT_MODEL_NAME`) для расширения коротких пользовательских описаний в подробные VR-промпты.
2. **GenAIClient**: Обертка над `google-genai` SDK для обработки парсинга структурированных данных, мультимодальной генерации изображений (`IMAGE_MODEL_NAME`) и визуальной QA-проверки (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: Оркестратор, который связывает воедино процессы улучшения, генерации и повторных попыток после валидации в единый целостный цикл.

## 🧪 Разработка и тестирование

Unit-тесты написаны с использованием `pytest` и `pytest-mock`. Проект стремится к 100% покрытию тестами.

**Использование Docker (Рекомендуется):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**Использование локального Python-окружения:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 Лицензия

Этот проект распространяется под лицензией MIT — подробнее см. в файле [LICENSE](LICENSE).