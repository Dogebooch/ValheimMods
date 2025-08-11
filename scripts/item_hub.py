import csv
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont


class ItemHubApp(tk.Tk):
    """A central hub GUI for tracking Valheim items with persistence.

    - Reads items from VNEI export CSV: VNEI.indexed.items.csv
    - Displays list with icons and supports filtering by Item Type and text search
    - Persists per-item notes/tags/status to a JSON file across sessions
    """

    CSV_FILENAME = "VNEI.indexed.items.csv"
    ICONS_DIRNAME = "icons"
    PERSIST_FILENAME = "item_changes.json"

    def __init__(self, vnei_dir: Optional[str] = None):
        super().__init__()
        self.title("Valheim Item Hub")

        # Color palette (forest/earth tones, soft oranges; avoid white)
        self.palette = {
            "bg": "#1e2a22",  # deep forest green
            "panel": "#243529",  # darker green panel
            "list_bg": "#2c3e30",  # muted green
            "list_alt": "#324a3a",  # alternate row
            "accent": "#d9a066",  # soft orange
            "accent2": "#b07d62",  # earthy brown/orange
            "text_primary": "#e4d9c5",  # warm pastel beige
            "text_muted": "#cbbba3",
            "border": "#3a523f",
            "button": "#36543f",
            "entry_bg": "#304536",
            "entry_fg": "#e4d9c5",
            "sel_bg": "#355e3b",
            "sel_fg": "#f0e6d6",
        }

        self.configure(bg=self.palette["bg"])
        # Zoom and fonts
        self.zoom = 1.0
        self._init_fonts()
        self._init_style()

        # Resolve paths
        self.script_dir = os.path.abspath(os.path.dirname(__file__))
        default_vnei_dir = os.path.abspath(
            os.path.join(
                self.script_dir,
                "..",
                "Valheim",
                "profiles",
                "Dogeheim_Player",
                "BepInEx",
                "VNEI-Export",
            )
        )
        self.vnei_dir = os.path.abspath(vnei_dir or default_vnei_dir)
        self.csv_path = os.path.join(self.vnei_dir, self.CSV_FILENAME)
        self.icons_dir = os.path.join(self.vnei_dir, self.ICONS_DIRNAME)
        self.persist_path = os.path.join(self.script_dir, self.PERSIST_FILENAME)
        self.items_cache_path = os.path.join(self.script_dir, ".items_cache.json")

        # Data
        self.items: List[Dict[str, str]] = []
        self.filtered_items: List[Dict[str, str]] = []
        self.item_types: List[str] = []
        self.changes: Dict[str, Dict] = {}  # internal name -> metadata
        self.growables: set[str] = set()
        self.internal_to_localized: Dict[str, str] = {}

        # Images
        self.photo_cache: Dict[str, ImageTk.PhotoImage] = {}
        self.missing_icon_cache: Dict[int, ImageTk.PhotoImage] = {}
        # Where to search for icons (VNEI export and Jotunn cached icons)
        self.icon_search_dirs: List[str] = [
            self.icons_dir,
            os.path.abspath(
                os.path.join(
                    self.script_dir,
                    "..",
                    "Valheim_Help_Docs",
                    "Valheim_PlayerWorldData",
                    "Jotunn",
                    "CachedIcons",
                )
            ),
        ]
        # Note: Removed config change tracking; simplifying the app

        # UI Vars
        self.var_filter_type = tk.StringVar(value="All")
        self.var_search = tk.StringVar()
        self.var_status = tk.StringVar(value="")
        self.var_only_growables = tk.BooleanVar(value=False)

        # Build UI
        self._build_layout()

        # Load data
        self._load_items()
        self._load_growables()
        self._load_recipes()
        self._load_changes()
        self._refresh_types()
        self._apply_filters()

        # Window geometry persistence (optional, best-effort)
        self._restore_geometry()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------------------------
    # Styling
    # ---------------------------
    def _init_fonts(self):
        # Named fonts so updating size propagates automatically
        self.font_base = tkfont.Font(family="Segoe UI", size=10)
        self.font_text = tkfont.Font(family="Segoe UI", size=10)
        self.font_heading = tkfont.Font(family="Segoe UI", size=12, weight="bold")

    def _icon_size(self) -> int:
        return max(16, int(24 * self.zoom))

    def _row_height(self) -> int:
        return max(22, self._icon_size() + 6)

    def _apply_zoom(self):
        base = max(8, int(10 * self.zoom))
        head = max(10, int(12 * self.zoom))
        self.font_base.configure(size=base, weight="normal")
        self.font_text.configure(size=base)
        self.font_heading.configure(size=head)

        style = ttk.Style()
        style.configure("TLabel", font=self.font_base)
        style.configure("TButton", font=self.font_base)
        style.configure("TCheckbutton", font=self.font_base)
        style.configure("TCombobox", font=self.font_base)
        style.configure("Treeview", font=self.font_base, rowheight=self._row_height())
        style.configure("Treeview.Heading", font=self.font_base)

        # Rebuild icons at new size
        self.photo_cache.clear()
        # Refresh current list to re-render icons and row height
        if hasattr(self, "filtered_items"):
            self._populate_tree()

    def _set_zoom(self, value: float):
        try:
            value = float(value)
        except Exception:
            return
        value = max(0.8, min(2.0, value))
        if abs(value - self.zoom) < 1e-3:
            return
        self.zoom = value
        self._apply_zoom()

    def _zoom_in(self):
        self._set_zoom(self.zoom + 0.1)

    def _zoom_out(self):
        self._set_zoom(self.zoom - 0.1)

    def _zoom_reset(self):
        self._set_zoom(1.0)

    def _init_style(self):
        style = ttk.Style()
        # Use 'clam' for better color support
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "TFrame",
            background=self.palette["panel"],
            bordercolor=self.palette["border"],
        )
        style.configure(
            "TLabel",
            background=self.palette["panel"],
            foreground=self.palette["text_primary"],
            font=self.font_base,
        )
        style.configure(
            "TButton",
            background=self.palette["button"],
            foreground=self.palette["text_primary"],
            focuscolor=self.palette["accent"],
            font=self.font_base,
        )
        style.map("TButton", background=[("active", self.palette["accent2"])])
        style.configure(
            "TCombobox",
            fieldbackground=self.palette["entry_bg"],
            background=self.palette["entry_bg"],
            foreground=self.palette["entry_fg"],
            font=self.font_base,
        )
        style.configure(
            "Treeview",
            background=self.palette["list_bg"],
            fieldbackground=self.palette["list_bg"],
            foreground=self.palette["text_primary"],
            bordercolor=self.palette["border"],
            font=self.font_base,
            rowheight=self._row_height(),
        )
        style.configure("Treeview.Heading", font=self.font_base)
        style.map(
            "Treeview",
            background=[("selected", self.palette["sel_bg"])],
            foreground=[("selected", self.palette["sel_fg"])],
        )

    # ---------------------------
    # UI
    # ---------------------------
    def _build_layout(self):
        # Top filter bar
        top = ttk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        ttk.Label(top, text="Item Type").pack(side=tk.LEFT)
        self.cmb_type = ttk.Combobox(top, textvariable=self.var_filter_type, state="readonly")
        self.cmb_type.pack(side=tk.LEFT, padx=(6, 12))
        self.cmb_type.bind("<<ComboboxSelected>>", lambda e: self._apply_filters())

        ttk.Label(top, text="Search").pack(side=tk.LEFT)
        ent_search = ttk.Entry(top, textvariable=self.var_search, font=self.font_text)
        ent_search.pack(side=tk.LEFT, padx=(6, 12), fill=tk.X, expand=True)
        ent_search.bind("<KeyRelease>", lambda e: self._apply_filters())

        chk_grow = ttk.Checkbutton(top, text="Growables only", variable=self.var_only_growables, command=self._apply_filters)
        chk_grow.pack(side=tk.LEFT, padx=(0, 12))

        btn_clear = ttk.Button(top, text="Clear Filters", command=self._clear_filters)
        btn_clear.pack(side=tk.LEFT)

        # Zoom controls
        ttk.Label(top, text="Zoom").pack(side=tk.LEFT, padx=(12, 4))
        ttk.Button(top, text="−", width=3, command=self._zoom_out).pack(side=tk.LEFT)
        ttk.Button(top, text="+", width=3, command=self._zoom_in).pack(side=tk.LEFT, padx=(2, 0))
        ttk.Button(top, text="Reset", command=self._zoom_reset).pack(side=tk.LEFT, padx=(6, 0))

        # Main split: list (left) and details (right)
        main = ttk.Frame(self)
        main.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Left: Treeview
        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Use the tree column (#0) to show item name + icon.
        # Additional columns hold metadata. First column 'done' acts as a checkbox.
        # We will add a 'grow' indicator column later after growables are loaded
        columns = ("done", "type", "mod", "internal")
        self.tree = ttk.Treeview(
            left,
            columns=columns,
            show="tree headings",
            selectmode="browse",
        )
        # Tree column heading
        self.tree.heading("#0", text="Item")
        self.tree.heading("done", text="Done")
        self.tree.heading("type", text="Item Type")
        self.tree.heading("mod", text="Source Mod")
        self.tree.heading("internal", text="Internal Name")
        self.tree.column("#0", width=300, anchor=tk.W)
        self.tree.column("done", width=60, anchor=tk.CENTER)
        self.tree.column("type", width=140, anchor=tk.W)
        self.tree.column("mod", width=120, anchor=tk.W)
        self.tree.column("internal", width=180, anchor=tk.W)

        vsb = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.LEFT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_select_item)
        # Toggle checkbox on click in 'done' column
        self.tree.bind("<Button-1>", self._on_tree_click)

        # Right: Details panel
        right = ttk.Frame(main)
        right.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

        ttk.Label(right, text="Item Details", font=self.font_heading, foreground=self.palette["accent"]).pack(anchor=tk.W)

        self.lbl_name = ttk.Label(right, text="Name: -")
        self.lbl_name.pack(anchor=tk.W, pady=(6, 0))

        self.lbl_type = ttk.Label(right, text="Type: -")
        self.lbl_type.pack(anchor=tk.W)

        self.lbl_internal = ttk.Label(right, text="Internal: -")
        self.lbl_internal.pack(anchor=tk.W)

        self.lbl_mod = ttk.Label(right, text="Source Mod: -")
        self.lbl_mod.pack(anchor=tk.W, pady=(0, 10))

        # Crafting info
        ttk.Label(right, text="Crafting Station").pack(anchor=tk.W)
        self.lbl_station = ttk.Label(right, text="-")
        self.lbl_station.pack(anchor=tk.W, pady=(0, 6))

        ttk.Label(right, text="Recipe (Ingredients)").pack(anchor=tk.W)
        self.txt_recipe = tk.Text(
            right,
            height=6,
            width=40,
            state="disabled",
            bg=self.palette["entry_bg"],
            fg=self.palette["entry_fg"],
            insertbackground=self.palette["entry_fg"],
            font=self.font_text,
        )
        self.txt_recipe.pack(fill=tk.BOTH, expand=False, pady=(0, 8))

        frm_status = ttk.Frame(right)
        frm_status.pack(fill=tk.X, pady=(4, 4))
        ttk.Label(frm_status, text="Status").pack(side=tk.LEFT)
        self.var_item_status = tk.StringVar(value="")
        self.cmb_status = ttk.Combobox(
            frm_status,
            textvariable=self.var_item_status,
            state="readonly",
            values=["", "todo", "in-progress", "done"],
        )
        self.cmb_status.pack(side=tk.LEFT, padx=(6, 0))

        ttk.Label(right, text="Tags (comma-separated)").pack(anchor=tk.W)
        self.txt_tags = tk.Text(right, height=2, width=40, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"], font=self.font_text)
        self.txt_tags.pack(fill=tk.X)

        ttk.Label(right, text="Notes").pack(anchor=tk.W)
        self.txt_notes = tk.Text(right, height=12, width=40, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"], font=self.font_text)
        self.txt_notes.pack(fill=tk.BOTH, expand=False)

        frm_actions = ttk.Frame(right)
        frm_actions.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(frm_actions, text="Save", command=self._save_current_item).pack(side=tk.LEFT)
        ttk.Button(frm_actions, text="Save All", command=self._save_changes).pack(side=tk.LEFT, padx=(8, 0))

        # Status bar
        status = ttk.Frame(self)
        status.pack(side=tk.BOTTOM, fill=tk.X)
        self.lbl_status = ttk.Label(status, textvariable=self.var_status)
        self.lbl_status.pack(side=tk.LEFT, padx=10)

    # ---------------------------
    # Data Loading & Persistence
    # ---------------------------
    def _load_items(self):
        # Use a lightweight cache to speed startup when CSV hasn't changed
        def read_csv_items(path: str) -> List[Dict[str, str]]:
            out: List[Dict[str, str]] = []
            with open(path, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    item = {
                        "Internal Name": row.get("Internal Name", "").strip(),
                        "Localized Name": row.get("Localized Name", "").strip(),
                        "Item Type": row.get("Item Type", "").strip() or "Undefined",
                        "Description": row.get("Description", "").strip(),
                        "Source Mod": row.get("Source Mod", "").strip() or "Valheim",
                    }
                    if item["Internal Name"]:
                        out.append(item)
            return out

        csv_exists = os.path.isfile(self.csv_path)
        cache_loaded = False

        # Try cache first
        if os.path.isfile(self.items_cache_path):
            try:
                with open(self.items_cache_path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                cached_items = cache.get("items", [])
                cached_meta = cache.get("meta", {})
                cached_csv = cached_meta.get("csv_path")
                cached_mtime = cached_meta.get("csv_mtime")
                cached_size = cached_meta.get("csv_size")
                if csv_exists:
                    st = os.stat(self.csv_path)
                    if (
                        os.path.abspath(cached_csv or "") == os.path.abspath(self.csv_path)
                        and int(cached_mtime or 0) == int(st.st_mtime)
                        and int(cached_size or -1) == int(st.st_size)
                        and isinstance(cached_items, list)
                    ):
                        self.items = cached_items
                        cache_loaded = True
                else:
                    # CSV missing; fall back to cached items if any
                    if isinstance(cached_items, list) and cached_items:
                        self.items = cached_items
                        cache_loaded = True
            except Exception:
                cache_loaded = False

        if not cache_loaded:
            if not csv_exists:
                messagebox.showerror("Missing CSV", f"Could not find VNEI CSV at:\n{self.csv_path}")
                self.destroy()
                return
            # Parse fresh and write cache
            items = read_csv_items(self.csv_path)
            self.items = items
            try:
                st = os.stat(self.csv_path)
                cache = {
                    "meta": {
                        "csv_path": os.path.abspath(self.csv_path),
                        "csv_mtime": int(st.st_mtime),
                        "csv_size": int(st.st_size),
                        "cached_at": datetime.utcnow().isoformat() + "Z",
                    },
                    "items": self.items,
                }
                with open(self.items_cache_path, "w", encoding="utf-8") as f:
                    json.dump(cache, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

        self.internal_to_localized = {it["Internal Name"]: it.get("Localized Name", it["Internal Name"]) for it in self.items}
        if cache_loaded:
            self._set_status("Loaded items from cache")

    def _load_changes(self):
        if os.path.isfile(self.persist_path):
            try:
                with open(self.persist_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.changes = data.get("items", {})
            except Exception:
                self.changes = {}
        else:
            self.changes = {}

    def _save_changes(self):
        data = {
            "last_modified": int(time.time()),
            "last_modified_iso": datetime.utcnow().isoformat() + "Z",
            "items": self.changes,
        }
        try:
            with open(self.persist_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self._set_status("Changes saved.")
        except Exception as exc:
            messagebox.showerror("Save Failed", str(exc))

    # ---------------------------
    # Filters & List
    # ---------------------------
    def _refresh_types(self):
        types = sorted({it["Item Type"] or "Undefined" for it in self.items})
        self.item_types = ["All"] + types
        self.cmb_type["values"] = self.item_types
        if self.var_filter_type.get() not in self.item_types:
            self.var_filter_type.set("All")

    def _apply_filters(self):
        q = self.var_search.get().strip().lower()
        sel_type = self.var_filter_type.get()

        def match(it: Dict[str, str]) -> bool:
            if sel_type and sel_type != "All" and it.get("Item Type") != sel_type:
                return False
            if q:
                hay = " ".join([
                    it.get("Localized Name", ""),
                    it.get("Internal Name", ""),
                    it.get("Item Type", ""),
                    it.get("Source Mod", ""),
                ]).lower()
                if q not in hay:
                    return False
            if self.var_only_growables.get():
                return it.get("Internal Name", "") in self.growables
            return True

        self.filtered_items = [it for it in self.items if match(it)]
        self._populate_tree()

    def _clear_filters(self):
        self.var_filter_type.set("All")
        self.var_search.set("")
        self.var_only_growables.set(False)
        self._apply_filters()

    # ---------------------------
    # Growables: parse PlantEverything to discover plantable items
    # ---------------------------
    def _load_growables(self):
        self.growables = set()
        # Build lookups for mapping arbitrary names to internal names
        internal_by_internal = {it.get("Internal Name", ""): it.get("Internal Name", "") for it in self.items}
        internal_by_internal_lower = {k.lower(): v for k, v in internal_by_internal.items()}
        internal_by_localized_lower = {it.get("Localized Name", "").lower(): it.get("Internal Name", "") for it in self.items}
        # Also support some common PlantEverything keys directly → internal names
        direct_map = {
            "barley": "Barley",
            "carrot": "Carrot",
            "flax": "Flax",
            "onion": "Onion",
            "seedcarrot": "SeedCarrot",
            "seedonion": "SeedOnion",
            "seedturnip": "SeedTurnip",
            "turnip": "Turnip",
            "magecap": "Magecap",
            "jotunpuffs": "JotunPuffs",
            "raspberry": "RaspberryBush",  # icon shows bush; internal may be Pickable_Raspberry etc.
            "blueberry": "Blueberries",
            "cloudberry": "Cloudberry",
            "dandelion": "Dandelion",
            "thistle": "Thistle",
            "mushroom": "Mushroom",
            "yellowmushroom": "MushroomYellow",
            "bluemushroom": "MushroomBlue",
            "smokepuff": "Smokepuff",
        }

        # Locate PlantEverything config
        pe_cfg = os.path.abspath(os.path.join(self.script_dir, "..", "Valheim", "profiles", "Dogeheim_Player", "BepInEx", "config", "advize.PlantEverything.cfg"))
        if not os.path.isfile(pe_cfg):
            return
        try:
            with open(pe_cfg, "r", encoding="utf-8") as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith("#") or line.startswith("##"):
                        continue
                    if "Cost =" in line:
                        # Example: BarleyCost = 1
                        parts = line.split("=", 1)
                        if len(parts) != 2:
                            continue
                        left = parts[0].strip()
                        right = parts[1].strip()
                        # Skip disabled (0 cost means disabled planting according to doc; keep >0)
                        try:
                            cost_val = int(right)
                        except ValueError:
                            continue
                        if cost_val <= 0:
                            continue
                        if left.endswith("Cost"):
                            name = left[:-4].strip()  # drop 'Cost'
                        else:
                            name = left

                        def map_name(n: str) -> str | None:
                            nl = n.lower()
                            if nl in direct_map:
                                target = direct_map[nl]
                                # Return matching internal if present
                                if target.lower() in internal_by_internal_lower:
                                    return internal_by_internal_lower[target.lower()]
                                if target.lower() in internal_by_localized_lower:
                                    return internal_by_localized_lower[target.lower()]
                            if nl in internal_by_internal_lower:
                                return internal_by_internal_lower[nl]
                            if nl in internal_by_localized_lower:
                                return internal_by_localized_lower[nl]
                            # Try simple pluralization variants
                            if nl.endswith("y"):
                                alt = nl[:-1] + "ies"
                                if alt in internal_by_internal_lower:
                                    return internal_by_internal_lower[alt]
                                if alt in internal_by_localized_lower:
                                    return internal_by_localized_lower[alt]
                            if not nl.endswith("s"):
                                alt = nl + "s"
                                if alt in internal_by_internal_lower:
                                    return internal_by_internal_lower[alt]
                                if alt in internal_by_localized_lower:
                                    return internal_by_localized_lower[alt]
                            return None

                        mapped = map_name(name)
                        if mapped:
                            self.growables.add(mapped)
        except Exception:
            # ignore parse errors gracefully
            pass

    def _populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        count = 0
        # Ensure grow column exists if we have growables info
        if "grow" not in self.tree["columns"]:
            new_cols = ("done", "grow", "type", "mod", "internal")
            self.tree.configure(columns=new_cols)
            self.tree.heading("grow", text="Grow")
            self.tree.column("grow", width=60, anchor=tk.CENTER)

        for idx, it in enumerate(self.filtered_items):
            internal = it.get("Internal Name", "")
            localized = it.get("Localized Name", internal)
            icon = self._get_icon_for_item(internal)
            checked = False
            meta = self.changes.get(internal)
            if isinstance(meta, dict):
                checked = bool(meta.get("checked", False))
            done_symbol = "☑" if checked else "☐"
            grow_symbol = "🌱" if internal in self.growables else ""
            iid = self.tree.insert(
                "",
                tk.END,
                text=localized,
                image=icon,
                values=(done_symbol, grow_symbol, it.get("Item Type", ""), it.get("Source Mod", ""), internal),
            )
            count += 1
        self._set_status(f"Showing {count} of {len(self.items)} items")

    # ---------------------------
    # Icons
    # ---------------------------
    def _ensure_missing_icon(self) -> Optional[ImageTk.PhotoImage]:
        if Image is None or ImageTk is None:
            return None
        size = self._icon_size()
        if size in self.missing_icon_cache:
            return self.missing_icon_cache[size]
        img = Image.new("RGBA", (size, size), self.palette["accent2"])  # soft earthy square
        photo = ImageTk.PhotoImage(img)
        self.missing_icon_cache[size] = photo
        return photo

    def _get_icon_for_item(self, internal_name: str) -> Optional[ImageTk.PhotoImage]:
        if Image is None or ImageTk is None:
            return None

        size = self._icon_size()
        key = f"{internal_name.lower()}@{size}"
        if key in self.photo_cache:
            return self.photo_cache[key]

        # Attempt to find icon file in icons dir by several strategies
        icon_path = None
        lowered = internal_name.lower()
        # Search through multiple directories
        for base_dir in self.icon_search_dirs:
            if not os.path.isdir(base_dir):
                continue
            # 1) Exact match
            for ext in (".png", ".jpg", ".jpeg"):
                candidate = os.path.join(base_dir, internal_name + ext)
                if os.path.isfile(candidate):
                    icon_path = candidate
                    break
            if icon_path:
                break
            # 2) Start-with match on internal name
            try:
                for fname in os.listdir(base_dir):
                    fnl = fname.lower()
                    if not fnl.endswith((".png", ".jpg", ".jpeg")):
                        continue
                    if fnl.startswith(lowered):
                        icon_path = os.path.join(base_dir, fname)
                        break
                if icon_path:
                    break
            except Exception:
                pass
            # 3) Try localized name variants
            loc = self.internal_to_localized.get(internal_name, internal_name)
            loc_low = loc.lower().replace(" ", "_")
            for ext in (".png", ".jpg", ".jpeg"):
                candidate = os.path.join(base_dir, loc + ext)
                candidate2 = os.path.join(base_dir, loc_low + ext)
                if os.path.isfile(candidate):
                    icon_path = candidate
                    break
                if os.path.isfile(candidate2):
                    icon_path = candidate2
                    break
            if icon_path:
                break

        try:
            if icon_path and os.path.isfile(icon_path):
                img = Image.open(icon_path).convert("RGBA")
                img.thumbnail((size, size), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.photo_cache[key] = photo
                return photo
        except Exception:
            pass

        return self._ensure_missing_icon()

    # ---------------------------
    # Selection & Editing
    # ---------------------------
    def _on_select_item(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        # Read from tree column (#0) and value columns
        localized = self.tree.item(iid, "text") or "-"
        vals = self.tree.item(iid, "values") or ("", "", "", "", "")
        # values order (after grow column added): done, grow, type, mod, internal
        item_type = vals[2] if len(vals) > 2 else ""
        source_mod = vals[3] if len(vals) > 3 else ""
        internal = vals[4] if len(vals) > 4 else ""

        self.lbl_name.config(text=f"Name: {localized}")
        self.lbl_type.config(text=f"Type: {item_type}")
        self.lbl_internal.config(text=f"Internal: {internal}")
        self.lbl_mod.config(text=f"Source Mod: {source_mod}")
        # Update crafting details
        station, ingredients = self._lookup_recipe(internal)
        self.lbl_station.config(text=station or "-")
        self._set_text_readonly(self.txt_recipe, self._format_ingredients(ingredients))

        meta = self.changes.get(internal, {})
        self.var_item_status.set(meta.get("status", ""))
        self._set_text(self.txt_tags, ", ".join(meta.get("tags", [])))
        self._set_text(self.txt_notes, meta.get("notes", ""))

    def _on_tree_click(self, event):
        # Toggle checkbox if clicking in 'done' column
        col = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)
        if not row:
            return
        if col != "#1":  # '#1' corresponds to first data column i.e., 'done'
            return

        vals = self.tree.item(row, "values") or ("", "", "", "")
        if len(vals) < 4:
            return
        internal = vals[3]
        current_symbol = vals[0]
        new_checked = False if current_symbol == "☑" else True
        new_symbol = "☑" if new_checked else "☐"
        # Update tree cell
        self.tree.set(row, "done", new_symbol)
        # Update persistence
        meta = self.changes.get(internal) or {}
        meta["checked"] = new_checked
        meta.setdefault("notes", meta.get("notes", ""))
        meta.setdefault("tags", meta.get("tags", []))
        meta.setdefault("status", meta.get("status", ""))
        meta["last_updated"] = datetime.utcnow().isoformat() + "Z"
        self.changes[internal] = meta
        self._save_changes()

    def _set_text(self, widget: tk.Text, text: str):
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)

    def _set_text_readonly(self, widget: tk.Text, text: str):
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def _save_current_item(self):
        sel = self.tree.selection()
        if not sel:
            self._set_status("No item selected.")
            return
        iid = sel[0]
        vals = self.tree.item(iid, values=True)
        internal = vals[3]

        notes = self.txt_notes.get("1.0", tk.END).strip()
        tags_str = self.txt_tags.get("1.0", tk.END).strip()
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        status = self.var_item_status.get().strip()

        self.changes[internal] = {
            "notes": notes,
            "tags": tags,
            "status": status,
            "last_updated": datetime.utcnow().isoformat() + "Z",
        }
        self._save_changes()

    # ---------------------------
    # Recipes (optional data source)
    # ---------------------------
    def _load_recipes(self):
        """Load recipes if an index file exists.

        Supported (searched in order):
          - VNEI-Export/VNEI.recipes.csv with columns: Internal Name, Station, Ingredients
              Ingredients example: Wood:10; Stone:2; Resin:3
          - scripts/item_recipes.json mapping internal -> {"station": str, "ingredients": [[name, qty], ...]}
        If none is present, crafting info will show as unavailable.
        """
        self.recipes: Dict[str, Dict] = {}
        # CSV in VNEI dir
        csv_recipes = os.path.join(self.vnei_dir, "VNEI.recipes.csv")
        if os.path.isfile(csv_recipes):
            try:
                with open(csv_recipes, "r", encoding="utf-8-sig", newline="") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        key = (row.get("Internal Name") or "").strip()
                        if not key:
                            continue
                        station = (row.get("Station") or "").strip()
                        ing = (row.get("Ingredients") or "").strip()
                        ingredients = []
                        if ing:
                            parts = [p.strip() for p in ing.split(";") if p.strip()]
                            for p in parts:
                                if ":" in p:
                                    n, q = p.split(":", 1)
                                    try:
                                        qv = int(q)
                                    except ValueError:
                                        qv = q.strip()
                                    ingredients.append([n.strip(), qv])
                                else:
                                    ingredients.append([p, "?"])
                        self.recipes[key] = {"station": station, "ingredients": ingredients}
                return
            except Exception:
                pass

        # JSON fallback in scripts dir
        json_path = os.path.join(self.script_dir, "item_recipes.json")
        if os.path.isfile(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self.recipes = data
            except Exception:
                self.recipes = {}
        else:
            self.recipes = {}

    def _lookup_recipe(self, internal_name: str) -> Tuple[Optional[str], List[List]]:
        meta = self.recipes.get(internal_name) if hasattr(self, "recipes") else None
        if not meta:
            return None, []
        return meta.get("station"), meta.get("ingredients", [])

    def _format_ingredients(self, ingredients: List[List]) -> str:
        if not ingredients:
            return "(No recipe data available)"
        lines = []
        for pair in ingredients:
            if isinstance(pair, (list, tuple)) and len(pair) >= 1:
                name = str(pair[0])
                qty = str(pair[1]) if len(pair) > 1 else "?"
                lines.append(f"- {name}: {qty}")
        return "\n".join(lines)

    # ---------------------------
    # Window geometry persistence
    # ---------------------------
    def _restore_geometry(self):
        try:
            geo_path = os.path.join(self.script_dir, ".item_hub_geometry.json")
            if os.path.isfile(geo_path):
                with open(geo_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                geo = data.get("geometry")
                if geo:
                    self.geometry(geo)
        except Exception:
            pass

    def _save_geometry(self):
        try:
            geo = self.geometry()
            geo_path = os.path.join(self.script_dir, ".item_hub_geometry.json")
            with open(geo_path, "w", encoding="utf-8") as f:
                json.dump({"geometry": geo}, f)
        except Exception:
            pass

    def _on_close(self):
        self._save_geometry()
        self.destroy()

    # ---------------------------
    # Utils
    # ---------------------------
    def _set_status(self, text: str):
        self.var_status.set(text)

    # ---------------------------
    # Changes Viewer (Config diffs + Changelog links)
    # ---------------------------
    def _open_changes_viewer(self):
        win = tk.Toplevel(self)
        win.title("What's Changed")
        win.configure(bg=self.palette["bg"])

        # Controls
        ctrl = ttk.Frame(win)
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)
        # Simple/Advanced toggle
        self.var_simple_view = tk.BooleanVar(value=True)
        ttk.Checkbutton(ctrl, text="Simple view", variable=self.var_simple_view, command=lambda: toggle_simple()).pack(side=tk.LEFT)
        self.var_changes_only = tk.BooleanVar(value=True)
        ttk.Checkbutton(ctrl, text="Only changed files", variable=self.var_changes_only, command=lambda: self._populate_changes_list(lst)).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Label(ctrl, text="Filter files").pack(side=tk.LEFT, padx=(12, 4))
        var_filter = tk.StringVar()
        ent = ttk.Entry(ctrl, textvariable=var_filter)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(ctrl, text="Scan for changes", command=lambda: self._populate_changes_list(lst, name_filter=var_filter.get().strip().lower())).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(ctrl, text="Remember as normal", command=lambda: self._update_config_baseline(lst, var_filter.get().strip().lower())).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(ctrl, text="Open Change Log", command=self._open_changelog_viewer).pack(side=tk.LEFT, padx=(8, 0))

        # Permanent-sync controls
        ttk.Button(ctrl, text="Mark Permanent (selected)", command=lambda: self._mark_permanent(lst)).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(ctrl, text="Remove Permanent", command=lambda: self._unmark_permanent(lst)).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(ctrl, text="Restore selected", command=lambda: self._restore_selected_from_permanent(lst)).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(ctrl, text="Fresh Sync of config", command=self._fresh_sync_permanent_all).pack(side=tk.LEFT, padx=(8, 0))

        # Baseline mode selector
        ttk.Label(ctrl, text="Baseline").pack(side=tk.LEFT, padx=(12, 4))
        self.var_baseline_mode = tk.StringVar(value="Snapshot")
        cmb_mode = ttk.Combobox(ctrl, textvariable=self.var_baseline_mode, state="readonly", values=["Snapshot", "Git HEAD", "In-File Defaults", "Mod Cache"])
        cmb_mode.pack(side=tk.LEFT)

        body = ttk.Frame(win)
        body.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Friendly help
        helpf = ttk.Frame(win)
        helpf.pack(fill=tk.X, padx=8)
        ttk.Label(helpf, text="Tip: Click a file on the left. Simple view shows a friendly summary. Switch to Advanced to see the full diff.", foreground=self.palette["text_muted"]).pack(anchor=tk.W)

        # Left: files list
        left = ttk.Frame(body)
        left.pack(side=tk.LEFT, fill=tk.Y)
        lst = ttk.Treeview(left, columns=("status",), show="tree headings", height=20)
        lst.heading("#0", text="File")
        lst.heading("status", text="Changed?")
        lst.column("#0", width=420, anchor=tk.W)
        lst.column("status", width=100, anchor=tk.W)
        sb = ttk.Scrollbar(left, orient="vertical", command=lst.yview)
        lst.configure(yscroll=sb.set)
        lst.pack(side=tk.LEFT, fill=tk.Y)
        sb.pack(side=tk.LEFT, fill=tk.Y)

        # Right: diff and changelog
        right = ttk.Frame(body)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))
        # Simple summary view
        ttk.Label(right, text="Summary of Changes", foreground=self.palette["accent"]).pack(anchor=tk.W)
        txt_summary = tk.Text(right, height=12, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"], font=self.font_text)
        txt_summary.pack(fill=tk.BOTH, expand=False)

        # Advanced diff view
        lbl_diff_title = ttk.Label(right, text="Diff", foreground=self.palette["accent"]) ; lbl_diff_title.pack(anchor=tk.W)
        txt_diff = tk.Text(right, height=14, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"], font=self.font_text)
        txt_diff.pack(fill=tk.BOTH, expand=True)

        ttk.Label(right, text="Related Change Log Entries", foreground=self.palette["accent"]).pack(anchor=tk.W, pady=(6, 0))
        txt_log = tk.Text(right, height=8, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"], font=self.font_text)
        txt_log.pack(fill=tk.BOTH, expand=False)

        def refresh_detail(event=None):
            sel = lst.selection()
            if not sel:
                return
            fpath = lst.item(sel[0], "text")
            mode = self.var_baseline_mode.get()
            lbl_diff_title.config(text=f"Diff vs {mode}")
            # Summary
            summary = self._summarize_changes(fpath, mode)
            txt_summary.configure(state="normal"); txt_summary.delete("1.0", tk.END); txt_summary.insert("1.0", summary or "(No changes)"); txt_summary.configure(state="disabled")
            # Diff
            diff_text = self._diff_file_vs_mode(fpath, mode)
            txt_diff.configure(state="normal"); txt_diff.delete("1.0", tk.END); txt_diff.insert("1.0", diff_text); txt_diff.configure(state="disabled")
            logs = self._find_changelog_entries_for_file(fpath)
            txt_log.configure(state="normal"); txt_log.delete("1.0", tk.END); txt_log.insert("1.0", logs or "(No related entries)"); txt_log.configure(state="disabled")

        lst.bind("<<TreeviewSelect>>", refresh_detail)

        def on_filter_change(*_):
            self._populate_changes_list(lst, name_filter=var_filter.get().strip().lower())

        var_filter.trace_add("write", on_filter_change)
        def toggle_simple():
            simple = self.var_simple_view.get()
            if simple:
                txt_summary.pack_configure(fill=tk.BOTH, expand=False)
                txt_diff.pack_configure_forget = False
                # Reduce diff visibility by shrinking height
                txt_diff.configure(height=8)
            else:
                txt_diff.configure(height=18)
            refresh_detail()

        self._populate_changes_list(lst)
        toggle_simple()

    def _populate_changes_list(self, tree: ttk.Treeview, name_filter: str = ""):
        for iid in tree.get_children():
            tree.delete(iid)
        files = self._scan_config_files_with_status()
        only_changed = getattr(self, "var_changes_only", tk.BooleanVar(value=False)).get()
        for rel, status in files:
            if self._is_permanent(rel):
                status = f"{status} (Permanent)"
            if only_changed and status == "Unchanged":
                continue
            if name_filter and name_filter not in rel.lower():
                continue
            tree.insert("", tk.END, text=rel, values=(status,))

    def _scan_config_files_with_status(self) -> List[Tuple[str, str]]:
        # Snapshot-based status (independent of git)
        snapshot = self._load_config_snapshot()
        current = self._build_current_config_state()
        files: List[Tuple[str, str]] = []
        # Determine New/Modified/Unchanged and also include Deleted
        snap_paths = set(snapshot.keys())
        cur_paths = set(current.keys())
        for rel in sorted(cur_paths):
            if rel not in snap_paths:
                status = "New"
            else:
                status = "Modified" if current[rel]["hash"] != snapshot[rel].get("hash") else "Unchanged"
            files.append((rel, status))
        for rel in sorted(snap_paths - cur_paths):
            files.append((rel, "Deleted"))
        # Sort: Modified/New/Deleted first
        order = {"Modified": 0, "New": 1, "Deleted": 2, "Unchanged": 3}
        files.sort(key=lambda x: (order.get(x[1], 99), x[0].lower()))
        return files

    def _diff_file_vs_baseline(self, rel_path: str) -> str:
        # Unified diff vs snapshot baseline; fallback to current content
        snapshot = self._load_config_snapshot()
        full = os.path.join(self.repo_root, rel_path)
        current_lines = []
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                current_lines = f.read().splitlines()
        except Exception:
            pass
        base_entry = snapshot.get(rel_path)
        base_lines = (base_entry.get("content", "").splitlines() if base_entry else [])
        if not base_entry:
            return "(No baseline; file considered New)\n" + "\n".join(current_lines)
        if not current_lines:
            return "(File missing locally; baseline exists)\n" + base_entry.get("content", "")
        diff = difflib.unified_diff(base_lines, current_lines, fromfile=f"baseline:{rel_path}", tofile=rel_path, lineterm="")
        out = "\n".join(diff)
        return out or "(No differences vs baseline)"

    def _diff_file_vs_mode(self, rel_path: str, mode: str) -> str:
        if mode == "Snapshot":
            return self._diff_file_vs_baseline(rel_path)
        elif mode == "Git HEAD":
            return self._diff_file_vs_git_head(rel_path)
        elif mode == "In-File Defaults":
            return self._diff_file_vs_defaults(rel_path)
        elif mode == "Mod Cache":
            return self._diff_file_vs_mod_cache(rel_path)
        return self._diff_file_vs_baseline(rel_path)

    def _get_base_and_current(self, rel_path: str, mode: str) -> Tuple[List[str], List[str]]:
        if mode == "Snapshot":
            snapshot = self._load_config_snapshot()
            base_entry = snapshot.get(rel_path)
            base_lines = (base_entry.get("content", "").splitlines() if base_entry else [])
            try:
                with open(os.path.join(self.repo_root, rel_path), "r", encoding="utf-8", errors="ignore") as f:
                    cur_lines = f.read().splitlines()
            except Exception:
                cur_lines = []
            return base_lines, cur_lines
        if mode == "Git HEAD":
            try:
                head_blob = subprocess.check_output(["git", "-C", self.repo_root, "show", f"HEAD:{rel_path.replace('\\', '/')}"], stderr=subprocess.STDOUT)
                base_lines = head_blob.decode("utf-8", errors="ignore").splitlines()
            except Exception:
                base_lines = []
            try:
                with open(os.path.join(self.repo_root, rel_path), "r", encoding="utf-8", errors="ignore") as f:
                    cur_lines = f.read().splitlines()
            except Exception:
                cur_lines = []
            return base_lines, cur_lines
        if mode == "In-File Defaults":
            try:
                with open(os.path.join(self.repo_root, rel_path), "r", encoding="utf-8", errors="ignore") as f:
                    cur_lines = f.read().splitlines()
            except Exception:
                cur_lines = []
            base_lines = self._synthesize_defaults_from_comments(cur_lines)
            return base_lines, cur_lines
        if mode == "Mod Cache":
            basename = os.path.basename(rel_path)
            cache_root = os.path.abspath(os.path.join(self.repo_root, "Valheim", "cache"))
            candidates: List[str] = []
            for root, _, fnames in os.walk(cache_root):
                for fn in fnames:
                    if fn == basename:
                        candidates.append(os.path.join(root, fn))
            candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
            base_lines = []
            if candidates:
                try:
                    with open(candidates[0], "r", encoding="utf-8", errors="ignore") as f:
                        base_lines = f.read().splitlines()
                except Exception:
                    base_lines = []
            try:
                with open(os.path.join(self.repo_root, rel_path), "r", encoding="utf-8", errors="ignore") as f:
                    cur_lines = f.read().splitlines()
            except Exception:
                cur_lines = []
            return base_lines, cur_lines
        return [], []

    def _summarize_changes(self, rel_path: str, mode: str) -> str:
        base_lines, cur_lines = self._get_base_and_current(rel_path, mode)
        if not base_lines and not cur_lines:
            return "(No data available)"
        # Parse key = value pairs (ignore comments/sections)
        def parse(lines: List[str]) -> Dict[str, str]:
            data: Dict[str, str] = {}
            re_set = re.compile(r"^\s*([A-Za-z0-9_\-. ]+?)\s*=\s*(.*)\s*$")
            for ln in lines:
                if ln.strip().startswith("#") or ln.strip().startswith("["):
                    continue
                m = re_set.match(ln)
                if not m:
                    continue
                key = m.group(1).strip()
                val = m.group(2).strip()
                if key:
                    data[key] = val
            return data
        a = parse(base_lines)
        b = parse(cur_lines)
        added = sorted([k for k in b.keys() if k not in a])
        removed = sorted([k for k in a.keys() if k not in b])
        changed = sorted([k for k in b.keys() if k in a and a[k] != b[k]])
        parts: List[str] = []
        if changed:
            parts.append("Changed:")
            for k in changed:
                parts.append(f"- {k}: {a.get(k, '')} → {b.get(k, '')}")
        if added:
            parts.append("\nAdded:")
            for k in added:
                parts.append(f"- {k}: {b.get(k, '')}")
        if removed:
            parts.append("\nRemoved:")
            for k in removed:
                parts.append(f"- {k}: {a.get(k, '')}")
        if not parts:
            return "(No changes)"
        return "\n".join(parts)

    def _diff_file_vs_git_head(self, rel_path: str) -> str:
        full = os.path.join(self.repo_root, rel_path)
        try:
            head_blob = subprocess.check_output(["git", "-C", self.repo_root, "show", f"HEAD:{rel_path.replace('\\', '/')}"], stderr=subprocess.STDOUT)
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                work_txt = f.read().splitlines()
            head_txt = head_blob.decode("utf-8", errors="ignore").splitlines()
            diff = difflib.unified_diff(head_txt, work_txt, fromfile=f"HEAD:{rel_path}", tofile=rel_path, lineterm="")
            return "\n".join(diff) or "(No differences vs HEAD)"
        except Exception as exc:
            return f"(Git HEAD unavailable)\n{str(exc)}"

    def _diff_file_vs_defaults(self, rel_path: str) -> str:
        full = os.path.join(self.repo_root, rel_path)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read().splitlines()
        except Exception as exc:
            return str(exc)
        default_lines = self._synthesize_defaults_from_comments(lines)
        diff = difflib.unified_diff(default_lines, lines, fromfile=f"defaults:{rel_path}", tofile=rel_path, lineterm="")
        out = "\n".join(diff)
        return out or "(No differences vs in-file defaults)"

    def _synthesize_defaults_from_comments(self, lines: List[str]) -> List[str]:
        out: List[str] = []
        last_default_value: Optional[str] = None
        # Pattern for default value lines and setting lines
        re_def = re.compile(r"^\s*#\s*Default value:\s*(.*)\s*$", re.IGNORECASE)
        re_set = re.compile(r"^\s*([A-Za-z0-9_\-.]+)\s*=\s*(.*)$")
        for ln in lines:
            mdef = re_def.match(ln)
            if mdef:
                last_default_value = mdef.group(1)
                out.append(ln)
                continue
            mset = re_set.match(ln)
            if mset and last_default_value is not None and not ln.strip().startswith("#"):
                key = mset.group(1)
                # Replace with default value for baseline
                out.append(f"{key} = {last_default_value}")
                last_default_value = None
            else:
                out.append(ln)
                # Reset default capture if other lines intervene long
                if not ln.strip().startswith("#"):
                    last_default_value = None
        return out

    def _diff_file_vs_mod_cache(self, rel_path: str) -> str:
        # Try to find a file with same basename under Valheim/cache/*/*/ (config or manifest dirs)
        basename = os.path.basename(rel_path)
        cache_root = os.path.abspath(os.path.join(self.repo_root, "Valheim", "cache"))
        candidates: List[str] = []
        for root, _, fnames in os.walk(cache_root):
            for fn in fnames:
                if fn == basename:
                    candidates.append(os.path.join(root, fn))
        if not candidates:
            return "(No mod cache candidate found)"
        # Pick most recently modified
        candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        cache_path = candidates[0]
        try:
            with open(cache_path, "r", encoding="utf-8", errors="ignore") as f:
                base_lines = f.read().splitlines()
        except Exception as exc:
            return str(exc)
        full = os.path.join(self.repo_root, rel_path)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                cur_lines = f.read().splitlines()
        except Exception as exc:
            cur_lines = []
        diff = difflib.unified_diff(base_lines, cur_lines, fromfile=f"cache:{os.path.relpath(cache_path, self.repo_root)}", tofile=rel_path, lineterm="")
        out = "\n".join(diff)
        return out or "(No differences vs mod cache)"

    # ---------------------------
    # Permanent baseline management
    # ---------------------------
    def _load_permanent_snapshot(self) -> Dict[str, Dict[str, str]]:
        try:
            with open(self.permanent_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return {}

    def _save_permanent_snapshot(self, snap: Dict[str, Dict[str, str]]):
        try:
            with open(self.permanent_path, "w", encoding="utf-8") as f:
                json.dump(snap, f, indent=2)
        except Exception:
            pass

    def _is_permanent(self, rel_path: str) -> bool:
        snap = self._load_permanent_snapshot()
        return rel_path in snap

    def _mark_permanent(self, tree: ttk.Treeview):
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Mark Permanent", "Please click a file first.")
            return
        rel = tree.item(sel[0], "text")
        full = os.path.join(self.repo_root, rel)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as exc:
            messagebox.showerror("Mark Permanent", str(exc))
            return
        snap = self._load_permanent_snapshot()
        snap[rel] = {
            "hash": hashlib.md5(content.encode("utf-8", errors="ignore")).hexdigest(),
            "content": content,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self._save_permanent_snapshot(snap)
        messagebox.showinfo("Mark Permanent", f"Saved permanent snapshot for\n{rel}")

    def _unmark_permanent(self, tree: ttk.Treeview):
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Remove Permanent", "Please click a file first.")
            return
        rel = tree.item(sel[0], "text")
        snap = self._load_permanent_snapshot()
        if rel in snap:
            del snap[rel]
            self._save_permanent_snapshot(snap)
            messagebox.showinfo("Remove Permanent", f"Removed permanent snapshot for\n{rel}")
        else:
            messagebox.showinfo("Remove Permanent", "This file is not marked permanent.")

    def _restore_selected_from_permanent(self, tree: ttk.Treeview):
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Restore", "Please click a file first.")
            return
        rel = tree.item(sel[0], "text")
        snap = self._load_permanent_snapshot()
        if rel not in snap:
            messagebox.showinfo("Restore", "This file is not marked permanent.")
            return
        if not messagebox.askyesno("Restore", f"Replace the current file with your permanent copy?\n\n{rel}"):
            return
        full = os.path.join(self.repo_root, rel)
        try:
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(snap[rel].get("content", ""))
            messagebox.showinfo("Restore", "File restored.")
        except Exception as exc:
            messagebox.showerror("Restore", str(exc))

    def _fresh_sync_permanent_all(self):
        snap = self._load_permanent_snapshot()
        if not snap:
            messagebox.showinfo("Fresh Sync", "No permanent files saved yet.")
            return
        if not messagebox.askyesno(
            "Fresh Sync",
            "This will overwrite current config files with your saved permanent versions. Continue?",
        ):
            return
        errors: List[str] = []
        for rel, meta in snap.items():
            full = os.path.join(self.repo_root, rel)
            try:
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w", encoding="utf-8") as f:
                    f.write(meta.get("content", ""))
            except Exception as exc:
                errors.append(f"{rel}: {exc}")
        if errors:
            messagebox.showerror("Fresh Sync", "Some files failed to restore:\n\n" + "\n".join(errors[:20]))
        else:
            messagebox.showinfo("Fresh Sync", "All permanent files restored.")

    def _build_current_config_state(self) -> Dict[str, Dict[str, str]]:
        state: Dict[str, Dict[str, str]] = {}
        for root, _, fnames in os.walk(self.config_dir):
            for fn in fnames:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, self.repo_root)
                try:
                    with open(full, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except Exception:
                    content = ""
                h = hashlib.md5(content.encode("utf-8", errors="ignore")).hexdigest()
                state[rel] = {"hash": h, "content": content}
        # Also include changelog if present
        if os.path.isfile(self.changelog_path):
            try:
                with open(self.changelog_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                content = ""
            h = hashlib.md5(content.encode("utf-8", errors="ignore")).hexdigest()
            state[self.changelog_rel] = {"hash": h, "content": content}
        return state

    def _load_config_snapshot(self) -> Dict[str, Dict[str, str]]:
        try:
            with open(self.snapshot_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return {}

    def _save_config_snapshot(self, snapshot: Dict[str, Dict[str, str]]):
        try:
            with open(self.snapshot_path, "w", encoding="utf-8") as f:
                json.dump(snapshot, f)
        except Exception:
            pass

    def _append_history(self, snapshot: Dict[str, Dict[str, str]]):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "files": {k: {"hash": v.get("hash")} for k, v in snapshot.items()},
        }
        try:
            history: List[Dict] = []
            if os.path.isfile(self.history_path):
                with open(self.history_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        history = data
            history.append(entry)
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception:
            pass

    def _update_config_baseline(self, tree: ttk.Treeview, name_filter: str = ""):
        current = self._build_current_config_state()
        self._save_config_snapshot(current)
        self._append_history(current)
        self._populate_changes_list(tree, name_filter=name_filter)

    # ---------------------------
    # Changelog Viewer
    # ---------------------------
    def _open_changelog_viewer(self):
        win = tk.Toplevel(self)
        win.title("Changelog Viewer")
        win.configure(bg=self.palette["bg"])

        ctrl = ttk.Frame(win)
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)
        ttk.Label(ctrl, text="Find").pack(side=tk.LEFT)
        var_q = tk.StringVar()
        ent = ttk.Entry(ctrl, textvariable=var_q)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))
        btn_next = ttk.Button(ctrl, text="Find Next")
        btn_next.pack(side=tk.LEFT)
        ttk.Button(ctrl, text="Diff vs Baseline", command=lambda: self._fill_changelog_diff(txt_diff)).pack(side=tk.LEFT, padx=(8, 0))

        body = ttk.Frame(win)
        body.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Top: Full changelog
        ttk.Label(body, text="Full Changelog", foreground=self.palette["accent"]).pack(anchor=tk.W)
        txt = tk.Text(body, height=22, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"], font=self.font_text)
        txt.pack(fill=tk.BOTH, expand=True)

        # Bottom: Diff
        ttk.Label(body, text="Diff vs Baseline", foreground=self.palette["accent"]).pack(anchor=tk.W, pady=(6, 0))
        txt_diff = tk.Text(body, height=12, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"], font=self.font_text)
        txt_diff.pack(fill=tk.BOTH, expand=False)

        def load_log():
            try:
                with open(self.changelog_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as exc:
                content = str(exc)
            txt.delete("1.0", tk.END)
            txt.insert("1.0", content)
            self._fill_changelog_diff(txt_diff)

        def do_find_next():
            q = var_q.get()
            if not q:
                return
            idx = txt.search(q, txt.index(tk.INSERT), nocase=True, stopindex=tk.END)
            if not idx:
                # wrap around
                idx = txt.search(q, "1.0", nocase=True, stopindex=tk.END)
                if not idx:
                    return
            end = f"{idx}+{len(q)}c"
            txt.tag_remove("sel", "1.0", tk.END)
            txt.tag_add("sel", idx, end)
            txt.mark_set(tk.INSERT, end)
            txt.see(idx)

        btn_next.configure(command=do_find_next)
        load_log()

    def _fill_changelog_diff(self, txt_widget: tk.Text):
        diff_text = self._diff_file_vs_baseline(self.changelog_rel)
        txt_widget.configure(state="normal")
        txt_widget.delete("1.0", tk.END)
        txt_widget.insert("1.0", diff_text)
        txt_widget.configure(state="disabled")

    def _find_changelog_entries_for_file(self, rel_path: str) -> str:
        # Heuristic: map config file base name to keywords, search in changelog
        changelog = os.path.abspath(os.path.join(self.script_dir, "..", ".continue", "VALHEIM_CHANGE_LOG.md"))
        try:
            with open(changelog, "r", encoding="utf-8") as f:
                log_txt = f.read()
        except Exception:
            return ""
        base = os.path.basename(rel_path)
        stem = os.path.splitext(base)[0]
        # Extract probable mod keyword
        key_parts = stem.split(".")
        hints = set([stem, key_parts[-1]] + key_parts)
        # Common friendly names
        alias = {
            "advize": "PlantEverything",
            "PlantEverything": "PlantEverything",
            "shudnal": "Seasons",
            "Seasons": "Seasons",
            "WackyMole": "EpicMMO",
            "EpicMMO": "EpicMMO",
            "warpalicious": "Warpalicious",
        }
        for p in list(hints):
            if p in alias:
                hints.add(alias[p])
        # Find matching lines/sections
        lines = log_txt.splitlines()
        out: List[str] = []
        capture = False
        current_section = []
        for ln in lines:
            if ln.startswith("## ") or ln.startswith("### "):
                # new section; flush previous
                if current_section:
                    if any(h.lower() in "\n".join(current_section).lower() for h in hints if h):
                        out.extend(current_section)
                    current_section = []
                current_section = [ln]
            else:
                if current_section is not None:
                    current_section.append(ln)
        if current_section:
            if any(h.lower() in "\n".join(current_section).lower() for h in hints if h):
                out.extend(current_section)
        return "\n".join(out)


def main():
    # Allow optional command-line arg to override VNEI dir
    vnei_dir = None
    if len(sys.argv) > 1:
        vnei_dir = sys.argv[1]
    app = ItemHubApp(vnei_dir=vnei_dir)
    # Sensible default size
    app.minsize(1000, 600)
    app.mainloop()


if __name__ == "__main__":
    main()


