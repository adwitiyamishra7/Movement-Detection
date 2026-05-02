import importlib
import importlib.util
import sys
import tempfile
import os
from cpp_comments import install, uninstall


def test_importer_converts(tmp_path, monkeypatch):
    # create a module file that uses // at start of line
    module_code = """
// note comment
VALUE = 42
"""
    module_path = tmp_path / "mymod.py"
    module_path.write_text(module_code, encoding="utf-8")

    # ensure temp dir is on sys.path
    sys.path.insert(0, str(tmp_path))
    try:
        install()
        mod = importlib.import_module("mymod")
        assert getattr(mod, "VALUE") == 42
    finally:
        uninstall()
        try:
            sys.path.remove(str(tmp_path))
        except Exception:
            pass
