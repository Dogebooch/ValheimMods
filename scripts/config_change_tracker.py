import os
import sys
import json
import shutil
import re
import hashlib
import threading
import subprocess
import platform
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
        # Ignore very large or noisy directories to keep scans responsive
        # Case-insensitive match on path parts
        self._ignored_dir_names = {"wackydatabase-bulkyml"}
        # In-memory caches to reduce disk I/O while app is open
        self._snapshot_cache: dict[str, dict] = {}
        # Minimal index cache: { type -> { 'session': str, 'index': { rel_path: {size, mtime, hash} } } }
        self._snapshot_index_cache: dict[str, dict] = {}

    def _should_ignore(self, file_path: Path) -> bool:
        try:
            rel_parts = (file_path.relative_to(self.config_root)).parts
        except Exception:
            rel_parts = file_path.parts
        for part in rel_parts:
            if part.lower() in self._ignored_dir_names:
                return True
        return False
        
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
            
            # Get all files first, excluding ignored directories
            files = [
                f for f in self.config_root.rglob('*')
                if f.is_file() and not self._should_ignore(f)
            ]
            
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
            # Update caches (minimal index and full snapshot)
            try:
                self._snapshot_cache[snapshot_type] = snapshot
                idx: dict[str, dict] = {rel: {'size': m.get('size', 0), 'mtime': m.get('mtime', 0), 'hash': m.get('hash', '')} for rel, m in snapshot['files'].items()}
                self._snapshot_index_cache[snapshot_type] = {'session': snapshot.get('session', ''), 'index': idx}
            except Exception:
                pass
            return True, msg
        except Exception as e:
            self.log_event(action="snapshot", success=False, extra={"error": str(e)})
            return False, f"Failed to create snapshot: {e}"
    
    def load_snapshot(self, snapshot_type: str = "current") -> dict:
        """Load a snapshot by type. Served from in-memory cache when available."""
        try:
            if snapshot_type in self._snapshot_cache:
                return self._snapshot_cache[snapshot_type]
            file_path = self.initial_snapshot_file if snapshot_type == "initial" else self.current_snapshot_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    snap = json.load(f)
                    self._snapshot_cache[snapshot_type] = snap
                    return snap
        except Exception:
            pass
        return {'timestamp': '', 'session': '', 'files': {}}

    def load_snapshot_index(self, snapshot_type: str = "current") -> dict:
        """Load a minimal snapshot index (session + file meta only), cached in memory."""
        try:
            if snapshot_type in self._snapshot_index_cache:
                return self._snapshot_index_cache[snapshot_type]
            snap = self.load_snapshot(snapshot_type)
            files = snap.get('files', {}) or {}
            idx: dict[str, dict] = {}
            for rel, meta in files.items():
                try:
                    idx[rel] = {
                        'size': meta.get('size', 0),
                        'mtime': meta.get('mtime', 0),
                        'hash': meta.get('hash', ''),
                    }
                except Exception:
                    continue
            result = {'session': snap.get('session', ''), 'index': idx}
            self._snapshot_index_cache[snapshot_type] = result
            return result
        except Exception:
            return {'session': '', 'index': {}}

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
        
        # Fast, IO-light scan: compare stat size/mtime first; avoid hashing entire file contents
        for file_path in self.config_root.rglob('*'):
            if not file_path.is_file():
                continue
            if self._should_ignore(file_path):
                continue
            rel_path = str(file_path.relative_to(self.config_root))
            try:
                stat = file_path.stat()
                cur_size = stat.st_size
                cur_mtime = stat.st_mtime
            except Exception:
                # If stat fails, fall back to marking as modified so UI can reflect something changed
                cur_size = -1
                cur_mtime = -1

            if rel_path in snapshot['files']:
                old_info = snapshot['files'][rel_path]
                old_size = old_info.get('size', -2)
                old_mtime = old_info.get('mtime', -2)
                # If either size or mtime changed, consider it modified (skip expensive hashing here)
                if cur_size != old_size or cur_mtime != old_mtime:
                    changes.append(('M', rel_path, self._get_mod_name(rel_path), snapshot.get('session', 'Unknown')))
            else:
                changes.append(('A', rel_path, self._get_mod_name(rel_path), snapshot.get('session', 'Unknown')))
        
        # Check for deleted files (skip ignored)
        for rel_path in snapshot['files']:
            try:
                abs_path = (self.config_root / rel_path)
                if self._should_ignore(abs_path):
                    continue
                if not abs_path.exists():
                    changes.append(('D', rel_path, self._get_mod_name(rel_path), snapshot.get('session', 'Unknown')))
            except Exception:
                # If any error occurs resolving a path, ignore deletion case
                pass
        
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
        
        # If the file is ignored, avoid heavy work and report as ignored
        try:
            if self._should_ignore(current_file):
                return f"[Ignored path: {file_path}]"
        except Exception:
            pass

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
        # Hidden entries persistence
        self.hidden_changes_file = self.snapshot.snapshots_dir / "hidden_changes.json"
        self.hidden_files: set[str] = set()
        self._load_hidden_changes()
        # Custom summary overrides persistence
        self.custom_summaries_file = self.snapshot.snapshots_dir / "custom_summaries.json"
        self.custom_summaries: dict[str, str] = {}
        self._load_custom_summaries()
        
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
        file_menu.add_command(label="Scan for Changes", command=self.refresh_changes)
        file_menu.add_separator()
        file_menu.add_command(label="Save Session Snapshot", command=self.create_snapshot)
        file_menu.add_command(label="Set New Baseline (All Files)", command=self.create_initial_snapshot)
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
        
        # Top controls (simplified)
        controls_frame = ttk.Frame(left_frame)
        controls_frame.pack(fill=tk.X, padx=6, pady=6)
        
        self.btn_refresh = ttk.Button(controls_frame, text="Scan for Changes", 
                                     style="Action.TButton", command=self.refresh_changes)
        self.btn_refresh.pack(side=tk.LEFT, padx=(0, 6))
        
        self.btn_relicheim = ttk.Button(controls_frame, text="Compare vs RelicHeim", 
                                       style="Action.TButton", command=self.show_relicheim_comparison)
        self.btn_relicheim.pack(side=tk.LEFT, padx=(0, 6))
        
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
        
        self.compare_var = tk.StringVar(value="Since Baseline (All-Time)")
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
        
        self.changes_header_var = tk.StringVar(value="Changes vs Baseline (Most Recent First):")
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
        # Context menu for quick actions
        self._changes_menu = tk.Menu(self.root, tearoff=False)
        self._changes_menu.add_command(label="Revert to Reference", command=self.revert_selected)
        self._changes_menu.add_command(label="Accept into Baseline", command=self.accept_selected_into_baseline)
        self._changes_menu.add_separator()
        self._changes_menu.add_command(label="Edit Summary…", command=lambda: self.edit_selected_summary(from_summary_tab=False))
        self._changes_menu.add_command(label="Clear Custom Summary", command=lambda: self.clear_selected_summary(from_summary_tab=False))
        self._changes_menu.add_separator()
        self._changes_menu.add_command(label="Hide (persist)", command=self.hide_selected_change)
        self._changes_menu.add_separator()
        self._changes_menu.add_command(label="Manage Hidden…", command=self.manage_hidden_changes)
        def on_changes_right_click(event):
            try:
                rowid = self.changes_tree.identify_row(event.y)
                if rowid:
                    self.changes_tree.selection_set(rowid)
                self._changes_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self._changes_menu.grab_release()
        self.changes_tree.bind("<Button-3>", on_changes_right_click)
        # Delete key hides selected
        self.root.bind("<Delete>", lambda e: self.hide_selected_change())
        # Double-click to open file in editor or edit summary
        self.changes_tree.bind("<Double-1>", self._on_changes_double_click)
        
        # Scrollbar for changes
        changes_scroll = ttk.Scrollbar(changes_frame, orient=tk.VERTICAL, 
                                      command=self.changes_tree.yview)
        self.changes_tree.configure(yscrollcommand=changes_scroll.set)
        changes_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel: Notebook with Diff and All-Time Summary
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        self.right_notebook = ttk.Notebook(right_frame)
        self.right_notebook.pack(fill=tk.BOTH, expand=True)

        # Diff tab
        self.diff_tab = ttk.Frame(self.right_notebook)
        self.right_notebook.add(self.diff_tab, text="Diff View")

        # Create a frame to hold the text widget and scrollbars
        diff_frame = ttk.Frame(self.diff_tab)
        diff_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.diff_text = tk.Text(diff_frame, bg=self.colors["panel"],
                                 fg=self.colors["text"],
                                 insertbackground=self.colors["text"],
                                 wrap=tk.NONE, font=self.font)
        self.diff_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        diff_yscroll = ttk.Scrollbar(diff_frame, orient=tk.VERTICAL, command=self.diff_text.yview)
        diff_yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontal scrollbar
        diff_xscroll = ttk.Scrollbar(self.diff_tab, orient=tk.HORIZONTAL, command=self.diff_text.xview)
        diff_xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure the text widget to use both scrollbars
        self.diff_text.configure(yscrollcommand=diff_yscroll.set, xscrollcommand=diff_xscroll.set)

        self.diff_text.tag_configure("added", foreground=self.colors["added"]) 
        self.diff_text.tag_configure("removed", foreground=self.colors["removed"]) 
        self.diff_text.tag_configure("header", foreground=self.colors["accent"]) 
        self.diff_text.tag_configure("modified", foreground=self.colors["modified"]) 

        # All-Time Summary tab
        self.summary_tab = ttk.Frame(self.right_notebook)
        self.right_notebook.add(self.summary_tab, text="All-Time Summary")

        cols = ("status", "file", "summary")
        self.summary_tree = ttk.Treeview(self.summary_tab, columns=cols, show="headings")
        for c, w in [("status", 90), ("file", 520), ("summary", 520)]:
            self.summary_tree.heading(c, text=c.capitalize())
            self.summary_tree.column(c, width=w)
        self.summary_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=6, pady=6)

        summary_yscroll = ttk.Scrollbar(self.summary_tab, orient=tk.VERTICAL, command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=summary_yscroll.set)
        summary_yscroll.pack(fill=tk.Y, side=tk.RIGHT)

        # Double-click: open diff or edit summary depending on column
        self.summary_tree.bind("<Double-1>", self._open_from_summary)
        # Right-click menu on summary list
        self._summary_menu = tk.Menu(self.root, tearoff=False)
        self._summary_menu.add_command(label="Edit Summary…", command=lambda: self.edit_selected_summary(from_summary_tab=True))
        self._summary_menu.add_command(label="Clear Custom Summary", command=lambda: self.clear_selected_summary(from_summary_tab=True))
        def on_summary_right_click(event):
            try:
                rowid = self.summary_tree.identify_row(event.y)
                if rowid:
                    self.summary_tree.selection_set(rowid)
                self._summary_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self._summary_menu.grab_release()
        self.summary_tree.bind("<Button-3>", on_summary_right_click)
        
        # Status bar with busy indicator
        self.status_var = tk.StringVar(value="Ready")
        status_container = tk.Frame(self.root, bg=self.colors["bg"]) 
        status_container.pack(side=tk.BOTTOM, fill=tk.X, padx=6, pady=2)
        status_bar = tk.Label(status_container, textvariable=self.status_var,
                              anchor="w", bg=self.colors["bg"], fg=self.colors["text"])
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.progress = ttk.Progressbar(status_container, mode="indeterminate", length=120)
        self.progress.pack(side=tk.RIGHT)
        try:
            self.progress.stop()
        except Exception:
            pass

        # Attach tooltips (simplified)
        try:
            Tooltip(self.btn_refresh, "Scan the config folder and list files that differ from the selected reference.")
            Tooltip(self.btn_relicheim, "Compare current configuration files against the base RelicHeim installation to see all changes.")
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
                    self.root.after(0, lambda: self._set_busy(True, "Creating initial snapshot..."))
                    ok, msg = self.snapshot.create_snapshot(is_initial=True)
                    if ok:
                        self.root.after(0, lambda: self._set_busy(False, msg))
                    else:
                        self.root.after(0, lambda: self._set_busy(False, f"Error: {msg}"))
                
                # Create current snapshot if none exists
                if not self.snapshot.current_snapshot_file.exists():
                    self.root.after(0, lambda: self._set_busy(True, "Creating current snapshot..."))
                    ok, msg = self.snapshot.create_snapshot()
                    if ok:
                        self.root.after(0, lambda: self._set_busy(False, msg))
                    else:
                        self.root.after(0, lambda: self._set_busy(False, f"Error: {msg}"))
                
                # Update snapshot info label
                def update_info():
                    ini = self.snapshot.load_snapshot("initial").get('timestamp', 'N/A')
                    cur = self.snapshot.load_snapshot("current").get('timestamp', 'N/A')
                    self.snapshot_info_var.set(f"Baseline set: {ini}    |    Last session snapshot: {cur}")
                self.root.after(0, update_info)

                # Auto-scan for changes and open All-Time Summary by default
                def do_initial_scan():
                    try:
                        self.compare_var.set("Since Baseline (All-Time)")
                        self.on_compare_change()
                        self.show_baseline_summary()
                    except Exception:
                        self.refresh_changes()
                self.root.after(0, do_initial_scan)
            except Exception as e:
                self.root.after(0, lambda: self._set_busy(False, f"Error: {e}"))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def create_snapshot(self) -> None:
        """Create a new current snapshot."""
        def worker():
            try:
                # Update status in main thread
                self.root.after(0, lambda: self._set_busy(True, "Creating current snapshot..."))
                ok, msg = self.snapshot.create_snapshot()
                
                # Update UI in main thread
                if ok:
                    def after_ok():
                        self._set_busy(False, "Session Snapshot saved. 'Since Last Snapshot' now compares to this point.")
                        # Update banner
                        ini = self.snapshot.load_snapshot("initial").get('timestamp', 'N/A')
                        cur = self.snapshot.load_snapshot("current").get('timestamp', 'N/A')
                        self.snapshot_info_var.set(f"Baseline set: {ini}    |    Last session snapshot: {cur}")
                    self.root.after(0, after_ok)
                    self.root.after(0, self.refresh_changes)
                else:
                    self.root.after(0, lambda: self._set_busy(False, f"Error: {msg}"))
            except Exception as e:
                self.root.after(0, lambda: self._set_busy(False, f"Error: {e}"))
        
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
                        self._set_busy(False, "Baseline update canceled")
                        return False
                    self._set_busy(True, "Creating new Baseline from current files...")
                    return True
                proceed = self.root.after(0, confirm_and_start)
                # Note: confirmation runs in main thread; if canceled, we just return later when UI updates
                # Continue with snapshot regardless; the confirm handler updates status and we proceed
                ok, msg = self.snapshot.create_snapshot(is_initial=True)
                
                # Update UI in main thread
                if ok:
                    def after_ok():
                        self._set_busy(False, "Baseline updated. 'Since Baseline' now compares to this point.")
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
                    self.root.after(0, lambda: self._set_busy(False, f"Error: {msg}"))
            except Exception as e:
                self.root.after(0, lambda: self._set_busy(False, f"Error: {e}"))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def refresh_changes(self) -> None:
        """Refresh the changes list."""
        def worker():
            try:
                self.root.after(0, lambda: self._set_busy(True, "Scanning for changes..."))
                
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
                    # Skip hidden
                    if file_path in self.hidden_files:
                        continue
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
                        # Apply custom override if present
                        if file_path in self.custom_summaries:
                            summary = self.custom_summaries[file_path]
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
                self.root.after(0, lambda: self._set_busy(False, f"Error: {e}"))
        
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
        try:
            self._set_busy(False)
        except Exception:
            pass
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

        # Ensure Diff tab is visible
        try:
            self.right_notebook.select(self.diff_tab)
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

    # --- Hidden changes persistence and actions ---
    def _load_hidden_changes(self) -> None:
        try:
            if self.hidden_changes_file.exists():
                data = json.loads(self.hidden_changes_file.read_text(encoding='utf-8'))
                if isinstance(data, list):
                    self.hidden_files = set(str(x) for x in data)
                elif isinstance(data, dict) and 'files' in data:
                    self.hidden_files = set(str(x) for x in data.get('files') or [])
        except Exception:
            self.hidden_files = set()

        # Ensure file exists
        try:
            self.hidden_changes_file.parent.mkdir(parents=True, exist_ok=True)
            if not self.hidden_changes_file.exists():
                self.hidden_changes_file.write_text("[]", encoding='utf-8', newline='\n')
        except Exception:
            pass

    def _save_hidden_changes(self) -> None:
        try:
            self.hidden_changes_file.parent.mkdir(parents=True, exist_ok=True)
            self.hidden_changes_file.write_text(
                json.dumps(sorted(self.hidden_files), indent=2, ensure_ascii=False),
                encoding='utf-8', newline='\n'
            )
        except Exception:
            pass

    def hide_selected_change(self) -> None:
        selection = self.changes_tree.selection()
        if not selection:
            return
        vals = self.changes_tree.item(selection[0]).get('values', [])
        if len(vals) < 2:
            return
        file_path = vals[1]
        if not file_path:
            return
        # Persist and remove from UI
        self.hidden_files.add(file_path)
        self._save_hidden_changes()
        try:
            self.changes_tree.delete(selection[0])
        except Exception:
            pass
        self._set_status(f"Hidden change: {file_path}")

    def manage_hidden_changes(self) -> None:
        try:
            win = tk.Toplevel(self.root)
            win.title("Hidden Changes")
            win.geometry("700x500")
            win.configure(bg=self.colors["bg"])

            top = ttk.Frame(win)
            top.pack(fill=tk.X, padx=8, pady=6)
            tk.Label(top, text="Hidden file entries (persisted):", bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w")

            container = ttk.Frame(win)
            container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

            listbox = tk.Listbox(container, selectmode=tk.EXTENDED, bg=self.colors["panel"], fg=self.colors["text"], activestyle='dotbox')
            listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
            yscroll = ttk.Scrollbar(container, orient=tk.VERTICAL, command=listbox.yview)
            listbox.configure(yscrollcommand=yscroll.set)
            yscroll.pack(fill=tk.Y, side=tk.RIGHT)

            for fp in sorted(self.hidden_files):
                listbox.insert(tk.END, fp)

            btns = ttk.Frame(win)
            btns.pack(fill=tk.X, padx=8, pady=6)
            def unhide_selected():
                sel = list(listbox.curselection())
                if not sel:
                    return
                items = [listbox.get(i) for i in sel]
                changed = False
                for it in items:
                    if it in self.hidden_files:
                        self.hidden_files.remove(it)
                        changed = True
                if changed:
                    self._save_hidden_changes()
                    # Remove from listbox
                    for i in reversed(sel):
                        listbox.delete(i)
                    self._set_status(f"Unhid {len(items)} entr{'y' if len(items)==1 else 'ies'}")
                    # Refresh main list asynchronously
                    self.refresh_changes()

            def unhide_all():
                if not self.hidden_files:
                    return
                if not messagebox.askyesno("Unhide All", "Remove all hidden entries?"):
                    return
                self.hidden_files.clear()
                self._save_hidden_changes()
                listbox.delete(0, tk.END)
                self._set_status("All hidden entries cleared")
                self.refresh_changes()

            ttk.Button(btns, text="Unhide Selected", style="Action.TButton", command=unhide_selected).pack(side=tk.LEFT, padx=(0,6))
            ttk.Button(btns, text="Unhide All", style="Action.TButton", command=unhide_all).pack(side=tk.LEFT)

            # Keyboard delete in manager
            win.bind("<Delete>", lambda e: unhide_selected())
        except Exception as e:
            self._set_status(f"Error managing hidden entries: {e}")

    # --- Custom summary overrides ---
    def _load_custom_summaries(self) -> None:
        try:
            if self.custom_summaries_file.exists():
                data = json.loads(self.custom_summaries_file.read_text(encoding='utf-8'))
                if isinstance(data, dict):
                    self.custom_summaries = {str(k): str(v) for k, v in data.items()}
        except Exception:
            self.custom_summaries = {}
        try:
            self.custom_summaries_file.parent.mkdir(parents=True, exist_ok=True)
            if not self.custom_summaries_file.exists():
                self.custom_summaries_file.write_text("{}", encoding='utf-8', newline='\n')
        except Exception:
            pass

    def _save_custom_summaries(self) -> None:
        try:
            self.custom_summaries_file.parent.mkdir(parents=True, exist_ok=True)
            self.custom_summaries_file.write_text(
                json.dumps(self.custom_summaries, indent=2, ensure_ascii=False),
                encoding='utf-8', newline='\n'
            )
        except Exception:
            pass

    def _on_changes_double_click(self, event) -> None:
        try:
            col = self.changes_tree.identify_column(event.x)
            if col == '#5':  # summary column
                self.edit_selected_summary(from_summary_tab=False)
            else:
                # Open file in default editor
                selection = self.changes_tree.selection()
                if selection:
                    item = self.changes_tree.item(selection[0])
                    file_path = item['values'][1]
                    self.open_file_in_editor(file_path)
        except Exception:
            pass

    def open_file_in_editor(self, file_path: str) -> None:
        """Open a file in the system's default editor with change highlighting."""
        try:
            full_path = self.config_root / file_path
            
            if not full_path.exists():
                self._set_status(f"File not found: {file_path}")
                return
            
            # Get the workspace root (Valheim_Testing directory)
            workspace_root = Path(__file__).resolve().parents[1]
            
            # Try to open with VS Code first (most common for development)
            system = platform.system().lower()
            
            if system == "windows":
                # Try VS Code first, then fall back to default
                try:
                    # Use VS Code with workspace folder and goto line if possible
                    line_number = self._get_first_change_line(file_path)
                    if line_number:
                        subprocess.Popen(['code', '-g', f'{full_path}:{line_number}', str(workspace_root)], shell=True)
                    else:
                        subprocess.Popen(['code', str(workspace_root)], shell=True)
                    self._set_status(f"Opened {file_path} in VS Code (workspace: {workspace_root.name})")
                    return
                except FileNotFoundError:
                    # Fall back to default editor
                    subprocess.Popen(['start', str(full_path)], shell=True)
            elif system == "darwin":  # macOS
                try:
                    line_number = self._get_first_change_line(file_path)
                    if line_number:
                        subprocess.Popen(['code', '-g', f'{full_path}:{line_number}', str(workspace_root)])
                    else:
                        subprocess.Popen(['code', str(workspace_root)])
                    self._set_status(f"Opened {file_path} in VS Code (workspace: {workspace_root.name})")
                    return
                except FileNotFoundError:
                    subprocess.Popen(['open', str(full_path)])
            else:  # Linux and other Unix-like systems
                try:
                    line_number = self._get_first_change_line(file_path)
                    if line_number:
                        subprocess.Popen(['code', '-g', f'{full_path}:{line_number}', str(workspace_root)])
                    else:
                        subprocess.Popen(['code', str(workspace_root)])
                    self._set_status(f"Opened {file_path} in VS Code (workspace: {workspace_root.name})")
                    return
                except FileNotFoundError:
                    # Try other editors
                    editors = ['nano', 'vim', 'gedit', 'kate', 'mousepad']
                    for editor in editors:
                        try:
                            subprocess.Popen([editor, str(full_path)])
                            break
                        except FileNotFoundError:
                            continue
                    else:
                        # Fall back to xdg-open
                        try:
                            subprocess.Popen(['xdg-open', str(full_path)])
                        except FileNotFoundError:
                            self._set_status(f"Could not open {file_path} - no suitable editor found")
                            return
            
            self._set_status(f"Opened {file_path} in default editor")
            
        except Exception as e:
            self._set_status(f"Error opening {file_path}: {e}")

    def _get_first_change_line(self, file_path: str) -> int | None:
        """Get the line number of the first change in the file for editor navigation."""
        try:
            # Determine comparison type
            compare_against = "initial" if self.compare_var.get() == "Since Baseline (All-Time)" else "current"
            diff = self.snapshot.get_diff(file_path, compare_against)
            
            if not diff or diff.startswith("[Ignored path:") or diff.startswith("File not found"):
                return None
            
            # Parse the diff to find the first change
            lines = diff.splitlines()
            for line in lines:
                # Look for @@ lines that indicate change locations
                if line.startswith("@@"):
                    # Extract line number from @@ -old_start,old_count +new_start,new_count @@
                    match = re.search(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
                    if match:
                        return int(match.group(1))
                # Look for + or - lines that indicate actual changes
                elif line.startswith('+') and not line.startswith('+++'):
                    # This is an added line, we need to find its context
                    # For simplicity, return None and let editor open normally
                    return None
                elif line.startswith('-') and not line.startswith('---'):
                    # This is a deleted line, we need to find its context
                    return None
            
            return None
        except Exception:
            return None

    def _generate_relicheim_diff_summary(self, current_content: str, base_content: str) -> str:
        """Generate a brief summary of differences between files."""
        try:
            # Parse both files as config-like
            current_kv = self.snapshot._parse_cfg_like(current_content)
            base_kv = self.snapshot._parse_cfg_like(base_content)
            
            # Count differences
            added = 0
            removed = 0
            modified = 0
            
            for key in set(current_kv.keys()) | set(base_kv.keys()):
                if key not in base_kv:
                    added += 1
                elif key not in current_kv:
                    removed += 1
                elif current_kv[key] != base_kv[key]:
                    modified += 1
            
            if added == 0 and removed == 0 and modified == 0:
                return "No changes detected"
            
            parts = []
            if added > 0:
                parts.append(f"+{added}")
            if removed > 0:
                parts.append(f"-{removed}")
            if modified > 0:
                parts.append(f"~{modified}")
            
            return f"{', '.join(parts)} changes"
        except Exception:
            # Fallback to line-based comparison
            current_lines = current_content.splitlines()
            base_lines = base_content.splitlines()
            
            added = sum(1 for line in current_lines if line.strip() and line.strip() not in base_lines)
            removed = sum(1 for line in base_lines if line.strip() and line.strip() not in current_lines)
            
            if added == 0 and removed == 0:
                return "No changes detected"
            
            parts = []
            if added > 0:
                parts.append(f"+{added} lines")
            if removed > 0:
                parts.append(f"-{removed} lines")
            
            return f"{', '.join(parts)}"

    def edit_selected_summary(self, from_summary_tab: bool) -> None:
        tree = self.summary_tree if from_summary_tab else self.changes_tree
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0]).get('values', [])
        # Determine file path and current summary based on tree shape
        if from_summary_tab:
            if len(vals) < 2:
                return
            file_path = vals[1]
            if not file_path or str(file_path).startswith('['):
                return
            current_summary = vals[2] if len(vals) >= 3 else ""
        else:
            if len(vals) < 5:
                return
            file_path = vals[1]
            current_summary = vals[4]

        # Pre-fill with custom override if present
        initial_text = self.custom_summaries.get(file_path, current_summary)

        # Build modal editor
        try:
            win = tk.Toplevel(self.root)
            win.title("Edit Summary")
            win.geometry("700x260")
            win.configure(bg=self.colors["bg"]) 

            tk.Label(win, text=f"File: {file_path}", bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor='w', padx=8, pady=(8,4))

            txt = tk.Text(win, height=5, bg=self.colors["panel"], fg=self.colors["text"], wrap=tk.WORD, font=self.font)
            txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
            txt.insert('1.0', initial_text)

            btns = ttk.Frame(win)
            btns.pack(fill=tk.X, padx=8, pady=8)

            def do_save():
                new_val = txt.get('1.0', 'end').strip()
                if new_val:
                    self.custom_summaries[file_path] = new_val
                else:
                    # Empty means clear
                    self.custom_summaries.pop(file_path, None)
                self._save_custom_summaries()
                win.destroy()
                # Refresh both views to reflect change
                self.refresh_changes()
                # Update summary tab if active
                self.show_baseline_summary()

            def do_clear():
                self.custom_summaries.pop(file_path, None)
                self._save_custom_summaries()
                win.destroy()
                self.refresh_changes()
                self.show_baseline_summary()

            ttk.Button(btns, text="Save", style="Action.TButton", command=do_save).pack(side=tk.LEFT, padx=(0,6))
            ttk.Button(btns, text="Clear Override", style="Action.TButton", command=do_clear).pack(side=tk.LEFT, padx=(0,6))
            ttk.Button(btns, text="Cancel", style="Action.TButton", command=win.destroy).pack(side=tk.LEFT)
        except Exception as e:
            self._set_status(f"Error editing summary: {e}")

    def clear_selected_summary(self, from_summary_tab: bool) -> None:
        tree = self.summary_tree if from_summary_tab else self.changes_tree
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0]).get('values', [])
        file_path = None
        if from_summary_tab:
            if len(vals) >= 2 and vals[1] and not str(vals[1]).startswith('['):
                file_path = vals[1]
        else:
            if len(vals) >= 2:
                file_path = vals[1]
        if not file_path:
            return
        if file_path in self.custom_summaries:
            self.custom_summaries.pop(file_path, None)
            self._save_custom_summaries()
            self._set_status(f"Cleared custom summary for {file_path}")
            self.refresh_changes()
            self.show_baseline_summary()

    def _open_from_summary(self, event=None) -> None:
        try:
            col = self.summary_tree.identify_column(event.x) if event else ''
            sel = self.summary_tree.selection()
            if not sel:
                return
            vals = self.summary_tree.item(sel[0]).get('values', [])
            if len(vals) < 2:
                return
            file_path = vals[1]
            if not file_path or str(file_path).startswith('['):
                return
            # If summary column was double-clicked, open editor; otherwise open diff
            if col == '#3':
                self.edit_selected_summary(from_summary_tab=True)
                return
            try:
                self.right_notebook.select(self.diff_tab)
            except Exception:
                pass

            def worker():
                try:
                    diff = self.snapshot.get_diff(file_path, compare_against="initial")
                    self.root.after(0, lambda: self._show_diff(diff, file_path, "initial"))
                except Exception as e:
                    self.root.after(0, lambda: self._set_status(f"Error loading diff: {e}"))

            threading.Thread(target=worker, daemon=True).start()
        except Exception:
            pass

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
        """Populate the embedded All-Time Summary tab and switch to it."""
        def worker():
            try:
                self.root.after(0, lambda: self._set_busy(True, "Building all-time summary..."))
                changes = self.snapshot.get_changes("initial")
                grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
                for status, file_path, mod, session in changes:
                    summary = self.snapshot.summarize_change(file_path, compare_against="initial", max_items=3)
                    grouped[mod].append((status, file_path, summary))

                def update_summary():
                    try:
                        # Clear current rows
                        for iid in self.summary_tree.get_children(""):
                            self.summary_tree.delete(iid)
                        # Insert grouped rows
                        for mod in sorted(grouped.keys()):
                            parent = self.summary_tree.insert("", "end", values=("", f"[{mod}]", ""))
                            for status, file_path, summary in grouped[mod]:
                                status_display = { 'A': 'Added', 'M': 'Modified', 'D': 'Deleted' }.get(status, status)
                                self.summary_tree.insert(parent, "end", values=(status_display, file_path, summary))
                        # Expand all
                        for iid in self.summary_tree.get_children(""):
                            self.summary_tree.item(iid, open=True)
                        # Switch to tab
                        self.right_notebook.select(self.summary_tab)
                        self._set_busy(False, "All-Time Summary updated")
                    except Exception as e:
                        self._set_busy(False, f"Error updating summary: {e}")

                self.root.after(0, update_summary)
            except Exception as e:
                self.root.after(0, lambda: self._set_busy(False, f"Error: {e}"))

        threading.Thread(target=worker, daemon=True).start()

    def _open_diff_from_summary(self, _event=None) -> None:
        try:
            sel = self.summary_tree.selection()
            if not sel:
                return
            vals = self.summary_tree.item(sel[0]).get('values', [])
            if len(vals) < 2:
                return
            file_path = vals[1]
            if not file_path or file_path.startswith('['):
                return
            # Switch to Diff tab and load diff vs baseline
            try:
                self.right_notebook.select(self.diff_tab)
            except Exception:
                pass

            def worker():
                try:
                    self.root.after(0, lambda: self._set_busy(True, "Loading diff..."))
                    diff = self.snapshot.get_diff(file_path, compare_against="initial")
                    self.root.after(0, lambda: (self._show_diff(diff, file_path, "initial"), self._set_busy(False)))
                except Exception as e:
                    self.root.after(0, lambda: self._set_busy(False, f"Error loading diff: {e}"))

            threading.Thread(target=worker, daemon=True).start()
        except Exception:
            pass

    def show_relicheim_comparison(self) -> None:
        """Show a comparison between current config files and RelicHeim base files.
        
        This function performs a comprehensive comparison between the current configuration
        files and the base RelicHeim installation files. It includes:
        
        1. Explicit file mappings for known RelicHeim files
        2. Directory-based comparisons for subdirectories
        3. Keyword-based detection for unmapped RelicHeim-related files
        4. Detection of backup files that aren't being used
        5. Comprehensive categorization of all files by mod/plugin
        
        The comparison covers all major RelicHeim components including:
        - Core mods (EpicMMO, EpicLoot, Drop That, Custom Raids, etc.)
        - Smoothbrain plugins (all org.bepinex.plugins.* files)
        - Creature and item configurations
        - Spawn That and Drop That configurations
        - Additional mods (Warpalicious, Vapok, Southsil, etc.)
        - System and utility files
        """
        try:
            win = tk.Toplevel(self.root)
            win.title("RelicHeim Base Comparison")
            win.geometry("1200x800")
            win.configure(bg=self.colors["bg"])

            # Create main container
            main_frame = ttk.Frame(win)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

            # Header
            header_frame = ttk.Frame(main_frame)
            header_frame.pack(fill=tk.X, pady=(0, 8))
            
            title_frame = ttk.Frame(header_frame)
            title_frame.pack(fill=tk.X)
            
            tk.Label(title_frame, text="Changes from RelicHeim Base Files", 
                    bg=self.colors["bg"], fg=self.colors["text"], 
                    font=("Arial", 12, "bold")).pack(side=tk.LEFT)
            
            # Export button
            export_btn = ttk.Button(title_frame, text="Export to MD", 
                                   style="Action.TButton", 
                                   command=lambda: export_to_markdown())
            export_btn.pack(side=tk.RIGHT, padx=(10, 0))
            
            # Add tooltip for export button
            try:
                Tooltip(export_btn, "Export the complete comparison results to a markdown file for further analysis")
            except Exception:
                pass
            
            tk.Label(header_frame, text="Right-click any item to open in editor", 
                    bg=self.colors["bg"], fg=self.colors["accent"]).pack(anchor="w")

            # Create treeview for comparison results
            cols = ("status", "file", "category", "summary")
            tree = ttk.Treeview(main_frame, columns=cols, show="headings")
            for c, w in [("status", 80), ("file", 400), ("category", 150), ("summary", 500)]:
                tree.heading(c, text=c.capitalize())
                tree.column(c, width=w)
            tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

            # Scrollbar
            yscroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=yscroll.set)
            yscroll.pack(fill=tk.Y, side=tk.RIGHT)

            # Get the backup directory path
            backup_dir = Path(__file__).resolve().parents[1] / "Valheim_Help_Docs" / "JewelHeim-RelicHeim-5.4.10_Backup" / "config"
            
            # RelicHeim file mapping - current file to backup file
            relicheim_mapping = {
                # Core mod files
                "WackyMole.EpicMMOSystem.cfg": "WackyMole.EpicMMOSystembackup.cfg",
                "WackyMole.EpicMMOSystemUI.cfg": "WackyMole.EpicMMOSystembackup.cfg",  # May be part of main config
                "randyknapp.mods.epicloot.cfg": "randyknapp.mods.epiclootbackup.cfg",
                "drop_that.cfg": "drop_thatbackup.cfg",
                "drop_that.character_drop.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBasebackup.cfg",
                "drop_that.drop_table.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.zBasebackup.cfg",
                "drop_that.character_drop.elite_additions.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBasebackup.cfg",
                "custom_raids.cfg": "custom_raidsbackup.cfg",
                "custom_raids.raids.cfg": "custom_raidsbackup.cfg",  # May be part of main config
                "custom_raids.supplemental.deathsquitoseason.cfg": "_RelicHeimFiles/Raids/custom_raids.supplemental.MoreRaidsbackup.cfg",
                "custom_raids.supplemental.ragnarok.cfg": "_RelicHeimFiles/Raids/custom_raids.supplemental.MoreRaidsbackup.cfg",
                "advize.PlantEverything.cfg": "advize.PlantEverythingbackup.cfg",
                "kg.ValheimEnchantmentSystem.cfg": "kg.ValheimEnchantmentSystembackup.cfg",
                "WackyMole.Tone_Down_the_Twang.cfg": "WackyMole.Tone_Down_the_Twangbackup.cfg",
                
                # Smoothbrain plugins - ALL of them
                "org.bepinex.plugins.smartskills.cfg": "org.bepinex.plugins.smartskillsbackup.cfg",
                "org.bepinex.plugins.targetportal.cfg": "org.bepinex.plugins.targetportalbackup.cfg",
                "org.bepinex.plugins.tenacity.cfg": "org.bepinex.plugins.tenacitybackup.cfg",
                "org.bepinex.plugins.sailing.cfg": "org.bepinex.plugins.sailingbackup.cfg",
                "org.bepinex.plugins.sailingspeed.cfg": "org.bepinex.plugins.sailingspeedbackup.cfg",
                "org.bepinex.plugins.passivepowers.cfg": "org.bepinex.plugins.passivepowersbackup.cfg",
                "org.bepinex.plugins.packhorse.cfg": "org.bepinex.plugins.packhorsebackup.cfg",
                "org.bepinex.plugins.mining.cfg": "org.bepinex.plugins.miningbackup.cfg",
                "org.bepinex.plugins.lumberjacking.cfg": "org.bepinex.plugins.lumberjackingbackup.cfg",
                "org.bepinex.plugins.foraging.cfg": "org.bepinex.plugins.foragingbackup.cfg",
                "org.bepinex.plugins.farming.cfg": "org.bepinex.plugins.farmingbackup.cfg",
                "org.bepinex.plugins.creaturelevelcontrol.cfg": "org.bepinex.plugins.creaturelevelcontrolbackup.cfg",
                "org.bepinex.plugins.conversionsizespeed.cfg": "org.bepinex.pluginsbackup.conversionsizespeed.cfg",
                "org.bepinex.plugins.building.cfg": "org.bepinex.pluginsbackup.building.cfg",
                "org.bepinex.plugins.blacksmithing.cfg": "org.bepinex.pluginsbackup.blacksmithing.cfg",
                "org.bepinex.plugins.backpacks.cfg": "org.bepinex.pluginsbackup.backpacks.cfg",
                "org.bepinex.plugins.ranching.cfg": "org.bepinex.pluginsbackup.backpacks.cfg",  # May not have backup
                "org.bepinex.plugins.groups.cfg": "org.bepinex.pluginsbackup.backpacks.cfg",  # May not have backup
                "org.bepinex.plugins.exploration.cfg": "org.bepinex.pluginsbackup.backpacks.cfg",  # May not have backup
                "org.bepinex.plugins.cooking.cfg": "org.bepinex.pluginsbackup.backpacks.cfg",  # May not have backup
                
                # Other important mods
                "RandomSteve.BreatheEasy.cfg": "RandomSteve.BreatheEasybackup.cfg",
                "Azumatt.AzuCraftyBoxes.cfg": "Azumatt.AzuCraftyBoxesbackup.yml",
                "Azumatt.FactionAssigner.cfg": "Azumatt.FactionAssignerbackup.yml",
                "horemvore.MushroomMonsters.cfg": "CreatureConfig_Creaturesbackup.yml",  # May be part of creature config
                "flueno.SmartContainers.cfg": "org.bepinex.pluginsbackup.backpacks.cfg",  # May not have backup
                
                # Creature configs (if they exist in current config)
                "CreatureConfig_Creatures.yml": "CreatureConfig_Creaturesbackup.yml",
                "CreatureConfig_Bosses.yml": "CreatureConfig_Bossesbackup.yml",
                "CreatureConfig_BiomeIncrease.yml": "CreatureConfig_BiomeIncreasebackup.yml",
                "CreatureConfig_Monstrum.yml": "CreatureConfig_Monstrumbackup.yml",
                "CreatureConfig_Wizardry.yml": "CreatureConfig_Wizardrybackup.yml",
                
                # Backpack configs (if they exist in current config)
                "Backpacks.Wizardry.yml": "Backpacks.Wizardrybackup.yml",
                "Backpacks.MajesticEpicLoot.yml": "Backpacks.MajesticEpicLootbackup.yml",
                "Backpacks.Majestic.yml": "Backpacks.Majesticbackup.yml",
                
                # Item configs (if they exist in current config)
                "ItemConfig_Base.yml": "ItemConfig_Basebackup.yml",
                
                # Spawn That files (if they exist in current config)
                "spawn_that.cfg": "_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBasebackup.cfg",
                "spawn_that.world_spawners_advanced.cfg": "_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBasebackup.cfg",
                "spawn_that.local_spawners_advanced.cfg": "_RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.Localsbackup.cfg",
                "spawn_that.spawnarea_spawners.cfg": "_RelicHeimFiles/Drop,Spawn_That/spawn_that.spawnarea_spawners.PilesNestsbackup.cfg",
                "spawn_that.simple.cfg": "_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBasebackup.cfg",
                
                # This Goes Here files (if they exist in current config)
                "Valheim.ThisGoesHere.MovingFiles.yml": "_RelicHeimFiles/Valheim.ThisGoesHere.MovingFilesbackup.yml",
                "Valheim.ThisGoesHere.DeletingFiles.yml": "_RelicHeimFiles/Valheim.ThisGoesHere.DeletingFilesbackup.yml",
                "Valheim.ThisGoesHere.DeleteWDBCache.yml": "_RelicHeimFiles/Valheim.ThisGoesHere.DeleteWDBCachebackup.yml",
                
                # Additional Drop That files (if they exist in current config)
                "drop_that.character_drop_list.zListDrops.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop_list.zListDropsbackup.cfg",
                "drop_that.character_drop.Wizardry.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Wizardrybackup.cfg",
                "drop_that.character_drop.VES.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.VESbackup.cfg",
                "drop_that.character_drop.Monstrum.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Monstrumbackup.cfg",
                "drop_that.character_drop.GoldTrophy.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.GoldTrophybackup.cfg",
                "drop_that.character_drop.Bosses.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bossesbackup.cfg",
                "drop_that.character_drop.aListDrops.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.aListDropsbackup.cfg",
                "drop_that.drop_table.EpicLootChest.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.EpicLootChestbackup.cfg",
                "drop_that.drop_table.Chests.cfg": "_RelicHeimFiles/Drop,Spawn_That/drop_that.drop_table.Chestsbackup.cfg",
                
                # Additional Spawn That files (if they exist in current config)
                "spawn_that.world_spawners.zVanilla.cfg": "_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zVanillabackup.cfg",
                "spawn_that.world_spawners.zBossSpawns.cfg": "_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBossSpawnsbackup.cfg",
                "spawn_that.local_spawners.LocalsDungeons.cfg": "_RelicHeimFiles/Drop,Spawn_That/spawn_that.local_spawners.LocalsDungeonsbackup.cfg",
                
                # Additional Custom Raids files (if they exist in current config)
                "custom_raids.supplemental.WizardryRaids.cfg": "_RelicHeimFiles/Raids/custom_raids.supplemental.WizardryRaidsbackup.cfg",
                "custom_raids.supplemental.VanillaRaids.cfg": "_RelicHeimFiles/Raids/custom_raids.supplemental.VanillaRaidsbackup.cfg",
                "custom_raids.supplemental.MonstrumRaids.cfg": "_RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumRaidsbackup.cfg",
                "custom_raids.supplemental.MonstrumDNRaids.cfg": "_RelicHeimFiles/Raids/custom_raids.supplemental.MonstrumDNRaidsbackup.cfg",
                
                # EpicMMO System files (if they exist in current config)
                "EpicMMOSystem/Version.txt": "EpicMMOSystembackup/Version.txt",
                "EpicMMOSystem/Valheim.ThisGoesHere.EpicMMOCleanup.yml": "EpicMMOSystembackup/Valheim.ThisGoesHere.EpicMMOCleanup.yml",
                "EpicMMOSystem/Therzie_Wizardry.json": "EpicMMOSystembackup/Therzie_Wizardry.json",
                "EpicMMOSystem/Therzie_Monstrum.json": "EpicMMOSystembackup/Therzie_Monstrum.json",
                "EpicMMOSystem/Monstrum_DeepNorth.json": "EpicMMOSystembackup/Monstrum_DeepNorth.json",
                "EpicMMOSystem/Jewelcrafting.json": "EpicMMOSystembackup/Jewelcrafting.json",
                "EpicMMOSystem/Default.json": "EpicMMOSystembackup/Default.json",
                
                # Valheim Enchantment System files (if they exist in current config)
                "ValheimEnchantmentSystem/ScrollRecipes.cfg": "ValheimEnchantmentSystembackup/ScrollRecipes.cfg",
                "ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg": "ValheimEnchantmentSystembackup/kg.ValheimEnchantmentSystem.cfg",
                "ValheimEnchantmentSystem/EnchantmentStats_Weapons.yml": "ValheimEnchantmentSystembackup/EnchantmentStats_Weapons.yml",
                "ValheimEnchantmentSystem/EnchantmentStats_Armor.yml": "ValheimEnchantmentSystembackup/EnchantmentStats_Armor.yml",
                "ValheimEnchantmentSystem/EnchantmentReqs.yml": "ValheimEnchantmentSystembackup/EnchantmentReqs.yml",
                "ValheimEnchantmentSystem/EnchantmentColors.yml": "ValheimEnchantmentSystembackup/EnchantmentColors.yml",
                "ValheimEnchantmentSystem/EnchantmentChancesV2.yml": "ValheimEnchantmentSystembackup/EnchantmentChancesV2.yml",
                
                # WackyDatabase files (if they exist in current config)
                "wackysDatabase/": "wackysDatabase_backup/",
                
                # EpicLoot files (if they exist in current config)
                "EpicLoot/": "EpicLootbackup/",
                
                # NEW ADDITIONS - Missing files that exist in current config
                
                # Warpalicious mods (multiple files)
                "warpalicious.Swamp_Pack_1.cfg": "warpalicious.Swamp_Pack_1backup.cfg",  # May not have backup
                "warpalicious.Underground_Ruins.cfg": "warpalicious.Underground_Ruinsbackup.cfg",  # May not have backup
                "warpalicious.More_World_Traders.cfg": "warpalicious.More_World_Tradersbackup.cfg",  # May not have backup
                "warpalicious.Mountains_Pack_1.cfg": "warpalicious.Mountains_Pack_1backup.cfg",  # May not have backup
                "warpalicious.Plains_Pack_1.cfg": "warpalicious.Plains_Pack_1backup.cfg",  # May not have backup
                "warpalicious.More_World_Locations_LootLists.yml": "warpalicious.More_World_Locations_LootListsbackup.yml",  # May not have backup
                "warpalicious.More_World_Locations_PickableItemLists.yml": "warpalicious.More_World_Locations_PickableItemListsbackup.yml",  # May not have backup
                "warpalicious.More_World_Locations_CreatureLists.yml": "warpalicious.More_World_Locations_CreatureListsbackup.yml",  # May not have backup
                "warpalicious.Meadows_Pack_2.cfg": "warpalicious.Meadows_Pack_2backup.cfg",  # May not have backup
                "warpalicious.Mistlands_Pack_1.cfg": "warpalicious.Mistlands_Pack_1backup.cfg",  # May not have backup
                "warpalicious.Meadows_Pack_1.cfg": "warpalicious.Meadows_Pack_1backup.cfg",  # May not have backup
                "warpalicious.Forbidden_Catacombs.cfg": "warpalicious.Forbidden_Catacombsbackup.cfg",  # May not have backup
                "warpalicious.MWL_Blackforest_Pack_1.cfg": "warpalicious.MWL_Blackforest_Pack_1backup.cfg",  # May not have backup
                "warpalicious.AshlandsPack1.cfg": "warpalicious.AshlandsPack1backup.cfg",  # May not have backup
                "warpalicious.Blackforest_Pack_2.cfg": "warpalicious.Blackforest_Pack_2backup.cfg",  # May not have backup
                "warpalicious.Adventure_Map_Pack_1.cfg": "warpalicious.Adventure_Map_Pack_1backup.cfg",  # May not have backup
                
                # Vapok mods
                "vapok.mods.adventurebackpacks.cfg": "vapok.mods.adventurebackpacksbackup.cfg",  # May not have backup
                
                # Southsil mods
                "southsil.SouthsilArmor.cfg": "southsil.SouthsilArmorbackup.cfg",  # May not have backup
                
                # Shudnal mods
                "shudnal.TradersExtended.cfg": "shudnal.TradersExtendedbackup.cfg",  # May not have backup
                "shudnal.TradersExtended.MWL_PlainsCamp1_Trader.buy.json": "shudnal.TradersExtended.MWL_PlainsCamp1_Trader.buybackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_PlainsCamp1_Trader.sell.json": "shudnal.TradersExtended.MWL_PlainsCamp1_Trader.sellbackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_PlainsTavern1_Trader.buy.json": "shudnal.TradersExtended.MWL_PlainsTavern1_Trader.buybackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_PlainsTavern1_Trader.sell.json": "shudnal.TradersExtended.MWL_PlainsTavern1_Trader.sellbackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_MountainsBlacksmith1_Trader.sell.json": "shudnal.TradersExtended.MWL_MountainsBlacksmith1_Trader.sellbackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_OceanTavern1_Trader.buy.json": "shudnal.TradersExtended.MWL_OceanTavern1_Trader.buybackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_OceanTavern1_Trader.sell.json": "shudnal.TradersExtended.MWL_OceanTavern1_Trader.sellbackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_MistlandsBlacksmith1_Trader.sell.json": "shudnal.TradersExtended.MWL_MistlandsBlacksmith1_Trader.sellbackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_MountainsBlacksmith1_Trader.buy.json": "shudnal.TradersExtended.MWL_MountainsBlacksmith1_Trader.buybackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_BlackForestBlacksmith1_Trader.buy.json": "shudnal.TradersExtended.MWL_BlackForestBlacksmith1_Trader.buybackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_BlackForestBlacksmith1_Trader.sell.json": "shudnal.TradersExtended.MWL_BlackForestBlacksmith1_Trader.sellbackup.json",  # May not have backup
                "shudnal.TradersExtended.MWL_MistlandsBlacksmith1_Trader.buy.json": "shudnal.TradersExtended.MWL_MistlandsBlacksmith1_Trader.buybackup.json",  # May not have backup
                "shudnal.Seasons.cfg": "shudnal.Seasonsbackup.cfg",  # May not have backup
                
                # Server and system files
                "server_devcommands.cfg": "server_devcommandsbackup.cfg",  # May not have backup
                "org.bepinex.valheim.displayinfo.cfg": "org.bepinex.valheim.displayinfobackup.cfg",  # May not have backup
                
                # Redseiko mods
                "redseiko.valheim.scenic.cfg": "redseiko.valheim.scenicbackup.cfg",  # May not have backup
                
                # OdinPlus mods
                "odinplus.plugins.odinskingdom.cfg": "odinplus.plugins.odinskingdombackup.cfg",  # May not have backup
                
                # Nex mods
                "nex.SpeedyPaths.cfg": "nex.SpeedyPathsbackup.cfg",  # May not have backup
                
                # Marcopogo mods
                "marcopogo.PlanBuild.cfg": "marcopogo.PlanBuildbackup.cfg",  # May not have backup
                
                # Marlthon mods
                "marlthon.OdinShipPlus.cfg": "marlthon.OdinShipPlusbackup.cfg",  # May not have backup
                
                # HTD mods
                "htd.armory.cfg": "htd.armorybackup.cfg",  # May not have backup
                
                # GoldenRevolver mods
                "goldenrevolver.quick_stack_store.cfg": "goldenrevolver.quick_stack_storebackup.cfg",  # May not have backup
                
                # Com mods
                "com.maxsch.valheim.vnei.cfg": "com.maxsch.valheim.vneibackup.cfg",  # May not have backup
                "com.odinplus.potionsplus.cfg": "com.odinplus.potionsplusbackup.cfg",  # May not have backup
                "com.bepis.bepinex.configurationmanager.cfg": "com.bepis.bepinex.configurationmanagerbackup.cfg",  # May not have backup
                "com.maxsch.valheim.pressure_plate.cfg": "com.maxsch.valheim.pressure_platebackup.cfg",  # May not have backup
                "com.maxsch.valheim.vnei.blacklist.txt": "com.maxsch.valheim.vnei.blacklistbackup.txt",  # May not have backup
                
                # Blacks7ar mods
                "blacks7ar.MagicRevamp.cfg": "blacks7ar.MagicRevampbackup.cfg",  # May not have backup
                "blacks7ar.FineWoodBuildPieces.cfg": "blacks7ar.FineWoodBuildPiecesbackup.cfg",  # May not have backup
                "blacks7ar.FineWoodFurnitures.cfg": "blacks7ar.FineWoodFurnituresbackup.cfg",  # May not have backup
                "blacks7ar.CookingAdditions.cfg": "blacks7ar.CookingAdditionsbackup.cfg",  # May not have backup
                
                # ZenDragon mods
                "ZenDragon.ZenUI.cfg": "ZenDragon.ZenUIbackup.cfg",  # May not have backup
                "WackyMole.WackysDatabase.cfg": "WackyMole.WackysDatabasebackup.cfg",  # May not have backup
                "ZenDragon.Zen.ModLib.cfg": "ZenDragon.Zen.ModLibbackup.cfg",  # May not have backup
                "WackyMole.EpicMMOSystemUI.cfg": "WackyMole.EpicMMOSystemUIbackup.cfg",  # May not have backup
                
                # Other files
                "binds.yaml": "bindsbackup.yaml",  # May not have backup
                "upgrade_world.cfg": "upgrade_worldbackup.cfg",  # May not have backup
                
                # Directory mappings for subdirectories
                "wackyDatabase-BulkYML/": "wackyDatabase-BulkYML_backup/",  # May not have backup
                "shudnal.Seasons/": "shudnal.Seasons_backup/",  # May not have backup
                "_RelicHeimFiles/": "_RelicHeimFiles_backup/",  # May not have backup
            }

            def get_file_category(filename: str) -> str:
                """Get category for file based on name."""
                # Handle subdirectory paths
                if '/' in filename or '\\' in filename:
                    # Extract the first directory or file name
                    parts = filename.replace('\\', '/').split('/')
                    if parts:
                        first_part = parts[0]
                        if first_part == "EpicMMOSystem":
                            return "EpicMMO System"
                        elif first_part == "ValheimEnchantmentSystem":
                            return "Enchantment System"
                        elif first_part == "wackysDatabase":
                            return "WackyDatabase"
                        elif first_part == "EpicLoot":
                            return "EpicLoot"
                        elif first_part == "wackyDatabase-BulkYML":
                            return "WackyDatabase Bulk"
                
                # Handle regular file names
                if filename.startswith("WackyMole.EpicMMOSystem"):
                    return "EpicMMO"
                elif filename.startswith("randyknapp.mods.epicloot"):
                    return "EpicLoot"
                elif filename.startswith("drop_that"):
                    return "Drop That"
                elif filename.startswith("custom_raids"):
                    return "Custom Raids"
                elif filename.startswith("org.bepinex.plugins"):
                    return "Smoothbrain"
                elif filename.startswith("CreatureConfig"):
                    return "Creature Config"
                elif filename.startswith("Backpacks"):
                    return "Backpacks"
                elif filename.startswith("ItemConfig"):
                    return "Item Config"
                elif filename.startswith("advize.PlantEverything"):
                    return "Plant Everything"
                elif filename.startswith("kg.ValheimEnchantmentSystem"):
                    return "Enchantment System"
                elif filename.startswith("WackyMole.Tone_Down_the_Twang"):
                    return "Tone Down Twang"
                elif filename.startswith("RandomSteve.BreatheEasy"):
                    return "Breathe Easy"
                elif filename.startswith("Azumatt"):
                    return "Azumatt Mods"
                elif filename.startswith("horemvore.MushroomMonsters"):
                    return "Mushroom Monsters"
                elif filename.startswith("flueno.SmartContainers"):
                    return "Smart Containers"
                elif filename.startswith("spawn_that"):
                    return "Spawn That"
                elif filename.startswith("Valheim.ThisGoesHere"):
                    return "This Goes Here"
                elif filename.startswith("shudnal"):
                    return "Shudnal Mods"
                elif filename.startswith("blacks7ar"):
                    return "Blacks7ar Mods"
                elif filename.startswith("odinplus"):
                    return "OdinPlus Mods"
                elif filename.startswith("com.maxsch"):
                    return "MaxSch Mods"
                elif filename.startswith("com.odinplus"):
                    return "OdinPlus Com"
                elif filename.startswith("com.bepis"):
                    return "BepInEx"
                elif filename.startswith("warpalicious"):
                    return "Warpalicious"
                elif filename.startswith("nex"):
                    return "Nex Mods"
                elif filename.startswith("marcopogo"):
                    return "Marcopogo"
                elif filename.startswith("marlthon"):
                    return "Marlthon"
                elif filename.startswith("htd"):
                    return "HTD Mods"
                elif filename.startswith("goldenrevolver"):
                    return "GoldenRevolver"
                elif filename.startswith("vapok"):
                    return "Vapok Mods"
                elif filename.startswith("southsil"):
                    return "Southsil"
                elif filename.startswith("redseiko"):
                    return "Redseiko"
                elif filename.startswith("ZenDragon"):
                    return "ZenDragon"
                elif filename.startswith("warpalicious"):
                    return "Warpalicious"
                elif filename.startswith("vapok"):
                    return "Vapok Mods"
                elif filename.startswith("southsil"):
                    return "Southsil"
                elif filename.startswith("shudnal"):
                    return "Shudnal Mods"
                elif filename.startswith("server_devcommands"):
                    return "Server Commands"
                elif filename.startswith("redseiko"):
                    return "Redseiko"
                elif filename.startswith("marcopogo"):
                    return "Marcopogo"
                elif filename.startswith("marlthon"):
                    return "Marlthon"
                elif filename.startswith("goldenrevolver"):
                    return "GoldenRevolver"
                elif filename.startswith("flueno"):
                    return "Flueno"
                elif filename.startswith("com.maxsch"):
                    return "MaxSch Mods"
                elif filename.startswith("com.odinplus"):
                    return "OdinPlus Com"
                elif filename.startswith("com.bepis"):
                    return "BepInEx"
                elif filename.startswith("blacks7ar"):
                    return "Blacks7ar Mods"
                elif filename.startswith("binds"):
                    return "Key Bindings"
                elif filename.startswith("upgrade_world"):
                    return "World Upgrade"
                elif filename.startswith("EnchantmentStats"):
                    return "Enchantment Stats"
                elif filename.startswith("EnchantmentReqs"):
                    return "Enchantment Reqs"
                elif filename.startswith("EnchantmentColors"):
                    return "Enchantment Colors"
                elif filename.startswith("EnchantmentChances"):
                    return "Enchantment Chances"
                elif filename.startswith("ScrollRecipes"):
                    return "Enchantment Scrolls"
                elif filename.startswith("Therzie_"):
                    return "Therzie Mods"
                elif filename.startswith("Monstrum_"):
                    return "Monstrum Mods"
                elif filename.startswith("Jewelcrafting"):
                    return "Jewelcrafting"
                elif filename.startswith("Version"):
                    return "System Files"
                else:
                    return "Other"

            def compare_files():
                """Compare current files with RelicHeim base files."""
                tree.delete(*tree.get_children())
                
                # Track which backup files are actually used
                used_backup_files = set()
                
                # First, check all mapped files
                for current_file, backup_file in relicheim_mapping.items():
                    current_path = self.config_root / current_file
                    backup_path = backup_dir / backup_file
                    
                    # Handle directory mappings (for wackysDatabase and EpicLoot)
                    if backup_file.endswith('/'):
                        # This is a directory mapping - scan all files in the directory
                        if current_path.exists() and current_path.is_dir():
                            for subfile in current_path.rglob('*'):
                                if subfile.is_file():
                                    rel_subfile = subfile.relative_to(current_path)
                                    backup_subfile = backup_dir / backup_file.rstrip('/') / rel_subfile
                                    
                                    if backup_subfile.exists():
                                        try:
                                            current_content = subfile.read_text(encoding='utf-8', errors='replace')
                                            backup_content = backup_subfile.read_text(encoding='utf-8', errors='replace')
                                            
                                            if current_content == backup_content:
                                                tree.insert("", "end", values=("Same", f"{current_file}{rel_subfile}", get_file_category(str(rel_subfile)), "No changes"))
                                            else:
                                                summary = self._generate_relicheim_diff_summary(current_content, backup_content)
                                                tree.insert("", "end", values=("Modified", f"{current_file}{rel_subfile}", get_file_category(str(rel_subfile)), summary))
                                            
                                            used_backup_files.add(str(backup_subfile.relative_to(backup_dir)))
                                        except Exception as e:
                                            tree.insert("", "end", values=("Error", f"{current_file}{rel_subfile}", get_file_category(str(rel_subfile)), f"Error: {e}"))
                                    else:
                                        tree.insert("", "end", values=("New", f"{current_file}{rel_subfile}", get_file_category(str(rel_subfile)), "No backup file found"))
                        continue
                    
                    # Handle regular file mappings
                    if not current_path.exists():
                        continue
                    
                    if not backup_path.exists():
                        # Backup file doesn't exist, mark as new
                        tree.insert("", "end", values=("New", current_file, get_file_category(current_file), "No backup file found"))
                        continue
                    
                    # Compare files
                    try:
                        current_content = current_path.read_text(encoding='utf-8', errors='replace')
                        backup_content = backup_path.read_text(encoding='utf-8', errors='replace')
                        
                        if current_content == backup_content:
                            # Files are identical
                            tree.insert("", "end", values=("Same", current_file, get_file_category(current_file), "No changes"))
                        else:
                            # Files differ, generate summary
                            summary = self._generate_relicheim_diff_summary(current_content, backup_content)
                            tree.insert("", "end", values=("Modified", current_file, get_file_category(current_file), summary))
                        
                        used_backup_files.add(backup_file)
                    except Exception as e:
                        tree.insert("", "end", values=("Error", current_file, get_file_category(current_file), f"Error: {e}"))
                
                # Now scan ALL config files in current directory and subdirectories for RelicHeim-related files
                current_config_files = set()
                relicheim_related_files = []
                
                for config_file in self.config_root.rglob("*"):
                    if config_file.is_file() and config_file.suffix in ['.cfg', '.yml', '.yaml', '.json', '.txt']:
                        # Get relative path from config root
                        rel_path = config_file.relative_to(self.config_root)
                        current_config_files.add(str(rel_path))
                        
                        # Check if this looks like a RelicHeim-related file
                        filename_lower = str(rel_path).lower()
                        if any(keyword in filename_lower for keyword in [
                            'wacky', 'randyknapp', 'drop_that', 'custom_raids', 
                            'org.bepinex', 'creatureconfig', 'backpacks', 
                            'itemconfig', 'advize', 'kg.', 'randomsteve', 
                            'azumatt', 'horemvore', 'flueno', 'spawn_that',
                            'shudnal', 'blacks7ar', 'odinplus', 'com.maxsch',
                            'com.odinplus', 'com.bepis', 'nex', 'marcopogo',
                            'marlthon', 'htd', 'goldenrevolver', 'vapok',
                            'southsil', 'redseiko', 'zen', 'epicmmo', 'valheimench',
                            'wackysdatabase', 'epicloot', 'warpalicious', 'southsil',
                            'server_devcommands', 'redseiko', 'marcopogo', 'marlthon',
                            'goldenrevolver', 'flueno', 'com.maxsch', 'com.odinplus',
                            'com.bepis', 'blacks7ar', 'zendragon', 'binds', 'upgrade_world'
                        ]):
                            relicheim_related_files.append(str(rel_path))
                
                # Check for unmapped RelicHeim-related files
                mapped_current_files = set(relicheim_mapping.keys())
                unmapped_relicheim_files = [f for f in relicheim_related_files if f not in mapped_current_files]
                
                if unmapped_relicheim_files:
                    # Group by likely mod/plugin
                    grouped_unmapped = {}
                    for file in unmapped_relicheim_files:
                        if file.startswith('org.bepinex.plugins.'):
                            mod = 'org.bepinex.plugins'
                        elif file.startswith('warpalicious.'):
                            mod = 'warpalicious'
                        elif file.startswith('shudnal.'):
                            mod = 'shudnal'
                        elif file.startswith('blacks7ar.'):
                            mod = 'blacks7ar'
                        elif file.startswith('odinplus.'):
                            mod = 'odinplus'
                        elif file.startswith('com.'):
                            mod = 'com'
                        elif file.startswith('vapok.'):
                            mod = 'vapok'
                        elif file.startswith('southsil.'):
                            mod = 'southsil'
                        elif file.startswith('redseiko.'):
                            mod = 'redseiko'
                        elif file.startswith('nex.'):
                            mod = 'nex'
                        elif file.startswith('marcopogo.'):
                            mod = 'marcopogo'
                        elif file.startswith('marlthon.'):
                            mod = 'marlthon'
                        elif file.startswith('htd.'):
                            mod = 'htd'
                        elif file.startswith('goldenrevolver.'):
                            mod = 'goldenrevolver'
                        elif file.startswith('flueno.'):
                            mod = 'flueno'
                        elif file.startswith('ZenDragon.'):
                            mod = 'zendragon'
                        elif file.startswith('WackyMole.'):
                            mod = 'wackymole'
                        elif file.startswith('server_devcommands'):
                            mod = 'server'
                        elif file.startswith('binds'):
                            mod = 'system'
                        elif file.startswith('upgrade_world'):
                            mod = 'system'
                        else:
                            mod = 'other'
                        
                        if mod not in grouped_unmapped:
                            grouped_unmapped[mod] = []
                        grouped_unmapped[mod].append(file)
                    
                    # Add info about unmapped files
                    for mod, files in grouped_unmapped.items():
                        if len(files) > 0:
                            file_list = ", ".join(sorted(files)[:3])  # Show first 3
                            if len(files) > 3:
                                file_list += f" and {len(files) - 3} more"
                            
                            tree.insert("", "end", values=("Info", f"Unmapped {mod} Files", "System", 
                                                          f"Found {len(files)} {mod} files not mapped: {file_list}"))
                
                # Check for backup files that aren't being used (including subdirectories)
                all_backup_files = set()
                for backup_file in backup_dir.rglob("*"):
                    if backup_file.is_file():
                        # Get relative path from backup_dir
                        rel_path = backup_file.relative_to(backup_dir)
                        all_backup_files.add(str(rel_path))
                
                unused_backup_files = all_backup_files - used_backup_files
                if unused_backup_files:
                    # Add a note about unused backup files
                    unused_list = ", ".join(sorted(unused_backup_files)[:5])  # Show first 5
                    if len(unused_backup_files) > 5:
                        unused_list += f" and {len(unused_backup_files) - 5} more"
                    
                    tree.insert("", "end", values=("Info", "Unused Backup Files", "System", 
                                                  f"Found {len(unused_backup_files)} backup files not mapped: {unused_list}"))
                
                # Add summary statistics
                total_mapped = len([item for item in tree.get_children() if tree.item(item)['values'][0] in ['Same', 'Modified', 'New', 'Error']])
                total_unmapped = len([item for item in tree.get_children() if tree.item(item)['values'][0] == 'Info' and 'Unmapped' in tree.item(item)['values'][1]])
                
                if total_mapped > 0 or total_unmapped > 0:
                    tree.insert("", "end", values=("Summary", "Total Files Checked", "System", 
                                                  f"Mapped: {total_mapped}, Unmapped RelicHeim: {total_unmapped}"))

            def export_to_markdown():
                """Export the comparison results to a markdown file."""
                try:
                    # Get file save location
                    from tkinter import filedialog
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    default_filename = f"RelicHeim_Changes_{timestamp}.md"
                    
                    file_path = filedialog.asksaveasfilename(
                        title="Export RelicHeim Changes",
                        defaultextension=".md",
                        filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
                        initialvalue=default_filename
                    )
                    
                    if not file_path:
                        return
                    
                    # Collect all items from the tree
                    items = []
                    for item_id in tree.get_children():
                        values = tree.item(item_id)['values']
                        if len(values) >= 4:
                            status, filename, category, summary = values
                            items.append((status, filename, category, summary))
                    
                    # Group by category
                    categories = {}
                    for status, filename, category, summary in items:
                        if category not in categories:
                            categories[category] = []
                        categories[category].append((status, filename, summary))
                    
                    # Generate markdown content
                    md_content = f"""# RelicHeim Configuration Changes Report

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

This report shows all changes made to configuration files compared to the base RelicHeim installation.

## Summary

"""
                    
                    # Add summary statistics
                    total_files = len(items)
                    modified_files = sum(1 for status, _, _, _ in items if status == "Modified")
                    new_files = sum(1 for status, _, _, _ in items if status == "New")
                    same_files = sum(1 for status, _, _, _ in items if status == "Same")
                    error_files = sum(1 for status, _, _, _ in items if status == "Error")
                    
                    md_content += f"""
- **Total Files**: {total_files}
- **Modified**: {modified_files}
- **New**: {new_files}
- **Unchanged**: {same_files}
- **Errors**: {error_files}

## Changes by Category

"""
                    
                    # Add detailed breakdown by category
                    for category in sorted(categories.keys()):
                        md_content += f"### {category}\n\n"
                        md_content += "| Status | File | Summary |\n"
                        md_content += "|--------|------|--------|\n"
                        
                        for status, filename, summary in categories[category]:
                            # Escape pipe characters in summary
                            safe_summary = summary.replace("|", "\\|") if summary else ""
                            md_content += f"| {status} | `{filename}` | {safe_summary} |\n"
                        
                        md_content += "\n"
                    
                    # Add detailed file list
                    md_content += "## Complete File List\n\n"
                    md_content += "| Status | Category | File | Summary |\n"
                    md_content += "|--------|----------|------|--------|\n"
                    
                    for status, filename, category, summary in sorted(items, key=lambda x: (x[2], x[1])):
                        safe_summary = summary.replace("|", "\\|") if summary else ""
                        md_content += f"| {status} | {category} | `{filename}` | {safe_summary} |\n"
                    
                    # Add footer
                    md_content += f"""

---

*Report generated by Config Change Tracker*
*Base RelicHeim version: 5.4.10*
"""
                    
                    # Write to file
                    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(md_content)
                    
                    # Show success message
                    messagebox.showinfo("Export Complete", 
                                      f"RelicHeim changes exported to:\n{file_path}\n\n"
                                      f"Total files: {total_files}\n"
                                      f"Modified: {modified_files}\n"
                                      f"New: {new_files}")
                    
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export: {e}")

            def on_tree_right_click(event):
                """Handle right-click on tree items."""
                try:
                    rowid = tree.identify_row(event.y)
                    if rowid:
                        tree.selection_set(rowid)
                        item = tree.item(rowid)
                        file_path = item['values'][1]
                        
                        # Open file in editor
                        self.open_file_in_editor(file_path)
                except Exception as e:
                    self._set_status(f"Error opening file: {e}")

            def on_tree_double_click(event):
                """Handle double-click on tree items."""
                try:
                    rowid = tree.identify_row(event.y)
                    if rowid:
                        item = tree.item(rowid)
                        file_path = item['values'][1]
                        
                        # Open file in editor
                        self.open_file_in_editor(file_path)
                except Exception as e:
                    self._set_status(f"Error opening file: {e}")

            # Bind events
            tree.bind("<Button-3>", on_tree_right_click)
            tree.bind("<Double-1>", on_tree_double_click)

            # Populate the tree
            compare_files()

        except Exception as e:
            self._set_status(f"Error showing RelicHeim comparison: {e}")

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

    def _set_busy(self, is_busy: bool, text: str | None = None) -> None:
        """Toggle busy UI state with optional status text."""
        try:
            if text is not None:
                self._set_status(text)
            # Busy cursor for whole window
            try:
                self.root.configure(cursor="watch" if is_busy else "")
            except Exception:
                pass
            # Start/stop progress animation
            if is_busy:
                try:
                    self.progress.start(60)
                except Exception:
                    pass
                # Disable main actions to avoid re-entry
                try:
                    self.btn_refresh.state(["disabled"])  # may not exist in some flows yet
                except Exception:
                    pass
            else:
                try:
                    self.progress.stop()
                except Exception:
                    pass
                try:
                    self.btn_refresh.state(["!disabled"])  # re-enable
                except Exception:
                    pass
            # Ensure redraw
            try:
                self.root.update_idletasks()
            except Exception:
                pass
        except Exception:
            # Fallback to plain status
            if text is not None:
                self._set_status(text)


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
