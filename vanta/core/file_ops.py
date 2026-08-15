import os
from pathlib import Path
from typing import Optional
from vanta.buffer import Buffer

class FileOperations:
    """File I/O operations"""
    
    @staticmethod
    def open_file(filepath: str) -> Buffer:
        """Open file and return buffer"""
        path = Path(filepath)
        
        if not path.exists():
            buf = Buffer(filepath=filepath)
            return buf
        
        # Check if binary file
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, IOError):
            buf = Buffer(filepath=filepath, read_only=True)
            buf.lines = ["[BINARY FILE - READ ONLY]"]
            return buf
        
        # Check if read-only
        read_only = not os.access(path, os.W_OK)
        
        buf = Buffer(
            lines=content.split('\n') if content else [""],
            filepath=filepath,
            modified=False,
            read_only=read_only
        )
        return buf
    
    @staticmethod
    def save_file(buffer: Buffer) -> bool:
        """Save buffer to file"""
        if buffer.read_only or not buffer.filepath:
            return False
        
        try:
            path = Path(buffer.filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(buffer.get_text())
            
            buffer.modified = False
            return True
        except IOError:
            return False
    
    @staticmethod
    def save_as(buffer: Buffer, new_path: str) -> bool:
        """Save buffer to new file"""
        if buffer.read_only:
            return False
        
        old_path = buffer.filepath
        buffer.filepath = new_path
        
        if FileOperations.save_file(buffer):
            return True
        else:
            buffer.filepath = old_path
            return False
    
    @staticmethod
    def create_file(filepath: str) -> Buffer:
        """Create new file buffer"""
        return Buffer(filepath=filepath, lines=[""])
    
    @staticmethod
    def get_file_info(filepath: str) -> dict:
        """Get file information"""
        path = Path(filepath)
        return {
            'exists': path.exists(),
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
            'size': path.stat().st_size if path.exists() else 0,
            'readable': os.access(path, os.R_OK) if path.exists() else False,
            'writable': os.access(path, os.W_OK) if path.exists() else True,
        }
