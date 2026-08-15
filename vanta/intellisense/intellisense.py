from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from vanta.buffer import Buffer
from vanta.lsp import LSPClient
import re

@dataclass
class CodeContext:
    """Extracted code context for analysis"""
    current_line: str
    previous_lines: List[str]
    next_lines: List[str]
    cursor_position: int
    word_at_cursor: str
    symbol_before_cursor: Optional[str]  # e.g., 'obj.' or 'module.'
    
    def get_full_context(self) -> str:
        """Get full context as string"""
        context_before = "\n".join(self.previous_lines[-10:])
        context_after = "\n".join(self.next_lines[:10])
        return f"{context_before}\n{self.current_line}\n{context_after}"

class IntelliSense:
    """Main IntelliSense engine"""
    
    def __init__(self, lsp_client: Optional[LSPClient] = None, buffer: Optional[Buffer] = None):
        self.lsp_client = lsp_client
        self.buffer = buffer
        self.hover_provider = None
        self.definition_provider = None
        self.references_provider = None
    
    def extract_context(self, line_num: int, col: int) -> CodeContext:
        """Extract code context around cursor"""
        if not self.buffer:
            return CodeContext("", [], [], col, "", None)
        
        current_line = self.buffer.get_line(line_num)
        previous_lines = [
            self.buffer.get_line(i) for i in range(max(0, line_num - 10), line_num)
        ]
        next_lines = [
            self.buffer.get_line(i) for i in range(line_num + 1, min(self.buffer.line_count(), line_num + 10))
        ]
        
        # Extract word at cursor
        word_at_cursor = self._extract_word_at_position(current_line, col)
        
        # Extract symbol before cursor (for member access)
        symbol_before = self._extract_symbol_before(current_line, col)
        
        return CodeContext(
            current_line=current_line,
            previous_lines=previous_lines,
            next_lines=next_lines,
            cursor_position=col,
            word_at_cursor=word_at_cursor,
            symbol_before_cursor=symbol_before
        )
    
    def _extract_word_at_position(self, line: str, col: int) -> str:
        """Extract word at cursor position"""
        if col > len(line):
            return ""
        
        # Find word boundaries
        start = col
        while start > 0 and (line[start - 1].isalnum() or line[start - 1] in '_.'):
            start -= 1
        
        end = col
        while end < len(line) and (line[end].isalnum() or line[end] in '_.'):
            end += 1
        
        return line[start:end]
    
    def _extract_symbol_before(self, line: str, col: int) -> Optional[str]:
        """Extract symbol/object before cursor (e.g., 'obj.' or 'module.')"""
        if col < 2 or line[col - 1] != '.':
            return None
        
        # Find the symbol before the dot
        start = col - 2
        while start >= 0 and (line[start].isalnum() or line[start] in '_[]'):
            start -= 1
        
        return line[start + 1:col - 1]
    
    def get_hover_info(self, filepath: str, line: int, col: int) -> Optional[str]:
        """Get hover information (type hint, docstring, etc)"""
        if not self.lsp_client:
            return self._get_local_hover_info(line, col)
        
        request_id = self.lsp_client.send_request(
            "textDocument/hover",
            {
                "textDocument": {"uri": f"file://{filepath}"},
                "position": {"line": line, "character": col}
            }
        )
        
        response = self.lsp_client.get_response(request_id)
        if response and "result" in response and response["result"]:
            contents = response["result"].get("contents", "")
            if isinstance(contents, dict):
                return contents.get("value", "")
            return str(contents)
        
        return self._get_local_hover_info(line, col)
    
    def _get_local_hover_info(self, line: int, col: int) -> Optional[str]:
        """Get hover info from local analysis (no LSP)"""
        context = self.extract_context(line, col)
        word = context.word_at_cursor
        
        if not word:
            return None
        
        # Simple local analysis
        for prev_line in reversed(context.previous_lines):
            if f"def {word}" in prev_line:
                return f"Function: {word}"
            if f"class {word}" in prev_line:
                return f"Class: {word}"
            if f"{word} =" in prev_line:
                return f"Variable: {word}"
        
        return None
    
    def get_definition_location(self, filepath: str, line: int, col: int) -> Optional[tuple]:
        """Get definition location (file, line, col)"""
        if not self.lsp_client:
            return self._get_local_definition(line, col)
        
        request_id = self.lsp_client.send_request(
            "textDocument/definition",
            {
                "textDocument": {"uri": f"file://{filepath}"},
                "position": {"line": line, "character": col}
            }
        )
        
        response = self.lsp_client.get_response(request_id)
        if response and "result" in response:
            result = response["result"]
            if isinstance(result, list) and result:
                loc = result[0]
                return (
                    loc["uri"].replace("file://", ""),
                    loc["range"]["start"]["line"],
                    loc["range"]["start"]["character"]
                )
            elif isinstance(result, dict):
                return (
                    result["uri"].replace("file://", ""),
                    result["range"]["start"]["line"],
                    result["range"]["start"]["character"]
                )
        
        return self._get_local_definition(line, col)
    
    def _get_local_definition(self, line: int, col: int) -> Optional[tuple]:
        """Find definition locally (no LSP)"""
        if not self.buffer:
            return None
        
        context = self.extract_context(line, col)
        word = context.word_at_cursor
        
        if not word:
            return None
        
        # Search for definition
        for i, line_text in enumerate(self.buffer.lines):
            if f"def {word}(" in line_text or f"class {word}" in line_text:
                return (self.buffer.filepath or "<buffer>", i, 0)
        
        return None
    
    def get_references(self, filepath: str, line: int, col: int) -> List[tuple]:
        """Find all references to symbol"""
        if not self.lsp_client:
            return self._get_local_references(line, col)
        
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
        
        return locations or self._get_local_references(line, col)
    
    def _get_local_references(self, line: int, col: int) -> List[tuple]:
        """Find references locally (no LSP)"""
        if not self.buffer:
            return []
        
        context = self.extract_context(line, col)
        word = context.word_at_cursor
        
        if not word:
            return []
        
        references = []
        for i, line_text in enumerate(self.buffer.lines):
            # Simple pattern matching
            for match in re.finditer(r'\b' + re.escape(word) + r'\b', line_text):
                references.append((
                    self.buffer.filepath or "<buffer>",
                    i,
                    match.start()
                ))
        
        return references
    
    def get_signature_help(self, filepath: str, line: int, col: int) -> Optional[Dict[str, Any]]:
        """Get function signature help"""
        if not self.lsp_client:
            return None
        
        request_id = self.lsp_client.send_request(
            "textDocument/signatureHelp",
            {
                "textDocument": {"uri": f"file://{filepath}"},
                "position": {"line": line, "character": col}
            }
        )
        
        response = self.lsp_client.get_response(request_id)
        return response.get("result") if response else None
    
    def get_document_symbols(self) -> List[Dict[str, Any]]:
        """Get all symbols in document"""
        if not self.buffer or not self.lsp_client:
            return self._get_local_symbols()
        
        request_id = self.lsp_client.send_request(
            "textDocument/documentSymbol",
            {"textDocument": {"uri": f"file://{self.buffer.filepath}"}}
        )
        
        response = self.lsp_client.get_response(request_id)
        return response.get("result", []) if response else self._get_local_symbols()
    
    def _get_local_symbols(self) -> List[Dict[str, Any]]:
        """Extract symbols locally (no LSP)"""
        if not self.buffer:
            return []
        
        symbols = []
        for i, line in enumerate(self.buffer.lines):
            # Find functions
            if match := re.search(r'def\s+(\w+)\s*\(', line):
                symbols.append({
                    "name": match.group(1),
                    "kind": "Function",
                    "location": {"line": i, "character": match.start()}
                })
            # Find classes
            if match := re.search(r'class\s+(\w+)', line):
                symbols.append({
                    "name": match.group(1),
                    "kind": "Class",
                    "location": {"line": i, "character": match.start()}
                })
        
        return symbols
    
    def rename_symbol(self, filepath: str, line: int, col: int, new_name: str) -> bool:
        """Rename symbol globally"""
        if not self.lsp_client:
            return False
        
        request_id = self.lsp_client.send_request(
            "textDocument/rename",
            {
                "textDocument": {"uri": f"file://{filepath}"},
                "position": {"line": line, "character": col},
                "newName": new_name
            }
        )
        
        response = self.lsp_client.get_response(request_id)
        return response is not None and "result" in response
