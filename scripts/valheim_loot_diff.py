#!/usr/bin/env python3
"""
valheim_loot_diff.py v1.1 — Compare baseline vs active Valheim loot material rates (RelicHeim/EpicLoot tiers).

What's new in v1.1 (relative to v1.0):
- Added tier synonyms: "Essence", "Reagent".
- Ignores VNEI export folders by default to avoid noise.
- Heuristic support for EpicLoot patch JSONs (e.g., zLootables_TreasureLoot_RelicHeim.json, zLootables_Equipment_RelicHeim.json).
  - Walks nested dicts/lists for tables with drops and weights; accepts "Rarity" as explicit tier.
- Optional YAML (PyYAML) parsing for pickable item lists (e.g., warpalicious More_World_Locations *.yml).
- Optional per-character composition: --compose-characters produces a character-level expected tier report by combining CharacterDrop entries with referenced DropTables.

Usage (unchanged for set diff):
    python valheim_loot_diff.py --baseline ./baseline_cfg --active ./ValheimMods/config --out ./loot_report

Extra options:
    --compose-characters        -> emit loot_report.characters.csv (best-effort per-kill tier expectation)
    --include-path path         -> repeatable; if provided, only include files under these paths (globs ok)
"""

import argparse
import os
import re
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple, Optional, Any
import json
import html
from fnmatch import fnmatch

# -------------------------------
# Heuristics / helpers
# -------------------------------

# Default regex mapping for item -> tier. Override with --tier-map-json
DEFAULT_TIER_PATTERNS = {
    "Mythic":    r"(?:mythic|runestonemythic|shardmythic|dustmythic|essencemythic|reagentmythic)",
    "Legendary": r"(?:legendary|runestonelegendary|shardlegendary|dustlegendary|essencelegendary|reagentlegendary)",
    "Epic":      r"(?:epic|runestoneepic|shardepic|dustepic|essenceepic|reagentepic)",
    "Rare":      r"(?:rare|runestonerare|shardrare|dustrare|essencerare|reagentrare)",
    "Magic":     r"(?:magic|runestonemagic|shardmagic|dustmagic|novus|essencemagic|reagentmagic)",
}

# Keys we look for when parsing entries/tables
ITEM_KEYS     = {"item", "prefab", "prefabname", "name"}
WEIGHT_KEYS   = {"weight", "setweight", "entryweight", "weightwhenrolled"}
CHANCE_KEYS   = {"chance", "dropchance", "probability", "rollchance"}
SET_KEYS      = {"set", "setname", "droptable", "table", "group", "parent", "pool"}
COUNT_MIN_KEYS= {"min", "amountmin", "dropmin", "rollsmin"}
COUNT_MAX_KEYS= {"max", "amountmax", "dropmax", "rollsmax"}
COUNT_ONEOF   = {"droponeof", "oneof", "pickone", "pickamount"}

Section = namedtuple("Section", ["name", "fields", "lineno", "file"])

def normkey(k: str) -> str:
    return re.sub(r"[^a-z0-9]", "", k.lower())

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def scan_sections_ini_like(text: str, file: str) -> List[Section]:
    sections = []
    cur_name = None
    cur = {}
    start_line = 1
    lines = text.splitlines()
    for idx, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("//") or s.startswith(";"):
            continue
        m = re.match(r"\[(.+?)\]\s*$", s)
        if m:
            if cur_name is not None:
                sections.append(Section(cur_name, cur, start_line, file))
            cur_name = m.group(1).strip()
            cur = {}
            start_line = idx
            continue
        m2 = re.match(r"([^:=]+)[:=]\s*(.+?)\s*$", s)
        if m2 and cur_name is not None:
            k = normkey(m2.group(1))
            v = m2.group(2).strip()
            v = re.split(r"\s*[#;] ", v)[0].strip()
            cur[k] = v
    if cur_name is not None:
        sections.append(Section(cur_name, cur, start_line, file))
    return sections

def guess_is_entry(sec: Section) -> bool:
    has_item = any(k in sec.fields for k in ITEM_KEYS)
    has_weight = any(k in sec.fields for k in WEIGHT_KEYS)
    has_set = any(k in sec.fields for k in SET_KEYS)
    return (has_item and (has_weight or has_set)) or (has_weight and has_set)

