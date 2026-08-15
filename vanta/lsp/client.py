import json
import subprocess
from typing import Optional, Dict, Any, List
import threading
import queue

class LSPClient:
    """JSON-RPC client for LSP communication"""
    
    def __init__(self, command: List[str]):
        self.command = command
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
        self.pending_responses: Dict[int, Any] = {}
        self.reader_thread: Optional[threading.Thread] = None
        self.running = False
    
    def start(self) -> bool:
        """Start language server process"""
        try:
            self.process = subprocess.Popen(
                self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            self.running = True
            self.reader_thread = threading.Thread(target=self._read_responses, daemon=True)
            self.reader_thread.start()
            return True
        except Exception:
            return False
    
    def stop(self) -> None:
        """Stop language server process"""
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
    
    def send_request(self, method: str, params: Optional[Dict] = None) -> int:
        """Send JSON-RPC request"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        if self.process and self.process.stdin:
            body = json.dumps(request)
            header = f"Content-Length: {len(body)}\r\n\r\n"
            try:
                self.process.stdin.write(header + body)
                self.process.stdin.flush()
            except Exception:
                pass
        
        return self.request_id
    
    def send_notification(self, method: str, params: Optional[Dict] = None) -> None:
        """Send JSON-RPC notification (no response expected)"""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }
        
        if self.process and self.process.stdin:
            body = json.dumps(notification)
            header = f"Content-Length: {len(body)}\r\n\r\n"
            try:
                self.process.stdin.write(header + body)
                self.process.stdin.flush()
            except Exception:
                pass
    
    def _read_responses(self) -> None:
        """Read responses from language server"""
        if not self.process or not self.process.stdout:
            return
        
        while self.running:
            try:
                line = self.process.stdout.readline()
                if not line:
                    break
                
                if line.startswith("Content-Length:"):
                    content_length = int(line.split(":")[1].strip())
                    self.process.stdout.readline()  # Skip empty line
                    body = self.process.stdout.read(content_length)
                    
                    try:
                        response = json.loads(body)
                        if "id" in response:
                            self.pending_responses[response["id"]] = response
                    except json.JSONDecodeError:
                        pass
            except Exception:
                continue
    
    def get_response(self, request_id: int, timeout: float = 5.0) -> Optional[Dict]:
        """Get response for request"""
        import time
        start = time.time()
        
        while time.time() - start < timeout:
            if request_id in self.pending_responses:
                return self.pending_responses.pop(request_id)
            time.sleep(0.01)
        
        return None
