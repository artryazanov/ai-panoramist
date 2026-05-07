import pytest
from app.core.ai_client import GenAIClient

def test_sanitize_prompt_feedback(mocker):
    mock_client = mocker.patch('app.core.ai_client.genai.Client').return_value
    
    # We create the class instance
    client = GenAIClient()
    
    # Mock the internal generate_text call
    mocker.patch.object(client, 'generate_text', return_value="Make sure the left and right edges seamlessly match.")
    
    result = client.sanitize_prompt_feedback("QA Validation Failed: The image fails because the left and right edges do not match.")
    
    assert result == "Make sure the left and right edges seamlessly match."
    client.generate_text.assert_called_once()
