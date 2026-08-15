import pytest
from vanta.undo import UndoManager, Action, ActionType

def test_undo_manager_creation():
    manager = UndoManager()
    assert not manager.can_undo()
    assert not manager.can_redo()

def test_undo_redo():
    manager = UndoManager()
    action = Action(
        type=ActionType.INSERT,
        line=0,
        col=0,
        data="test",
        undo_fn=lambda: None,
        redo_fn=lambda: None
    )
    manager.push(action)
    assert manager.can_undo()
    assert manager.undo()
    assert manager.can_redo()
    assert manager.redo()

def test_undo_clears_redo():
    manager = UndoManager()
    action = Action(
        type=ActionType.INSERT,
        line=0,
        col=0,
        data="test",
        undo_fn=lambda: None,
        redo_fn=lambda: None
    )
    manager.push(action)
    manager.undo()
    manager.push(action)
    assert not manager.can_redo()
