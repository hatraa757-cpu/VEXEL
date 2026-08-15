from dataclasses import dataclass
from typing import Optional
from vanta.buffer import Buffer

@dataclass
class Cursor:
    """Cursor position and selection"""
    line: int = 0
    col: int = 0
    sel_start: Optional[tuple[int, int]] = None  # (line, col) for selection
    sel_end: Optional[tuple[int, int]] = None
    
    def has_selection(self) -> bool:
        """Check if text is selected"""
        return self.sel_start is not None and self.sel_end is not None
    
    def get_selection(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Get selection bounds (start, end)"""
        if not self.has_selection():
            return ((self.line, self.col), (self.line, self.col))
        start = self.sel_start
        end = self.sel_end
        if start > end:
            start, end = end, start
        return (start, end)
    
    def start_selection(self) -> None:
        """Begin selection at current position"""
        self.sel_start = (self.line, self.col)
        self.sel_end = (self.line, self.col)
    
    def extend_selection(self) -> None:
        """Extend selection to current position"""
        if self.sel_start is None:
            self.sel_start = (self.line, self.col)
        self.sel_end = (self.line, self.col)
    
    def clear_selection(self) -> None:
        """Clear selection"""
        self.sel_start = None
        self.sel_end = None
    
    def move_left(self, buffer: Buffer, shift: bool = False) -> None:
        """Move cursor left"""
        if self.col > 0:
            self.col -= 1
        elif self.line > 0:
            self.line -= 1
            self.col = buffer.line_length(self.line)
        
        if shift:
            self.extend_selection()
        else:
            self.clear_selection()
    
    def move_right(self, buffer: Buffer, shift: bool = False) -> None:
        """Move cursor right"""
        line_len = buffer.line_length(self.line)
        if self.col < line_len:
            self.col += 1
        elif self.line < buffer.line_count() - 1:
            self.line += 1
            self.col = 0
        
        if shift:
            self.extend_selection()
        else:
            self.clear_selection()
    
    def move_up(self, buffer: Buffer, shift: bool = False) -> None:
        """Move cursor up"""
        if self.line > 0:
            self.line -= 1
            self.col = min(self.col, buffer.line_length(self.line))
        
        if shift:
            self.extend_selection()
        else:
            self.clear_selection()
    
    def move_down(self, buffer: Buffer, shift: bool = False) -> None:
        """Move cursor down"""
        if self.line < buffer.line_count() - 1:
            self.line += 1
            self.col = min(self.col, buffer.line_length(self.line))
        
        if shift:
            self.extend_selection()
        else:
            self.clear_selection()
    
    def move_home(self, buffer: Buffer, shift: bool = False) -> None:
        """Move to start of line"""
        self.col = 0
        if shift:
            self.extend_selection()
        else:
            self.clear_selection()
    
    def move_end(self, buffer: Buffer, shift: bool = False) -> None:
        """Move to end of line"""
        self.col = buffer.line_length(self.line)
        if shift:
            self.extend_selection()
        else:
            self.clear_selection()
    
    def move_word_forward(self, buffer: Buffer, shift: bool = False) -> None:
        """Move to next word"""
        line = buffer.get_line(self.line)
        col = self.col
        # Skip current word
        while col < len(line) and line[col] != ' ':
            col += 1
        # Skip spaces
        while col < len(line) and line[col] == ' ':
            col += 1
        self.col = col
        
        if shift:
            self.extend_selection()
        else:
            self.clear_selection()
    
    def move_word_back(self, buffer: Buffer, shift: bool = False) -> None:
        """Move to previous word"""
        line = buffer.get_line(self.line)
        col = self.col - 1
        # Skip spaces
        while col >= 0 and line[col] == ' ':
            col -= 1
        # Skip current word
        while col >= 0 and line[col] != ' ':
            col -= 1
        self.col = max(0, col + 1)
        
        if shift:
            self.extend_selection()
        else:
            self.clear_selection()
    
    def clamp(self, buffer: Buffer) -> None:
        """Clamp cursor to valid position"""
        self.line = max(0, min(self.line, buffer.line_count() - 1))
        self.col = max(0, min(self.col, buffer.line_length(self.line)))
