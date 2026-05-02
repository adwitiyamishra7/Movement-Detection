"""Utilities to allow C++-style '//' comments in Python source.

API:
- convert_source(src, force=False)
- install(force=False) — install import hook
- uninstall() — remove import hook
"""
from .convert import convert_source, convert_file_inplace
from .importer import install, uninstall

__all__ = ["convert_source", "convert_file_inplace", "install", "uninstall"]
