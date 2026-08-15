import pytest
from vanta.cursor import Cursor
from vanta.buffer import Buffer

def test_cursor_creation():
    cur = Cursor()
    assert cur.line == 0
    assert cur.col == 0

def test_cursor_movement():
    buf = Buffer(lines=["hello", "world"])
    cur = Cursor()
    cur.move_right(buf)
    assert cur.col == 1

def test_cursor_selection():
    cur = Cursor()
    cur.start_selection()
    assert cur.has_selection()
    cur.clear_selection()
    assert not cur.has_selection()

def test_cursor_clamp():
    buf = Buffer(lines=["hello"])
    cur = Cursor(line=10, col=100)
    cur.clamp(buf)
    assert cur.line == 0
    assert cur.col == 5
