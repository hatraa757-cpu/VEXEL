from dataclasses import dataclass
from typing import Optional

@dataclass
class StatusBar:
    """Status bar display"""
    filename: str = "untitled"
    line: int = 1
    col: int = 1
    mode: str = "NORMAL"
    modified: bool = False
    encoding: str = "utf-8"
    
    def render(self) -> str:
        """Render status bar text"""
        modified_indicator = "[+]" if self.modified else ""
        return f" {self.filename} {modified_indicator} | Line {self.line}, Col {self.col} | {self.encoding} | {self.mode}"
