import logging
from typing import Optional, List
from app.core.ai_client import GenAIClient
from app.core.models import EnhancedPrompt

logger = logging.getLogger(__name__)

class PromptEnhancer:
    def __init__(self, ai_client: GenAIClient):
        self.ai_client = ai_client

    def enhance(self, user_prompt: str, reference_images: Optional[List[str]] = None) -> str:
        """
        Takes a simple user prompt and expands it into a detailed equirectangular VR prompt.
        """
        logger.info("Enhancing prompt for 360-degree panorama...")
        
        system_instruction = f"""
        You are an expert VR Environment Designer and Prompt Engineer.
        The user wants to generate a 360-degree equirectangular panorama.
        
        User's base idea: "{user_prompt}"
        
        Your task is to expand this idea into a highly detailed, immersive prompt suitable for an AI image generator.
        
        CRITICAL RULES:
        1. You MUST invent a logical zenith (what is straight above the viewer's head, like the sky, a ceiling, or canopy). The zenith should logically complete the environment for a spherical view.
        2. You MUST invent a logical nadir (what is straight below the viewer's feet, like the ground, a chasm, or floor). The nadir should logically complete the environment for a spherical view.
        3. You MUST invent a detailed 360-degree horizon at eye level.
        4. The left and right edges MUST perfectly mirror each other for a seamless horizontal wrap. Any object or structure that extends past the right boundary MUST continue on the left boundary at the exact same vertical position and angle.
        5. The final `combined_prompt` MUST include the following exact phrases:
           - "true equirectangular projection"
           - "seamless 360-degree VR panorama"
           - "mathematically seamless left and right edges"
        6. Describe the scene as a single, cohesive environment. Do not use negative prompts or meta-language like "Generate an image of...".
        7. If the user's base idea mentions attached reference images, extract their instructions about them and populate the `reference_instructions` field.
        
        Return the structured JSON output.
        """

        try:
            enhanced_data = self.ai_client.generate_text(
                system_instruction, 
                schema=EnhancedPrompt,
                reference_images=reference_images
            )
            logger.info(f"Enhanced Data Dict: {enhanced_data.dict() if hasattr(enhanced_data, 'dict') else enhanced_data}")
            final_prompt = enhanced_data.combined_prompt
            if hasattr(enhanced_data, 'reference_instructions') and enhanced_data.reference_instructions:
                final_prompt += f"\n\n[META-INSTRUCTION FOR IMAGE GENERATOR]: {enhanced_data.reference_instructions}"
            logger.info(f"Enhanced Prompt: {final_prompt}")
            return final_prompt
        except Exception as e:
            logger.warning(f"Failed to enhance prompt: {e}. Falling back to basic VR prompt.")
            # Fallback that at least adds the mandatory keywords
            return (
                f"A seamless 360-degree VR panorama, true equirectangular projection. "
                f"{user_prompt}. "
                f"Highly detailed, 8k resolution, ray-traced lighting, immersive spherical background, "
                f"mathematically seamless left and right edges for continuous VR mapping."
            )
