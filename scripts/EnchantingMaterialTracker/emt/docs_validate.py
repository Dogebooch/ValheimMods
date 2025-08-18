
from __future__ import annotations
import re, os
def parse_materials_from_markdown(md_path: str):
    if not (md_path and os.path.exists(md_path)): return {}
    text = open(md_path, "r", encoding="utf-8", errors="ignore").read()
    out = {}
    for m in re.finditer(r"\|\s*([A-Za-z0-9_]+)\s*\|\s*([0-9.]+)\s*\|", text):
        name, val = m.group(1), m.group(2)
        try: out[name] = float(val)
        except: pass
    for m in re.finditer(r"^\s*([A-Za-z0-9_]+)\s*[:=]\s*([0-9.]+)\s*$", text, flags=re.MULTILINE):
        name, val = m.group(1), m.group(2)
        try: out[name] = float(val)
        except: pass
    return out
