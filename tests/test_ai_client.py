import pytest
import os
import time
from PIL import Image
from app.core.ai_client import GenAIClient
from app.core.models import ImageValidationResult, EnhancedPrompt
from google.genai import types

@pytest.fixture
def mock_genai_client(mocker):
    # Patch the underlying genai.Client so we don't make real network calls
    mocker.patch('app.core.ai_client.genai.Client')
    return GenAIClient()

@pytest.fixture(autouse=True)
def no_sleep(mocker):
    # Disable time.sleep so tenacity retries happen instantly
    mocker.patch('time.sleep')

def test_sanitize_prompt_feedback(mocker, mock_genai_client):
    mocker.patch.object(mock_genai_client, 'generate_text', return_value="Make sure the left and right edges seamlessly match.")
    result = mock_genai_client.sanitize_prompt_feedback("QA Validation Failed: The image fails because the left and right edges do not match.")
    assert result == "Make sure the left and right edges seamlessly match."
    mock_genai_client.generate_text.assert_called_once()

def test_sanitize_prompt_feedback_exception(mocker, mock_genai_client):
    mocker.patch.object(mock_genai_client, 'generate_text', side_effect=Exception("API Error"))
    result = mock_genai_client.sanitize_prompt_feedback("Original Feedback")
    # Should fallback to original feedback
    assert result == "Original Feedback"

def test_generate_text_success_no_schema(mocker, mock_genai_client):
    mock_response = mocker.Mock()
    mock_response.text = "Here is some generated text"
    mock_genai_client.client.models.generate_content.return_value = mock_response

    result = mock_genai_client.generate_text("test prompt")
    assert result == "Here is some generated text"
    mock_genai_client.client.models.generate_content.assert_called_once()

def test_generate_text_with_schema_native_parsing(mocker, mock_genai_client):
    mock_response = mocker.Mock()
    mock_parsed = EnhancedPrompt(
        zenith_description="zenith", nadir_description="nadir", 
        horizon_description="horizon", reference_instructions="", combined_prompt="prompt"
    )
    mock_response.parsed = mock_parsed
    mock_genai_client.client.models.generate_content.return_value = mock_response

    result = mock_genai_client.generate_text("test prompt", schema=EnhancedPrompt)
    assert result == mock_parsed

def test_generate_text_with_schema_fallback_parsing(mocker, mock_genai_client):
    mock_response = mocker.Mock()
    # Deliberately removing parsed to force fallback
    del mock_response.parsed
    mock_response.text = '```json\n{"zenith_description": "z", "nadir_description": "n", "horizon_description": "h", "reference_instructions": "", "combined_prompt": "c"}\n```'
    mock_genai_client.client.models.generate_content.return_value = mock_response

    result = mock_genai_client.generate_text("test prompt", schema=EnhancedPrompt)
    assert result.zenith_description == "z"
    assert result.combined_prompt == "c"

def test_generate_text_with_reference_images(mocker, mock_genai_client, tmp_path):
    img_path = tmp_path / "test.jpg"
    Image.new('RGB', (10, 10)).save(img_path)
    
    mock_response = mocker.Mock()
    mock_response.text = "Result with image"
    mock_genai_client.client.models.generate_content.return_value = mock_response

    # include a non-existent path to test exception handling inside loop
    result = mock_genai_client.generate_text("test prompt", reference_images=[str(img_path), "does_not_exist.jpg"])
    assert result == "Result with image"
    call_args = mock_genai_client.client.models.generate_content.call_args[1]
    assert len(call_args['contents']) == 2 # Prompt + 1 Valid Image

def test_generate_text_exception(mocker, mock_genai_client):
    mock_genai_client.client.models.generate_content.side_effect = Exception("API Error")
    with pytest.raises(Exception):
        mock_genai_client.generate_text("test prompt")

