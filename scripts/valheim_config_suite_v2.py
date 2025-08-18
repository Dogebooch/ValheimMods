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
        result = {}
        source = None
        if self.items_csv.exists():
            source = self.items_csv
        elif self.items_txt.exists():
            source = self.items_txt
        elif self.items_yml.exists():
            source = self.items_yml
        if source is None:
            return result

        if source.suffix.lower() in (".csv",".txt"):
            with open(source, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                lower = [h.lower().strip() for h in headers]
                item_col, _ = self._guess_columns(headers)
                def get_num(row, cand):
                    for k in cand:
                        if k in lower:
                            v = row.get(headers[lower.index(k)], "")
                            if v is None: continue
                            try:
                                s = str(v).strip()
                                s = re.sub(r"\s*\([^)]*\)", "", s).replace(",", "").split()[0]
                                if "-" in s: 
                                    parts = [float(p) for p in s.split("-") if p]
                                    if parts:
                                        return sum(parts)/len(parts)
                                return float(s)
                            except Exception:
                                continue
                    return None
                for row in reader:
                    key = (row.get(item_col, "") or "").strip()
                    if not key:
                        continue
                    armor = get_num(row, ["armor","armour","defense"])
                    dmg = get_num(row, ["damage","totaldamage","dmg","basedamage"])
                    station = ""
                    for k in ("craftingstation","crafting_station","station","workbench","forge","table"):
                        if k in lower:
                            station = row.get(headers[lower.index(k)], "") or ""
                            break
                    parts = []
                    if armor is not None:
                        parts.append(f"Armor {int(armor) if float(armor).is_integer() else round(armor,1)}")
                    elif dmg is not None:
                        parts.append(f"DMG {int(dmg) if float(dmg).is_integer() else round(dmg,1)}")
                    result[key] = {"station": station, "stats": " | ".join(parts)}
        else:
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

class WackyBulkIndex:
    def __init__(self, bulk_root: Path):
        self.bulk_root = bulk_root

    def _iter_yaml(self) -> list[Path]:
        if not self.bulk_root or not self.bulk_root.exists():
            return []
        files = []
        for sub in ("Items","Recipes","Creatures","Pickables"):
            p = self.bulk_root/sub
            if p.exists():
                files.extend(p.rglob("*.yml"))
                files.extend(p.rglob("*.yaml"))
        files.extend(self.bulk_root.glob("*.yml"))
        files.extend(self.bulk_root.glob("*.yaml"))
        seen = set()
        uniq = []
        for f in files:
            s = str(f.resolve())
            if s not in seen:
                uniq.append(f)
                seen.add(s)
        return uniq

    def _product_from_recipe_name(self, name: str) -> str:
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

    def scan(self) -> dict[str, dict]:
        info = {}
        for path in self._iter_yaml():
            text = read_text_safely(path)
            pstr = str(path).replace("\\","/")
            is_recipe = "/Recipes/" in pstr
            prefab_candidates = set()
            if is_recipe:
                m = re.search(r"^\s*name\s*:\s*([A-Za-z0-9_\-.]+)\s*$", text, re.MULTILINE)
                if m:
                    prod = self._product_from_recipe_name(m.group(1))
                    if prod:
                        prefab_candidates.add(prod)
            if not prefab_candidates:
                for m in re.finditer(r"^\s*(?:-\s*)?PrefabName\s*:\s*([A-Za-z0-9_\-.]+)\s*$", text, re.MULTILINE):
                    prefab_candidates.add(m.group(1))
                for m in re.finditer(r"^\s*(?:-\s*)?(?:name|InternalName)\s*:\s*([A-Za-z0-9_\-.]+)\s*$", text, re.MULTILINE|re.IGNORECASE):
                    prefab_candidates.add(m.group(1))
            station = ""
            station_level = None
            tier = None
            world_level = None
            def find_num(key):
                m = re.search(re.escape(key)+r"\s*:\s*([0-9.\-]+)", text, re.IGNORECASE)
                if not m:
                    return None
                try:
                    return float(m.group(1))
                except Exception:
                    return None
            m_station = re.search(r"(CraftingStation|Station|WorkBench)\s*:\s*([A-Za-z0-9_\- ]+)", text, re.IGNORECASE)
            if m_station:
                station = m_station.group(2).strip()
            for key in ("CraftingStationLevel","StationLevel","RequiredStationLevel","minStationLevel"):
                v = find_num(key)
                if v is not None:
                    station_level = int(v)
                    break
            v = find_num("Tier") or find_num("m_toolTier")
            tier = int(v) if v is not None else tier
            v = find_num("WorldLevel") or find_num("ConditionWorldLevelMin")
            world_level = int(v) if v is not None else world_level
            stats = {}
            def pick(keys):
                for k in keys:
                    vv = find_num(k)
                    if vv is not None:
                        return vv
                return None
            dmg_total = pick(["TotalDamage","Damage","BaseDamage","total_damage","base_damage","attack_damage"])
            armor = pick(["armor","armour","defense","defence","protection"])
            block = pick(["blockpower","block","parry","parrypower","blockvalue"])
            if armor is not None:
                stats["armor"] = str(int(armor) if float(armor).is_integer() else round(armor,1))
            if dmg_total is not None:
                stats["damage_total"] = str(int(dmg_total) if float(dmg_total).is_integer() else round(dmg_total,1))
            if block is not None:
                stats["block"] = str(int(block) if float(block).is_integer() else round(block,1))
            recipe=[]
            for rm in re.finditer(r"^-\s*(?:Item|Prefab|Name)\s*:\s*([A-Za-z0-9_\-.]+).*?(?:Amount|Qty|Quantity)\s*:\s*([0-9]+)", text, re.IGNORECASE|re.MULTILINE|re.DOTALL):
                recipe.append((rm.group(1), int(rm.group(2))))
            if not recipe:
                im=re.search(r"(Resources|Recipe|Requirements)\s*:\s*([^\n]+)", text, re.IGNORECASE)
                if im:
                    vals=im.group(2)
                    for part in vals.split(","):
                        part=part.strip()
                        if ":" in part:
                            mat,qty=[p.strip() for p in part.split(":",1)]
                            try: recipe.append((mat,int(qty)))
                            except Exception: pass
            for prefab in prefab_candidates or {"(Unknown)"}:
                e=info.setdefault(prefab,{})
                if station: e["station"]=station
                if station_level is not None: e["station_level"]=station_level
                if tier is not None: e["tier"]=tier
                if world_level is not None: e["world_level"]=world_level
                if stats: e.setdefault("stats",{}).update(stats)
                if recipe: e["recipe"]=recipe
        return info

# ---------- UI ----------
class RevertPreview(tk.Toplevel):
    def __init__(self, parent, rel_path: str, diff_text: str, meta_old: str, meta_new: str):
        super().__init__(parent)
        self.title(f"Revert Preview — {rel_path}"); self.geometry("1000x650"); self.resizable(True, True)
        self.result=None
        frm=ttk.Frame(self, padding=10); frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text=rel_path, font=("Consolas", 11, "bold")).pack(anchor="w", pady=(0,6))
        ttk.Label(frm, text=f"Snapshot: {meta_old}   |   Current: {meta_new}", foreground="#888").pack(anchor="w", pady=(0,8))
        text=tk.Text(frm, wrap=tk.NONE, bg="#1e1e1e", fg="#eee", insertbackground="#eee")
        sy=ttk.Scrollbar(frm, orient=tk.VERTICAL, command=text.yview)
        sx=ttk.Scrollbar(frm, orient=tk.HORIZONTAL, command=text.xview)
        text.configure(yscrollcommand=sy.set, xscrollcommand=sx.set); text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        sy.pack(side=tk.RIGHT, fill=tk.Y); sx.pack(side=tk.BOTTOM, fill=tk.X)
        text.tag_configure("add", foreground="#9ece6a"); text.tag_configure("del", foreground="#f7768e"); text.tag_configure("hunk", foreground="#7aa2f7")
        for ln in diff_text.splitlines(True):
            tag=None
            if ln.startswith("+") and not ln.startswith("+++"): tag="add"
            elif ln.startswith("-") and not ln.startswith("---"): tag="del"
            elif ln.startswith("@@"): tag="hunk"
            text.insert("end", ln, tag if tag else ())
        text.config(state=tk.DISABLED)
        opts=ttk.Frame(frm); opts.pack(fill=tk.X, pady=8)
        self.do_backup=tk.BooleanVar(value=True); ttk.Checkbutton(opts, text="Backup current file before revert", variable=self.do_backup).pack(side=tk.LEFT)
        btns=ttk.Frame(frm); btns.pack(fill=tk.X)
        ttk.Button(btns, text="Cancel", command=self._cancel).pack(side=tk.RIGHT, padx=(6,0))
        ttk.Button(btns, text="Revert", style="Accent.TButton", command=self._ok).pack(side=tk.RIGHT)
        self.transient(parent); self.grab_set(); self.wait_visibility(); self.focus_set()
    def _ok(self): self.result={"backup": self.do_backup.get()}; self.destroy()
    def _cancel(self): self.result=None; self.destroy()

