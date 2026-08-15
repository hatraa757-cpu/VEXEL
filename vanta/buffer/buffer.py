from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Buffer:
    """Text buffer with line-based storage"""
    lines: List[str] = field(default_factory=lambda: [""])
    filepath: Optional[str] = None
    modified: bool = False
    read_only: bool = False
    
    def get_line(self, line_num: int) -> str:
        """Get line content (0-indexed)"""
        if 0 <= line_num < len(self.lines):
            return self.lines[line_num]
        return ""
    
    def insert_char(self, line: int, col: int, char: str) -> None:
        """Insert character at position"""
        if self.read_only:
            return
        if 0 <= line < len(self.lines):
            text = self.lines[line]
            self.lines[line] = text[:col] + char + text[col:]
            self.modified = True
    
    def delete_char(self, line: int, col: int) -> None:
        """Delete character at position"""
        if self.read_only:
            return
        if 0 <= line < len(self.lines) and col > 0:
            text = self.lines[line]
            self.lines[line] = text[:col-1] + text[col:]
            self.modified = True
    
    def delete_forward(self, line: int, col: int) -> None:
        """Delete character after cursor"""
        if self.read_only:
            return
        if 0 <= line < len(self.lines) and col < len(self.lines[line]):
            text = self.lines[line]
            self.lines[line] = text[:col] + text[col+1:]
            self.modified = True
    
    def insert_line(self, line: int, content: str = "") -> None:
        """Insert new line at position"""
        if self.read_only:
            return
        if 0 <= line <= len(self.lines):
            self.lines.insert(line, content)
            self.modified = True
    
    def delete_line(self, line: int) -> None:
        """Delete line at position"""
        if self.read_only:
            return
        if 0 <= line < len(self.lines):
            self.lines.pop(line)
            if not self.lines:
                self.lines = [""]
            self.modified = True
    
    def split_line(self, line: int, col: int) -> None:
        """Split line at cursor position"""
        if self.read_only:
            return
        if 0 <= line < len(self.lines):
            text = self.lines[line]
            self.lines[line] = text[:col]
            self.lines.insert(line + 1, text[col:])
            self.modified = True
    
    def join_lines(self, line: int) -> None:
        """Join current line with next line"""
        if self.read_only:
            return
        if 0 <= line < len(self.lines) - 1:
            self.lines[line] += self.lines[line + 1]
            self.lines.pop(line + 1)
            self.modified = True
    
    def get_text(self) -> str:
        """Get entire buffer content"""
        return "\n".join(self.lines)
    
    def set_text(self, text: str) -> None:
        """Replace entire buffer content"""
        if self.read_only:
            return
        self.lines = text.split("\n")
        self.modified = True
    
    def line_count(self) -> int:
        """Get number of lines"""
        return len(self.lines)
    
    def line_length(self, line: int) -> int:
        """Get length of line"""
        return len(self.get_line(line))
