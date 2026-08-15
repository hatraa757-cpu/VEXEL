# LSP Integration Guide

## What is LSP?

Language Server Protocol enables editors to provide:
- Code completion
- Go to definition
- Find references
- Diagnostics (errors/warnings)
- Hover information
- Code formatting
- Refactoring

## LSP Architecture in VANTA

```
VANTA Editor
    ↓
LSPClient (JSON-RPC)
    ↓
Language Server Process (e.g., pyright)
```

## Supported Language Servers

| Language | Server | Install |
|----------|--------|----------|
| Python | pyright | `npm install -g pyright` |
| JavaScript | tsserver | `npm install -g typescript` |
| TypeScript | tsserver | `npm install -g typescript` |
| Rust | rust-analyzer | Built-in or cargo |
| Go | gopls | `go install github.com/golang/tools/gopls@latest` |
| Java | Custom | Configure in VANTA |

## Configuration

### Enable LSP

```toml
[lsp]
enable = true
timeout = 5000
```

### Configure Language Server

```toml
[lsp.python]
server = "pyright"
args = ["--stdio"]

[lsp.javascript]
server = "tsserver"

[lsp.rust]
server = "rust-analyzer"
```

## Using LSP Features

### Completion

```python
from vanta.completion import CompletionEngine

engine = CompletionEngine(lsp_client)
completions = engine.get_completions(
    filepath="file.py",
    line=5,
    col=10
)

for item in completions:
    print(item.label)        # e.g., "function_name"
    print(item.kind)         # e.g., "Method"
    print(item.detail)       # e.g., "function_name(arg1, arg2) -> str"
    print(item.documentation)
```

### Diagnostics

```python
from vanta.diagnostics import DiagnosticsEngine

engine = DiagnosticsEngine(lsp_client)
diagnostics = engine.get_diagnostics("file.py")

for diag in diagnostics:
    print(f"Line {diag.line}: {diag.message}")
    print(f"Severity: {diag.severity.name}")
```

### Go to Definition

```python
request_id = lsp_client.send_request(
    "textDocument/definition",
    {
        "textDocument": {"uri": "file:///path/file.py"},
        "position": {"line": 5, "character": 10}
    }
)
response = lsp_client.get_response(request_id)
locations = response["result"]
```

### Find References

```python
request_id = lsp_client.send_request(
    "textDocument/references",
    {
        "textDocument": {"uri": "file:///path/file.py"},
        "position": {"line": 5, "character": 10},
        "context": {"includeDeclaration": True}
    }
)
response = lsp_client.get_response(request_id)
references = response["result"]
```

### Hover

```python
request_id = lsp_client.send_request(
    "textDocument/hover",
    {
        "textDocument": {"uri": "file:///path/file.py"},
        "position": {"line": 5, "character": 10}
    }
)
response = lsp_client.get_response(request_id)
hover_info = response["result"]
print(hover_info["contents"])
```

## Implementing Custom LSP

### 1. Create Language Server Manager

```python
from vanta.lsp import ServerManager

manager = ServerManager()

# Check if available
if manager.check_server_available("python"):
    # Start server
    manager.start_server("python")
    client = manager.get_client("python")
else:
    print("Language server not found")
```

### 2. Initialize Server

```python
request_id = client.send_request(
    "initialize",
    {
        "processId": os.getpid(),
        "rootPath": os.getcwd(),
        "capabilities": {
            "textDocument": {
                "completion": {},
                "synchronization": {},
                "definition": {}
            }
        }
    }
)
response = client.get_response(request_id)
```

### 3. Send Notifications

```python
client.send_notification(
    "textDocument/didOpen",
    {
        "textDocument": {
            "uri": "file:///path/file.py",
            "languageId": "python",
            "version": 1,
            "text": open("file.py").read()
        }
    }
)
```

## Error Handling

```python
try:
    client = LSPClient(["pyright", "--stdio"])
    if not client.start():
        print("Failed to start language server")
        # Continue without LSP
        lsp_client = None
except Exception as e:
    print(f"LSP error: {e}")
    lsp_client = None
```

## Performance Tips

1. **Lazy Loading** - Start LSP only when needed
2. **Caching** - Cache completion results
3. **Timeouts** - Set reasonable request timeouts
4. **Filtering** - Filter requests by file type
5. **Background** - Run LSP in background thread

## Debugging LSP

```python
# Enable logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check server output
if client.process:
    stderr = client.process.stderr.read()
    print(f"Server errors: {stderr}")
```

## Common Issues

### Server not found

```bash
# Install pyright
npm install -g pyright

# Check installation
which pyright
pyright --version
```

### Completion not working

1. Check server started: `manager.get_client("python") is not None`
2. Send initialize request first
3. Send didOpen notification
4. Verify position is correct

### Slow responses

1. Increase timeout: `[lsp] timeout = 10000`
2. Check server performance
3. Reduce request frequency
4. Use local server (not remote)

## Reference

- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [Language Servers](https://langserver.org/)
- VANTA `vanta/lsp/` module
