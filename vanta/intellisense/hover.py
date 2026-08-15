"""Hover information provider"""
from typing import Optional
from vanta.lsp import LSPClient

class HoverProvider:
    """Provides hover tooltips"""
    
    def __init__(self, lsp_client: Optional[LSPClient] = None):
        self.lsp_client = lsp_client
    
    def get_hover(self, filepath: str, line: int, col: int) -> Optional[str]:
        """Get hover information"""
        if not self.lsp_client:
            return None
        
        request_id = self.lsp_client.send_request(
            "textDocument/hover",
            {
                "textDocument": {"uri": f"file://{filepath}"},
                "position": {"line": line, "character": col}
            }
        )
        
        response = self.lsp_client.get_response(request_id)
        if not response or "result" not in response:
            return None
        
        result = response["result"]
        if not result:
            return None
        
        contents = result.get("contents", "")
        if isinstance(contents, dict):
            return contents.get("value", "")
        elif isinstance(contents, list):
            return "\n".join(str(c) for c in contents)
        
        return str(contents)
