
from __future__ import annotations
import datetime
from .config import load_materials_registry
from .scanner import map_files
from .registry import ALL_PARSERS
from .db import DB
def take_snapshot(root_dir: str, settings: dict, kind_label: str = "") -> int:
    mats = load_materials_registry(settings["materials_registry"])
    all_materials = set()
    for tier_materials in mats.get("tiers", {}).values():
        if isinstance(tier_materials, list):
            all_materials.update(tier_materials)
    aliases = mats.get("aliases", {})
    db = DB(settings["db_path"])
    snap_id = db.insert_snapshot(root_dir=root_dir, created_at=datetime.datetime.utcnow().isoformat())
    for source_type, path in map_files(root_dir, settings.get("scan_globs", {})):
        for parser in ALL_PARSERS:
            if parser.source_type == source_type and parser.supports(path):
                items = list(parser.parse(path, all_materials, aliases))
                if items:
                    db.insert_metrics(snap_id, items)
                break
    db.close()
    return snap_id
