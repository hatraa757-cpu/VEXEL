from dataclasses import dataclass
from typing import List, Optional
from vanta.lsp import LSPClient

@dataclass
class CompletionItem:
    """Single completion item"""
    label: str
    kind: str  # Method, Function, Variable, etc
    detail: Optional[str] = None
    documentation: Optional[str] = None
    insert_text: Optional[str] = None

class CompletionEngine:
    """Handles code completion"""
    
    def __init__(self, lsp_client: Optional[LSPClient] = None):
        self.lsp_client = lsp_client
        self.completions: List[CompletionItem] = []
        self.current_index = 0
    
    def get_completions(self, filepath: str, line: int, col: int) -> List[CompletionItem]:
        """Get completions at position"""
        if not self.lsp_client:
            return []
        
        request_id = self.lsp_client.send_request(
            "textDocument/completion",
            {
                "textDocument": {"uri": f"file://{filepath}"},
                "position": {"line": line, "character": col}
            }
        )
        
        response = self.lsp_client.get_response(request_id)
        if not response or "result" not in response:
            return []
        
        self.completions = []
        for item in response["result"]:
            completion = CompletionItem(
                label=item.get("label", ""),
                kind=item.get("kind", "Unknown"),
                detail=item.get("detail"),
                documentation=item.get("documentation"),
                insert_text=item.get("insertText") or item.get("label")
            )
            self.completions.append(completion)
        
        self.current_index = 0
        return self.completions
    
    def next_completion(self) -> Optional[CompletionItem]:
        """Get next completion"""
        if not self.completions:
            return None
        self.current_index = (self.current_index + 1) % len(self.completions)
        return self.completions[self.current_index]
    
    def prev_completion(self) -> Optional[CompletionItem]:
        """Get previous completion"""
        if not self.completions:
            return None
        self.current_index = (self.current_index - 1) % len(self.completions)
        return self.completions[self.current_index]
    
    def get_current_completion(self) -> Optional[CompletionItem]:
        """Get current completion item"""
        if 0 <= self.current_index < len(self.completions):
            return self.completions[self.current_index]
        return None
    
    def filter_completions(self, prefix: str) -> List[CompletionItem]:
        """Filter completions by prefix"""
        return [c for c in self.completions if c.label.startswith(prefix)]
