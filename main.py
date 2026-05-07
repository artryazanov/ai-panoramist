import click
import logging
from pathlib import Path
from dotenv import load_dotenv

from app.config import Config, setup_directories
from app.core.panoramist import Panoramist

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@click.command()
@click.option('--prompt', required=True, type=str, help='A descriptive prompt for the panorama (e.g., "A cyberpunk city at night").')
@click.option('--image-refs', multiple=True, type=click.Path(exists=True), help='Optional paths to reference images. Can be used for style, character reference, or base photos.')
@click.option('--output-dir', default="output", help='Directory to save results.')
def main(prompt, image_refs, output_dir):
    """
    Generates seamless, equirectangular 360-degree panoramas using Gemini.
    """
    # 1. Config & Setup
    load_dotenv()
    try:
        Config.validate()
    except ValueError as e:
        logger.error(str(e))
        return

    output_path = Path(output_dir)
    setup_directories(output_path)

    # Convert tuple to list for consistency
    reference_images = list(image_refs)

    logger.info(f"Starting generation for prompt: '{prompt}'")
    if reference_images:
        logger.info(f"Using {len(reference_images)} reference images: {reference_images}")

    # 2. Initialize and Run Orchestrator
    try:
        panoramist = Panoramist(output_path)
        final_image_path = panoramist.generate_panorama(prompt, reference_images)
        logger.info(f"Success! Panorama saved to {final_image_path}")
    except Exception as e:
        logger.error(f"Failed to generate panorama: {e}")

if __name__ == '__main__':
    main()
