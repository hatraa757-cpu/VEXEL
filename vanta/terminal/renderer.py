import sys
import os
from typing import Optional, List, Tuple

class Renderer:
    """Terminal rendering engine"""
    
    def __init__(self):
        self.width = 80
        self.height = 24
        self.buffer = ""
        self.update_size()
    
    def update_size(self) -> None:
        """Update terminal size"""
        try:
            self.height, self.width = os.popen('stty size', 'r').read().split()
            self.height = int(self.height)
            self.width = int(self.width)
        except:
            pass
    
    def clear(self) -> None:
        """Clear screen"""
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
    
    def move_cursor(self, line: int, col: int) -> None:
        """Move cursor to position"""
        sys.stdout.write(f'\033[{line+1};{col+1}H')
        sys.stdout.flush()
    
    def hide_cursor(self) -> None:
        """Hide cursor"""
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()
    
    def show_cursor(self) -> None:
        """Show cursor"""
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
    
    def set_cursor_style(self, style: str) -> None:
        """Set cursor style: block, underline, bar"""
        styles = {
            'block': '\033[2 q',
            'underline': '\033[4 q',
            'bar': '\033[6 q'
        }
        if style in styles:
            sys.stdout.write(styles[style])
            sys.stdout.flush()
    
    def render_line(self, text: str, x: int = 0, y: int = 0) -> None:
        """Render single line"""
        self.move_cursor(y, x)
        sys.stdout.write(text[:self.width - x])
        sys.stdout.flush()
    
    def render_status_bar(self, status: str) -> None:
        """Render status bar at bottom"""
        self.move_cursor(self.height - 1, 0)
        sys.stdout.write('\033[7m')  # Inverse video
        sys.stdout.write(status.ljust(self.width)[:self.width])
        sys.stdout.write('\033[0m')  # Reset
        sys.stdout.flush()
    
    def render_command_bar(self, text: str) -> None:
        """Render command bar"""
        self.move_cursor(self.height - 2, 0)
        sys.stdout.write(text.ljust(self.width)[:self.width])
        sys.stdout.flush()
    
    def get_input(self) -> Optional[str]:
        """Get single key input (non-blocking)"""
        try:
            import select
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
        except:
            pass
        return None
    
    def reset(self) -> None:
        """Reset terminal"""
        sys.stdout.write('\033[0m')  # Reset all
        sys.stdout.write('\033[?25h')  # Show cursor
        sys.stdout.flush()
