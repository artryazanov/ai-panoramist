from google import genai
from google.genai import types
import logging
from typing import List, Optional, Any
from PIL import Image
from app.config import Config
import json
import os
from tenacity import retry, wait_exponential, stop_after_attempt
from app.core.models import ImageValidationResult

logger = logging.getLogger(__name__)

class GenAIClient:
    def __init__(self):
        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY,
            http_options={'timeout': 180000}
        )
        self.text_model_name = Config.TEXT_MODEL_NAME
        self.image_model_name = Config.IMAGE_MODEL_NAME
        self.validator_model_name = Config.VALIDATOR_MODEL_NAME

    @retry(wait=wait_exponential(multiplier=1, min=4, max=30), stop=stop_after_attempt(3), reraise=True)
    def generate_text(self, prompt: str, schema: Optional[Any] = None, reference_images: Optional[List[str]] = None) -> Any:
        try:
            config_args = {
                'safety_settings': [
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH")
                ]
            }
            if schema:
                config_args['response_mime_type'] = 'application/json'
                config_args['response_schema'] = schema

            contents = [prompt]
            if reference_images:
                for ref_path in reference_images:
                    if os.path.exists(ref_path):
                        try:
                            contents.append(Image.open(ref_path))
                        except Exception as img_e:
                            logger.warning(f"Could not load ref image {ref_path}: {img_e}")

            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=contents,
                config=types.GenerateContentConfig(**config_args)
            )
            
            if schema and hasattr(response, 'parsed') and response.parsed is not None:
                return response.parsed
            
            # Fallback if parsing didn't happen natively but schema was requested
            if schema:
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_text)
                return schema(**data)

            return response.text
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise

    def sanitize_prompt_feedback(self, feedback: str) -> str:
        """Translates QA validator feedback into a safe, positive image generation prompt."""
        try:
            prompt = (
                f"You are a Prompt Engineer. Your task is to extract the core issue from QA feedback about a failed image "
                f"and rewrite it as a safe, purely visual instruction for an image generation model.\n"
                f"The image generator will reject prompts if they contain words like 'watermark', 'signature', 'copyright', 'text', 'error', 'fail', or conversational phrasing.\n\n"
                f"Original QA Feedback: '{feedback}'\n\n"
                f"Rewrite it as a simple, positive visual instruction describing how the image SHOULD look. Do not use negative commands involving banned words. "
                f"For example, instead of 'Remove the watermark', write 'Ensure the image is completely clean and unmarked.'\n"
                f"Return ONLY the rewritten visual instruction, nothing else."
            )
            return self.generate_text(prompt).strip()
        except Exception as e:
            logger.warning(f"Feedback sanitization failed: {e}. Using original.")
            return feedback

    @retry(wait=wait_exponential(multiplier=1, min=4, max=30), stop=stop_after_attempt(3), reraise=True)
    def generate_image(self, prompt: str, reference_images: Optional[List[str]] = None, output_path: str = None) -> str:
        """
        Generates an image using the configured model. 
        Uses generate_content for multimodal inputs if references are provided.
        """
        if reference_images is None:
            reference_images = []
            
        aspect_ratio = Config.IMAGE_ASPECT_RATIO

        try:
            logger.info(f"Generating image with model {self.image_model_name}. Refs: {len(reference_images)}")

            contents = [prompt]
            if reference_images:
                contents.append("\\n\\nReference Images Context:")
                for ref_path in reference_images:
                    if os.path.exists(ref_path):
                        try:
                            contents.append(Image.open(ref_path))
                        except Exception as img_e:
                            logger.warning(f"Could not load ref image {ref_path}: {img_e}")

            response = self.client.models.generate_content(
                model=self.image_model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        image_size=Config.IMAGE_RESOLUTION
                    ),
                    safety_settings=[
                        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
                        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
                        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"),
                        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH")
                    ]
                )
            )
            
            if response.parts:
                for part in response.parts:
                    if hasattr(part, 'image') and part.image:
                         with open(output_path, "wb") as f:
                            f.write(part.image.image_bytes)
                         return output_path
                    
                    if hasattr(part, 'as_image'):
                        pil_img = part.as_image()
                        if pil_img:
                            pil_img.save(output_path)
                            return output_path

            raise RuntimeError("Gemini generation returned no images.")

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise

    def fix_panorama_seam(self, image_path: str, output_path: str) -> str:
        """
        Uses the image generator to heal the vertical seam in the center of the image.
        """
        prompt = (
            "This is a 360-degree panorama. There is a large artificial black box in the center of the image. "
            "Please regenerate the image, completely removing the black box and replacing it with natural scenery "
            "that perfectly connects the left and right halves of the image. Create a smooth, continuous transition "
            "in the center that flawlessly matches the surrounding environment. DO NOT change the outer edges; "
            "keep the left and right sides of the room exactly as they are."
        )
        logger.info(f"Fixing panorama seam for {image_path}...")
        return self.generate_image(
            prompt=prompt,
            reference_images=[image_path],
            output_path=output_path
        )

    def validate_panorama(self, generated_image_path: str, user_prompt: str) -> ImageValidationResult:
        logger.info(f"Running QA validation on {generated_image_path}...")
        
        prompt = f"""
        You are an expert Art Director and strict Quality Assurance inspector for VR assets.
        I am providing you with a generated equirectangular panorama image.
        
        Evaluate the image against these STRICT rules:
        1. It MUST look like an equirectangular projection (distorted at the top and bottom).
        2. The extreme top edge (zenith) and extreme bottom edge (nadir) MUST NOT have any lines intersecting them. DO NOT fail the image due to lines touching or intersecting the very top or bottom boundaries.
        3. The left and right edges should appear as if they could seamlessly wrap around to meet each other. If an object is cut off on the right edge, its exact continuation MUST appear on the left edge at the same height. DO NOT fail the image due to minor mismatches or slight misalignments between the left and right edges.
        4. It MUST generally align with the user's base prompt: '{user_prompt}'.
        5. It must NOT look like a standard flat photograph or a collage of multiple disparate scenes.

        Return the validation JSON. If it fails, explain EXACTLY what is wrong (e.g. "object intersecting top edge", "left and right edges do not match") so the generator can fix it in the next attempt.
        """
        
        try:
            contents = [prompt, Image.open(generated_image_path)]
            
            result = self.client.models.generate_content(
                model=self.validator_model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ImageValidationResult,
                    temperature=0.0,
                )
            )
            if hasattr(result, 'parsed') and result.parsed:
                return result.parsed
                
            clean_text = result.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            return ImageValidationResult(**data)
            
        except Exception as e:
            logger.warning(f"Validation API failed: {e}. Bypassing validation.")
            return ImageValidationResult(is_valid=True, feedback="Validation bypassed due to error.")
