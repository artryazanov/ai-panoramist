> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** — это CLI-инструмент на Python, предназначенный для создания бесшовных эквидистантных 360-градусных панорам с использованием передовых возможностей мультимодальной генерации и улучшения промптов Google Gemini.

Автоматически применяя математически точные маркеры форматирования и пространственную логику (зенит/надир), этот инструмент помогает создавать высококачественные ассеты, готовые к использованию в VR-маппинге или 360-градусных просмотрщиках.

## 🖼️ Примеры

![Cyberpunk Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/cyberpunk_example.jpg)
![Beach Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/beach_example.jpg)

## ✨ Возможности

- **Цикл улучшения промпта**: Преобразует простые пользовательские запросы (например, «Киберпанк-город ночью») в строгие VR-совместимые промпты, содержащие спецификации зенита, надира и горизонта.
- **Автоматизированная проверка качества (QA) и доработка**: Встроенная проверка качества на базе LLM анализирует сгенерированные изображения, чтобы убедиться, что они выглядят как правильные панорамы. Если попытка неудачна, критика передается обратно генератору для создания исправленной панорамы при следующей попытке.
- **Условное бесшовное смешивание**: После успешной генерации инструмент анализирует изображение на наличие вертикальных швов на стыке. Если обнаруживается грубый шов, он автоматически использует ИИ-инпейтинг и альфа-смешивание для его устранения, обеспечивая идеальное бесшовное 360-градусное замыкание.
- **Поддержка мультимодальных референсов**: Возможность использовать локальные изображения для управления генерацией (перенос стиля, добавление персонажей или базовых планировок).
- **Поддержка Docker**: Легко развернуть и запустить в изолированной среде с помощью Docker Compose.

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
Скопируйте пример файла окружения и добавьте ваш API-ключ.
```bash
cp .env.example .env
```
Откройте `.env` и задайте ваши переменные:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Запуск с помощью Docker (рекомендуется)

Сборка Docker-образа:
```bash
docker-compose build
```

Запуск команды по умолчанию:
```bash
docker-compose up
```

### 4. Локальный запуск

Создание виртуального окружения:
```bash
python -m venv venv
source venv/bin/activate
```

Установка зависимостей:
```bash
pip install -r requirements.txt
```

## 💡 Использование

### Локальное использование CLI

Запустите скрипт `main.py` и укажите промпт:

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**Использование референсных изображений:**
Если вы хотите передать изображение для контекста стиля или контента, используйте флаг `--image-refs`.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
Вы можете передать несколько референсных изображений, повторяя этот флаг:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### Использование Docker Compose

Если вы хотите запустить определенные CLI-команды с помощью Docker, вы можете выполнить:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(Убедитесь, что любые пути к референсам доступны внутри контейнера; обычно это делается путем их монтирования или размещения в директории вашего проекта).*

## 🏗️ Архитектура

Проект состоит из трех основных компонентов в директории `app/core`:
1. **PromptEnhancer**: Взаимодействует с текстовой моделью (`TEXT_MODEL_NAME`) для расширения коротких пользовательских описаний до подробных VR-промптов.
2. **GenAIClient**: Обертка над SDK `google-genai` для обработки структурированного вывода, мультимодальной генерации изображений (`IMAGE_MODEL_NAME`) и визуальной проверки качества (QA) (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: Оркестратор, который объединяет процессы улучшения, генерации и повторные попытки валидации в единый связный цикл.

## 🧪 Разработка и тестирование

Юнит-тесты написаны с использованием `pytest` и `pytest-mock`. Цель проекта — 100% покрытие тестами.

**Использование Docker (рекомендуется):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**Использование локального Python-окружения:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 Лицензия

Этот проект распространяется по лицензии MIT — подробности см. в файле [LICENSE](LICENSE).