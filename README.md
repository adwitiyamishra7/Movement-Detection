# C++-style `//` comments for Python (workspace demo)

This workspace provides a small utility that lets you write `//` single-line
comments in Python source similar to C++/Java.

Usage:

- Run a script with preprocessing (safe default):

```powershell
python pycpp.py demo_cpp_comments.py
```

- Force full C++ semantics (danger: will convert floor-division `//` into
  comments):

```powershell
python pycpp.py --force demo_cpp_comments.py
```

- Install import hook at runtime to allow `//` in imported modules:

```python
from cpp_comments import install
install()  # defaults to safe behavior
import your_module  # your_module.py can contain //-style comments
```

Notes:

- Default behavior only converts `//` that are the first non-whitespace
  characters on a line (safe for `a // b` floor-division).
- Use `--force` or `install(force=True)` to convert any `//` outside strings
  (this is closer to C++ semantics but can break code that uses floor-division).
