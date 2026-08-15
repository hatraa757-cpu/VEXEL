import shutil
from typing import Optional, Dict, List
from .client import LSPClient

class ServerManager:
    """Manages language server instances"""
    
    SERVERS = {
        "python": ["pyright", "--stdio"],
        "javascript": ["node", "--input-type=module"],
        "typescript": ["tsserver"],
        "rust": ["rust-analyzer"],
        "go": ["gopls"],
        "java": ["java", "-cp", "."],
    }
    
    def __init__(self):
        self.clients: Dict[str, LSPClient] = {}
        self.available_servers: Dict[str, bool] = {}
    
    def check_server_available(self, language: str) -> bool:
        """Check if language server is available"""
        if language not in self.SERVERS:
            return False
        
        if language in self.available_servers:
            return self.available_servers[language]
        
        command = self.SERVERS[language]
        executable = command[0]
        available = shutil.which(executable) is not None
        self.available_servers[language] = available
        return available
    
    def start_server(self, language: str) -> bool:
        """Start language server for language"""
        if language in self.clients:
            return True
        
        if not self.check_server_available(language):
            return False
        
        client = LSPClient(self.SERVERS[language])
        if client.start():
            self.clients[language] = client
            return True
        return False
    
    def stop_server(self, language: str) -> None:
        """Stop language server"""
        if language in self.clients:
            self.clients[language].stop()
            del self.clients[language]
    
    def get_client(self, language: str) -> Optional[LSPClient]:
        """Get client for language"""
        return self.clients.get(language)
    
    def stop_all(self) -> None:
        """Stop all servers"""
        for language in list(self.clients.keys()):
            self.stop_server(language)