def guess_is_table(sec: Section) -> bool:
    has_roll = any(k in sec.fields for k in COUNT_MIN_KEYS|COUNT_MAX_KEYS|COUNT_ONEOF|CHANCE_KEYS)
    lacks_item = all(k not in sec.fields for k in ITEM_KEYS)
    return has_roll and lacks_item

def extract_item_name(fields: Dict[str,str]) -> Optional[str]:
    for k in ITEM_KEYS:
        if k in fields:
            return fields[k]
    return None

def extract_weight(fields: Dict[str,str]) -> float:
    for k in WEIGHT_KEYS:
        if k in fields:
            try:
                return float(fields[k])
            except:
                pass
    return 1.0

def parse_percentish(v: Any) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        val = float(v)
        if val > 1.0 and val <= 100.0:  # handle 10..100 as %
            return val/100.0
        return max(min(val, 1.0), 0.0)
    if isinstance(v, str):
        s = v.strip()
        if s.endswith("%"):
            try:
                return max(min(float(s.strip("%"))/100.0, 1.0), 0.0)
            except:
                return None
        try:
            val = float(s)
            if val > 1.0 and val <= 100.0:
                return val/100.0
            return max(min(val, 1.0), 0.0)
        except:
            return None
    return None

def extract_chance(fields: Dict[str,str]) -> float:
    for k in CHANCE_KEYS:
        if k in fields:
            v = fields[k]
            c = parse_percentish(v)
            if c is not None:
                return c
    return 1.0

def extract_set(fields: Dict[str,str]) -> Optional[str]:
    for k in SET_KEYS:
        if k in fields:
            return fields[k]
    return None

def extract_minmax(fields: Dict[str,str]) -> Tuple[Optional[int], Optional[int]]:
    mn = None
    mx = None
    for k in COUNT_MIN_KEYS:
        if k in fields:
            try:
                mn = int(float(fields[k]))
                break
            except:
                pass
    for k in COUNT_MAX_KEYS:
        if k in fields:
            try:
                mx = int(float(fields[k]))
                break
            except:
                pass
    return mn, mx

def find_oneof(fields: Dict[str,str]) -> Optional[int]:
    for k in COUNT_ONEOF:
        if k in fields:
            try:
                return int(float(fields[k]))
            except:
                pass
    return None

# -------------------------------
# Data model
# -------------------------------

class LootSet:
    def __init__(self, name: str):
        self.name = name
        # entries: list of dicts: {"item": str|None, "weight": float, "chance": float, "tier": Optional[str]}
        self.entries: List[Dict[str, Any]] = []
        self.table_chance = 1.0
        self.rolls_min = None
        self.rolls_max = None
        self.pick_one_of = None

    def add_entry(self, item: Optional[str], weight: float, chance: float, tier: Optional[str] = None):
        self.entries.append({"item": item, "weight": max(weight, 0.0), "chance": max(min(chance, 1.0), 0.0), "tier": tier})

    def set_table_meta(self, chance: Optional[float], mn: Optional[int], mx: Optional[int], oneof: Optional[int]):
        if chance is not None:
            self.table_chance = max(min(chance, 1.0), 0.0)
        if mn is not None:
            self.rolls_min = mn
        if mx is not None:
            self.rolls_max = mx
        if oneof is not None:
            self.pick_one_of = oneof

    def normalized_entry_probs(self) -> List[Tuple[Dict[str, Any], float]]:
        weights = []
        for e in self.entries:
            weights.append(max(e["weight"], 0.0) * max(min(e["chance"], 1.0), 0.0))
        total = sum(weights)
        if total <= 0:
            return [(e, 0.0) for e in self.entries]
        return [(self.entries[i], weights[i]/total) for i in range(len(self.entries))]

    def expected_picks(self) -> Optional[float]:
        picks = None
        if self.pick_one_of is not None:
            picks = float(self.pick_one_of)
        elif self.rolls_min is not None and self.rolls_max is not None:
            lo, hi = int(self.rolls_min), int(self.rolls_max)
            if hi < lo:
                lo, hi = hi, lo
            n = hi - lo + 1
            picks = sum(range(lo, hi+1))/n
        elif self.rolls_min is not None:
            picks = float(self.rolls_min)
        elif self.rolls_max is not None:
            picks = float(self.rolls_max)
        if picks is None:
            return None
        return self.table_chance * picks

