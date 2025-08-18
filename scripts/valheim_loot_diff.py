#!/usr/bin/env python3
"""
valheim_loot_diff.py v1.2 — Compare baseline vs active Valheim loot material rates (RelicHeim/EpicLoot tiers).

What's new in v1.2 (relative to v1.1):
- Added GUI mode: --gui launches Tkinter interface
- Combined CLI and GUI into single script for easier maintenance

What's new in v1.1 (relative to v1.0):
- Added tier synonyms: "Essence", "Reagent".
- Ignores VNEI export folders by default to avoid noise.
- Heuristic support for EpicLoot patch JSONs (e.g., zLootables_TreasureLoot_RelicHeim.json, zLootables_Equipment_RelicHeim.json).
  - Walks nested dicts/lists for tables with drops and weights; accepts "Rarity" as explicit tier.
- Optional YAML (PyYAML) parsing for pickable item lists (e.g., warpalicious More_World_Locations *.yml).
- Optional per-character composition: --compose-characters produces a character-level expected tier report by combining CharacterDrop entries with referenced DropTables.

Usage (CLI mode):
    python valheim_loot_diff.py --baseline ./baseline_cfg --active ./ValheimMods/config --out ./loot_report

Usage (GUI mode):
    python valheim_loot_diff.py --gui

Extra options:
    --gui                     -> launch Tkinter GUI interface
    --compose-characters      -> emit loot_report.characters.csv (best-effort per-kill tier expectation)
    --include-path path       -> repeatable; if provided, only include files under these paths (globs ok)
    --scan-all                -> ignore default include filters and scan all supported config files
    --set-weight-json file    -> JSON { setName: weight } to weight set contributions for global aggregation
    --assert-tier-change expr -> assertion like "Magic:+10%" to verify global change vs baseline
"""

import argparse
import os
import re
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple, Optional, Any
import json
import html
from fnmatch import fnmatch
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

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

# Identify enchanting material item types specifically
ENCHANT_TYPE_PATTERN = re.compile(r"(?:essence|runestone|shard|dust|reagent)", re.IGNORECASE)

# GUI Color palette
PALETTE = {
    "bg_dark": "#260B01",
    "bg_mid": "#64563C", 
    "accent": "#8D5B2F",
    "muted": "#939789",
    "paper": "#DBD5CA",
    "sand": "#CBB89C",
}

# Keys we look for when parsing entries/tables
ITEM_KEYS     = {"item", "prefab", "prefabname", "name"}
# Include Drop That style keys (SetTemplateWeight, SetDropChance, etc.)
WEIGHT_KEYS   = {"weight", "setweight", "entryweight", "weightwhenrolled", "settemplateweight"}
CHANCE_KEYS   = {"chance", "dropchance", "probability", "rollchance", "setdropchance"}
SET_KEYS      = {"set", "setname", "droptable", "table", "group", "parent", "pool"}
COUNT_MIN_KEYS= {"min", "amountmin", "dropmin", "rollsmin", "setdropmin", "setamountmin"}
COUNT_MAX_KEYS= {"max", "amountmax", "dropmax", "rollsmax", "setdropmax", "setamountmax"}
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

    def expected_items_per_pick(self) -> float:
        """
        Expected number of successful item drops per pick of this table.
        Assumes one entry is selected per pick, proportionally to weight, and each
        selected entry then succeeds with its own chance. This returns the average
        success probability across a pick: sum_i (w_i/sum_j w_j) * chance_i.
        """
        total_weight = 0.0
        weighted_success = 0.0
        for e in self.entries:
            w = max(e.get("weight", 0.0), 0.0)
            c = max(min(e.get("chance", 1.0), 1.0), 0.0)
            total_weight += w
            weighted_success += w * c
        if total_weight <= 0.0:
            return 0.0
        return weighted_success / total_weight

    def expected_materials_per_pick_by_tier(self, tier_regex: Dict[str, str]) -> Dict[str, float]:
        """
        Expected number of enchanting material items produced per pick, split by tier.
        Only counts entries whose item name includes essence/runestone/shard/dust/reagent.
        For each entry i: P(select i) * chance_i, where P(select i) = weight_i / sum_j weight_j.
        """
        totals_by_tier: Dict[str, float] = {"Magic": 0.0, "Rare": 0.0, "Epic": 0.0, "Legendary": 0.0, "Mythic": 0.0}
        total_weight = 0.0
        for e in self.entries:
            total_weight += max(e.get("weight", 0.0), 0.0)
        if total_weight <= 0.0:
            return totals_by_tier
        for e in self.entries:
            item = e.get("item")
            if not item:
                continue
            if not ENCHANT_TYPE_PATTERN.search(str(item)):
                continue
            tier = e.get("tier") or tier_of(item, tier_regex)
            if not tier or tier not in totals_by_tier:
                continue
            w = max(e.get("weight", 0.0), 0.0)
            c = max(min(e.get("chance", 1.0), 1.0), 0.0)
            p_select = 0.0 if total_weight <= 0 else (w / total_weight)
            totals_by_tier[tier] += p_select * c
        return totals_by_tier

    def expected_materials_per_pick_by_item(self, tier_regex: Dict[str, str]) -> Dict[str, float]:
        """
        Expected number of enchanting material items produced per pick, keyed by exact item name.
        Only counts entries whose item name includes essence/runestone/shard/dust/reagent.
        """
        totals_by_item: Dict[str, float] = {}
        total_weight = 0.0
        for e in self.entries:
            total_weight += max(e.get("weight", 0.0), 0.0)
        if total_weight <= 0.0:
            return totals_by_item
        for e in self.entries:
            item = e.get("item")
            if not item:
                continue
            if not ENCHANT_TYPE_PATTERN.search(str(item)):
                continue
            w = max(e.get("weight", 0.0), 0.0)
            c = max(min(e.get("chance", 1.0), 1.0), 0.0)
            p_select = 0.0 if total_weight <= 0 else (w / total_weight)
            totals_by_item[item] = totals_by_item.get(item, 0.0) + p_select * c
        return totals_by_item

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

