#!/usr/bin/env python3
"""Validate More World Locations loot list references.

Scans warpalicious location config files for locations that enable
custom loot lists and verifies that the referenced list exists in the
warpalicious.More_World_Locations_LootLists.yml file and contains at
least one item.
"""

from __future__ import annotations
import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config"
LOOT_FILE = CONFIG_DIR / "warpalicious.More_World_Locations_LootLists.yml"

try:
    loot_data = yaml.safe_load(LOOT_FILE.read_text())
except Exception as exc:  # pragma: no cover - printed for debugging
    print(f"Failed to read loot lists: {exc}")
    sys.exit(1)

loot_lists = {k for k, v in loot_data.items() if isinstance(v, list) and v}

missing: list[tuple[str, str]] = []
for cfg_path in CONFIG_DIR.glob("warpalicious.*.cfg"):
    lines = cfg_path.read_text().splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("Use Custom Loot YAML file") and "On" in line:
            for j in range(i + 1, min(i + 6, len(lines))):
                m = re.search(r"Name of Loot List = (.+)", lines[j])
                if m:
                    name = m.group(1).strip()
                    if name not in loot_lists:
                        missing.append((str(cfg_path), name))
                    break

if missing:
    print("Missing or empty loot lists found:")
    for path, name in missing:
        print(f"  {path}: {name}")
    sys.exit(1)
else:
    print("All referenced loot lists exist and contain items.")
