import pytest
from vanta.search import SearchEngine
from vanta.buffer import Buffer

def test_search_simple():
    buf = Buffer(lines=["hello world", "hello test"])
    engine = SearchEngine(buf)
    matches = engine.search("hello")
    assert len(matches) == 2

def test_search_case_sensitive():
    buf = Buffer(lines=["Hello world", "hello test"])
    engine = SearchEngine(buf)
    matches = engine.search("hello", case_sensitive=True)
    assert len(matches) == 1

def test_search_regex():
    buf = Buffer(lines=["test123", "test456"])
    engine = SearchEngine(buf)
    matches = engine.search(r"test\d+", regex=True)
    assert len(matches) == 2

def test_replace():
    buf = Buffer(lines=["hello world"])
    engine = SearchEngine(buf)
    engine.search("hello")
    count = engine.replace("hi")
    assert count == 1
    assert buf.get_line(0) == "hi world"

def test_replace_all():
    buf = Buffer(lines=["hello hello"])
    engine = SearchEngine(buf)
    engine.search("hello")
    count = engine.replace("hi", all=True)
    assert count == 2
    assert buf.get_line(0) == "hi hi"
