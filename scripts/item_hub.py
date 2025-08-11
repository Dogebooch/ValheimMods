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

        # Data
        self.items: List[Dict[str, str]] = []
        self.filtered_items: List[Dict[str, str]] = []
        self.item_types: List[str] = []
        self.changes: Dict[str, Dict] = {}  # internal name -> metadata

        # Images
        self.photo_cache: Dict[str, ImageTk.PhotoImage] = {}
        self.missing_icon: Optional[ImageTk.PhotoImage] = None

        # UI Vars
        self.var_filter_type = tk.StringVar(value="All")
        self.var_search = tk.StringVar()
        self.var_status = tk.StringVar(value="")

        # Build UI
        self._build_layout()

        # Load data
        self._load_items()
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
        )
        style.configure(
            "TButton",
            background=self.palette["button"],
            foreground=self.palette["text_primary"],
            focuscolor=self.palette["accent"],
        )
        style.map("TButton", background=[("active", self.palette["accent2"])])
        style.configure(
            "TCombobox",
            fieldbackground=self.palette["entry_bg"],
            background=self.palette["entry_bg"],
            foreground=self.palette["entry_fg"],
        )
        style.configure(
            "Treeview",
            background=self.palette["list_bg"],
            fieldbackground=self.palette["list_bg"],
            foreground=self.palette["text_primary"],
            bordercolor=self.palette["border"],
        )
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
        ent_search = ttk.Entry(top, textvariable=self.var_search)
        ent_search.pack(side=tk.LEFT, padx=(6, 12), fill=tk.X, expand=True)
        ent_search.bind("<KeyRelease>", lambda e: self._apply_filters())

        btn_clear = ttk.Button(top, text="Clear Filters", command=self._clear_filters)
        btn_clear.pack(side=tk.LEFT)

        # Main split: list (left) and details (right)
        main = ttk.Frame(self)
        main.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Left: Treeview
        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Use the tree column (#0) to show item name + icon.
        # Additional columns hold metadata. First column 'done' acts as a checkbox.
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

        ttk.Label(right, text="Item Details", font=("Segoe UI", 11, "bold"), foreground=self.palette["accent"]).pack(anchor=tk.W)

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
        self.txt_tags = tk.Text(right, height=2, width=40, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"])
        self.txt_tags.pack(fill=tk.X)

        ttk.Label(right, text="Notes").pack(anchor=tk.W)
        self.txt_notes = tk.Text(right, height=12, width=40, bg=self.palette["entry_bg"], fg=self.palette["entry_fg"], insertbackground=self.palette["entry_fg"])
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
        if not os.path.isfile(self.csv_path):
            messagebox.showerror("Missing CSV", f"Could not find VNEI CSV at:\n{self.csv_path}")
            self.destroy()
            return

        items: List[Dict[str, str]] = []
        with open(self.csv_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalize keys we rely on
                item = {
                    "Internal Name": row.get("Internal Name", "").strip(),
                    "Localized Name": row.get("Localized Name", "").strip(),
                    "Item Type": row.get("Item Type", "").strip() or "Undefined",
                    "Description": row.get("Description", "").strip(),
                    "Source Mod": row.get("Source Mod", "").strip() or "Valheim",
                }
                if item["Internal Name"]:
                    items.append(item)

        self.items = items

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
                return q in hay
            return True

        self.filtered_items = [it for it in self.items if match(it)]
        self._populate_tree()

    def _clear_filters(self):
        self.var_filter_type.set("All")
        self.var_search.set("")
        self._apply_filters()

    def _populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        count = 0
        for idx, it in enumerate(self.filtered_items):
            internal = it.get("Internal Name", "")
            localized = it.get("Localized Name", internal)
            icon = self._get_icon_for_item(internal)
            checked = False
            meta = self.changes.get(internal)
            if isinstance(meta, dict):
                checked = bool(meta.get("checked", False))
            done_symbol = "☑" if checked else "☐"
            iid = self.tree.insert(
                "",
                tk.END,
                text=localized,
                image=icon,
                values=(done_symbol, it.get("Item Type", ""), it.get("Source Mod", ""), internal),
            )
            count += 1
        self._set_status(f"Showing {count} of {len(self.items)} items")

    # ---------------------------
    # Icons
    # ---------------------------
    def _ensure_missing_icon(self) -> Optional[ImageTk.PhotoImage]:
        if self.missing_icon is not None:
            return self.missing_icon
        if Image is None or ImageTk is None:
            return None
        img = Image.new("RGBA", (24, 24), self.palette["accent2"])  # soft earthy square
        self.missing_icon = ImageTk.PhotoImage(img)
        return self.missing_icon

    def _get_icon_for_item(self, internal_name: str) -> Optional[ImageTk.PhotoImage]:
        if Image is None or ImageTk is None:
            return None

        key = internal_name.lower()
        if key in self.photo_cache:
            return self.photo_cache[key]

        # Attempt to find icon file in icons dir by several strategies
        icon_path = None
        if os.path.isdir(self.icons_dir):
            # 1) Exact match (case-insensitive) with common extensions
            for ext in (".png", ".jpg", ".jpeg"):
                candidate = os.path.join(self.icons_dir, internal_name + ext)
                if os.path.isfile(candidate):
                    icon_path = candidate
                    break

            # 2) Fallback: scan for file starting with internal name
            if icon_path is None:
                lowered = internal_name.lower()
                try:
                    for fname in os.listdir(self.icons_dir):
                        if fname.lower().startswith(lowered) and fname.lower().endswith((".png", ".jpg", ".jpeg")):
                            icon_path = os.path.join(self.icons_dir, fname)
                            break
                except Exception:
                    pass

        try:
            if icon_path and os.path.isfile(icon_path):
                img = Image.open(icon_path).convert("RGBA")
                img.thumbnail((24, 24), Image.LANCZOS)
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
        vals = self.tree.item(iid, "values") or ("", "", "", "")
        # values order: done, type, mod, internal
        item_type = vals[1] if len(vals) > 1 else ""
        source_mod = vals[2] if len(vals) > 2 else ""
        internal = vals[3] if len(vals) > 3 else ""

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


