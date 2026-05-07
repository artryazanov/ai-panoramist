import logging
from pathlib import Path
from typing import List, Optional
import time

from app.config import Config
from app.core.ai_client import GenAIClient
from app.core.prompt_enhancer import PromptEnhancer

logger = logging.getLogger(__name__)

class Panoramist:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.ai_client = GenAIClient()
        self.enhancer = PromptEnhancer(self.ai_client)

    def generate_panorama(self, user_prompt: str, reference_images: Optional[List[str]] = None) -> str:
        """
        Orchestrates the panorama generation process.
        """
        # 1. Enhance the prompt
        enhanced_prompt = self.enhancer.enhance(user_prompt)

        max_retries = Config.MAX_RETRIES
        current_attempt = 1
        qa_feedback = ""

        # Safe slug for filename
        slug = "".join(x for x in user_prompt[:20].lower() if x.isalnum() or x == '_')
        if not slug:
            slug = "panorama"

        timestamp = int(time.time())
        final_output_path = ""

        # 2. Generation Loop with QA
        while current_attempt <= max_retries:
            logger.info(f"--- Attempt {current_attempt}/{max_retries} ---")
            
            # Incorporate QA feedback if we have it
            current_prompt = enhanced_prompt
            if qa_feedback:
                safe_feedback = self.ai_client.sanitize_prompt_feedback(qa_feedback)
                current_prompt += f"\n\n[CRITICAL CORRECTIONS]: {safe_feedback}"

            output_filename = f"{slug}_{timestamp}_v{current_attempt}.png"
            attempt_output_path = str(self.output_dir / output_filename)

            try:
                # Generate Image
                saved_path = self.ai_client.generate_image(
                    prompt=current_prompt,
                    reference_images=reference_images,
                    output_path=attempt_output_path
                )
                logger.info(f"Image generated at: {saved_path}")

                # QA Validation
                validation_result = self.ai_client.validate_panorama(saved_path, user_prompt)
                
                if validation_result.is_valid:
                    logger.info("QA Validation Passed! The panorama looks correct.")
                    final_output_path = saved_path
                    break
                else:
                    logger.warning(f"QA Validation Failed: {validation_result.feedback}")
                    qa_feedback = validation_result.feedback
                    final_output_path = saved_path # Keep it in case we run out of retries
                    
            except Exception as e:
                logger.error(f"Generation attempt failed: {e}")
                if current_attempt == max_retries:
                    raise

            current_attempt += 1

        if current_attempt > max_retries:
            logger.warning("Max retries reached. Returning the last generated image despite QA failures.")

        return final_output_path
