#!/usr/bin/env python3
"""
Adds a simple build stamp meta tag to every .html file so we can verify
which version the browser is serving (helps diagnose caching / wrong deploy).
"""

from __future__ import annotations

import os
from pathlib import Path


STAMP = '2025-12-16-navfix-01'
META = f'<meta name="mm-build" content="{STAMP}">'


def stamp_html(path: Path) -> bool:
    s = path.read_text(encoding="utf-8", errors="ignore")
    if 'name="mm-build"' in s:
        return False

    needle = '<meta charset="utf-8">'
    idx = s.find(needle)
    if idx == -1:
        return False

    insert_at = idx + len(needle)
    s2 = s[:insert_at] + "  " + META + s[insert_at:]
    path.write_text(s2, encoding="utf-8")
    return True


def main() -> None:
    root = Path(".")
    changed = 0
    scanned = 0

    for dirpath, dirnames, filenames in os.walk(root):
        if any(part in {".git", "node_modules", "__pycache__"} for part in Path(dirpath).parts):
            continue
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            scanned += 1
            p = Path(dirpath) / fn
            if stamp_html(p):
                changed += 1

    print(f"Scanned {scanned} HTML files. Stamped {changed}. (STAMP={STAMP})")


if __name__ == "__main__":
    main()


