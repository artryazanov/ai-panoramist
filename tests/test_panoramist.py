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
    mock_draw = mocker.patch('app.core.panoramist.draw_center_black_box')
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
    mock_draw = mocker.patch('app.core.panoramist.draw_center_black_box')
    mock_blend = mocker.patch('app.core.panoramist.blend_center_patch')

    panoramist = Panoramist(tmp_path)
    result = panoramist.generate_panorama("test prompt")

    assert result.endswith("_final.png")
    assert mock_ai_client.generate_image.call_count == 2
    assert mock_ai_client.validate_panorama.call_count == 2
    mock_ai_client.fix_panorama_seam.assert_called_once()
    assert mock_swap.call_count == 2
    mock_draw.assert_called_once()
    mock_blend.assert_called_once()

def test_generate_panorama_post_processing_failure(mocker, tmp_path):
    mock_ai_client = mocker.patch('app.core.panoramist.GenAIClient').return_value
    mock_ai_client.generate_image.return_value = str(tmp_path / "test_image.png")
    mock_ai_client.validate_panorama.return_value = ImageValidationResult(is_valid=True, feedback="Looks good")
    
    mock_enhancer = mocker.patch('app.core.panoramist.PromptEnhancer').return_value
    mock_enhancer.enhance.return_value = "Enhanced VR Prompt"
    
    # Force an exception during post-processing
    mocker.patch('app.core.panoramist.swap_image_halves', side_effect=Exception("Post processing failed"))

    panoramist = Panoramist(tmp_path)
    result = panoramist.generate_panorama("test prompt")
    
    # Should return original image without _final
    assert result.endswith("test_image.png")

def test_generate_panorama_max_retries_reached(mocker, tmp_path):
    mocker.patch('app.core.panoramist.Config.MAX_RETRIES', 1)
    
    mock_ai_client = mocker.patch('app.core.panoramist.GenAIClient').return_value
    mock_ai_client.generate_image.return_value = str(tmp_path / "fail_image.png")
    mock_ai_client.validate_panorama.return_value = ImageValidationResult(is_valid=False, feedback="Fail")
    
    mock_enhancer = mocker.patch('app.core.panoramist.PromptEnhancer').return_value
    mock_enhancer.enhance.return_value = "Enhanced VR Prompt"
    
    mocker.patch('app.core.panoramist.swap_image_halves')
    mocker.patch('app.core.panoramist.draw_center_black_box')
    mocker.patch('app.core.panoramist.blend_center_patch')
    
    panoramist = Panoramist(tmp_path)
    result = panoramist.generate_panorama("test prompt")
    
    # Even if it failed all retries, it proceeds to post processing on the last generated image
    assert result.endswith("_final.png")
    assert mock_ai_client.generate_image.call_count == 1
    
def test_generate_panorama_accumulated_feedback(mocker, tmp_path):
    mocker.patch('app.core.panoramist.Config.MAX_RETRIES', 3)
    
    mock_ai_client = mocker.patch('app.core.panoramist.GenAIClient').return_value
    mock_ai_client.generate_image.return_value = str(tmp_path / "test_image.png")
    
    # Return 2 fails then pass
    mock_ai_client.validate_panorama.side_effect = [
        ImageValidationResult(is_valid=False, feedback="Error 1"),
        ImageValidationResult(is_valid=False, feedback="Error 2"),
        ImageValidationResult(is_valid=True, feedback="Looks good")
    ]
    mock_ai_client.sanitize_prompt_feedback.side_effect = lambda f: f"Safe {f}"
    
    mock_enhancer = mocker.patch('app.core.panoramist.PromptEnhancer').return_value
    mock_enhancer.enhance.return_value = "Base Prompt"
    
    mocker.patch('app.core.panoramist.swap_image_halves')
    mocker.patch('app.core.panoramist.draw_center_black_box')
    mocker.patch('app.core.panoramist.blend_center_patch')

    panoramist = Panoramist(tmp_path)
    panoramist.generate_panorama("test prompt")
    
    # Check the prompts sent to generate_image
    calls = mock_ai_client.generate_image.call_args_list
    assert len(calls) == 3
    
    # 1st attempt: no feedback
    assert "[CRITICAL CORRECTIONS REQUIRED]" not in calls[0].kwargs['prompt']
    
    # 2nd attempt: 1 feedback
    assert "[CRITICAL CORRECTIONS REQUIRED]" in calls[1].kwargs['prompt']
    assert "1. Safe Error 1" in calls[1].kwargs['prompt']
    assert "2. Safe Error 2" not in calls[1].kwargs['prompt']
    
    # 3rd attempt: 2 accumulated feedbacks
    assert "1. Safe Error 1" in calls[2].kwargs['prompt']
    assert "2. Safe Error 2" in calls[2].kwargs['prompt']

def test_generate_panorama_empty_slug(mocker, tmp_path):
    mock_ai_client = mocker.patch('app.core.panoramist.GenAIClient').return_value
    mock_ai_client.generate_image.return_value = str(tmp_path / "test_image.png")
    mock_ai_client.validate_panorama.return_value = ImageValidationResult(is_valid=True, feedback="Looks good")
    
    mock_enhancer = mocker.patch('app.core.panoramist.PromptEnhancer').return_value
    mock_enhancer.enhance.return_value = "Enhanced VR Prompt"
    
    mocker.patch('app.core.panoramist.swap_image_halves')
    mocker.patch('app.core.panoramist.draw_center_black_box')
    mocker.patch('app.core.panoramist.blend_center_patch')
    mock_ai_client.fix_panorama_seam.return_value = "ai_fixed_path.png"

    panoramist = Panoramist(tmp_path)
    panoramist.generate_panorama("!!! ***")
    
    calls = mock_ai_client.generate_image.call_args_list
    output_path = calls[0].kwargs['output_path']
    assert "panorama_" in output_path

def test_generate_panorama_generation_exception(mocker, tmp_path):
    mocker.patch('app.core.panoramist.Config.MAX_RETRIES', 2)
    mock_ai_client = mocker.patch('app.core.panoramist.GenAIClient').return_value
    mock_ai_client.generate_image.side_effect = Exception("API Error")
    
    mock_enhancer = mocker.patch('app.core.panoramist.PromptEnhancer').return_value
    mock_enhancer.enhance.return_value = "Enhanced VR Prompt"

    panoramist = Panoramist(tmp_path)
    with pytest.raises(Exception, match="API Error"):
        panoramist.generate_panorama("test prompt")
    
    assert mock_ai_client.generate_image.call_count == 2
