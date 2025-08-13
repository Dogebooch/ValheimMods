import csv
import json
import re
import sys
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkfont

class VNEIItemIndex:
    def __init__(self, vnei_dir: Path):
        self.vnei_dir = vnei_dir
        self.items_csv = vnei_dir / "VNEI.indexed.items.csv"
        self.items_txt = vnei_dir / "VNEI.indexed.items.txt"
        self.items_yml = vnei_dir / "VNEI.indexed.items.yml"

    def _guess_columns(self, headers: list[str]) -> tuple[str | None, str | None]:
        lower = [h.lower().strip() for h in headers]
        # Try item column
        item_candidates = [
            "internalname", "item", "name", "id", "prefab", "prefabname",
        ]
        station_candidates = [
            "craftingstation", "crafting_station", "station", "workbench", "forge", "table",
        ]
        item_col = None
        station_col = None
        for cand in item_candidates:
            if cand in lower:
                item_col = headers[lower.index(cand)]
                break
        for cand in station_candidates:
            if cand in lower:
                station_col = headers[lower.index(cand)]
                break
        # Best-effort fallback
        if item_col is None and headers:
            item_col = headers[0]
        if station_col is None:
            # try to find any column containing 'station'
            for i, h in enumerate(lower):
                if 'station' in h:
                    station_col = headers[i]
                    break
        return item_col, station_col

    def load_items(self) -> dict[str, str]:
        """Return mapping: item_name -> crafting_station (may be empty string)."""
        item_to_station: dict[str, str] = {}
        source = None
        if self.items_csv.exists():
            source = self.items_csv
        elif self.items_txt.exists():
            source = self.items_txt
        elif self.items_yml.exists():
            source = self.items_yml

        if source is None:
            return item_to_station

        if source.suffix.lower() == ".csv" or source.suffix.lower() == ".txt":
            with open(source, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                item_col, station_col = self._guess_columns(headers)
                for row in reader:
                    item = (row.get(item_col, "") or "").strip()
                    station = (row.get(station_col, "") or "").strip() if station_col else ""
                    if item:
                        item_to_station[item] = station
        else:
            # Very light YML parsing: expect blocks with keys including item name and station
            try:
                with open(source, 'r', encoding='utf-8') as f:
                    text = f.read()
                # Try to find lines like: name: XYZ, crafting_station: ABC
                current_item = None
                for raw in text.splitlines():
                    line = raw.strip()
                    if not line or line.startswith('#'):
                        continue
                    m_item = re.search(r"(name|item|internal|prefab)\s*:\s*([A-Za-z0-9_\-\.]+)", line, re.IGNORECASE)
                    if m_item:
                        current_item = m_item.group(2)
                    m_station = re.search(r"(crafting[_\s]?station|station)\s*:\s*([A-Za-z0-9_\-\. ]+)", line, re.IGNORECASE)
                    if m_station and current_item:
                        item_to_station[current_item] = m_station.group(2).strip()
                        current_item = None
            except Exception:
                pass

        return item_to_station

    def load_items_with_stats(self) -> dict[str, dict]:
        """Return mapping: item_name -> { 'station': str, 'stats': str }.

        Heuristically summarizes useful stats for deciding Blacksmithing level.
        """
        result: dict[str, dict] = {}
        source = None
        if self.items_csv.exists():
            source = self.items_csv
        elif self.items_txt.exists():
            source = self.items_txt
        elif self.items_yml.exists():
            source = self.items_yml

        def summarize_row(row: dict[str, str], lower_headers: list[str]) -> tuple[str, str]:
            # Determine station
            station = ""
            for key in ("craftingstation", "crafting_station", "station", "workbench", "forge", "table"):
                if key in lower_headers:
                    station = (row.get(lower_headers[lower_headers.index(key)], "") or "").strip()
                    break

            # Extract numeric-ish values
            def get_num(keys: list[str]) -> float | None:
                for k in keys:
                    if k in lower_headers:
                        v = row.get(lower_headers[lower_headers.index(k)], "")
                        if v is None:
                            continue
                        try:
                            # Handle formats like "45", "45.0", "45 (Slash)", "45-60"
                            s = str(v).strip()
                            s = s.split()[0]
                            if "-" in s:
                                parts = [float(p) for p in s.split("-") if p]
                                if parts:
                                    return sum(parts) / len(parts)
                            return float(s)
                        except Exception:
                            continue
                return None

            lower_map = {h.lower().strip(): h for h in lower_headers}
            # Damage detection
            damage_total = get_num([
                "damage", "totaldamage", "dmg", "basedamage",
                "slash", "pierce", "blunt", "fire", "frost", "poison", "lightning", "spirit",
            ])
            # Armor / Block
            armor = get_num(["armor", "armour"])
            block = get_num(["blockpower", "block", "parry"])
            # Tier / Weight / Durability
            tier = get_num(["tier", "crafting_tier", "level"])
            weight = get_num(["weight"]) 
            durability = get_num(["durability", "maxdurability"])

            # Build summary string
            parts: list[str] = []
            if armor is not None:
                parts.append(f"Armor {int(armor) if armor.is_integer() else round(armor,1)}")
            elif block is not None and (damage_total is None or block >= (damage_total or 0) * 0.6):
                parts.append(f"Block {int(block) if block.is_integer() else round(block,1)}")
            elif damage_total is not None:
                parts.append(f"DMG {int(damage_total) if damage_total.is_integer() else round(damage_total,1)}")

            if tier is not None:
                parts.append(f"T{int(tier)}")
            if weight is not None:
                parts.append(f"Wt {round(weight,1)}")
            if durability is not None:
                parts.append(f"Dur {int(durability) if durability.is_integer() else round(durability,0)}")

            summary = " 3 ".join(parts) if parts else ""
            return station, summary

        if source is None:
            return result

        if source.suffix.lower() in (".csv", ".txt"):
            with open(source, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                lower_headers = [h for h in headers]
                item_col, _station_col = self._guess_columns(headers)
                for row in reader:
                    item = (row.get(item_col, "") or "").strip()
                    if not item:
                        continue
                    station, summary = summarize_row(row, lower_headers)
                    result[item] = {"station": station, "stats": summary}
        else:
            # Try to parse YML roughly for name and a few numbers
            try:
                with open(source, 'r', encoding='utf-8') as f:
                    text = f.read()
                current_item = None
                stash: dict[str, str] = {}
                for raw in text.splitlines():
                    line = raw.strip()
                    if not line or line.startswith('#'):
                        continue
                    m_item = re.search(r"(name|item|internal|prefab)\s*:\s*([A-Za-z0-9_\-\.]+)", line, re.IGNORECASE)
                    if m_item:
                        if current_item and stash:
                            # Summarize
                            station = stash.get('station', '')
                            dmg = stash.get('damage')
                            armor = stash.get('armor')
                            summary_parts = []
                            if armor:
                                summary_parts.append(f"Armor {armor}")
                            elif dmg:
                                summary_parts.append(f"DMG {dmg}")
                            summary = " 3 ".join(summary_parts)
                            result[current_item] = {"station": station, "stats": summary}
                        current_item = m_item.group(2)
                        stash = {}
                        continue
                    m_station = re.search(r"(crafting[_\s]?station|station)\s*:\s*([A-Za-z0-9_\-\. ]+)", line, re.IGNORECASE)
                    if m_station:
                        stash['station'] = m_station.group(2).strip()
                    m_damage = re.search(r"(damage|slash|pierce|blunt)\s*:\s*([0-9.\-]+)", line, re.IGNORECASE)
                    if m_damage:
                        stash['damage'] = m_damage.group(2)
                    m_armor = re.search(r"armor\s*:\s*([0-9.]+)", line, re.IGNORECASE)
                    if m_armor:
                        stash['armor'] = m_armor.group(1)
                if current_item and stash and current_item not in result:
                    station = stash.get('station', '')
                    dmg = stash.get('damage')
                    armor = stash.get('armor')
                    summary_parts = []
                    if armor:
                        summary_parts.append(f"Armor {armor}")
                    elif dmg:
                        summary_parts.append(f"DMG {dmg}")
                    summary = " 3 ".join(summary_parts)
                    result[current_item] = {"station": station, "stats": summary}
            except Exception:
                pass
        return result


class WackyBulkIndex:
    def __init__(self, bulk_root: Path):
        self.bulk_root = bulk_root

    def _iter_yaml_files(self) -> list[Path]:
        if not self.bulk_root or not self.bulk_root.exists():
            return []
        files: list[Path] = []
        try:
            for sub in ("Items", "Recipes", "Creatures", "Pickables"):
                p = self.bulk_root / sub
                if p.exists():
                    files.extend(p.rglob("*.yml"))
                    files.extend(p.rglob("*.yaml"))
            # Fallback: scan root too
            files.extend(self.bulk_root.glob("*.yml"))
            files.extend(self.bulk_root.glob("*.yaml"))
        except Exception:
            pass
        # De-duplicate
        uniq: list[Path] = []
        seen: set[str] = set()
        for f in files:
            s = str(f.resolve())
            if s not in seen:
                uniq.append(f)
                seen.add(s)
        return uniq

    def _parse_simple_yaml_block(self, text: str) -> list[dict[str, str]]:
        entries: list[dict[str, str]] = []
        current: dict[str, str] | None = None
        current_key: str | None = None
        current_indent = 0
        for raw in text.splitlines():
            if not raw.strip() or raw.lstrip().startswith(('#', '//', ';')):
                continue
            indent = len(raw) - len(raw.lstrip(' '))
            line = raw.strip()
            if line.startswith('- '):
                # New list entry
                if current:
                    entries.append(current)
                current = {}
                current_indent = indent
                kv = line[2:]
                if ':' in kv:
                    k, v = kv.split(':', 1)
                    current[k.strip()] = v.strip()
                continue
            # key: value
            m = re.match(r"^([A-Za-z0-9_\-\.]+)\s*:\s*(.*)$", line)
            if m:
                k, v = m.group(1), m.group(2)
                if current is not None and indent > current_indent:
                    # nested under current
                    current[k] = v
                else:
                    # top-level; start a synthetic single-entry document
                    if current:
                        entries.append(current)
                    current = {k: v}
                    current_indent = indent
                current_key = k
                continue
            # Continuation lines for multi-line scalars not handled; skip
        if current:
            entries.append(current)
        return entries

    def scan(self) -> dict[str, dict]:
        """Return mapping: prefab -> rich info from Wacky Bulk YAML.

        Fields:
          - recipe: list[(item, qty)]
          - station: str
          - station_level: int
          - stats: {armor, damage_total, weight, block, durability, effects}
          - tier: int
          - world_level: int | ''
          - rarity: str
        """
        info: dict[str, dict] = {}
        for path in self._iter_yaml_files():
            try:
                text = path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            # Heuristics: try to find prefab blocks
            # Prefer explicit PrefabName fields
            prefab_candidates: set[str] = set()
            for m in re.finditer(r"^\s*(?:-\s*)?PrefabName\s*:\s*([A-Za-z0-9_\-.]+)\s*$", text, re.MULTILINE):
                prefab_candidates.add(m.group(1))
            # Fallback: look for name:
            for m in re.finditer(r"^\s*(?:-\s*)?(?:name|InternalName)\s*:\s*([A-Za-z0-9_\-.]+)\s*$", text, re.MULTILINE | re.IGNORECASE):
                prefab_candidates.add(m.group(1))

            # Parse coarse key-values for station, level, rarity, tier
            station = ""
            station_level: int | None = None
            rarity = ""
            tier: int | None = None
            world_level: int | None = None
            # Common station keys
            m_station = re.search(r"(CraftingStation|Station|WorkBench)\s*:\s*([A-Za-z0-9_\- ]+)", text, re.IGNORECASE)
            if m_station:
                station = m_station.group(2).strip()
            m_slevel = re.search(r"(CraftingStationLevel|StationLevel|RequiredStationLevel)\s*:\s*([0-9]+)", text, re.IGNORECASE)
            if m_slevel:
                try:
                    station_level = int(m_slevel.group(2))
                except Exception:
                    station_level = None
            m_tier = re.search(r"(m_toolTier|Tier)\s*:\s*([0-9]+)", text, re.IGNORECASE)
            if m_tier:
                try:
                    tier = int(m_tier.group(2))
                except Exception:
                    tier = None
            m_wl = re.search(r"(WorldLevel|ConditionWorldLevelMin)\s*:\s*([0-9]+)", text, re.IGNORECASE)
            if m_wl:
                try:
                    world_level = int(m_wl.group(2))
                except Exception:
                    world_level = None
            m_rarity = re.search(r"(EpicLoot|RelicHeim).*?(Rarity|Tier)\s*:\s*([A-Za-z0-9_\-]+)", text, re.IGNORECASE | re.DOTALL)
            if m_rarity:
                rarity = m_rarity.group(3)

            # Stats heuristics
            stats: dict[str, str] = {}
            def find_num(key_pattern: str) -> str | None:
                m = re.search(key_pattern + r"\s*:\s*([0-9.\-]+)", text, re.IGNORECASE)
                return m.group(1) if m else None
            dmg_total = None
            for key in ["TotalDamage", "Damage", "BaseDamage", "slash", "pierce", "blunt", "fire", "frost", "poison", "lightning", "spirit"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        dmg_total = (float(dmg_total) if dmg_total is not None else 0.0) + float(v)
                    except Exception:
                        pass
            armor = find_num(r"armor|armour")
            weight = find_num(r"weight")
            block = find_num(r"block(power)?")
            durability = find_num(r"(durability|maxdurability)")
            if armor: stats['armor'] = armor
            if dmg_total is not None: stats['damage_total'] = str(int(dmg_total) if float(dmg_total).is_integer() else round(float(dmg_total), 1))
            if weight: stats['weight'] = weight
            if block: stats['block'] = block
            if durability: stats['durability'] = durability

            # Recipe extraction heuristics
            recipe: list[tuple[str, int]] = []
            # Pattern A: YAML list of requirements entries
            for rm in re.finditer(r"^-\s*(Item|Prefab|Name)\s*:\s*([A-Za-z0-9_\-.]+).*?(Amount|Qty|Quantity)\s*:\s*([0-9]+)", text, re.IGNORECASE | re.MULTILINE | re.DOTALL):
                mat = rm.group(2)
                qty = int(rm.group(4))
                recipe.append((mat, qty))
            # Pattern B: inline CSV-like: Iron:5, Wood:2
            if not recipe:
                im = re.search(r"(Resources|Recipe|Requirements)\s*:\s*([^\n]+)", text, re.IGNORECASE)
                if im:
                    vals = im.group(2)
                    for part in vals.split(','):
                        part = part.strip()
                        if not part:
                            continue
                        if ':' in part:
                            a, b = part.split(':', 1)
                            a = a.strip()
                            try:
                                bq = int(b.strip())
                            except Exception:
                                bq = 1
                            recipe.append((a, bq))

            # Assign into info for all discovered prefab candidates
            for prefab in prefab_candidates or [""]:
                if not prefab:
                    continue
                d = info.setdefault(prefab, {})
                if station and not d.get('station'):
                    d['station'] = station
                if station_level is not None and not d.get('station_level'):
                    d['station_level'] = station_level
                if recipe and not d.get('recipe'):
                    d['recipe'] = recipe
                if stats and not d.get('stats'):
                    d['stats'] = stats
                if tier is not None and not d.get('tier'):
                    d['tier'] = tier
                if world_level is not None and not d.get('world_level'):
                    d['world_level'] = world_level
                if rarity and not d.get('rarity'):
                    d['rarity'] = rarity
        return info

    def load_item_metadata(self) -> dict[str, dict]:
        """Return mapping: item_name -> { 'localized': str, 'type': str, 'source_mod': str }.

        Pulls from CSV/TXT if available; falls back to empty strings.
        """
        meta: dict[str, dict] = {}
        source = None
        if self.items_csv.exists():
            source = self.items_csv
        elif self.items_txt.exists():
            source = self.items_txt
        if source is None:
            return meta
        try:
            if source.suffix.lower() in ('.csv', '.txt'):
                with open(source, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        key = (row.get('Internal Name', '') or row.get('internalname', '') or '').strip()
                        if not key:
                            continue
                        meta[key] = {
                            'localized': (row.get('Localized Name', '') or '').strip(),
                            'type': (row.get('Item Type', '') or '').strip(),
                            'source_mod': (row.get('Source Mod', '') or '').strip(),
                        }
        except Exception:
            pass
        return meta

    def load_tool_tiers(self, config_root: Path) -> dict[str, int]:
        """Parse Wacky's Database cache for m_toolTier per item (if present)."""
        tiers: dict[str, int] = {}
        cache_dir = config_root / "wackysDatabase" / "Cache"
        if not cache_dir.exists():
            return tiers
        try:
            for path in cache_dir.glob("*.zz"):
                try:
                    text = path.read_text(encoding='utf-8', errors='ignore')
                except Exception:
                    continue
                name = None
                tier_val = None
                for raw in text.splitlines():
                    if name is None and raw.startswith("name:"):
                        name = raw.split(":", 1)[1].strip()
                        continue
                    if tier_val is None and "m_toolTier:" in raw:
                        try:
                            tier_val = int(raw.split(":", 1)[1].strip())
                        except Exception:
                            pass
                    if name and tier_val is not None:
                        break
                if name and tier_val is not None:
                    tiers[name] = tier_val
        except Exception:
            pass
        return tiers

    @staticmethod
    def map_tool_tier_to_world_level(tool_tier: int) -> tuple[int, str]:
        """Map tool tier to (WL number, biome name), including Deep North and Ashlands.

        Mapping is heuristic and can be adjusted:
          0→(1, Meadows), 1→(2, Black Forest), 2→(3, Swamp), 3→(4, Mountains),
          4→(5, Plains), 5→(6, Mistlands), 6→(7, Deep North), 7+→(8, Ashlands)
        """
        mapping = {
            0: (1, "Meadows"),
            1: (2, "Black Forest"),
            2: (3, "Swamp"),
            3: (4, "Mountains"),
            4: (5, "Plains"),
            5: (6, "Mistlands"),
            6: (7, "Deep North"),
        }
        if tool_tier in mapping:
            return mapping[tool_tier]
        if tool_tier is not None and tool_tier >= 7:
            return (8, "Ashlands")
        return (0, "")

    @staticmethod
    def parse_crafting_costs(value: str) -> str:
        """Normalize recipe string like 'Iron:5,WitheredBone:2' to 'Iron x5, WitheredBone x2'."""
        parts = []
        for tok in (value or "").split(','):
            tok = tok.strip()
            if not tok:
                continue
            if ':' in tok:
                a, b = tok.split(':', 1)
                parts.append(f"{a.strip()} x{b.strip()}")
            else:
                parts.append(tok)
        return ', '.join(parts)

    def scan_configs_for_recipes_and_unlocks(self, config_root: Path) -> dict[str, dict]:
        """Scan known config files for recipe/unlock/BiS notes by item.

        Returns mapping: item -> {
          'recipe': str,
          'station': str,
          'station_level': str,
          'unlock': str,
          'prestige': str,
          'set': str,
          'bis': str
        }
        """
        info: dict[str, dict] = {}
        root = config_root
        # 1) Therzie.Wizardry.cfg craft lines as example (format rich and consistent)
        tw = root / "Therzie.Wizardry.cfg"
        if tw.exists():
            try:
                for raw in tw.read_text(encoding='utf-8', errors='ignore').splitlines():
                    line = raw.strip()
                    if line.startswith("Crafting Costs (") and "=" in line:
                        # Crafting Costs (Name) = Item:Q,Item:Q
                        try:
                            left, val = line.split('=', 1)
                            val = val.strip()
                            # Extract Name inside parentheses for mapping hint
                            name = left[left.find('(')+1:left.find(')')].strip()
                            recipe = self.parse_crafting_costs(val)
                            if name:
                                d = info.setdefault(name, {})
                                d['recipe'] = recipe
                        except Exception:
                            pass
                    elif line.startswith("Crafting Station (") and "=" in line:
                        try:
                            left, val = line.split('=', 1)
                            val = val.strip()
                            name = left[left.find('(')+1:left.find(')')].strip()
                            if name:
                                d = info.setdefault(name, {})
                                d['station'] = val
                        except Exception:
                            pass
                    elif line.startswith("Crafting Station Level (") and "=" in line:
                        try:
                            left, val = line.split('=', 1)
                            val = val.strip()
                            name = left[left.find('(')+1:left.find(')')].strip()
                            if name:
                                d = info.setdefault(name, {})
                                d['station_level'] = val
                        except Exception:
                            pass
            except Exception:
                pass

        # 2) TradersExtended buy jsons to infer early unlock via trader tier
        for path in root.glob("shudnal.TradersExtended.*_Trader.buy.json"):
            try:
                txt = path.read_text(encoding='utf-8', errors='ignore')
                m = re.search(r'"prefab"\s*:\s*"([A-Za-z0-9_\-\.]+)"', txt)
                if m:
                    prefab = m.group(1)
                    tier = "Blacksmith tier?"
                    if "tier1" in txt:
                        tier = "Blacksmith tier 1"
                    elif "tier2" in txt:
                        tier = "Blacksmith tier 2"
                    elif "tier3" in txt:
                        tier = "Blacksmith tier 3"
                    d = info.setdefault(prefab, {})
                    d['unlock'] = (d.get('unlock') + "; " if d.get('unlock') else "") + f"Sold by trader ({tier})"
            except Exception:
                pass

        # 3) World-level hints from Spawn_That/Drop_That/EpicLoot patches
        # Add a coarse note if an item name appears inside lines with WorldLevel or ConditionWorldLevelMin
        wl_files = list(root.rglob("*.cfg")) + list((root / "EpicLoot" / "patches").rglob("*.json"))
        for p in wl_files:
            try:
                txt = p.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            if ("WorldLevel" not in txt) and ("ConditionWorldLevelMin" not in txt):
                continue
            # Heuristic: if an item internal name appears on a line near WL markers, attach a note
            for item in list(info.keys()):
                if item in txt:
                    d = info.setdefault(item, {})
                    d['unlock'] = (d.get('unlock') + "; " if d.get('unlock') else "") + "WL-gated content nearby"
        return info


class SkillConfig:
    def __init__(self, config_dir: Path, filename_hint: str = "ItemRequiresSkillLevel"):
        self.config_dir = config_dir
        self.filename_hint = filename_hint
        self.path = self._find_file()

    def _find_file(self) -> Path | None:
        if not self.config_dir.exists():
            return None
        # Search for possible files containing the hint
        for p in self.config_dir.glob("**/*.yml"):
            if self.filename_hint.lower() in p.name.lower():
                return p
        return None

    def pick_file(self) -> None:
        chosen = filedialog.askopenfilename(
            title="Select Skill Config YAML",
            filetypes=[("YAML", "*.yml;*.yaml"), ("All Files", "*.*")],
            initialdir=str(self.config_dir) if self.config_dir.exists() else str(Path.cwd()),
        )
        if chosen:
            self.path = Path(chosen)

    def load_items(self) -> set[str]:
        """Return set of item names present as top-level keys in the YAML-like file."""
        items: set[str] = set()
        if not self.path or not self.path.exists():
            return items
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                for raw in f:
                    line = raw.rstrip()
                    if not line.strip() or line.lstrip().startswith(('#', '//')):
                        continue
                    # item_name:
                    m = re.match(r"^([A-Za-z0-9_\-\.]+):\s*(\{|$)", line)
                    if m and (len(line) - len(line.lstrip())) == 0:
                        items.add(m.group(1))
        except Exception:
            pass
        return items

    def load_blacksmithing_levels(self) -> dict[str, int]:
        """Best-effort parse to extract required Blacksmithing level per item.

        Supports two shapes:
        1) Top-level mapping:
           ItemName:\n  Requirements:\n    - Skill: Blacksmithing\n      Level: N
        2) List of entries:
           - PrefabName: ItemName\n  Requirements: ... as above
        """
        levels: dict[str, int] = {}
        if not self.path or not self.path.exists():
            return levels
        try:
            text = self.path.read_text(encoding='utf-8')
        except Exception:
            return levels

        current_item: str | None = None
        in_requirements = False
        in_blacksmith = False
        for raw in text.splitlines():
            line = raw.rstrip()
            stripped = line.strip()
            if not stripped or stripped.startswith(('#', '//')):
                continue
            # Detect new item header (mapping form)
            m_top = re.match(r"^([A-Za-z0-9_\-\.]+):\s*(\{|$)", line)
            if m_top and (len(line) - len(line.lstrip())) == 0:
                current_item = m_top.group(1)
                in_requirements = False
                in_blacksmith = False
                continue
            # Detect list-form PrefabName
            m_prefab = re.match(r"^\s*-\s*PrefabName:\s*([A-Za-z0-9_\-\.]+)\s*$", line)
            if m_prefab:
                current_item = m_prefab.group(1)
                in_requirements = False
                in_blacksmith = False
                continue
            # Track entering requirements
            if re.match(r"^\s*Requirements\s*:\s*(\{|$)", line):
                in_requirements = True
                in_blacksmith = False
                continue
            # Within requirements, look for a Blacksmithing skill block
            if in_requirements and re.search(r"Skill\s*:\s*Blacksmithing", line, re.IGNORECASE):
                in_blacksmith = True
                continue
            # Capture Level when in a Blacksmithing block
            m_lvl = re.search(r"Level\s*:\s*([0-9]+)", line)
            if in_requirements and in_blacksmith and m_lvl and current_item:
                try:
                    levels[current_item] = int(m_lvl.group(1))
                except Exception:
                    pass
                in_blacksmith = False  # consume one block
                continue
            # Reset blacksmith flag when hitting next skill entry in list
            if in_requirements and re.match(r"^\s*-\s*Skill\s*:\s*", line):
                in_blacksmith = False
        return levels

    def load_blacksmithing_rules(self) -> dict[str, dict]:
        """Parse Detalhes.ItemRequiresSkillLevel.yml for Blacksmithing rules per item.

        Returns mapping: item -> { 'level': int, 'block_craft': bool, 'block_equip': bool }
        """
        rules: dict[str, dict] = {}
        if not self.path or not self.path.exists():
            return rules
        try:
            text = self.path.read_text(encoding='utf-8')
        except Exception:
            return rules

        current_item: str | None = None
        in_requirements = False
        in_blacksmith = False
        for raw in text.splitlines():
            line = raw.rstrip()
            stripped = line.strip()
            if not stripped or stripped.startswith(('#', '//')):
                continue
            m_prefab = re.match(r"^\s*-\s*PrefabName:\s*([A-Za-z0-9_\-\.]+)\s*$", line)
            if m_prefab:
                current_item = m_prefab.group(1)
                in_requirements = False
                in_blacksmith = False
                rules.setdefault(current_item, { 'level': 0, 'block_craft': False, 'block_equip': False })
                continue
            if re.match(r"^\s*Requirements\s*:\s*(\{|$)", line):
                in_requirements = True
                in_blacksmith = False
                continue
            if in_requirements and re.search(r"Skill\s*:\s*Blacksmithing", line, re.IGNORECASE):
                in_blacksmith = True
                continue
            if current_item and in_requirements and in_blacksmith:
                m_lvl = re.search(r"Level\s*:\s*([0-9]+)", line)
                if m_lvl:
                    try:
                        rules[current_item]['level'] = int(m_lvl.group(1))
                    except Exception:
                        pass
                    continue
                m_bc = re.search(r"BlockCraft\s*:\s*(true|false)", line, re.IGNORECASE)
                if m_bc:
                    rules[current_item]['block_craft'] = (m_bc.group(1).lower() == 'true')
                    continue
                m_be = re.search(r"BlockEquip\s*:\s*(true|false)", line, re.IGNORECASE)
                if m_be:
                    rules[current_item]['block_equip'] = (m_be.group(1).lower() == 'true')
                    continue
        return rules


class PersistentState:
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.data: dict = {"highlights": {}, "skill_levels": {}, "notes": {}, "hidden_items": [], "last_paths": {}, "window": {}}
        self.load()

    def load(self) -> None:
        try:
            if self.state_file.exists():
                self.data = json.loads(self.state_file.read_text(encoding='utf-8'))
        except Exception:
            self.data = {"highlights": {}, "skill_levels": {}, "notes": {}, "hidden_items": [], "last_paths": {}, "window": {}}

    def save(self) -> None:
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            self.state_file.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding='utf-8', newline='\n')
        except Exception:
            pass


class ItemSkillTrackerApp:
    def __init__(self, root: tk.Tk, workspace: Path):
        self.root = root
        self.workspace = workspace
        self.base_font_size = 10
        self.zoom_level = 1.2
        self.font = tkfont.Font(family="Consolas" if sys.platform.startswith("win") else "Courier New", size=self.base_font_size)
        self.colors = {
            "bg": "#2e2b23",
            "panel": "#3b352a",
            "text": "#e8e2d0",
            "accent": "#a3a17a",
            "highlight": "#7d6f5e",
        }
        self.style = None
        # Icon cache (path mapping and loaded PhotoImage refs)
        self.icon_paths: dict[str, Path] = {}
        self.icon_images: dict[str, tk.PhotoImage] = {}

        # Default paths
        self.vnei_dir = workspace / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "VNEI-Export"
        self.config_dir = workspace / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config"
        self.state = PersistentState(workspace / "scripts" / "snapshots" / "item_skill_tracker_state.json")
        # Restore last chosen paths if present
        lp = self.state.data.get("last_paths", {})
        if lp.get("vnei_dir"):
            self.vnei_dir = Path(lp["vnei_dir"]) 
        if lp.get("skill_file"):
            # Legacy: previously allowed custom YAML selection; ignore now
            pass

        self.vnei_index = VNEIItemIndex(self.vnei_dir)
        # Wacky Database Bulk YAML root
        self.wacky_bulk_dir = workspace / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config" / "wackyDatabase-BulkYML"
        self.wacky_index = WackyBulkIndex(self.wacky_bulk_dir)
        self.skill_config = SkillConfig(self.config_dir, filename_hint="ItemRequiresSkillLevel")
        # Always target the default configuration file
        self.skill_config.path = self.config_dir / "Detalhes.ItemRequiresSkillLevel.yml"

        self._build_ui()
        self._index_icons()
        # After icons indexed, update layout for icon width
        try:
            self._update_tree_columns_layout()
        except Exception:
            pass
        # Build marker image (gold star-like) and display image cache
        try:
            self.marker_img = self._create_star_marker(12)
        except Exception:
            self.marker_img = None
        self.display_images: dict[tuple[str, bool], tk.PhotoImage] = {}
        self._refresh_data()

    def _build_ui(self) -> None:
        self.root.title("Item Skill Tracker")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.colors["bg"])

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["text"])
        style.configure("Action.TButton", background=self.colors["highlight"], foreground=self.colors["text"], padding=6)
        style.map("Action.TButton", background=[("active", self.colors["accent"])])
        style.configure("Treeview", background=self.colors["panel"], fieldbackground=self.colors["panel"], foreground=self.colors["text"], font=self.font)
        style.configure("Treeview.Heading", background=self.colors["highlight"], foreground=self.colors["text"], font=self.font)
        self.style = style
        # Ensure row height matches current font size
        try:
            self._update_row_height()
        except Exception:
            pass

        # Top controls
        top = ttk.Frame(self.root)
        top.pack(fill=tk.X, padx=8, pady=6)

        ttk.Button(top, text="Refresh", style="Action.TButton", command=self._refresh_data).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(top, text="Save", style="Action.TButton", command=self._persist_state).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(top, text="Write to configuration file", style="Action.TButton", command=self._write_to_config).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(top, text="Export Items.md", style="Action.TButton", command=self._export_items_mod_md).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(top, text="Export AI Summary", style="Action.TButton", command=self._export_ai_summary_jsonl).pack(side=tk.LEFT, padx=(0, 6))
        # Zoom controls (minimalist)
        zoom_frame = ttk.Frame(top)
        zoom_frame.pack(side=tk.RIGHT)
        ttk.Button(zoom_frame, text="A-", width=3, style="Action.TButton", command=self.zoom_out).pack(side=tk.RIGHT, padx=(0, 6))
        ttk.Button(zoom_frame, text="A+", width=3, style="Action.TButton", command=self.zoom_in).pack(side=tk.RIGHT)

        # Search/filter
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=8)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        ent = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        ent.pack(side=tk.LEFT, padx=(6, 6))
        ent.bind("<KeyRelease>", lambda e: self._filter_rows())

        # Hidden filter
        ttk.Label(search_frame, text="Show:").pack(side=tk.LEFT, padx=(16, 4))
        self.show_filter = tk.StringVar(value="Visible")
        show_combo = ttk.Combobox(search_frame, textvariable=self.show_filter, state="readonly", width=12)
        show_combo['values'] = ("Visible", "Hidden", "All")
        show_combo.pack(side=tk.LEFT)
        show_combo.bind("<<ComboboxSelected>>", lambda e: self._filter_rows())

        # Tree with left-most icon/star column and columns ordered for readability
        # Put Skill Level next to Item for straight-across reading, and show Mod
        columns = ("item", "mod", "skill_level", "station", "station_lvl", "in_yaml")
        self.tree = ttk.Treeview(self.root, columns=columns, show="tree headings", selectmode='extended')
        self.tree.heading("#0", text="★")
        self.tree.heading("item", text="Item")
        self.tree.heading("mod", text="Mod")
        self.tree.heading("skill_level", text="Skill Level")
        self.tree.heading("station", text="Crafting Station")
        self.tree.heading("station_lvl", text="Station Lvl")
        self.tree.heading("in_yaml", text="In Skill YAML")
        self.tree.column("#0", width=36, stretch=False)
        self.tree.column("item", width=360, stretch=False)
        self.tree.column("mod", width=160, stretch=False)
        self.tree.column("skill_level", width=110, stretch=False, anchor='center')
        self.tree.column("station", width=200, stretch=False)
        self.tree.column("station_lvl", width=110, stretch=False, anchor='center')
        self.tree.column("in_yaml", width=100, stretch=False, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        yscroll = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        # Horizontal scrollbar to avoid cutoff when zooming
        xscroll = ttk.Scrollbar(self.tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=xscroll.set)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        # Tag to color craftable items
        try:
            self.tree.tag_configure("craftable", foreground="#6aa84f")
        except Exception:
            pass

        # Remember base column widths to scale on zoom
        self._base_tree_col_widths = {"#0": 36, "item": 360, "mod": 160, "skill_level": 110, "station": 200, "station_lvl": 110, "in_yaml": 100}
        # Flex weights for responsive layout (A+C mix): distribute extra width to these
        self._flex_weights = {"item": 3.0, "station": 1.5}

        # Interactions
        self.tree.bind("<Double-1>", self._on_tree_double_click)
        self.tree.bind("<space>", self._toggle_highlight)
        self.tree.bind("<Button-3>", self._show_context_menu)

        # Re-layout columns on window resize (debounced)
        self._resize_after = None
        self.root.bind("<Configure>", self._on_window_resize)

        # Bulk level editor
        bulk_frame = ttk.Frame(self.root)
        bulk_frame.pack(fill=tk.X, padx=8, pady=(0, 4))
        ttk.Label(bulk_frame, text="Set level for selected:").pack(side=tk.LEFT)
        self.bulk_level_var = tk.StringVar()
        bulk_entry = ttk.Entry(bulk_frame, textvariable=self.bulk_level_var, width=8)
        bulk_entry.pack(side=tk.LEFT, padx=(6, 6))
        ttk.Button(bulk_frame, text="Apply", style="Action.TButton", command=self._bulk_set_level_from_entry).pack(side=tk.LEFT)

        # Footer
        self.status = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status).pack(fill=tk.X, padx=8, pady=(0, 6))

        # Initial layout pass
        try:
            self._layout_tree_columns()
        except Exception:
            pass

        # Context menu
        self.menu = tk.Menu(self.root, tearoff=False)
        self.menu.add_command(label="Toggle Highlight", command=lambda: self._toggle_highlight(None))
        self.menu.add_command(label="Edit Skill Level", command=lambda: self._begin_inline_level_edit(None))
        self.menu.add_command(label="Hide Item", command=self._hide_selected_item)
        self.menu.add_command(label="Unhide Item", command=self._unhide_selected_item)

        # Keyboard zoom shortcuts
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.reset_zoom())

    def zoom_in(self):
        self.zoom_level = min(self.zoom_level * 1.2, 3.0)
        self._apply_zoom()

    def zoom_out(self):
        self.zoom_level = max(self.zoom_level / 1.2, 0.6)
        self._apply_zoom()

    def reset_zoom(self):
        self.zoom_level = 1.0
        self._apply_zoom()

    def _apply_zoom(self):
        new_size = int(self.base_font_size * self.zoom_level)
        self.font.configure(size=new_size)
        try:
            self.style.configure("Treeview", font=self.font)
            self.style.configure("Treeview.Heading", font=self.font)
            self.style.configure("Action.TButton", font=self.font)
            self.style.configure("TLabel", font=self.font)
        except Exception:
            pass
        # Re-layout columns considering zoom and window size
        try:
            self._layout_tree_columns()
        except Exception:
            pass
        # Also increase row height with font size
        try:
            self._update_row_height()
        except Exception:
            pass
        # Adjust #0 width to fit icon at current zoom (keep compact for easier reading)
        try:
            self._update_tree_columns_layout()
        except Exception:
            pass

    def _update_row_height(self) -> None:
        """Adjust ttk Treeview row height based on current font and icon size."""
        # Compute line height from font metrics and add padding
        try:
            line_space = int(self.font.metrics("linespace"))
        except Exception:
            line_space = max(12, int(self.base_font_size * self.zoom_level))
        # Estimate icon height; prefer any loaded icon else a safe default
        try:
            icon_h = 0
            if getattr(self, "icon_images", None):
                for _k, img in self.icon_images.items():
                    try:
                        icon_h = max(icon_h, int(img.height()))
                    except Exception:
                        pass
            if icon_h == 0:
                icon_h = 24
        except Exception:
            icon_h = 24
        # Compose final row height (some padding so glyphs aren't clipped)
        # Provide extra left padding in the tree column to separate icon and star
        row_h = max(line_space + 10, icon_h + 6, 24)
        try:
            self.style.configure("Treeview", rowheight=row_h)
            # Slightly increase heading padding to match
            pad = max(4, int(row_h * 0.15))
            self.style.configure("Treeview.Heading", padding=(4, pad))
        except Exception:
            pass

    def _update_tree_columns_layout(self) -> None:
        """Ensure the image column (#0) is wide enough to avoid overlap with text, considering zoom and icon size."""
        # Determine max icon width
        try:
            icon_w = 0
            if getattr(self, "icon_images", None):
                for _k, img in self.icon_images.items():
                    try:
                        icon_w = max(icon_w, int(img.width()))
                    except Exception:
                        pass
            # Also account for composite marker+icon width if present
            if getattr(self, "display_images", None):
                for _k, img in self.display_images.items():
                    try:
                        icon_w = max(icon_w, int(img.width()))
                    except Exception:
                        pass
            if icon_w == 0:
                icon_w = 24
        except Exception:
            icon_w = 24
        # Compute scaled base width
        base_zero = self._base_tree_col_widths.get("#0", 36)
        scaled_zero = max(28, int(base_zero * self.zoom_level))
        # Require some margin to the next column
        required_zero = min(icon_w + 8, 56)
        final_zero = max(scaled_zero, required_zero)
        try:
            self.tree.column("#0", width=final_zero, stretch=False)
        except Exception:
            pass

    def _layout_tree_columns(self) -> None:
        """Responsive layout: scale fixed columns with zoom; distribute extra width to flex columns.

        Mix of fixed base widths (Option A) and responsive growth for key columns (Option C).
        """
        try:
            # Ensure icon column width is up-to-date
            self._update_tree_columns_layout()
            try:
                zero_w = int(self.tree.column("#0", option="width"))
            except Exception:
                zero_w = int(max(24, int(self._base_tree_col_widths.get("#0", 36) * self.zoom_level)))

            # Determine available tree width
            try:
                avail = int(self.tree.winfo_width())
            except Exception:
                avail = int(self.root.winfo_width() * 0.9)
            avail = max(800, avail)

            # Compute scaled fixed widths
            scaled: dict[str, int] = {}
            fixed_cols = ["mod", "skill_level", "station_lvl", "in_yaml"]
            for col in fixed_cols:
                bw = self._base_tree_col_widths.get(col, 80)
                scaled[col] = max(40, int(bw * self.zoom_level))

            # Base widths for flex columns before extra distribution
            flex_cols = [c for c in ("item", "station") if c in self._base_tree_col_widths]
            for col in flex_cols:
                bw = self._base_tree_col_widths.get(col, 120)
                scaled[col] = max(80, int(bw * self.zoom_level))

            # Total base width (zero + fixed + flex base)
            base_total = zero_w + sum(scaled.get(c, 0) for c in fixed_cols + flex_cols)
            extra = max(0, avail - base_total)

            if extra > 0 and flex_cols:
                # Distribute extra space based on weights
                weights = self._flex_weights if hasattr(self, "_flex_weights") else {"item": 1.0, "station": 1.0}
                w_sum = sum(weights.get(c, 0) for c in flex_cols) or 1.0
                for col in flex_cols:
                    add = int(extra * (weights.get(col, 0) / w_sum))
                    scaled[col] += add

            # Apply widths
            try:
                self.tree.column("item", width=scaled.get("item", 300))
            except Exception:
                pass
            try:
                self.tree.column("station", width=scaled.get("station", 200))
            except Exception:
                pass
            for col in fixed_cols:
                try:
                    self.tree.column(col, width=scaled[col])
                except Exception:
                    pass
        except Exception:
            pass

    def _on_window_resize(self, event) -> None:
        try:
            if event.widget is not self.root:
                return
            # Debounce rapid resize events
            if getattr(self, "_resize_after", None):
                try:
                    self.root.after_cancel(self._resize_after)
                except Exception:
                    pass
            self._resize_after = self.root.after(80, lambda: (setattr(self, "_resize_after", None), self._layout_tree_columns()))
        except Exception:
            pass

    def _create_star_marker(self, size: int = 12) -> tk.PhotoImage:
        """Create a simple gold 'star-like' marker image on panel-colored background."""
        bg = self.colors.get("panel", "#3b352a")
        star = tk.PhotoImage(width=size, height=size)
        # Fill background
        star.put(bg, to=(0, 0, size, size))
        # Draw a simple plus and x to resemble a star
        cx = size // 2
        cy = size // 2
        col1 = "#ffd24d"  # gold
        col2 = "#ffb300"  # darker gold
        for r in range(size):
            # vertical and horizontal
            star.put(col1, (cx, r))
            star.put(col1, (r, cy))
        # diagonals
        for d in range(size):
            star.put(col2, (d, d))
            star.put(col2, (size - 1 - d, d))
        # Thicken center
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                x = max(0, min(size - 1, cx + dx))
                y = max(0, min(size - 1, cy + dy))
                star.put(col1, (x, y))
        return star

    def _compose_marker_with_icon(self, icon: tk.PhotoImage | None, highlighted: bool) -> tk.PhotoImage | None:
        """Return a composite image with marker to the left of icon if highlighted."""
        if not highlighted:
            return icon
        if self.marker_img is None:
            return icon
        if icon is None:
            return self.marker_img
        try:
            mw = int(self.marker_img.width())
            mh = int(self.marker_img.height())
            iw = int(icon.width())
            ih = int(icon.height())
            pad = 4
            W = mw + pad + iw
            H = max(mh, ih)
            out = tk.PhotoImage(width=W, height=H)
            # Fill background
            bg = self.colors.get("panel", "#3b352a")
            out.put(bg, to=(0, 0, W, H))
            # Center vertically
            my = (H - mh) // 2
            iy = (H - ih) // 2
            # Copy marker
            out.tk.call(out, 'copy', self.marker_img, '-from', 0, 0, mw, mh, '-to', 0, my)
            # Copy icon
            out.tk.call(out, 'copy', icon, '-from', 0, 0, iw, ih, '-to', mw + pad, iy)
            return out
        except Exception:
            return icon

    def _get_display_icon(self, item_name: str, highlighted: bool) -> tk.PhotoImage | None:
        base = self._get_icon_for_item(item_name)
        key = (str(self.icon_paths.get(item_name.lower(), '')) or item_name.lower(), highlighted)
        if key in self.display_images:
            return self.display_images[key]
        img = self._compose_marker_with_icon(base, highlighted)
        if img is not None:
            self.display_images[key] = img
        return img

    def _show_context_menu(self, event) -> None:
        try:
            rowid = self.tree.identify_row(event.y)
            if rowid:
                current_sel = set(self.tree.selection())
                # If right-clicked row is not in the current selection, select just that row.
                # Otherwise, keep existing multi-selection intact.
                if rowid not in current_sel:
                    self.tree.selection_set(rowid)
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def _hide_selected_item(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        hidden = set(self.state.data.get("hidden_items", []) or [])
        for iid in sel:
            vals = list(self.tree.item(iid).get('values', []))
            if not vals:
                continue
            label = str(vals[0]).replace("★ ", "")
            m = re.search(r"\(([^)]+)\)$", label)
            if not m:
                continue
            prefab = m.group(1)
            hidden.add(prefab)
        self.state.data["hidden_items"] = sorted(hidden)
        self.state.save()
        self._filter_rows()

    def _unhide_selected_item(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        hidden = set(self.state.data.get("hidden_items", []) or [])
        for iid in sel:
            vals = list(self.tree.item(iid).get('values', []))
            if not vals:
                continue
            label = str(vals[0]).replace("★ ", "")
            m = re.search(r"\(([^)]+)\)$", label)
            if not m:
                continue
            prefab = m.group(1)
            if prefab in hidden:
                hidden.remove(prefab)
        self.state.data["hidden_items"] = sorted(hidden)
        self.state.save()
        self._filter_rows()

    def _on_tree_double_click(self, event) -> None:
        # If double-click on first column (#0), toggle highlight; if on skill_level column, begin inline edit
        try:
            col = self.tree.identify_column(event.x)
        except Exception:
            col = ''
        if col == '#1':
            self._toggle_highlight(event)
            return
        # New column order: #1 item, #2 mod, #3 skill_level, #4 station, #5 in_yaml
        if col == '#3':
            self._begin_inline_level_edit(event)
            return

    # Legacy selectors removed per request; rely on defaults
    def _choose_vnei(self) -> None:
        pass

    def _choose_skill(self) -> None:
        pass

    def _persist_state(self) -> None:
        self.state.save()
        self.status.set(f"Saved at {datetime.now().strftime('%H:%M:%S')}")

    def _autosize_item_column(self) -> None:
        """Autosize the Item column to fit the longest 'Name (Prefab)'."""
        try:
            max_text = 12
            for iid in self.tree.get_children(""):
                vals = self.tree.item(iid).get('values', [])
                if not vals:
                    continue
                s = str(vals[0])
                if len(s) > max_text:
                    max_text = len(s)
            # Estimate pixels per character (~7 at base font 10), scale with zoom
            px_per_char = max(6.0, 7.0 * self.zoom_level)
            new_width = int(px_per_char * (max_text + 2))
            new_width = max(240, min(new_width, 1000))
            self.tree.column("item", width=new_width)
        except Exception:
            pass

    def _begin_inline_level_edit(self, event) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        # Get bounding box for the skill_level cell (column index 2 for values)
        try:
            bbox = self.tree.bbox(iid, column="#3")
        except Exception:
            bbox = None
        vals = list(self.tree.item(iid).get('values', []))
        if len(vals) < 3:
            return
        current_item = str(vals[0]).lstrip('★ ').strip()
        current_level = str(vals[2]).strip()
        # Create an Entry overlay for inline edit
        var = tk.StringVar(value=current_level)
        entry = ttk.Entry(self.tree, textvariable=var, width=8)
        def place_entry():
            try:
                if bbox:
                    x, y, w, h = bbox
                    entry.place(x=x+2, y=y+1, width=w-4, height=h-2)
                    entry.focus_set()
            except Exception:
                pass
        place_entry()

        def commit_inline():
            val = var.get().strip()
            if val and not val.isdigit():
                messagebox.showerror("Invalid", "Enter a whole number (or leave blank to clear)")
                entry.destroy()
                return
            if val:
                vals[2] = val
                self.state.data.setdefault("skill_levels", {})[current_item] = val
            else:
                vals[2] = ""
                self.state.data.setdefault("skill_levels", {}).pop(current_item, None)
            self.tree.item(iid, values=vals)
            self.state.save()
            entry.destroy()

        entry.bind("<Return>", lambda e: commit_inline())
        entry.bind("<Escape>", lambda e: (entry.destroy()))
        entry.bind("<FocusOut>", lambda e: commit_inline())
        # Tab to next row's Skill Level
        def on_tab(_e):
            commit_inline()
            try:
                all_rows = list(self.tree.get_children(""))
                idx = all_rows.index(iid)
                if idx < len(all_rows) - 1:
                    next_iid = all_rows[idx + 1]
                    self.tree.selection_set(next_iid)
                    # Start inline edit on next row
                    self.tree.after(10, lambda: self._begin_inline_level_edit(None))
            except Exception:
                pass
            return "break"
        entry.bind("<Tab>", on_tab)

    def _bulk_set_level_from_entry(self) -> None:
        val = (self.bulk_level_var.get() or "").strip()
        if val and not val.isdigit():
            messagebox.showerror("Invalid", "Enter a whole number (or leave blank to clear)")
            return
        sel = self.tree.selection()
        if not sel:
            return
        for iid in sel:
            vals = list(self.tree.item(iid).get('values', []))
            if len(vals) < 3:
                continue
            item_label = str(vals[0]).replace("★ ", "")
            m = re.search(r"\(([^)]+)\)$", item_label)
            prefab = m.group(1) if m else item_label
            if val:
                vals[2] = val
                self.state.data.setdefault("skill_levels", {})[prefab] = val
            else:
                vals[2] = ""
                self.state.data.setdefault("skill_levels", {}).pop(prefab, None)
            self.tree.item(iid, values=vals)
        self.state.save()

    def _refresh_data(self) -> None:
        self.status.set("Loading VNEI items…")
        items_basic = self.vnei_index.load_items()
        items_rich = self.vnei_index.load_items_with_stats()
        meta = self.vnei_index.load_item_metadata()
        # Merge in Wacky Bulk YAML info
        self.status.set("Scanning Wacky Bulk YAML…")
        wacky = self.wacky_index.scan()
        self.status.set("Loading skill YAML…")
        yaml_items = self.skill_config.load_items()
        levels = self.skill_config.load_blacksmithing_levels()

        # Rebuild table
        self.tree.delete(*self.tree.get_children())
        self.all_item_iids: list[str] = []
        highlights: dict[str, bool] = self.state.data.setdefault("highlights", {})
        count_in_yaml = 0
        for item, station in sorted(items_basic.items(), key=lambda kv: kv[0].lower()):
            in_yaml = item in yaml_items
            if in_yaml:
                count_in_yaml += 1
            marked = highlights.get(item, False)
            img = self._get_display_icon(item, marked)
            # Load persisted manual level or from yaml if present
            manual_levels: dict[str, str] = self.state.data.setdefault("skill_levels", {})
            level_str = str(manual_levels.get(item, ""))
            if not level_str and item in levels:
                level_str = str(levels[item])
            # Mod/source from VNEI metadata
            meta_row = (meta.get(item, {}) or {})
            mod_name = meta_row.get('source_mod') or ''
            localized = meta_row.get('localized') or ''
            display_name = localized if localized else item
            item_label = f"{display_name} ({item})"
            # Do not prefix with a white star in text; composite icon carries the mark
            # Build item kwargs and avoid passing an invalid/None image to Tcl
            # Heuristic craftable: color item green if station is known
            craftable = bool(station or (items_rich.get(item, {}).get('station') or "") or (wacky.get(item, {}).get('station') or ""))
            # Pull station/station level & recipe from Wacky if present
            station_from_wacky = (wacky.get(item, {}) or {}).get('station') or station or (items_rich.get(item, {}).get('station') or "")
            station_lvl_from_wacky = (wacky.get(item, {}) or {}).get('station_level') or ""
            item_kwargs = {
                "text": "",
                "values": (item_label, mod_name, level_str, station_from_wacky or "", str(station_lvl_from_wacky) if station_lvl_from_wacky else "", "Yes" if in_yaml else "No"),
            }
            if img is not None:
                item_kwargs["image"] = img
            iid_new = self.tree.insert("", "end", tags=("craftable",) if craftable else (), **item_kwargs)
            self.all_item_iids.append(iid_new)

        self.status.set(f"Loaded {len(items_basic)} items; {count_in_yaml} in skill YAML. Use search to filter; double-click or Space to toggle highlight.")
        self._filter_rows()  # apply any current filter
        try:
            self._layout_tree_columns()
        except Exception:
            pass

    def _filter_rows(self) -> None:
        needle = (self.search_var.get() or "").strip().lower()
        hidden = set(self.state.data.get("hidden_items", []) or [])
        show_mode = (self.show_filter.get() if hasattr(self, 'show_filter') else "Visible")
        source_iids = getattr(self, 'all_item_iids', None)
        if not source_iids:
            source_iids = list(self.tree.get_children(""))
        for iid in source_iids:
            vals = self.tree.item(iid).get('values', [])
            # Build text from item label only for matching
            text = (str(vals[0]) if vals else '').lower()
            # Determine item's prefab from label "Name (Prefab)"
            prefab = None
            try:
                label = str(vals[0]) if vals else ''
                m = re.search(r"\(([^)]+)\)$", label.replace("★ ", ""))
                if m:
                    prefab = m.group(1)
            except Exception:
                prefab = None
            is_hidden = prefab in hidden if prefab else False
            visible = True
            if show_mode == "Visible" and is_hidden:
                visible = False
            elif show_mode == "Hidden" and not is_hidden:
                visible = False
            if needle and needle not in text:
                visible = False
            if visible:
                try:
                    self.tree.reattach(iid, '', 'end')
                except Exception:
                    # Fallback to move if reattach not available
                    try:
                        self.tree.move(iid, '', 'end')
                    except Exception:
                        pass
            else:
                try:
                    self.tree.detach(iid)
                except Exception:
                    pass
        try:
            self._layout_tree_columns()
        except Exception:
            pass

    def _toggle_highlight(self, event) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = list(self.tree.item(iid).get('values', []))
        if not vals:
            return
        item_text = str(vals[0])
        # Manage star prefix without breaking the "Name (Prefab)" content
        has_star = item_text.startswith("★ ")
        plain = item_text[2:].lstrip() if has_star else item_text
        new_item_text = plain if has_star else f"★ {plain}"
        vals[0] = new_item_text
        # Rebuild composite icon for this item
        try:
            base_prefab = plain
            # Try to recover prefab from parentheses if present
            m = re.search(r"\(([^)]+)\)$", plain)
            if m:
                base_prefab = m.group(1)
            img = self._get_display_icon(base_prefab, not has_star)
            if img is not None:
                self.tree.item(iid, image=img, values=vals, text="")
            else:
                self.tree.item(iid, image="", values=vals, text="")
        except Exception:
            self.tree.item(iid, values=vals, text="")
        # Persist by prefab key if we could parse it, else by plain name
        key_for_highlight = base_prefab
        self.state.data.setdefault("highlights", {})[key_for_highlight] = not has_star
        # Save immediately for persistence
        self.state.save()
        try:
            self._autosize_item_column()
        except Exception:
            pass

    def _mark_all_filtered(self) -> None:
        for iid in self.tree.get_children(""):
            vals = list(self.tree.item(iid).get('values', []))
            if not vals:
                continue
            item_text = str(vals[0])
            plain = item_text[2:].lstrip() if item_text.startswith("★ ") else item_text
            vals[0] = f"★ {plain}"
            base_prefab = plain
            m = re.search(r"\(([^)]+)\)$", plain)
            if m:
                base_prefab = m.group(1)
            img = self._get_display_icon(base_prefab, True)
            if img is not None:
                self.tree.item(iid, image=img, values=vals, text="")
            else:
                self.tree.item(iid, image="", values=vals, text="")
            self.state.data.setdefault("highlights", {})[base_prefab] = True
        self.state.save()

    def _unmark_all_filtered(self) -> None:
        for iid in self.tree.get_children(""):
            vals = list(self.tree.item(iid).get('values', []))
            if not vals:
                continue
            item_text = str(vals[0])
            plain = item_text[2:].lstrip() if item_text.startswith("★ ") else item_text
            vals[0] = plain
            base_prefab = plain
            m = re.search(r"\(([^)]+)\)$", plain)
            if m:
                base_prefab = m.group(1)
            img = self._get_display_icon(base_prefab, False)
            if img is not None:
                self.tree.item(iid, image=img, values=vals, text="")
            else:
                self.tree.item(iid, image="", values=vals, text="")
            self.state.data.setdefault("highlights", {})[base_prefab] = False
        self.state.save()

    def _write_to_config(self) -> None:
        """Append new items with entered levels to the target YAML in required format.

        - Only adds entries that are not already present by PrefabName.
        - If config file doesn't exist, creates it.
        """
        # Determine target file: if user selected a specific YAML, respect that; else default under config_dir
        # Always write to the default Detalhes file in config directory
        target = self.config_dir / "Detalhes.ItemRequiresSkillLevel.yml"
        try:
            existing_text = target.read_text(encoding='utf-8') if target.exists() else ""
        except Exception:
            existing_text = ""

        existing_items: set[str] = set()
        # Parse existing PrefabName lines (fast heuristic)
        for line in existing_text.splitlines():
            m = re.match(r"^\s*-\s*PrefabName:\s*([A-Za-z0-9_\-\.]+)\s*$", line)
            if m:
                existing_items.add(m.group(1))

        # Collect desired writes from UI state
        levels_map: dict[str, str] = self.state.data.get("skill_levels", {})
        # Also include any levels inferred from load_blacksmithing_levels that user hasn't overridden?
        # We'll only write items that have a manual level in UI to avoid surprises

        to_write: list[tuple[str, str]] = []  # (item, level)
        for item, level in levels_map.items():
            level_str = str(level).strip()
            if not level_str:
                continue
            if item in existing_items:
                continue
            to_write.append((item, level_str))

        if not to_write:
            messagebox.showinfo("Write", "No new items to write. Either all are already present or no levels entered.")
            return

        # Build YAML chunks
        chunks: list[str] = []
        for item, lvl in sorted(to_write, key=lambda x: x[0].lower()):
            chunks.append(
                "- PrefabName: " + item + "\n" +
                "  Requirements:\n" +
                "    - Skill: Blacksmithing\n" +
                f"      Level: {lvl}\n" +
                "      BlockCraft: true\n" +
                "      BlockEquip: false\n" +
                "      EpicMMO: false\n" +
                "      ExhibitionName: \n"
            )

        new_text = existing_text.rstrip() + ("\n\n" if existing_text.strip() else "") + "\n".join(chunks) + "\n"

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(new_text, encoding='utf-8', newline='\n')
            # No need to persist a chosen file; path is fixed
            messagebox.showinfo("Write", f"Wrote {len(to_write)} new entr{'y' if len(to_write)==1 else 'ies'} to\n{target}")
        except Exception as e:
            messagebox.showerror("Write", f"Failed to write configuration: {e}")

    def _export_items_mod_md(self) -> None:
        """Export Markdown: item prefabs, localized names, and associated source mod."""
        try:
            items_basic = self.vnei_index.load_items()
            meta = self.vnei_index.load_item_metadata()
            hidden = set(self.state.data.get("hidden_items", []) or [])
            manual_levels: dict[str, str] = self.state.data.get("skill_levels", {})
            lines: list[str] = []
            lines.append("# Items by Mod\n")
            lines.append("Generated by Item Skill Tracker\n")
            lines.append("")
            lines.append("| Prefab | Localized | Mod |")
            lines.append("|---|---|---|")
            def esc(s: str) -> str:
                return (s or "").replace('|', '\\|')
            for item in sorted(items_basic.keys(), key=lambda s: s.lower()):
                if item in hidden:
                    continue
                # Only include items without a manually assigned skill level
                lvl = str(manual_levels.get(item, "")).strip()
                if lvl:
                    continue
                m = meta.get(item, {})
                localized = m.get('localized') or ''
                mod = m.get('source_mod') or ''
                lines.append(f"| `{esc(item)}` | {esc(localized)} | {esc(mod)} |")
            export_path = self.workspace / "Valheim_Help_Docs" / "Files for GPT" / "Items_By_Mod.md"
            export_path.parent.mkdir(parents=True, exist_ok=True)
            export_path.write_text("\n".join(lines) + "\n", encoding='utf-8', newline='\n')
            messagebox.showinfo("Export", f"Markdown exported to\n{export_path}")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export markdown: {e}")

    # (WL inference/export removed from GUI per request)

    def _export_ai_summary_jsonl(self) -> None:
        """Export a compact JSONL summary per item for AI contexts (minimal but complete)."""
        try:
            self.status.set("Building AI summary…")
            # Load sources
            items_basic = self.vnei_index.load_items()
            meta = self.vnei_index.load_item_metadata()
            wacky = self.wacky_index.scan()
            levels_yaml = self.skill_config.load_blacksmithing_levels()
            manual_levels: dict[str, str] = self.state.data.get("skill_levels", {})

            lines: list[str] = []
            for item in sorted(items_basic.keys(), key=lambda s: s.lower()):
                m = meta.get(item, {}) or {}
                w = wacky.get(item, {}) or {}
                # Compose minimal, readable record
                rec = {
                    "pf": item,  # prefab
                }
                if m.get('localized'):
                    rec["nm"] = m.get('localized')
                if m.get('source_mod'):
                    rec["md"] = m.get('source_mod')
                # Station and level
                st = w.get('station') or ""
                if st:
                    rec["st"] = st
                sl = w.get('station_level')
                if isinstance(sl, int) and sl > 0:
                    rec["sl"] = sl
                # Skill level preference: manual > yaml > none
                lvl = (manual_levels.get(item) or levels_yaml.get(item))
                try:
                    if lvl is not None and str(lvl).strip() != "":
                        rec["sk"] = int(lvl)
                except Exception:
                    pass
                # Recipe
                rlist = w.get('recipe') or []
                if rlist:
                    # Normalize to [[mat, qty], ...]
                    try:
                        rec["rec"] = [[a, int(b)] for a, b in rlist if a]
                    except Exception:
                        rec["rec"] = [[str(a), int(b)] if str(b).isdigit() else [str(a), str(b)] for a, b in rlist]
                # Stats (only include present ones)
                stx = w.get('stats') or {}
                stats_out = {}
                for k_src, k_out in [("damage_total", "dm"), ("armor", "ar"), ("weight", "wt"), ("block", "bl"), ("durability", "du")]:
                    v = stx.get(k_src)
                    if v is not None and str(v).strip() != "":
                        try:
                            # store numeric when possible
                            val = float(v)
                            stats_out[k_out] = int(val) if val.is_integer() else round(val, 2)
                        except Exception:
                            stats_out[k_out] = v
                if stats_out:
                    rec["sx"] = stats_out
                # Tier / WL / rarity
                if isinstance(w.get('tier'), int):
                    rec["ti"] = w.get('tier')
                if isinstance(w.get('world_level'), int):
                    rec["wl"] = w.get('world_level')
                if w.get('rarity'):
                    rec["ra"] = w.get('rarity')

                lines.append(json.dumps(rec, ensure_ascii=False))

            export_path = self.workspace / "Valheim_Help_Docs" / "Files for GPT" / "Items_AI_Summary.jsonl"
            export_path.parent.mkdir(parents=True, exist_ok=True)
            export_path.write_text("\n".join(lines) + "\n", encoding='utf-8', newline='\n')

            # Put into clipboard as well (optional nice-to-have)
            try:
                self.root.clipboard_clear()
                # Limit clipboard to a reasonable size chunk if extremely large
                blob = "\n".join(lines)
                self.root.clipboard_append(blob)
            except Exception:
                pass

            messagebox.showinfo("Export", f"AI summary exported to\n{export_path}\n\nAlso copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export AI summary: {e}")

    def _index_icons(self) -> None:
        """Scan VNEI-Export/icons for PNGs and index by basename (lower)."""
        icons_dir = self.vnei_dir / "icons"
        self.icon_paths.clear()
        if not icons_dir.exists():
            return
        for path in icons_dir.rglob("*.png"):
            key = path.stem.lower()
            # Do not overwrite existing keys; prefer first found
            if key not in self.icon_paths:
                self.icon_paths[key] = path

    def _get_icon_for_item(self, item_name: str) -> tk.PhotoImage | None:
        """Return a Tk image for the item if we can find a matching icon."""
        key = item_name.lower()
        # Try exact
        path = self.icon_paths.get(key)
        if not path:
            # Try simple normalizations
            simple = re.sub(r"[^a-z0-9]+", "", key)
            for k, p in self.icon_paths.items():
                if simple == re.sub(r"[^a-z0-9]+", "", k):
                    path = p
                    break
        if not path:
            # Try contains
            for k, p in self.icon_paths.items():
                if key in k:
                    path = p
                    break
        if not path:
            return None
        # Cache PhotoImage
        cache_key = str(path)
        img = self.icon_images.get(cache_key)
        if img is None:
            try:
                img = tk.PhotoImage(file=str(path))
                # Optionally downscale large icons
                if img.width() > 32:
                    # crude subsample to fit ~32px
                    factor = max(1, int(img.width() / 32))
                    img = img.subsample(factor, factor)
                self.icon_images[cache_key] = img
            except Exception:
                return None
        return img


def default_workspace() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    ws = default_workspace()
    root = tk.Tk()
    app = ItemSkillTrackerApp(root, ws)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


