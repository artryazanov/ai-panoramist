import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Models
    TEXT_MODEL_NAME = os.getenv("TEXT_MODEL_NAME", "gemini-3.1-pro-preview")
    IMAGE_MODEL_NAME = os.getenv("IMAGE_MODEL_NAME", "gemini-3.1-flash-image-preview")
    VALIDATOR_MODEL_NAME = os.getenv("VALIDATOR_MODEL_NAME", "gemini-3.1-pro-preview")

    # Generation settings
    IMAGE_ASPECT_RATIO = os.getenv("IMAGE_ASPECT_RATIO", "16:9")
    IMAGE_RESOLUTION = os.getenv("IMAGE_RESOLUTION", "4K")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

    @staticmethod
    def validate():
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

def setup_directories(base_path: Path):
    """Ensure output directories exist."""
    base_path.mkdir(parents=True, exist_ok=True)