def tier_of(item: Optional[str], tier_regex: Dict[str, str]) -> Optional[str]:
    if item is None:
        return None
    s = item.lower()
    for tier, patt in tier_regex.items():
        if re.search(patt, s):
            return tier
    return None

def summarize_set_by_tier(ls: LootSet, tier_regex: Dict[str,str]) -> Dict[str, float]:
    by_tier = defaultdict(float)
    for e, p in ls.normalized_entry_probs():
        t = e.get("tier") or tier_of(e.get("item"), tier_regex)
        if t:
            by_tier[t] += p
    for t in ["Magic","Rare","Epic","Legendary","Mythic"]:
        by_tier[t] += 0.0
    return dict(by_tier)

# -------------------------------
# Parsing configs into LootSets
# -------------------------------

def find_sets_in_text(text: str, file: str) -> Dict[str, LootSet]:
    sections = scan_sections_ini_like(text, file)
    sets: Dict[str, LootSet] = {}
    # First pass: entries that reference a set/table by name
    for sec in sections:
        if guess_is_entry(sec):
            fields = sec.fields
            item = extract_item_name(fields)
            weight = extract_weight(fields)
            chance = extract_chance(fields)
            setname = extract_set(fields)
            if not setname:
                m = re.match(r"(?i)(?:droptable|pool|set|group)\.([^.\]]+)\.", sec.name)
                if m:
                    setname = m.group(1)
            if item or setname:
                # if no set, we treat section header name as a pseudo-set to avoid losing entries
                setname = setname or sec.name
                ls = sets.setdefault(setname, LootSet(setname))
                ls.add_entry(item, weight, chance)
    # Second pass: table-level metadata for sets
    for sec in sections:
        if guess_is_table(sec):
            fields = sec.fields
            target = extract_set(fields)
            if not target:
                m = re.match(r"(?i)(?:droptable|pool|set|group)\.([^.\]]+)(?:\.\d+)?$", sec.name)
                if m:
                    target = m.group(1)
            if target:
                mn, mx = extract_minmax(fields)
                ch = extract_chance(fields)
                oneof = find_oneof(fields)
                ls = sets.setdefault(target, LootSet(target))
                ls.set_table_meta(ch, mn, mx, oneof)
    return sets

def crawl_configs(root: str, include_paths: List[str]) -> Dict[str, LootSet]:
    lootsets: Dict[str, LootSet] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip VNEI exports (noise)
        if "VNEI-Export" in dirpath:
            continue
        for fn in filenames:
            low = fn.lower()
            p = os.path.join(dirpath, fn)
            # If include_paths are provided, enforce them
            if include_paths:
                matched = any(fnmatch(p, patt) or fnmatch(p.replace("\\","/"), patt) for patt in include_paths)
                if not matched:
                    continue
            if not (low.endswith((".cfg",".ini",".txt",".conf",".toml",".yml",".yaml",".json"))):
                continue
            try:
                txt = read_text(p)
            except Exception:
                continue

            handled_json = False
            # Try specialized JSON walker for EpicLoot patches
            if low.endswith(".json"):
                try:
                    data = json.loads(txt)
                    # If object, walk it for tables/drops
                    if isinstance(data, dict):
                        sets_from_json = parse_epicloot_json(data, file_hint=fn)
                        for k, v in sets_from_json.items():
                            dst = lootsets.setdefault(k, LootSet(k))
                            dst.entries.extend(v.entries)
                            if (dst.rolls_min, dst.rolls_max, dst.pick_one_of) == (None, None, None):
                                dst.table_chance = v.table_chance
                                dst.rolls_min = v.rolls_min
                                dst.rolls_max = v.rolls_max
                                dst.pick_one_of = v.pick_one_of
                        handled_json = True
                except Exception:
                    pass

            if handled_json:
                continue

            # Optional YAML parsing (requires PyYAML)
            if low.endswith((".yml",".yaml")):
                try:
                    import yaml  # type: ignore
                    data = yaml.safe_load(txt)
                    if data is not None:
                        sets_from_yaml = parse_pickables_yaml(data, file_hint=fn)
                        for k, v in sets_from_yaml.items():
                            dst = lootsets.setdefault(k, LootSet(k))
                            dst.entries.extend(v.entries)
                            if (dst.rolls_min, dst.rolls_max, dst.pick_one_of) == (None, None, None):
                                dst.table_chance = v.table_chance
                                dst.rolls_min = v.rolls_min
                                dst.rolls_max = v.rolls_max
                                dst.pick_one_of = v.pick_one_of
                        continue
                except Exception:
                    # fall back to INI-like heuristic
                    pass

            # INI-like parsing (Drop That)
            found = find_sets_in_text(txt, p)
            for k, v in found.items():
                dst = lootsets.setdefault(k, LootSet(k))
                dst.entries.extend(v.entries)
                if (dst.rolls_min, dst.rolls_max, dst.pick_one_of) == (None, None, None):
                    dst.table_chance = v.table_chance
                    dst.rolls_min = v.rolls_min
                    dst.rolls_max = v.rolls_max
                    dst.pick_one_of = v.pick_one_of
    return lootsets