def compute_global_material_expectation(sets: Dict[str, LootSet], tier_regex: Dict[str,str], set_weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    Aggregate expected enchanting material drops by tier across all sets.
    Each set contributes: (expected_picks for the set) * (expected materials per pick by tier).
    """
    totals: Dict[str, float] = {"Magic": 0.0, "Rare": 0.0, "Epic": 0.0, "Legendary": 0.0, "Mythic": 0.0}
    for name, ls in sets.items():
        picks = ls.expected_picks() or 1.0
        if set_weights and name in set_weights:
            try:
                picks *= float(set_weights[name])
            except Exception:
                pass
        per_pick = ls.expected_materials_per_pick_by_tier(tier_regex)
        for t in totals.keys():
            totals[t] += picks * per_pick.get(t, 0.0)
    return totals

def compute_global_material_expectation_by_item(sets: Dict[str, LootSet], tier_regex: Dict[str,str], set_weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    Aggregate expected enchanting material drops by exact item across all sets.
    Each set contributes: (expected_picks for the set [weighted]) * (expected materials per pick by item).
    """
    totals: Dict[str, float] = {}
    for name, ls in sets.items():
        picks = ls.expected_picks() or 1.0
        if set_weights and name in set_weights:
            try:
                picks *= float(set_weights[name])
            except Exception:
                pass
        per_item = ls.expected_materials_per_pick_by_item(tier_regex)
        for item, val in per_item.items():
            totals[item] = totals.get(item, 0.0) + picks * val
    return totals

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
    # Average success probability per pick (0..1) for each set
    set_success_per_pick = {k: v.expected_items_per_pick() for k, v in set_map.items()}
    for cname, cd in sorted(char_map.items(), key=lambda x: x[0].lower()):
        tier_counts = defaultdict(float)
        # combine table refs
        for ref in cd.table_refs:
            sname = ref.get("set")
            if sname in set_share:
                picks = set_picks.get(sname, 1.0)
                success_rate = set_success_per_pick.get(sname, 0.0)
                chance = max(min(float(ref.get("chance",1.0)), 1.0), 0.0)
                # Expected number of successful items produced by this set ref
                mult = chance * picks * success_rate
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

class LootDiffGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Valheim Loot Diff")
        master.configure(bg=PALETTE["bg_dark"])

        # Main frame
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title
        ttk.Label(self.main_frame, text="Valheim Loot Diff", font=("Helvetica", 24, "bold"), foreground=PALETTE["paper"], background=PALETTE["bg_dark"]).pack(pady=10)

        # Input paths
        self.baseline_path = ttk.Entry(self.main_frame, width=50)
        self.baseline_path.pack(pady=5)
        ttk.Button(self.main_frame, text="Select Baseline", command=self.select_baseline).pack(pady=2)

        self.active_path = ttk.Entry(self.main_frame, width=50)
        self.active_path.pack(pady=5)
        ttk.Button(self.main_frame, text="Select Active", command=self.select_active).pack(pady=2)

        self.out_path = ttk.Entry(self.main_frame, width=50)
        self.out_path.pack(pady=5)
        ttk.Button(self.main_frame, text="Select Output", command=self.select_output).pack(pady=2)

        # Options
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Options", padding="5")
        self.options_frame.pack(pady=10, fill="x")

        self.compose_chars = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.options_frame, text="Compose per-character expected tier counts", variable=self.compose_chars).pack(pady=5)

        self.scan_all = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.options_frame, text="Scan all supported config files", variable=self.scan_all).pack(pady=5)

        self.tier_map_json = ttk.Entry(self.options_frame, width=50)
        self.tier_map_json.pack(pady=5)
        ttk.Button(self.options_frame, text="Select Tier Map JSON", command=self.select_tier_map_json).pack(pady=2)

        self.set_weight_json = ttk.Entry(self.options_frame, width=50)
        self.set_weight_json.pack(pady=5)
        ttk.Button(self.options_frame, text="Select Set Weight JSON", command=self.select_set_weight_json).pack(pady=2)

        self.assert_tier_change = ttk.Entry(self.options_frame, width=20)
        self.assert_tier_change.pack(pady=5)
        ttk.Label(self.options_frame, text="Assert global tier change (e.g., Magic:+10% or Magic:+0.10)").pack(pady=2)

        self.gui_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.options_frame, text="Run in GUI mode", variable=self.gui_mode).pack(pady=5)

        # Run button
        self.run_button = ttk.Button(self.main_frame, text="Run Diff", command=self.run_diff)
        self.run_button.pack(pady=20)

        # Status/Output area
        self.status_text = tk.Text(self.main_frame, state="disabled", bg=PALETTE["paper"], fg=PALETTE["bg_dark"])
        self.status_text.pack(pady=10, expand=True, fill="both")

        # GUI-specific attributes
        self.baseline_dir = ""
        self.active_dir = ""
        self.out_dir = ""
        self.tier_map_file = ""
        self.set_weight_file = ""
        self.include_paths = []
        self.tier_regex = DEFAULT_TIER_PATTERNS.copy()
        self.set_weights = {}
        self.char_map = {}
        self.set_map = {}
        self.base_shares = {}
        self.act_shares = {}
        self.global_base = {}
        self.global_act = {}
        self.item_base = {}
        self.item_act = {}

    def select_baseline(self):
        path = filedialog.askdirectory()
        if path:
            self.baseline_path.delete(0, tk.END)
            self.baseline_path.insert(0, path)
            self.baseline_dir = path

    def select_active(self):
        path = filedialog.askdirectory()
        if path:
            self.active_path.delete(0, tk.END)
            self.active_path.insert(0, path)
            self.active_dir = path

    def select_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
        if path:
            self.out_path.delete(0, tk.END)
            self.out_path.insert(0, path)
            self.out_dir = os.path.dirname(path)

    def select_tier_map_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if path:
            self.tier_map_json.delete(0, tk.END)
            self.tier_map_json.insert(0, path)
            self.tier_map_file = path
            self.load_tier_map()

    def select_set_weight_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if path:
            self.set_weight_json.delete(0, tk.END)
            self.set_weight_json.insert(0, path)
            self.set_weight_file = path
            self.load_set_weights()

    def load_tier_map(self):
        if self.tier_map_file:
            try:
                with open(self.tier_map_file, "r", encoding="utf-8") as f:
                    m = json.load(f)
                    for k,v in m.items():
                        self.tier_regex[k] = v
                    self.status_text.insert(tk.END, f"Loaded tier map from {self.tier_map_file}\n")
                    self.status_text.see(tk.END)
            except Exception as e:
                self.status_text.insert(tk.END, f"Error loading tier map from {self.tier_map_file}: {e}\n")
                self.status_text.see(tk.END)

    def load_set_weights(self):
        if self.set_weight_file:
            try:
                with open(self.set_weight_file, "r", encoding="utf-8") as f:
                    w = json.load(f)
                    if isinstance(w, dict):
                        self.set_weights = {str(k): float(v) for k, v in w.items()}
                    self.status_text.insert(tk.END, f"Loaded set weights from {self.set_weight_file}\n")
                    self.status_text.see(tk.END)
            except Exception as e:
                self.status_text.insert(tk.END, f"Error loading set weights from {self.set_weight_file}: {e}\n")
                self.status_text.see(tk.END)

    def run_diff(self):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Running Valheim Loot Diff...\n")
        self.status_text.see(tk.END)

        baseline_path = self.baseline_path.get()
        active_path = self.active_path.get()
        out_path = self.out_path.get()
        compose_chars = self.compose_chars.get()
        scan_all = self.scan_all.get()
        tier_map_json = self.tier_map_json.get()
        set_weight_json = self.set_weight_json.get()
        assert_tier_change = self.assert_tier_change.get()
        gui_mode = self.gui_mode.get()

        if not baseline_path:
            messagebox.showerror("Error", "Please select a baseline directory.")
            return
        if not active_path:
            messagebox.showerror("Error", "Please select an active directory.")
            return
        if not out_path:
            messagebox.showerror("Error", "Please select an output path.")
            return

        if not gui_mode:
            self.status_text.insert(tk.END, "Running in CLI mode...\n")
            self.status_text.see(tk.END)
            self.include_paths = [] if scan_all else self.get_include_paths()
            self.set_map = crawl_configs(baseline_path, self.include_paths)
            self.char_map = crawl_characters(baseline_path, self.include_paths)
            self.base_shares = compute_shares(self.set_map, self.tier_regex)
            self.act_shares = compute_shares(crawl_configs(active_path, self.include_paths), self.tier_regex)
            self.global_base = compute_global_material_expectation(self.set_map, self.tier_regex, self.set_weights)
            self.global_act = compute_global_material_expectation(crawl_configs(active_path, self.include_paths), self.tier_regex, self.set_weights)
            self.item_base = compute_global_material_expectation_by_item(self.set_map, self.tier_regex, self.set_weights)
            self.item_act = compute_global_material_expectation_by_item(crawl_configs(active_path, self.include_paths), self.tier_regex, self.set_weights)

            self.write_reports(out_path, compose_chars)
            self.assert_global_change(assert_tier_change)
        else:
            self.status_text.insert(tk.END, "Running in GUI mode...\n")
            self.status_text.see(tk.END)
            self.gui_thread = threading.Thread(target=self.run_diff_gui_thread, args=(baseline_path, active_path, out_path, compose_chars, scan_all, tier_map_json, set_weight_json, assert_tier_change, gui_mode))
            self.gui_thread.start()

    def run_diff_gui_thread(self, baseline_path, active_path, out_path, compose_chars, scan_all, tier_map_json, set_weight_json, assert_tier_change, gui_mode):
        self.master.withdraw() # Hide main window
        try:
            self.include_paths = [] if scan_all else self.get_include_paths()
            self.set_map = crawl_configs(baseline_path, self.include_paths)
            self.char_map = crawl_characters(baseline_path, self.include_paths)
            self.base_shares = compute_shares(self.set_map, self.tier_regex)
            self.act_shares = compute_shares(crawl_configs(active_path, self.include_paths), self.tier_regex)
            self.global_base = compute_global_material_expectation(self.set_map, self.tier_regex, self.set_weights)
            self.global_act = compute_global_material_expectation(crawl_configs(active_path, self.include_paths), self.tier_regex, self.set_weights)
            self.item_base = compute_global_material_expectation_by_item(self.set_map, self.tier_regex, self.set_weights)
            self.item_act = compute_global_material_expectation_by_item(crawl_configs(active_path, self.include_paths), self.tier_regex, self.set_weights)

            self.write_reports(out_path, compose_chars)
            self.assert_global_change(assert_tier_change)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during the diff process: {e}")
        finally:
            self.master.deiconify() # Show main window

    def get_include_paths(self) -> List[str]:
        paths = []
        for p in self.include_paths:
            if p:
                paths.append(p)
        return paths

    def write_reports(self, out_path: str, compose_chars: bool):
        self.status_text.insert(tk.END, "Writing reports...\n")
        self.status_text.see(tk.END)

        out_csv = out_path + ".csv"
        out_html = out_path + ".html"
        self.write_csv_report(out_csv, self.get_common_sets_rows())
        self.write_html_report(out_html, compose_chars)

        global_csv = out_path + ".materials.global.csv"
        self.write_csv_report(global_csv, self.get_global_material_rows())

        if compose_chars:
            base_chars_csv = out_path + ".characters.base.csv"
            act_chars_csv = out_path + ".characters.active.csv"
            self.write_csv_report(base_chars_csv, compose_characters_report(self.char_map, self.set_map, self.tier_regex))
            self.write_csv_report(act_chars_csv, compose_characters_report(crawl_characters(self.active_path.get(), self.include_paths), self.set_map, self.tier_regex))
            self.status_text.insert(tk.END, "Wrote character reports.\n")
            self.status_text.see(tk.END)

        item_csv = out_path + ".materials.items.csv"
        self.write_csv_report(item_csv, self.get_item_material_rows())

    def write_csv_report(self, path: str, rows: List[Dict[str, str]]):
        if not rows:
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)

    def write_html_report(self, path: str, compose_chars: bool):
        parts = []
        parts.append("<html><head><meta charset='utf-8'><title>Valheim Loot Diff</title></head><body>")
        parts.append("<h1>Valheim Loot Diff — Material Tier Shares (per pick)</h1>")
        parts.append("<p>This report compares per-pick tier shares for sets/tables found in both baseline and active configs. "
                     "Estimated picks per roll are shown when parseable (table chance × expected rolls).</p>")
        parts.append(render_html_table(self.get_common_sets_rows(), "Common Sets — Tier Share Diff"))
        # Global expected enchanting materials by tier
        parts.append(render_html_table(self.get_global_material_rows(), "Global Expected Enchanting Materials by Tier (per run)"))
        # Also write CSV for global materials
        global_csv = self.out_path.get() + ".materials.global.csv"
        self.write_csv_report(global_csv, self.get_global_material_rows())

        if compose_chars:
            base_chars_csv = self.out_path.get() + ".characters.base.csv"
            act_chars_csv = self.out_path.get() + ".characters.active.csv"
            self.write_csv_report(base_chars_csv, compose_characters_report(self.char_map, self.set_map, self.tier_regex))
            self.write_csv_report(act_chars_csv, compose_characters_report(crawl_characters(self.active_path.get(), self.include_paths), self.set_map, self.tier_regex))
            parts.append("<h2>Character Composition Reports</h2>")
            parts.append(f"<p>Wrote character reports to {base_chars_csv} and {act_chars_csv}</p>")

        parts.append(render_html_table(self.get_item_material_rows(), "Global Expected Enchanting Materials — Per Item"))
        parts.append("</body></html>")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(parts))
        self.status_text.insert(tk.END, f"Wrote HTML report to {path}\n")
        self.status_text.see(tk.END)

    def get_common_sets_rows(self) -> List[Dict[str, str]]:
        common = sorted(set(self.base_shares.keys()) & set(self.act_shares.keys()))
        rows = []
        for name in common:
            b = self.set_map[name]; a = self.act_sets[name] # Use self.act_sets here
            b_sh = self.base_shares[name]; a_sh = self.act_shares[name]
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
        return rows

    def get_global_material_rows(self) -> List[Dict[str, str]]:
        tiers = ["Magic","Rare","Epic","Legendary","Mythic"]
        global_rows: List[Dict[str, str]] = []
        for t in tiers:
            b = self.global_base.get(t, 0.0)
            a = self.global_act.get(t, 0.0)
            d = a - b
            pct = (d / b * 100.0) if b > 0 else (100.0 if a > 0 else 0.0)
            global_rows.append({
                "Tier": t,
                "Base E[item]": f"{b:.6f}",
                "Active E[item]": f"{a:.6f}",
                "Δ E[item]": f"{d:.6f}",
                "Δ %": f"{pct:.2f}"
            })
        # Totals row
        total_b = sum(self.global_base.values())
        total_a = sum(self.global_act.values())
        total_d = total_a - total_b
        total_pct = (total_d / total_b * 100.0) if total_b > 0 else (100.0 if total_a > 0 else 0.0)
        global_rows.append({
            "Tier": "Total",
            "Base E[item]": f"{total_b:.6f}",
            "Active E[item]": f"{total_a:.6f}",
            "Δ E[item]": f"{total_d:.6f}",
            "Δ %": f"{total_pct:.2f}"
        })
        return global_rows

    def get_item_material_rows(self) -> List[Dict[str, str]]:
        # Build rows grouped by tier then item
        item_rows: List[Dict[str, str]] = []
        def item_tier(name: str) -> str:
            t = tier_of(name, self.tier_regex) or ""
            return t
        items_all = sorted(set(self.item_base.keys()) | set(self.item_act.keys()), key=lambda s: (item_tier(s), s.lower()))
        for item in items_all:
            b = self.item_base.get(item, 0.0)
            a = self.item_act.get(item, 0.0)
            d = a - b
            pct = (d / b * 100.0) if b > 0 else (100.0 if a > 0 else 0.0)
            item_rows.append({
                "Tier": item_tier(item),
                "Item": item,
                "Base E[item]": f"{b:.6f}",
                "Active E[item]": f"{a:.6f}",
                "Δ E[item]": f"{d:.6f}",
                "Δ %": f"{pct:.2f}"
            })
        return item_rows

    def assert_global_change(self, expr: str):
        if not expr:
            return
        m = re.match(r"^([A-Za-z]+):([+\-]?[0-9.]+%?)$", expr.strip())
        if m:
            tier = m.group(1).capitalize()
            inc = m.group(2)
            target_ratio = None
            if inc.endswith('%'):
                try:
                    pct = float(inc.strip('%'))/100.0
                    target_ratio = 1.0 + pct
                except Exception:
                    target_ratio = None
            else:
                try:
                    frac = float(inc)
                    if abs(frac) < 2.0:
                        target_ratio = 1.0 + frac
                    else:
                        # treat absolute factor
                        target_ratio = frac
                except Exception:
                    target_ratio = None
            if target_ratio is not None and tier in self.global_base and tier in self.global_act:
                b = self.global_base.get(tier, 0.0)
                a = self.global_act.get(tier, 0.0)
                achieved = (a / b) if b > 0 else (float('inf') if a > 0 else 1.0)
                print(f"Assert {tier} change: baseline={b:.6f}, active={a:.6f}, ratio={achieved:.4f}, target={target_ratio:.4f}")
                # Simple tolerance
                tol = 0.02
                if not (abs(achieved - target_ratio) <= tol * max(target_ratio, 1.0)):
                    messagebox.showwarning("Warning", f"Global tier change deviates beyond tolerance for {tier}.")
            else:
                messagebox.showwarning("Warning", f"Tier '{tier}' not found in global reports or not parseable.")
        else:
            messagebox.showwarning("Warning", f"Assertion '{expr}' is not in the correct format (e.g., Magic:+10% or Magic:+0.10).")

