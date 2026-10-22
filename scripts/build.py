#!/usr/bin/env python3
"""Renders templates/ into themes/ with the colors in palette.json. Run from the repo root: python3 scripts/build.py"""
import json, pathlib, re

PALETTE = json.loads(pathlib.Path("palette.json").read_text())

def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

# Apps that don't take #RRGGBB.
FORMATS = {
    "chrome": lambda h: "[%d, %d, %d]" % rgb(h),
    "claude-code": lambda h: "rgb(%d,%d,%d)" % rgb(h),
    "jetbrains": lambda h: h[1:].lower(),
    "xcode": lambda h: " ".join("%.6f" % (c / 255) for c in rgb(h)),
}

for src in sorted(pathlib.Path("templates").rglob("*")):
    if not src.is_file() or src.name.startswith("."):
        continue
    fmt = FORMATS.get(src.parts[1], str)
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: fmt(PALETTE[m.group(1)]), src.read_bytes().decode())
    pathlib.Path("themes", *src.parts[1:]).write_bytes(text.encode())
