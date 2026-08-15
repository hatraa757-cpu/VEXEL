# Plugin Development Guide

## Plugin Basics

Every plugin inherits from `Plugin` base class:

```python
from vanta.plugins import Plugin, PluginInfo

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info = PluginInfo(
            name="my-plugin",
            version="1.0.0",
            description="Awesome plugin",
            author="Your Name"
        )
    
    def initialize(self, editor):
        """Called when plugin loads"""
        self.editor = editor
        # Set up plugin here
        return True  # Success
    
    def shutdown(self):
        """Called when plugin unloads"""
        # Clean up here
        pass
```

## Plugin File Structure

```
~/.config/vanta/plugins/
├── my-plugin/
│   ├── __init__.py      # Plugin entry point
│   ├── plugin.py        # Main plugin class
│   └── README.md        # Documentation
```

## Registering Commands

```python
def initialize(self, editor):
    self.register_command(
        "my_command",
        self.my_command_handler
    )
    return True

def my_command_handler(self):
    # Handle command
    buffer = self.editor.buffers[self.editor.current_buffer_id]
    buffer.insert_char(0, 0, 'x')
```

Command is then available as:
- `my-plugin:my_command` in command palette
- Via keybinding

## Registering Keybindings

```python
def initialize(self, editor):
    self.register_command("my_command", self.handler)
    self.register_keybinding("alt-x", "my-plugin:my_command")
    return True
```

## Listening to Events

```python
def initialize(self, editor):
    self.listen_event("file_opened", self.on_file_opened)
    self.listen_event("file_saved", self.on_file_saved)
    self.listen_event("buffer_changed", self.on_buffer_changed)
    return True

def on_file_opened(self, filepath):
    print(f"File opened: {filepath}")

def on_file_saved(self, filepath):
    print(f"File saved: {filepath}")

def on_buffer_changed(self):
    print("Buffer modified")
```

## Accessing Editor State

```python
# Get current buffer
buffer = self.editor.buffers[self.editor.current_buffer_id]

# Get all buffers
for buffer_id, buffer in self.editor.buffers.items():
    print(f"Buffer: {buffer_id}")
    print(f"Lines: {buffer.line_count()}")
    print(f"Modified: {buffer.modified}")
    print(f"Read-only: {buffer.read_only}")

# Get configuration
theme = self.editor.config.get("theme")

# Get current theme
theme = self.editor.theme_manager.get_current_theme()

# Get LSP client
lsp_client = self.editor.server_manager.get_client("python")
```

## Example: Formatter Plugin

```python
from vanta.plugins import Plugin, PluginInfo

class FormatterPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info = PluginInfo(
            name="formatter",
            version="1.0.0",
            description="Code formatter",
            author="Example"
        )
    
    def initialize(self, editor):
        self.editor = editor
        self.register_command("format", self.format_code)
        self.register_keybinding("alt-f", "formatter:format")
        self.listen_event("file_saved", self.on_save)
        return True
    
    def shutdown(self):
        pass
    
    def format_code(self):
        buffer = self.editor.buffers[self.editor.current_buffer_id]
        code = buffer.get_text()
        
        # Format code (example: black)
        import subprocess
        result = subprocess.run(
            ["black", "-"],
            input=code,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            buffer.set_text(result.stdout)
            buffer.modified = True
    
    def on_save(self, filepath):
        if filepath.endswith(".py"):
            self.format_code()
```

## Example: Git Status Plugin

```python
from vanta.plugins import Plugin, PluginInfo
import subprocess

class GitStatusPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info = PluginInfo(
            name="git-status",
            version="1.0.0",
            description="Show git status in status bar",
            author="Example"
        )
    
    def initialize(self, editor):
        self.editor = editor
        self.register_command("show_git_status", self.show_status)
        return True
    
    def shutdown(self):
        pass
    
    def show_status(self):
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(result.stdout)
        except:
            pass
```

## Plugin Lifecycle

1. **Load** - Plugin file imported, class instantiated
2. **Initialize** - `initialize()` called with editor
3. **Active** - Plugin can register commands, listen to events
4. **Shutdown** - `shutdown()` called when unloading
5. **Unload** - Plugin removed from memory

## Error Handling

Plugin errors don't crash editor:

```python
def initialize(self, editor):
    try:
        self.setup()
    except Exception as e:
        # Log error
        print(f"Plugin init failed: {e}")
        return False  # Disable plugin
    return True
```

## Plugin Configuration

Access plugin config:

```python
def initialize(self, editor):
    config = editor.config
    
    # Get plugin-specific config
    my_option = config.get("plugins.my-plugin.option1")
    
    return True
```

Add to `~/.config/vanta/config.toml`:

```toml
[plugins.my-plugin]
option1 = "value"
enabled = true
```

## Testing Plugin

```python
from vanta.cli.main import Editor
from vanta.config import Config
from vanta.plugins import PluginManager

# Create editor
config = Config()
editor = Editor(config)

# Load plugin
manager = PluginManager()
manager.load_plugin("/path/to/my_plugin.py", editor)

# Test command
editor.command_registry.execute("my-plugin:my_command")

# Cleanup
manager.shutdown_all()
```

## Publishing Plugin

1. Create GitHub repo: `vanta-my-plugin`
2. Include `plugin.py` with `Plugin` class
3. Add README with usage
4. Tag release
5. Users add to config:

```toml
[plugins]
paths = [
    "~/.config/vanta/plugins",
    "/path/to/vanta-my-plugin"
]
```

## Best Practices

1. **Error Handling** - Catch and handle exceptions gracefully
2. **No Blocking** - Don't block editor thread
3. **Logging** - Use logging module
4. **Dependencies** - Minimize external dependencies
5. **Documentation** - Write clear README
6. **Testing** - Include unit tests
7. **Performance** - Cache expensive operations

## API Reference

See `vanta/plugins/plugin.py` for full API.