# ---- Specialized parsers ----

def parse_epicloot_json(obj: Any, file_hint: str = "") -> Dict[str, LootSet]:
    """
    Heuristically detect loot tables in EpicLoot patch JSONs.
    Looks for dicts with "Name"/"Table"/"LootTable" and a list called "Drops"/"Loot"/"Entries".
    Accepts entries with ("Prefab"/"Item"/"Name") + ("Weight" or "Chance").
    If an entry has "Rarity": "Magic/Rare/..." we record explicit tier and omit item mapping.
    """
    sets: Dict[str, LootSet] = {}

    def add_set_entry(setname: str, item: Optional[str], weight: float, chance: float, tier: Optional[str] = None):
        ls = sets.setdefault(setname, LootSet(setname))
        ls.add_entry(item, weight, chance, tier)

    def walk(node: Any, ctx_name: Optional[str] = None, table_meta: Optional[Dict[str, Any]] = None):
        if isinstance(node, dict):
            # infer set/table name
            setname = ctx_name
            for k in ["name","tablename","table","loottable"]:
                if k in node and isinstance(node[k], str):
                    setname = node[k]
                    break
            # parse table-level meta if available
            ch = parse_percentish(node.get("chance"))
            mn = node.get("min") if isinstance(node.get("min"), int) else None
            mx = node.get("max") if isinstance(node.get("max"), int) else None
            oneof = node.get("oneof") if isinstance(node.get("oneof"), int) else None
            new_meta = {"chance": ch, "min": mn, "max": mx, "oneof": oneof}

            # If we have a concrete set and meta, record it
            if setname:
                ls = sets.setdefault(setname, LootSet(setname))
                ls.set_table_meta(ch, mn, mx, oneof)

            # Detect drops arrays
            for drops_key in ["drops","loot","entries","items"]:
                if drops_key in node and isinstance(node[drops_key], list) and setname:
                    for e in node[drops_key]:
                        if isinstance(e, dict):
                            item = None
                            for k in ["prefab","item","name"]:
                                if k in e and isinstance(e[k], str):
                                    item = e[k]
                                    break
                            weight = e.get("weight", 1.0)
                            try:
                                weight = float(weight)
                            except:
                                weight = 1.0
                            chance = parse_percentish(e.get("chance"))
                            if chance is None:
                                chance = 1.0
                            rarity = e.get("rarity")
                            tier = None
                            if isinstance(rarity, str):
                                r = rarity.strip().lower()
                                if r in ("magic","rare","epic","legendary","mythic"):
                                    tier = r.capitalize()
                            add_set_entry(setname, item, weight, chance, tier)
            # Recurse into values
            for v in node.values():
                walk(v, setname, new_meta)
        elif isinstance(node, list):
            for v in node:
                walk(v, ctx_name, table_meta)
        else:
            return

    walk(obj)
    return sets

