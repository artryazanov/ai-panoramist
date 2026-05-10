import pytest
from pathlib import Path
from app.core.panoramist import Panoramist
from app.core.models import ImageValidationResult

def test_generate_panorama_success_first_try(mocker, tmp_path):
    # Mock GenAIClient
    mock_ai_client = mocker.patch('app.core.panoramist.GenAIClient').return_value
    mock_ai_client.generate_image.return_value = str(tmp_path / "test_image.png")
    mock_ai_client.validate_panorama.return_value = ImageValidationResult(is_valid=True, feedback="Looks good")

    # Mock PromptEnhancer
    mock_enhancer = mocker.patch('app.core.panoramist.PromptEnhancer').return_value
    mock_enhancer.enhance.return_value = "Enhanced VR Prompt"

    # Mock post-processing
    mock_swap = mocker.patch('app.core.panoramist.swap_image_halves')
    mock_blend = mocker.patch('app.core.panoramist.blend_center_patch')
    mock_ai_client.fix_panorama_seam.return_value = "ai_fixed_path.png"

    panoramist = Panoramist(tmp_path)
    result = panoramist.generate_panorama("test prompt")

    # It returns the final fixed path
    assert result.endswith("_final.png")
    mock_ai_client.generate_image.assert_called_once()
    mock_ai_client.validate_panorama.assert_called_once()
    mock_ai_client.fix_panorama_seam.assert_called_once()
    assert mock_swap.call_count == 2
    mock_blend.assert_called_once()

def test_generate_panorama_retry_on_qa_fail(mocker, tmp_path):
    mocker.patch('app.core.panoramist.Config.MAX_RETRIES', 2)
    
    mock_ai_client = mocker.patch('app.core.panoramist.GenAIClient').return_value
    mock_ai_client.generate_image.return_value = str(tmp_path / "test_image.png")
    
    # First fail, second pass
    mock_ai_client.validate_panorama.side_effect = [
        ImageValidationResult(is_valid=False, feedback="Fix horizon"),
        ImageValidationResult(is_valid=True, feedback="Looks good")
    ]

    mock_enhancer = mocker.patch('app.core.panoramist.PromptEnhancer').return_value
    mock_enhancer.enhance.return_value = "Enhanced VR Prompt"

    # Mock post-processing
    mock_swap = mocker.patch('app.core.panoramist.swap_image_halves')
    mock_blend = mocker.patch('app.core.panoramist.blend_center_patch')

    panoramist = Panoramist(tmp_path)
    result = panoramist.generate_panorama("test prompt")

    assert result.endswith("_final.png")
    assert mock_ai_client.generate_image.call_count == 2
    assert mock_ai_client.validate_panorama.call_count == 2
    mock_ai_client.fix_panorama_seam.assert_called_once()
    assert mock_swap.call_count == 2
    mock_blend.assert_called_once()
