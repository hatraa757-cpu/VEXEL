# Configuration Guide

## Configuration File

Location: `~/.config/vanta/config.toml`

VANTA will create this file with defaults if it doesn't exist.

## Default Configuration

```toml
theme = "dark"
tab_size = 4
use_spaces = true
line_numbers = true
word_wrap = false
autosave = false
autosave_delay = 5000  # milliseconds
cursor_style = "block"  # block, underline, bar
mouse_support = true

[keybindings]
ctrl-s = "save"
ctrl-q = "quit"
ctrl-o = "open"
ctrl-n = "new"
ctrl-f = "search"
ctrl-h = "replace"
ctrl-z = "undo"
ctrl-y = "redo"
ctrl-a = "select_all"
ctrl-c = "copy"
ctrl-x = "cut"
ctrl-v = "paste"
# Add your custom keybindings here

[lsp]
enable = true
timeout = 5000  # milliseconds

[plugins]
enabled = true
paths = [
    "~/.config/vanta/plugins",
    "./local_plugins"
]

[ai]
enable = false
provider = "openai"  # openai, local, custom
model = "gpt-4"
# api_key = "sk-..."  # Set via environment variable OPENAI_API_KEY
```

## Configuration Options

### Display Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `theme` | string | "dark" | Theme name |
| `line_numbers` | bool | true | Show line numbers |
| `word_wrap` | bool | false | Enable word wrapping |
| `cursor_style` | string | "block" | Cursor appearance |
| `mouse_support` | bool | true | Enable mouse input |

### Editor Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `tab_size` | int | 4 | Spaces per tab |
| `use_spaces` | bool | true | Use spaces instead of tabs |
| `autosave` | bool | false | Auto-save files |
| `autosave_delay` | int | 5000 | Delay before auto-save (ms) |

### LSP Settings

```toml
[lsp]
enable = true              # Enable language servers
timeout = 5000             # Request timeout (ms)

[lsp.python]
server = "pyright"
args = ["--stdio"]

[lsp.javascript]
server = "tsserver"

[lsp.rust]
server = "rust-analyzer"
```

### Plugin Settings

```toml
[plugins]
enabled = true
paths = ["~/.config/vanta/plugins"]

[plugins.example-plugin]
enable = true
option1 = "value"
```

### AI Settings

```toml
[ai]
enable = false
provider = "openai"
model = "gpt-4"
# Set API key via environment:
# export OPENAI_API_KEY="sk-..."

# Or for local models:
# provider = "local"
# endpoint = "http://localhost:11434"
# model = "mistral"
```

## Custom Keybindings

Add to `[keybindings]` section:

```toml
[keybindings]
# Built-in commands
ctrl-s = "save"
alt-d = "duplicate_line"
ctrl-shift-k = "delete_line"

# Plugin commands
ctrl-alt-p = "my_plugin:custom_command"
```

## Available Key Modifiers

- `ctrl`, `control`, `c`
- `alt`, `option`, `a`
- `shift`, `s`
- `super`, `windows`, `cmd`

## Custom Themes

Create `~/.config/vanta/themes/my_theme.toml`:

```toml
[theme]
name = "my_theme"

[colors]
foreground = "#ffffff"
background = "#000000"
keyword = "#ff00ff"
string = "#00ff00"
comment = "#808080"
number = "#0080ff"
operator = "#ffa500"
error = "#ff0000"
warning = "#ffaa00"
```

Then in `config.toml`:

```toml
theme = "my_theme"
```

## Environment Variables

```bash
# OpenAI API Key
export OPENAI_API_KEY="sk-..."

# Override config path
export VANTA_CONFIG="/path/to/config.toml"

# Override home directory for plugins/themes
export VANTA_HOME="/path/to/vanta"

# Enable debug logging
export VANTA_DEBUG=1
```

## Configuration Precedence

1. Command-line arguments (highest)
2. Environment variables
3. User config file (`~/.config/vanta/config.toml`)
4. Defaults (lowest)

## Programmatic Access

```python
from vanta.config import Config

config = Config()

# Get values
theme = config.get("theme")
tab_size = config.get("tab_size")
lsp_timeout = config.get("lsp.timeout")

# Set values
config.set("theme", "light")
config.set("tab_size", 2)
config.set("lsp.python.server", "basedpyright")

# Save changes
config.save()

# Reset to defaults
config.reset()
```

## Troubleshooting

### Config not loading

1. Check file path: `~/.config/vanta/config.toml`
2. Verify TOML syntax
3. Check permissions: `chmod 644 ~/.config/vanta/config.toml`
4. Run: `vanta --config /path/to/config.toml`

### LSP not working

```toml
[lsp]
enable = false  # Disable LSP
```

Then restart VANTA.

### Plugins not loading

1. Check plugin path in config
2. Verify plugin file has `Plugin` class
3. Check logs: `~/.local/state/vanta/vanta.log`