def parse_pickables_yaml(obj: Any, file_hint: str = "") -> Dict[str, LootSet]:
    """
    Heuristic for world pickable item lists (warpalicious More_World_Locations).
    We look for lists of items with Weight/Chance under a named group.
    """
    sets: Dict[str, LootSet] = {}
    def add(name: str, item: Optional[str], weight: float, chance: float):
        ls = sets.setdefault(name, LootSet(name))
        ls.add_entry(item, weight, chance)

    def walk(node: Any, ctx_name: Optional[str] = None):
        if isinstance(node, dict):
            name = ctx_name
            # use explicit Name if present
            for k in ["Name","ListName","Group","Table"]:
                if k in node and isinstance(node[k], str):
                    name = node[k]
                    break
            # entries under common keys
            for drops_key in ["Items","Drops","Entries","PickableItemList","Pickables"]:
                if drops_key in node and isinstance(node[drops_key], list) and name:
                    for e in node[drops_key]:
                        if isinstance(e, dict):
                            item = None
                            for k in ["Item","Prefab","Name"]:
                                if k in e and isinstance(e[k], str):
                                    item = e[k]
                                    break
                            weight = e.get("Weight", 1.0)
                            try:
                                weight = float(weight)
                            except:
                                weight = 1.0
                            chance = parse_percentish(e.get("Chance"))
                            if chance is None:
                                chance = 1.0
                            add(name, item, weight, chance)
            for v in node.values():
                walk(v, name)
        elif isinstance(node, list):
            for v in node:
                walk(v, ctx_name)
    walk(obj)
    return sets

# -------------------------------
# Character composition (optional)
# -------------------------------

class CharacterDrops:
    def __init__(self, name: str):
        self.name = name
        # list of {"set": setname, "chance": float, "min": int|None, "max": int|None, "oneof": int|None}
        self.table_refs: List[Dict[str, Any]] = []
        # direct items
        self.direct: List[Dict[str, Any]] = []  # {"item": str, "chance": float, "weight": float}

def parse_characters_from_text(text: str, file: str) -> Dict[str, CharacterDrops]:
    sections = scan_sections_ini_like(text, file)
    chars: Dict[str, CharacterDrops] = {}
    for sec in sections:
        if re.match(r"(?i)characterdrop\.", sec.name):
            # Extract character name: CharacterDrop.<Name> or CharacterDrop.<Name>.<idx>
            m = re.match(r"(?i)characterdrop\.([^.\]]+)", sec.name)
            cname = m.group(1) if m else sec.name
            cd = chars.setdefault(cname, CharacterDrops(cname))
            fields = sec.fields
            setname = extract_set(fields)
            ch = extract_chance(fields)
            mn, mx = extract_minmax(fields)
            oneof = find_oneof(fields)
            item = extract_item_name(fields)
            weight = extract_weight(fields)
            if setname:
                cd.table_refs.append({"set": setname, "chance": ch, "min": mn, "max": mx, "oneof": oneof, "weight": weight})
            elif item:
                cd.direct.append({"item": item, "chance": ch, "weight": weight})
    return chars

def crawl_characters(root: str, include_paths: List[str]) -> Dict[str, CharacterDrops]:
    out: Dict[str, CharacterDrops] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        if "VNEI-Export" in dirpath:
            continue
        for fn in filenames:
            low = fn.lower()
            p = os.path.join(dirpath, fn)
            if include_paths:
                from fnmatch import fnmatch
                matched = any(fnmatch(p, patt) or fnmatch(p.replace("\\","/"), patt) for patt in include_paths)
                if not matched:
                    continue
            if not (low.endswith((".cfg",".ini",".txt",".conf",".toml"))):
                continue
            try:
                txt = read_text(p)
            except Exception:
                continue
            chars = parse_characters_from_text(txt, p)
            for k, v in chars.items():
                dst = out.setdefault(k, CharacterDrops(k))
                dst.table_refs.extend(v.table_refs)
                dst.direct.extend(v.direct)
    return out

# -------------------------------
# Diff & reporting
# -------------------------------

def compute_shares(sets: Dict[str, LootSet], tier_regex: Dict[str,str]) -> Dict[str, Dict[str, float]]:
    out = {}
    for name, ls in sets.items():
        out[name] = summarize_set_by_tier(ls, tier_regex)
    return out

def write_csv(path: str, rows: List[Dict[str, str]]):
    import csv
    if not rows:
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)

