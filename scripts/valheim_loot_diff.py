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
import csv
import threading
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

# GUI Color palette - User preferred colors
PALETTE = {
    "bg_dark": "#260B01",    # Dark brown/black
    "bg_mid": "#64563C",     # Medium brown
    "accent": "#8D5B2F",     # Rich brown
    "muted": "#939789",      # Muted green-gray
    "paper": "#DBD5CA",      # Light cream
    "sand": "#CBB89C",       # Sand color
}

# Keys we look for when parsing entries/tables
ITEM_KEYS     = {"item", "prefab", "prefabname", "name"}
# Include Drop That style keys (SetTemplateWeight, SetDropChance, etc.)
WEIGHT_KEYS   = {"weight", "setweight", "entryweight", "weightwhenrolled", "settemplateweight"}
# Include more Drop-That style chance keys found in configs (ChanceToDrop, SetChanceToDrop)
CHANCE_KEYS   = {"chance", "dropchance", "probability", "rollchance", "setdropchance", "chancetodrop", "setchancetodrop"}
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
        self.direct: List[Dict[str, Any]] = []  # {"item": str, "chance": float, "weight": float, "min": int|None, "max": int|None}

def parse_characters_from_text(text: str, file: str) -> Tuple[Dict[str, CharacterDrops], Dict[str, float]]:
    sections = scan_sections_ini_like(text, file)
    chars: Dict[str, CharacterDrops] = {}
    refs: Dict[str, float] = {}

    NON_CHAR_GROUPS = {"GlobalDrops", "AdjustedForSpawners"}

    for sec in sections:
        fields = sec.fields

        # Skip table-only metadata sections
        if guess_is_table(sec) and not guess_is_entry(sec):
            continue

        cname: Optional[str] = None
        m = re.match(r"(?i)^characterdrop\.([^.\]]+)", sec.name)
        if m:
            cname = m.group(1)
        else:
            m2 = re.match(r"^([A-Za-z0-9_]+)\.(?:[0-9]+).*", sec.name)
            if m2:
                group = m2.group(1)
                if group in NON_CHAR_GROUPS:
                    cname = "__GLOBAL__"
                else:
                    cname = group

        if not cname:
            continue

        cond_states = fields.get("ConditionCreatureStates") or fields.get("conditioncreaturestates") or ""
        if cname == "__GLOBAL__" and ("Event" in cond_states or "event" in cond_states.lower()):
            # Skip event-only globals for per-kill estimates
            continue

        cd = chars.setdefault(cname, CharacterDrops(cname))

        setname = extract_set(fields)
        ch = extract_chance(fields)
        mn, mx = extract_minmax(fields)
        oneof = find_oneof(fields)
        item = extract_item_name(fields)
        weight = extract_weight(fields)

        if setname:
            cd.table_refs.append({"set": setname, "chance": ch, "min": mn, "max": mx, "oneof": oneof, "weight": weight})
            refs[setname] = refs.get(setname, 0.0) + (weight if weight is not None else 1.0)
        elif item:
            cd.direct.append({"item": item, "chance": ch, "weight": weight, "min": mn, "max": mx})
    return chars, refs

def crawl_characters(root: str, include_paths: List[str]) -> Tuple[Dict[str, CharacterDrops], Dict[str, float]]:
    out: Dict[str, CharacterDrops] = {}
    refs: Dict[str, float] = {}
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
            chars, set_refs = parse_characters_from_text(txt, p)
            for k, v in chars.items():
                dst = out.setdefault(k, CharacterDrops(k))
                dst.table_refs.extend(v.table_refs)
                dst.direct.extend(v.direct)
            for k, v in set_refs.items():
                refs[k] = refs.get(k, 0.0) + v
    return out, refs

# -------------------------------
# Diff & reporting
# -------------------------------

def compute_shares(sets: Dict[str, LootSet], tier_regex: Dict[str,str]) -> Dict[str, Dict[str, float]]:
    out = {}
    for name, ls in sets.items():
        out[name] = summarize_set_by_tier(ls, tier_regex)
    return out