class ValheimConfigSuite(tk.Tk):
    def __init__(self, config_root: Path, vnei_root: Path, wdbulk_root: Path, prefs_file: Path):
        super().__init__()
        self.title("Valheim Config Suite — v2"); self.geometry("1660x980"); self.minsize(1120,720)
        self.style=ttk.Style()
        try: self.style.theme_use("clam")
        except Exception: pass
        self.colors={"bg":"#1f1f1f","panel":"#262626","text":"#e8e8e8","muted":"#aaaaaa","accent":"#7aa2f7","accent2":"#9ece6a"}
        self.configure(bg=self.colors["bg"])
        base_font=tkfont.Font(family="Consolas" if sys.platform.startswith("win") else "Courier New", size=10)
        for nm in ("TLabel","TButton","Treeview","Treeview.Heading","TEntry","TCombobox"):
            self.style.configure(nm, background=self.colors["panel"], foreground=self.colors["text"], font=base_font)
        self.style.configure("Treeview", fieldbackground=self.colors["panel"])
        self.style.configure("Accent.TButton", background=self.colors["accent"], foreground="#111")
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
        m_file.add_command(label="Quit", command=self.destroy)
        menubar.add_cascade(label="File", menu=m_file)
        m_help=tk.Menu(menubar, tearoff=False)
        m_help.add_command(label="Event Log", command=self._open_event_log)
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
        self.diff_text.tag_configure("add", foreground="#9ece6a"); self.diff_text.tag_configure("del", foreground="#f7768e"); self.diff_text.tag_configure("hunk", foreground="#7aa2f7")

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
        for k in ("station", "station_level", "tier", "world_level"):
            if k in d:
                lines.append(f"{k.replace('_',' ').title()}: {d[k]}")
        stats = d.get("stats")
        if stats:
            if isinstance(stats, dict):
                lines.append("Stats: " + ", ".join(f"{k} {v}" for k, v in stats.items()))
            else:
                lines.append(f"Stats: {stats}")
        if d.get("recipe"):
            lines.append("Recipe:")
            for mat, qty in d["recipe"]:
                lines.append(f"  - {mat}: {qty}")
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

    def _about(self):
        messagebox.showinfo("About", "Valheim Config Suite — v2\nBackups • Revert Preview • Profiles • Bulk Ops")

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