def render_html_table(rows: List[Dict[str,str]], title: str) -> str:
    if not rows:
        return f"<h2>{html.escape(title)}</h2><p>No rows.</p>"
    headers = list(rows[0].keys())
    ths = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    trs = []
    for r in rows:
        tds = "".join(f"<td>{html.escape(str(r.get(h, '')))}</td>" for h in headers)
        trs.append(f"<tr>{tds}</tr>")
    body = "\n".join(trs)
    return f"<h2>{html.escape(title)}</h2><table border='1' cellspacing='0' cellpadding='4'><thead><tr>{ths}</tr></thead><tbody>{body}</tbody></table>"

def percent(x: float) -> str:
    return f"{x*100:.2f}%"

def compose_characters_report(char_map: Dict[str, CharacterDrops], set_map: Dict[str, LootSet], tier_regex: Dict[str,str]) -> List[Dict[str,str]]:
    rows = []
    # Precompute per-pick tier share for sets
    set_share = {k: summarize_set_by_tier(v, tier_regex) for k, v in set_map.items()}
    set_picks = {k: v.expected_picks() or 1.0 for k, v in set_map.items()}
    for cname, cd in sorted(char_map.items(), key=lambda x: x[0].lower()):
        tier_counts = defaultdict(float)
        # combine table refs
        for ref in cd.table_refs:
            sname = ref.get("set")
            if sname in set_share:
                picks = set_picks.get(sname, 1.0)
                chance = max(min(float(ref.get("chance",1.0)), 1.0), 0.0)
                mult = chance * picks
                for tier, share in set_share[sname].items():
                    tier_counts[tier] += mult * share
        # direct items
        for e in cd.direct:
            t = tier_of(e.get("item"), tier_regex)
            if t:
                chance = max(min(float(e.get("chance",1.0)), 1.0), 0.0)
                tier_counts[t] += chance  # treat as one pick of that tier
        if sum(tier_counts.values()) <= 0:
            continue
        row = {"Character": cname}
        for tier in ["Magic","Rare","Epic","Legendary","Mythic"]:
            row[tier+" E[item/kill]"] = f"{tier_counts[tier]:.4f}"
        rows.append(row)
    return rows

