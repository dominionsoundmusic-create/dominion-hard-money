#!/usr/bin/env python3
"""Repair spots where the first dash clean-up removed a separator after a
closing tag (e.g. "<b>Interest</b>interest-only"). Pass page paths to limit."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
items = json.load(open(sys.argv[1]))
only = sys.argv[2:]
fixed = 0
for f, tag, after in items:
    if only and not any(f.startswith(o) for o in only):
        continue
    p = ROOT / "_src/pages" / f
    s = p.read_text(encoding="utf-8")
    a = after.strip()[:12]
    sep = ": " if tag in ("</b>", "</strong>") else ", "
    pat = re.escape(tag) + r"(?=" + re.escape(a) + ")"
    s2, n = re.subn(pat, tag + sep, s, count=1)
    if n:
        p.write_text(s2, encoding="utf-8"); fixed += 1
print("fixed", fixed)
