from dataclasses import dataclass
from typing import List, Optional, Callable

@dataclass
class PaletteItem:
    """Command palette item"""
    name: str
    description: str
    handler: Callable

class CommandPalette:
    """Command palette for quick access to commands"""
    
    def __init__(self):
        self.items: List[PaletteItem] = []
        self.filtered_items: List[PaletteItem] = []
        self.current_index = 0
        self.query = ""
    
    def add_item(self, name: str, description: str, handler: Callable) -> None:
        """Add item to palette"""
        self.items.append(PaletteItem(name, description, handler))
    
    def filter(self, query: str) -> List[PaletteItem]:
        """Filter items by query"""
        self.query = query.lower()
        self.filtered_items = [
            item for item in self.items
            if self.query in item.name.lower() or self.query in item.description.lower()
        ]
        self.current_index = 0
        return self.filtered_items
    
    def next_item(self) -> Optional[PaletteItem]:
        """Move to next item"""
        if not self.filtered_items:
            return None
        self.current_index = (self.current_index + 1) % len(self.filtered_items)
        return self.filtered_items[self.current_index]
    
    def prev_item(self) -> Optional[PaletteItem]:
        """Move to previous item"""
        if not self.filtered_items:
            return None
        self.current_index = (self.current_index - 1) % len(self.filtered_items)
        return self.filtered_items[self.current_index]
    
    def get_current(self) -> Optional[PaletteItem]:
        """Get current item"""
        if 0 <= self.current_index < len(self.filtered_items):
            return self.filtered_items[self.current_index]
        return None
    
    def execute_current(self) -> bool:
        """Execute current item"""
        item = self.get_current()
        if item:
            try:
                item.handler()
                return True
            except Exception:
                return False
        return False
