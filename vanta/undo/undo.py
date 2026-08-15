from dataclasses import dataclass
from typing import List, Any, Callable
from enum import Enum

class ActionType(Enum):
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"
    SPLIT_LINE = "split_line"
    JOIN_LINE = "join_line"
    CUSTOM = "custom"

@dataclass
class Action:
    """Represents an undoable action"""
    type: ActionType
    line: int
    col: int
    data: Any
    redo_fn: Callable[[], None]
    undo_fn: Callable[[], None]

class UndoManager:
    """Manages undo/redo stack"""
    def __init__(self, max_stack: int = 1000):
        self.undo_stack: List[Action] = []
        self.redo_stack: List[Action] = []
        self.max_stack = max_stack
    
    def push(self, action: Action) -> None:
        """Push action to undo stack"""
        self.undo_stack.append(action)
        self.redo_stack.clear()
        
        if len(self.undo_stack) > self.max_stack:
            self.undo_stack.pop(0)
    
    def undo(self) -> bool:
        """Undo last action"""
        if not self.undo_stack:
            return False
        
        action = self.undo_stack.pop()
        action.undo_fn()
        self.redo_stack.append(action)
        return True
    
    def redo(self) -> bool:
        """Redo last undone action"""
        if not self.redo_stack:
            return False
        
        action = self.redo_stack.pop()
        action.redo_fn()
        self.undo_stack.append(action)
        return True
    
    def can_undo(self) -> bool:
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0
    
    def clear(self) -> None:
        """Clear undo/redo history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
