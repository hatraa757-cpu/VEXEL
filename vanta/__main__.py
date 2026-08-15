"""VANTA - Terminal Code Editor with LSP & IntelliSense

Fast, modern terminal editor with language server protocol support,
code intelligence, syntax highlighting, and extensible plugin system.

Usage:
    vanta [FILES...] [OPTIONS]

Examples:
    vanta file.py
    vanta file1.py file2.py
    vanta --help
    vanta --safe-mode

Features:
    ⚡ Fast terminal editor
    🧠 LSP + IntelliSense
    🎨 Syntax highlighting
    🔌 Plugin system
    ⌨️  Customizable keybindings
    🔍 Search & Replace
    📝 Multiple files/tabs
    ↩️  Undo/Redo
    🤖 AI-ready architecture
"""

from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
