import pytest
from vanta.buffer import Buffer

def test_buffer_creation():
    buf = Buffer()
    assert buf.line_count() == 1
    assert buf.get_line(0) == ""

def test_buffer_insert():
    buf = Buffer()
    buf.insert_char(0, 0, 'a')
    assert buf.get_line(0) == "a"
    assert buf.modified

def test_buffer_delete():
    buf = Buffer(lines=["hello"])
    buf.delete_char(0, 5)
    assert buf.get_line(0) == "hell"

def test_buffer_insert_line():
    buf = Buffer()
    buf.insert_line(1, "new line")
    assert buf.line_count() == 2
    assert buf.get_line(1) == "new line"

def test_buffer_read_only():
    buf = Buffer(read_only=True)
    buf.insert_char(0, 0, 'x')
    assert buf.get_line(0) == ""
    assert not buf.modified
