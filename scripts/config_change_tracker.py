import os
import sys
import json
import shutil
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from difflib import unified_diff

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkfont


class ConfigSnapshot:
    def __init__(self, config_root: Path):
        self.config_root = config_root
        # Store snapshots in the scripts directory
        scripts_dir = Path(__file__).parent
        self.snapshots_dir = scripts_dir / "snapshots"
        self.current_snapshot_file = self.snapshots_dir / "current_snapshot.json"
        self.initial_snapshot_file = self.snapshots_dir / "initial_snapshot.json"
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
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2, ensure_ascii=False)
            
            snapshot_type = "initial" if is_initial else "current"
            return True, f"{snapshot_type.capitalize()} snapshot created with {len(snapshot['files'])} files"
        except Exception as e:
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
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Action.TButton", 
                       background=self.colors["highlight"], 
                       foreground=self.colors["text"], 
                       padding=6)
        style.map("Action.TButton", 
                 background=[("active", self.colors["accent"])])
        style.configure("Treeview", 
                       background=self.colors["panel"], 
                       fieldbackground=self.colors["panel"], 
                       foreground=self.colors["text"])
        style.configure("Treeview.Heading", 
                       background=self.colors["highlight"], 
                       foreground=self.colors["text"])
        
        # Menu bar
        menubar = tk.Menu(self.root, tearoff=False)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Create Current Snapshot", command=self.create_snapshot)
        file_menu.add_command(label="Create Initial Snapshot", command=self.create_initial_snapshot)
        file_menu.add_command(label="Refresh Changes", command=self.refresh_changes)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=False)
        view_menu.add_command(label="Zoom In (Ctrl +)", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out (Ctrl -)", command=self.zoom_out)
        view_menu.add_command(label="Reset Zoom (Ctrl 0)", command=self.reset_zoom)
        menubar.add_cascade(label="View", menu=view_menu)
        
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
        
        self.btn_snapshot = ttk.Button(controls_frame, text="Create Snapshot", 
                                       style="Action.TButton", command=self.create_snapshot)
        self.btn_snapshot.pack(side=tk.LEFT, padx=(0, 6))
        
        self.btn_initial = ttk.Button(controls_frame, text="Set Initial", 
                                     style="Action.TButton", command=self.create_initial_snapshot)
        self.btn_initial.pack(side=tk.LEFT, padx=(0, 6))
        
        self.btn_refresh = ttk.Button(controls_frame, text="Refresh", 
                                     style="Action.TButton", command=self.refresh_changes)
        self.btn_refresh.pack(side=tk.LEFT, padx=(0, 6))
        
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
        compare_label = tk.Label(filter_frame, text="Compare Against:", 
                                bg=self.colors["bg"], fg=self.colors["text"])
        compare_label.pack(anchor="w")
        
        self.compare_var = tk.StringVar(value="Current Session")
        self.compare_combo = ttk.Combobox(filter_frame, textvariable=self.compare_var, 
                                         state="readonly", width=30)
        self.compare_combo['values'] = ["Current Session", "Initial State"]
        self.compare_combo.pack(fill=tk.X, pady=(3, 6))
        self.compare_combo.bind("<<ComboboxSelected>>", self.on_compare_change)
        
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
        
        changes_label = tk.Label(changes_frame, text="Changed Files (Most Recent First):", 
                                bg=self.colors["bg"], fg=self.colors["text"])
        changes_label.pack(anchor="w")
        
        # Create Treeview for changes
        self.changes_tree = ttk.Treeview(changes_frame, columns=("status", "file", "mod", "time", "session"), 
                                        show="headings", height=20)
        self.changes_tree.heading("status", text="Status")
        self.changes_tree.heading("file", text="File")
        self.changes_tree.heading("mod", text="Mod")
        self.changes_tree.heading("time", text="Modified")
        self.changes_tree.heading("session", text="Session")
        
        self.changes_tree.column("status", width=60)
        self.changes_tree.column("file", width=180)
        self.changes_tree.column("mod", width=100)
        self.changes_tree.column("time", width=100)
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
        self.diff_text.configure(font=self.font)
    
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
                    self.root.after(0, lambda: self._set_status(msg))
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
                self.root.after(0, lambda: self._set_status("Creating initial snapshot..."))
                ok, msg = self.snapshot.create_snapshot(is_initial=True)
                
                # Update UI in main thread
                if ok:
                    self.root.after(0, lambda: self._set_status(msg))
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
                compare_against = "initial" if self.compare_var.get() == "Initial State" else "current"
                changes = self.snapshot.get_changes(compare_against)
                
                # Update mod filter options
                mods = {"All Mods"} | {mod for _, _, mod, _ in changes}
                
                # Filter changes based on current selection
                selected_mod = self.mod_filter_var.get()
                if selected_mod != "All Mods":
                    changes = [(status, file_path, mod, session) for status, file_path, mod, session in changes if mod == selected_mod]
                
                # Sort by modification time (most recent first)
                changes_with_time = []
                for status, file_path, mod, session in changes:
                    try:
                        file_obj = self.config_root / file_path
                        if file_obj.exists():
                            mtime = file_obj.stat().st_mtime
                            time_str = datetime.fromtimestamp(mtime).strftime("%m/%d %H:%M")
                        else:
                            time_str = "Deleted"
                    except Exception:
                        time_str = "Unknown"
                    
                    changes_with_time.append((status, file_path, mod, time_str, session))
                
                changes_with_time.sort(key=lambda x: x[3], reverse=True)
                
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
        for status, file_path, mod, time_str, session in changes:
            status_display = {
                'A': 'Added',
                'M': 'Modified',
                'D': 'Deleted'
            }.get(status, status)
            
            self.changes_tree.insert("", "end", values=(status_display, file_path, mod, time_str, session))
        
        self._set_status(f"Found {len(changes)} changed file(s)")
    
    def on_mod_filter_change(self, event=None) -> None:
        """Handle mod filter change."""
        self.refresh_changes()
    
    def on_compare_change(self, event=None) -> None:
        """Handle comparison type change."""
        self.refresh_changes()
    
    def on_change_select(self, event=None) -> None:
        """Handle change selection."""
        selection = self.changes_tree.selection()
        if not selection:
            return
        
        item = self.changes_tree.item(selection[0])
        file_path = item['values'][1]
        
        # Show diff in background thread
        def worker():
            try:
                # Determine comparison type
                compare_against = "initial" if self.compare_var.get() == "Initial State" else "current"
                diff = self.snapshot.get_diff(file_path, compare_against)
                self.root.after(0, lambda: self._show_diff(diff, file_path))
            except Exception as e:
                self.root.after(0, lambda: self._set_status(f"Error loading diff: {e}"))
        
        threading.Thread(target=worker, daemon=True).start()
    
    def _show_diff(self, diff: str, file_path: str) -> None:
        """Display diff in the text widget."""
        self.diff_text.config(state=tk.NORMAL)
        self.diff_text.delete("1.0", tk.END)
        
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
