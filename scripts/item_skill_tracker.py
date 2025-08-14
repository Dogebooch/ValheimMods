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

            # Enhanced numeric extraction with better pattern matching
            def get_num(keys: list[str]) -> float | None:
                for k in keys:
                    if k in lower_headers:
                        v = row.get(lower_headers[lower_headers.index(k)], "")
                        if v is None:
                            continue
                        try:
                            # Handle formats like "45", "45.0", "45 (Slash)", "45-60", "45.5", "45,000"
                            s = str(v).strip()
                            # Remove common suffixes and parentheses
                            s = re.sub(r'\s*\([^)]*\)', '', s)  # Remove (Slash) etc
                            s = re.sub(r'\s*[A-Za-z]+$', '', s)  # Remove trailing text
                            s = s.replace(',', '')  # Handle thousands separators
                            s = s.split()[0] if s else ""
                            
                            if "-" in s:
                                parts = [float(p) for p in s.split("-") if p]
                                if parts:
                                    return sum(parts) / len(parts)
                            elif s:
                                return float(s)
                        except Exception:
                            continue
                return None

            # Enhanced damage detection - look for individual damage types and total
            damage_types = {
                "slash": get_num(["slash", "slashdamage", "slash_damage"]),
                "pierce": get_num(["pierce", "piercedamage", "pierce_damage"]),
                "blunt": get_num(["blunt", "bluntdamage", "blunt_damage"]),
                "fire": get_num(["fire", "firedamage", "fire_damage"]),
                "frost": get_num(["frost", "frostdamage", "frost_damage"]),
                "poison": get_num(["poison", "poisondamage", "poison_damage"]),
                "lightning": get_num(["lightning", "lightningdamage", "lightning_damage"]),
                "spirit": get_num(["spirit", "spiritdamage", "spirit_damage"]),
                "physical": get_num(["physical", "physicaldamage", "physical_damage"]),
                "magic": get_num(["magic", "magicdamage", "magic_damage"]),
            }
            
            # Get total damage from various possible fields
            damage_total = get_num([
                "damage", "totaldamage", "dmg", "basedamage", "total_damage", "base_damage",
                "weapondamage", "weapon_damage", "attackdamage", "attack_damage"
            ])
            
            # If no total damage found, sum up individual types
            if damage_total is None:
                damage_total = sum(v for v in damage_types.values() if v is not None)
                if damage_total == 0:
                    damage_total = None

            # Enhanced armor detection
            armor = get_num([
                "armor", "armour", "armorvalue", "armourvalue", "armor_value", "armour_value",
                "defense", "defence", "protection", "armorrating", "armourrating"
            ])
            
            # Enhanced block detection
            block = get_num([
                "blockpower", "block", "parry", "blockpower", "block_power", "parrypower",
                "blockvalue", "parryvalue", "block_value", "parry_value"
            ])
            
            # Enhanced tier detection
            tier = get_num([
                "tier", "crafting_tier", "level", "itemtier", "item_tier", "craftingtier",
                "tooltier", "tool_tier", "mtooltier", "m_tooltier"
            ])
            
            # Enhanced weight detection
            weight = get_num([
                "weight", "itemweight", "item_weight", "mass", "carryweight", "carry_weight"
            ])
            
            # Enhanced durability detection
            durability = get_num([
                "durability", "maxdurability", "max_durability", "maxdurability", "durability_max",
                "uses", "maxuses", "max_uses", "lifetime", "maxlifetime"
            ])
            
            # New stat detections
            speed = get_num([
                "speed", "attackspeed", "attack_speed", "swingspeed", "swing_speed",
                "usespeed", "use_speed", "craftspeed", "craft_speed"
            ])
            
            range_val = get_num([
                "range", "attackrange", "attack_range", "reach", "distance", "maxrange"
            ])
            
            knockback = get_num([
                "knockback", "knock_back", "pushback", "push_back", "force"
            ])
            
            backstab = get_num([
                "backstab", "back_stab", "backstabmultiplier", "back_stab_multiplier"
            ])
            
            parry_force = get_num([
                "parryforce", "parry_force", "parrybonus", "parry_bonus"
            ])
            
            movement = get_num([
                "movement", "movementspeed", "movement_speed", "movespeed", "move_speed"
            ])
            
            stamina = get_num([
                "stamina", "staminause", "stamina_use", "staminaconsumption", "stamina_consumption"
            ])

            # Build comprehensive summary string
            parts: list[str] = []
            
            # Primary combat stats (damage/armor/block)
            if armor is not None:
                parts.append(f"Armor {int(armor) if armor.is_integer() else round(armor,1)}")
            elif block is not None and (damage_total is None or block >= (damage_total or 0) * 0.6):
                parts.append(f"Block {int(block) if block.is_integer() else round(block,1)}")
            elif damage_total is not None:
                parts.append(f"DMG {int(damage_total) if damage_total.is_integer() else round(damage_total,1)}")
                
                # Add damage type breakdown if we have individual types
                damage_parts = []
                for dmg_type, dmg_val in damage_types.items():
                    if dmg_val is not None and dmg_val > 0:
                        damage_parts.append(f"{dmg_type.capitalize()}:{int(dmg_val) if dmg_val.is_integer() else round(dmg_val,1)}")
                if damage_parts and len(damage_parts) > 1:
                    parts.append(f"({', '.join(damage_parts)})")

            # Secondary combat stats
            if speed is not None:
                parts.append(f"Spd {round(speed,1)}")
            if range_val is not None:
                parts.append(f"Rng {int(range_val) if range_val.is_integer() else round(range_val,1)}")
            if knockback is not None:
                parts.append(f"KB {int(knockback) if knockback.is_integer() else round(knockback,1)}")
            if backstab is not None:
                parts.append(f"BS {int(backstab) if backstab.is_integer() else round(backstab,1)}")
            if parry_force is not None:
                parts.append(f"PF {int(parry_force) if parry_force.is_integer() else round(parry_force,1)}")

            # Utility stats
            if tier is not None:
                parts.append(f"T{int(tier)}")
            if weight is not None:
                parts.append(f"Wt {round(weight,1)}")
            if durability is not None:
                parts.append(f"Dur {int(durability) if durability.is_integer() else round(durability,0)}")
            if movement is not None:
                parts.append(f"Mov {round(movement,1)}")
            if stamina is not None:
                parts.append(f"Sta {int(stamina) if stamina.is_integer() else round(stamina,1)}")

            summary = " | ".join(parts) if parts else ""
            return station, summary

        if source is None:
            return result

        if source.suffix.lower() in (".csv", ".txt"):
            with open(source, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                lower_headers = [h.lower().strip() for h in headers]
                item_col, _station_col = self._guess_columns(headers)
                for row in reader:
                    item = (row.get(item_col, "") or "").strip()
                    if not item:
                        continue
                    station, summary = summarize_row(row, lower_headers)
                    result[item] = {"station": station, "stats": summary}
        else:
            # Enhanced YML parsing with more comprehensive stat detection
            try:
                with open(source, 'r', encoding='utf-8') as f:
                    text = f.read()
                current_item = None
                stash: dict[str, str] = {}
                
                def parse_yml_stats() -> tuple[str, str]:
                    station = stash.get('station', '')
                    
                    # Enhanced stat extraction from stash
                    stats_parts = []
                    
                    # Damage detection
                    damage_total = None
                    damage_types = {}
                    
                    # Look for total damage
                    for dmg_key in ['damage', 'totaldamage', 'dmg', 'basedamage']:
                        if dmg_key in stash:
                            try:
                                damage_total = float(stash[dmg_key])
                                break
                            except:
                                pass
                    
                    # Look for individual damage types
                    for dmg_type in ['slash', 'pierce', 'blunt', 'fire', 'frost', 'poison', 'lightning', 'spirit']:
                        if dmg_type in stash:
                            try:
                                damage_types[dmg_type] = float(stash[dmg_type])
                            except:
                                pass
                    
                    # Sum up damage types if no total found
                    if damage_total is None and damage_types:
                        damage_total = sum(damage_types.values())
                    
                    # Armor detection
                    armor = None
                    for armor_key in ['armor', 'armour', 'defense', 'defence']:
                        if armor_key in stash:
                            try:
                                armor = float(stash[armor_key])
                                break
                            except:
                                pass
                    
                    # Block detection
                    block = None
                    for block_key in ['block', 'blockpower', 'parry']:
                        if block_key in stash:
                            try:
                                block = float(stash[block_key])
                                break
                            except:
                                pass
                    
                    # Build stats string
                    if armor is not None:
                        stats_parts.append(f"Armor {int(armor) if armor.is_integer() else round(armor,1)}")
                    elif block is not None and (damage_total is None or block >= (damage_total or 0) * 0.6):
                        stats_parts.append(f"Block {int(block) if block.is_integer() else round(block,1)}")
                    elif damage_total is not None:
                        stats_parts.append(f"DMG {int(damage_total) if damage_total.is_integer() else round(damage_total,1)}")
                        
                        # Add damage breakdown if we have types
                        if damage_types and len(damage_types) > 1:
                            dmg_parts = [f"{k.capitalize()}:{int(v) if v.is_integer() else round(v,1)}" 
                                        for k, v in damage_types.items() if v > 0]
                            if dmg_parts:
                                stats_parts.append(f"({', '.join(dmg_parts)})")
                    
                    # Add other stats
                    for stat_key in ['weight', 'durability', 'tier', 'speed', 'range']:
                        if stat_key in stash:
                            try:
                                val = float(stash[stat_key])
                                if stat_key == 'weight':
                                    stats_parts.append(f"Wt {round(val,1)}")
                                elif stat_key == 'durability':
                                    stats_parts.append(f"Dur {int(val) if val.is_integer() else round(val,0)}")
                                elif stat_key == 'tier':
                                    stats_parts.append(f"T{int(val)}")
                                elif stat_key == 'speed':
                                    stats_parts.append(f"Spd {round(val,1)}")
                                elif stat_key == 'range':
                                    stats_parts.append(f"Rng {int(val) if val.is_integer() else round(val,1)}")
                            except:
                                pass
                    
                    summary = " | ".join(stats_parts) if stats_parts else ""
                    return station, summary
                
                for raw in text.splitlines():
                    line = raw.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Item name detection
                    m_item = re.search(r"(name|item|internal|prefab)\s*:\s*([A-Za-z0-9_\-\.]+)", line, re.IGNORECASE)
                    if m_item:
                        if current_item and stash:
                            # Summarize previous item
                            station, summary = parse_yml_stats()
                            result[current_item] = {"station": station, "stats": summary}
                        current_item = m_item.group(2)
                        stash = {}
                        continue
                    
                    # Enhanced stat detection patterns
                    patterns = [
                        # Station
                        (r"(crafting[_\s]?station|station)\s*:\s*([A-Za-z0-9_\-\. ]+)", 'station'),
                        # Damage types
                        (r"(damage|totaldamage|dmg|basedamage)\s*:\s*([0-9.\-]+)", 'damage'),
                        (r"(slash|pierce|blunt|fire|frost|poison|lightning|spirit)\s*:\s*([0-9.\-]+)", r'\1'),
                        # Armor/Block
                        (r"(armor|armour|defense|defence)\s*:\s*([0-9.]+)", 'armor'),
                        (r"(block|blockpower|parry)\s*:\s*([0-9.]+)", 'block'),
                        # Utility stats
                        (r"(weight|mass)\s*:\s*([0-9.]+)", 'weight'),
                        (r"(durability|maxdurability|uses)\s*:\s*([0-9.]+)", 'durability'),
                        (r"(tier|level|mtooltier)\s*:\s*([0-9.]+)", 'tier'),
                        (r"(speed|attackspeed|swingspeed)\s*:\s*([0-9.]+)", 'speed'),
                        (r"(range|attackrange|reach)\s*:\s*([0-9.]+)", 'range'),
                        (r"(knockback|pushback|force)\s*:\s*([0-9.]+)", 'knockback'),
                        (r"(backstab|back_stab)\s*:\s*([0-9.]+)", 'backstab'),
                        (r"(parryforce|parry_force)\s*:\s*([0-9.]+)", 'parryforce'),
                        (r"(movement|movespeed)\s*:\s*([0-9.]+)", 'movement'),
                        (r"(stamina|staminause)\s*:\s*([0-9.]+)", 'stamina'),
                    ]
                    
                    for pattern, key in patterns:
                        m = re.search(pattern, line, re.IGNORECASE)
                        if m:
                            if isinstance(key, str):
                                stash[key] = m.group(2)
                            else:
                                # For damage types, use the matched group as key
                                stash[m.group(1)] = m.group(2)
                            break
                
                # Handle last item
                if current_item and stash and current_item not in result:
                    station, summary = parse_yml_stats()
                    result[current_item] = {"station": station, "stats": summary}
                    
            except Exception:
                pass
        return result

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

    def _product_from_recipe_name(self, name: str) -> str:
        """Map a recipe name to its output prefab (best-effort).

        Examples:
          Recipe_Svandemcrescent -> Svandemcrescent
          Recipe_ElectromancerBackpack_Recipe_Custom -> ElectromancerBackpack
        """
        s = (name or "").strip()
        if not s:
            return ""
        try:
            s = re.sub(r"^(Recipe_)+", "", s, flags=re.IGNORECASE)
            s = re.sub(r"_Recipe.*$", "", s, flags=re.IGNORECASE)
            s = re.sub(r"^Recipe_", "", s, flags=re.IGNORECASE)
        except Exception:
            pass
        return s

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

            # Heuristics: try to find prefab blocks; if recipe file, infer product from recipe name
            pstr = str(path).replace("\\", "/")
            is_recipe_file = "/Recipes/" in pstr
            prefab_candidates: set[str] = set()
            if is_recipe_file:
                m_rname = re.search(r"^\s*name\s*:\s*([A-Za-z0-9_\-.]+)\s*$", text, re.MULTILINE)
                if m_rname:
                    prod = self._product_from_recipe_name(m_rname.group(1))
                    if prod:
                        prefab_candidates.add(prod)
            if not prefab_candidates:
                for m in re.finditer(r"^\s*(?:-\s*)?PrefabName\s*:\s*([A-Za-z0-9_\-.]+)\s*$", text, re.MULTILINE):
                    prefab_candidates.add(m.group(1))
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
            m_slevel = re.search(r"(CraftingStationLevel|StationLevel|RequiredStationLevel|minStationLevel)\s*:\s*([0-9]+)", text, re.IGNORECASE)
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
            
            # Enhanced damage detection with individual types
            damage_types = {}
            dmg_total = None
            
            # Look for total damage first
            for key in ["TotalDamage", "Damage", "BaseDamage", "total_damage", "base_damage", "weapon_damage", "attack_damage"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        dmg_total = float(v)
                        break
                    except Exception:
                        pass
            
            # Look for individual damage types
            for key in ["slash", "pierce", "blunt", "fire", "frost", "poison", "lightning", "spirit", "physical", "magic"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        damage_types[key] = float(v)
                    except Exception:
                        pass
            
            # Sum up damage types if no total found
            if dmg_total is None and damage_types:
                dmg_total = sum(damage_types.values())
                if dmg_total == 0:
                    dmg_total = None
            
            # Enhanced armor detection
            armor = None
            for key in ["armor", "armour", "armorvalue", "armourvalue", "defense", "defence", "protection"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        armor = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced block detection
            block = None
            for key in ["blockpower", "block", "parry", "block_power", "parrypower", "blockvalue", "parryvalue"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        block = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced weight detection
            weight = None
            for key in ["weight", "itemweight", "mass", "carryweight"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        weight = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced durability detection
            durability = None
            for key in ["durability", "maxdurability", "max_durability", "uses", "maxuses", "lifetime"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        durability = float(v)
                        break
                    except Exception:
                        pass
            
            # New stat detections
            speed = None
            for key in ["speed", "attackspeed", "attack_speed", "swingspeed", "swing_speed", "usespeed", "craftspeed"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        speed = float(v)
                        break
                    except Exception:
                        pass
            
            range_val = None
            for key in ["range", "attackrange", "attack_range", "reach", "distance", "maxrange"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        range_val = float(v)
                        break
                    except Exception:
                        pass
            
            knockback = None
            for key in ["knockback", "knock_back", "pushback", "push_back", "force"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        knockback = float(v)
                        break
                    except Exception:
                        pass
            
            backstab = None
            for key in ["backstab", "back_stab", "backstabmultiplier", "back_stab_multiplier"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        backstab = float(v)
                        break
                    except Exception:
                        pass
            
            parry_force = None
            for key in ["parryforce", "parry_force", "parrybonus", "parry_bonus"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        parry_force = float(v)
                        break
                    except Exception:
                        pass
            
            movement = None
            for key in ["movement", "movementspeed", "movement_speed", "movespeed", "move_speed"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        movement = float(v)
                        break
                    except Exception:
                        pass
            
            stamina = None
            for key in ["stamina", "staminause", "stamina_use", "staminaconsumption", "stamina_consumption"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        stamina = float(v)
                        break
                    except Exception:
                        pass
            
            # Store stats with proper formatting
            if armor is not None: 
                stats['armor'] = str(int(armor) if armor.is_integer() else round(armor, 1))
            if dmg_total is not None: 
                stats['damage_total'] = str(int(dmg_total) if dmg_total.is_integer() else round(dmg_total, 1))
                # Add damage breakdown if we have individual types
                if damage_types and len(damage_types) > 1:
                    dmg_parts = [f"{k.capitalize()}:{int(v) if v.is_integer() else round(v,1)}" 
                                for k, v in damage_types.items() if v > 0]
                    if dmg_parts:
                        stats['damage_breakdown'] = ', '.join(dmg_parts)
            if weight is not None: 
                stats['weight'] = str(round(weight, 1))
            if block is not None: 
                stats['block'] = str(int(block) if block.is_integer() else round(block, 1))
            if durability is not None: 
                stats['durability'] = str(int(durability) if durability.is_integer() else round(durability, 0))
            if speed is not None: 
                stats['speed'] = str(round(speed, 1))
            if range_val is not None: 
                stats['range'] = str(int(range_val) if range_val.is_integer() else round(range_val, 1))
            if knockback is not None: 
                stats['knockback'] = str(int(knockback) if knockback.is_integer() else round(knockback, 1))
            if backstab is not None: 
                stats['backstab'] = str(int(backstab) if backstab.is_integer() else round(backstab, 1))
            if parry_force is not None: 
                stats['parry_force'] = str(int(parry_force) if parry_force.is_integer() else round(parry_force, 1))
            if movement is not None: 
                stats['movement'] = str(round(movement, 1))
            if stamina is not None: 
                stats['stamina'] = str(int(stamina) if stamina.is_integer() else round(stamina, 1))

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

            # Pattern C: Wacky reqs list lines: "- ItemName:Qty:..."
            if not recipe and re.search(r"^\s*reqs\s*:\s*$", text, re.IGNORECASE | re.MULTILINE):
                for rm in re.finditer(r"^\s*-\s*([A-Za-z0-9_\-.]+)\s*:\s*([0-9]+)\s*:", text, re.MULTILINE):
                    try:
                        recipe.append((rm.group(1), int(rm.group(2))))
                    except Exception:
                        pass

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

        # 4) EpicLoot patch recipes: parse JSON patches that target recipes
        patches_dir = root / "EpicLoot" / "patches"
        if patches_dir.exists():
            for p in patches_dir.rglob("*.json"):
                try:
                    j = json.loads(p.read_text(encoding='utf-8', errors='ignore'))
                except Exception:
                    continue
                patches = j.get("Patches") or j.get("patches") or []
                for ent in patches:
                    path_expr = str(ent.get("Path", ""))
                    # Extract recipe name and the targeted field
                    m_name = re.search(r"name\s*==\s*'([^']+)'", path_expr)
                    m_field = re.search(r"\]\.(craftingStation|resources|RequiredStationLevel|StationLevel|minStationLevel)", path_expr, re.IGNORECASE)
                    if not m_name or not m_field:
                        continue
                    rname = m_name.group(1)
                    field = m_field.group(1)
                    product = self._product_from_recipe_name(rname)
                    if not product:
                        continue
                    d = info.setdefault(product, {})
                    if field.lower() == 'craftingstation':
                        val = ent.get('Value')
                        if isinstance(val, str) and val:
                            d['station'] = val
                    elif field.lower() in ('requiredstationlevel', 'stationlevel', 'minstationlevel'):
                        try:
                            lvl_val = ent.get('Value')
                            if lvl_val is not None:
                                d['station_level'] = str(int(lvl_val))
                        except Exception:
                            pass
                    elif field.lower() == 'resources':
                        val = ent.get('Value')
                        if isinstance(val, list):
                            try:
                                parts = []
                                for r in val:
                                    it = r.get('item') or r.get('name') or r.get('prefab')
                                    amt = r.get('amount') or r.get('qty') or r.get('quantity')
                                    if it:
                                        if amt is None:
                                            parts.append(str(it))
                                        else:
                                            parts.append(f"{it} x{amt}")
                                if parts:
                                    d['recipe'] = ', '.join(parts)
                            except Exception:
                                pass

        # 5) Wacky DB recipes outside BulkYML: parse as in Wacky but scoped to this config folder
        wdb_recipes_dir = root / "wackysDatabase" / "Recipes"
        if wdb_recipes_dir.exists():
            for yml in wdb_recipes_dir.rglob("*.yml"):
                try:
                    txt = yml.read_text(encoding='utf-8', errors='ignore')
                except Exception:
                    continue
                # Extract product from name
                m_n = re.search(r"^\s*name\s*:\s*([A-Za-z0-9_\-.]+)\s*$", txt, re.MULTILINE)
                product = self._product_from_recipe_name(m_n.group(1)) if m_n else ""
                if not product:
                    continue
                dd = info.setdefault(product, {})
                # Station and level
                m_st = re.search(r"(CraftingStation|craftingStation|Station|WorkBench)\s*:\s*([A-Za-z0-9_\- $]+)", txt)
                if m_st and not dd.get('station'):
                    dd['station'] = m_st.group(2).strip()
                m_sl = re.search(r"(CraftingStationLevel|StationLevel|RequiredStationLevel|minStationLevel)\s*:\s*([0-9]+)", txt)
                if m_sl and not dd.get('station_level'):
                    dd['station_level'] = m_sl.group(2)
                # reqs list like "- Iron:20:4:True"
                recipe_parts: list[str] = []
                for rm in re.finditer(r"^\s*-\s*([A-Za-z0-9_\-.]+)\s*:\s*([0-9]+)\s*:", txt, re.MULTILINE):
                    try:
                        recipe_parts.append(f"{rm.group(1)} x{int(rm.group(2))}")
                    except Exception:
                        pass
                if recipe_parts and not dd.get('recipe'):
                    dd['recipe'] = ', '.join(recipe_parts)
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
        actions_btn = ttk.Menubutton(top, text="Actions", style="Action.TButton")
        actions_menu = tk.Menu(actions_btn, tearoff=False)
        actions_menu.add_command(label="Save", command=self._persist_state)
        actions_menu.add_separator()
        actions_menu.add_command(label="Write to configuration file", command=self._write_to_config)
        actions_menu.add_separator()
        actions_menu.add_command(label="Export Items.md", command=self._export_items_mod_md)
        actions_menu.add_separator()
        actions_menu.add_command(label="Validate Skill YAML", command=self._validate_skill_yaml)
        actions_btn["menu"] = actions_menu
        actions_btn.pack(side=tk.LEFT, padx=(0, 6))
        # Consolidated export button with options dialog
        ttk.Button(top, text="Export…", style="Action.TButton", command=self._open_export_dialog).pack(side=tk.LEFT, padx=(0, 6))
        # Paste levels button
        ttk.Button(top, text="Paste Levels…", style="Action.TButton", command=self._open_paste_levels_dialog).pack(side=tk.LEFT, padx=(0, 6))
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
        # Craftable filter
        self.craftable_only_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(search_frame, text="Craftable only", variable=self.craftable_only_var, command=self._filter_rows).pack(side=tk.LEFT, padx=(12, 0))

        # Tree with left-most icon/star column and columns ordered for readability
        # Put Skill Level next to Item for straight-across reading, and show Mod
        columns = ("item", "mod", "skill_level", "station", "station_lvl", "stats", "in_yaml")
        self.tree = ttk.Treeview(self.root, columns=columns, show="tree headings", selectmode='extended')
        self.tree.heading("#0", text="★")
        self.tree.heading("item", text="Item")
        self.tree.heading("mod", text="Mod")
        self.tree.heading("skill_level", text="Skill Level")
        self.tree.heading("station", text="Crafting Station")
        self.tree.heading("station_lvl", text="Station Lvl")
        self.tree.heading("stats", text="Stats")
        self.tree.heading("in_yaml", text="In Skill YAML")
        self.tree.column("#0", width=36, stretch=False)
        self.tree.column("item", width=360, stretch=False)
        self.tree.column("mod", width=160, stretch=False)
        self.tree.column("skill_level", width=110, stretch=False, anchor='center')
        self.tree.column("station", width=200, stretch=False)
        self.tree.column("station_lvl", width=110, stretch=False, anchor='center')
        self.tree.column("stats", width=300, stretch=False)
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
            # Tag to color inferred/guessed levels
            self.tree.tag_configure("guessed", foreground="#ffd966")
        except Exception:
            pass

        # Remember base column widths to scale on zoom
        self._base_tree_col_widths = {"#0": 36, "item": 360, "mod": 160, "skill_level": 110, "station": 200, "station_lvl": 110, "stats": 300, "in_yaml": 100}
        # Flex weights for responsive layout (A+C mix): distribute extra width to these
        self._flex_weights = {"item": 3.0, "station": 1.5, "stats": 2.0}

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
        self.menu.add_separator()
        self.menu.add_command(label="Item Details…", command=self._open_item_details)

        # Keyboard zoom shortcuts
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.reset_zoom())
        self.root.bind("<Return>", lambda e: self._open_item_details())

    def _open_paste_levels_dialog(self) -> None:
        """Open a dialog with a multiline text box to paste lines: 'English Name, Level'.

        Only items with an empty Skill Level cell and without a manual level set will be updated.
        """
        dlg = tk.Toplevel(self.root)
        dlg.title("Paste Levels")
        dlg.configure(bg=self.colors["bg"])
        dlg.geometry("720x420")
        try:
            dlg.transient(self.root)
            dlg.grab_set()
        except Exception:
            pass
        frame = ttk.Frame(dlg)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        msg = (
            "Paste lines in the format: Name and Level\n"
            "Examples:\n"
            "Iron battleaxe, 3\nSilver Battlehammer — 5\n\n"
            "Only rows with no Skill Level set will be changed.\n"
            "Press Ctrl+Enter to apply; Esc to cancel."
        )
        lbl = ttk.Label(frame, text=msg, justify=tk.LEFT)
        lbl.pack(anchor=tk.W)
        text = tk.Text(frame, height=16, wrap=tk.NONE)
        text.pack(fill=tk.BOTH, expand=True, pady=(6, 6))
        try:
            text.focus_set()
        except Exception:
            pass
        btns = ttk.Frame(frame)
        btns.pack(fill=tk.X)
        def on_apply():
            content = text.get("1.0", tk.END)
            self._apply_pasted_levels(content)
            dlg.destroy()
        def on_cancel():
            dlg.destroy()
        ttk.Button(btns, text="Apply (Ctrl+Enter)", style="Action.TButton", command=on_apply).pack(side=tk.LEFT)
        ttk.Button(btns, text="Cancel", style="Action.TButton", command=on_cancel).pack(side=tk.RIGHT)
        try:
            text.bind("<Control-Return>", lambda e: (on_apply(), "break"))
            dlg.bind("<Control-Return>", lambda e: (on_apply(), "break"))
            text.bind("<Control-KP_Enter>", lambda e: (on_apply(), "break"))
            dlg.bind("<Control-KP_Enter>", lambda e: (on_apply(), "break"))
            dlg.bind("<Escape>", lambda e: (on_cancel(), "break"))
        except Exception:
            pass

    def _apply_pasted_levels(self, raw_text: str) -> None:
        """Parse pasted text and update manual skill levels by matching English name to items.

        - Lines must be 'English Name, Level'. Extra spaces and quotes are trimmed.
        - Case-insensitive match against VNEI 'Localized Name'.
        - Only updates items with no manual level set and an empty Skill Level cell.
        """
        if not raw_text or not raw_text.strip():
            return
        # Build lookup: english(localized) -> list[prefab]
        try:
            meta = self.vnei_index.load_item_metadata()
        except Exception:
            meta = {}
        name_to_prefabs: dict[str, list[str]] = {}
        for prefab, m in (meta or {}).items():
            name = (m.get('localized') or '').strip()
            if not name:
                continue
            key = name.casefold()
            name_to_prefabs.setdefault(key, []).append(prefab)

        # Determine full set of rows to iterate over (all, not just visible)
        iids = getattr(self, 'all_item_iids', None)
        if not iids:
            iids = list(self.tree.get_children(""))

        updated_count = 0
        unknown_names: list[str] = []
        ambiguous: list[str] = []
        fuzzy_matched: list[tuple[str, str]] = []  # (input_name, prefab)
        # Cache current manual map
        manual_levels: dict[str, str] = self.state.data.setdefault("skill_levels", {})
        # Track which prefabs were inferred (yellow tag)
        guessed_levels: dict[str, bool] = self.state.data.setdefault("guessed_levels", {})

        # Helper: normalization and tokenization for fuzzy matching
        def normalize_string(s: str) -> str:
            s = (s or "").casefold().strip()
            # Remove quotes and extra decorations
            s = s.replace('★', '')
            # Keep alphanumerics and spaces
            s = re.sub(r"[^a-z0-9\s]", " ", s)
            s = re.sub(r"\s+", " ", s).strip()
            return s

        def tokenize(s: str) -> list[str]:
            return [t for t in normalize_string(s).split() if t]

        def parse_line(line: str) -> tuple[str | None, str | None]:
            if not line or not line.strip():
                return None, None
            s = line.strip()
            # Case 1: explicit comma separator
            if "," in s:
                left, right = s.split(",", 1)
                name = left.strip().strip('"').strip("'")
                # Trim trailing decorations like hyphen/en dash/em dash labels
                name = re.sub(r"\s*[-–—:]\s*.+$", "", name).strip()
                lvl_raw = right.strip()
                m = re.search(r"(-?\d+)", lvl_raw)
                lvl = m.group(1) if m else lvl_raw
                return (name if name else None), (lvl if lvl else None)
            # Case 2: free form — take the last integer as level, rest as name
            m = re.search(r"(-?\d+)\s*$", s)
            if m:
                lvl = m.group(1)
                name_part = s[:m.start()].strip()
                # Strip trailing separators between name and number
                name_part = re.sub(r"[\s,:–—-]+$", "", name_part)
                name = name_part.strip().strip('"').strip("'")
                return (name if name else None), (lvl if lvl else None)
            return None, None

        pairs: list[tuple[str, str]] = []
        for raw in raw_text.splitlines():
            name, lvl = parse_line(raw)
            if name and lvl:
                pairs.append((name, lvl))

        if not pairs:
            messagebox.showwarning("Paste Levels", "No valid 'Name, Level' lines found.")
            return

        # Build quick indices and an ordered list of visible rows for order-aware fuzzy matching
        prefab_to_iid: dict[str, str] = {}
        prefab_to_display_level: dict[str, str] = {}
        prefab_to_index: dict[str, int] = {}
        visible_rows: list[dict] = []
        for idx, iid in enumerate(iids):
            vals = self.tree.item(iid).get('values', [])
            if not vals:
                continue
            raw_label = str(vals[0])
            label = raw_label.replace("★ ", "").strip()
            # Extract display name and prefab from "Name (Prefab)"
            m_pref = re.search(r"\(([^)]+)\)$", label)
            if m_pref:
                prefab = m_pref.group(1)
                display_name = label[:label.rfind("(")].strip()
            else:
                prefab = label
                display_name = label
            prefab_to_iid[prefab] = iid
            prefab_to_index[prefab] = idx
            # skill level column is index 2
            try:
                prefab_to_display_level[prefab] = str(vals[2])
            except Exception:
                prefab_to_display_level[prefab] = ""
            visible_rows.append({
                "index": idx,
                "iid": iid,
                "prefab": prefab,
                "display_name": display_name,
                "display_norm": normalize_string(display_name),
                "display_tokens": tokenize(display_name),
            })

        def is_missing(prefab: str) -> bool:
            if prefab in manual_levels and str(manual_levels.get(prefab) or "").strip():
                return False
            disp = (prefab_to_display_level.get(prefab) or "").strip()
            return disp == ""

        def similarity_score(input_tokens: list[str], candidate_tokens: list[str]) -> float:
            if not input_tokens:
                return 0.0
            hits = 0
            cand_set = set(candidate_tokens)
            for t in input_tokens:
                if t in cand_set:
                    hits += 1
            return hits / max(1, len(input_tokens))

        # Track last matched index to respect order; start at first row
        last_matched_index: int | None = None
        assigned_prefabs: set[str] = set()

        for name, lvl in pairs:
            key = name.casefold()
            prefabs = name_to_prefabs.get(key, [])

            chosen_prefab: str | None = None
            chosen_index: int | None = None

            # Step A: exact match via metadata name
            if prefabs:
                candidates = [p for p in prefabs if is_missing(p) and p not in assigned_prefabs]
                if candidates:
                    if len(candidates) > 1:
                        ambiguous.append(name)
                        # Pick nearest to last matched index if possible
                        if last_matched_index is not None:
                            candidates.sort(key=lambda p: abs(prefab_to_index.get(p, 1_000_000) - last_matched_index))
                    chosen_prefab = candidates[0]
                    chosen_index = prefab_to_index.get(chosen_prefab)

            # Step B: fuzzy/window-based by visible order if not found
            if chosen_prefab is None:
                input_tokens = tokenize(name)
                # Determine window center
                center = last_matched_index if last_matched_index is not None else 0
                lo = max(0, center - 5)
                hi = min(len(visible_rows) - 1, center + 5)
                best_score = 0.0
                best: tuple[int, str] | None = None  # (index, prefab)
                for idx in range(lo, hi + 1):
                    row = visible_rows[idx]
                    prefab = row["prefab"]
                    if prefab in assigned_prefabs or not is_missing(prefab):
                        continue
                    score = similarity_score(input_tokens, row["display_tokens"])
                    if score > best_score or (score == best_score and best and abs(idx - center) < abs(best[0] - center)):
                        best_score = score
                        best = (idx, prefab)
                if best and best_score >= 0.6:
                    chosen_index, chosen_prefab = best
                    fuzzy_matched.append((name, chosen_prefab))

            if chosen_prefab is None:
                unknown_names.append(name)
                continue

            # Apply assignment
            manual_levels[chosen_prefab] = str(lvl).strip()
            iid = prefab_to_iid.get(chosen_prefab)
            if iid:
                vals = list(self.tree.item(iid).get('values', []))
                while len(vals) < 6:
                    vals.append("")
                vals[2] = str(lvl).strip()
                # If chosen by fuzzy/window step, mark guessed; exact metadata match remains untagged
                # Heuristic: we consider it guessed if it came from Step B
                was_fuzzy = any(chosen_prefab == pf for _n, pf in fuzzy_matched)
                if was_fuzzy:
                    guessed_levels[chosen_prefab] = True
                    # add 'guessed' tag to row
                    try:
                        cur_tags = tuple(self.tree.item(iid).get('tags', []) or [])
                        if 'guessed' not in cur_tags:
                            self.tree.item(iid, tags=cur_tags + ('guessed',), values=tuple(vals))
                        else:
                            self.tree.item(iid, values=tuple(vals))
                    except Exception:
                        self.tree.item(iid, values=tuple(vals))
                else:
                    guessed_levels.pop(chosen_prefab, None)
                    self.tree.item(iid, values=tuple(vals))
            updated_count += 1
            assigned_prefabs.add(chosen_prefab)
            if chosen_index is not None:
                last_matched_index = chosen_index

        self.state.save()
        msg_parts = [f"Updated {updated_count} item(s)."]
        if unknown_names:
            msg_parts.append(f"{len(unknown_names)} name(s) not found: " + ", ".join(sorted(set(unknown_names))[:10]) + ("…" if len(set(unknown_names)) > 10 else ""))
        if ambiguous:
            msg_parts.append(f"{len(set(ambiguous))} ambiguous name(s) matched multiple items (all missing were updated).")
        if fuzzy_matched:
            msg_parts.append(f"{len(fuzzy_matched)} fuzzy-matched by nearby order.")
        self.status.set(" ".join(msg_parts))
        messagebox.showinfo("Paste Levels", "\n".join(msg_parts))

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
            flex_cols = [c for c in ("item", "station", "stats") if c in self._base_tree_col_widths]
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
            try:
                self.tree.column("stats", width=scaled.get("stats", 300))
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

    def _open_item_details(self) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = list(self.tree.item(iid).get('values', []))
        if not vals:
            return
        # Extract prefab from "Name (Prefab)"
        label = str(vals[0])
        prefab = self._extract_prefab_name(label)

        # Gather sources
        try:
            meta = self.vnei_index.load_item_metadata()
        except Exception:
            meta = {}
        try:
            wacky = self.wacky_index.scan()
        except Exception:
            wacky = {}
        try:
            yaml_levels = self.skill_config.load_blacksmithing_levels()
        except Exception:
            yaml_levels = {}
        manual_levels: dict[str, str] = self.state.data.get("skill_levels", {})

        mrow = meta.get(prefab, {}) or {}
        wrow = wacky.get(prefab, {}) or {}

        name = mrow.get('localized') or prefab
        mod = mrow.get('source_mod') or ''
        st = wrow.get('station') or vals[3] if len(vals) >= 4 else ''
        sl = wrow.get('station_level') or vals[4] if len(vals) >= 5 else ''
        lvl = manual_levels.get(prefab) or yaml_levels.get(prefab) or ''
        recipe = wrow.get('recipe') or []
        stats = wrow.get('stats') or {}
        tier = wrow.get('tier')
        wl = wrow.get('world_level')
        rarity = wrow.get('rarity')

        # Build a compact, readable text
        lines = []
        lines.append(f"Item: {name} ({prefab})")
        if mod:
            lines.append(f"Mod: {mod}")
        if st:
            lines.append(f"Station: {st}{(' Lvl ' + str(sl)) if str(sl) else ''}")
        if str(lvl):
            lines.append(f"Blacksmithing: {lvl}")
        if tier is not None:
            lines.append(f"Tier: {tier}")
        if wl is not None:
            lines.append(f"WorldLevel: {wl}")
        if rarity:
            lines.append(f"Rarity: {rarity}")
        if recipe:
            parts = [f"{a} x{b}" for a, b in recipe]
            lines.append("Recipe: " + ", ".join(parts))
        if stats:
            s_parts = []
            if 'damage_total' in stats:
                s_parts.append(f"DMG {stats['damage_total']}")
            if 'armor' in stats:
                s_parts.append(f"Armor {stats['armor']}")
            if 'block' in stats:
                s_parts.append(f"Block {stats['block']}")
            if 'weight' in stats:
                s_parts.append(f"Wt {stats['weight']}")
            if 'durability' in stats:
                s_parts.append(f"Dur {stats['durability']}")
            if s_parts:
                lines.append("Stats: " + ", ".join(s_parts))

        detail_text = "\n".join(lines)

        # Show dialog
        win = tk.Toplevel(self.root)
        win.title("Item Details")
        win.configure(bg=self.colors.get("bg", "#2e2b23"))
        win.geometry("520x360")
        txt = tk.Text(win, bg=self.colors.get("panel", "#3b352a"), fg=self.colors.get("text", "#e8e2d0"), wrap=tk.WORD, font=self.font)
        txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        txt.insert('1.0', detail_text)
        txt.config(state=tk.DISABLED)
        btns = ttk.Frame(win)
        btns.pack(fill=tk.X, padx=8, pady=(0,8))
        def copy():
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(detail_text)
            except Exception:
                pass
        ttk.Button(btns, text="Copy", style="Action.TButton", command=copy).pack(side=tk.RIGHT)

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

    def _extract_prefab_name(self, item_label: str) -> str:
        """Extract the clean prefab name from an item label.
        
        Handles formats like:
        - "Name (PrefabName)"
        - "Name: 'Description' (PrefabName)"
        - "PrefabName" (no parentheses)
        """
        # Remove star prefix if present
        label = item_label.lstrip('★ ').strip()
        
        # Look for parentheses at the end
        m = re.search(r"\(([^)]+)\)$", label)
        if m:
            prefab = m.group(1).strip()
            # Remove any quotes that might be around the prefab name
            prefab = prefab.strip("'\"")
            return prefab
        
        # If no parentheses, return the whole label
        return label

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
        # Determine prefab key from label "Name (Prefab)"
        label_for_row = str(vals[0])
        current_item = self._extract_prefab_name(label_for_row)
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
                # Persist manual level keyed by prefab internal name so it survives refresh
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
            prefab = self._extract_prefab_name(item_label)
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
        # Also scan config files for additional recipe/station hints
        cfg_info = self.wacky_index.scan_configs_for_recipes_and_unlocks(self.config_dir)
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
            guessed_levels: dict[str, bool] = self.state.data.setdefault("guessed_levels", {})
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
            # Heuristic craftable: color item green if station or recipe is known
            wrow_tmp = (wacky.get(item, {}) or {})
            crow_tmp = (cfg_info.get(item, {}) or {})
            has_station = bool(
                station or
                (items_rich.get(item, {}).get('station') or "") or
                (wrow_tmp.get('station') or "") or
                (crow_tmp.get('station') or "")
            )
            has_recipe = bool(wrow_tmp.get('recipe') or crow_tmp.get('recipe'))
            craftable = bool(has_station or has_recipe)
            # Pull station/station level & recipe from Wacky if present
            station_from_wacky = (
                (wacky.get(item, {}) or {}).get('station') or
                (crow_tmp.get('station') or "") or
                station or
                (items_rich.get(item, {}).get('station') or "")
            )
            station_lvl_from_wacky = (wacky.get(item, {}) or {}).get('station_level') or (crow_tmp.get('station_level') or "")
            
            # Build comprehensive stats string
            stats_parts = []
            
            # Get stats from VNEI
            vnei_stats = items_rich.get(item, {}).get('stats', '')
            if vnei_stats:
                stats_parts.append(f"VNEI: {vnei_stats}")
            
            # Get stats from Wacky
            wacky_stats = wrow_tmp.get('stats', {})
            if wacky_stats:
                wacky_parts = []
                for stat_key, stat_val in wacky_stats.items():
                    if stat_key == 'damage_breakdown':
                        wacky_parts.append(f"Dmg: {stat_val}")
                    elif stat_key == 'damage_total':
                        wacky_parts.append(f"DMG {stat_val}")
                    elif stat_key == 'armor':
                        wacky_parts.append(f"Armor {stat_val}")
                    elif stat_key == 'block':
                        wacky_parts.append(f"Block {stat_val}")
                    elif stat_key == 'weight':
                        wacky_parts.append(f"Wt {stat_val}")
                    elif stat_key == 'durability':
                        wacky_parts.append(f"Dur {stat_val}")
                    elif stat_key == 'speed':
                        wacky_parts.append(f"Spd {stat_val}")
                    elif stat_key == 'range':
                        wacky_parts.append(f"Rng {stat_val}")
                    elif stat_key == 'knockback':
                        wacky_parts.append(f"KB {stat_val}")
                    elif stat_key == 'backstab':
                        wacky_parts.append(f"BS {stat_val}")
                    elif stat_key == 'parry_force':
                        wacky_parts.append(f"PF {stat_val}")
                    elif stat_key == 'movement':
                        wacky_parts.append(f"Mov {stat_val}")
                    elif stat_key == 'stamina':
                        wacky_parts.append(f"Sta {stat_val}")
                    else:
                        wacky_parts.append(f"{stat_key.capitalize()} {stat_val}")
                
                if wacky_parts:
                    stats_parts.append(f"Wacky: {' | '.join(wacky_parts)}")
            
            # Combine stats
            stats_display = " | ".join(stats_parts) if stats_parts else ""
            
            # Build row tags
            row_tags: list[str] = []
            if craftable:
                row_tags.append("craftable")
            if guessed_levels.get(item):
                row_tags.append("guessed")

            item_kwargs = {
                "text": "",
                "values": (item_label, mod_name, level_str, station_from_wacky or "", str(station_lvl_from_wacky) if station_lvl_from_wacky else "", stats_display, "Yes" if in_yaml else "No"),
            }
            if img is not None:
                item_kwargs["image"] = img
            iid_new = self.tree.insert("", "end", tags=tuple(row_tags), **item_kwargs)
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
                prefab = self._extract_prefab_name(label)
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
            # Apply craftable-only flag using row tag
            try:
                if visible and getattr(self, 'craftable_only_var', None) and self.craftable_only_var.get():
                    tags = set(self.tree.item(iid).get('tags', []) or [])
                    if 'craftable' not in tags:
                        visible = False
            except Exception:
                pass
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

    def _open_export_dialog(self) -> None:
        """Open a small dialog to choose export columns and scope, then export to CSV or Markdown."""
        win = tk.Toplevel(self.root)
        win.title("Export Options")
        win.configure(bg=self.colors.get("bg", "#2e2b23"))
        pad = {"padx": 8, "pady": 6}

        # Scope
        scope_frame = ttk.LabelFrame(win, text="Scope")
        scope_frame.pack(fill=tk.X, **pad)
        only_visible_var = tk.BooleanVar(value=True)
        craftable_only_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(scope_frame, text="Export only visible rows", variable=only_visible_var).pack(anchor='w', padx=8, pady=2)
        ttk.Checkbutton(scope_frame, text="Export only craftable items", variable=craftable_only_var).pack(anchor='w', padx=8, pady=2)

        # Columns
        cols_frame = ttk.LabelFrame(win, text="Include Columns")
        cols_frame.pack(fill=tk.X, **pad)
        vars_map: dict[str, tk.BooleanVar] = {}
        def add_opt(key: str, label: str, default: bool) -> None:
            v = tk.BooleanVar(value=default)
            vars_map[key] = v
            ttk.Checkbutton(cols_frame, text=label, variable=v).pack(side=tk.LEFT, padx=6, pady=2)
        # Always include prefab
        add_opt('name', 'Localized Name', True)
        add_opt('mod', 'Mod', True)
        add_opt('station', 'Station', True)
        add_opt('station_level', 'Station Lvl', True)
        add_opt('skill_level', 'Skill Level', True)
        add_opt('recipe', 'Recipe', True)
        # Stats group
        stats_row = ttk.Frame(cols_frame)
        stats_row.pack(fill=tk.X)
        stats_label = ttk.Label(stats_row, text="Stats:")
        stats_label.pack(side=tk.LEFT, padx=(6, 0))
        stats_vars: dict[str, tk.BooleanVar] = {}
        for k, lab in [("damage_total", "DMG"), ("armor", "Armor"), ("block", "Block"), ("weight", "Weight"), ("durability", "Durability")]:
            b = tk.BooleanVar(value=(k in ("damage_total", "armor")))
            stats_vars[k] = b
            ttk.Checkbutton(stats_row, text=lab, variable=b).pack(side=tk.LEFT, padx=6)
        
        # Additional stats row
        stats_row2 = ttk.Frame(cols_frame)
        stats_row2.pack(fill=tk.X)
        for k, lab in [("speed", "Speed"), ("range", "Range"), ("knockback", "Knockback"), ("backstab", "Backstab"), ("parry_force", "Parry Force"), ("movement", "Movement"), ("stamina", "Stamina")]:
            b = tk.BooleanVar(value=False)
            stats_vars[k] = b
            ttk.Checkbutton(stats_row2, text=lab, variable=b).pack(side=tk.LEFT, padx=6)
        
        # Other fields
        lower_row = ttk.Frame(cols_frame)
        lower_row.pack(fill=tk.X)
        add_opt('tier', 'Tier', False)
        add_opt('world_level', 'World Level', False)
        add_opt('rarity', 'Rarity', False)

        # Format
        fmt_frame = ttk.LabelFrame(win, text="Format")
        fmt_frame.pack(fill=tk.X, **pad)
        format_var = tk.StringVar(value='csv')
        ttk.Radiobutton(fmt_frame, text="CSV", value='csv', variable=format_var).pack(side=tk.LEFT, padx=8)
        ttk.Radiobutton(fmt_frame, text="Markdown Table", value='md', variable=format_var).pack(side=tk.LEFT, padx=8)

        # Buttons
        btns = ttk.Frame(win)
        btns.pack(fill=tk.X, **pad)
        def do_export():
            try:
                # Determine items to export
                if only_visible_var.get():
                    # Visible rows are those attached to root
                    visible_iids = list(self.tree.get_children(""))
                    items: list[str] = []
                    for iid in visible_iids:
                        vals = list(self.tree.item(iid).get('values', []))
                        if not vals:
                            continue
                        label = str(vals[0]).replace("★ ", "")
                        prefab = self._extract_prefab_name(label)
                        items.append(prefab)
                else:
                    items = sorted(self.vnei_index.load_items().keys(), key=lambda s: s.lower())

                # Optional craftable filter
                if craftable_only_var.get():
                    wacky = self.wacky_index.scan()
                    items_rich = self.vnei_index.load_items_with_stats()
                    filtered: list[str] = []
                    for it in items:
                        st = (wacky.get(it, {}) or {}).get('station') or (items_rich.get(it, {}) or {}).get('station') or ''
                        rec = (wacky.get(it, {}) or {}).get('recipe') or []
                        if st or rec:
                            filtered.append(it)
                    items = filtered

                # Load sources once
                meta = self.vnei_index.load_item_metadata()
                wacky = self.wacky_index.scan()
                levels_yaml = self.skill_config.load_blacksmithing_levels()
                manual_levels: dict[str, str] = self.state.data.get("skill_levels", {})

                # Build header
                headers = ["Prefab"]
                if vars_map['name'].get(): headers.append("Name")
                if vars_map['mod'].get(): headers.append("Mod")
                if vars_map['station'].get(): headers.append("Station")
                if vars_map['station_level'].get(): headers.append("Station Lvl")
                if vars_map['skill_level'].get(): headers.append("Skill Level")
                if vars_map['recipe'].get(): headers.append("Recipe")
                # Stats headers
                stats_order = [
                    ("damage_total", "DMG"), ("armor", "Armor"), ("block", "Block"), ("weight", "Weight"), ("durability", "Durability"),
                    ("speed", "Speed"), ("range", "Range"), ("knockback", "Knockback"), ("backstab", "Backstab"), 
                    ("parry_force", "Parry Force"), ("movement", "Movement"), ("stamina", "Stamina")
                ]
                for key, lab in stats_order:
                    if stats_vars[key].get():
                        headers.append(lab)
                if vars_map['tier'].get(): headers.append("Tier")
                if vars_map['world_level'].get(): headers.append("World Level")
                if vars_map['rarity'].get(): headers.append("Rarity")

                # Choose file
                defext = '.csv' if format_var.get() == 'csv' else '.md'
                filetypes = [("CSV", "*.csv")] if defext == '.csv' else [("Markdown", "*.md")]
                save_path = filedialog.asksaveasfilename(title="Save Export", defaultextension=defext, filetypes=filetypes, initialdir=str(self.workspace))
                if not save_path:
                    return

                # Write rows
                rows: list[list[str]] = []
                for it in items:
                    mrow = meta.get(it, {}) or {}
                    wrow = wacky.get(it, {}) or {}
                    row: list[str] = [it]
                    if vars_map['name'].get(): row.append(mrow.get('localized', ''))
                    if vars_map['mod'].get(): row.append(mrow.get('source_mod', ''))
                    if vars_map['station'].get(): row.append(wrow.get('station') or '')
                    if vars_map['station_level'].get(): row.append(str(wrow.get('station_level') or ''))
                    if vars_map['skill_level'].get():
                        lvl = (manual_levels.get(it) or levels_yaml.get(it) or '')
                        row.append(str(lvl))
                    if vars_map['recipe'].get():
                        rlist = wrow.get('recipe') or []
                        row.append(', '.join([f"{a} x{b}" for a, b in rlist]))
                    stx = wrow.get('stats') or {}
                    for key, _lab in stats_order:
                        if stats_vars[key].get():
                            row.append(str(stx.get(key) or ''))
                    if vars_map['tier'].get(): row.append(str(wrow.get('tier') or ''))
                    if vars_map['world_level'].get(): row.append(str(wrow.get('world_level') or ''))
                    if vars_map['rarity'].get(): row.append(str(wrow.get('rarity') or ''))
                    rows.append(row)

                if format_var.get() == 'csv':
                    try:
                        with open(save_path, 'w', encoding='utf-8', newline='') as f:
                            w = csv.writer(f)
                            w.writerow(headers)
                            for r in rows:
                                w.writerow(r)
                    except Exception as e:
                        messagebox.showerror("Export", f"Failed to write CSV: {e}")
                        return
                else:
                    # Markdown table
                    def esc(s: str) -> str:
                        return (s or '').replace('|', '\\|')
                    lines: list[str] = []
                    lines.append("| " + " | ".join([esc(h) for h in headers]) + " |")
                    lines.append("|" + "---|" * len(headers))
                    for r in rows:
                        lines.append("| " + " | ".join([esc(c) for c in r]) + " |")
                    try:
                        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                        Path(save_path).write_text("\n".join(lines) + "\n", encoding='utf-8', newline='\n')
                    except Exception as e:
                        messagebox.showerror("Export", f"Failed to write Markdown: {e}")
                        return

                messagebox.showinfo("Export", f"Exported {len(rows)} items to\n{save_path}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Export", f"Export failed: {e}")

        ttk.Button(btns, text="Cancel", style="Action.TButton", command=win.destroy).pack(side=tk.RIGHT)
        ttk.Button(btns, text="Export", style="Action.TButton", command=do_export).pack(side=tk.RIGHT, padx=(0, 6))

    def _validate_skill_yaml(self) -> None:
        """Check Detalhes.ItemRequiresSkillLevel.yml for valid, known prefabs.

        - Flags entries whose `PrefabName` does not match a known internal item name.
        - Suggests corrections based on VNEI item list and fuzzy token match.
        - Shows a summary dialog with counts and first N issues.
        """
        try:
            # Load known item prefabs from VNEI
            known_items = set(self.vnei_index.load_items().keys())
            # Parse skill YAML blocks
            rules = self.skill_config.load_blacksmithing_rules()  # maps prefab -> rule dict
            # Collect suspect entries
            unknown: list[str] = []
            suggestions: list[tuple[str, str]] = []
            def normalize(s: str) -> str:
                s = (s or '').casefold().strip()
                s = re.sub(r"[^a-z0-9\s]", " ", s)
                s = re.sub(r"\s+", " ", s).strip()
                return s
            def tokens(s: str) -> list[str]:
                return [t for t in normalize(s).split() if t]
            def score(a: list[str], b: list[str]) -> float:
                if not a:
                    return 0.0
                bs = set(b)
                hit = sum(1 for t in a if t in bs)
                return hit / max(1, len(a))
            for prefab in sorted(rules.keys(), key=lambda s: s.lower()):
                if prefab in known_items:
                    continue
                # Try to recover possible real prefab from a label like "Name (Prefab)"
                m = re.search(r"\(([^)]+)\)$", prefab)
                candidate = m.group(1) if m else prefab
                if candidate in known_items:
                    suggestions.append((prefab, candidate))
                    continue
                # Fuzzy suggestion by tokens over known items
                a = tokens(prefab)
                best = None
                best_score = 0.0
                for k in known_items:
                    sc = score(a, tokens(k))
                    if sc > best_score:
                        best_score = sc
                        best = k
                unknown.append(prefab)
                if best_score >= 0.6 and best:
                    suggestions.append((prefab, best))
            # Build report
            lines: list[str] = []
            lines.append(f"Checked {len(rules)} YAML entries against {len(known_items)} known prefabs.")
            if not unknown and not suggestions:
                lines.append("All PrefabName entries appear valid.")
            else:
                if suggestions:
                    lines.append(f"Suggestions ({min(20, len(suggestions))} shown):")
                    for old, new in suggestions[:20]:
                        lines.append(f"  {old}  →  {new}")
                if unknown:
                    lines.append(f"Unknown (no good suggestion) ({min(20, len(unknown))} shown):")
                    for pf in unknown[:20]:
                        lines.append(f"  {pf}")
            messagebox.showinfo("Validate Skill YAML", "\n".join(lines))
        except Exception as e:
            messagebox.showerror("Validate Skill YAML", f"Validation failed: {e}")

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
            base_prefab = self._extract_prefab_name(plain)
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
            base_prefab = self._extract_prefab_name(plain)
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
            base_prefab = self._extract_prefab_name(plain)
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
        - If an item already exists, update its Blacksmithing Level instead of appending a duplicate.
        - Handles multiple formats and edge cases in existing YAML.
        """
        # Always write to the default Detalhes file in config directory
        target = self.config_dir / "Detalhes.ItemRequiresSkillLevel.yml"
        try:
            existing_text = target.read_text(encoding='utf-8') if target.exists() else ""
        except Exception:
            existing_text = ""

        # Enhanced duplicate detection - parse existing items more thoroughly
        existing_items: set[str] = set()
        existing_blocks: dict[str, tuple[int, int]] = {}  # item -> (start_line, end_line)
        
        # Parse existing YAML more comprehensively
        lines = existing_text.splitlines()
        current_item = None
        current_start = 0
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Detect new item block
            m = re.match(r"^\s*-\s*PrefabName:\s*([A-Za-z0-9_\-\.]+)\s*$", line)
            if m:
                # Save previous item block if exists
                if current_item:
                    existing_blocks[current_item] = (current_start, i)
                
                # Start new item block
                current_item = m.group(1)
                current_start = i
                existing_items.add(current_item)
        
        # Save last item block
        if current_item:
            existing_blocks[current_item] = (current_start, len(lines))

        # Collect desired writes from UI state
        levels_map: dict[str, str] = self.state.data.get("skill_levels", {})
        
        # Enhanced helper: update Level inside an existing PrefabName block
        def _update_level_in_text(text: str, item_name: str, new_level: str) -> tuple[str, bool]:
            try:
                # More robust pattern matching
                block_pat = rf"(?ms)^-\s*PrefabName:\s*{re.escape(item_name)}\s*(?P<body>(?:\n(?!-\s*PrefabName:).*)*)"
                bm = re.search(block_pat, text)
                if not bm:
                    return text, False
                
                body = bm.group('body')
                
                # Find Blacksmithing skill block - handle multiple formats
                skill_patterns = [
                    r"(?ms)(^\s*-\s*Skill\s*:\s*Blacksmithing\s*$)(?P<blk>(?:\n\s+.*)*)",
                    r"(?ms)(^\s*Skill\s*:\s*Blacksmithing\s*$)(?P<blk>(?:\n\s+.*)*)",
                ]
                
                for skill_pat in skill_patterns:
                    sm = re.search(skill_pat, body)
                    if sm:
                        blk = sm.group('blk')
                        
                        # Look for Level field in various formats
                        level_patterns = [
                            r"(^\s*Level\s*:\s*)(\d+)",
                            r"(^\s*level\s*:\s*)(\d+)",
                            r"(^\s*Level\s*:\s*)(\d+\.\d+)",
                        ]
                        
                        for lvl_pat in level_patterns:
                            lm = re.search(lvl_pat, blk, re.MULTILINE)
                            if lm:
                                cur_lvl = lm.group(2)
                                if cur_lvl == str(new_level):
                                    return text, False  # No change needed
                                
                                # Update the level
                                blk_new = re.sub(lvl_pat, rf"\\g<1>{int(new_level)}", blk, count=1, flags=re.MULTILINE)
                                body_new = body[:sm.start('blk')] + blk_new + body[sm.end('blk'):]
                                text_new = text[:bm.start('body')] + body_new + text[bm.end('body'):]
                                return text_new, True
                
                # If no existing skill block found, add one
                if not any(re.search(sp, body) for sp in skill_patterns):
                    # Add Blacksmithing skill block to existing item
                    skill_block = f"\n    - Skill: Blacksmithing\n      Level: {int(new_level)}\n      BlockCraft: true\n      BlockEquip: false\n      EpicMMO: false\n      ExhibitionName: "
                    
                    # Find where to insert (after Requirements: line)
                    req_match = re.search(r"^\s*Requirements\s*:\s*$", body, re.MULTILINE)
                    if req_match:
                        insert_pos = req_match.end()
                        body_new = body[:insert_pos] + skill_block + body[insert_pos:]
                        text_new = text[:bm.start('body')] + body_new + text[bm.end('body'):]
                        return text_new, True
                
                return text, False
            except Exception as e:
                print(f"Error updating level for {item_name}: {e}")
                return text, False

        # Enhanced helper: remove duplicate entries
        def _remove_duplicate_entries(text: str, item_name: str) -> str:
            """Remove all but the first occurrence of an item entry."""
            try:
                # Find all occurrences of this item
                pattern = rf"(?ms)^-\s*PrefabName:\s*{re.escape(item_name)}\s*(?:\n(?!-\s*PrefabName:).*)*"
                matches = list(re.finditer(pattern, text))
                
                if len(matches) > 1:
                    # Keep only the first occurrence, remove the rest
                    result = text
                    # Remove from last to first to maintain positions
                    for match in reversed(matches[1:]):
                        result = result[:match.start()] + result[match.end():]
                    return result
                
                return text
            except Exception:
                return text

        to_write: list[tuple[str, str]] = []  # (item, level)
        updated_count = 0
        removed_duplicates = 0
        updated_items: list[str] = []  # Track which items were updated
        
        for item, level in levels_map.items():
            level_str = str(level).strip()
            if not level_str:
                continue
                
            if item in existing_items:
                # Remove any duplicate entries first
                existing_text = _remove_duplicate_entries(existing_text, item)
                
                # Update in place if different
                existing_text, changed = _update_level_in_text(existing_text, item, level_str)
                if changed:
                    updated_count += 1
                    updated_items.append(item)
                continue
            else:
                # Check for case-insensitive matches
                item_lower = item.lower()
                found_case_variant = False
                for existing_item in existing_items:
                    if existing_item.lower() == item_lower:
                        # Remove duplicates and update the existing one
                        existing_text = _remove_duplicate_entries(existing_text, existing_item)
                        existing_text, changed = _update_level_in_text(existing_text, existing_item, level_str)
                        if changed:
                            updated_count += 1
                            updated_items.append(existing_item)
                        found_case_variant = True
                        break
                
                if found_case_variant:
                    continue
                    
            to_write.append((item, level_str))

        if not to_write and updated_count == 0:
            messagebox.showinfo("Write", "No changes to write. No entries were updated and no new entries were added.")
            return

        # Build YAML chunks for new items
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

        new_text = existing_text.rstrip()
        if chunks:
            new_text += ("\n\n" if new_text.strip() else "") + "\n".join(chunks) + "\n"

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(new_text, encoding='utf-8', newline='\n')
            
            # Build comprehensive status message
            message_parts = []
            if updated_count > 0:
                if updated_count == 1:
                    message_parts.append(f"Updated 1 entry: {updated_items[0]}")
                else:
                    # Show first few entries, then count the rest
                    if len(updated_items) <= 5:
                        entries_list = ", ".join(updated_items)
                        message_parts.append(f"Updated {updated_count} entries: {entries_list}")
                    else:
                        entries_list = ", ".join(updated_items[:3])
                        remaining = len(updated_items) - 3
                        message_parts.append(f"Updated {updated_count} entries: {entries_list} and {remaining} more")
            else:
                # No entries were updated
                message_parts.append("No entries were updated")
                
            if to_write:
                if len(to_write) == 1:
                    message_parts.append(f"Added 1 entry: {to_write[0][0]}")
                else:
                    message_parts.append(f"Added {len(to_write)} entries")
            if removed_duplicates > 0:
                message_parts.append(f"Removed {removed_duplicates} duplicate entr{'y' if removed_duplicates==1 else 'ies'}")
            
            message = f"{' and '.join(message_parts)} to\n{target}"
            messagebox.showinfo("Write", message)
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


