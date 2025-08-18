
from __future__ import annotations
import os, glob
from typing import Iterator, Tuple
def scan_files(root: str, globs: list[str]) -> Iterator[str]:
    if not os.path.exists(root):
        return  # Return empty iterator if root doesn't exist
    for pattern in globs:
        full_pat = os.path.join(root, pattern)
        for p in glob.iglob(full_pat, recursive=True):
            if os.path.isfile(p):
                yield os.path.abspath(p)
def map_files(root: str, scan_globs: dict) -> Iterator[Tuple[str, str]]:
    if not scan_globs: return
    for key, gls in scan_globs.items():
        if "epicloot_chests_cfg" in key:
            stype = "epicloot_chest_cfg"
        elif "drop_that_lists" in key:
            stype = "drop_that_list_cfg"
        elif "drop_that_chars" in key:
            stype = "drop_that_char_cfg"
        elif "world_locations" in key:
            stype = "world_locations_yml"
        elif "epicloot_json" in key:
            stype = "epicloot_json"
        elif "relicheim_loot" in key:
            stype = "relicheim_loot"
        elif "backpacks" in key:
            stype = "backpack_cfg"
        else:
            stype = key
        for path in scan_files(root, gls):
            yield (stype, path)