def compute_global_material_expectation(
    sets: Dict[str, LootSet],
    tier_regex: Dict[str, str],
    set_weights: Optional[Dict[str, float]] = None,
    character_weights: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """
    Aggregate expected enchanting material drops by tier across all sets.
    Each set contributes: (expected_picks for the set) * (expected materials per pick by tier).
    If ``character_weights`` is provided, each set's contribution is multiplied by the
    number of times it is referenced by characters (or their spawn weights).
    """
    totals: Dict[str, float] = {"Magic": 0.0, "Rare": 0.0, "Epic": 0.0, "Legendary": 0.0, "Mythic": 0.0}
    for name, ls in sets.items():
        picks = ls.expected_picks() or 1.0
        if set_weights and name in set_weights:
            try:
                picks *= float(set_weights[name])
            except Exception:
                pass
        elif character_weights and name in character_weights:
            try:
                picks *= float(character_weights[name])
            except Exception:
                pass
        per_pick = ls.expected_materials_per_pick_by_tier(tier_regex)
        for t in totals.keys():
            totals[t] += picks * per_pick.get(t, 0.0)
    return totals

def compute_global_material_expectation_by_item(
    sets: Dict[str, LootSet],
    tier_regex: Dict[str, str],
    set_weights: Optional[Dict[str, float]] = None,
    character_weights: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """
    Aggregate expected enchanting material drops by exact item across all sets.
    Each set contributes: (expected_picks for the set [weighted]) * (expected materials per pick by item).
    If ``character_weights`` is provided, each set's contribution is multiplied by the
    number of times it is referenced by characters (or their spawn weights).
    """
    totals: Dict[str, float] = {}
    for name, ls in sets.items():
        picks = ls.expected_picks() or 1.0
        if set_weights and name in set_weights:
            try:
                picks *= float(set_weights[name])
            except Exception:
                pass
        elif character_weights and name in character_weights:
            try:
                picks *= float(character_weights[name])
            except Exception:
                pass
        per_item = ls.expected_materials_per_pick_by_item(tier_regex)
        for item, val in per_item.items():
            totals[item] = totals.get(item, 0.0) + picks * val
    return totals

def write_csv(path: str, rows: List[Dict[str, str]]):
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

def compose_characters_report(
    char_map: Dict[str, CharacterDrops],
    set_map: Dict[str, LootSet],
    tier_regex: Dict[str,str],
    *,
    star_multiplier_creature: float = 1.0,
    star_multiplier_boss: float = 1.0,
) -> List[Dict[str,str]]:
    rows = []
    # Precompute per-pick tier share for sets
    set_share = {k: summarize_set_by_tier(v, tier_regex) for k, v in set_map.items()}
    set_picks = {k: v.expected_picks() or 1.0 for k, v in set_map.items()}
    # Average success probability per pick (0..1) for each set
    set_success_per_pick = {k: v.expected_items_per_pick() for k, v in set_map.items()}

    # Extract global drops, if present
    global_cd = char_map.get("__GLOBAL__")

    KNOWN_BOSSES = {"Eikthyr", "gd_king", "Bonemass", "Dragon", "GoblinKing", "SeekerQueen", "Fader",
                    "BossAsmodeus_TW", "BossSvalt_TW", "BossVrykolathas_TW", "BossStormHerald_TW", "BossGorr_TW"}

    for cname, cd in sorted(char_map.items(), key=lambda x: x[0].lower()):
        if cname == "__GLOBAL__":
            continue
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
        # direct items (respect amount min/max)
        for e in cd.direct:
            t = tier_of(e.get("item"), tier_regex)
            if t:
                chance = max(min(float(e.get("chance",1.0)), 1.0), 0.0)
                mn = e.get("min"); mx = e.get("max")
                amt = 1.0
                if isinstance(mn, int) or isinstance(mx, int):
                    lo = int(mn) if isinstance(mn, int) else int(mx)
                    hi = int(mx) if isinstance(mx, int) else int(mn)
                    if hi < lo:
                        lo, hi = hi, lo
                    amt = (lo + hi) / 2.0
                tier_counts[t] += chance * amt

        # Add global drops (non-event) to every character
        if global_cd is not None:
            for e in global_cd.direct:
                t = tier_of(e.get("item"), tier_regex)
                if not t:
                    continue
                chance = max(min(float(e.get("chance",1.0)), 1.0), 0.0)
                mn = e.get("min"); mx = e.get("max")
                amt = 1.0
                if isinstance(mn, int) or isinstance(mx, int):
                    lo = int(mn) if isinstance(mn, int) else int(mx)
                    hi = int(mx) if isinstance(mx, int) else int(mn)
                    if hi < lo:
                        lo, hi = hi, lo
                    amt = (lo + hi) / 2.0
                tier_counts[t] += chance * amt

        # Apply star-based additional loot multipliers approximations from CLLC
        is_boss = (cname in KNOWN_BOSSES) or cname.lower().startswith("boss")
        star_mult = star_multiplier_boss if is_boss else star_multiplier_creature
        for tier in list(tier_counts.keys()):
            tier_counts[tier] *= star_mult

        if sum(tier_counts.values()) <= 0:
            continue
        row = {"Character": cname}
        for tier in ["Magic","Rare","Epic","Legendary","Mythic"]:
            row[tier+" E[item/kill]"] = f"{tier_counts[tier]:.4f}"
        rows.append(row)
    return rows

def _parse_percent_list(val: str) -> List[float]:
    try:
        parts = [p.strip() for p in val.split(',') if p.strip()]
        nums = [float(p) for p in parts]
        return nums
    except Exception:
        return []

def _compute_expected_stars_from_distribution(dist_percent: List[float]) -> float:
    # dist_percent corresponds to [p1, p2, ..., pk] in percent; p0 is remainder
    total = sum(dist_percent)
    if total > 100.0:
        # normalize down
        dist = [p * (100.0/total) for p in dist_percent]
        total = 100.0
    else:
        dist = dist_percent[:]
    # expected stars: sum s * p_s
    exp = 0.0
    for i, p in enumerate(dist, start=1):
        exp += i * (p/100.0)
    return exp

def parse_cllc_star_multipliers(root_dir: str, world_level: int) -> Tuple[float, float]:
    cfg_path = None
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fn in filenames:
            low = fn.lower()
            if low.startswith("org.bepinex.plugins.creaturelevelcontrol") and low.endswith(".cfg"):
                cfg_path = os.path.join(dirpath, fn)
                break
        if cfg_path:
            break
    if not cfg_path:
        return 1.0, 1.0

    txt = read_text(cfg_path)
    lines = txt.splitlines()

    # Defaults
    creature_extra_chance = 1.0  # 100%
    boss_extra_chance = 0.5      # 50%
    use_creature_for_boss = False
    boss_star_line = ""
    wl_line = ""

    # Find settings
    for ln in lines:
        s = ln.strip()
        if s.lower().startswith("chance for additional loot per star for creatures"):
            m = re.search(r"=\s*([0-9.]+)", s)
            if m:
                creature_extra_chance = max(min(float(m.group(1))/100.0, 1.0), 0.0)
        elif s.lower().startswith("chance for additional loot per star for bosses"):
            m = re.search(r"=\s*([0-9.]+)", s)
            if m:
                boss_extra_chance = max(min(float(m.group(1))/100.0, 1.0), 0.0)
        elif s.lower().startswith("use creature level chances for bosses"):
            use_creature_for_boss = ("on" in s.lower())
        elif s.lower().startswith("star chances for bosses"):
            boss_star_line = s
        elif s.lower().startswith(f"chances for stars at world level {world_level} "):
            wl_line = s

    # Creature expected stars from world level distribution
    exp_stars_creature = 0.0
    if wl_line:
        m = re.search(r"=\s*(.+)$", wl_line)
        if m:
            lst = _parse_percent_list(m.group(1))
            exp_stars_creature = _compute_expected_stars_from_distribution(lst)

    # Boss expected stars
    exp_stars_boss = exp_stars_creature
    if not use_creature_for_boss and boss_star_line:
        m2 = re.search(r"=\s*(.+)$", boss_star_line)
        if m2:
            lstb = _parse_percent_list(m2.group(1))
            exp_stars_boss = _compute_expected_stars_from_distribution(lstb)

    # Multipliers: 1 + P(extra per star) * E[stars]
    mult_creature = 1.0 + creature_extra_chance * exp_stars_creature
    mult_boss = 1.0 + boss_extra_chance * exp_stars_boss
    return mult_creature, mult_boss

class LootDiffGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Valheim Loot Diff")
        master.configure(bg=PALETTE["bg_dark"])
        master.geometry("1600x1000")

        # Configure ttk styles for better color integration
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        style.configure('TFrame', background=PALETTE["bg_dark"])
        style.configure('TLabel', background=PALETTE["bg_dark"], foreground=PALETTE["paper"])
        style.configure('TButton', background=PALETTE["accent"], foreground=PALETTE["paper"])
        style.configure('TLabelframe', background=PALETTE["bg_dark"], foreground=PALETTE["sand"])
        style.configure('TLabelframe.Label', background=PALETTE["bg_dark"], foreground=PALETTE["sand"])
        style.configure('TNotebook', background=PALETTE["bg_dark"])
        style.configure('TNotebook.Tab', background=PALETTE["bg_mid"], foreground=PALETTE["paper"])
        style.map('TNotebook.Tab', background=[('selected', PALETTE["accent"])])
        style.configure('Treeview', background=PALETTE["paper"], foreground=PALETTE["bg_dark"], fieldbackground=PALETTE["paper"])
        style.configure('Treeview.Heading', background=PALETTE["bg_mid"], foreground=PALETTE["paper"])

        # Main frame
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title with enhanced styling
        title_label = tk.Label(self.main_frame, text="Valheim Loot Diff", 
                              font=("Helvetica", 28, "bold"), 
                              foreground=PALETTE["paper"], 
                              background=PALETTE["bg_dark"])
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(self.main_frame, 
                                 text="Enchanting Material Drop Rate Analysis", 
                                 font=("Helvetica", 12), 
                                 foreground=PALETTE["sand"], 
                                 background=PALETTE["bg_dark"])
        subtitle_label.pack(pady=2)

        # Minimal controls frame
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.pack(pady=10, fill="x")

        # World Level control
        world_frame = ttk.Frame(controls_frame)
        world_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(world_frame, text="World Level:", foreground=PALETTE["paper"], font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(0,5))
        self.world_level = tk.StringVar(value="5")
        world_spinbox = ttk.Spinbox(world_frame, from_=0, to=7, width=5, textvariable=self.world_level, font=("Helvetica", 10))
        world_spinbox.pack(side=tk.LEFT)

        # Character Analysis toggle
        self.compose_chars = tk.BooleanVar(value=True)
        char_check = ttk.Checkbutton(controls_frame, text="Include Character Analysis", variable=self.compose_chars)
        char_check.pack(side=tk.LEFT, padx=20)

        # Refresh button
        self.refresh_button = tk.Button(controls_frame, 
                                      text="Refresh Analysis", 
                                      command=self.run_diff,
                                      font=("Helvetica", 11, "bold"),
                                      bg=PALETTE["accent"],
                                      fg=PALETTE["paper"],
                                      activebackground=PALETTE["bg_mid"],
                                      activeforeground=PALETTE["paper"],
                                      relief="raised",
                                      bd=2,
                                      padx=15,
                                      pady=3)
        self.refresh_button.pack(side=tk.RIGHT, padx=10)

        # Export button (writes reports on demand)
        self.export_button = tk.Button(controls_frame,
                                      text="Export Reports",
                                      command=self.export_reports,
                                      font=("Helvetica", 11, "bold"),
                                      bg=PALETTE["bg_mid"],
                                      fg=PALETTE["paper"],
                                      activebackground=PALETTE["accent"],
                                      activeforeground=PALETTE["paper"],
                                      relief="raised",
                                      bd=2,
                                      padx=12,
                                      pady=3)
        self.export_button.pack(side=tk.RIGHT, padx=10)

        # Coverage check button (diagnostics)
        self.coverage_button = tk.Button(controls_frame,
                                        text="Coverage Check",
                                        command=self.coverage_check,
                                        font=("Helvetica", 11, "bold"),
                                        bg=PALETTE["bg_mid"],
                                        fg=PALETTE["paper"],
                                        activebackground=PALETTE["accent"],
                                        activeforeground=PALETTE["paper"],
                                        relief="raised",
                                        bd=2,
                                        padx=12,
                                        pady=3)
        self.coverage_button.pack(side=tk.RIGHT, padx=10)

        # Main display area - simplified layout
        self.display_frame = ttk.Frame(self.main_frame)
        self.display_frame.pack(expand=True, fill="both", pady=10)

        # Overall drop rates summary
        summary_label = tk.Label(self.display_frame, 
                                text="Overall Drop Rates (All Monsters)", 
                                font=("Helvetica", 14, "bold"),
                                bg=PALETTE["bg_dark"], 
                                fg=PALETTE["paper"])
        summary_label.pack(pady=(0, 5))

        self.summary_text = tk.Text(self.display_frame, 
                               state="normal", 
                               bg=PALETTE["paper"], 
                               fg=PALETTE["bg_dark"], 
                               wrap=tk.WORD,
                               font=("Consolas", 12),
                               height=8)
        self.summary_text.pack(expand=False, fill="x", padx=5, pady=5)

        # Per-monster breakdown
        monster_label = tk.Label(self.display_frame, 
                                text="Per-Monster Breakdown", 
                                font=("Helvetica", 14, "bold"),
                                bg=PALETTE["bg_dark"], 
                                fg=PALETTE["paper"])
        monster_label.pack(pady=(10, 5))

        # Create treeview for monster data (active % and Δ vs baseline in percentage points)
        columns = (
            "Monster",
            "Magic %", "Δ Magic (pp)",
            "Rare %", "Δ Rare (pp)",
            "Epic %", "Δ Epic (pp)",
            "Legendary %", "Δ Legendary (pp)",
            "Mythic %", "Δ Mythic (pp)"
        )
        self.monster_tree = self.create_treeview(self.display_frame, columns)

        # Status text for logging
        self.status_text = tk.Text(self.display_frame, 
                                  state="normal", 
                                  bg=PALETTE["paper"], 
                                  fg=PALETTE["bg_dark"], 
                                  wrap=tk.WORD,
                                  font=("Consolas", 8),
                                  height=8)
        self.status_text.pack(expand=False, fill="x", padx=5, pady=5)

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
        self.act_sets = {}
        self.base_shares = {}
        self.act_shares = {}
        self.global_base = {}
        self.global_act = {}
        self.item_base = {}
        self.item_act = {}
        self.auto_export = False

        # Set default paths
        self.baseline_path = os.path.normpath("Valheim_Help_Docs/JewelHeim-RelicHeim-5.4.10_Backup/")
        self.active_path = os.path.normpath("Valheim/profiles/Dogeheim_Player/BepInEx/config/")
        self.out_path = "./loot_report"

        # Auto-run analysis after a short delay
        self.master.after(500, self.auto_run_analysis)

    def auto_run_analysis(self):
        """Automatically run the analysis when GUI launches"""
        self.log_message("Auto-running analysis with default settings...")
        self.run_diff()

    def create_treeview(self, parent, columns, show_headers=True):
        """Create a Treeview widget with the specified columns"""
        # Create a frame to hold the treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(expand=True, fill="both")
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings" if show_headers else "tree")
        if show_headers:
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, minwidth=80)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout within the frame
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        return tree

    def populate_treeview(self, tree, data, clear_existing=True):
        """Populate a Treeview with data"""
        if clear_existing:
            for item in tree.get_children():
                tree.delete(item)
        
        if not data:
            return
        
        for row_data in data:
            values = [row_data.get(col, "") for col in tree["columns"]]
            tree.insert("", "end", values=values)

    # File selection methods removed for minimalist interface
    # All paths are now hardcoded to defaults

    # Load methods removed for minimalist interface

    def log_message(self, message):
        """Add a message to the status text"""
        self.status_text.insert(tk.END, f"{message}\n")
                    self.status_text.see(tk.END)
        self.master.update()

    def run_diff(self):
        self.status_text.delete(1.0, tk.END)
        self.log_message("Running Valheim Loot Diff...")

        # Use default paths
        baseline_path = self.baseline_path
        active_path = self.active_path
        out_path = self.out_path
        compose_chars = self.compose_chars.get()
        scan_all = False  # Use default include paths
        tier_map_json = ""
        set_weight_json = ""
        assert_tier_change = ""
        
        # Get world level from spinbox
        try:
            world_level = int(self.world_level.get())
            world_level = max(0, min(7, world_level))  # Clamp to 0-7
        except ValueError:
            world_level = 5  # Default if invalid

        # Run analysis in a separate thread to keep GUI responsive
        self.refresh_button.config(state="disabled", bg=PALETTE["muted"])
        self.gui_thread = threading.Thread(target=self.run_analysis_thread, 
                                         args=(baseline_path, active_path, out_path, compose_chars, 
                                               scan_all, tier_map_json, set_weight_json, 
                                               assert_tier_change, world_level))
            self.gui_thread.start()

    def run_analysis_thread(self, baseline_path, active_path, out_path, compose_chars, 
                          scan_all, tier_map_json, set_weight_json, assert_tier_change, world_level):
        try:
            self.log_message("Loading configurations...")
            self.include_paths = [] if scan_all else self.get_include_paths()
            self.set_map = crawl_configs(baseline_path, self.include_paths)
            self.act_sets = crawl_configs(active_path, self.include_paths)
            
            self.log_message("Computing shares...")
            self.base_shares = compute_shares(self.set_map, self.tier_regex)
            self.act_shares = compute_shares(self.act_sets, self.tier_regex)
            
            self.log_message("Computing global expectations...")
            self.global_base = compute_global_material_expectation(self.set_map, self.tier_regex, self.set_weights)
            self.global_act = compute_global_material_expectation(self.act_sets, self.tier_regex, self.set_weights)
            
            self.log_message("Computing per-item expectations...")
            self.item_base = compute_global_material_expectation_by_item(self.set_map, self.tier_regex, self.set_weights)
            self.item_act = compute_global_material_expectation_by_item(self.act_sets, self.tier_regex, self.set_weights)

            # Update GUI with results
            self.master.after(0, self.update_results_display, compose_chars, world_level)
            
            # Write reports only if explicitly requested (Export button)
            if out_path and self.auto_export:
                self.log_message("Auto-export enabled: writing reports to files...")
                self.write_reports(out_path, compose_chars)
            
            self.assert_global_change(assert_tier_change)
            self.log_message("Analysis complete!")
            
        except Exception as e:
            self.master.after(0, lambda e=e: messagebox.showerror("Error", f"An error occurred during analysis: {e}"))
        finally:
            self.master.after(0, lambda: self.refresh_button.config(state="normal", bg=PALETTE["accent"]))

    def update_results_display(self, compose_chars, world_level):
        """Update GUI with analysis results - simplified layout"""
        try:
            # Update overall summary
            self.update_summary_display()
            
            # Update per-monster breakdown
            self.update_monster_breakdown(compose_chars, world_level)
            
            self.log_message("GUI updated with analysis results")
            
        except Exception as e:
            self.log_message(f"Error updating GUI: {e}")

    def update_summary_display(self):
        """Update the overall summary display"""
        self.summary_text.delete(1.0, tk.END)
        
        # Get global material data
        global_data = self.get_global_material_rows()
        
        summary = "Overall Expected Items per Kill (All Monsters):\n\n"
        for row in global_data:
            tier = row.get("Tier", "")
            base_ev = row.get("Base E[item]", "")
            active_ev = row.get("Active E[item]", "")
            delta = row.get("Δ E[item]", "")
            delta_pct = row.get("Δ %", "")
            
            if tier and base_ev and active_ev:
                summary += f"{tier:12} | Base: {base_ev:>8} | Active: {active_ev:>8} | Δ: {delta:>8} ({delta_pct:>6})\n"
        
        self.summary_text.insert(tk.END, summary)

    def update_monster_breakdown(self, compose_chars, world_level):
        """Update the per-monster breakdown display with Active % and Δ vs Baseline (pp)."""
        try:
            # Use star multipliers from ACTIVE config
            mult_creature, mult_boss = parse_cllc_star_multipliers(self.active_path, world_level=world_level)

            # BASELINE: characters + baseline sets
            base_chars_map, _ = crawl_characters(self.baseline_path, self.include_paths)
            base_rows = compose_characters_report(
                base_chars_map, self.set_map, self.tier_regex,
                star_multiplier_creature=mult_creature,
                star_multiplier_boss=mult_boss,
            )
            base_by_char = {}
            for r in base_rows:
                try:
                    base_by_char[r.get("Character", "")] = {
                        "Magic": float(r.get("Magic E[item/kill]", 0) or 0.0),
                        "Rare": float(r.get("Rare E[item/kill]", 0) or 0.0),
                        "Epic": float(r.get("Epic E[item/kill]", 0) or 0.0),
                        "Legendary": float(r.get("Legendary E[item/kill]", 0) or 0.0),
                        "Mythic": float(r.get("Mythic E[item/kill]", 0) or 0.0),
                    }
                except Exception:
                    continue

            # ACTIVE: characters + active sets
            act_chars_map, _ = crawl_characters(self.active_path, self.include_paths)
            act_rows = compose_characters_report(
                act_chars_map, self.act_sets, self.tier_regex,
                star_multiplier_creature=mult_creature,
                star_multiplier_boss=mult_boss,
            )

            # Debug: log what characters we found
            all_chars = [r.get("Character", "") for r in act_rows if r.get("Character", "")]
            self.log_message(f"Found {len(all_chars)} characters: {all_chars[:10]}...")
            
            # Debug: show some sample data
            if act_rows:
                sample_row = act_rows[0]
                self.log_message(f"Sample row keys: {list(sample_row.keys())}")
                self.log_message(f"Sample row: {dict(list(sample_row.items())[:5])}")

            # Filter out only known bosses
            KNOWN_BOSSES = {"Eikthyr", "TheElder", "Bonemass", "Moder", "Yagluth"}
            
            out_rows = []
            for r in act_rows:
                cname = r.get("Character", "")
                if not cname:
                    continue
                    
                # Skip only known bosses
                if cname in KNOWN_BOSSES:
                    continue
                    
                try:
                    a_magic = float(r.get("Magic E[item/kill]", 0) or 0.0)
                    a_rare = float(r.get("Rare E[item/kill]", 0) or 0.0)
                    a_epic = float(r.get("Epic E[item/kill]", 0) or 0.0)
                    a_legend = float(r.get("Legendary E[item/kill]", 0) or 0.0)
                    a_myth = float(r.get("Mythic E[item/kill]", 0) or 0.0)
                    a_total = a_magic + a_rare + a_epic + a_legend + a_myth

                    # Include all entries, even if no enchanting drops (for debugging)
                    b_vals = base_by_char.get(cname, {"Magic":0.0,"Rare":0.0,"Epic":0.0,"Legendary":0.0,"Mythic":0.0})
                    b_magic = float(b_vals.get("Magic", 0.0))
                    b_rare = float(b_vals.get("Rare", 0.0))
                    b_epic = float(b_vals.get("Epic", 0.0))
                    b_legend = float(b_vals.get("Legendary", 0.0))
                    b_myth = float(b_vals.get("Mythic", 0.0))
                    b_total = b_magic + b_rare + b_epic + b_legend + b_myth

                    def pct(x, tot):
                        return (x / tot * 100.0) if tot > 0 else 0.0

                    a_magic_pct = pct(a_magic, a_total); b_magic_pct = pct(b_magic, b_total)
                    a_rare_pct = pct(a_rare, a_total); b_rare_pct = pct(b_rare, b_total)
                    a_epic_pct = pct(a_epic, a_total); b_epic_pct = pct(b_epic, b_total)
                    a_legend_pct = pct(a_legend, a_total); b_legend_pct = pct(b_legend, b_total)
                    a_myth_pct = pct(a_myth, a_total); b_myth_pct = pct(b_myth, b_total)

                    out_rows.append({
                        "Monster": cname,
                        "Magic %": f"{a_magic_pct:.2f}%", "Δ Magic (pp)": f"{(a_magic_pct - b_magic_pct):+.2f}",
                        "Rare %": f"{a_rare_pct:.2f}%", "Δ Rare (pp)": f"{(a_rare_pct - b_rare_pct):+.2f}",
                        "Epic %": f"{a_epic_pct:.2f}%", "Δ Epic (pp)": f"{(a_epic_pct - b_epic_pct):+.2f}",
                        "Legendary %": f"{a_legend_pct:.2f}%", "Δ Legendary (pp)": f"{(a_legend_pct - b_legend_pct):+.2f}",
                        "Mythic %": f"{a_myth_pct:.2f}%", "Δ Mythic (pp)": f"{(a_myth_pct - b_myth_pct):+.2f}",
                        "__sort_key": a_total,
                    })
                except Exception as e:
                    self.log_message(f"Error processing {cname}: {e}")
                    continue

            self.log_message(f"Found {len(out_rows)} entries after processing")
            
            # Sort by active total expected enchanting items per kill (desc)
            out_rows.sort(key=lambda d: float(d.get("__sort_key", 0.0)), reverse=True)
            for d in out_rows:
                d.pop("__sort_key", None)

            self.populate_treeview(self.monster_tree, out_rows)

        except Exception as e:
            self.log_message(f"Error updating monster breakdown: {e}")

    def get_include_paths(self) -> List[str]:
        # Return the default include paths used by the CLI
        return [
            # Active configurations - Loot Tables & Drop Configurations
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChest.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop_list.zListDrops.cfg",
            # Active configurations - Character Drop Files (these contain the actual monster loot)
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBase.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.VES.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Monstrum.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardry.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bosses.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophy.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.aListDrops.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.MushroomMonsters.cfg",
            # Active configurations - Additional Drop Tables
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.zBase.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chests.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/RockPiles/drop_that.drop_table.PileOres.cfg",
            # Active configurations - EpicLoot Patches
            "**/EpicLoot/patches/RelicHeimPatches/zLootables_TreasureLoot_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/zLootables_Equipment_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/zLootables_CreatureDrops_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/zLootables_BossDrops_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/zLootables_Adjustments_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/zLootables_MissingItems_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/zLootables_MissingItems_CreatureSpecific_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/Lootables_Wizardry_RelicHeim.json",
            # Active configurations - Enchanting System Files
            "**/EpicLoot/patches/RelicHeimPatches/EnchantCost_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/MaterialConversion_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/EnchantingUpgrades_RelicHeim.json",
            # Active configurations - Adventure/Shop System Files
            "**/EpicLoot/patches/RelicHeimPatches/AdventureData_SecretStash_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/AdventureData_Bounties_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/AdventureData_Gamble_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/AdventureData_TherzieWizardry_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/AdventureData_TherzieArmory_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/AdventureData_TherzieWarfare_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/AdventureData_TherzieWarfareFI_RelicHeim.json",
            # Active configurations - Item Info Files
            "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_Wizardry_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_Armory_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_Warfare_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_WarfareFI_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_zRandom_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_zOK_RelicHeim.json",
            # Active configurations - Legendary Sets
            "**/EpicLoot/patches/RelicHeimPatches/Legendaries_SetsLegendary_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/Legendaries_SetsMythic_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/Legendaries_SetsRemoved_RelicHeim.json",
            # Active configurations - Magic Effects
            "**/EpicLoot/patches/RelicHeimPatches/MagicEffects_RelicHeim.json",
            # Active configurations - Other EpicLoot Files
            "**/EpicLoot/patches/RelicHeimPatches/Recipes_RelicHeim.json",
            "**/EpicLoot/patches/RelicHeimPatches/Ability_RelicHeim.json",
            # Active configurations - Backpack Configuration Files
            "**/Backpacks.MajesticEpicLoot.yml",
            # Active configurations - World Location Pickable Items
            "**/warpalicious.More_World_Locations_PickableItemLists.yml",
            "**/warpalicious.More_World_Locations_LootLists.yml",
            # Active configurations - Creature Configurations
            "**/CreatureConfig_Creatures.yml",
            # Canonical RelicHeim files - Backup Loot Tables & Drop Configurations
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChestbackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop_list.zListDropsbackup.cfg",
            # Canonical RelicHeim files - Backup Character Drop Files
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBasebackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.VESbackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Monstrumbackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardrybackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bossesbackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophybackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.aListDropsbackup.cfg",
            # Canonical RelicHeim files - Backup Additional Drop Tables
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.zBasebackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chestsbackup.cfg",
            "**/_RelicHeimFiles/Drop,Spawn_That/RockPiles/drop_that.drop_table.PileOresbackup.cfg",
            # Canonical RelicHeim files - Backup EpicLoot Patches
            "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_TreasureLoot_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_Equipment_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_CreatureDrops_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_BossDrops_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_Adjustments_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/Lootables_Wizardry_RelicHeim.json",
            # Canonical RelicHeim files - Backup Enchanting System Files
            "**/EpicLootbackup/patches/RelicHeimPatches/EnchantCost_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/MaterialConversion_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/EnchantingUpgrades_RelicHeim.json",
            # Canonical RelicHeim files - Backup Adventure/Shop System Files
            "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_SecretStash_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_Bounties_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_Gamble_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_TherzieWizardry_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_TherzieArmory_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_TherzieWarfare_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_TherzieWarfareFI_RelicHeim.json",
            # Canonical RelicHeim files - Backup Item Info Files
            "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_Wizardry_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_Armory_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_Warfare_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_WarfareFI_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_zRandom_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_zOK_RelicHeim.json",
            # Canonical RelicHeim files - Backup Legendary Sets
            "**/EpicLootbackup/patches/RelicHeimPatches/Legendaries_SetsLegendary_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/Legendaries_SetsMythic_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/Legendaries_SetsRemoved_RelicHeim.json",
            # Canonical RelicHeim files - Backup Magic Effects
            "**/EpicLootbackup/patches/RelicHeimPatches/MagicEffects_RelicHeim.json",
            # Canonical RelicHeim files - Backup Other EpicLoot Files
            "**/EpicLootbackup/patches/RelicHeimPatches/Recipes_RelicHeim.json",
            "**/EpicLootbackup/patches/RelicHeimPatches/Ability_RelicHeim.json",
            # Canonical RelicHeim files - Backup Backpack Configuration Files
            "**/Backpacks.MajesticEpicLootbackup.yml",
            # Canonical RelicHeim files - Backup Item Database Files
            "**/wackysDatabase_backup/Items/_RelicHeimWDB2.0/zOther/Item_EssenceMagic.yml",
            "**/wackysDatabase_backup/Items/_RelicHeimWDB2.0/zOther/EpicLoot/Item_LeatherBelt.yml",
            # Canonical RelicHeim files - Backup Creature Configurations
            "**/CreatureConfig_Creaturesbackup.yml",
            "**/CreatureConfig_Monstrumbackup.yml",
            "**/CreatureConfig_Wizardrybackup.yml",
            "**/CreatureConfig_BiomeIncreasebackup.yml",
            "**/CreatureConfig_Bossesbackup.yml"
        ]

    def write_reports(self, out_path: str, compose_chars: bool):
        """Write reports to files (existing functionality)"""
        self.log_message("Writing reports...")

        out_csv = out_path + ".csv"
        out_html = out_path + ".html"
        self.write_csv_report(out_csv, self.get_common_sets_rows())
        self.write_html_report(out_html, compose_chars)

        global_csv = out_path + ".materials.global.csv"
        self.write_csv_report(global_csv, self.get_global_material_rows())

        if compose_chars:
            base_chars_csv = out_path + ".characters.base.csv"
            act_chars_csv = out_path + ".characters.active.csv"
            # Use CLLC multipliers from active config path with user-selected world level
            try:
                wl = int(self.world_level.get())
                wl = max(0, min(7, wl))
            except ValueError:
                wl = 5
            mult_creature, mult_boss = parse_cllc_star_multipliers(self.active_path, world_level=wl)
            self.log_message(f"Using world level {wl}: creature multiplier={mult_creature:.2f}, boss multiplier={mult_boss:.2f}")
            self.write_csv_report(base_chars_csv, compose_characters_report(self.char_map, self.set_map, self.tier_regex, star_multiplier_creature=mult_creature, star_multiplier_boss=mult_boss))
            act_char_map, _ = crawl_characters(self.active_path, self.include_paths)
            self.write_csv_report(act_chars_csv, compose_characters_report(act_char_map, self.set_map, self.tier_regex, star_multiplier_creature=mult_creature, star_multiplier_boss=mult_boss))
            self.log_message("Wrote character reports.")

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
        global_csv = path + ".materials.global.csv"
        self.write_csv_report(global_csv, self.get_global_material_rows())

        if compose_chars:
            base_chars_csv = path + ".characters.base.csv"
            act_chars_csv = path + ".characters.active.csv"
            # Use world level from GUI spinbox
            try:
                wl = int(self.world_level.get())
                wl = max(0, min(7, wl))
            except ValueError:
                wl = 5
            mult_creature, mult_boss = parse_cllc_star_multipliers(self.active_path, world_level=wl)
            self.write_csv_report(base_chars_csv, compose_characters_report(self.char_map, self.set_map, self.tier_regex, star_multiplier_creature=mult_creature, star_multiplier_boss=mult_boss))
            act_char_map, _ = crawl_characters(self.active_path, self.include_paths)
            self.write_csv_report(act_chars_csv, compose_characters_report(act_char_map, self.set_map, self.tier_regex, star_multiplier_creature=mult_creature, star_multiplier_boss=mult_boss))
            parts.append("<h2>Character Composition Reports</h2>")
            parts.append(f"<p>Wrote character reports to {base_chars_csv} and {act_chars_csv}</p>")

        parts.append(render_html_table(self.get_item_material_rows(), "Global Expected Enchanting Materials — Per Item"))
        parts.append("</body></html>")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(parts))
        self.log_message(f"Wrote HTML report to {path}")

    def get_common_sets_rows(self) -> List[Dict[str, str]]:
        common = sorted(set(self.base_shares.keys()) & set(self.act_shares.keys()))
        rows = []
        for name in common:
            b = self.set_map[name]; a = self.act_sets[name]
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
                self.log_message(f"Assert {tier} change: baseline={b:.6f}, active={a:.6f}, ratio={achieved:.4f}, target={target_ratio:.4f}")
                # Simple tolerance
                tol = 0.02
                if not (abs(achieved - target_ratio) <= tol * max(target_ratio, 1.0)):
                    messagebox.showwarning("Warning", f"Global tier change deviates beyond tolerance for {tier}.")
            else:
                messagebox.showwarning("Warning", f"Tier '{tier}' not found in global reports or not parseable.")
        else:
            messagebox.showwarning("Warning", f"Assertion '{expr}' is not in the correct format (e.g., Magic:+10% or Magic:+0.10).")

    def export_reports(self):
        """Export reports to files on demand from the GUI."""
        try:
            compose_chars = self.compose_chars.get()
            self.log_message(f"Exporting reports to base path: {self.out_path}")
            self.write_reports(self.out_path, compose_chars)
            self.log_message("Export complete.")
        except Exception as e:
            self.log_message(f"Export failed: {e}")

    def coverage_check(self):
        """Compare parsed monsters vs creatures referenced in active configs and log coverage gaps."""
        try:
            # Parsed monsters from current active analysis
            mult_creature, mult_boss = parse_cllc_star_multipliers(self.active_path, world_level=max(0, min(7, int(self.world_level.get() or 5))))
            act_chars_map, _ = crawl_characters(self.active_path, self.include_paths)
            act_rows = compose_characters_report(
                act_chars_map, self.act_sets, self.tier_regex,
                star_multiplier_creature=mult_creature,
                star_multiplier_boss=mult_boss,
            )
            parsed = {r.get("Character", "") for r in act_rows if r.get("Character", "")}

            # Expected from Drop That character_drop.* headers
            import re, json
            expected: set[str] = set()
            header_re = re.compile(r"^\[([^\].]+?)\.\d+\]")
            for root, _, files in os.walk(self.active_path):
                for fn in files:
                    if fn.startswith("drop_that.character_drop.") and fn.endswith(".cfg"):
                        fp = os.path.join(root, fn)
                        try:
                            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                                for line in f:
                                    m = header_re.match(line.strip())
                                    if m:
                                        expected.add(m.group(1))
                        except Exception:
                            pass

            # Expected from EpicLoot creature drops JSON (heuristic)
            def find_files(substring: str) -> list[str]:
                paths = []
                for root, _, files in os.walk(self.active_path):
                    for fn in files:
                        if substring in fn:
                            paths.append(os.path.join(root, fn))
                return paths

            def extract_creatures_from_json(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if isinstance(v, (dict, list)):
                            extract_creatures_from_json(v)
                        elif isinstance(v, str) and any(s in k.lower() for s in ("creature", "monster", "prefab")):
                            expected.add(v)
                elif isinstance(obj, list):
                    for it in obj:
                        extract_creatures_from_json(it)

            for name in ["zLootables_CreatureDrops_RelicHeim.json", "zLootables_BossDrops_RelicHeim.json"]:
                for fp in find_files(name):
                    try:
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            data = json.load(f)
                        extract_creatures_from_json(data)
                    except Exception:
                        pass

            # Expected from CreatureConfig_Creatures.yml (prefab names)
            try:
                prefab_re = re.compile(r"^\s*PrefabName\s*:\s*([A-Za-z0-9_]+)")
                for root, _, files in os.walk(self.active_path):
                    for fn in files:
                        if fn == "CreatureConfig_Creatures.yml":
                            with open(os.path.join(root, fn), "r", encoding="utf-8", errors="ignore") as f:
                                for line in f:
                                    m = prefab_re.match(line)
                                    if m:
                                        expected.add(m.group(1))
            except Exception:
                pass

            missing = sorted(x for x in expected if x not in parsed)
            self.log_message(f"Coverage: parsed={len(parsed)}, expected={len(expected)}, missing={len(missing)}")
            if missing:
                self.log_message(f"Missing examples: {missing[:25]}{' ...' if len(missing)>25 else ''}")
        except Exception as e:
            self.log_message(f"Coverage check failed: {e}")

def main():
    ap = argparse.ArgumentParser(description="Diff RelicHeim/EpicLoot material rates between baseline and active configs (v1.2).")
    # Default paths are relative to this repository so the script works out-of-the-box
    ap.add_argument("--baseline", required=False, default="Valheim_Help_Docs/JewelHeim-RelicHeim-5.4.10_Backup/", help="Path to baseline (pristine) config dir")
    ap.add_argument("--active", required=False, default="Valheim/profiles/Dogeheim_Player/BepInEx/config/", help="Path to active repo/config dir")
    ap.add_argument("--out", required=False, default="./loot_report", help="Output path prefix (without extension)")
    ap.add_argument("--tier-map-json", help="Optional JSON file overriding tier regex mapping")
    ap.add_argument("--set-weight-json", help="Optional JSON { setName: weight } to weight/scale set contributions for global aggregation")
    ap.add_argument("--use-character-weights", action="store_true", help="Weight sets by character drop references instead of manual weights")
    ap.add_argument("--assert-tier-change", help="Optional assertion of form Tier:+10%% or Tier:+0.10 to verify global change vs baseline")
    ap.add_argument("--gui", action="store_true", help="Launch Tkinter GUI interface")
    ap.add_argument("--compose-characters", action="store_true", help="Compose per-character expected tier counts and emit a report")
    ap.add_argument("--scan-all", action="store_true", help="Ignore default include filters and scan all supported config files under baseline/active")
    ap.add_argument("--world-level", type=int, default=5, help="Static world level (0-7) used to approximate star multipliers (default: 5)")
    ap.add_argument("--include-path", action="append", default=[
        # Active configurations - Loot Tables & Drop Configurations
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChest.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop_list.zListDrops.cfg",
        # Active configurations - Character Drop Files (these contain the actual monster loot)
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBase.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.VES.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Monstrum.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardry.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bosses.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophy.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.aListDrops.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.MushroomMonsters.cfg",
        # Active configurations - Additional Drop Tables
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.zBase.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chests.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/RockPiles/drop_that.drop_table.PileOres.cfg",
        # Active configurations - EpicLoot Patches
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_TreasureLoot_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_Equipment_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_CreatureDrops_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_BossDrops_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_Adjustments_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_MissingItems_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/zLootables_MissingItems_CreatureSpecific_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/Lootables_Wizardry_RelicHeim.json",
        # Active configurations - Enchanting System Files
        "**/EpicLoot/patches/RelicHeimPatches/EnchantCost_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/MaterialConversion_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/EnchantingUpgrades_RelicHeim.json",
        # Active configurations - Adventure/Shop System Files
        "**/EpicLoot/patches/RelicHeimPatches/AdventureData_SecretStash_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/AdventureData_Bounties_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/AdventureData_Gamble_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/AdventureData_TherzieWizardry_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/AdventureData_TherzieArmory_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/AdventureData_TherzieWarfare_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/AdventureData_TherzieWarfareFI_RelicHeim.json",
        # Active configurations - Item Info Files
        "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_Wizardry_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_Armory_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_Warfare_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_WarfareFI_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_zRandom_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/ItemInfo_zOK_RelicHeim.json",
        # Active configurations - Legendary Sets
        "**/EpicLoot/patches/RelicHeimPatches/Legendaries_SetsLegendary_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/Legendaries_SetsMythic_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/Legendaries_SetsRemoved_RelicHeim.json",
        # Active configurations - Magic Effects
        "**/EpicLoot/patches/RelicHeimPatches/MagicEffects_RelicHeim.json",
        # Active configurations - Other EpicLoot Files
        "**/EpicLoot/patches/RelicHeimPatches/Recipes_RelicHeim.json",
        "**/EpicLoot/patches/RelicHeimPatches/Ability_RelicHeim.json",
        # Active configurations - Backpack Configuration Files
        "**/Backpacks.MajesticEpicLoot.yml",
        # Active configurations - World Location Pickable Items
        "**/warpalicious.More_World_Locations_PickableItemLists.yml",
        "**/warpalicious.More_World_Locations_LootLists.yml",
        # Active configurations - Creature Configurations
        "**/CreatureConfig_Creatures.yml",
        # Canonical RelicHeim files - Backup Loot Tables & Drop Configurations
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChestbackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop_list.zListDropsbackup.cfg",
        # Canonical RelicHeim files - Backup Character Drop Files
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBasebackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.VESbackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Monstrumbackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardrybackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bossesbackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophybackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.aListDropsbackup.cfg",
        # Canonical RelicHeim files - Backup Additional Drop Tables
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.zBasebackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chestsbackup.cfg",
        "**/_RelicHeimFiles/Drop,Spawn_That/RockPiles/drop_that.drop_table.PileOresbackup.cfg",
        # Canonical RelicHeim files - Backup EpicLoot Patches
        "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_TreasureLoot_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_Equipment_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_CreatureDrops_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_BossDrops_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/zLootables_Adjustments_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/Lootables_Wizardry_RelicHeim.json",
        # Canonical RelicHeim files - Backup Enchanting System Files
        "**/EpicLootbackup/patches/RelicHeimPatches/EnchantCost_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/MaterialConversion_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/EnchantingUpgrades_RelicHeim.json",
        # Canonical RelicHeim files - Backup Adventure/Shop System Files
        "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_SecretStash_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_Bounties_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_Gamble_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_TherzieWizardry_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_TherzieArmory_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_TherzieWarfare_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/AdventureData_TherzieWarfareFI_RelicHeim.json",
        # Canonical RelicHeim files - Backup Item Info Files
        "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_Wizardry_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_Armory_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_Warfare_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_WarfareFI_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_zRandom_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/ItemInfo_zOK_RelicHeim.json",
        # Canonical RelicHeim files - Backup Legendary Sets
        "**/EpicLootbackup/patches/RelicHeimPatches/Legendaries_SetsLegendary_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/Legendaries_SetsMythic_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/Legendaries_SetsRemoved_RelicHeim.json",
        # Canonical RelicHeim files - Backup Magic Effects
        "**/EpicLootbackup/patches/RelicHeimPatches/MagicEffects_RelicHeim.json",
        # Canonical RelicHeim files - Backup Other EpicLoot Files
        "**/EpicLootbackup/patches/RelicHeimPatches/Recipes_RelicHeim.json",
        "**/EpicLootbackup/patches/RelicHeimPatches/Ability_RelicHeim.json",
        # Canonical RelicHeim files - Backup Backpack Configuration Files
        "**/Backpacks.MajesticEpicLootbackup.yml",
        # Canonical RelicHeim files - Backup Item Database Files
        "**/wackysDatabase_backup/Items/_RelicHeimWDB2.0/zOther/Item_EssenceMagic.yml",
        "**/wackysDatabase_backup/Items/_RelicHeimWDB2.0/zOther/EpicLoot/Item_LeatherBelt.yml",
        # Canonical RelicHeim files - Backup Creature Configurations
        "**/CreatureConfig_Creaturesbackup.yml",
        "**/CreatureConfig_Monstrumbackup.yml",
        "**/CreatureConfig_Wizardrybackup.yml",
        "**/CreatureConfig_BiomeIncreasebackup.yml",
        "**/CreatureConfig_Bossesbackup.yml"
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

    base_chars: Dict[str, CharacterDrops] = {}
    act_chars: Dict[str, CharacterDrops] = {}
    base_char_weights: Dict[str, float] = {}
    act_char_weights: Dict[str, float] = {}
    if args.use_character_weights or args.compose_characters:
        base_chars, base_char_weights = crawl_characters(args.baseline, include_filters)
        act_chars, act_char_weights = crawl_characters(args.active, include_filters)

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
    base_global = compute_global_material_expectation(
        base_sets,
        tier_map,
        None if args.use_character_weights else set_weights,
        base_char_weights if args.use_character_weights else None,
    )
    act_global  = compute_global_material_expectation(
        act_sets,
        tier_map,
        None if args.use_character_weights else set_weights,
        act_char_weights if args.use_character_weights else None,
    )
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
        # Parse star multipliers from active CLLC config using requested world level
        mult_creature, mult_boss = parse_cllc_star_multipliers(args.active, max(min(args.world_level,7),0))
        base_rows = compose_characters_report(base_chars, base_sets, tier_map, star_multiplier_creature=mult_creature, star_multiplier_boss=mult_boss)
        act_rows  = compose_characters_report(act_chars, act_sets, tier_map, star_multiplier_creature=mult_creature, star_multiplier_boss=mult_boss)
        write_csv(args.out + ".characters.base.csv", base_rows)
        write_csv(args.out + ".characters.active.csv", act_rows)
        print(f"Wrote: {args.out}.characters.base.csv")
        print(f"Wrote: {args.out}.characters.active.csv")

    # Per-item global report
    base_items = compute_global_material_expectation_by_item(
        base_sets,
        tier_map,
        None if args.use_character_weights else set_weights,
        base_char_weights if args.use_character_weights else None,
    )
    act_items  = compute_global_material_expectation_by_item(
        act_sets,
        tier_map,
        None if args.use_character_weights else set_weights,
        act_char_weights if args.use_character_weights else None,
    )
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
    app = LootDiffGUI(root)
    
    # Bring window to front
    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

    root.mainloop()

if __name__ == "__main__":
    main()
