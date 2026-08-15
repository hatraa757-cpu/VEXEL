# VANTA Architecture

## Design Philosophy

VANTA is built on these core principles:

1. **Modularity** - Each component is independent and replaceable
2. **Extensibility** - Plugins can extend every aspect
3. **Performance** - No unnecessary processing or rendering
4. **Graceful Degradation** - Works without LSP, AI, or plugins
5. **User Control** - Highly customizable, transparent defaults

## Core Components

### Buffer (`vanta/buffer/`)

Line-based text storage with efficient operations:

```python
buffer = Buffer()
buffer.insert_char(line=0, col=0, char='a')
buffer.insert_line(1, "new line")
buffer.split_line(0, 5)  # Split at column 5
```

**Key Methods:**
- `insert_char(line, col, char)` - Insert character
- `delete_char(line, col)` - Delete backward
- `delete_forward(line, col)` - Delete forward
- `insert_line(line, content)` - Insert new line
- `delete_line(line)` - Delete line
- `split_line(line, col)` - Split line at position
- `join_lines(line)` - Join with next line
- `get_text()` - Get entire buffer
- `set_text(text)` - Replace entire buffer

### Cursor (`vanta/cursor/`)

Cursor position and selection management:

```python
cursor = Cursor(line=0, col=0)
cursor.move_right(buffer)
cursor.start_selection()
cursor.extend_selection()
start, end = cursor.get_selection()
```

**Features:**
- Line/column tracking
- Selection support
- Word navigation
- Home/End/Page Up/Down
- Boundary clamping

### Undo/Redo (`vanta/undo/`)

Action-based undo/redo system:

```python
undo_manager = UndoManager()
action = Action(
    type=ActionType.INSERT,
    line=0, col=0,
    data="text",
    undo_fn=lambda: ...,
    redo_fn=lambda: ...
)
undo_manager.push(action)
undo_manager.undo()
undo_manager.redo()
```

### File Operations (`vanta/core/file_ops.py`)

File I/O with safety checks:

```python
buffer = FileOperations.open_file("file.py")
FileOperations.save_file(buffer)
FileOperations.save_as(buffer, "new_path.py")
```

**Handles:**
- Binary file detection
- Read-only detection
- Encoding (UTF-8)
- Directory creation
- Permission checking

### Syntax Highlighting (`vanta/syntax/`)

Tokenization with ANSI colors:

```python
lexer = Lexer("python")
tokens = lexer.tokenize(code)

highlighter = Highlighter("python")
colored_code = highlighter.highlight(code)
```

**Supported:**
- Keywords, strings, numbers, comments
- Identifiers, operators, punctuation
- Extensible language support
- ANSI color output

### Search (`vanta/search/`)

Pattern matching and replacement:

```python
search_engine = SearchEngine(buffer)
matches = search_engine.search("pattern", regex=True)
search_engine.next_match()
search_engine.replace("replacement", all=True)
```

**Features:**
- Regex support
- Case sensitivity
- Whole word matching
- Replace single/all
- Match navigation

### Commands (`vanta/commands/`)

Command registry and execution:

```python
command_registry = CommandRegistry()
command_registry.register("save", "Save file", save_handler)
command_registry.execute("save")
```

### Keybindings (`vanta/keymap/`)

Configurable keyboard shortcuts:

```python
keymap = Keymap()
keymap.bind("ctrl-s", "save")
command = keymap.get_command("ctrl-s")
```

### LSP (`vanta/lsp/`)

Language Server Protocol client:

```python
client = LSPClient(["pyright", "--stdio"])
client.start()
request_id = client.send_request("textDocument/completion", params)
response = client.get_response(request_id)
client.stop()
```

**Features:**
- JSON-RPC communication
- Async request handling
- Process management
- Multi-language support

### Completion (`vanta/completion/`)

Code completion engine:

```python
completion = CompletionEngine(lsp_client)
completions = completion.get_completions("file.py", line=5, col=10)
completion.filter_completions("prefix")
```

### Diagnostics (`vanta/diagnostics/`)

Error and warning management:

```python
diagnostics = DiagnosticsEngine(lsp_client)
diags = diagnostics.get_diagnostics_for_line(10)
diagnostics.next_diagnostic(current_line)
```

### Plugins (`vanta/plugins/`)

Extensible plugin system:

```python
class MyPlugin(Plugin):
    def initialize(self, editor):
        self.register_command("cmd", handler)
        self.listen_event("file_saved", on_save)
        return True
    
    def shutdown(self):
        pass

manager = PluginManager()
manager.load_plugin("path/to/plugin.py", editor)
```

### Themes (`vanta/themes/`)

Theme management with colors:

```python
theme_manager = ThemeManager()
theme_manager.set_theme("dark")
theme = theme_manager.get_current_theme()
```

### Configuration (`vanta/config/`)

TOML configuration system:

```python
config = Config()
value = config.get("theme")
config.set("tab_size", 2)
config.save()
```

### Terminal (`vanta/terminal/`)

Terminal rendering:

```python
renderer = Renderer()
renderer.clear()
renderer.render_line("text", x=0, y=0)
renderer.render_status_bar("status")
```

### AI (`vanta/ai/`)

AI provider interface:

```python
provider = OpenAIProvider(api_key="...")
if provider.is_available():
    explanation = provider.explain_code(code)
    fix = provider.fix_code(code, error)
```

## Data Flow

```
Terminal Input
    ↓
Keymap (maps key to command)
    ↓
CommandRegistry (executes command)
    ↓
Buffer (modifies text)
    ↓
UndoManager (records action)
    ↓
SearchEngine/LSP (process content)
    ↓
Renderer (displays output)
    ↓
Terminal Output
```

## Extension Points

### Add Custom Language

```python
from vanta.syntax import Lexer, TokenType

class CustomLexer(Lexer):
    def tokenize(self, code):
        # Custom tokenization
        return tokens
```

### Add LSP Server

Update `vanta/lsp/server_manager.py`:

```python
SERVERS = {
    "custom_lang": ["custom-server", "--stdio"]
}
```

### Add Custom Command

```python
editor.command_registry.register(
    "my_command",
    "Description",
    my_handler
)
```

### Add Event Listeners

```python
editor.event_emitter.on("buffer_modified", on_modified)
editor.event_emitter.on("file_saved", on_saved)
```

## Performance Considerations

1. **Buffer Operations** - O(1) line access, O(n) buffer text
2. **Lexing** - Single-pass tokenization
3. **LSP** - Non-blocking requests, response caching
4. **Rendering** - Only changed lines redrawn
5. **Search** - Regex compiled once, reused

## Thread Safety

- Main thread: UI, input handling
- LSP thread: Non-blocking server communication
- Background workers: File I/O, heavy processing

All thread communication via queues.

## Error Handling Strategy

1. Graceful degradation - features disable, not crash
2. User feedback - clear error messages
3. Logging - detailed debug logs
4. Recovery - attempt to continue normal operation

## Testing Strategy

- Unit tests for each module
- Integration tests for major features
- Manual testing for terminal interactions

See `tests/` directory.
