#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valheim Config Suite — v2
- Clear Revert Preview with colorized diff & metadata
- Automatic Backups + Restore Last Backup
- Bulk operations (multi-select Revert / Accept)
- Status & path filters; +N/-N summary
- Context menu (Open, Reveal, Copy Path, Revert, Accept, Restore)
- Commit messages for Accept
- Simple Profiles in Settings

Run:
python valheim_config_suite_v2.py --config "<BepInEx/config>" --vnei "<VNEI-Export>" --wdbulk "<wackyDatabase-BulkYML>"
"""
import os, sys, json, csv, re, shutil, threading, queue, hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import tkinter.font as tkfont

# ---------- Utilities ----------
def atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding=encoding, newline="\n")
    try:
        if path.exists(): os.replace(tmp, path)
        else: tmp.rename(path)
    finally:
        if tmp.exists():
            try: tmp.unlink()
            except Exception: pass

def read_text_safely(path: Path, max_bytes: int = 10 * 1024 * 1024) -> str:
    try:
        if not path.exists(): return ""
        if path.stat().st_size > max_bytes: return f"[File too large: {path.stat().st_size} bytes]"
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        try: return path.read_text(encoding="latin-1", errors="replace")
        except Exception: return ""

def sha256_of_file(path: Path) -> str:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
        return h.hexdigest()
    except Exception: return ""

def open_external(path: Path):
    try:
        if sys.platform.startswith("win"): os.startfile(str(path))
        elif sys.platform == "darwin":
            import subprocess; subprocess.Popen(["open", str(path)])
        else:
            import subprocess; subprocess.Popen(["xdg-open", str(path)])
    except Exception as e:
        messagebox.showerror("Open", f"Failed to open: {e}")

def reveal_in_folder(path: Path):
    try:
        if sys.platform.startswith("win"):
            import subprocess; subprocess.Popen(["explorer", "/select,", str(path)])
        elif sys.platform == "darwin":
            import subprocess; subprocess.Popen(["open", "-R", str(path)])
        else: open_external(path.parent)
    except Exception as e: messagebox.showerror("Reveal", f"Failed to reveal: {e}")

# ---------- Persistence ----------
@dataclass
class AppPrefs:
    config_root: str = ""
    vnei_root: str = ""
    wacky_bulk_root: str = ""
    ignored_dirs: list[str] = field(default_factory=lambda: ["wackydatabase-bulkyml"])
    use_hashing: bool = False
    theme: str = "dark"
    last_window: dict = field(default_factory=dict)
    backups_to_keep: int = 8
    profiles: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "AppPrefs":
        try:
            if path.exists(): return cls(**json.loads(path.read_text(encoding="utf-8")))
        except Exception: pass
        return cls()

    def save(self, path: Path) -> None:
        try: atomic_write_text(path, json.dumps(self.__dict__, indent=2, ensure_ascii=False))
        except Exception: pass

# ---------- Config Snapshots & Backups ----------
class ConfigSnapshot:
    def __init__(self, config_root: Path, store_dir: Path, ignored_dir_names: set[str], backups_to_keep: int = 8):
        self.config_root = config_root
        self.snapshots_dir = store_dir; self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.current_snapshot_file = self.snapshots_dir / "current_snapshot.json"
        self.initial_snapshot_file = self.snapshots_dir / "initial_snapshot.json"
        self.event_log_file = self.snapshots_dir / "event_log.jsonl"
        self.backups_dir = self.snapshots_dir / "backups"; self.backups_dir.mkdir(exist_ok=True)
        self._ignored = {s.lower() for s in ignored_dir_names}
        self._cache = {}
        self.backups_to_keep = backups_to_keep

    def _should_ignore(self, abs_path: Path) -> bool:
        try: rel_parts = abs_path.relative_to(self.config_root).parts
        except Exception: return False
        return any(p.lower() in self._ignored for p in rel_parts)

    def _file_meta(self, p: Path, with_hash: bool = False) -> dict:
        st = p.stat(); meta = {"size": st.st_size, "mtime": st.st_mtime, "hash": ""}
        if st.st_size <= 10 * 1024 * 1024 and with_hash: meta["hash"] = sha256_of_file(p)
        return meta

    def _log(self, action: str, ok: bool, file: str = "", details: Optional[dict] = None):
        rec = {"ts": datetime.now().isoformat(timespec="seconds"), "action": action, "file": file, "ok": ok, "details": details or {}}
        try:
            with open(self.event_log_file, "a", encoding="utf-8", newline="\n") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception: pass

    def _load_snapshot(self, which: str) -> dict:
        if which in self._cache: return self._cache[which]
        path = self.initial_snapshot_file if which == "initial" else self.current_snapshot_file
        if not path.exists():
            snap = {"timestamp": "", "session": "", "files": {}}
            self._cache[which] = snap; return snap
        try:
            snap = json.loads(path.read_text(encoding="utf-8")); self._cache[which] = snap; return snap
        except Exception as e:
            try: shutil.copy2(path, path.with_suffix(path.suffix + f".corrupted.{int(datetime.now().timestamp())}"))
            except Exception: pass
            self._log("load_snapshot", False, details={"which": which, "error": str(e)})
            snap = {"timestamp": "", "session": "", "files": {}}
            self._cache[which] = snap; return snap

    def create_snapshot(self, is_initial: bool, use_hash: bool = False) -> tuple[bool, str]:
        try:
            files = [p for p in self.config_root.rglob("*") if p.is_file() and not self._should_ignore(p)]
            snap = {"timestamp": datetime.now().isoformat(), "session": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), "files": {}}
            for p in files:
                rel = str(p.relative_to(self.config_root))
                snap["files"][rel] = self._file_meta(p, with_hash=use_hash)
                snap["files"][rel]["content"] = read_text_safely(p) if snap["files"][rel]["size"] <= 10*1024*1024 else f"[File too large: {snap['files'][rel]['size']} bytes]"
            target = self.initial_snapshot_file if is_initial else self.current_snapshot_file
            atomic_write_text(target, json.dumps(snap, indent=2, ensure_ascii=False))
            self._cache["initial" if is_initial else "current"] = snap
            self._log("snapshot", True, details={"initial": is_initial, "count": len(snap["files"])})
            return True, f"{'Initial' if is_initial else 'Current'} snapshot created with {len(snap['files'])} files."
        except Exception as e:
            self._log("snapshot", False, details={"initial": is_initial, "error": str(e)})
            return False, f"Failed to create snapshot: {e}"

    def list_changes(self, compare_against: str = "current") -> list[tuple[str, str]]:
        snap = self._load_snapshot(compare_against); recorded = snap.get("files", {}); recorded_keys = set(recorded.keys())
        on_disk = {}
        for p in self.config_root.rglob("*"):
            if p.is_file() and not self._should_ignore(p):
                rel = str(p.relative_to(self.config_root))
                try: st = p.stat(); on_disk[rel] = {"size": st.st_size, "mtime": st.st_mtime}
                except Exception: on_disk[rel] = {"size": -1, "mtime": -1}
        changes = []
        for rel, meta in on_disk.items():
            if rel not in recorded: changes.append(("A", rel))
            else:
                old = recorded[rel]
                if meta["size"] != old.get("size") or meta["mtime"] != old.get("mtime"): changes.append(("M", rel))
        for rel in recorded_keys - set(on_disk.keys()): changes.append(("D", rel))
        return changes

    # Backups
    def _backup_write(self, rel_path: str, content: str) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S"); dest = self.backups_dir / ts / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True); atomic_write_text(dest, content)
        folders = sorted([p for p in self.backups_dir.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
        for old in folders[self.backups_to_keep:]: 
            try: shutil.rmtree(old)
            except Exception: pass
        return dest

    def backup_current_file(self, rel_path: str) -> Optional[Path]:
        abs_target = self.config_root / rel_path
        if not abs_target.exists(): return None
        content = read_text_safely(abs_target); return self._backup_write(rel_path, content)

    def restore_last_backup(self, rel_path: str) -> tuple[bool, str]:
        folders = sorted([p for p in self.backups_dir.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
        for folder in folders:
            candidate = folder / rel_path
            if candidate.exists():
                try:
                    abs_target = self.config_root / rel_path
                    abs_target.parent.mkdir(parents=True, exist_ok=True)
                    atomic_write_text(abs_target, candidate.read_text(encoding="utf-8", errors="replace"))
                    self._log("restore_backup", True, rel_path, {"from": str(candidate)})
                    return True, f"Restored from {folder.name}."
                except Exception as e:
                    self._log("restore_backup", False, rel_path, {"error": str(e)})
                    return False, f"Restore failed: {e}"
        return False, "No backups found for this file."

    # Revert / Accept
    def revert_file(self, rel_path: str, from_snapshot: str = "current", do_backup: bool = True) -> tuple[bool, str]:
        snap = self._load_snapshot(from_snapshot); entry = snap.get("files", {}).get(rel_path)
        abs_target = self.config_root / rel_path
        try:
            if do_backup and abs_target.exists(): self.backup_current_file(rel_path)
            if not entry:
                if abs_target.exists(): abs_target.unlink()
                self._log("revert", True, rel_path, {"action": "delete"})
                return True, f"Deleted {rel_path} (not in {from_snapshot})."
            abs_target.parent.mkdir(parents=True, exist_ok=True)
            atomic_write_text(abs_target, entry.get("content",""))
            self._log("revert", True, rel_path, {"action": "write"})
            return True, f"Reverted {rel_path} to {from_snapshot}."
        except Exception as e:
            self._log("revert", False, rel_path, {"error": str(e)})
            return False, f"Failed to revert {rel_path}: {e}"

    def accept_into_baseline(self, rel_path: str, commit_message: str = "", do_backup: bool = True) -> tuple[bool, str]:
        initial = self._load_snapshot("initial"); abs_target = self.config_root / rel_path
        try:
            if do_backup and abs_target.exists(): self.backup_current_file(rel_path)
            if abs_target.exists():
                st = abs_target.stat()
                entry = {"size": st.st_size, "mtime": st.st_mtime, "hash": "", "content": read_text_safely(abs_target)}
                initial.setdefault("files", {})[rel_path] = entry; action = "Updated baseline for"
            else:
                if rel_path in initial.get("files", {}): del initial["files"][rel_path]
                action = "Removed from baseline"
            atomic_write_text(self.initial_snapshot_file, json.dumps(initial, indent=2, ensure_ascii=False))
            self._cache["initial"] = initial; self._log("accept_baseline", True, rel_path, {"action": action, "message": commit_message})
            return True, f"{action} {rel_path}."
        except Exception as e:
            self._log("accept_baseline", False, rel_path, {"error": str(e)}); return False, f"Failed to accept into baseline: {e}"

    def get_diff_text(self, rel_path: str, compare_against: str = "current") -> str:
        import difflib
        snap = self._load_snapshot(compare_against); entry = snap.get("files", {}).get(rel_path)
        abs_target = self.config_root / rel_path
        if not entry and not abs_target.exists(): return ""
        if not entry and abs_target.exists():
            new = read_text_safely(abs_target); return "New file\n" + "\n".join("+ " + ln for ln in new.splitlines())
        old = entry.get("content","") if entry else ""
        if not abs_target.exists(): return "Deleted file\n" + "\n".join("- " + ln for ln in old.splitlines())
        new = read_text_safely(abs_target)
        lines = list(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                          fromfile=f"a/{rel_path}", tofile=f"b/{rel_path}", lineterm=""))
        return "".join(lines)

# ---------- Item / Recipe / Stats Index ----------
class VNEIItemIndex:
    def __init__(self, vnei_dir: Path):
        self.vnei_dir = vnei_dir
        self.items_csv = vnei_dir / "VNEI.indexed.items.csv"
        self.items_txt = vnei_dir / "VNEI.indexed.items.txt"
        self.items_yml = vnei_dir / "VNEI.indexed.items.yml"

    def _guess_columns(self, headers: list[str]) -> tuple[Optional[str], Optional[str]]:
        lower = [h.lower().strip() for h in headers]
        item = None
        station = None
        for cand in ["internalname","item","name","id","prefab","prefabname"]:
            if cand in lower:
                item = headers[lower.index(cand)]
                break
        for cand in ["craftingstation","crafting_station","station","workbench","forge","table"]:
            if cand in lower:
                station = headers[lower.index(cand)]
                break
        if item is None and headers:
            item = headers[0]
        if station is None:
            for i, h in enumerate(lower):
                if "station" in h:
                    station = headers[i]
                    break
        return item, station

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

        if source.suffix.lower() in (".csv",".txt"):
            with open(source, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                lower = [h.lower().strip() for h in headers]
                item_col, _station_col = self._guess_columns(headers)
                for row in reader:
                    item = (row.get(item_col, "") or "").strip()
                    if not item:
                        continue
                    station, summary = summarize_row(row, lower)
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
                                block = float(block_key)
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
                    if not line or line.startswith("#"):
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
                    m_station = re.search(r"(crafting[_\s]?station|station)\s*:\s*([A-Za-z0-9_\-\. ]+)", line, re.IGNORECASE)
                    if m_station:
                        stash['station'] = m_station.group(2).strip()
                        continue
                    
                    # Enhanced damage detection
                    for dmg_key in ['damage', 'totaldamage', 'dmg', 'basedamage', 'slash', 'pierce', 'blunt', 'fire', 'frost', 'poison', 'lightning', 'spirit']:
                        m_dmg = re.search(re.escape(dmg_key) + r"\s*:\s*([0-9.\-]+)", line, re.IGNORECASE)
                        if m_dmg:
                            stash[dmg_key] = m_dmg.group(1)
                            break
                    
                    # Enhanced armor detection
                    for armor_key in ['armor', 'armour', 'defense', 'defence']:
                        m_arm = re.search(re.escape(armor_key) + r"\s*:\s*([0-9.]+)", line, re.IGNORECASE)
                        if m_arm:
                            stash[armor_key] = m_arm.group(1)
                            break
                    
                    # Enhanced block detection
                    for block_key in ['block', 'blockpower', 'parry']:
                        m_block = re.search(re.escape(block_key) + r"\s*:\s*([0-9.]+)", line, re.IGNORECASE)
                        if m_block:
                            stash[block_key] = m_block.group(1)
                            break
                    
                    # Other stats
                    for stat_key in ['weight', 'durability', 'tier', 'speed', 'range']:
                        m_stat = re.search(re.escape(stat_key) + r"\s*:\s*([0-9.\-]+)", line, re.IGNORECASE)
                        if m_stat:
                            stash[stat_key] = m_stat.group(1)
                            break
                
                # Don't forget the last item
                if current_item and stash:
                    station, summary = parse_yml_stats()
                    result[current_item] = {"station": station, "stats": summary}
                    
            except Exception as e:
                # Fallback to simple parsing if enhanced parsing fails
                text = read_text_safely(source)
                current = None
                station = ""
                stats = ""
                line_items = {}
                for raw in text.splitlines():
                    line = raw.strip()
                    if not line or line.startswith("#"):
                        continue
                    m_item = re.search(r"(name|item|internal|prefab)\s*:\s*([A-Za-z0-9_\-\.]+)", line, re.IGNORECASE)
                    if m_item:
                        if current:
                            line_items[current] = {"station": station, "stats": stats}
                        current = m_item.group(2)
                        station = ""
                        stats = ""
                        continue
                    m_station = re.search(r"(crafting[_\s]?station|station)\s*:\s*([A-Za-z0-9_\-\. ]+)", line, re.IGNORECASE)
                    if m_station:
                        station = m_station.group(2).strip()
                    m_dmg = re.search(r"(damage|totaldamage|dmg|basedamage)\s*:\s*([0-9.\-]+)", line, re.IGNORECASE)
                    m_arm = re.search(r"(armor|armour|defense|defence)\s*:\s*([0-9.]+)", line, re.IGNORECASE)
                    if m_arm:
                        v = float(m_arm.group(2))
                        stats = f"Armor {int(v) if float(v).is_integer() else round(v,1)}"
                    elif m_dmg:
                        v = float(m_dmg.group(2))
                        stats = f"DMG {int(v) if float(v).is_integer() else round(v,1)}"
                if current:
                    line_items[current] = {"station": station, "stats": stats}
                result.update(line_items)
        
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

    def _iter_yaml(self) -> list[Path]:
        if not self.bulk_root or not self.bulk_root.exists():
            return []
        files: list[Path] = []
        try:
            for sub in ("Items","Recipes","Creatures","Pickables"):
                p = self.bulk_root/sub
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
            s = re.sub(r"^(Recipe_)+","",s,flags=re.IGNORECASE)
            s = re.sub(r"_Recipe.*$","",s,flags=re.IGNORECASE)
            s = re.sub(r"^Recipe_","",s,flags=re.IGNORECASE)
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
            if ':' in line and not line.startswith('-'):
                k, v = line.split(':', 1)
                k, v = k.strip(), v.strip()
                if current is not None and indent == current_indent:
                    current[k] = v
                elif current is not None and indent > current_indent:
                    # Nested under current key
                    if current_key is not None:
                        current.setdefault(current_key, {})[k] = v
                else:
                    # New top-level entry
                    if current:
                        entries.append(current)
                    current = {k: v}
                    current_indent = indent
                    current_key = k
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
        for path in self._iter_yaml():
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
            
            # Enhanced speed detection
            speed = None
            for key in ["speed", "attackspeed", "attack_speed", "swingspeed", "swing_speed"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        speed = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced range detection
            range_val = None
            for key in ["range", "attackrange", "attack_range", "reach", "distance"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        range_val = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced knockback detection
            knockback = None
            for key in ["knockback", "knock_back", "pushback", "push_back", "force"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        knockback = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced backstab detection
            backstab = None
            for key in ["backstab", "back_stab", "backstabmultiplier", "back_stab_multiplier"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        backstab = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced parry force detection
            parry_force = None
            for key in ["parryforce", "parry_force", "parrybonus", "parry_bonus"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        parry_force = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced movement detection
            movement = None
            for key in ["movement", "movementspeed", "movement_speed", "movespeed", "move_speed"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        movement = float(v)
                        break
                    except Exception:
                        pass
            
            # Enhanced stamina detection
            stamina = None
            for key in ["stamina", "staminause", "stamina_use", "staminaconsumption", "stamina_consumption"]:
                v = find_num(re.escape(key))
                if v:
                    try:
                        stamina = float(v)
                        break
                    except Exception:
                        pass

            # Build stats dictionary
            if armor is not None:
                stats["armor"] = str(int(armor) if float(armor).is_integer() else round(armor,1))
            if dmg_total is not None:
                stats["damage_total"] = str(int(dmg_total) if float(dmg_total).is_integer() else round(dmg_total,1))
            if block is not None:
                stats["block"] = str(int(block) if float(block).is_integer() else round(block,1))
            if weight is not None:
                stats["weight"] = str(round(weight,1))
            if durability is not None:
                stats["durability"] = str(int(durability) if float(durability).is_integer() else round(durability,0))
            if speed is not None:
                stats["speed"] = str(round(speed,1))
            if range_val is not None:
                stats["range"] = str(int(range_val) if float(range_val).is_integer() else round(range_val,1))
            if knockback is not None:
                stats["knockback"] = str(int(knockback) if float(knockback).is_integer() else round(knockback,1))
            if backstab is not None:
                stats["backstab"] = str(int(backstab) if float(backstab).is_integer() else round(backstab,1))
            if parry_force is not None:
                stats["parry_force"] = str(int(parry_force) if float(parry_force).is_integer() else round(parry_force,1))
            if movement is not None:
                stats["movement"] = str(round(movement,1))
            if stamina is not None:
                stats["stamina"] = str(int(stamina) if float(stamina).is_integer() else round(stamina,1))

            # Recipe parsing
            recipe = []
            for rm in re.finditer(r"^-\s*(?:Item|Prefab|Name)\s*:\s*([A-Za-z0-9_\-.]+).*?(?:Amount|Qty|Quantity)\s*:\s*([0-9]+)", text, re.IGNORECASE|re.MULTILINE|re.DOTALL):
                recipe.append((rm.group(1), int(rm.group(2))))
            if not recipe:
                im = re.search(r"(Resources|Recipe|Requirements)\s*:\s*([^\n]+)", text, re.IGNORECASE)
                if im:
                    vals = im.group(2)
                    for part in vals.split(","):
                        part = part.strip()
                        if ":" in part:
                            mat, qty = [p.strip() for p in part.split(":",1)]
                            try:
                                recipe.append((mat,int(qty)))
                            except Exception:
                                pass

            # Add to info for each prefab candidate
            for prefab in prefab_candidates or {"(Unknown)"}:
                e = info.setdefault(prefab, {})
                if station:
                    e["station"] = station
                if station_level is not None:
                    e["station_level"] = station_level
                if tier is not None:
                    e["tier"] = tier
                if world_level is not None:
                    e["world_level"] = world_level
                if rarity:
                    e["rarity"] = rarity
                if stats:
                    e.setdefault("stats", {}).update(stats)
                if recipe:
                    e["recipe"] = recipe

        return info

    def load_item_metadata(self) -> dict[str, dict]:
        """Return mapping: item_name -> { 'localized': str, 'type': str, 'source_mod': str }.

        Pulls from CSV/TXT if available; falls back to empty strings.
        """
        meta: dict[str, dict] = {}
        source = None
        if self.bulk_root:
            for ext in ['.csv', '.txt']:
                for name in ['items', 'metadata', 'index']:
                    p = self.bulk_root / f"{name}{ext}"
                    if p.exists():
                        source = p
                        break
                if source:
                    break
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

        # 2) Scan other common config patterns
        for cfg_file in root.glob("*.cfg"):
            if cfg_file.name in ["Therzie.Wizardry.cfg"]:  # Already processed
                continue
            try:
                for raw in cfg_file.read_text(encoding='utf-8', errors='ignore').splitlines():
                    line = raw.strip()
                    if "=" not in line:
                        continue
                    # Look for recipe patterns
                    if any(keyword in line.lower() for keyword in ["recipe", "crafting", "cost"]):
                        try:
                            key, val = line.split('=', 1)
                            key, val = key.strip(), val.strip()
                            # Try to extract item name from key
                            if '(' in key and ')' in key:
                                name = key[key.find('(')+1:key.find(')')].strip()
                                if name and any(char.isalnum() for char in name):
                                    d = info.setdefault(name, {})
                                    if "cost" in key.lower() or "recipe" in key.lower():
                                        d['recipe'] = self.parse_crafting_costs(val)
                                    elif "station" in key.lower():
                                        d['station'] = val
                        except Exception:
                            pass
            except Exception:
                pass

        return info

# ---------- UI ----------
class RevertPreview(tk.Toplevel):
    def __init__(self, parent, rel_path: str, diff_text: str, meta_old: str, meta_new: str):
        super().__init__(parent)
        self.title(f"Revert Preview — {rel_path}")
        self.geometry("1000x650")
        self.resizable(True, True)
        self.result = None
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text=rel_path, font=("Consolas", 11, "bold")).pack(anchor="w", pady=(0,6))
        ttk.Label(frm, text=f"Snapshot: {meta_old}   |   Current: {meta_new}", foreground="#654735").pack(anchor="w", pady=(0,8))
        text = tk.Text(frm, wrap=tk.NONE, bg="#414535", fg="#b07b53", insertbackground="#b07b53")
        sy = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=text.yview)
        sx = ttk.Scrollbar(frm, orient=tk.HORIZONTAL, command=text.xview)
        text.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        sy.pack(side=tk.RIGHT, fill=tk.Y)
        sx.pack(side=tk.BOTTOM, fill=tk.X)
        text.tag_configure("add", foreground="#5f633e")
        text.tag_configure("del", foreground="#654735")
        text.tag_configure("hunk", foreground="#b07b53")
        for ln in diff_text.splitlines(True):
            tag = None
            if ln.startswith("+") and not ln.startswith("+++"):
                tag = "add"
            elif ln.startswith("-") and not ln.startswith("---"):
                tag = "del"
            elif ln.startswith("@@"):
                tag = "hunk"
            text.insert("end", ln, tag if tag else ())
        text.config(state=tk.DISABLED)
        opts = ttk.Frame(frm)
        opts.pack(fill=tk.X, pady=8)
        self.do_backup = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts, text="Backup current file before revert", variable=self.do_backup).pack(side=tk.LEFT)
        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Cancel", command=self._cancel).pack(side=tk.RIGHT, padx=(6,0))
        ttk.Button(btns, text="Revert", style="Accent.TButton", command=self._ok).pack(side=tk.RIGHT)
        self.transient(parent)
        self.grab_set()
        self.wait_visibility()
        self.focus_set()
    def _ok(self):
        self.result = {"backup": self.do_backup.get()}
        self.destroy()
    def _cancel(self):
        self.result = None
        self.destroy()

class ValheimConfigSuite(tk.Tk):
    def __init__(self, config_root: Path, vnei_root: Path, wdbulk_root: Path, prefs_file: Path):
        super().__init__()
        self.title("Valheim Config Suite — v2"); self.geometry("1660x980"); self.minsize(1120,720)
        self.style=ttk.Style()
        try: self.style.theme_use("clam")
        except Exception: pass
        self.colors={"bg":"#152616","panel":"#414535","text":"#b07b53","muted":"#654735","accent":"#5f633e","accent2":"#654735"}
        self.configure(bg=self.colors["bg"])
        base_font=tkfont.Font(family="Consolas" if sys.platform.startswith("win") else "Courier New", size=10)
        for nm in ("TLabel","TButton","Treeview","Treeview.Heading","TEntry","TCombobox"):
            self.style.configure(nm, background=self.colors["panel"], foreground=self.colors["text"], font=base_font)
        self.style.configure("Treeview", fieldbackground=self.colors["panel"])
        self.style.configure("Accent.TButton", background=self.colors["accent"], foreground="#152616")
        self.style.map("Accent.TButton", background=[("active", self.colors["accent2"])])

        self.prefs_file=prefs_file; self.prefs=AppPrefs.load(self.prefs_file)
        if config_root: self.prefs.config_root=str(config_root)
        if vnei_root: self.prefs.vnei_root=str(vnei_root)
        if wdbulk_root: self.prefs.wacky_bulk_root=str(wdbulk_root)

        self.store_dir=Path(__file__).parent / "snapshots"; self.store_dir.mkdir(parents=True, exist_ok=True)
        self.snapshot=ConfigSnapshot(Path(self.prefs.config_root) if self.prefs.config_root else Path.cwd(), self.store_dir, set(self.prefs.ignored_dirs), backups_to_keep=self.prefs.backups_to_keep)
        self.vnei=VNEIItemIndex(Path(self.prefs.vnei_root) if self.prefs.vnei_root else Path.cwd())
        self.wacky=WackyBulkIndex(Path(self.prefs.wacky_bulk_root) if self.prefs.wacky_bulk_root else Path.cwd())

        self.work_q: "queue.Queue[tuple[str, dict]]" = queue.Queue(); self.after(50, self._pump_ui)

        # Menus
        menubar=tk.Menu(self, tearoff=False)
        m_file=tk.Menu(menubar, tearoff=False)
        m_file.add_command(label="Save Session Snapshot", command=lambda: self._run_bg("snapshot", {"initial": False}))
        m_file.add_command(label="Set New Baseline", command=lambda: self._run_bg("snapshot", {"initial": True}))
        m_file.add_separator()
        m_file.add_command(label="Export Changes as CSV", command=self._export_changes_csv)
        m_file.add_command(label="Export Items/Recipes as CSV", command=self._export_items_csv)
        m_file.add_separator()
        m_file.add_command(label="RelicHeim Comparison", command=self._show_relicheim_comparison)
        m_file.add_command(label="Game-Changing Changes", command=self._show_game_changing_changes)
        m_file.add_separator()
        m_file.add_command(label="Quit", command=self.destroy)
        menubar.add_cascade(label="File", menu=m_file)
        m_help=tk.Menu(menubar, tearoff=False)
        m_help.add_command(label="Event Log", command=self._open_event_log)
        m_help.add_command(label="Debug Info", command=self._show_debug_info)
        m_help.add_command(label="About", command=self._about)
        menubar.add_cascade(label="Help", menu=m_help)
        self.config(menu=menubar)

        # Toolbar
        tbar=ttk.Frame(self, padding=(8,6)); tbar.pack(fill=tk.X)
        ttk.Button(tbar, text="Scan Changes", style="Accent.TButton", command=lambda: self._run_bg("scan_changes", {})).pack(side=tk.LEFT)
        ttk.Button(tbar, text="Re-scan Items/Recipes", command=lambda: self._run_bg("scan_items", {})).pack(side=tk.LEFT, padx=(8,0))
        ttk.Separator(tbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Label(tbar, text="Status:").pack(side=tk.LEFT)
        self.status_filter=tk.StringVar(value="All")
        ttk.Combobox(tbar, textvariable=self.status_filter, state="readonly", width=10, values=["All","Added","Modified","Deleted"]).pack(side=tk.LEFT, padx=(4,10))
        self.status_filter.trace_add("write", lambda *_: self._filter_changes())
        ttk.Label(tbar, text="Path filter:").pack(side=tk.LEFT)
        self.path_filter=tk.StringVar(value=""); ent=ttk.Entry(tbar, textvariable=self.path_filter, width=36); ent.pack(side=tk.LEFT, padx=(4,10))
        ent.bind("<KeyRelease>", lambda e: self._filter_changes())
        ttk.Button(tbar, text="Settings", command=self._open_settings).pack(side=tk.LEFT)
        ttk.Separator(tbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Button(tbar, text="Restore Last Backup (Selected)", command=self._restore_selected_backup).pack(side=tk.LEFT)
        self.busy_var=tk.StringVar(value="Ready"); ttk.Label(tbar, textvariable=self.busy_var, foreground=self.colors["muted"]).pack(side=tk.RIGHT)

        # Notebook
        nb=ttk.Notebook(self); nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8); self.nb=nb

        # Changes tab
        self.tab_changes=ttk.Frame(nb); nb.add(self.tab_changes, text="Changes")
        row=ttk.Frame(self.tab_changes); row.pack(fill=tk.X, pady=(6,6))
        ttk.Label(row, text="Compare against:").pack(side=tk.LEFT)
        self.compare_var=tk.StringVar(value="Since Baseline")
        ttk.Combobox(row, textvariable=self.compare_var, width=22, state="readonly", values=["Since Baseline","Since Last Snapshot"]).pack(side=tk.LEFT, padx=(6,12))
        ttk.Button(row, text="Revert Selected", command=self._revert_selected).pack(side=tk.LEFT)
        ttk.Button(row, text="Accept into Baseline", command=self._accept_selected).pack(side=tk.LEFT, padx=(6,0))
        body=ttk.Panedwindow(self.tab_changes, orient=tk.HORIZONTAL); body.pack(fill=tk.BOTH, expand=True)
        left=ttk.Frame(body); right=ttk.Frame(body); body.add(left, weight=1); body.add(right, weight=2)
        cols=("status","file","size","mtime","summary")
        self.tree_changes=ttk.Treeview(left, columns=cols, show="headings", height=20, selectmode="extended")
        for c,w in zip(cols,(70,520,110,160,280)):
            self.tree_changes.heading(c, text=c.capitalize()); self.tree_changes.column(c, width=w, anchor=tk.W)
        vs=ttk.Scrollbar(left, orient=tk.VERTICAL, command=self.tree_changes.yview)
        self.tree_changes.configure(yscrollcommand=vs.set)
        self.tree_changes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); vs.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_changes.bind("<<TreeviewSelect>>", lambda e: self._show_selected_diff())
        self.tree_changes.bind("<Button-3>", self._changes_context_menu)
        self.diff_text=tk.Text(right, wrap=tk.NONE, bg=self.colors["panel"], fg=self.colors["text"], insertbackground=self.colors["text"])
        y=ttk.Scrollbar(right, orient=tk.VERTICAL, command=self.diff_text.yview)
        x=ttk.Scrollbar(right, orient=tk.HORIZONTAL, command=self.diff_text.xview)
        self.diff_text.configure(yscrollcommand=y.set, xscrollcommand=x.set)
        self.diff_text.pack(fill=tk.BOTH, expand=True); y.pack(side=tk.RIGHT, fill=tk.Y); x.pack(side=tk.BOTTOM, fill=tk.X)
        self.diff_text.tag_configure("add", foreground="#5f633e")
        self.diff_text.tag_configure("del", foreground="#654735")
        self.diff_text.tag_configure("hunk", foreground="#b07b53")

        # Items tab
        self.tab_items=ttk.Frame(nb); nb.add(self.tab_items, text="Items / Recipes")
        top=ttk.Frame(self.tab_items); top.pack(fill=tk.X, pady=(6,6))
        ttk.Label(top, text="Filter:").pack(side=tk.LEFT)
        self.filter_var=tk.StringVar(value=""); ent2=ttk.Entry(top, textvariable=self.filter_var, width=40); ent2.pack(side=tk.LEFT, padx=(6,12))
        ent2.bind("<KeyRelease>", lambda e: self._filter_items())
        ttk.Button(top, text="Export Selection to CSV", command=self._export_items_csv).pack(side=tk.LEFT)
        body2=ttk.Panedwindow(self.tab_items, orient=tk.HORIZONTAL); body2.pack(fill=tk.BOTH, expand=True)
        left2=ttk.Frame(body2); right2=ttk.Frame(body2); body2.add(left2, weight=1); body2.add(right2, weight=2)
        icols=("item","station","tier","world_level","stats","recipe")
        self.tree_items=ttk.Treeview(left2, columns=icols, show="headings", height=20, selectmode="extended")
        for c,w,h in zip(icols,(260,170,70,90,360,280),("Item","Station","Tier","WL","Stats","Recipe")):
            self.tree_items.heading(c, text=h); self.tree_items.column(c, width=w, anchor=tk.W)
        vsi=ttk.Scrollbar(left2, orient=tk.VERTICAL, command=self.tree_items.yview)
        self.tree_items.configure(yscrollcommand=vsi.set)
        self.tree_items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); vsi.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_items.bind("<<TreeviewSelect>>", lambda e: self._show_item_detail())
        self.item_detail=tk.Text(right2, wrap=tk.WORD, bg=self.colors["panel"], fg=self.colors["text"], insertbackground=self.colors["text"])
        y2=ttk.Scrollbar(right2, orient=tk.VERTICAL, command=self.item_detail.yview)
        self.item_detail.configure(yscrollcommand=y2.set); self.item_detail.pack(fill=tk.BOTH, expand=True); y2.pack(side=tk.RIGHT, fill=tk.Y)

        # Settings tab with Profiles
        self.tab_settings=ttk.Frame(nb); nb.add(self.tab_settings, text="Settings")
        sfrm=ttk.Frame(self.tab_settings, padding=12); sfrm.pack(fill=tk.BOTH, expand=True)
        def row_of(label, var, browse_cmd):
            fr=ttk.Frame(sfrm); fr.pack(fill=tk.X, pady=6)
            ttk.Label(fr, text=label, width=22).pack(side=tk.LEFT)
            ent=ttk.Entry(fr, textvariable=var); ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10,10))
            if browse_cmd: ttk.Button(fr, text="Browse…", command=browse_cmd).pack(side=tk.LEFT)
            return ent
        self.var_config=tk.StringVar(value=self.prefs.config_root)
        self.var_vnei=tk.StringVar(value=self.prefs.vnei_root)
        self.var_bulk=tk.StringVar(value=self.prefs.wacky_bulk_root)
        row_of("Config Root", self.var_config, self._browse_config); row_of("VNEI Export Root", self.var_vnei, self._browse_vnei); row_of("Wacky Bulk YML Root", self.var_bulk, self._browse_bulk)
        self.var_hashing=tk.BooleanVar(value=self.prefs.use_hashing); ttk.Checkbutton(sfrm, text="Hash file contents (slower, more precise)", variable=self.var_hashing).pack(anchor="w", pady=(6,0))
        prof_fr=ttk.LabelFrame(sfrm, text="Profiles"); prof_fr.pack(fill=tk.X, pady=(10,0))
        self.profile_name=tk.StringVar(value=""); ttk.Label(prof_fr, text="Profile:").pack(side=tk.LEFT, padx=(6,4))
        self.profile_combo=ttk.Combobox(prof_fr, values=list(self.prefs.profiles.keys()), width=24, state="readonly"); self.profile_combo.pack(side=tk.LEFT, padx=(0,6))
        ttk.Button(prof_fr, text="Load", command=self._load_profile).pack(side=tk.LEFT)
        ttk.Entry(prof_fr, textvariable=self.profile_name, width=18).pack(side=tk.LEFT, padx=(12,6))
        ttk.Button(prof_fr, text="Save Current as New", command=self._save_profile).pack(side=tk.LEFT)
        ttk.Button(prof_fr, text="Delete", command=self._delete_profile).pack(side=tk.LEFT, padx=(6,0))
        ttk.Button(sfrm, text="Save Preferences", style="Accent.TButton", command=self._save_prefs).pack(anchor="e", pady=(18,0))

        self._run_bg("scan_items", {})
        self._run_bg("scan_changes", {})
        try:
            if self.prefs.last_window:
                x, y, w, h = (self.prefs.last_window.get(k) for k in ("x","y","w","h"))
                if None not in (x, y, w, h):
                    self.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------- Workers ----------
    def _pump_ui(self):
        try:
            while True:
                name, payload = self.work_q.get_nowait()
                if name == "busy": self.busy_var.set(payload.get("msg",""))
                elif name == "changes_ready":
                    self._changes_raw = payload["changes"]
                    self._changes_info = payload["info"]
                    self._populate_changes()
                    self.busy_var.set("Ready")
                elif name == "items_ready":
                    self._populate_items(payload["items"])
                    self.busy_var.set("Ready")
        except queue.Empty:
            pass
        self.after(80, self._pump_ui)

    def _run_bg(self, op: str, args: dict):
        def worker():
            if op == "snapshot":
                initial=args.get("initial", False)
                self.work_q.put(("busy", {"msg": ("Creating baseline…" if initial else "Saving snapshot…")}))
                ok, msg = self.snapshot.create_snapshot(is_initial=initial, use_hash=self.var_hashing.get())
                self.work_q.put(("busy", {"msg": msg}))
            elif op == "scan_changes":
                self.work_q.put(("busy", {"msg": "Scanning for changes…"}))
                compare = "initial" if self.compare_var.get().startswith("Since Baseline") else "current"
                changes = self.snapshot.list_changes(compare_against=compare)
                info = {}
                for status, rel in changes:
                    p = Path(self.snapshot.config_root) / rel
                    try:
                        st = p.stat()
                        mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
                        size = st.st_size
                    except Exception:
                        mtime, size = "", 0
                    summary = ""
                    try:
                        diff = self.snapshot.get_diff_text(rel, compare_against=compare)
                        adds = sum(1 for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++"))
                        dels = sum(1 for ln in diff.splitlines() if ln.startswith("-") and not ln.startswith("---"))
                        if adds or dels: summary = f"+{adds} / -{dels}"
                    except Exception: pass
                    info[rel] = {"mtime": mtime, "size": size, "summary": summary, "status": status}
                self.work_q.put(("changes_ready", {"changes": changes, "info": info}))
            elif op == "scan_items":
                self.work_q.put(("busy", {"msg": "Indexing items & recipes…"}))
                try:
                    vnei = self.vnei.load_items_with_stats()
                    vnei_meta = self.vnei.load_item_metadata()
                    wacky = self.wacky.scan()
                    wacky_meta = self.wacky.load_item_metadata()
                    wacky_tiers = self.wacky.load_tool_tiers(Path(self.prefs.config_root) if self.prefs.config_root else Path.cwd())
                    wacky_configs = self.wacky.scan_configs_for_recipes_and_unlocks(Path(self.prefs.config_root) if self.prefs.config_root else Path.cwd())
                    
                    merged = {}
                    keys = set(vnei.keys()) | set(wacky.keys())
                    for k in sorted(keys):
                        e = {}
                        e.update(vnei.get(k, {}))
                        e.update(wacky.get(k, {}))
                        
                        # Add metadata
                        vnei_m = vnei_meta.get(k, {})
                        wacky_m = wacky_meta.get(k, {})
                        if vnei_m or wacky_m:
                            e["metadata"] = {**vnei_m, **wacky_m}
                        
                        # Add tool tier if available
                        if k in wacky_tiers:
                            e["tool_tier"] = wacky_tiers[k]
                            wl_num, wl_name = self.wacky.map_tool_tier_to_world_level(wacky_tiers[k])
                            e["world_level"] = wl_num
                            e["world_level_name"] = wl_name
                        
                        # Add config info
                        if k in wacky_configs:
                            e.update(wacky_configs[k])
                        
                        merged[k] = e
                    
                    self.work_q.put(("items_ready", {"items": merged}))
                except Exception as e:
                    self.work_q.put(("busy", {"msg": f"Error scanning items: {e}"}))
                    # Fallback to basic scanning
                    try:
                        vnei = self.vnei.load_items_with_stats()
                        wacky = self.wacky.scan()
                        merged = {}
                        keys = set(vnei.keys()) | set(wacky.keys())
                        for k in sorted(keys):
                            e = {}
                            e.update(vnei.get(k, {}))
                            e.update(wacky.get(k, {}))
                            merged[k] = e
                        self.work_q.put(("items_ready", {"items": merged}))
                    except Exception as e2:
                        self.work_q.put(("busy", {"msg": f"Failed to scan items: {e2}"}))
        threading.Thread(target=worker, daemon=True).start()

    # ---------- Changes Tab ----------
    def _populate_changes(self):
        self.tree_changes.delete(*self.tree_changes.get_children())
        for status, rel in sorted(self._changes_raw, key=lambda it: (self._changes_info.get(it[1],{}).get("mtime",""), it[1]), reverse=True):
            meta=self._changes_info.get(rel, {})
            self.tree_changes.insert("", "end", values=(status, rel, meta.get("size",0), meta.get("mtime",""), meta.get("summary","")))
        self._filter_changes()

    def _filter_changes(self):
        want = self.status_filter.get()
        patt = self.path_filter.get().lower().strip()
        for iid in self.tree_changes.get_children():
            st, rel, *_ = self.tree_changes.item(iid, "values")
            show = True
            if want != "All":
                show = (want[0] == st)
            if show and patt:
                show = patt in str(rel).lower()
            if not show:
                self.tree_changes.detach(iid)
            else:
                self.tree_changes.reattach(iid, "", "end")

    def _get_selected_rel_paths(self) -> list[str]:
        return [self.tree_changes.item(s, "values")[1] for s in self.tree_changes.selection()]

    def _show_selected_diff(self):
        sels = self.tree_changes.selection()
        text = ""
        compare = "initial" if self.compare_var.get().startswith("Since Baseline") else "current"
        if sels:
            rel = self.tree_changes.item(sels[0], "values")[1]
            text = self.snapshot.get_diff_text(rel, compare_against=compare)
        self.diff_text.config(state=tk.NORMAL)
        self.diff_text.delete("1.0", tk.END)
        for ln in text.splitlines(True):
            tag = None
            if ln.startswith("+") and not ln.startswith("+++"):
                tag = "add"
            elif ln.startswith("-") and not ln.startswith("---"):
                tag = "del"
            elif ln.startswith("@@"):
                tag = "hunk"
            self.diff_text.insert("end", ln, tag if tag else ())
        self.diff_text.config(state=tk.DISABLED)

    def _revert_selected(self):
        rels = self._get_selected_rel_paths()
        if not rels:
            return
        compare = "initial" if self.compare_var.get().startswith("Since Baseline") else "current"
        if len(rels) == 1:
            rel = rels[0]
            try:
                st = (Path(self.snapshot.config_root)/rel).stat()
                meta_new = f"{st.st_size} bytes @ {datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M')}"
            except Exception:
                meta_new = "missing"
            snap = self.snapshot._load_snapshot(compare).get("files", {}).get(rel)
            meta_old = f"{snap.get('size',0)} bytes @ {datetime.fromtimestamp(snap.get('mtime',0)).strftime('%Y-%m-%d %H:%M') if snap and snap.get('mtime') else 'n/a'}" if snap else "not in snapshot"
            diff_text = self.snapshot.get_diff_text(rel, compare_against=compare)
            dlg = RevertPreview(self, rel, diff_text, meta_old, meta_new)
            self.wait_window(dlg)
            if dlg.result:
                ok, msg = self.snapshot.revert_file(rel, from_snapshot=compare, do_backup=dlg.result.get("backup", True))
                messagebox.showinfo("Revert", msg)
        else:
            counts = {"A": 0, "M": 0, "D": 0}
            for r in rels:
                counts[self._changes_info.get(r, {}).get("status", "?")] = counts.get(self._changes_info.get(r, {}).get("status", "?"), 0) + 1
            do_backup = messagebox.askyesno("Bulk Revert", f"Revert {len(rels)} files?\nAdded: {counts.get('A',0)}  Modified: {counts.get('M',0)}  Deleted: {counts.get('D',0)}\n\nBack up current files before reverting?")
            for r in rels:
                self.snapshot.revert_file(r, from_snapshot=compare, do_backup=do_backup)
            messagebox.showinfo("Bulk Revert", f"Reverted {len(rels)} files.")
        self._run_bg("scan_changes", {})

    def _accept_selected(self):
        rels = self._get_selected_rel_paths()
        if not rels:
            return
        msg = simpledialog.askstring("Accept into Baseline", "Optional commit message (why accept?)", parent=self) or ""
        do_backup = True
        if len(rels) > 1:
            do_backup = messagebox.askyesno("Bulk Accept", f"Accept {len(rels)} files into baseline?\nBack up current files first?")
        for r in rels:
            self.snapshot.accept_into_baseline(r, commit_message=msg, do_backup=do_backup)
        messagebox.showinfo("Accept", f"Accepted {len(rels)} file(s) into baseline.")
        self._run_bg("scan_changes", {})

    def _restore_selected_backup(self):
        rels = self._get_selected_rel_paths()
        if not rels:
            return
        restored = 0
        for r in rels:
            ok, _ = self.snapshot.restore_last_backup(r)
            if ok:
                restored += 1
        messagebox.showinfo("Restore", f"Restored {restored} file(s) from latest backups (if available).")
        self._run_bg("scan_changes", {})

    def _changes_context_menu(self, event):
        iid = self.tree_changes.identify_row(event.y)
        if not iid:
            return
        self.tree_changes.selection_set(iid)
        rel = self.tree_changes.item(iid, "values")[1]
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Open", command=lambda: open_external(Path(self.snapshot.config_root)/rel))
        menu.add_command(label="Reveal in Folder", command=lambda: reveal_in_folder(Path(self.snapshot.config_root)/rel))
        menu.add_separator()
        menu.add_command(label="Revert…", command=self._revert_selected)
        menu.add_command(label="Accept into Baseline…", command=self._accept_selected)
        menu.add_command(label="Restore Last Backup", command=self._restore_selected_backup)
        menu.add_separator()
        menu.add_command(label="Copy Relative Path", command=lambda: (self.clipboard_clear(), self.clipboard_append(rel)))
        menu.post(event.x_root, event.y_root)

    # ---------- Items Tab ----------
    def _populate_items(self, merged: dict[str, dict]):
        self._items_data = merged
        self._filter_items()

    def _filter_items(self):
        q = self.filter_var.get().strip().lower()
        self.tree_items.delete(*self.tree_items.get_children())
        for item, d in sorted(self._items_data.items()):
            rec = ", ".join([f"{m}:{n}" for m, n in d.get("recipe", [])]) if d.get("recipe") else ""
            stats = " | ".join([f"{k.capitalize()} {v}" for k, v in (d.get("stats") or {}).items()]) if isinstance(d.get("stats"), dict) else (d.get("stats") or "")
            row = (item, d.get("station", ""), d.get("tier", ""), d.get("world_level", ""), stats, rec)
            if not q or any(q in str(cell).lower() for cell in row):
                self.tree_items.insert("", "end", values=row)

    def _show_item_detail(self):
        sel = self.tree_items.selection()
        if not sel:
            return
        vals = self.tree_items.item(sel[0], "values")
        item = vals[0]
        d = self._items_data.get(item, {})
        lines = [f"Item: {item}"]
        
        # Basic info
        for k in ("station", "station_level", "tier", "world_level", "tool_tier"):
            if k in d:
                lines.append(f"{k.replace('_',' ').title()}: {d[k]}")
        
        # World level name if available
        if "world_level_name" in d:
            lines.append(f"World Level Name: {d['world_level_name']}")
        
        # Stats
        stats = d.get("stats")
        if stats:
            if isinstance(stats, dict):
                lines.append("Stats: " + ", ".join(f"{k} {v}" for k, v in stats.items()))
            else:
                lines.append(f"Stats: {stats}")
        
        # Metadata
        metadata = d.get("metadata", {})
        if metadata:
            lines.append("Metadata:")
            for k, v in metadata.items():
                if v:
                    lines.append(f"  {k.replace('_',' ').title()}: {v}")
        
        # Recipe
        if d.get("recipe"):
            lines.append("Recipe:")
            for mat, qty in d["recipe"]:
                lines.append(f"  - {mat}: {qty}")
        
        # Config info
        config_keys = ["recipe", "station", "station_level", "unlock", "prestige", "set", "bis"]
        config_info = []
        for k in config_keys:
            if k in d and k != "recipe":  # recipe already shown above
                config_info.append(f"{k.replace('_',' ').title()}: {d[k]}")
        if config_info:
            lines.append("Config Info:")
            lines.extend(f"  {info}" for info in config_info)
        
        self.item_detail.config(state=tk.NORMAL)
        self.item_detail.delete("1.0", tk.END)
        self.item_detail.insert("1.0", "\n".join(lines))
        self.item_detail.config(state=tk.DISABLED)

    # ---------- Settings & Profiles ----------
    def _browse_config(self):
        p = filedialog.askdirectory(title="Choose config root")
        self.var_config.set(p or self.var_config.get())

    def _browse_vnei(self):
        p = filedialog.askdirectory(title="Choose VNEI export root")
        self.var_vnei.set(p or self.var_vnei.get())

    def _browse_bulk(self):
        p = filedialog.askdirectory(title="Choose Wacky Bulk YML root")
        self.var_bulk.set(p or self.var_bulk.get())

    def _save_prefs(self):
        self.prefs.config_root = self.var_config.get().strip()
        self.prefs.vnei_root = self.var_vnei.get().strip()
        self.prefs.wacky_bulk_root = self.var_bulk.get().strip()
        self.prefs.use_hashing = bool(self.var_hashing.get())
        self.prefs.save(self.prefs_file)
        self.snapshot = ConfigSnapshot(Path(self.prefs.config_root) if self.prefs.config_root else Path.cwd(), self.store_dir, set(self.prefs.ignored_dirs), backups_to_keep=self.prefs.backups_to_keep)
        self.vnei = VNEIItemIndex(Path(self.prefs.vnei_root) if self.prefs.vnei_root else Path.cwd())
        self.wacky = WackyBulkIndex(Path(self.prefs.wacky_bulk_root) if self.prefs.wacky_bulk_root else Path.cwd())
        messagebox.showinfo("Saved", "Preferences saved.")
        self._run_bg("scan_items", {})
        self._run_bg("scan_changes", {})

    def _load_profile(self):
        name = self.profile_combo.get().strip()
        if not name or name not in self.prefs.profiles:
            return
        pf = self.prefs.profiles[name]
        self.var_config.set(pf.get("config_root", ""))
        self.var_vnei.set(pf.get("vnei_root", ""))
        self.var_bulk.set(pf.get("wacky_bulk_root", ""))
        self._save_prefs()

    def _save_profile(self):
        name = self.profile_name.get().strip() or simpledialog.askstring("Profile Name", "Enter a name for this profile:", parent=self)
        if not name:
            return
        self.prefs.profiles[name] = {"config_root": self.var_config.get().strip(), "vnei_root": self.var_vnei.get().strip(), "wacky_bulk_root": self.var_bulk.get().strip()}
        self.prefs.save(self.prefs_file)
        self.profile_combo["values"] = list(self.prefs.profiles.keys())
        self.profile_combo.set(name)
        messagebox.showinfo("Profiles", f"Saved profile '{name}'.")

    def _delete_profile(self):
        name = self.profile_combo.get().strip()
        if not name or name not in self.prefs.profiles:
            return
        if messagebox.askyesno("Delete Profile", f"Delete profile '{name}'?"):
            del self.prefs.profiles[name]
            self.prefs.save(self.prefs_file)
            self.profile_combo["values"] = list(self.prefs.profiles.keys())
            self.profile_combo.set("")
            messagebox.showinfo("Profiles", "Deleted.")

    def _open_settings(self):
        # Switch to Settings tab
        for i, tid in enumerate(self.nb.tabs()):
            if self.nb.tab(tid, "text") == "Settings":
                self.nb.select(tid)
                break

    # ---------- Export / Help / Close ----------
    def _export_changes_csv(self):
        fname = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], title="Export Changes")
        if not fname:
            return
        compare = "initial" if self.compare_var.get().startswith("Since Baseline") else "current"
        changes = self.snapshot.list_changes(compare_against=compare)
        with open(fname, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Status","File"])
            [w.writerow([st, rel]) for st, rel in changes]
        messagebox.showinfo("Export", f"Exported {len(changes)} rows.")

    def _export_items_csv(self):
        fname = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], title="Export Items/Recipes")
        if not fname:
            return
        count = 0
        with open(fname, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Item","Station","StationLevel","Tier","WorldLevel","Stats","Recipe"])
            for item, d in sorted(getattr(self, "_items_data", {}).items()):
                stats = " | ".join([f"{k}:{v}" for k, v in (d.get("stats") or {}).items()]) if isinstance(d.get("stats"), dict) else (d.get("stats") or "")
                recipe = ", ".join([f"{m}:{q}" for m, q in d.get("recipe", [])])
                w.writerow([item, d.get("station",""), d.get("station_level",""), d.get("tier",""), d.get("world_level",""), stats, recipe])
                count += 1
        messagebox.showinfo("Export", f"Exported {count} items.")

    def _open_event_log(self):
        p = self.snapshot.event_log_file
        if not p.exists():
            messagebox.showinfo("Event Log", "No events yet.")
            return
        try:
            os.startfile(str(p))
        except Exception:
            try:
                import subprocess
                subprocess.Popen(["xdg-open", str(p)])
            except Exception:
                messagebox.showinfo("Event Log", f"Log at: {p}")

    def _show_debug_info(self):
        """Show debug information to help troubleshoot issues."""
        try:
            info_lines = []
            info_lines.append("=== Debug Information ===")
            info_lines.append(f"Config Root: {self.prefs.config_root}")
            info_lines.append(f"VNEI Root: {self.prefs.vnei_root}")
            info_lines.append(f"Wacky Bulk Root: {self.prefs.wacky_bulk_root}")
            info_lines.append("")
            
            # Check VNEI files
            info_lines.append("=== VNEI Files ===")
            vnei_path = Path(self.prefs.vnei_root) if self.prefs.vnei_root else Path.cwd()
            info_lines.append(f"VNEI Path: {vnei_path}")
            info_lines.append(f"VNEI Path exists: {vnei_path.exists()}")
            if vnei_path.exists():
                for file in ["VNEI.indexed.items.csv", "VNEI.indexed.items.txt", "VNEI.indexed.items.yml"]:
                    file_path = vnei_path / file
                    info_lines.append(f"  {file}: {file_path.exists()} ({file_path.stat().st_size if file_path.exists() else 0} bytes)")
            
            # Check Wacky files
            info_lines.append("")
            info_lines.append("=== Wacky Bulk Files ===")
            wacky_path = Path(self.prefs.wacky_bulk_root) if self.prefs.wacky_bulk_root else Path.cwd()
            info_lines.append(f"Wacky Path: {wacky_path}")
            info_lines.append(f"Wacky Path exists: {wacky_path.exists()}")
            if wacky_path.exists():
                yaml_files = list(wacky_path.rglob("*.yml")) + list(wacky_path.rglob("*.yaml"))
                info_lines.append(f"  YAML files found: {len(yaml_files)}")
                for subdir in ["Items", "Recipes", "Creatures", "Pickables"]:
                    sub_path = wacky_path / subdir
                    if sub_path.exists():
                        sub_files = list(sub_path.rglob("*.yml")) + list(sub_path.rglob("*.yaml"))
                        info_lines.append(f"  {subdir}: {len(sub_files)} files")
            
            # Check items data
            info_lines.append("")
            info_lines.append("=== Items Data ===")
            if hasattr(self, '_items_data'):
                info_lines.append(f"Items loaded: {len(self._items_data)}")
                if self._items_data:
                    sample_items = list(self._items_data.keys())[:5]
                    info_lines.append(f"Sample items: {', '.join(sample_items)}")
            else:
                info_lines.append("No items data loaded yet")
            
            # Show in dialog
            info_text = "\n".join(info_lines)
            
            # Create a dialog to show the info
            dialog = tk.Toplevel(self)
            dialog.title("Debug Information")
            dialog.geometry("600x500")
            dialog.transient(self)
            dialog.grab_set()
            
            text_widget = tk.Text(dialog, wrap=tk.WORD, font=("Consolas", 9))
            scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget.insert("1.0", info_text)
            text_widget.config(state=tk.DISABLED)
            
            ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Debug Error", f"Failed to show debug info: {e}")

    def _about(self):
        messagebox.showinfo("About", "Valheim Config Suite — v2\nBackups • Revert Preview • Profiles • Bulk Ops")

    def _show_relicheim_comparison(self):
        """Show RelicHeim comparison dialog."""
        try:
            # This would need to be implemented based on config_change_tracker.py
            # For now, show a placeholder
            messagebox.showinfo("RelicHeim Comparison", "RelicHeim comparison feature coming soon!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show RelicHeim comparison: {e}")

    def _show_game_changing_changes(self):
        """Show game-changing changes dialog."""
        try:
            # This would need to be implemented based on config_change_tracker.py
            # For now, show a placeholder
            messagebox.showinfo("Game-Changing Changes", "Game-changing changes feature coming soon!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show game-changing changes: {e}")

    def _on_close(self):
        try:
            x = self.winfo_x()
            y = self.winfo_y()
            w = self.winfo_width()
            h = self.winfo_height()
            self.prefs.last_window = {"x": x, "y": y, "w": w, "h": h}
            self.prefs.save(self.prefs_file)
        except Exception:
            pass
        self.destroy()

def parse_args(argv: list[str]):
    import argparse
    ap = argparse.ArgumentParser(description="Valheim Config Suite — v2")
    ap.add_argument("--config", help="Config root directory")
    ap.add_argument("--vnei", help="VNEI export directory")
    ap.add_argument("--wdbulk", help="WackyDatabase-BulkYML directory")
    return ap.parse_args(argv)

def main():
    args = parse_args(sys.argv[1:])
    prefs = Path(__file__).parent / "snapshots" / "preferences.json"
    app = ValheimConfigSuite(config_root=Path(args.config) if args.config else Path(""),
                           vnei_root=Path(args.vnei) if args.vnei else Path(""),
                           wdbulk_root=Path(args.wdbulk) if args.wdbulk else Path(""),
                           prefs_file=prefs)
    app.mainloop()

if __name__ == "__main__":
    main()
