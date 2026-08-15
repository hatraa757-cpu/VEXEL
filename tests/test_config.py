import pytest
from vanta.config import Config
from pathlib import Path
import tempfile

def test_config_defaults():
    config = Config()
    assert config.get("theme") == "dark"
    assert config.get("tab_size") == 4

def test_config_get_nested():
    config = Config()
    assert config.get("lsp.enable") == True
    assert config.get("lsp.timeout") == 5000

def test_config_set():
    config = Config()
    config.set("theme", "light")
    assert config.get("theme") == "light"

def test_config_save_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "config.toml"
        config = Config(str(config_file))
        config.set("theme", "custom")
        config.save()
        
        config2 = Config(str(config_file))
        config2.load()
        assert config2.get("theme") == "custom"
