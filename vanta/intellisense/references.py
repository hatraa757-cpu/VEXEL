"""References provider for find-references"""
from typing import List, Tuple
from vanta.lsp import LSPClient

class ReferencesProvider:
    """Finds all references to a symbol"""
    
    def __init__(self, lsp_client: Optional[LSPClient] = None):
        self.lsp_client = lsp_client
    
    def get_references(self, filepath: str, line: int, col: int) -> List[Tuple[str, int, int]]:
        """Get all references to symbol"""
        if not self.lsp_client:
            return []
        
        request_id = self.lsp_client.send_request(
            "textDocument/references",
            {
                "textDocument": {"uri": f"file://{filepath}"},
                "position": {"line": line, "character": col},
                "context": {"includeDeclaration": True}
            }
        )
        
        response = self.lsp_client.get_response(request_id)
        locations = []
        
        if response and "result" in response:
            for loc in response["result"]:
                locations.append((
                    loc["uri"].replace("file://", ""),
                    loc["range"]["start"]["line"],
                    loc["range"]["start"]["character"]
                ))
        
        return locations
