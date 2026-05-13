> 🌐 **Idiomas:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** es una herramienta CLI de Python diseñada para generar panoramas de 360 grados equirrectangulares y sin interrupciones (seamless) utilizando la generación multimodal avanzada y las capacidades de mejora de prompts de Google Gemini.

Al aplicar automáticamente los marcadores de formato matemáticamente correctos y la lógica espacial (cenit/nadir), esta herramienta ayuda a generar recursos de alta calidad listos para su uso en mapeo de RV (Realidad Virtual) o visores de 360 grados.

## 🖼️ Ejemplos

![Cyberpunk Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/cyberpunk_example.jpg)
![Beach Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/beach_example.jpg)

## ✨ Características

- **Bucle de Mejora de Prompts**: Convierte prompts simples del usuario (por ejemplo, "Una ciudad cyberpunk de noche") en prompts rigurosos listos para RV que contienen especificaciones de cenit, nadir y horizonte.
- **Validación y Refinamiento Automatizado (QA)**: El control de calidad (QA) con LLM integrado verifica las imágenes generadas para garantizar que parezcan panoramas adecuados. Si un intento falla, retroalimenta la crítica al generador para producir un panorama corregido en el siguiente intento.
- **Mezcla Continua Condicional (Seamless Blending)**: Después de una generación exitosa, la herramienta analiza la imagen en busca de uniones o cortes verticales en la parte posterior. Si se detecta un corte pronunciado, utiliza automáticamente inpainting por IA y mezcla alfa (alpha-blending) para repararlo, asegurando un panorama envolvente de 360 grados perfectamente continuo.
- **Soporte de Referencias Multimodales**: Proporciona imágenes locales para guiar la generación (transferencia de estilo, inclusión de personajes o diseños base).
- **Listo para Docker**: Fácil de desplegar y ejecutar en un entorno aislado utilizando Docker Compose.

## 🛠️ Requisitos previos

- **Python 3.12+** (si se ejecuta localmente)
- **Docker** y **Docker Compose** (recomendado para aislamiento)
- **Clave de API de Google Cloud** con acceso a los modelos de Gemini (incluyendo capacidades de generación de imágenes).

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone git@github.com:artryazanov/ai-panoramist.git
cd ai-panoramist
```

### 2. Configurar el Entorno
Copia el archivo de entorno de ejemplo y añade tu clave de API.
```bash
cp .env.example .env
```
Abre `.env` y configura tus variables:
```ini
GEMINI_API_KEY=tu_clave_de_api_aqui
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

### 4. Ejecutar Localmente

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

### Usar la CLI Localmente

Ejecuta el script `main.py` y proporciona un prompt:

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**Uso de Imágenes de Referencia:**
Si deseas pasar una imagen para dar contexto de estilo o contenido, utiliza la bandera `--image-refs`.

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
*(Asegúrate de que cualquier ruta de referencia sea accesible dentro del contenedor, típicamente montándolas o colocándolas en el directorio de tu proyecto).*

## 🏗️ Arquitectura

El proyecto consta de tres componentes principales bajo `app/core`:
1. **PromptEnhancer**: Se comunica con el modelo de texto (`TEXT_MODEL_NAME`) para expandir descripciones cortas del usuario en prompts detallados para RV.
2. **GenAIClient**: Envuelve el SDK de `google-genai` para manejar el análisis de salida estructurada, la generación de imágenes multimodales (`IMAGE_MODEL_NAME`) y la inspección visual de control de calidad (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: El orquestador que enlaza los reintentos de mejora, generación y validación en un ciclo cohesivo.

## 🧪 Desarrollo y Pruebas

Las pruebas unitarias están escritas usando `pytest` y `pytest-mock`. El proyecto tiene como objetivo una cobertura de pruebas del 100%.

**Usando Docker (Recomendado):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**Usando el Entorno Python Local:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.