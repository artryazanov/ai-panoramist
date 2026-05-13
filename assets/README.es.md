> 🌐 **Idiomas:** [English](https://github.com/artryazanov/ai-panoramist/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-panoramist/blob/main/assets/README.ar.md)

# AI Panoramist

[![Tests](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-panoramist/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-panoramist/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-panoramist)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Panoramist** es una herramienta CLI de Python diseñada para generar panoramas continuos y equirrectangulares de 360 grados utilizando la generación multimodal avanzada y las capacidades de mejora de *prompts* de Google Gemini.

Al aplicar automáticamente los marcadores de formato matemáticamente correctos y la lógica espacial (cenit/nadir), esta herramienta ayuda a generar recursos de alta calidad listos para usarse en mapeo de realidad virtual (VR) o visores de 360 grados.

## 🖼️ Ejemplos

![Cyberpunk Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/cyberpunk_example.jpg)
![Beach Example](https://raw.githubusercontent.com/artryazanov/ai-panoramist/main/assets/beach_example.jpg)

> [!NOTE]
> Los panoramas generados no son matemáticamente perfectos. Pueden contener distorsiones menores o artefactos de fusión, ¡pero el resultado visual general sigue siendo bastante impresionante!

## ✨ Características

- **Bucle de mejora de prompts**: Convierte indicaciones o *prompts* sencillos del usuario (por ejemplo, "Una ciudad ciberpunk de noche") en *prompts* rigurosos listos para realidad virtual que contienen especificaciones de cenit, nadir y horizonte.
- **Validación y refinamiento automático de control de calidad (QA)**: El control de calidad integrado por LLM revisa las imágenes generadas para asegurar que se vean como panoramas adecuados. Si un intento falla, retroalimenta la crítica al generador para producir un panorama corregido en el siguiente intento.
- **Fusión continua condicional**: Después de una generación exitosa, la herramienta analiza la imagen en busca de costuras verticales en la parte posterior. Si se detecta una costura grave, utiliza automáticamente *inpainting* con IA y fusión alfa (*alpha-blending*) para repararla, asegurando un entorno de 360 grados perfectamente continuo sin interrupciones.
- **Soporte de referencias multimodales**: Proporciona imágenes locales para guiar la generación (transferencia de estilo, inclusión de personajes o diseños base).
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
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Ejecución con Docker (Recomendado)

Construye la imagen de Docker:
```bash
docker-compose build
```

Ejecuta el comando predeterminado:
```bash
docker-compose up
```

### 4. Ejecución local

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

### Usando la CLI localmente

Ejecuta el script `main.py` y proporciona un *prompt*:

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**Uso de imágenes de referencia:**
Si deseas pasar una imagen para darle contexto al estilo o al contenido, usa la bandera `--image-refs`.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
Puedes pasar múltiples imágenes de referencia repitiendo la bandera:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### Usando Docker Compose

Si deseas ejecutar comandos CLI específicos usando Docker, puedes ejecutar:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(Asegúrate de que cualquier ruta de referencia sea accesible dentro del contenedor, normalmente montándolas o colocándolas en el directorio de tu proyecto).*

## 🏗️ Arquitectura

El proyecto consta de tres componentes principales bajo `app/core`:
1. **PromptEnhancer**: Se comunica con el modelo de texto (`TEXT_MODEL_NAME`) para expandir descripciones breves del usuario en *prompts* detallados de realidad virtual (VR).
2. **GenAIClient**: Envuelve el SDK `google-genai` para manejar el análisis de salida estructurada, la generación de imágenes multimodales (`IMAGE_MODEL_NAME`) y la inspección visual de control de calidad (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: El orquestador que une la mejora, la generación y los reintentos de validación en un único bucle cohesivo.

## 🧪 Desarrollo y pruebas

Las pruebas unitarias están escritas usando `pytest` y `pytest-mock`. El proyecto tiene como objetivo un 100% de cobertura de pruebas.

**Usando Docker (Recomendado):**
```bash
docker-compose run --rm --entrypoint "pytest --cov=app tests/" panoramist
```

**Usando un entorno local de Python:**
```bash
source venv/bin/activate
pytest --cov=app tests/
```

## 📜 Licencia

Este proyecto está licenciado bajo la Licencia MIT; consulta el archivo [LICENSE](LICENSE) para más detalles.