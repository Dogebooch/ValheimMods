import os
import sys
import json
import shutil
import re
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from difflib import unified_diff

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkfont


class Tooltip:
    """Simple tooltip for Tk widgets."""
    def __init__(self, widget, text: str, delay_ms: int = 450):
        self.widget = widget
        self.text = text
        self.delay_ms = delay_ms
        self._tip_window = None
        self._after_id = None
        try:
            widget.bind("<Enter>", self._schedule)
            widget.bind("<Leave>", self._unschedule)
            widget.bind("<ButtonPress>", self._unschedule)
        except Exception:
            pass

    def _schedule(self, _event=None):
        self._unschedule()
        try:
            self._after_id = self.widget.after(self.delay_ms, self._show)
        except Exception:
            pass

    def _unschedule(self, _event=None):
        try:
            if self._after_id:
                self.widget.after_cancel(self._after_id)
                self._after_id = None
            self._hide()
        except Exception:
            pass

    def _show(self):
        if self._tip_window or not self.text:
            return
        try:
            x, y, cx, cy = self.widget.bbox("insert") if hasattr(self.widget, "bbox") else (0, 0, 0, 0)
        except Exception:
            x = y = 0
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self._tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#333", foreground="#fff",
                         relief=tk.SOLID, borderwidth=1,
                         font=("Consolas" if sys.platform.startswith("win") else "Courier New", 9))
        label.pack(ipadx=6, ipady=4)

    def _hide(self):
        try:
            if self._tip_window is not None:
                self._tip_window.destroy()
                self._tip_window = None
        except Exception:
            pass

