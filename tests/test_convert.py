import tempfile
import os
from cpp_comments.convert import convert_source


def test_line_start_comment_converted():
    src = """
// this is a comment
x = 1
"""
    out = convert_source(src)
    assert "# this is a comment" in out


def test_inline_floor_division_preserved():
    src = """
x = 10 // 3
"""
    out = convert_source(src)
    assert "//" in out and "#" not in out


def test_force_converts_inline():
    src = """
x = 10 // 3 // comment
"""
    out = convert_source(src, force=True)
    assert "# comment" in out


def test_strings_untouched():
    src = """
text = "this has // inside a string"
text2 = '''triple
string // still inside
end'''
// comment here
"""
    out = convert_source(src)
    assert "this has // inside a string" in out
    assert "# comment here" in out
