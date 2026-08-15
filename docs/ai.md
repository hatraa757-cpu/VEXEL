# AI Features Guide

## Overview

VANTA has AI-ready architecture for:
- Code explanation
- Error fixing
- Refactoring suggestions
- Test generation
- Documentation

**Important:** AI is completely optional and not required to use VANTA.

## Enabling AI

### 1. Update Config

```toml
[ai]
enable = true
provider = "openai"
model = "gpt-4"
```

### 2. Set API Key

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

Or add to `~/.bashrc` or `~/.zshrc`:

```bash
export OPENAI_API_KEY="sk-..."
```

### 3. Run VANTA

```bash
vanta file.py
# AI commands now available
```

## AI Providers

### OpenAI (Recommended)

```toml
[ai]
provider = "openai"
model = "gpt-4"  # or gpt-3.5-turbo
```

```bash
export OPENAI_API_KEY="sk-..."
```

### Local Models (Ollama)

```toml
[ai]
provider = "local"
model = "mistral"
endpoint = "http://localhost:11434"
```

```bash
# Install Ollama
brew install ollama

# Start server
ollama serve

# Pull model
ollama pull mistral
```

### Custom Provider

```python
from vanta.ai.providers import AIProvider

class CustomProvider(AIProvider):
    def initialize(self):
        # Your setup
        return True
    
    def explain_code(self, code):
        # Call your API
        return explanation
    
    # Implement other methods...
```

## Available Commands

### Explain Code

```
Ctrl+Shift+E
```

Explains selected code or current function.

**Example:**
```python
# Selected code
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

# AI explains:
# This is a merge sort implementation that recursively divides
# the array in half and merges sorted halves back together.
```

### Fix Error

```
Ctrl+Shift+F
```

Suggests fix for current error.

**Example:**
```python
# Code with error
def calculate(x):
    result = x / 0  # ZeroDivisionError
    return result

# AI suggests:
# Add error handling: if x != 0: result = x / y
# Or provide default value
```

### Refactor Code

```
Ctrl+Shift+R
```

Suggests refactoring improvements.

**Example:**
```python
# Before
if x > 0:
    if y > 0:
        if z > 0:
            return True
return False

# AI suggests:
return all([x > 0, y > 0, z > 0])
```

### Generate Tests

```
Ctrl+Shift+T
```

Generates unit tests for function.

**Example:**
```python
# Function
def add(a, b):
    return a + b

# AI generates:
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### Document Code

```
Ctrl+Shift+D
```

Generates documentation/docstring.

**Example:**
```python
# Before
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# After (AI-generated docstring)
def calculate_average(numbers):
    """Calculate average of a list of numbers.
    
    Args:
        numbers: List of numeric values
    
    Returns:
        float: Average of the numbers
    
    Raises:
        ZeroDivisionError: If list is empty
    """
    return sum(numbers) / len(numbers)
```

## Using AI Programmatically

```python
from vanta.ai.providers import OpenAIProvider

provider = OpenAIProvider(api_key="sk-...")

if provider.is_available():
    code = "def hello(): print('world')"
    
    # Explain
    explanation = provider.explain_code(code)
    print(explanation)
    
    # Fix error
    error = "NameError: name 'x' is not defined"
    fix = provider.fix_code(code, error)
    print(fix)
    
    # Refactor
    refactored = provider.refactor_code(code)
    print(refactored)
    
    # Generate tests
    tests = provider.generate_tests(code)
    print(tests)
    
    # Document
    docs = provider.document_code(code)
    print(docs)
else:
    print("AI provider not available")
```

## Cost Management

### OpenAI Pricing

- GPT-4: ~$0.03 / 1K tokens
- GPT-3.5-turbo: ~$0.0005 / 1K tokens

### Tips to Reduce Costs

1. Use `gpt-3.5-turbo` instead of `gpt-4`
2. Set API usage limits in OpenAI console
3. Use local models for free (Ollama)
4. Cache responses
5. Only request AI when needed

```toml
[ai]
enable = true
provider = "openai"
model = "gpt-3.5-turbo"  # Cheaper than gpt-4
```

## Fallback to Local

```python
from vanta.ai.providers import OpenAIProvider, LocalModelProvider

try:
    provider = OpenAIProvider()
    if not provider.is_available():
        print("OpenAI not available, trying local...")
        provider = LocalModelProvider()
except:
    provider = LocalModelProvider()
```

## Privacy Considerations

**OpenAI:**
- Code is sent to OpenAI servers
- Review [OpenAI privacy policy](https://openai.com/policies/privacy-policy)
- Never send sensitive data

**Local Models (Ollama):**
- Code stays on your machine
- Privacy-focused
- No internet required

## Troubleshooting

### "AI provider not available"

```bash
# Check API key
echo $OPENAI_API_KEY

# Test connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### "API rate limit exceeded"

1. Wait a moment
2. Check OpenAI console for limits
3. Upgrade plan if needed
4. Use local provider (free)

### "Connection timeout"

1. Check internet connection
2. Verify API key
3. Check OpenAI status page
4. Increase timeout: `[ai] timeout = 30000`

## Disabling AI

```toml
[ai]
enable = false
```

Or:

```bash
vanta --safe-mode file.py
```

## Future Enhancements

- Voice commands
- Real-time suggestions
- Code clone detection
- Performance optimization suggestions
- Architectural recommendations
