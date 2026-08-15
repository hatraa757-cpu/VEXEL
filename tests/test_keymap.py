import pytest
from vanta.keymap import Keymap

def test_keymap_defaults():
    km = Keymap()
    assert km.get_command("ctrl-s") == "save"
    assert km.get_command("ctrl-q") == "quit"

def test_keymap_bind():
    km = Keymap()
    km.bind("alt-x", "custom_command")
    assert km.get_command("alt-x") == "custom_command"

def test_keymap_unbind():
    km = Keymap()
    km.unbind("ctrl-s")
    assert km.get_command("ctrl-s") is None

def test_keymap_load_from_dict():
    km = Keymap()
    config = {"ctrl-d": "duplicate_line"}
    km.load_from_dict(config)
    assert km.get_command("ctrl-d") == "duplicate_line"
