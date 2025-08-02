"""Generate Drop That and Epic Loot configuration snippets from a master table.

The master table is stored in ``master_loot_table.yml`` and contains a list of
entries keyed by ``PrefabID``. Each entry defines both Drop That and EpicLoot
parameters. This script emits two files:

* ``drop_that.generated.cfg`` – drop_that.character_drop style config
* ``epicloot.generated.cfg`` – randyknapp.mods.epicloot.cfg style config

The goal is to consolidate the loot data so edits can be made in one place.
This is a minimal reference implementation and can be extended with additional
fields as needed.
"""

from __future__ import annotations

import pathlib
from typing import Any, Dict

import yaml

ROOT = pathlib.Path(__file__).resolve().parent
MASTER_FILE = ROOT / "master_loot_table.yml"
DROPTHAT_OUT = ROOT / "drop_that.generated.cfg"
EPICLOOT_OUT = ROOT / "epicloot.generated.cfg"


def load_master() -> list[Dict[str, Any]]:
    with MASTER_FILE.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_dropthat(entries: list[Dict[str, Any]]) -> str:
    lines = ["# Generated from master_loot_table.yml", ""]
    for entry in entries:
        dt = entry.get("DropThat", {})
        lines.extend([
            f"[{entry['PrefabID']}]",
            f"item={entry['ItemPrefab']}",
            f"set_chance_to_drop={dt.get('SetChanceToDrop', 0)}",
            f"world_level_min={dt.get('WorldLevelMin', 0)}",
            f"creature_stars_required={dt.get('CreatureStarsRequired', 0)}",
            "",
        ])
    return "\n".join(lines)


def render_epicloot(entries: list[Dict[str, Any]]) -> str:
    lines = ["# Generated from master_loot_table.yml", ""]
    for entry in entries:
        el = entry.get("EpicLoot", {})
        rarity = el.get("RarityWeights", {})
        lines.extend([
            f"[{entry['PrefabID']}]",
            f"item={entry['ItemPrefab']}",
            f"world_level_min={el.get('WorldLevelMin', 0)}",
        ])
        for rar, weight in rarity.items():
            lines.append(f"rarity_weight_{rar.lower()}={weight}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    entries = load_master()
    DROPTHAT_OUT.write_text(render_dropthat(entries), encoding="utf-8")
    EPICLOOT_OUT.write_text(render_epicloot(entries), encoding="utf-8")
    print(f"Wrote {DROPTHAT_OUT} and {EPICLOOT_OUT}")


if __name__ == "__main__":
    main()
