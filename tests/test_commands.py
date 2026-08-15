import pytest
from vanta.commands import CommandRegistry

def test_command_registry():
    registry = CommandRegistry()
    handler = lambda x: x * 2
    registry.register("double", "Double a number", handler)
    assert registry.command_exists("double")

def test_execute_command():
    registry = CommandRegistry()
    registry.register("add", "Add numbers", lambda x, y: x + y)
    result = registry.execute("add", 2, 3)
    assert result == 5

def test_nonexistent_command():
    registry = CommandRegistry()
    result = registry.execute("nonexistent")
    assert result is None
