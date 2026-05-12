> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** — это консольная утилита (CLI) на Python, предназначенная для генерации бесшовных эквидистантных 360-градусных панорам с использованием передовых возможностей мультимодальной генерации и улучшения промптов Google Gemini.

За счет автоматического применения математически корректных маркеров форматирования и пространственной логики (зенит/надир), этот инструмент помогает создавать высококачественные ассеты, готовые к использованию в VR-маппинге или 360-градусных просмотрщиках.

## ✨ Возможности

- **Цикл улучшения промптов (Prompt Enhancement Loop)**: Преобразует простые пользовательские запросы (например, «Киберпанк-город ночью») в строгие промпты, готовые для VR, содержащие спецификации зенита, надира и горизонта.
- **Автоматическая проверка качества (QA) и доработка**: Встроенный LLM QA проверяет сгенерированные изображения на соответствие формату правильных панорам. В случае неудачи критика отправляется обратно генератору, а отклоненное изображение используется в качестве основы для **доработки в режиме img2img** при следующей попытке.
- **Условное бесшовное смешивание (Conditional Seamless Blending)**: После успешной генерации инструмент анализирует изображение на наличие вертикальных задних швов. Если обнаруживается грубый шов, он автоматически использует ИИ-инпейнтинг и альфа-смешивание для его исправления, обеспечивая идеально бесшовную 360-градусную развертку.
- **Поддержка мультимодальных референсов**: Предоставьте локальные изображения для направления генерации (перенос стиля, добавление персонажей или базовые макеты).
- **Поддержка Docker**: Легко развертывать и запускать в изолированной среде с помощью Docker Compose.

## 🛠️ Предварительные требования

- **Python 3.12+** (при локальном запуске)
- **Docker** и **Docker Compose** (рекомендуется для изоляции)
- **API-ключ Google Cloud** с доступом к моделям Gemini (включая возможности генерации изображений).

## 🚀 Установка и настройка

### 1. Клонирование репозитория
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. Настройка окружения
Скопируйте файл с примерами переменных окружения и добавьте свой API-ключ.
```bash
cp .env.example .env
```
Откройте файл `.env` и задайте ваши переменные:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Запуск через Docker (Рекомендуется)

Соберите Docker-образ:
```bash
docker-compose build
```

Запустите команду по умолчанию:
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

### Локальное использование CLI

Запустите скрипт `main.py` и передайте промпт:

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**Использование референсных изображений:**
Если вы хотите передать изображение для задания стиля или контекста, используйте флаг `--image-refs`.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
Вы можете передать несколько референсных изображений, повторив этот флаг:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### Использование Docker Compose

Если вы хотите выполнить определенные команды CLI через Docker, вы можете запустить:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(Убедитесь, что пути к референсам доступны внутри контейнера; обычно для этого их нужно примонтировать или поместить в директорию вашего проекта).*

## 🏗️ Архитектура

Проект состоит из трех основных компонентов в директории `app/core`:
1. **PromptEnhancer**: Взаимодействует с текстовой моделью (`TEXT_MODEL_NAME`) для расширения кратких пользовательских описаний в подробные VR-промпты.
2. **GenAIClient**: Является оберткой для SDK `google-genai`, обрабатывающей парсинг структурированного вывода, мультимодальную генерацию изображений (`IMAGE_MODEL_NAME`) и визуальную проверку качества (QA) (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: Оркестратор, который связывает улучшение промптов, генерацию и повторные попытки валидации в единый согласованный цикл.

## 🧪 Разработка и тестирование

Юнит-тесты написаны с использованием `pytest` и `pytest-mock`. Проект стремится к 100% покрытию тестами.

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

Этот проект лицензирован на условиях лицензии MIT — подробности см. в файле [LICENSE](LICENSE).