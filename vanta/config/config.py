import os
from pathlib import Path
from typing import Dict, Any, Optional
import tomli
import tomli_w

class Config:
    """VANTA configuration manager"""
    
    DEFAULT_CONFIG = {
        "theme": "dark",
        "tab_size": 4,
        "use_spaces": True,
        "line_numbers": True,
        "word_wrap": False,
        "autosave": False,
        "autosave_delay": 5000,
        "cursor_style": "block",
        "mouse_support": True,
        "keybindings": {},
        "lsp": {
            "enable": True,
            "timeout": 5000,
        },
        "plugins": {
            "enabled": True,
            "paths": []
        },
        "ai": {
            "enable": False,
            "provider": "openai",
            "model": "gpt-4"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_dir = Path.home() / ".config" / "vanta"
            config_path = str(config_dir / "config.toml")
        
        self.config_path = Path(config_path)
        self.data: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self) -> bool:
        """Load configuration from file"""
        if not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'rb') as f:
                loaded = tomli.load(f)
            self.data.update(loaded)
            return True
        except Exception:
            return False
    
    def save(self) -> bool:
        """Save configuration to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'wb') as f:
                tomli_w.dump(self.data, f)
            return True
        except Exception:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        keys = key.split(".")
        current = self.data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    
    def reset(self) -> None:
        """Reset to defaults"""
        self.data = self.DEFAULT_CONFIG.copy()
