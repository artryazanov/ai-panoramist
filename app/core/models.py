from typing import Optional
from pydantic import BaseModel, Field

class EnhancedPrompt(BaseModel):
    zenith_description: str = Field(description="Detailed visual description of what is directly overhead (zenith).")
    nadir_description: str = Field(description="Detailed visual description of what is directly underfoot (nadir).")
    horizon_description: str = Field(description="Detailed visual description of the 360-degree environment at eye level.")
    reference_instructions: str = Field(description="MANDATORY if the user mentions attached images. Extract any sentences from the user's base idea that mention attached images, references, or how to use them. Translate them to English.")
    combined_prompt: str = Field(description="The final cohesive prompt merging zenith, nadir, and horizon with the strict VR markers ('true equirectangular projection', 'seamless 360-degree VR panorama', 'mathematically seamless left and right edges').")

class ImageValidationResult(BaseModel):
    is_valid: bool = Field(description="True if the image PERFECTLY meets the criteria for a 360-degree equirectangular panorama without obvious stitching errors or non-panoramic layouts.")
    feedback: str = Field(description="If invalid, provide EXTREMELY specific feedback on what is wrong and how the image generator must fix it in the next attempt.")