def test_generate_image_success_image_bytes(mocker, mock_genai_client, tmp_path):
    mock_response = mocker.Mock()
    mock_part = mocker.Mock()
    mock_part.image.image_bytes = b"fake_image_data"
    mock_response.parts = [mock_part]
    mock_genai_client.client.models.generate_content.return_value = mock_response

    out_path = str(tmp_path / "out.png")
    result = mock_genai_client.generate_image("test prompt", output_path=out_path)
    assert result == out_path
    assert os.path.exists(out_path)
    with open(out_path, "rb") as f:
        assert f.read() == b"fake_image_data"

def test_generate_image_success_as_image(mocker, mock_genai_client, tmp_path):
    mock_response = mocker.Mock()
    mock_part = mocker.Mock()
    del mock_part.image # Force fallback to as_image()
    mock_pil = mocker.Mock()
    mock_part.as_image.return_value = mock_pil
    mock_response.parts = [mock_part]
    mock_genai_client.client.models.generate_content.return_value = mock_response

    out_path = str(tmp_path / "out2.png")
    result = mock_genai_client.generate_image("test prompt", output_path=out_path)
    assert result == out_path
    mock_pil.save.assert_called_once_with(out_path)

def test_generate_image_with_reference_images(mocker, mock_genai_client, tmp_path):
    img_path = tmp_path / "test.jpg"
    Image.new('RGB', (10, 10)).save(img_path)

    mock_response = mocker.Mock()
    mock_part = mocker.Mock()
    mock_part.image.image_bytes = b"fake_image_data"
    mock_response.parts = [mock_part]
    mock_genai_client.client.models.generate_content.return_value = mock_response

    out_path = str(tmp_path / "out3.png")
    result = mock_genai_client.generate_image("test prompt", reference_images=[str(img_path), "does_not_exist.jpg"], output_path=out_path)
    assert result == out_path
    call_args = mock_genai_client.client.models.generate_content.call_args[1]
    # prompt + text reference label + image
    assert len(call_args['contents']) == 3

def test_generate_image_no_images_returned(mocker, mock_genai_client):
    mock_response = mocker.Mock()
    mock_response.parts = []
    mock_genai_client.client.models.generate_content.return_value = mock_response

    with pytest.raises(RuntimeError, match="returned no images"):
        mock_genai_client.generate_image("test prompt", output_path="out.png")

def test_generate_image_exception(mocker, mock_genai_client):
    mock_genai_client.client.models.generate_content.side_effect = Exception("API Error")
    with pytest.raises(Exception):
         mock_genai_client.generate_image("test prompt", output_path="out.png")

def test_validate_panorama_native_parsing(mocker, mock_genai_client, tmp_path):
    img_path = tmp_path / "test.jpg"
    Image.new('RGB', (10, 10)).save(img_path)

    mock_response = mocker.Mock()
    mock_parsed = ImageValidationResult(is_valid=True, feedback="Good")
    mock_response.parsed = mock_parsed
    mock_genai_client.client.models.generate_content.return_value = mock_response

    result = mock_genai_client.validate_panorama(str(img_path), "test prompt")
    assert result == mock_parsed

def test_validate_panorama_fallback_parsing(mocker, mock_genai_client, tmp_path):
    img_path = tmp_path / "test.jpg"
    Image.new('RGB', (10, 10)).save(img_path)

    mock_response = mocker.Mock()
    del mock_response.parsed
    mock_response.text = '```json\n{"is_valid": false, "feedback": "Bad"}\n```'
    mock_genai_client.client.models.generate_content.return_value = mock_response

    result = mock_genai_client.validate_panorama(str(img_path), "test prompt")
    assert result.is_valid is False
    assert result.feedback == "Bad"

def test_validate_panorama_exception_bypass(mocker, mock_genai_client, tmp_path):
    img_path = tmp_path / "test.jpg"
    Image.new('RGB', (10, 10)).save(img_path)

    mock_genai_client.client.models.generate_content.side_effect = Exception("API Error")

    result = mock_genai_client.validate_panorama(str(img_path), "test prompt")
    assert result.is_valid is True
    assert "bypassed" in result.feedback
