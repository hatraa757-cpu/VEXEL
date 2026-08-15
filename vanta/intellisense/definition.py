"""Definition provider for go-to-definition"""
from typing import Optional, Tuple
from vanta.lsp import LSPClient

class DefinitionProvider:
    """Finds symbol definitions"""
    
    def __init__(self, lsp_client: Optional[LSPClient] = None):
        self.lsp_client = lsp_client
    
    def get_definition(self, filepath: str, line: int, col: int) -> Optional[Tuple[str, int, int]]:
        """Get definition location"""
        if not self.lsp_client:
            return None
        
        request_id = self.lsp_client.send_request(
            "textDocument/definition",
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
        
        # Handle different response formats
        if isinstance(result, list):
            if not result:
                return None
            loc = result[0]
        else:
            loc = result
        
        return (
            loc["uri"].replace("file://", ""),
            loc["range"]["start"]["line"],
            loc["range"]["start"]["character"]
        )
