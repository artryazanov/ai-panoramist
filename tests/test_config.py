import pytest
from pathlib import Path
from app.config import Config, setup_directories

def test_config_validate_success(mocker):
    mocker.patch.object(Config, 'GEMINI_API_KEY', "fake_key")
    # Should not raise
    Config.validate()

def test_config_validate_failure(mocker):
    mocker.patch.object(Config, 'GEMINI_API_KEY', None)
    with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is not set"):
        Config.validate()

def test_setup_directories(tmp_path):
    out_dir = tmp_path / "new_folder"
    assert not out_dir.exists()
    setup_directories(out_dir)
    assert out_dir.exists()
    assert out_dir.is_dir()
