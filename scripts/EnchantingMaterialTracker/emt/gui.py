
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading, os, sys
from .config import load_settings
from .snapshot import take_snapshot
from .compare import compare_snapshots

class EMTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enchanting Material Tracker")
        self.geometry("980x540")
        self.minsize(800, 600)
        
        # Apply dark theme colors matching valheim_config_suite_v2
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        
        # Color scheme matching valheim_config_suite_v2
        self.colors = {
            "bg": "#152616",
            "panel": "#414535", 
            "text": "#b07b53",
            "muted": "#654735",
            "accent": "#5f633e",
            "accent2": "#654735"
        }
        
        self.configure(bg=self.colors["bg"])
        
        # Configure styles for all widgets
        import tkinter.font as tkfont
        base_font = tkfont.Font(family="Consolas" if sys.platform.startswith("win") else "Courier New", size=10)
        
        for nm in ("TLabel", "TButton", "Treeview", "Treeview.Heading", "TEntry", "TCombobox", "TFrame", "TLabelframe"):
            self.style.configure(nm, background=self.colors["panel"], foreground=self.colors["text"], font=base_font)
        
        self.style.configure("Treeview", fieldbackground=self.colors["panel"])
        self.style.configure("Accent.TButton", background=self.colors["accent"], foreground="#152616")
        self.style.map("Accent.TButton", background=[("active", self.colors["accent2"])])
        
        self.settings = load_settings()
        
        # Create menu bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Data", command=self._export)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Tools menu
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Scan & Compare", command=self._scan_compare)
        tools_menu.add_command(label="Take Snapshot", command=self._take_snapshot)
        tools_menu.add_separator()
        tools_menu.add_command(label="Refresh Data", command=self._scan_compare)
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)
        
        frm = ttk.Frame(self, padding=10); frm.pack(fill="both", expand=True)
        path_frame = ttk.LabelFrame(frm, text="Paths"); path_frame.pack(fill="x", pady=8)
        self.active_var = tk.StringVar(value=self.settings.get("active_config_dir",""))
        self.base_var = tk.StringVar(value=self.settings.get("baseline_backup_dir",""))
        ttk.Label(path_frame, text="Active Config Dir:").grid(row=0, column=0, sticky="w")
        ttk.Entry(path_frame, textvariable=self.active_var, width=80).grid(row=0, column=1, padx=6, pady=4)
        ttk.Button(path_frame, text="Browse", command=self._browse_active).grid(row=0, column=2)
        ttk.Label(path_frame, text="Baseline Backup Dir:").grid(row=1, column=0, sticky="w")
        ttk.Entry(path_frame, textvariable=self.base_var, width=80).grid(row=1, column=1, padx=6, pady=4)
        ttk.Button(path_frame, text="Browse", command=self._browse_base).grid(row=1, column=2)
        
        # Main action buttons
        btns = ttk.Frame(frm); btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="🔄 Scan & Compare", style="Accent.TButton", command=self._scan_compare).pack(side="left", padx=2)
        ttk.Button(btns, text="📊 Export Data", command=self._export).pack(side="left", padx=2)
        ttk.Button(btns, text="📸 Take Snapshot", command=self._take_snapshot).pack(side="left", padx=2)
        ttk.Button(btns, text="❓ Help", command=self._show_help).pack(side="left", padx=2)
        
        # Add a separator
        ttk.Separator(frm, orient='horizontal').pack(fill='x', pady=4)
        
        # Create frame for treeview and scrollbar
        tree_frame = ttk.Frame(frm)
        tree_frame.pack(fill="both", expand=True)
        
        cols = ("material","total_base","total_current","pct_change_total")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="extended")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140 if c!="material" else 220, anchor="center")
        
        # Add scrollbars
        tree_scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        tree_scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar_y.pack(side="right", fill="y")
        tree_scrollbar_x.pack(side="bottom", fill="x")
        
        # Add right-click context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy Material Name", command=self._copy_material_name)
        self.context_menu.add_command(label="Copy Row Data", command=self._copy_row_data)
        self.context_menu.add_command(label="Copy Selected Rows", command=self._copy_selected_rows)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Refresh Data", command=self._scan_compare)
        
        self.tree.bind("<Button-3>", self._show_context_menu)  # Right-click
        self.tree.bind("<Double-Button-1>", self._copy_material_name)  # Double-click
        
        # Add keyboard shortcuts
        self.bind("<Control-c>", lambda e: self._copy_selected_rows())
        self.bind("<Control-r>", lambda e: self._scan_compare())
        self.bind("<F5>", lambda e: self._scan_compare())
        
        self.status = tk.StringVar(value="Initializing...")
        ttk.Label(frm, textvariable=self.status, foreground=self.colors["muted"]).pack(side="bottom", anchor="w")
        self._results = []
        
        # Auto-sync data when GUI launches
        self.after(100, self._auto_sync)
    
    def _auto_sync(self):
        """Automatically sync data when GUI launches"""
        self.status.set("Auto-syncing data...")
        def work():
            try:
                settings = self.settings
                settings["active_config_dir"] = self.active_var.get()
                settings["baseline_backup_dir"] = self.base_var.get()
                base_id = take_snapshot(settings["baseline_backup_dir"], settings)
                act_id = take_snapshot(settings["active_config_dir"], settings)
                from .compare import compare_snapshots
                self._results = compare_snapshots(settings["db_path"], base_id, act_id)
                self._render_results(self._results)
                self.status.set("Ready. Data synced automatically.")
            except Exception as e:
                self.status.set(f"Auto-sync failed: {str(e)}")
        threading.Thread(target=work, daemon=True).start()
    
    def _browse_active(self):
        p = filedialog.askdirectory()
        if p: self.active_var.set(p)
    def _browse_base(self):
        p = filedialog.askdirectory()
        if p: self.base_var.set(p)
    def _scan_compare(self):
        self.status.set("Scanning..."); self.tree.delete(*self.tree.get_children())
        def work():
            try:
                settings = self.settings
                settings["active_config_dir"] = self.active_var.get()
                settings["baseline_backup_dir"] = self.base_var.get()
                base_id = take_snapshot(settings["baseline_backup_dir"], settings)
                act_id = take_snapshot(settings["active_config_dir"], settings)
                from .compare import compare_snapshots
                self._results = compare_snapshots(settings["db_path"], base_id, act_id)
                self._render_results(self._results); self.status.set("Done.")
            except Exception as e:
                self.status.set(f"Error: {str(e)}")
        threading.Thread(target=work, daemon=True).start()
    
    def _render_results(self, results):
        # Custom sorting order for materials
        material_order = [
            "RunestoneMagic",
            "RunestoneRare", 
            "RunestoneEpic",
            "RunestoneLegendary"
        ]
        
        # Create a mapping for custom sorting
        def get_material_sort_key(material):
            try:
                return material_order.index(material)
            except ValueError:
                return len(material_order) + len(material)  # Put unknown materials at the end
        
        # Sort results by custom order
        sorted_results = sorted(results, key=lambda x: get_material_sort_key(x["material"]))
        
        for r in sorted_results:
            pct = f"{r['pct_change_total']:.2f}%"
            self.tree.insert("", "end", values=(r["material"], f"{r['total_base']:.4f}", f"{r['total_current']:.4f}", pct))
    
    def _export(self):
        if not self._results:
            messagebox.showinfo("Export", "No results to export yet."); return
        outdir = os.path.join(os.path.dirname(self.settings["db_path"]), "exports")
        from .export import export_json, export_csv, export_md
        p_json = export_json(self._results, outdir); p_csv = export_csv(self._results, outdir); p_md = export_md(self._results, outdir)
        messagebox.showinfo("Export", f"Exported:\n{p_json}\n{p_csv}\n{p_md}")
    
    def _take_snapshot(self):
        """Take a snapshot of the active config directory"""
        self.status.set("Taking snapshot...")
        def work():
            try:
                settings = self.settings
                settings["active_config_dir"] = self.active_var.get()
                snap_id = take_snapshot(settings["active_config_dir"], settings)
                self.status.set(f"Snapshot {snap_id} created successfully.")
                messagebox.showinfo("Snapshot", f"Snapshot {snap_id} created for {settings['active_config_dir']}")
            except Exception as e:
                self.status.set(f"Snapshot failed: {str(e)}")
                messagebox.showerror("Error", f"Failed to take snapshot: {str(e)}")
        threading.Thread(target=work, daemon=True).start()
    
    def _show_help(self):
        """Show help information"""
        help_text = """Enchanting Material Tracker

This tool compares active enchanting-material configurations vs a baseline RelicHeim backup.

Features:
• 🔄 Scan & Compare: Takes snapshots and compares baseline vs active configurations
• 📊 Export Data: Exports results to JSON, CSV, and Markdown formats
• 📸 Take Snapshot: Creates a snapshot of the active config directory
• ❓ Help: Shows this help information

Keyboard Shortcuts:
• Ctrl+C: Copy selected rows to clipboard
• Ctrl+R or F5: Refresh data
• Double-click: Copy material name to clipboard

Multi-selection:
• Click and drag to select multiple rows
• Ctrl+click to select individual rows
• Shift+click to select ranges

The program automatically syncs data when launched and displays:
• Material names (sorted in custom order: Magic, Rare, Epic, Legendary)
• Baseline availability scores
• Current availability scores  
• Percentage changes

Paths can be configured in settings.json or changed via the Browse buttons.

For more information, see the README.md file."""
        
        help_window = tk.Toplevel(self)
        help_window.title("Help - Enchanting Material Tracker")
        help_window.geometry("600x500")
        help_window.resizable(True, True)
        
        # Create a text widget with scrollbar
        text_frame = ttk.Frame(help_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap="word", padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")  # Make read-only
        
        # Add a close button
        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)
    
    def _show_context_menu(self, event):
        """Show context menu on right-click"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def _copy_material_name(self):
        """Copy selected material name to clipboard"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            material_name = item['values'][0]
            self.clipboard_clear()
            self.clipboard_append(material_name)
            self.status.set(f"Copied '{material_name}' to clipboard")
    
    def _copy_row_data(self):
        """Copy selected row data to clipboard"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            row_data = f"Material: {values[0]}, Baseline: {values[1]}, Current: {values[2]}, Change: {values[3]}"
            self.clipboard_clear()
            self.clipboard_append(row_data)
            self.status.set("Copied row data to clipboard")
    
    def _copy_selected_rows(self):
        """Copy all selected rows to clipboard"""
        selection = self.tree.selection()
        if not selection:
            self.status.set("No rows selected")
            return
        
        clipboard_text = []
        for item_id in selection:
            item = self.tree.item(item_id)
            values = item['values']
            row_data = f"Material: {values[0]}, Baseline: {values[1]}, Current: {values[2]}, Change: {values[3]}"
            clipboard_text.append(row_data)
        
        final_text = "\n".join(clipboard_text)
        self.clipboard_clear()
        self.clipboard_append(final_text)
        self.status.set(f"Copied {len(selection)} selected rows to clipboard")
    
    def _show_about(self):
        """Show about information"""
        about_text = """Enchanting Material Tracker v1.0

A tool for tracking and comparing enchanting material availability
in Valheim mod configurations.

Features:
• Compare baseline vs active configurations
• Export data in multiple formats
• Take snapshots of config directories
• GUI and command-line interfaces
• Multi-row selection and copying
• Custom material sorting order

For help and documentation, see the Help menu."""
        
        messagebox.showinfo("About - Enchanting Material Tracker", about_text)

def main(): EMTApp().mainloop()
if __name__ == "__main__": main()
