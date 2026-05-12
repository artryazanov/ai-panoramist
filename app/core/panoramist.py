import logging
from pathlib import Path
from typing import List, Optional
import time

from app.config import Config
from app.core.ai_client import GenAIClient
from app.core.prompt_enhancer import PromptEnhancer
from app.core.image_utils import swap_image_halves, blend_center_patch, draw_center_black_box

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
        enhanced_prompt = self.enhancer.enhance(user_prompt, reference_images)

        max_retries = Config.MAX_RETRIES
        current_attempt = 1
        accumulated_feedbacks = []

        # Safe slug for filename
        slug = "".join(x for x in user_prompt[:20].lower() if x.isalnum() or x == '_')
        if not slug:
            slug = "panorama"

        timestamp = int(time.time())
        final_output_path = ""

        # 2. Generation Loop with QA
        while current_attempt <= max_retries:
            logger.info(f"--- Attempt {current_attempt}/{max_retries} ---")
            
            # Incorporate accumulated QA feedback
            current_prompt = enhanced_prompt
            if accumulated_feedbacks:
                current_prompt += "\n\n[CRITICAL CORRECTIONS REQUIRED]\n"
                current_prompt += "The attached reference image is your previous attempt. It contains errors.\n"
                current_prompt += "You MUST use the reference image as your base and regenerate it, fixing the following issues while keeping the rest of the image intact:\n"
                for i, fb in enumerate(accumulated_feedbacks, 1):
                    current_prompt += f"{i}. {fb}\n"

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
                    safe_feedback = self.ai_client.sanitize_prompt_feedback(validation_result.feedback)
                    accumulated_feedbacks.append(safe_feedback)
                    final_output_path = saved_path # Keep it in case we run out of retries
                    
                    # Update reference images to the failed image for img2img refinement
                    logger.info(f"Using {saved_path} as reference image for the next attempt.")
                    reference_images = [saved_path]
                    
            except Exception as e:
                logger.error(f"Generation attempt failed: {e}")
                if current_attempt == max_retries:
                    raise

            current_attempt += 1

        if current_attempt > max_retries:
            logger.warning("Max retries reached. Returning the last generated image despite QA failures.")

        # 3. Post-Processing: Seam Fixing
        if final_output_path:
            logger.info("Applying post-processing to fix the back seam...")
            try:
                # Setup intermediate paths
                base_name = Path(final_output_path).stem
                swapped_path = str(self.output_dir / f"{base_name}_swapped.png")
                ai_fixed_path = str(self.output_dir / f"{base_name}_ai_fixed.png")
                blended_path = str(self.output_dir / f"{base_name}_blended.png")
                final_fixed_path = str(self.output_dir / f"{base_name}_final.png")

                # Step 1: Swap halves to move the seam to the center
                swap_image_halves(final_output_path, swapped_path)

                # Step 1.5: Check if a seam actually exists before trying to fix it
                logger.info("Analyzing if a central seam exists...")
                seam_analysis = self.ai_client.analyze_center_seam(swapped_path)
                
                if not seam_analysis.has_seam:
                    logger.info(f"No seam detected! Skipping seam repair. Reasoning: {seam_analysis.reasoning}")
                    return final_output_path
                else:
                    logger.info(f"Seam detected, proceeding with repair. Reasoning: {seam_analysis.reasoning}")

                # Step 2: Draw a black box over the seam to force the AI to inpaint it
                black_box_path = str(self.output_dir / f"{base_name}_black_box.png")
                draw_center_black_box(swapped_path, black_box_path, box_width_ratio=0.2)

                # Step 3: Use AI to fix the center seam (inpaint the black box)
                self.ai_client.fix_panorama_seam(black_box_path, ai_fixed_path)

                # Step 4: Blend the AI-fixed center patch onto the original swapped image
                blend_center_patch(swapped_path, ai_fixed_path, blended_path)

                # Step 5: Swap halves back to restore original orientation
                swap_image_halves(blended_path, final_fixed_path)

                logger.info(f"Seam fixing completed successfully. Final image: {final_fixed_path}")
                final_output_path = final_fixed_path
            except Exception as e:
                logger.error(f"Seam fixing post-processing failed: {e}. Returning original output.")
                # We return the original final_output_path if post-processing fails

        return final_output_path
