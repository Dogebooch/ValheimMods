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


class PersistentState:
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.data: dict = {"highlights": {}, "last_paths": {}, "window": {}}
        self.load()

    def load(self) -> None:
        try:
            if self.state_file.exists():
                self.data = json.loads(self.state_file.read_text(encoding='utf-8'))
        except Exception:
            self.data = {"highlights": {}, "last_paths": {}, "window": {}}

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
        self.zoom_level = 1.0
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
            # If user chose a specific file before, prefer its parent as config_dir
            p = Path(lp["skill_file"]) 
            if p.exists():
                self.config_dir = p.parent

        self.vnei_index = VNEIItemIndex(self.vnei_dir)
        self.skill_config = SkillConfig(self.config_dir, filename_hint="ItemRequiresSkillLevel")
        if lp.get("skill_file"):
            self.skill_config.path = Path(lp["skill_file"]) 

        self._build_ui()
        self._index_icons()
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

        # Top controls
        top = ttk.Frame(self.root)
        top.pack(fill=tk.X, padx=8, pady=6)

        ttk.Button(top, text="Refresh", style="Action.TButton", command=self._refresh_data).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(top, text="Select VNEI Folder", style="Action.TButton", command=self._choose_vnei).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(top, text="Select Skill YAML", style="Action.TButton", command=self._choose_skill).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(top, text="Save Highlights", style="Action.TButton", command=self._persist_state).pack(side=tk.LEFT, padx=(0, 6))
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

        # Tree (use tree column for icon + item text)
        columns = ("station", "in_yaml", "highlight")
        self.tree = ttk.Treeview(self.root, columns=columns, show="tree headings")
        self.tree.heading("#0", text="Item")
        self.tree.heading("station", text="Crafting Station")
        self.tree.heading("in_yaml", text="In Skill YAML")
        self.tree.heading("highlight", text="Highlight")
        self.tree.column("#0", width=420)
        self.tree.column("station", width=260)
        self.tree.column("in_yaml", width=120)
        self.tree.column("highlight", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        yscroll = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Interactions
        self.tree.bind("<Double-1>", self._toggle_highlight)
        self.tree.bind("<space>", self._toggle_highlight)
        self.tree.bind("<Button-3>", self._show_context_menu)

        # Footer
        self.status = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status).pack(fill=tk.X, padx=8, pady=(0, 6))

        # Context menu
        self.menu = tk.Menu(self.root, tearoff=False)
        self.menu.add_command(label="Toggle Highlight", command=lambda: self._toggle_highlight(None))
        self.menu.add_command(label="Mark All Filtered", command=self._mark_all_filtered)
        self.menu.add_command(label="Unmark All Filtered", command=self._unmark_all_filtered)

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

    def _show_context_menu(self, event) -> None:
        try:
            rowid = self.tree.identify_row(event.y)
            if rowid:
                self.tree.selection_set(rowid)
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def _choose_vnei(self) -> None:
        chosen = filedialog.askdirectory(title="Select VNEI-Export Folder", initialdir=str(self.vnei_dir if self.vnei_dir.exists() else self.workspace))
        if chosen:
            self.vnei_dir = Path(chosen)
            self.state.data.setdefault("last_paths", {})["vnei_dir"] = str(self.vnei_dir)
            self._refresh_data()

    def _choose_skill(self) -> None:
        self.skill_config.pick_file()
        if self.skill_config.path:
            self.state.data.setdefault("last_paths", {})["skill_file"] = str(self.skill_config.path)
        self._refresh_data()

    def _persist_state(self) -> None:
        self.state.save()
        self.status.set(f"Saved at {datetime.now().strftime('%H:%M:%S')}")

    def _refresh_data(self) -> None:
        self.status.set("Loading VNEI items…")
        items = self.vnei_index.load_items()
        self.status.set("Loading skill YAML…")
        yaml_items = self.skill_config.load_items()

        # Rebuild table
        self.tree.delete(*self.tree.get_children())
        highlights: dict[str, bool] = self.state.data.setdefault("highlights", {})
        count_in_yaml = 0
        for item, station in sorted(items.items(), key=lambda kv: kv[0].lower()):
            in_yaml = item in yaml_items
            if in_yaml:
                count_in_yaml += 1
            marked = highlights.get(item, False)
            img = self._get_icon_for_item(item)
            # Build item kwargs and avoid passing an invalid/None image to Tcl
            item_kwargs = {
                "text": item,
                "values": (station or "", "Yes" if in_yaml else "No", "★" if marked else ""),
            }
            if img is not None:
                item_kwargs["image"] = img
            self.tree.insert("", "end", **item_kwargs)

        self.status.set(f"Loaded {len(items)} items; {count_in_yaml} in skill YAML. Use search to filter; double-click or Space to toggle highlight.")
        self._filter_rows()  # apply any current filter

    def _filter_rows(self) -> None:
        needle = (self.search_var.get() or "").strip().lower()
        for iid in self.tree.get_children(""):
            vals = self.tree.item(iid).get('values', [])
            text = (self.tree.item(iid).get('text', '') + ' ' + ' '.join(str(v) for v in vals[:1])).lower()
            if needle in text:
                self.tree.reattach(iid, '', 'end')
            else:
                self.tree.detach(iid)

    def _toggle_highlight(self, event) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = list(self.tree.item(iid).get('values', []))
        if len(vals) < 3:
            return
        item_name = self.tree.item(iid).get('text', '')
        highlighted = (vals[2] == "★")
        vals[2] = "" if highlighted else "★"
        self.tree.item(iid, values=vals)
        self.state.data.setdefault("highlights", {})[item_name] = not highlighted
        # Save immediately for persistence
        self.state.save()

    def _mark_all_filtered(self) -> None:
        for iid in self.tree.get_children(""):
            vals = list(self.tree.item(iid).get('values', []))
            if len(vals) < 3:
                continue
            item_name = self.tree.item(iid).get('text', '')
            vals[2] = "★"
            self.tree.item(iid, values=vals)
            self.state.data.setdefault("highlights", {})[item_name] = True
        self.state.save()

    def _unmark_all_filtered(self) -> None:
        for iid in self.tree.get_children(""):
            vals = list(self.tree.item(iid).get('values', []))
            if len(vals) < 3:
                continue
            item_name = self.tree.item(iid).get('text', '')
            vals[2] = ""
            self.tree.item(iid, values=vals)
            self.state.data.setdefault("highlights", {})[item_name] = False
        self.state.save()

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


