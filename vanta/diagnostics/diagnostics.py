from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from vanta.lsp import LSPClient

class DiagnosticSeverity(Enum):
    ERROR = 1
    WARNING = 2
    INFORMATION = 3
    HINT = 4

@dataclass
class Diagnostic:
    """Single diagnostic message"""
    line: int
    col: int
    end_line: int
    end_col: int
    severity: DiagnosticSeverity
    message: str
    code: Optional[str] = None

class DiagnosticsEngine:
    """Manages diagnostics from LSP"""
    
    def __init__(self, lsp_client: Optional[LSPClient] = None):
        self.lsp_client = lsp_client
        self.diagnostics: List[Diagnostic] = []
    
    def get_diagnostics(self, filepath: str) -> List[Diagnostic]:
        """Get diagnostics for file"""
        if not self.lsp_client:
            return []
        
        # Diagnostics come via notification, not request
        # This would need to be updated when notifications are received
        return self.diagnostics
    
    def add_diagnostic(self, diagnostic: Diagnostic) -> None:
        """Add diagnostic"""
        self.diagnostics.append(diagnostic)
    
    def clear_diagnostics(self) -> None:
        """Clear all diagnostics"""
        self.diagnostics.clear()
    
    def get_diagnostics_for_line(self, line: int) -> List[Diagnostic]:
        """Get diagnostics for specific line"""
        return [d for d in self.diagnostics if d.line == line]
    
    def next_diagnostic(self, current_line: int) -> Optional[Diagnostic]:
        """Get next diagnostic"""
        for diag in self.diagnostics:
            if diag.line > current_line:
                return diag
        return self.diagnostics[0] if self.diagnostics else None
    
    def prev_diagnostic(self, current_line: int) -> Optional[Diagnostic]:
        """Get previous diagnostic"""
        for diag in reversed(self.diagnostics):
            if diag.line < current_line:
                return diag
        return self.diagnostics[-1] if self.diagnostics else None