def main():
    ap = argparse.ArgumentParser(description="Diff RelicHeim/EpicLoot material rates between baseline and active configs (v1.1).")
    ap.add_argument("--baseline", required=True, default="C:/Users/drumm/OneDrive/Desktop/Valheim_Testing/Valheim_Help_Docs/JewelHeim-RelicHeim-5.4.10_Backup/", help="Path to baseline (pristine) config dir (e.g., C:/Users/drumm/OneDrive/Desktop/Valheim_Testing/Valheim_Help_Docs/JewelHeim-RelicHeim-5.4.10_Backup/)")
    ap.add_argument("--active", required=True, default="C:/Users/drumm/OneDrive/Desktop/Valheim_Testing/Valheim/profiles/Dogeheim_Player/BepInEx/config/", help="Path to active repo/config dir")
    ap.add_argument("--out", required=True, help="Output path prefix (without extension)")
    ap.add_argument("--tier-map-json", help="Optional JSON file overriding tier regex mapping")
    ap.add_argument("--compose-characters", action="store_true", help="Compose per-character expected tier counts and emit a report")
    ap.add_argument("--include-path", action="append", default=[
        # Active configurations - Loot Tables & Drop Configurations
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChest.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop_list.zListDrops.cfg",
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_TreasureLoot_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_Equipment_RelicHeim.json",
        # Active configurations - Enchanting System Files
        "**/EpicLoot/patches/RelicHeimPatches/EnchantCost_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/MaterialConversion_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/EnchantingUpgrades_RelicHeim.json",
        # Active configurations - Adventure/Shop System Files
        "**/EpicLoot/patches/RelicHeimPatches/AdventureData_SecretStash_RelicHeim.json",
        # Active configurations - Backpack Configuration Files
        "**/Backpacks.MajesticEpicLoot.yml",
        # Active configurations - Item Database Files
        "**/VNEI-Export/VNEI.indexed.items.yml",
        "**/VNEI-Export/VNEI.indexed.items.txt",
        "**/VNEI-Export/VNEI.indexed.items.csv",
        # Active configurations - World Location Pickable Items
        "**/warpalicious.More_World_Locations_PickableItemLists.yml",
        # Canonical RelicHeim files - Backup Loot Tables & Drop Configurations
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChestbackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop_list.zListDropsbackup.cfg",
        "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_TreasureLoot_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_Equipment_RelicHeim.json",
        # Canonical RelicHeim files - Backup Enchanting System Files
        "**/EpicLootbackup/patches/RelicHeimPatches/EnchantCost_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/MaterialConversion_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/EnchantingUpgrades_RelicHeim.json",
        # Canonical RelicHeim files - Backup Adventure/Shop System Files
        "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_SecretStash_RelicHeim.json",
        # Canonical RelicHeim files - Backup Backpack Configuration Files
        "**/Backpacks.MajesticEpicLootbackup.yml",
        # Canonical RelicHeim files - Backup Item Database Files
        "**/wackysDatabase_backup/Items/_RelicHeimWDB2.0/zOther/Item_EssenceMagic.yml"
    ], help="Restrict parsing to these paths/globs (repeatable)")
    args = ap.parse_args()

    tier_map = DEFAULT_TIER_PATTERNS.copy()
    if args.tier_map_json:
        with open(args.tier_map_json, "r", encoding="utf-8") as f:
            m = json.load(f)
            for k,v in m.items():
                tier_map[k] = v

    base_sets = crawl_configs(args.baseline, args.include_path)
    act_sets  = crawl_configs(args.active, args.include_path)

    base_shares = compute_shares(base_sets, tier_map)
    act_shares  = compute_shares(act_sets, tier_map)

    common = sorted(set(base_shares.keys()) & set(act_shares.keys()))
    rows = []
    for name in common:
        b = base_sets[name]; a = act_sets[name]
        b_sh = base_shares[name]; a_sh = act_shares[name]
        row = {
            "Set": name,
            "Base Picks (est)": f"{b.expected_picks():.2f}" if b.expected_picks() is not None else "",
            "Active Picks (est)": f"{a.expected_picks():.2f}" if a.expected_picks() is not None else "",
        }
        for tier in ["Magic","Rare","Epic","Legendary","Mythic"]:
            row[f"Base {tier}"]   = percent(b_sh.get(tier, 0.0))
            row[f"Active {tier}"] = percent(a_sh.get(tier, 0.0))
            delta = a_sh.get(tier, 0.0) - b_sh.get(tier, 0.0)
            row[f"Δ {tier} (pp)"] = f"{delta*100:.2f}"
        rows.append(row)

    only_base = sorted(set(base_shares.keys()) - set(act_shares.keys()))
    only_act  = sorted(set(act_shares.keys()) - set(base_shares.keys()))

    out_csv = args.out + ".csv"
    out_html = args.out + ".html"
    write_csv(out_csv, rows)

    parts = []
    parts.append("<html><head><meta charset='utf-8'><title>Valheim Loot Diff</title></head><body>")
    parts.append("<h1>Valheim Loot Diff — Material Tier Shares (per pick)</h1>")
    parts.append("<p>This report compares per-pick tier shares for sets/tables found in both baseline and active configs. "
                 "Estimated picks per roll are shown when parseable (table chance × expected rolls).</p>")
    parts.append(render_html_table(rows, "Common Sets — Tier Share Diff"))
    if only_base:
        parts.append("<h2>Sets only in BASELINE</h2><ul>" + "".join(f"<li>{html.escape(s)}</li>" for s in only_base) + "</ul>")
    if only_act:
        parts.append("<h2>Sets only in ACTIVE</h2><ul>" + "".join(f"<li>{html.escape(s)}</li>" for s in only_act) + "</ul>")
    parts.append("</body></html>")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"Wrote: {out_csv}")
    print(f"Wrote: {out_html}")

    # Optional: character composition
    if args.compose-characters:
        base_chars = crawl_characters(args.baseline, args.include_path)
        act_chars  = crawl_characters(args.active, args.include_path)

        base_rows = compose_characters_report(base_chars, base_sets, tier_map)
        act_rows  = compose_characters_report(act_chars, act_sets, tier_map)
        write_csv(args.out + ".characters.base.csv", base_rows)
        write_csv(args.out + ".characters.active.csv", act_rows)
        print(f"Wrote: {args.out}.characters.base.csv")
        print(f"Wrote: {args.out}.characters.active.csv")

if __name__ == "__main__":
    main()