def main():
    ap = argparse.ArgumentParser(description="Diff RelicHeim/EpicLoot material rates between baseline and active configs (v1.2).")
    # Default paths are relative to this repository so the script works out-of-the-box
    ap.add_argument("--baseline", required=False, default="Valheim_Help_Docs/JewelHeim-RelicHeim-5.4.10_Backup/", help="Path to baseline (pristine) config dir")
    ap.add_argument("--active", required=False, default="Valheim/profiles/Dogeheim_Player/BepInEx/config/", help="Path to active repo/config dir")
    ap.add_argument("--out", required=False, default="./loot_report", help="Output path prefix (without extension)")
    ap.add_argument("--tier-map-json", help="Optional JSON file overriding tier regex mapping")
    ap.add_argument("--set-weight-json", help="Optional JSON { setName: weight } to weight/scale set contributions for global aggregation")
    ap.add_argument("--assert-tier-change", help="Optional assertion of form Tier:+10%% or Tier:+0.10 to verify global change vs baseline")
    ap.add_argument("--gui", action="store_true", help="Launch Tkinter GUI interface")
    ap.add_argument("--compose-characters", action="store_true", help="Compose per-character expected tier counts and emit a report")
    ap.add_argument("--scan-all", action="store_true", help="Ignore default include filters and scan all supported config files under baseline/active")
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

    if args.gui:
        launch_gui()
        return

    # CLI mode - existing logic
    tier_map = DEFAULT_TIER_PATTERNS.copy()
    if args.tier_map_json:
        with open(args.tier_map_json, "r", encoding="utf-8") as f:
            m = json.load(f)
            for k,v in m.items():
                tier_map[k] = v
    set_weights = None
    if args.set_weight_json:
        try:
            with open(args.set_weight_json, "r", encoding="utf-8") as f:
                w = json.load(f)
                if isinstance(w, dict):
                    set_weights = {str(k): float(v) for k, v in w.items()}
        except Exception:
            set_weights = None

    include_filters = [] if args.scan_all else args.include_path
    base_sets = crawl_configs(args.baseline, include_filters)
    act_sets  = crawl_configs(args.active, include_filters)

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
    # Global expected enchanting materials by tier
    base_global = compute_global_material_expectation(base_sets, tier_map, set_weights)
    act_global  = compute_global_material_expectation(act_sets, tier_map, set_weights)
    tiers = ["Magic","Rare","Epic","Legendary","Mythic"]
    global_rows: List[Dict[str, str]] = []
    for t in tiers:
        b = base_global.get(t, 0.0)
        a = act_global.get(t, 0.0)
        d = a - b
        pct = (d / b * 100.0) if b > 0 else (100.0 if a > 0 else 0.0)
        global_rows.append({
            "Tier": t,
            "Base E[item]": f"{b:.6f}",
            "Active E[item]": f"{a:.6f}",
            "Δ E[item]": f"{d:.6f}",
            "Δ %": f"{pct:.2f}"
        })
    # Totals row
    total_b = sum(base_global.values())
    total_a = sum(act_global.values())
    total_d = total_a - total_b
    total_pct = (total_d / total_b * 100.0) if total_b > 0 else (100.0 if total_a > 0 else 0.0)
    global_rows.append({
        "Tier": "Total",
        "Base E[item]": f"{total_b:.6f}",
        "Active E[item]": f"{total_a:.6f}",
        "Δ E[item]": f"{total_d:.6f}",
        "Δ %": f"{total_pct:.2f}"
    })
    parts.append(render_html_table(global_rows, "Global Expected Enchanting Materials by Tier (per run)"))
    # Also write CSV for global materials
    global_csv = args.out + ".materials.global.csv"
    write_csv(global_csv, global_rows)

    # Optional assertion check for a tier change like Magic:+10% or Magic:+0.10
    if args.assert_tier_change:
        m = re.match(r"^([A-Za-z]+):([+\-]?[0-9.]+%?)$", args.assert_tier_change.strip())
        if m:
            tier = m.group(1).capitalize()
            inc = m.group(2)
            target_ratio = None
            if inc.endswith('%'):
                try:
                    pct = float(inc.strip('%'))/100.0
                    target_ratio = 1.0 + pct
                except Exception:
                    target_ratio = None
            else:
                try:
                    frac = float(inc)
                    if abs(frac) < 2.0:
                        target_ratio = 1.0 + frac
                    else:
                        # treat absolute factor
                        target_ratio = frac
                except Exception:
                    target_ratio = None
            if target_ratio is not None and tier in base_global and tier in act_global:
                b = base_global.get(tier, 0.0)
                a = act_global.get(tier, 0.0)
                achieved = (a / b) if b > 0 else (float('inf') if a > 0 else 1.0)
                print(f"Assert {tier} change: baseline={b:.6f}, active={a:.6f}, ratio={achieved:.4f}, target={target_ratio:.4f}")
                # Simple tolerance
                tol = 0.02
                if not (abs(achieved - target_ratio) <= tol * max(target_ratio, 1.0)):
                    print("WARNING: Global tier change deviates beyond tolerance.")
            else:
                print(f"WARNING: Assertion '{args.assert_tier_change}' is not in the correct format (e.g., Magic:+10% or Magic:+0.10).")
    if only_base:
        parts.append("<h2>Sets only in BASELINE</h2><ul>" + "".join(f"<li>{html.escape(s)}</li>" for s in only_base) + "</ul>")
    if only_act:
        parts.append("<h2>Sets only in ACTIVE</h2><ul>" + "".join(f"<li>{html.escape(s)}</li>" for s in only_act) + "</ul>")
    parts.append("</body></html>")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"Wrote: {out_csv}")
    print(f"Wrote: {out_html}")
    print(f"Wrote: {global_csv}")

    # Optional: character composition
    if args.compose_characters:
        base_chars = crawl_characters(args.baseline, include_filters)
        act_chars  = crawl_characters(args.active, include_filters)

        base_rows = compose_characters_report(base_chars, base_sets, tier_map)
        act_rows  = compose_characters_report(act_chars, act_sets, tier_map)
        write_csv(args.out + ".characters.base.csv", base_rows)
        write_csv(args.out + ".characters.active.csv", act_rows)
        print(f"Wrote: {args.out}.characters.base.csv")
        print(f"Wrote: {args.out}.characters.active.csv")

    # Per-item global report
    base_items = compute_global_material_expectation_by_item(base_sets, tier_map, set_weights)
    act_items  = compute_global_material_expectation_by_item(act_sets, tier_map, set_weights)
    # Build rows grouped by tier then item
    item_rows: List[Dict[str, str]] = []
    def item_tier(name: str) -> str:
        t = tier_of(name, tier_map) or ""
        return t
    items_all = sorted(set(base_items.keys()) | set(act_items.keys()), key=lambda s: (item_tier(s), s.lower()))
    for item in items_all:
        b = base_items.get(item, 0.0)
        a = act_items.get(item, 0.0)
        d = a - b
        pct = (d / b * 100.0) if b > 0 else (100.0 if a > 0 else 0.0)
        item_rows.append({
            "Tier": item_tier(item),
            "Item": item,
            "Base E[item]": f"{b:.6f}",
            "Active E[item]": f"{a:.6f}",
            "Δ E[item]": f"{d:.6f}",
            "Δ %": f"{pct:.2f}"
        })
    write_csv(args.out + ".materials.items.csv", item_rows)
    # Add to HTML
    parts = []
    with open(out_html, "r", encoding="utf-8") as f:
        parts = f.read().splitlines()
    # remove closing tags
    if parts and parts[-1].strip().lower() == "</html>":
        parts.pop()
    if parts and parts[-1].strip().lower() == "</body>":
        parts.pop()
    parts.append(render_html_table(item_rows, "Global Expected Enchanting Materials — Per Item"))
    parts.append("</body></html>")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Wrote: {args.out}.materials.items.csv")


