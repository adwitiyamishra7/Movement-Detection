"""Utilities to convert C++-style '//' comments into Python '#' comments.

Conversion rules (safe default):
- Only convert '//' that begin the comment at the start of a line (i.e., the first
  non-whitespace characters on that line). This avoids turning floor-division
  operators (``a // b``) into comments accidentally.

Optional behavior:
- If `force=True`, convert any '//' outside strings into a comment start
  (C++ semantics); use with care.

The converter avoids touching '//' sequences that appear inside string literals
including single-line and triple-quoted strings.
"""
from typing import Tuple


def convert_source(source: str, force: bool = False) -> str:
    """Return a new source string where C++-style '//' comments are converted
    into Python-style '#' comments.

    Args:
        source: original Python source code
        force: if True, treat any '//' outside strings as the start of a comment
               (C++ semantics); if False (default), only convert '//' when it is
               the first non-whitespace content on the line.
    """
    out_chars = []
    i = 0
    n = len(source)
    # track if we are inside a triple-quoted or single/double-quoted string
    in_string = False
    string_delim = ""
    # track the index of start of current line
    line_start = 0

    while i < n:
        ch = source[i]
        # handle newlines
        if ch == "\n":
            out_chars.append(ch)
            i += 1
            line_start = i
            continue

        # handle string starts and ends
        if not in_string:
            # check for triple-quotes
            if source.startswith("\'\'\'", i) or source.startswith('"""', i):
                in_string = True
                string_delim = source[i:i+3]
                out_chars.append(string_delim)
                i += 3
                continue
            # single-quote or double-quote
            if ch == '"' or ch == "'":
                in_string = True
                string_delim = ch
                out_chars.append(ch)
                i += 1
                continue
        else:
            # we're in a string
            if string_delim in ("\'\'\'", '"""'):
                if source.startswith(string_delim, i):
                    out_chars.append(string_delim)
                    i += 3
                    in_string = False
                    string_delim = ""
                    continue
                else:
                    out_chars.append(ch)
                    i += 1
                    continue
            else:
                # single-quoted string
                if ch == "\\":
                    # escape sequence, copy two chars if possible
                    if i + 1 < n:
                        out_chars.append(ch)
                        out_chars.append(source[i+1])
                        i += 2
                        continue
                    else:
                        out_chars.append(ch)
                        i += 1
                        continue
                if ch == string_delim:
                    out_chars.append(ch)
                    i += 1
                    in_string = False
                    string_delim = ""
                    continue
                else:
                    out_chars.append(ch)
                    i += 1
                    continue

        # if not in string, check for '//' starting here
        if source.startswith("//", i):
            # determine if we should convert this // into a comment
            if force:
                # To be less surprising when floor-division and trailing
                # comments coexist, prefer treating the *rightmost* // on a
                # line as the comment start. Look ahead: if there is another
                # '//' outside of strings later on the same line, then skip
                # converting this one so a later one can be considered.
                j = i + 2
                found_later = False
                look_in_string = False
                look_delim = ""
                while j < n and source[j] != "\n":
                    if not look_in_string:
                        if source.startswith("\'\'\'", j) or source.startswith('"""', j):
                            look_in_string = True
                            look_delim = source[j:j+3]
                            j += 3
                            continue
                        if source[j] in ('"', "'"):
                            look_in_string = True
                            look_delim = source[j]
                            j += 1
                            continue
                        if source.startswith("//", j):
                            found_later = True
                            break
                        j += 1
                    else:
                        if look_delim in ("\'\'\'", '"""'):
                            if source.startswith(look_delim, j):
                                look_in_string = False
                                look_delim = ""
                                j += 3
                                continue
                            j += 1
                        else:
                            if source[j] == "\\":
                                j += 2
                                continue
                            if source[j] == look_delim:
                                look_in_string = False
                                look_delim = ""
                                j += 1
                                continue
                            j += 1

                if found_later:
                    # leave this '//' as-is (likely a floor-division), move on
                    out_chars.append("/")
                    out_chars.append("/")
                    i += 2
                    continue
                # otherwise this is the last '//' on the line: convert to comment
                out_chars.append("#")
                i += 2
                while i < n and source[i] != "\n":
                    out_chars.append(source[i])
                    i += 1
                continue
            else:
                # safe default: only convert if there is no non-whitespace
                # character between line_start and this position
                prefix = source[line_start:i]
                if prefix.strip() == "":
                    out_chars.append("#")
                    i += 2
                    while i < n and source[i] != "\n":
                        out_chars.append(source[i])
                        i += 1
                    continue
                else:
                    # treat as operator (floor-division) — leave as-is
                    out_chars.append("/")
                    out_chars.append("/")
                    i += 2
                    continue

        # default: copy character
        out_chars.append(ch)
        i += 1

    return "".join(out_chars)


def convert_file_inplace(path: str, *, force: bool = False) -> Tuple[str, str]:
    """Read file at `path`, convert source, return (original, converted) strings."""
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    new = convert_source(src, force=force)
    return src, new
