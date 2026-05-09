import pytest
from app.core.prompt_enhancer import PromptEnhancer
from app.core.models import EnhancedPrompt

def test_enhance_success(mocker):
    # Mock the ai_client
    mock_ai_client = mocker.Mock()
    
    # Setup mock return value
    mock_enhanced = EnhancedPrompt(
        zenith_description="A glowing starry sky",
        nadir_description="A deep crystal canyon",
        horizon_description="Alien flora glowing in the dark",
        reference_instructions="",
        combined_prompt="A seamless 360-degree VR panorama, true equirectangular projection, mathematically seamless left and right edges. A glowing starry sky above, alien flora around, deep crystal canyon below."
    )
    mock_ai_client.generate_text.return_value = mock_enhanced

    enhancer = PromptEnhancer(mock_ai_client)
    result = enhancer.enhance("alien world")

    assert "true equirectangular projection" in result
    assert "starry sky" in result
    mock_ai_client.generate_text.assert_called_once()

def test_enhance_fallback_on_error(mocker):
    mock_ai_client = mocker.Mock()
    mock_ai_client.generate_text.side_effect = Exception("API Error")

    enhancer = PromptEnhancer(mock_ai_client)
    result = enhancer.enhance("alien world")

    # Should return fallback prompt
    assert "true equirectangular projection" in result
    assert "alien world" in result
    assert "mathematically seamless left and right edges" in result