def launch_gui():
    """Launch the Tkinter GUI interface"""
    root = tk.Tk()
    root.title("Valheim Loot Diff — Enchanting Materials")
    root.configure(bg=PALETTE["bg_dark"])
    root.geometry("1200x800")

    # State variables
    baseline_var = tk.StringVar(value=os.path.normpath("Valheim_Help_Docs/JewelHeim-RelicHeim-5.4.10_Backup/"))
    active_var = tk.StringVar(value=os.path.normpath("Valheim/profiles/Dogeheim_Player/BepInEx/config/"))
    out_var = tk.StringVar(value="./loot_report")
    scan_all_var = tk.BooleanVar(value=False)
    compose_chars_var = tk.BooleanVar(value=False)
    weights_path_var = tk.StringVar(value="")
    assert_var = tk.StringVar(value="")

    def browse_directory(var):
        d = filedialog.askdirectory()
        if d:
            var.set(d)

    def browse_json_file(var):
        p = filedialog.askopenfilename(filetypes=[["JSON files", "*.json"], ["All files", "*.*"]])
        if p:
            var.set(p)

    def browse_save_prefix(var):
        p = filedialog.asksaveasfilename(defaultextension=".csv",
                                         filetypes=[["CSV files", "*.csv"], ["All files", "*.*"]])
        if p:
            if p.lower().endswith(".csv"):
                p = p[:-4]
            var.set(p)

    def run_analysis():
        try:
            # Validate paths
            baseline = baseline_var.get().strip()
            active = active_var.get().strip()
            out_path = out_var.get().strip()
            
            if not os.path.isdir(baseline):
                messagebox.showerror("Error", f"Baseline directory does not exist:\n{baseline}")
                return
            if not os.path.isdir(active):
                messagebox.showerror("Error", f"Active directory does not exist:\n{active}")
                return

            # Build command line args
            cmd_args = [
                "--baseline", baseline,
                "--active", active,
                "--out", out_path
            ]
            
            if scan_all_var.get():
                cmd_args.append("--scan-all")
            if compose_chars_var.get():
                cmd_args.append("--compose-characters")
            if weights_path_var.get().strip():
                cmd_args.extend(["--set-weight-json", weights_path_var.get().strip()])
            if assert_var.get().strip():
                cmd_args.extend(["--assert-tier-change", assert_var.get().strip()])

            # Run the analysis
            import sys
            sys.argv = [sys.argv[0]] + cmd_args
            main()
            
            messagebox.showinfo("Success", f"Analysis complete!\nOutput written to:\n{out_path}.csv\n{out_path}.html\n{out_path}.materials.global.csv\n{out_path}.materials.items.csv")
            
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    # Build GUI
    frm = tk.Frame(root, bg=PALETTE["bg_mid"], bd=0, highlightthickness=0)
    frm.pack(fill=tk.X, padx=12, pady=12)

    def row(parent, label, var, browse_fn):
        r = tk.Frame(parent, bg=PALETTE["bg_mid"])
        tk.Label(r, text=label, fg=PALETTE["paper"], bg=PALETTE["bg_mid"]).pack(side=tk.LEFT, padx=(0,6))
        e = tk.Entry(r, textvariable=var, width=80)
        e.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(r, text="Browse", command=lambda: browse_fn(var)).pack(side=tk.LEFT, padx=6)
        r.pack(fill=tk.X, pady=4)

    row(frm, "Baseline dir:", baseline_var, browse_directory)
    row(frm, "Active dir:", active_var, browse_directory)
    row(frm, "Output prefix:", out_var, browse_save_prefix)

    opts = tk.Frame(frm, bg=PALETTE["bg_mid"]) 
    tk.Checkbutton(opts, text="Scan all files", variable=scan_all_var, fg=PALETTE["paper"], bg=PALETTE["bg_mid"], selectcolor=PALETTE["bg_mid"]).pack(side=tk.LEFT)
    tk.Checkbutton(opts, text="Compose characters", variable=compose_chars_var, fg=PALETTE["paper"], bg=PALETTE["bg_mid"], selectcolor=PALETTE["bg_mid"]).pack(side=tk.LEFT)
    opts.pack(fill=tk.X, pady=4)

    row(frm, "Set weights JSON (optional):", weights_path_var, browse_json_file)

    ar = tk.Frame(frm, bg=PALETTE["bg_mid"]) 
    tk.Label(ar, text="Assert tier change (e.g., Magic:+10%):", fg=PALETTE["paper"], bg=PALETTE["bg_mid"]).pack(side=tk.LEFT)
    tk.Entry(ar, textvariable=assert_var, width=20).pack(side=tk.LEFT, padx=6)
    tk.Button(ar, text="Run Analysis", command=run_analysis, bg=PALETTE["accent"], fg="white", activebackground=PALETTE["accent"]).pack(side=tk.RIGHT)
    ar.pack(fill=tk.X, pady=(6,0))

    root.mainloop()

if __name__ == "__main__":
    main()
