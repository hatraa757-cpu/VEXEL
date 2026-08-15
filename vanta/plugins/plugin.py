from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass

@dataclass
class PluginInfo:
    name: str
    version: str
    description: str
    author: str

class Plugin(ABC):
    """Base plugin class"""
    
    def __init__(self):
        self.info: Optional[PluginInfo] = None
        self.editor = None
    
    @abstractmethod
    def initialize(self, editor: Any) -> bool:
        """Initialize plugin with editor instance"""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown plugin"""
        pass
    
    def register_command(self, name: str, handler: Callable) -> None:
        """Register command"""
        if self.editor and hasattr(self.editor, 'command_registry'):
            self.editor.command_registry.register(name, f"{self.info.name}:{name}", handler)
    
    def register_keybinding(self, key: str, command: str) -> None:
        """Register keybinding"""
        if self.editor and hasattr(self.editor, 'keymap'):
            self.editor.keymap.bind(key, command)
    
    def listen_event(self, event_name: str, handler: Callable) -> None:
        """Listen to editor event"""
        if self.editor and hasattr(self.editor, 'event_emitter'):
            self.editor.event_emitter.on(event_name, handler)

class PluginManager:
    """Manages plugins"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.load_paths: List[str] = []
    
    def add_load_path(self, path: str) -> None:
        """Add path to search for plugins"""
        self.load_paths.append(path)
    
    def load_plugin(self, filepath: str, editor: Any) -> bool:
        """Load plugin from file"""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("plugin", filepath)
            if not spec or not spec.loader:
                return False
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for Plugin subclass
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                    plugin = attr()
                    plugin.editor = editor
                    if plugin.initialize(editor):
                        self.plugins[plugin.info.name] = plugin
                        return True
            return False
        except Exception:
            return False
    
    def unload_plugin(self, name: str) -> bool:
        """Unload plugin"""
        if name in self.plugins:
            self.plugins[name].shutdown()
            del self.plugins[name]
            return True
        return False
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin by name"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> Dict[str, Plugin]:
        """List all loaded plugins"""
        return self.plugins.copy()
    
    def shutdown_all(self) -> None:
        """Shutdown all plugins"""
        for plugin in list(self.plugins.values()):
            plugin.shutdown()
        self.plugins.clear()
