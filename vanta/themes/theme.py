from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Color:
    r: int
    g: int
    b: int
    
    def to_ansi(self) -> str:
        return f"\033[38;2;{self.r};{self.g};{self.b}m"

@dataclass
class Theme:
    name: str
    foreground: Color
    background: Color
    keyword: Color
    string: Color
    comment: Color
    number: Color
    operator: Color
    selection: Color
    cursor: Color
    status_bar: Color
    error: Color
    warning: Color

class ThemeManager:
    """Manages themes"""
    
    LIGHT_THEME = Theme(
        name="light",
        foreground=Color(0, 0, 0),
        background=Color(255, 255, 255),
        keyword=Color(128, 0, 128),
        string=Color(0, 128, 0),
        comment=Color(128, 128, 128),
        number=Color(0, 128, 255),
        operator=Color(255, 128, 0),
        selection=Color(200, 200, 255),
        cursor=Color(0, 0, 0),
        status_bar=Color(200, 200, 200),
        error=Color(255, 0, 0),
        warning=Color(255, 165, 0)
    )
    
    DARK_THEME = Theme(
        name="dark",
        foreground=Color(255, 255, 255),
        background=Color(30, 30, 30),
        keyword=Color(200, 100, 255),
        string=Color(100, 200, 100),
        comment=Color(128, 128, 128),
        number=Color(100, 200, 255),
        operator=Color(255, 165, 0),
        selection=Color(100, 100, 200),
        cursor=Color(255, 255, 255),
        status_bar=Color(60, 60, 60),
        error=Color(255, 100, 100),
        warning=Color(255, 200, 100)
    )
    
    def __init__(self):
        self.themes: Dict[str, Theme] = {
            "light": self.LIGHT_THEME,
            "dark": self.DARK_THEME,
        }
        self.current_theme = self.DARK_THEME
    
    def register_theme(self, theme: Theme) -> None:
        """Register a theme"""
        self.themes[theme.name] = theme
    
    def set_theme(self, name: str) -> bool:
        """Set current theme"""
        if name in self.themes:
            self.current_theme = self.themes[name]
            return True
        return False
    
    def get_theme(self, name: str) -> Optional[Theme]:
        """Get theme by name"""
        return self.themes.get(name)
    
    def get_current_theme(self) -> Theme:
        """Get current theme"""
        return self.current_theme
    
    def list_themes(self) -> Dict[str, Theme]:
        """List all themes"""
        return self.themes.copy()
