import pytest
import os
import numpy as np
from PIL import Image
from app.core.image_utils import swap_image_halves, blend_center_patch

@pytest.fixture
def dummy_image(tmp_path):
    img = Image.new("RGB", (100, 50), color="white")
    # Draw something to distinguish left and right
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 50, 50], fill="red")
    draw.rectangle([50, 0, 100, 50], fill="blue")
    
    img_path = str(tmp_path / "dummy.png")
    img.save(img_path)
    return img_path

def test_swap_image_halves(tmp_path, dummy_image):
    output_path = str(tmp_path / "swapped.png")
    result_path = swap_image_halves(dummy_image, output_path)
    
    assert os.path.exists(result_path)
    
    with Image.open(result_path) as img:
        assert img.size == (100, 50)
        # Now left should be blue (50-100 of original), right should be red (0-50 of original)
        assert img.getpixel((25, 25))[:3] == (0, 0, 255) # Blue
        assert img.getpixel((75, 25))[:3] == (255, 0, 0) # Red

def test_blend_center_patch(tmp_path):
    orig = Image.new("RGB", (100, 50), color="black")
    fixed = Image.new("RGB", (100, 50), color="white")
    
    orig_path = str(tmp_path / "orig.png")
    fixed_path = str(tmp_path / "fixed.png")
    output_path = str(tmp_path / "blended.png")
    
    orig.save(orig_path)
    fixed.save(fixed_path)
    
    result_path = blend_center_patch(orig_path, fixed_path, output_path, patch_width_ratio=0.4)
    assert os.path.exists(result_path)
    
    with Image.open(result_path) as img:
        assert img.size == (100, 50)
        # Patch is 40 pixels wide. Center is from x=30 to x=70.
        # Edges of the original image (x=0..29, x=71..99) should remain pure black
        assert img.getpixel((10, 25))[:3] == (0, 0, 0)
        assert img.getpixel((90, 25))[:3] == (0, 0, 0)
        
        # Dead center (x=50) should be pure white
        assert img.getpixel((50, 25))[:3] == (255, 255, 255)
        
        # The feathered area (e.g., x=31, which is 1 pixel into the 2-pixel feather)
        # should be a mix of black and white (gray).
        gray_val = img.getpixel((31, 25))[0]
        assert 0 < gray_val < 255

def test_swap_image_halves_jpg(tmp_path, dummy_image):
    output_path = str(tmp_path / "swapped.jpg")
    result_path = swap_image_halves(dummy_image, output_path)
    assert result_path.endswith(".jpg")
    assert os.path.exists(result_path)

def test_draw_center_black_box_jpg(tmp_path, dummy_image):
    output_path = str(tmp_path / "black_box.jpg")
    from app.core.image_utils import draw_center_black_box
    result_path = draw_center_black_box(dummy_image, output_path)
    assert result_path.endswith(".jpg")
    assert os.path.exists(result_path)

def test_blend_center_patch_jpg(tmp_path):
    orig = Image.new("RGB", (100, 50), color="black")
    fixed = Image.new("RGB", (100, 50), color="white")
    orig_path = str(tmp_path / "orig.png")
    fixed_path = str(tmp_path / "fixed.png")
    output_path = str(tmp_path / "blended.jpg")
    orig.save(orig_path)
    fixed.save(fixed_path)
    result_path = blend_center_patch(orig_path, fixed_path, output_path, patch_width_ratio=0.4)
    assert result_path.endswith(".jpg")
    assert os.path.exists(result_path)

def test_swap_image_halves_exception():
    with pytest.raises(Exception):
        swap_image_halves("nonexistent_image.png", "output.png")

def test_draw_center_black_box_exception():
    from app.core.image_utils import draw_center_black_box
    with pytest.raises(Exception):
        draw_center_black_box("nonexistent_image.png", "output.png")

def test_blend_center_patch_exception():
    with pytest.raises(Exception):
        blend_center_patch("nonexistent_orig.png", "nonexistent_fixed.png", "output.png")

def test_blend_center_patch_resize(tmp_path):
    orig = Image.new("RGB", (100, 50), color="black")
    fixed = Image.new("RGB", (80, 40), color="white") # different size
    orig_path = str(tmp_path / "orig.png")
    fixed_path = str(tmp_path / "fixed.png")
    output_path = str(tmp_path / "blended.png")
    orig.save(orig_path)
    fixed.save(fixed_path)
    blend_center_patch(orig_path, fixed_path, output_path)
    
def test_blend_center_patch_odd_width(tmp_path):
    orig = Image.new("RGB", (100, 50), color="black")
    fixed = Image.new("RGB", (100, 50), color="white") 
    orig_path = str(tmp_path / "orig.png")
    fixed_path = str(tmp_path / "fixed.png")
    output_path = str(tmp_path / "blended.png")
    orig.save(orig_path)
    fixed.save(fixed_path)
    # 0.33 * 100 = 33 (odd)
    blend_center_patch(orig_path, fixed_path, output_path, patch_width_ratio=0.33)
