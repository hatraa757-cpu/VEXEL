from abc import ABC, abstractmethod
from typing import Optional, List
from enum import Enum

class AIProviderType(Enum):
    OPENAI = "openai"
    LOCAL = "local"
    CUSTOM = "custom"

class AIProvider(ABC):
    """Abstract AI provider"""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize provider"""
        pass
    
    @abstractmethod
    def explain_code(self, code: str) -> Optional[str]:
        """Explain code snippet"""
        pass
    
    @abstractmethod
    def fix_code(self, code: str, error: str) -> Optional[str]:
        """Suggest fix for error"""
        pass
    
    @abstractmethod
    def refactor_code(self, code: str) -> Optional[str]:
        """Refactor code"""
        pass
    
    @abstractmethod
    def generate_tests(self, code: str) -> Optional[str]:
        """Generate tests for code"""
        pass
    
    @abstractmethod
    def document_code(self, code: str) -> Optional[str]:
        """Generate documentation for code"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass

class OpenAIProvider(AIProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.model = "gpt-4"
    
    def initialize(self) -> bool:
        import os
        self.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        return self.api_key is not None
    
    def explain_code(self, code: str) -> Optional[str]:
        if not self.is_available():
            return None
        # Implementation would use OpenAI API
        return f"Explanation for: {code[:50]}..."
    
    def fix_code(self, code: str, error: str) -> Optional[str]:
        if not self.is_available():
            return None
        return f"Fix for error: {error}"
    
    def refactor_code(self, code: str) -> Optional[str]:
        if not self.is_available():
            return None
        return code
    
    def generate_tests(self, code: str) -> Optional[str]:
        if not self.is_available():
            return None
        return "# Generated tests\n"
    
    def document_code(self, code: str) -> Optional[str]:
        if not self.is_available():
            return None
        return "# Generated documentation\n"
    
    def is_available(self) -> bool:
        return self.api_key is not None

class LocalModelProvider(AIProvider):
    """Local model provider (e.g., Ollama)"""
    
    def __init__(self, model: str = "mistral", endpoint: str = "http://localhost:11434"):
        self.model = model
        self.endpoint = endpoint
    
    def initialize(self) -> bool:
        import urllib.request
        try:
            urllib.request.urlopen(f"{self.endpoint}/api/tags", timeout=2)
            return True
        except:
            return False
    
    def explain_code(self, code: str) -> Optional[str]:
        if not self.is_available():
            return None
        return f"Local explanation for: {code[:50]}..."
    
    def fix_code(self, code: str, error: str) -> Optional[str]:
        if not self.is_available():
            return None
        return f"Local fix for error: {error}"
    
    def refactor_code(self, code: str) -> Optional[str]:
        if not self.is_available():
            return None
        return code
    
    def generate_tests(self, code: str) -> Optional[str]:
        if not self.is_available():
            return None
        return "# Generated tests\n"
    
    def document_code(self, code: str) -> Optional[str]:
        if not self.is_available():
            return None
        return "# Generated documentation\n"
    
    def is_available(self) -> bool:
        return self.initialize()

class NoOpAIProvider(AIProvider):
    """No-op provider when AI is disabled"""
    
    def initialize(self) -> bool:
        return True
    
    def explain_code(self, code: str) -> Optional[str]:
        return None
    
    def fix_code(self, code: str, error: str) -> Optional[str]:
        return None
    
    def refactor_code(self, code: str) -> Optional[str]:
        return None
    
    def generate_tests(self, code: str) -> Optional[str]:
        return None
    
    def document_code(self, code: str) -> Optional[str]:
        return None
    
    def is_available(self) -> bool:
        return False
