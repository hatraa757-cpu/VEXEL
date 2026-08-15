import sys
import argparse
from pathlib import Path
from vanta.core.file_ops import FileOperations
from vanta.buffer import Buffer
from vanta.cursor import Cursor
from vanta.config import Config
from vanta.terminal import Renderer
from vanta.syntax import Highlighter
from vanta.commands import CommandRegistry
from vanta.keymap import Keymap
from vanta.lsp import ServerManager
from vanta.plugins import PluginManager
from vanta.themes import ThemeManager
from vanta.ai.providers import NoOpAIProvider, OpenAIProvider

class Editor:
    """Main VANTA editor"""
    
    def __init__(self, config: Config, safe_mode: bool = False):
        self.config = config
        self.safe_mode = safe_mode
        self.renderer = Renderer()
        self.command_registry = CommandRegistry()
        self.keymap = Keymap()
        self.theme_manager = ThemeManager()
        self.server_manager = ServerManager()
        self.plugin_manager = PluginManager()
        
        # Initialize AI
        if safe_mode or not config.get("ai.enable", False):
            self.ai_provider = NoOpAIProvider()
        else:
            self.ai_provider = OpenAIProvider()
        
        self.buffers = {}
        self.current_buffer_id = None
        self.running = False
        
        self.register_commands()
    
    def register_commands(self) -> None:
        """Register built-in commands"""
        self.command_registry.register("save", "Save current file", self.save_file)
        self.command_registry.register("quit", "Quit editor", self.quit)
        self.command_registry.register("open", "Open file", self.open_file)
        self.command_registry.register("new", "Create new file", self.new_file)
    
    def open_file(self, filepath: str) -> bool:
        """Open file"""
        buffer = FileOperations.open_file(filepath)
        buffer_id = filepath
        self.buffers[buffer_id] = buffer
        self.current_buffer_id = buffer_id
        return True
    
    def new_file(self, filepath: str = "untitled") -> bool:
        """Create new file"""
        buffer = FileOperations.create_file(filepath)
        self.buffers[filepath] = buffer
        self.current_buffer_id = filepath
        return True
    
    def save_file(self) -> bool:
        """Save current file"""
        if self.current_buffer_id and self.current_buffer_id in self.buffers:
            buffer = self.buffers[self.current_buffer_id]
            return FileOperations.save_file(buffer)
        return False
    
    def quit(self) -> None:
        """Quit editor"""
        self.running = False
    
    def run(self) -> None:
        """Run editor main loop"""
        self.running = True
        self.renderer.clear()
        self.renderer.hide_cursor()
        
        try:
            while self.running:
                self.render()
                key = self.renderer.get_input()
                if key:
                    self.handle_key(key)
        finally:
            self.renderer.show_cursor()
            self.renderer.clear()
            self.renderer.reset()
    
    def render(self) -> None:
        """Render editor"""
        if self.current_buffer_id not in self.buffers:
            return
        
        buffer = self.buffers[self.current_buffer_id]
        highlighter = Highlighter("python")
        
        # Render lines
        for i, line in enumerate(buffer.lines[:self.renderer.height - 2]):
            highlighted = highlighter.highlight_line(line, i)
            self.renderer.render_line(f"{i+1:4d} | {highlighted}", 0, i)
        
        # Render status bar
        status = f" {self.current_buffer_id} | Lines: {buffer.line_count()} | Modified: {buffer.modified}"
        self.renderer.render_status_bar(status)
    
    def handle_key(self, key: str) -> None:
        """Handle keyboard input"""
        # Implement key handling
        pass
    
    def shutdown(self) -> None:
        """Shutdown editor"""
        self.plugin_manager.shutdown_all()
        self.server_manager.stop_all()

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description="VANTA Terminal Code Editor")
    parser.add_argument("files", nargs="*", help="Files to open")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--config", help="Config file path")
    parser.add_argument("--safe-mode", action="store_true", help="Run without plugins and AI")
    
    args = parser.parse_args()
    
    if args.version:
        print("VANTA 0.1.0")
        return 0
    
    config = Config(args.config)
    editor = Editor(config, args.safe_mode)
    
    try:
        for filepath in args.files:
            editor.open_file(filepath)
        
        if not editor.buffers:
            editor.new_file()
        
        editor.run()
    finally:
        editor.shutdown()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
