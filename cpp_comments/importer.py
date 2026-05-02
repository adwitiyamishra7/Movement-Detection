"""Import hook that preprocesses module source to accept '//' as comments.

Call `install(force=False)` to install a meta-path finder that will convert
source before it is compiled. `force=True` enables C++-like behavior (convert
any // outside strings) — that may break floor-division uses.
"""
import importlib.abc
import importlib.machinery
import importlib.util
import sys
from typing import Optional
from .convert import convert_source


class CPPCommentLoader(importlib.machinery.SourceFileLoader):
    def __init__(self, fullname, path, *, force=False):
        super().__init__(fullname, path)
        self.force = force

    def get_data(self, path):
        data = super().get_data(path)
        try:
            text = data.decode("utf-8")
        except Exception:
            return data
        converted = convert_source(text, force=self.force)
        return converted.encode("utf-8")


class CPPFinder(importlib.abc.MetaPathFinder):
    def __init__(self, *, force=False):
        self.force = force

    def find_spec(self, fullname, path, target=None):
        # delegate to standard machinery to find a spec, then wrap loader
        try:
            spec = importlib.util.find_spec(fullname)
        except Exception:
            return None
        if spec is None:
            return None
        if spec.origin is None or not spec.origin.endswith(".py"):
            return None
        # return a new spec using our loader
        loader = CPPCommentLoader(fullname, spec.origin, force=self.force)
        new_spec = importlib.util.spec_from_file_location(fullname, spec.origin, loader=loader)
        return new_spec


_installed_finder: Optional[CPPFinder] = None


def install(force: bool = False):
    """Install the import hook. Returns the finder installed so it can be
    uninstalled later (via uninstall)."""
    global _installed_finder
    if _installed_finder is not None:
        raise RuntimeError("cpp_comments importer already installed")
    finder = CPPFinder(force=force)
    sys.meta_path.insert(0, finder)
    _installed_finder = finder
    return finder


def uninstall():
    global _installed_finder
    if _installed_finder is None:
        return
    try:
        sys.meta_path.remove(_installed_finder)
    except ValueError:
        pass
    _installed_finder = None
