# VANTA - Terminal Code Editor

## Installation

```bash
git clone https://github.com/hatraa757-cpu/VEXEL.git
cd VEXEL
pip install -e .
```

## Quick Start

```bash
vanta file.py
vanta directory/
vanta --help
```

## Features

- ⚡ Fast terminal editor
- 🧠 LSP + IntelliSense
- 🎨 Syntax highlighting
- 🔌 Plugin system
- ⌨️ Customizable keybindings
- 🔍 Search & Replace
- 📝 Multiple files/tabs
- ↩️ Undo/Redo
- 🤖 AI-ready architecture

## Architecture

- `vanta/buffer/` - Text buffer management
- `vanta/cursor/` - Cursor and selection
- `vanta/undo/` - Undo/Redo system
- `vanta/core/` - File operations
- `vanta/lsp/` - Language server protocol
- `vanta/syntax/` - Syntax highlighting
- `vanta/terminal/` - Terminal UI
- `vanta/commands/` - Command system
- `vanta/plugins/` - Plugin API
- `vanta/config/` - Configuration
- `vanta/ai/` - AI integration

## License

GPL-3.0
