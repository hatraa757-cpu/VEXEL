# VANTA - Terminal Code Editor

⚡ **Fast. Smart. Extensible.**

A modern terminal code editor with LSP support, IntelliSense, syntax highlighting, and AI-ready architecture. Built to compete with nano/micro while bringing real code intelligence.

## 🎯 Features

- ⚡ Lightning-fast terminal editor
- 🧠 LSP + IntelliSense (real code completion)
- 🎨 Syntax highlighting (15+ languages)
- 🔌 Extensible plugin system
- ⌨️  Customizable keybindings
- 🔍 Search & Replace (regex support)
- 📑 Multiple files/tabs
- ↩️  Undo/Redo
- 🤖 AI-ready architecture
- 🎭 Themes (Light/Dark)
- ⚙️  Modular, maintainable codebase

## 📦 Installation

```bash
git clone https://github.com/hatraa757-cpu/VEXEL.git
cd VEXEL
pip install -e .
```

## 🚀 Quick Start

```bash
# Open a file
vanta file.py

# Open multiple files
vanta file1.py file2.js file3.json

# Create new file
vanta new_file.py

# Safe mode (no plugins/AI)
vanta --safe-mode file.py

# Show help
vanta --help

# Show version
vanta --version
```

## ⌨️  Default Keybindings

| Key | Action |
|-----|--------|
| `Ctrl+S` | Save file |
| `Ctrl+Q` | Quit |
| `Ctrl+O` | Open file |
| `Ctrl+N` | New file |
| `Ctrl+F` | Search |
| `Ctrl+H` | Replace |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+A` | Select all |
| `Ctrl+C` | Copy |
| `Ctrl+X` | Cut |
| `Ctrl+V` | Paste |
| `Ctrl+Space` | AutoComplete |
| `F12` | Go to Definition |
| `Shift+F12` | Find References |
| `Ctrl+K` | Command Palette |

## 📁 Project Structure

```
vanta/
├── buffer/          # Text buffer management
├── cursor/          # Cursor and selection
├── undo/            # Undo/Redo system
├── core/            # File operations
├── lsp/             # Language Server Protocol
├── syntax/          # Syntax highlighting
├── terminal/        # Terminal rendering
├── commands/        # Command system
├── keymap/          # Key binding management
├── completion/      # Code completion
├── diagnostics/     # Error/warning display
├── search/          # Search & Replace
├── plugins/         # Plugin API
├── themes/          # Theme system
├── config/          # Configuration management
├── ai/              # AI providers
├── ui/              # UI components
└── cli/             # CLI entry point

tests/               # Unit tests
```

## 🔧 Configuration

Configuration file: `~/.config/vanta/config.toml`

```toml
theme = "dark"
tab_size = 4
use_spaces = true
line_numbers = true
word_wrap = false
autosave = false
cursor_style = "block"

[lsp]
enable = true
timeout = 5000

[plugins]
enabled = true
paths = []

[ai]
enable = false
provider = "openai"
model = "gpt-4"
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_buffer.py

# With coverage
pytest --cov=vanta
```

## 🤖 Language Server Support

VANTA auto-detects and uses available language servers:

- **Python**: pyright, basedpyright
- **JavaScript/TypeScript**: tsserver
- **Rust**: rust-analyzer
- **Go**: gopls
- **Java**: Language server (configurable)

No LSP required to use VANTA - it works perfectly without them!

## 🎨 Supported Languages (Syntax Highlighting)

- Python
- JavaScript
- TypeScript
- JSON
- HTML
- CSS
- Bash
- Markdown
- YAML
- Rust
- C
- C++
- Java
- Go
- And more!

## 🔌 Plugin Development

Create a simple plugin:

```python
from vanta.plugins import Plugin, PluginInfo

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info = PluginInfo(
            name="my-plugin",
            version="1.0.0",
            description="My awesome plugin",
            author="Your Name"
        )
    
    def initialize(self, editor):
        self.editor = editor
        self.register_command("my_command", self.my_handler)
        return True
    
    def shutdown(self):
        pass
    
    def my_handler(self):
        print("Plugin works!")
```

See `docs/plugins.md` for full plugin API.

## 🤖 AI Integration

VANTA has AI-ready architecture (optional):

```python
from vanta.ai.providers import OpenAIProvider

provider = OpenAIProvider(api_key="sk-...")
if provider.is_available():
    explanation = provider.explain_code(code)
    fix = provider.fix_code(code, error)
    refactored = provider.refactor_code(code)
```

AI is **completely optional** - works great without it!

## 🐛 Error Handling

VANTA gracefully handles:

- Missing language servers
- Invalid configuration
- File permission issues
- Binary files
- Large files
- Terminal resize
- Plugin errors

Errors are logged to `~/.local/state/vanta/vanta.log`

## 📖 Documentation

- [Architecture Guide](docs/architecture.md)
- [Configuration](docs/configuration.md)
- [Plugin Development](docs/plugins.md)
- [LSP Integration](docs/lsp.md)
- [AI Features](docs/ai.md)

## 📝 License

GPL-3.0 - See LICENSE file

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md

## ⚠️ Security

See SECURITY.md for security policy.

## 📧 Support

Open an issue on GitHub or check existing issues.

---

**Built with ❤️ for developers who love the terminal**
