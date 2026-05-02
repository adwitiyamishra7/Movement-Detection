"""Small CLI runner which preprocesses Python files to allow C++-style
`//` comments.

Usage:
    python pycpp.py [--force] file.py [args...]

If --force is passed, any '//' outside strings will be treated as comment
start (C++ semantics). Otherwise only '//' as the first non-whitespace on a
line will be converted (safer; preserves ``a // b`` floor division).
"""
import sys
import runpy
import tempfile
import os
from cpp_comments.convert import convert_source


def main(argv=None):
    argv = argv or sys.argv[1:]
    force = False
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--force":
        force = True
        argv = argv[1:]
    if not argv:
        print("Usage: pycpp.py [--force] script.py [args...]")
        return 2
    script, *script_args = argv
    # read and convert
    with open(script, "r", encoding="utf-8") as f:
        src = f.read()
    converted = convert_source(src, force=force)

    # write to a temporary file and execute so __file__ etc behave like normal
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp.write(converted)
        tmp_path = tmp.name

    # adjust argv and run
    old_argv = sys.argv
    try:
        sys.argv = [script] + script_args
        runpy.run_path(tmp_path, run_name="__main__")
    finally:
        sys.argv = old_argv
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
