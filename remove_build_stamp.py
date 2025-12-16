#!/usr/bin/env python3
"""
Removes the temporary build stamp meta tag added for deploy verification:
  <meta name="mm-build" content="...">
"""

from __future__ import annotations

import os
import re
from pathlib import Path


MM_BUILD_RE = re.compile(r'\s*<meta name="mm-build" content="[^"]*">\s*')


def strip_stamp(html: str) -> str:
    return MM_BUILD_RE.sub(" ", html)


def main() -> None:
    root = Path(".")
    scanned = 0
    changed = 0

    for dirpath, dirnames, filenames in os.walk(root):
        if any(part in {".git", "node_modules", "__pycache__"} for part in Path(dirpath).parts):
            continue
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            scanned += 1
            p = Path(dirpath) / fn
            s = p.read_text(encoding="utf-8", errors="ignore")
            s2 = strip_stamp(s)
            if s2 != s:
                p.write_text(s2, encoding="utf-8")
                changed += 1

    print(f"Scanned {scanned} HTML files. Removed stamp from {changed}.")


if __name__ == "__main__":
    main()


