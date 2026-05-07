# AI Panoramist

**AI Panoramist** is a Python CLI tool designed to generate seamless, equirectangular 360-degree panoramas using Google Gemini's advanced multimodal generation and prompt-enhancement capabilities.

By automatically applying the mathematically correct formatting markers and spatial logic (zenith/nadir), this tool helps generate high-quality assets ready for use in VR mapping or 360-degree viewers.

## Features

- **Prompt Enhancement Loop**: Converts simple user prompts (e.g., "A cyberpunk city at night") into rigorous VR-ready prompts containing zenith, nadir, and horizon specifications.
- **Automated QA Validation**: The built-in LLM QA checks generated images to ensure they look like proper panoramas. If an attempt fails, it feeds the critique back to the generator for a better next attempt.
- **Multimodal Reference Support**: Provide local images to guide the generation (style transfer, character inclusion, or base layouts).
- **Docker Ready**: Easy to deploy and run in an isolated environment using Docker Compose.

---

## Installation

### Option 1: Local Python Environment

1. Clone the repository and set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API key:
   - Copy `.env.example` to `.env`
   - Add your Google Gemini API key:
     ```env
     GEMINI_API_KEY=your_actual_api_key_here
     ```

### Option 2: Docker

1. Ensure Docker and Docker Compose are installed.
2. Copy `.env.example` to `.env` and fill in your `GEMINI_API_KEY`.
3. Build and run the default command:
   ```bash
   docker-compose build
   docker-compose up
   ```

---

## Usage

### Using the CLI Locally

Run the `main.py` script and provide a prompt:

```bash
python main.py --prompt "A futuristic space station interior" --output-dir ./panoramas
```

**Using Reference Images:**
If you want to pass an image for style or content context, use the `--image-refs` flag.

```bash
python main.py --prompt "A magical forest in the style of this image" --image-refs ./style.jpg --output-dir ./panoramas
```
You can pass multiple reference images by repeating the flag:
```bash
python main.py --prompt "Include these two characters in an ancient ruin panorama" --image-refs ./char1.png --image-refs ./char2.png
```

### Using Docker Compose

If you want to run specific CLI commands using Docker, you can run:

```bash
docker-compose run --rm panoramist --prompt "A sunny beach panorama" --image-refs ./references/sun.jpg
```
*(Ensure any reference paths are accessible inside the container, typically by mounting them or placing them in your project directory).*

## Architecture

The project consists of three main components under `app/core`:
1. **PromptEnhancer**: Communicates with the text model (`TEXT_MODEL_NAME`) to expand short user descriptions into detailed VR prompts.
2. **GenAIClient**: Wraps the `google-genai` SDK to handle structured output parsing, multimodal image generation (`IMAGE_MODEL_NAME`), and the QA visual inspection (`VALIDATOR_MODEL_NAME`).
3. **Panoramist**: The orchestrator that ties enhancement, generation, and validation retries together into one cohesive loop.

## Running Tests

Unit tests are written using `pytest` and `pytest-mock`. To run the tests locally:

```bash
source venv/bin/activate
pytest --cov=app tests/
```