class ConfigSnapshot:
    def __init__(self, config_root: Path):
        self.config_root = config_root
        # Store snapshots in the scripts directory
        scripts_dir = Path(__file__).parent
        self.snapshots_dir = scripts_dir / "snapshots"
        self.current_snapshot_file = self.snapshots_dir / "current_snapshot.json"
        self.initial_snapshot_file = self.snapshots_dir / "initial_snapshot.json"
        self.event_log_file = self.snapshots_dir / "event_log.jsonl"
        self.snapshots_dir.mkdir(exist_ok=True)
        
    def get_file_hash(self, file_path: Path) -> str:
        """Get SHA256 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""
    
    def get_file_info(self, file_path: Path) -> dict:
        """Get file metadata and content hash."""
        try:
            stat = file_path.stat()
            
            # Skip very large files to prevent memory issues
            if stat.st_size > 10 * 1024 * 1024:  # 10MB limit
                return {
                    'size': stat.st_size,
                    'mtime': stat.st_mtime,
                    'hash': '',
                    'content': f'[File too large: {stat.st_size} bytes]'
                }
            
            return {
                'size': stat.st_size,
                'mtime': stat.st_mtime,
                'hash': self.get_file_hash(file_path),
                'content': file_path.read_text(encoding='utf-8', errors='replace')
            }
        except Exception:
            return {'size': 0, 'mtime': 0, 'hash': '', 'content': ''}
    
    def create_snapshot(self, is_initial: bool = False) -> tuple[bool, str]:
        """Create a snapshot of current config state."""
        try:
            snapshot = {
                'timestamp': datetime.now().isoformat(),
                'session': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                'files': {}
            }
            
            # Get all files first
            files = [f for f in self.config_root.rglob('*') 
                    if f.is_file()]
            
            for i, file_path in enumerate(files):
                rel_path = str(file_path.relative_to(self.config_root))
                snapshot['files'][rel_path] = self.get_file_info(file_path)
                
                # Progress update every 10 files
                if i % 10 == 0:
                    print(f"Processing file {i+1}/{len(files)}: {rel_path}")
            
            # Save snapshot
            target_file = self.initial_snapshot_file if is_initial else self.current_snapshot_file
            with open(target_file, 'w', encoding='utf-8', newline='\n') as f:
                json.dump(snapshot, f, indent=2, ensure_ascii=False)
            
            snapshot_type = "initial" if is_initial else "current"
            msg = f"{snapshot_type.capitalize()} snapshot created with {len(snapshot['files'])} files"
            self.log_event(action="snapshot", success=True, extra={"type": snapshot_type, "file_count": len(snapshot['files'])})
            return True, msg
        except Exception as e:
            self.log_event(action="snapshot", success=False, extra={"error": str(e)})
            return False, f"Failed to create snapshot: {e}"
    
    def load_snapshot(self, snapshot_type: str = "current") -> dict:
        """Load a snapshot by type."""
        try:
            if snapshot_type == "initial":
                file_path = self.initial_snapshot_file
            else:
                file_path = self.current_snapshot_file
                
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {'timestamp': '', 'session': '', 'files': {}}

    def revert_file(self, rel_path: str, from_snapshot: str = "current") -> tuple[bool, str]:
        """Revert a single file to the content stored in the chosen snapshot.

        - If the file did not exist in the snapshot, delete it.
        - If the file existed, write the snapshot content to disk.
        """
        try:
            snapshot = self.load_snapshot(from_snapshot)
            target = self.config_root / rel_path

            if rel_path not in snapshot['files']:
                # File was not tracked in that snapshot → delete if exists
                if target.exists():
                    target.unlink()
                self.log_event(action="revert", file=rel_path, success=True, extra={"from": from_snapshot, "method": "delete"})
                return True, f"Deleted {rel_path} (not present in {from_snapshot} snapshot)"

            # Ensure directory exists
            target.parent.mkdir(parents=True, exist_ok=True)
            content = snapshot['files'][rel_path].get('content', '')
            target.write_text(content, encoding='utf-8', newline='\n')
            self.log_event(action="revert", file=rel_path, success=True, extra={"from": from_snapshot, "method": "write"})
            return True, f"Reverted {rel_path} to {from_snapshot} snapshot"
        except Exception as e:
            self.log_event(action="revert", file=rel_path, success=False, extra={"from": from_snapshot, "error": str(e)})
            return False, f"Failed to revert {rel_path}: {e}"

    def accept_into_baseline(self, rel_path: str) -> tuple[bool, str]:
        """Accept the current on-disk version of a file into the initial baseline.

        - If the file exists: update/insert its entry in the initial snapshot
        - If it does not exist: remove it from the initial snapshot
        """
        try:
            initial = self.load_snapshot("initial")
            target = self.config_root / rel_path
            if target.exists():
                initial['files'][rel_path] = self.get_file_info(target)
                action = "Updated baseline for"
            else:
                if rel_path in initial['files']:
                    del initial['files'][rel_path]
                action = "Removed from baseline"

            # Save updated initial snapshot
            with open(self.initial_snapshot_file, 'w', encoding='utf-8', newline='\n') as f:
                json.dump(initial, f, indent=2, ensure_ascii=False)
            self.log_event(action="accept_baseline", file=rel_path, success=True, extra={"action": action})
            return True, f"{action} {rel_path}"
        except Exception as e:
            self.log_event(action="accept_baseline", file=rel_path, success=False, extra={"error": str(e)})
            return False, f"Failed to accept into baseline: {e}"

    def log_event(self, action: str, file: str | None = None, success: bool = True, extra: dict | None = None) -> None:
        """Append a single event to the JSONL event log."""
        try:
            rec = {
                "timestamp": datetime.now().isoformat(timespec='seconds'),
                "action": action,
                "file": file or "",
                "success": success,
            }
            if extra:
                rec.update({"details": extra})
            self.event_log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.event_log_file, 'a', encoding='utf-8', newline='\n') as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception:
            # Best-effort logging; ignore failures
            pass
    
    def get_changes(self, compare_against: str = "current") -> list[tuple[str, str, str, str]]:
        """Get list of (status, file_path, mod_name, session) for changed files."""
        snapshot = self.load_snapshot(compare_against)
        changes = []
        
        for file_path in self.config_root.rglob('*'):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(self.config_root))
                current_info = self.get_file_info(file_path)
                
                if rel_path in snapshot['files']:
                    old_info = snapshot['files'][rel_path]
                    if current_info['hash'] != old_info['hash']:
                        changes.append(('M', rel_path, self._get_mod_name(rel_path), snapshot.get('session', 'Unknown')))
                else:
                    changes.append(('A', rel_path, self._get_mod_name(rel_path), snapshot.get('session', 'Unknown')))
        
        # Check for deleted files
        for rel_path in snapshot['files']:
            if not (self.config_root / rel_path).exists():
                changes.append(('D', rel_path, self._get_mod_name(rel_path), snapshot.get('session', 'Unknown')))
        
        return changes
    
    def _get_mod_name(self, file_path: str) -> str:
        """Extract mod name from file path."""
        # Extract mod name from common patterns
        if '.' in file_path:
            parts = file_path.split('.')
            if len(parts) >= 2:
                return parts[0]  # First part is usually mod name
        return Path(file_path).stem
    
    def get_diff(self, file_path: str, compare_against: str = "current") -> str:
        """Get diff between current and snapshot version."""
        snapshot = self.load_snapshot(compare_against)
        current_file = self.config_root / file_path
        
        if file_path not in snapshot['files']:
            # New file
            if current_file.exists():
                content = current_file.read_text(encoding='utf-8', errors='replace')
                return f"New file: {file_path}\n" + '\n'.join(f"+ {line}" for line in content.splitlines())
            return "File not found"
        
        old_content = snapshot['files'][file_path]['content']
        
        if not current_file.exists():
            # Deleted file
            return f"Deleted file: {file_path}\n" + '\n'.join(f"- {line}" for line in old_content.splitlines())
        
        current_content = current_file.read_text(encoding='utf-8', errors='replace')
        
        # Generate unified diff
        diff_lines = list(unified_diff(
            old_content.splitlines(keepends=True),
            current_content.splitlines(keepends=True),
            fromfile=f'a/{file_path}',
            tofile=f'b/{file_path}',
            lineterm=''
        ))
        
        return ''.join(diff_lines)

    # --- Change summarization helpers ---
    def _flatten_json(self, obj, prefix="") -> dict:
        flat = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_p = f"{prefix}.{k}" if prefix else str(k)
                flat.update(self._flatten_json(v, new_p))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_p = f"{prefix}[{i}]"
                flat.update(self._flatten_json(v, new_p))
        else:
            flat[prefix] = "" if obj is None else str(obj)
        return flat

    def _parse_cfg_like(self, text: str) -> dict:
        data = {}
        current_section = None
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith(('#', ';', '//')):
                continue
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].strip()
                continue
            m = re.match(r"^([^#;=:\n]+?)\s*[:=]\s*(.*)$", line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip()
                full_key = f"{current_section}.{key}" if current_section else key
                data[full_key] = val
        return data

    def _parse_yaml_like(self, text: str) -> dict:
        # Heuristic: support up to 3 levels of indentation with 2 spaces
        data = {}
        stack = []  # list of (indent_level, key_prefix)
        for raw in text.splitlines():
            if not raw.strip() or raw.lstrip().startswith(('#', '//')):
                continue
            indent = len(raw) - len(raw.lstrip(' '))
            line = raw.strip()
            # key: value or key:
            m = re.match(r"^([A-Za-z0-9_.-]+):\s*(.*)$", line)
            if not m:
                continue
            key, val = m.group(1), m.group(2)
            # adjust stack by indent
            while stack and stack[-1][0] >= indent:
                stack.pop()
            prefix = stack[-1][1] if stack else ""
            full_key = f"{prefix}.{key}" if prefix else key
            if val == "" or val == "|" or val == ">":
                # parent key
                stack.append((indent, full_key))
            else:
                data[full_key] = val
        return data

    def summarize_change(self, file_path: str, compare_against: str = "current", max_items: int = 3) -> str:
        snap = self.load_snapshot(compare_against)
        old_entry = snap['files'].get(file_path)
        current_file = self.config_root / file_path
        exists_now = current_file.exists()
        if not old_entry and not exists_now:
            return ""
        if not old_entry and exists_now:
            return "New file"
        if old_entry and not exists_now:
            return "Deleted file"

        old_text = old_entry.get('content', '') if old_entry else ''
        new_text = current_file.read_text(encoding='utf-8', errors='replace') if exists_now else ''
        ext = Path(file_path).suffix.lower()

        summaries = []
        try:
            if ext in ('.cfg', '.ini', '.conf'):
                old_kv = self._parse_cfg_like(old_text)
                new_kv = self._parse_cfg_like(new_text)
            elif ext in ('.yml', '.yaml'):
                old_kv = self._parse_yaml_like(old_text)
                new_kv = self._parse_yaml_like(new_text)
            elif ext == '.json':
                try:
                    old_kv = self._flatten_json(json.loads(old_text or '{}'))
                    new_kv = self._flatten_json(json.loads(new_text or '{}'))
                except Exception:
                    old_kv = {}
                    new_kv = {}
            else:
                old_kv = {}
                new_kv = {}

            # Prefer structured diffs
            changed_keys = []
            for k in sorted(set(old_kv.keys()) | set(new_kv.keys())):
                o = old_kv.get(k)
                n = new_kv.get(k)
                if o is None and n is not None:
                    changed_keys.append((k, None, n, 'added'))
                elif o is not None and n is None:
                    changed_keys.append((k, o, None, 'removed'))
                elif o is not None and n is not None and o != n:
                    changed_keys.append((k, o, n, 'modified'))

            for k, o, n, kind in changed_keys[:max_items]:
                if kind == 'modified':
                    summaries.append(f"{k} changed from {o} to {n}")
                elif kind == 'added':
                    summaries.append(f"{k} set to {n}")
                elif kind == 'removed':
                    summaries.append(f"{k} removed (was {o})")

            extra = len(changed_keys) - len(summaries)
            if extra > 0:
                summaries.append(f"(+{extra} more)")
        except Exception:
            summaries = []

        if not summaries:
            # Fallback to line-diff heuristic
            diff = self.get_diff(file_path, compare_against)
            adds = sum(1 for ln in diff.splitlines() if ln.startswith('+') and not ln.startswith('+++'))
            dels = sum(1 for ln in diff.splitlines() if ln.startswith('-') and not ln.startswith('---'))
            if adds or dels:
                return f"{adds} additions, {dels} deletions"
            return "Modified"

        return '; '.join(summaries)


class ConfigChangeTrackerApp:
    def __init__(self, root: tk.Tk, config_root: Path):
        self.root = root
        self.config_root = config_root
        self.snapshot = ConfigSnapshot(config_root)
        
        # UI State
        self.base_font_size = 10
        self.font = tkfont.Font(family="Consolas" if sys.platform.startswith("win") else "Courier New", size=self.base_font_size)
        self.zoom_level = 1.0
        
        # Colors (earthy tones)
        self.colors = {
            "bg": "#2e2b23",  # deep brown
            "panel": "#3b352a",  # dark umber
            "text": "#e8e2d0",  # parchment
            "accent": "#a3a17a",  # sage
            "highlight": "#7d6f5e",  # clay
            "added": "#6aa84f",  # green
            "removed": "#cc0000",  # red
            "modified": "#e69138",  # amber
            "border": "#5d4e37",  # darker brown
        }
        
        self._build_ui()
        self._init_snapshot_and_refresh()
    
    def _build_ui(self) -> None:
        self.root.title("Config Change Tracker")
        self.root.geometry("1600x900")
        self.root.configure(bg=self.colors["bg"])
        
        # Configure styles
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        
        self.style.configure("TFrame", background=self.colors["bg"])
        self.style.configure("Action.TButton", 
                       background=self.colors["highlight"], 
                       foreground=self.colors["text"], 
                       padding=6)
        self.style.map("Action.TButton", 
                 background=[("active", self.colors["accent"])])
        self.style.configure("Treeview", 
                       background=self.colors["panel"], 
                       fieldbackground=self.colors["panel"], 
                       foreground=self.colors["text"])
        self.style.configure("Treeview.Heading", 
                       background=self.colors["highlight"], 
                       foreground=self.colors["text"])
        # Default fonts for ttk widgets
        try:
            self.style.configure("Treeview", font=self.font)
            self.style.configure("Treeview.Heading", font=self.font)
            self.style.configure("Action.TButton", font=self.font)
            self.style.configure("TLabel", font=self.font)
            self.style.configure("TCombobox", font=self.font)
        except Exception:
            pass
        
        # Menu bar
        menubar = tk.Menu(self.root, tearoff=False)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Save Session Snapshot", command=self.create_snapshot)
        file_menu.add_command(label="Set New Baseline (All Files)", command=self.create_initial_snapshot)
        file_menu.add_command(label="Scan for Changes", command=self.refresh_changes)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=False)
        view_menu.add_command(label="Zoom In (Ctrl +)", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out (Ctrl -)", command=self.zoom_out)
        view_menu.add_command(label="Reset Zoom (Ctrl 0)", command=self.reset_zoom)
        view_menu.add_separator()
        view_menu.add_command(label="All Changes Since Baseline...", command=self.show_baseline_summary)
        menubar.add_cascade(label="View", menu=view_menu)

        # Tools menu (optional/advanced)
        tools_menu = tk.Menu(menubar, tearoff=False)
        tools_menu.add_command(label="Open Event Log (Detailed)", command=self.open_event_log)
        tools_menu.add_separator()
        tools_menu.add_command(label="Help: What do these buttons do?", command=self.show_help)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        self.root.config(menu=menubar)
        
        # Keyboard shortcuts
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.reset_zoom())
        
        # Main container with paned windows for resizing
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # Left panel: Controls and mod filter
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Top controls
        controls_frame = ttk.Frame(left_frame)
        controls_frame.pack(fill=tk.X, padx=6, pady=6)
        
        self.btn_refresh = ttk.Button(controls_frame, text="Scan for Changes", 
                                     style="Action.TButton", command=self.refresh_changes)
        self.btn_refresh.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_snapshot = ttk.Button(controls_frame, text="Save Session Snapshot", 
                                       style="Action.TButton", command=self.create_snapshot)
        self.btn_snapshot.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_revert = ttk.Button(controls_frame, text="Revert Selected to Reference", 
                                     style="Action.TButton", command=self.revert_selected)
        self.btn_revert.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_accept = ttk.Button(controls_frame, text="Promote Selected to Baseline", 
                                     style="Action.TButton", command=self.accept_selected_into_baseline)
        self.btn_accept.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_baseline_summary = ttk.Button(controls_frame, text="All-Time Change Summary", 
                                               style="Action.TButton", command=self.show_baseline_summary)
        self.btn_baseline_summary.pack(side=tk.LEFT, padx=(0, 6))
        
        # Zoom controls
        zoom_frame = ttk.Frame(controls_frame)
        zoom_frame.pack(side=tk.RIGHT)
        
        self.btn_zoom_out = ttk.Button(zoom_frame, text="A-", width=3, 
                                      style="Action.TButton", command=self.zoom_out)
        self.btn_zoom_out.pack(side=tk.RIGHT, padx=(0, 3))
        
        self.btn_zoom_in = ttk.Button(zoom_frame, text="A+", width=3, 
                                     style="Action.TButton", command=self.zoom_in)
        self.btn_zoom_in.pack(side=tk.RIGHT)
        
        # Comparison and filter controls
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, padx=6, pady=(0, 6))
        
        # Comparison selector
        compare_label = tk.Label(filter_frame, text="View changes relative to:", 
                                bg=self.colors["bg"], fg=self.colors["text"])
        compare_label.pack(anchor="w")
        
        self.compare_var = tk.StringVar(value="Since Last Snapshot (This Session)")
        self.compare_combo = ttk.Combobox(filter_frame, textvariable=self.compare_var, 
                                         state="readonly", width=30)
        self.compare_combo['values'] = [
            "Since Last Snapshot (This Session)",
            "Since Baseline (All-Time)"
        ]
        self.compare_combo.pack(fill=tk.X, pady=(3, 6))
        self.compare_combo.bind("<<ComboboxSelected>>", self.on_compare_change)

        # Inline explanation of selected comparison
        self.compare_help_var = tk.StringVar(value="Shows differences from the most recent Session Snapshot.")
        compare_help = tk.Label(filter_frame, textvariable=self.compare_help_var,
                                bg=self.colors["bg"], fg=self.colors["accent"])
        compare_help.pack(anchor="w", pady=(0, 6))
        
        # Snapshot info
        self.snapshot_info_var = tk.StringVar(value="")
        snapshot_info_label = tk.Label(filter_frame, textvariable=self.snapshot_info_var,
                                       bg=self.colors["bg"], fg=self.colors["text"])
        snapshot_info_label.pack(anchor="w", pady=(0, 6))

        # Mod filter
        filter_label = tk.Label(filter_frame, text="Filter by Mod:", 
                               bg=self.colors["bg"], fg=self.colors["text"])
        filter_label.pack(anchor="w")
        
        self.mod_filter_var = tk.StringVar(value="All Mods")
        self.mod_filter_combo = ttk.Combobox(filter_frame, textvariable=self.mod_filter_var, 
                                            state="readonly", width=30)
        self.mod_filter_combo.pack(fill=tk.X, pady=(3, 0))
        self.mod_filter_combo.bind("<<ComboboxSelected>>", self.on_mod_filter_change)
        
        # Changes list
        changes_frame = ttk.Frame(left_frame)
        changes_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        self.changes_header_var = tk.StringVar(value="Changes vs Last Snapshot (Most Recent First):")
        changes_label = tk.Label(changes_frame, textvariable=self.changes_header_var, 
                                bg=self.colors["bg"], fg=self.colors["text"])
        changes_label.pack(anchor="w")
        
        # Create Treeview for changes
        self.changes_tree = ttk.Treeview(changes_frame, columns=("status", "file", "mod", "time", "summary", "session"), 
                                        show="headings", height=20)
        self.changes_tree.heading("status", text="Status")
        self.changes_tree.heading("file", text="File")
        self.changes_tree.heading("mod", text="Mod")
        self.changes_tree.heading("time", text="Modified")
        self.changes_tree.heading("summary", text="Summary")
        self.changes_tree.heading("session", text="Session")
        
        self.changes_tree.column("status", width=60)
        self.changes_tree.column("file", width=230)
        self.changes_tree.column("mod", width=100)
        self.changes_tree.column("time", width=100)
        self.changes_tree.column("summary", width=350)
        self.changes_tree.column("session", width=120)
        
        self.changes_tree.pack(fill=tk.BOTH, expand=True, pady=(3, 0))
        self.changes_tree.bind("<<TreeviewSelect>>", self.on_change_select)
        
        # Scrollbar for changes
        changes_scroll = ttk.Scrollbar(changes_frame, orient=tk.VERTICAL, 
                                      command=self.changes_tree.yview)
        self.changes_tree.configure(yscrollcommand=changes_scroll.set)
        changes_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel: Diff viewer
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        diff_label = tk.Label(right_frame, text="Diff View:", 
                             bg=self.colors["bg"], fg=self.colors["text"])
        diff_label.pack(anchor="w", padx=6, pady=(6, 0))
        
        # Diff text widget
        self.diff_text = tk.Text(right_frame, bg=self.colors["panel"], 
                                fg=self.colors["text"], 
                                insertbackground=self.colors["text"], 
                                wrap=tk.NONE, font=self.font)
        self.diff_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # Diff scrollbars
        diff_yscroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, 
                                    command=self.diff_text.yview)
        diff_xscroll = ttk.Scrollbar(right_frame, orient=tk.HORIZONTAL, 
                                    command=self.diff_text.xview)
        self.diff_text.configure(yscrollcommand=diff_yscroll.set, 
                                xscrollcommand=diff_xscroll.set)
        diff_yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        diff_xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure diff text tags
        self.diff_text.tag_configure("added", foreground=self.colors["added"])
        self.diff_text.tag_configure("removed", foreground=self.colors["removed"])
        self.diff_text.tag_configure("header", foreground=self.colors["accent"])
        self.diff_text.tag_configure("modified", foreground=self.colors["modified"])
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             anchor="w", bg=self.colors["bg"], fg=self.colors["text"])
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=6, pady=2)

        # Attach tooltips
        try:
            Tooltip(self.btn_refresh, "Scan the config folder and list files that differ from the selected reference.")
            Tooltip(self.btn_snapshot, "Save a Session Snapshot now. 'Since Last Snapshot' compares against this save point.")
            Tooltip(self.btn_revert, "Revert the selected file so it matches the chosen reference (Baseline or Last Snapshot).")
            Tooltip(self.btn_accept, "Update the all-time Baseline with the current on-disk version of the selected file.")
            Tooltip(self.btn_baseline_summary, "Show every change since the all-time Baseline, grouped by mod.")
            Tooltip(self.compare_combo, "Choose whether to compare against the last Session Snapshot or the all-time Baseline.")
        except Exception:
            pass
    
    def zoom_in(self) -> None:
        """Increase zoom level."""
        self.zoom_level = min(self.zoom_level * 1.2, 3.0)
        self._apply_zoom()
    
    def zoom_out(self) -> None:
        """Decrease zoom level."""
        self.zoom_level = max(self.zoom_level / 1.2, 0.5)
        self._apply_zoom()
    
    def reset_zoom(self) -> None:
        """Reset zoom to default."""
        self.zoom_level = 1.0
        self._apply_zoom()
    
    def _apply_zoom(self) -> None:
        """Apply current zoom level to fonts."""
        new_size = int(self.base_font_size * self.zoom_level)
        self.font.configure(size=new_size)
        # Apply font to key widgets and ttk styles
        try:
            self.diff_text.configure(font=self.font)
        except Exception:
            pass
        try:
            self.style.configure("Treeview", font=self.font)
            self.style.configure("Treeview.Heading", font=self.font)
            self.style.configure("Action.TButton", font=self.font)
            self.style.configure("TLabel", font=self.font)
            self.style.configure("TCombobox", font=self.font)
        except Exception:
            pass
        # Update tk.Label widgets as well
        try:
            self._apply_font_to_widgets(self.root)
        except Exception:
            pass

    def _apply_font_to_widgets(self, widget):
        for child in widget.winfo_children():
            try:
                if isinstance(child, (tk.Label, tk.Text)):
                    child.configure(font=self.font)
            except Exception:
                pass
            self._apply_font_to_widgets(child)
    
    def _init_snapshot_and_refresh(self) -> None:
        """Initialize snapshot and refresh changes."""
        def worker():
            try:
                # Create initial snapshot if none exists
                if not self.snapshot.initial_snapshot_file.exists():
                    self.root.after(0, lambda: self._set_status("Creating initial snapshot..."))
                    ok, msg = self.snapshot.create_snapshot(is_initial=True)
                    if ok:
                        self.root.after(0, lambda: self._set_status(msg))
                    else:
                        self.root.after(0, lambda: self._set_status(f"Error: {msg}"))
                
                # Create current snapshot if none exists
                if not self.snapshot.current_snapshot_file.exists():
                    self.root.after(0, lambda: self._set_status("Creating current snapshot..."))
                    ok, msg = self.snapshot.create_snapshot()
                    if ok:
                        self.root.after(0, lambda: self._set_status(msg))
                    else:
                        self.root.after(0, lambda: self._set_status(f"Error: {msg}"))
                
                # Update snapshot info label
                def update_info():
                    ini = self.snapshot.load_snapshot("initial").get('timestamp', 'N/A')
                    cur = self.snapshot.load_snapshot("current").get('timestamp', 'N/A')
                    self.snapshot_info_var.set(f"Baseline set: {ini}    |    Last session snapshot: {cur}")
                self.root.after(0, update_info)

                self.root.after(0, self.refresh_changes)
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error: {e}"))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def create_snapshot(self) -> None:
        """Create a new current snapshot."""
        def worker():
            try:
                # Update status in main thread
                self.root.after(0, lambda: self._set_status("Creating current snapshot..."))
                ok, msg = self.snapshot.create_snapshot()
                
                # Update UI in main thread
                if ok:
                    def after_ok():
                        self._set_status("Session Snapshot saved. 'Since Last Snapshot' now compares to this point.")
                        # Update banner
                        ini = self.snapshot.load_snapshot("initial").get('timestamp', 'N/A')
                        cur = self.snapshot.load_snapshot("current").get('timestamp', 'N/A')
                        self.snapshot_info_var.set(f"Baseline set: {ini}    |    Last session snapshot: {cur}")
                    self.root.after(0, after_ok)
                    self.root.after(0, self.refresh_changes)
                else:
                    self.root.after(0, lambda: self._set_status(f"Error: {msg}"))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error: {e}"))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def create_initial_snapshot(self) -> None:
        """Create a new initial snapshot."""
        def worker():
            try:
                # Update status in main thread
                def confirm_and_start():
                    if not messagebox.askyesno(
                        "Set New Baseline",
                        "This will replace your all-time Baseline with the current on-disk state for ALL tracked files.\n\nAfter this, 'Since Baseline' will compare against this new point.\n\nProceed?"
                    ):
                        self._set_status("Baseline update canceled")
                        return False
                    self._set_status("Creating new Baseline from current files...")
                    return True
                proceed = self.root.after(0, confirm_and_start)
                # Note: confirmation runs in main thread; if canceled, we just return later when UI updates
                # Continue with snapshot regardless; the confirm handler updates status and we proceed
                ok, msg = self.snapshot.create_snapshot(is_initial=True)
                
                # Update UI in main thread
                if ok:
                    def after_ok():
                        self._set_status("Baseline updated. 'Since Baseline' now compares to this point.")
                        ini = self.snapshot.load_snapshot("initial").get('timestamp', 'N/A')
                        cur = self.snapshot.load_snapshot("current").get('timestamp', 'N/A')
                        self.snapshot_info_var.set(f"Baseline set: {ini}    |    Last session snapshot: {cur}")
                    self.root.after(0, after_ok)
                    def update_info():
                        ini = self.snapshot.load_snapshot("initial").get('timestamp', 'N/A')
                        cur = self.snapshot.load_snapshot("current").get('timestamp', 'N/A')
                        self.snapshot_info_var.set(f"Baseline set: {ini}    |    Last session snapshot: {cur}")
                    self.root.after(0, update_info)
                    self.root.after(0, self.refresh_changes)
                else:
                    self.root.after(0, lambda: self._set_status(f"Error: {msg}"))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error: {e}"))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def refresh_changes(self) -> None:
        """Refresh the changes list."""
        def worker():
            try:
                self.root.after(0, lambda: self._set_status("Scanning for changes..."))
                
                # Determine comparison type
                compare_against = "initial" if self.compare_var.get() == "Since Baseline (All-Time)" else "current"
                changes = self.snapshot.get_changes(compare_against)
                
                # Update mod filter options
                mods = {"All Mods"} | {mod for _, _, mod, _ in changes}
                
                # Filter changes based on current selection
                selected_mod = self.mod_filter_var.get()
                if selected_mod != "All Mods":
                    changes = [(status, file_path, mod, session) for status, file_path, mod, session in changes if mod == selected_mod]
                
                # Sort by modification time (most recent first)
                changes_with_time = []
                added = modified = deleted = 0
                for status, file_path, mod, session in changes:
                    try:
                        file_obj = self.config_root / file_path
                        if file_obj.exists():
                            mtime = file_obj.stat().st_mtime
                            time_str = datetime.fromtimestamp(mtime).strftime("%m/%d %H:%M")
                        else:
                            mtime = -1
                            time_str = "Deleted"
                    except Exception:
                        mtime = -1
                        time_str = "Unknown"
                    
                    # Generate brief summary
                    try:
                        compare_against = "initial" if self.compare_var.get() == "Since Baseline (All-Time)" else "current"
                        summary = self.snapshot.summarize_change(file_path, compare_against)
                    except Exception:
                        summary = ""

                    if status == 'A':
                        added += 1
                    elif status == 'M':
                        modified += 1
                    elif status == 'D':
                        deleted += 1
                    
                    changes_with_time.append((status, file_path, mod, time_str, summary, session, mtime))
                
                # Update header summary with target
                target_label = "Baseline" if compare_against == "initial" else "Last Snapshot"
                summary = f"Changes vs {target_label}  (A:{added}  M:{modified}  D:{deleted})"
                self.root.after(0, lambda s=summary: self.changes_header_var.set(s))
                
                changes_with_time.sort(key=lambda x: x[6], reverse=True)
                
                # Update UI in main thread
                self.root.after(0, lambda: self._update_changes_list(changes_with_time, mods))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error: {e}"))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def _update_changes_list(self, changes: list, mods: set) -> None:
        """Update the changes list in the UI."""
        # Clear existing items
        for item in self.changes_tree.get_children():
            self.changes_tree.delete(item)
        
        # Update mod filter options
        self.mod_filter_combo['values'] = sorted(mods)
        
        # Add new items
        for status, file_path, mod, time_str, summary, session, _mtime in changes:
            status_display = {
                'A': 'Added',
                'M': 'Modified',
                'D': 'Deleted'
            }.get(status, status)
            
            self.changes_tree.insert("", "end", values=(status_display, file_path, mod, time_str, summary, session))
        
        self._set_status(f"Found {len(changes)} changed file(s)")
    
    def on_mod_filter_change(self, event=None) -> None:
        """Handle mod filter change."""
        self.refresh_changes()
    
    def on_compare_change(self, event=None) -> None:
        """Handle comparison type change."""
        # Update inline explanation
        try:
            if self.compare_var.get() == "Since Baseline (All-Time)":
                self.compare_help_var.set("Shows differences from the all-time Baseline.")
            else:
                self.compare_help_var.set("Shows differences from the most recent Session Snapshot.")
        except Exception:
            pass
        # Update immediately
        self._set_status(f"View switched to '{self.compare_var.get()}'")
        self.refresh_changes()
    
    def on_change_select(self, event=None) -> None:
        """Handle change selection."""
        selection = self.changes_tree.selection()
        if not selection:
            # Disable action buttons when nothing is selected
            try:
                self.btn_revert.state(["disabled"])
                self.btn_accept.state(["disabled"])
            except Exception:
                pass
            return
        
        item = self.changes_tree.item(selection[0])
        file_path = item['values'][1]
        
        # Enable action buttons when selection exists
        try:
            self.btn_revert.state(["!disabled"])
            self.btn_accept.state(["!disabled"])
        except Exception:
            pass

        # Show diff in background thread
        def worker():
            try:
                # Determine comparison type
                compare_against = "initial" if self.compare_var.get() == "Since Baseline (All-Time)" else "current"
                diff = self.snapshot.get_diff(file_path, compare_against)
                self.root.after(0, lambda: self._show_diff(diff, file_path, compare_against))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error loading diff: {e}"))
        
        threading.Thread(target=worker, daemon=True).start()

    def revert_selected(self) -> None:
        """Revert the selected file to the currently selected comparison baseline."""
        selection = self.changes_tree.selection()
        if not selection:
            self._set_status("No file selected to revert")
            return
        file_path = self.changes_tree.item(selection[0])['values'][1]

        def worker():
            try:
                compare_against = "initial" if self.compare_var.get() == "Since Baseline (All-Time)" else "current"
                ok, msg = self.snapshot.revert_file(file_path, from_snapshot=compare_against)
                if ok:
                    def post_ok():
                        self._set_status(msg)
                        # Remove reverted item from the list immediately for responsiveness
                        for iid in self.changes_tree.get_children(""):
                            vals = self.changes_tree.item(iid).get('values', [])
                            if len(vals) >= 2 and vals[1] == file_path:
                                self.changes_tree.delete(iid)
                                break
                        # Also refresh in background to recompute summaries & counts
                        self.refresh_changes()
                    self.root.after(0, post_ok)
                else:
                    self.root.after(0, lambda: self._set_status(f"Error: {msg}"))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error: {e}"))

        threading.Thread(target=worker, daemon=True).start()

    def accept_selected_into_baseline(self) -> None:
        """Accept the selected file into the baseline (initial snapshot)."""
        selection = self.changes_tree.selection()
        if not selection:
            self._set_status("No file selected to accept into baseline")
            return
        file_path = self.changes_tree.item(selection[0])['values'][1]

        def worker():
            try:
                ok, msg = self.snapshot.accept_into_baseline(file_path)
                if ok:
                    self.root.after(0, lambda: self._set_status(msg))
                    self.root.after(0, self.refresh_changes)
                else:
                    self.root.after(0, lambda: self._set_status(f"Error: {msg}"))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error: {e}"))

        threading.Thread(target=worker, daemon=True).start()
    
    def _show_diff(self, diff: str, file_path: str, compare_against: str = "current") -> None:
        """Display diff in the text widget."""
        self.diff_text.config(state=tk.NORMAL)
        self.diff_text.delete("1.0", tk.END)
        try:
            header = f"Diff vs {'Baseline' if compare_against == 'initial' else 'Last Snapshot'} — {file_path}\n\n"
            self.diff_text.insert(tk.END, header, "header")
        except Exception:
            pass
        
        for line in diff.splitlines(True):
            tag = None
            if line.startswith("+++") or line.startswith("---") or line.startswith("diff ") or line.startswith("index "):
                tag = "header"
            elif line.startswith("+"):
                tag = "added"
            elif line.startswith("-"):
                tag = "removed"
            elif line.startswith("@@"):
                tag = "modified"
            
            if tag:
                self.diff_text.insert(tk.END, line, tag)
            else:
                self.diff_text.insert(tk.END, line)
        
        self.diff_text.config(state=tk.DISABLED)
        self._set_status(f"Viewing diff: {file_path}")

    def show_help(self) -> None:
        """Show a concise help dialog explaining the main controls."""
        try:
            help_text = (
                "Compare selector — choose what you're comparing against:\n"
                " • Since Last Snapshot (This Session): compares to your most recent Session Snapshot.\n"
                " • Since Baseline (All-Time): compares to the all-time Baseline.\n\n"
                "Save Session Snapshot — saves the current on-disk state as the 'Last Snapshot' for this session.\n"
                "Set New Baseline (All Files) — replaces the all-time Baseline with the current on-disk state.\n\n"
                "Revert Selected to Reference — make the selected file match the chosen reference (Baseline or Last Snapshot).\n"
                "Promote Selected to Baseline — update the all-time Baseline to the current version of the selected file.\n\n"
                "All-Time Change Summary — lists every change since the Baseline, grouped by mod."
            )
            messagebox.showinfo("Help", help_text)
        except Exception as e:
            self._set_status(f"Error showing help: {e}")

    def show_baseline_summary(self) -> None:
        """Show a modal with all changes relative to the initial baseline."""
        def worker():
            try:
                changes = self.snapshot.get_changes("initial")
                # Build a grouped summary by mod
                grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
                for status, file_path, mod, session in changes:
                    summary = self.snapshot.summarize_change(file_path, compare_against="initial", max_items=3)
                    grouped[mod].append((status, file_path, summary))

                def open_modal():
                    win = tk.Toplevel(self.root)
                    win.title("All Changes Since Baseline")
                    win.geometry("1100x700")
                    win.configure(bg=self.colors["bg"])

                    top = ttk.Frame(win)
                    top.pack(fill=tk.X, padx=8, pady=6)
                    lbl = tk.Label(top, text="All Changes Since Baseline (Initial State)",
                                   bg=self.colors["bg"], fg=self.colors["text"])
                    lbl.pack(side=tk.LEFT)

                    container = ttk.Frame(win)
                    container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

                    cols = ("status", "file", "summary")
                    tree = ttk.Treeview(container, columns=cols, show="headings")
                    for c, w in [("status", 80), ("file", 420), ("summary", 520)]:
                        tree.heading(c, text=c.capitalize())
                        tree.column(c, width=w)
                    tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

                    yscroll = ttk.Scrollbar(container, orient=tk.VERTICAL, command=tree.yview)
                    tree.configure(yscrollcommand=yscroll.set)
                    yscroll.pack(fill=tk.Y, side=tk.RIGHT)

                    # Insert grouped mods as category rows
                    for mod in sorted(grouped.keys()):
                        parent = tree.insert("", "end", values=("", f"[{mod}]", ""))
                        for status, file_path, summary in grouped[mod]:
                            status_display = { 'A': 'Added', 'M': 'Modified', 'D': 'Deleted' }.get(status, status)
                            tree.insert(parent, "end", values=(status_display, file_path, summary))

                    # Expand all
                    for iid in tree.get_children(""):
                        tree.item(iid, open=True)

                self.root.after(0, open_modal)
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error: {e}"))

        threading.Thread(target=worker, daemon=True).start()

    def open_event_log(self) -> None:
        """Open an interactive viewer for the JSONL event log with right-click delete."""
        try:
            if not self.snapshot.event_log_file.exists():
                messagebox.showinfo("Event Log", "No events have been logged yet.")
                return

            win = tk.Toplevel(self.root)
            win.title("Detailed Event Log")
            win.geometry("1100x750")
            win.configure(bg=self.colors["bg"])

            container = ttk.Frame(win)
            container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

            cols = ("time", "action", "file", "success", "details")
            tree = ttk.Treeview(container, columns=cols, show="headings")
            for c, w in [("time", 160), ("action", 120), ("file", 380), ("success", 80), ("details", 300)]:
                tree.heading(c, text=c.capitalize())
                tree.column(c, width=w)
            tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

            yscroll = ttk.Scrollbar(container, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=yscroll.set)
            yscroll.pack(fill=tk.Y, side=tk.RIGHT)

            iid_to_line_idx: dict[str, int] = {}

            def refresh_tree():
                tree.delete(*tree.get_children())
                iid_to_line_idx.clear()
                try:
                    with open(self.snapshot.event_log_file, 'r', encoding='utf-8') as f:
                        for idx, line in enumerate(f):
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                obj = json.loads(line)
                            except Exception:
                                obj = {"timestamp": "", "action": "?", "file": "", "success": "", "details": line[:200]}
                            ts = obj.get("timestamp", "")
                            action = obj.get("action", "")
                            filev = obj.get("file", "")
                            success = obj.get("success", "")
                            details = obj.get("details", "")
                            if isinstance(details, dict):
                                details = json.dumps(details, ensure_ascii=False)
                            iid = tree.insert("", "end", values=(ts, action, filev, success, details))
                            iid_to_line_idx[iid] = idx
                except Exception as e:
                    messagebox.showerror("Event Log", f"Failed to read log: {e}")

            def delete_selected_event():
                sel = tree.selection()
                if not sel:
                    return
                if not messagebox.askyesno("Delete Event", "Delete selected event(s) from the log? This cannot be undone."):
                    return
                try:
                    to_delete = sorted({iid_to_line_idx[i] for i in sel}, reverse=True)
                    with open(self.snapshot.event_log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    for li in to_delete:
                        if 0 <= li < len(lines):
                            del lines[li]
                    with open(self.snapshot.event_log_file, 'w', encoding='utf-8', newline='\n') as f:
                        f.writelines(lines)
                    refresh_tree()
                except Exception as e:
                    messagebox.showerror("Delete Event", f"Failed to delete: {e}")

            # Context menu
            menu = tk.Menu(win, tearoff=False)
            menu.add_command(label="Delete", command=delete_selected_event)

            def on_right_click(event):
                try:
                    rowid = tree.identify_row(event.y)
                    if rowid:
                        tree.selection_set(rowid)
                        menu.tk_popup(event.x_root, event.y_root)
                finally:
                    menu.grab_release()

            tree.bind("<Button-3>", on_right_click)
            win.bind("<Delete>", lambda e: delete_selected_event())

            refresh_tree()
        except Exception as e:
            self._set_status(f"Error opening event log: {e}")
    
    def _set_status(self, text: str) -> None:
        """Update status bar."""
        ts = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{ts}] {text}")


def locate_config_root() -> Path:
    """Locate the config directory."""
    if len(sys.argv) >= 2:
        arg = Path(sys.argv[1]).expanduser().resolve()
        return arg
    
    # Default to the known path
    workspace = Path(__file__).resolve().parents[1]
    candidate = workspace / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config"
    return candidate


def main() -> int:
    config_root = locate_config_root()
    if not config_root.exists():
        messagebox.showerror("Config Path Not Found", 
                           f"Config directory does not exist:\n{config_root}")
        return 2
    
    root = tk.Tk()
    app = ConfigChangeTrackerApp(root, config_root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
