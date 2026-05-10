import logging
from PIL import Image, ImageDraw
import numpy as np

logger = logging.getLogger(__name__)

def draw_center_black_box(image_path: str, output_path: str, box_width_ratio: float = 0.2) -> str:
    """
    Draws a black box over the center of the image to force the AI to inpaint it.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            width, height = img.size
            box_width = int(width * box_width_ratio)
            left_bound = (width - box_width) // 2
            right_bound = left_bound + box_width

            draw = ImageDraw.Draw(img)
            draw.rectangle([left_bound, 0, right_bound, height], fill="black")

            if output_path.lower().endswith(('.jpg', '.jpeg')):
                img = img.convert("RGB")
                
            img.save(output_path)
            logger.info(f"Drew black box on {image_path} to {output_path}")
            return output_path
    except Exception as e:
        logger.error(f"Failed to draw black box: {e}")
        raise

def swap_image_halves(image_path: str, output_path: str) -> str:
    """
    Splits the image vertically down the middle and swaps the left and right halves.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            width, height = img.size
            mid = width // 2

            left_half = img.crop((0, 0, mid, height))
            right_half = img.crop((mid, 0, width, height))

            new_img = Image.new("RGBA", (width, height))
            new_img.paste(right_half, (0, 0))
            new_img.paste(left_half, (width - mid, 0))

            # Convert back to RGB for standard saving if needed, but RGBA is safe for PNG
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                new_img = new_img.convert("RGB")
                
            new_img.save(output_path)
            logger.info(f"Swapped halves of {image_path} to {output_path}")
            return output_path
    except Exception as e:
        logger.error(f"Failed to swap image halves: {e}")
        raise

def blend_center_patch(original_path: str, fixed_path: str, output_path: str, patch_width_ratio: float = 0.4, feather_ratio: float = 0.05) -> str:
    """
    Extracts a center patch from the fixed image and overlays it on the original image 
    with feathered (alpha-blended) edges to ensure a seamless transition.
    """
    try:
        with Image.open(original_path) as orig_img, Image.open(fixed_path) as fixed_img:
            orig_img = orig_img.convert("RGBA")
            fixed_img = fixed_img.convert("RGBA")

            if orig_img.size != fixed_img.size:
                # Resize fixed_img to match orig_img just in case AI altered dimensions slightly
                logger.warning("Fixed image size differs from original. Resizing fixed image.")
                fixed_img = fixed_img.resize(orig_img.size, Image.Resampling.LANCZOS)

            width, height = orig_img.size
            patch_width = int(width * patch_width_ratio)
            
            # Ensure patch width is even
            if patch_width % 2 != 0:
                patch_width += 1

            left_bound = (width - patch_width) // 2
            right_bound = left_bound + patch_width

            # Extract the center patch from the fixed image
            fixed_patch = fixed_img.crop((left_bound, 0, right_bound, height))

            # Create an alpha mask for the patch
            mask = Image.new("L", (patch_width, height), color=255)
            
            # Define feathering width, controlled by feather_ratio to keep the blend near the edges
            feather_width = int(patch_width * feather_ratio)

            # Create gradient edges using numpy for performance
            # We want a 1D gradient array that we repeat across height
            gradient = np.ones((height, patch_width), dtype=np.uint8) * 255
            
            # Left gradient: 0 to 255
            for x in range(feather_width):
                alpha_val = int((x / feather_width) * 255)
                gradient[:, x] = alpha_val
                
            # Right gradient: 255 to 0
            for x in range(feather_width):
                alpha_val = int(((feather_width - x - 1) / feather_width) * 255)
                gradient[:, patch_width - feather_width + x] = alpha_val

            # Apply gradient to mask
            mask = Image.fromarray(gradient, mode="L")
            
            # Apply the mask to the fixed patch
            fixed_patch.putalpha(mask)

            # Create a transparent layer the size of the original image
            transparent_layer = Image.new("RGBA", orig_img.size)
            # Paste the patch with its alpha channel onto the transparent layer
            transparent_layer.paste(fixed_patch, (left_bound, 0))
            
            # Use alpha_composite for mathematically correct blending without dark halos
            result_img = Image.alpha_composite(orig_img, transparent_layer)

            if output_path.lower().endswith(('.jpg', '.jpeg')):
                result_img = result_img.convert("RGB")

            result_img.save(output_path)
            logger.info(f"Blended center patch into {output_path}")
            return output_path
    except Exception as e:
        logger.error(f"Failed to blend center patch: {e}")
        raise
