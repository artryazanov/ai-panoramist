> 🌐 **Idiomas:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** es una herramienta de línea de comandos (CLI) en Python diseñada para generar panorámicas de 360 grados equirectangulares y sin costuras utilizando las capacidades avanzadas de generación multimodal y mejora de prompts de Google Gemini.

Al aplicar automáticamente los marcadores de formato y la lógica espacial matemáticamente correctos (cénit/nadir), esta herramienta ayuda a generar recursos de alta calidad listos para usarse en mapeo de realidad virtual (VR) o visores de 360 grados.

## ✨ Características

- **Bucle de mejora de prompts**: Convierte instrucciones sencillas del usuario (por ejemplo, "Una ciudad ciberpunk de noche") en descripciones rigurosas listas para VR que contienen especificaciones de cénit, nadir y horizonte.
- **Validación y refinamiento automatizados de control de calidad (QA)**: El control de calidad integrado por LLM comprueba las imágenes generadas para asegurar que luzcan como panorámicas adecuadas. Si un intento falla, retroalimenta la crítica al generador y utiliza la imagen rechazada como base para un **refinamiento img2img** en el siguiente intento.
- **Fusión perfecta condicional**: Después de una generación exitosa, la herramienta analiza la imagen en busca de costuras verticales en la parte posterior. Si se detecta una costura grave, utiliza automáticamente inpainting por IA y mezcla alfa para repararla, garantizando un entorno de 360 grados perfectamente continuo y sin uniones visibles.
- **Soporte de referencia multimodal**: Proporciona imágenes locales para guiar la generación (transferencia de estilo, inclusión de personajes o diseños base).
- **Listo para Docker**: Fácil de desplegar y ejecutar en un entorno aislado usando Docker Compose.

## 🛠️ Requisitos previos

- **Python 3.12+** (si se ejecuta localmente)
- **Docker** y **Docker Compose** (recomendado para aislamiento)
- **Clave de API de Google Cloud** con acceso a los modelos de Gemini (incluidas las capacidades de generación de imágenes).

## 🚀 Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. Configurar el entorno
Copia el archivo de entorno de ejemplo y añade tu clave de API.
```bash
cp .env.example .env
```
Abre `.env` y configura tus variables:
```ini
GEMINI_API_KEY=tu_clave_de_api_real_aqui
```

### 3. Ejecutar con Docker (Recomendado)

Construye la imagen de Docker:
```bash
docker-compose build
```

Ejecuta el comando por defecto:
```bash
docker-compose up
```

### 4. Ejecutar localmente

Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate
```

Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 💡 Uso

### Usar la CLI localmente

Ejecuta el script `main.py` y proporciona un prompt (instrucción):

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**Uso de imágenes de referencia:**
Si deseas pasar una imagen para contexto de estilo o contenido, usa la bandera `--image-refs`.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
Puedes pasar múltiples imágenes de referencia repitiendo la bandera:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### Usar Docker Compose

Si deseas ejecutar comandos específicos de la CLI usando Docker, puedes ejecutar:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(Asegúrate de que las rutas de referencia sean accesibles dentro del contenedor, normalmente montándolas o colocándolas en el directorio de tu proyecto).*

## 🏗️ Arquitectura

El proyecto consta de tres componentes principales bajo `app/core`:
1. **PromptEnhancer**: Se comunica con el modelo de texto (`TEXT_MODEL_NAME`) para expandir descripciones cortas del usuario en prompts detallados para VR.
2. **GenAIClient**: Envuelve el SDK de `google-genai` para manejar el análisis de salidas estructuradas, la generación de imágenes multimodales (`IMAGE_MODEL_NAME`) y la inspección visual de control de calidad (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: El orquestador que une la mejora, la generación y los reintentos de validación en un ciclo cohesivo.

## 🧪 Desarrollo y pruebas

Las pruebas unitarias están escritas usando `pytest` y `pytest-mock`. El proyecto tiene como objetivo alcanzar el 100% de cobertura de pruebas.

**Usar Docker (Recomendado):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**Usar entorno local de Python:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.