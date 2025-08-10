import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import yaml
from PIL import Image, ImageTk
import threading
import webbrowser
from pathlib import Path
import re

class ValheimModManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Valheim Mod Manager")
        self.root.geometry("1200x800")
        
        # Paths
        self.valheim_path = Path("Valheim")
        self.cache_path = self.valheim_path / "cache"
        self.profiles_path = self.valheim_path / "profiles"
        self.config_path = self.profiles_path / "Dogeheim_Player" / "BepInEx" / "config"
        
        # Data storage
        self.mods_data = {}
        self.filtered_mods = []
        self.mod_icons = {}
        self.categories = {
            "🛡️ Armor & Equipment": ["armor", "equipment", "clothing"],
            "⚔️ Weapons & Combat": ["weapon", "combat", "warfare"],
            "🧙‍♂️ Magic & Spells": ["magic", "spell", "wizardry"],
            "🎒 Loot & Progression": ["loot", "progression", "backpack", "relic"],
            "🍖 Food & Consumables": ["food", "cooking", "potion", "consumable"],
            "🌱 Farming & Agriculture": ["farming", "agriculture", "plant", "ranching"],
            "🏰 Building & Locations": ["building", "location", "architect", "scenic"],
            "⛵ Naval & Ships": ["ship", "sailing", "naval"],
            "🌍 Environmental & Seasons": ["environment", "season", "weather"],
            "🐉 Monsters & Bosses": ["monster", "boss", "creature"],
            "🎮 Gameplay & Systems": ["gameplay", "system", "skill", "mmo"],
            "🗑️ Quality of Life": ["qol", "quality", "utility"],
            "🔧 Framework & Utilities": ["framework", "utility", "bepinex", "jotunn"]
        }
        
        self.setup_ui()
        self.load_mods_data()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search and filter controls
        search_frame = ttk.LabelFrame(control_frame, text="Search & Filter")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search entry
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_mods)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Category filter
        ttk.Label(search_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_var.set("All Categories")
        category_combo = ttk.Combobox(search_frame, textvariable=self.category_var, 
                                     values=["All Categories"] + list(self.categories.keys()),
                                     state="readonly", width=25)
        category_combo.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        category_combo.bind('<<ComboboxSelected>>', self.filter_mods)
        
        # Status filter
        ttk.Label(search_frame, text="Status:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.status_var = tk.StringVar()
        self.status_var.set("All")
        status_combo = ttk.Combobox(search_frame, textvariable=self.status_var,
                                   values=["All", "Active", "Inactive"], state="readonly", width=15)
        status_combo.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        status_combo.bind('<<ComboboxSelected>>', self.filter_mods)
        
        # Refresh button
        refresh_btn = ttk.Button(search_frame, text="🔄 Refresh", command=self.refresh_data)
        refresh_btn.grid(row=0, column=6, padx=5, pady=5)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Mod list
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Mod list with scrollbar
        list_frame = ttk.LabelFrame(left_frame, text="Mods")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for mod list
        columns = ("Name", "Version", "Status")
        self.mod_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=20)
        
        # Configure columns
        self.mod_tree.heading("#0", text="Icon")
        self.mod_tree.column("#0", width=50, minwidth=50)
        self.mod_tree.heading("Name", text="Mod Name")
        self.mod_tree.column("Name", width=200, minwidth=150)
        self.mod_tree.heading("Version", text="Version")
        self.mod_tree.column("Version", width=80, minwidth=80)
        self.mod_tree.heading("Status", text="Status")
        self.mod_tree.column("Status", width=80, minwidth=80)
        
        # Scrollbar for mod list
        mod_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.mod_tree.yview)
        self.mod_tree.configure(yscrollcommand=mod_scrollbar.set)
        
        self.mod_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mod_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.mod_tree.bind('<<TreeviewSelect>>', self.on_mod_select)
        
        # Right panel - Mod details
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Mod details frame
        details_frame = ttk.LabelFrame(right_frame, text="Mod Details")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mod icon
        self.icon_label = ttk.Label(details_frame, text="No mod selected")
        self.icon_label.pack(pady=10)
        
        # Mod info text
        info_frame = ttk.Frame(details_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Mod name
        self.mod_name_label = ttk.Label(info_frame, text="", font=("Arial", 12, "bold"))
        self.mod_name_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Mod version
        self.mod_version_label = ttk.Label(info_frame, text="")
        self.mod_version_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Mod description
        self.mod_desc_label = ttk.Label(info_frame, text="", wraplength=400)
        self.mod_desc_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Category
        self.mod_category_label = ttk.Label(info_frame, text="")
        self.mod_category_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Config files section
        config_frame = ttk.LabelFrame(details_frame, text="Configuration Files")
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Config files listbox
        self.config_listbox = tk.Listbox(config_frame, height=6)
        config_scrollbar = ttk.Scrollbar(config_frame, orient=tk.VERTICAL, command=self.config_listbox.yview)
        self.config_listbox.configure(yscrollcommand=config_scrollbar.set)
        
        self.config_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        config_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Config file buttons
        config_btn_frame = ttk.Frame(config_frame)
        config_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(config_btn_frame, text="Open Config", command=self.open_config_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(config_btn_frame, text="Open Folder", command=self.open_config_folder).pack(side=tk.LEFT, padx=2)
        
        # Action buttons
        action_frame = ttk.Frame(details_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Open Mod Folder", command=self.open_mod_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="View Readme", command=self.view_readme).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="Toggle Status", command=self.toggle_mod_status).pack(side=tk.LEFT, padx=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_mods_data(self):
        """Load mod data from cache and configuration"""
        self.status_var.set("Loading mod data...")
        self.root.update()
        
        # Load mod data from the summary file
        self.load_mods_from_summary()
        
        # Load mod icons
        self.load_mod_icons()
        
        # Load mod status from profiles
        self.load_mod_status()
        
        # Populate the tree
        self.populate_mod_tree()
        
        self.status_var.set(f"Loaded {len(self.mods_data)} mods")
        
    def load_mods_from_summary(self):
        """Load mod data from the Valheim_Content_Mods_Summary.md file"""
        summary_file = Path("Valheim_Content_Mods_Summary.md")
        if not summary_file.exists():
            messagebox.showerror("Error", "Valheim_Content_Mods_Summary.md not found!")
            return
            
        with open(summary_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the summary file to extract mod information
        # This is a simplified parser - you might want to enhance it
        lines = content.split('\n')
        current_mod = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('### **') and line.endswith('**'):
                # Extract mod name and version
                mod_info = line[4:-3]  # Remove ### ** and **
                if '(' in mod_info and ')' in mod_info:
                    mod_name = mod_info[:mod_info.rfind('(')].strip()
                    version = mod_info[mod_info.rfind('(')+1:mod_info.rfind(')')].strip()
                    
                    # Clean up mod name
                    if mod_name.startswith('[') and mod_name.endswith(']'):
                        mod_name = mod_name[1:-1]
                    
                    current_mod = {
                        'name': mod_name,
                        'version': version,
                        'description': '',
                        'category': self.categorize_mod(mod_name),
                        'config_files': [],
                        'status': 'Unknown'
                    }
                    self.mods_data[mod_name] = current_mod
                    
            elif current_mod and line.startswith('- **'):
                # Extract key features
                feature = line[4:].strip()
                if current_mod['description']:
                    current_mod['description'] += '; ' + feature
                else:
                    current_mod['description'] = feature
                    
        # Special handling for RelicHeim patches
        self.combine_relicheim_patches()
        
    def categorize_mod(self, mod_name):
        """Categorize a mod based on its name and description"""
        mod_name_lower = mod_name.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in mod_name_lower:
                    return category
                    
        return "🎮 Gameplay & Systems"  # Default category
        
    def combine_relicheim_patches(self):
        """Combine RelicHeim patches into a single mod entry"""
        relicheim_mods = []
        
        # Find all RelicHeim related mods
        for mod_name, mod_data in list(self.mods_data.items()):
            if 'relicheim' in mod_name.lower() or 'jewelheim' in mod_name.lower():
                relicheim_mods.append((mod_name, mod_data))
                
        if relicheim_mods:
            # Create combined entry
            combined_mod = {
                'name': 'JewelHeim-RelicHeim (Combined)',
                'version': '5.4.9',
                'description': 'Combined RelicHeim mod pack with all patches and components',
                'category': '🎒 Loot & Progression',
                'config_files': [],
                'status': 'Unknown',
                'patches': []
            }
            
            # Collect all patches
            for mod_name, mod_data in relicheim_mods:
                combined_mod['patches'].append(mod_name)
                if mod_data['config_files']:
                    combined_mod['config_files'].extend(mod_data['config_files'])
                    
            # Remove individual entries and add combined one
            for mod_name, _ in relicheim_mods:
                del self.mods_data[mod_name]
                
            self.mods_data['JewelHeim-RelicHeim (Combined)'] = combined_mod
            
    def load_mod_icons(self):
        """Load mod icons from cache directories"""
        if not self.cache_path.exists():
            return
            
        for mod_dir in self.cache_path.iterdir():
            if mod_dir.is_dir():
                # Find the latest version directory
                version_dirs = [d for d in mod_dir.iterdir() if d.is_dir()]
                if version_dirs:
                    latest_version = max(version_dirs, key=lambda x: x.name)
                    icon_path = latest_version / "icon.png"
                    
                    if icon_path.exists():
                        try:
                            # Load and resize icon
                            image = Image.open(icon_path)
                            image = image.resize((32, 32), Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(image)
                            self.mod_icons[mod_dir.name] = photo
                        except Exception as e:
                            print(f"Error loading icon for {mod_dir.name}: {e}")
                            
    def load_mod_status(self):
        """Load mod status from profiles"""
        if not self.config_path.exists():
            return
            
        # Check which mods have config files (indicating they're active)
        config_files = list(self.config_path.glob("*.cfg"))
        config_files.extend(list(self.config_path.glob("*.yml")))
        
        for mod_name, mod_data in self.mods_data.items():
            # Check if mod has config files
            has_config = False
            for config_file in config_files:
                if self.mod_has_config(mod_name, config_file.name):
                    has_config = True
                    mod_data['config_files'].append(str(config_file))
                    
            mod_data['status'] = 'Active' if has_config else 'Inactive'
            
    def mod_has_config(self, mod_name, config_filename):
        """Check if a mod has a specific config file"""
        mod_name_lower = mod_name.lower()
        config_lower = config_filename.lower()
        
        # Extract author and mod name from mod_name
        if '-' in mod_name:
            author, mod_part = mod_name.split('-', 1)
            author_lower = author.lower()
            mod_part_lower = mod_part.lower()
            
            # Check various patterns
            patterns = [
                f"{author_lower}.{mod_part_lower}",
                f"{mod_part_lower}",
                f"{author_lower}",
                mod_name_lower.replace('-', '.'),
                mod_name_lower.replace('-', '')
            ]
            
            for pattern in patterns:
                if pattern in config_lower:
                    return True
                    
        return mod_name_lower in config_lower
        
    def populate_mod_tree(self):
        """Populate the mod tree with loaded data"""
        # Clear existing items
        for item in self.mod_tree.get_children():
            self.mod_tree.delete(item)
            
        # Group mods by category
        categorized_mods = {}
        for mod_name, mod_data in self.mods_data.items():
            category = mod_data['category']
            if category not in categorized_mods:
                categorized_mods[category] = []
            categorized_mods[category].append((mod_name, mod_data))
            
        # Add categories and mods to tree
        for category, mods in categorized_mods.items():
            category_item = self.mod_tree.insert("", "end", text=category, values=("", "", ""))
            
            for mod_name, mod_data in mods:
                # Get icon
                icon = ""
                for cache_name, icon_photo in self.mod_icons.items():
                    if cache_name.lower() in mod_name.lower() or mod_name.lower() in cache_name.lower():
                        icon = "📦"  # Use emoji as placeholder for icon
                        break
                        
                self.mod_tree.insert(category_item, "end", text=icon, 
                                   values=(mod_data['name'], mod_data['version'], mod_data['status']))
                                   
        # Expand all categories
        for item in self.mod_tree.get_children():
            self.mod_tree.item(item, open=True)
            
    def filter_mods(self, event=None):
        """Filter mods based on search and category criteria"""
        search_term = self.search_var.get().lower()
        selected_category = self.category_var.get()
        selected_status = self.status_var.get()
        
        # Hide all items first
        for item in self.mod_tree.get_children():
            self.mod_tree.item(item, open=False)
            
        # Show matching items
        for category_item in self.mod_tree.get_children():
            category_text = self.mod_tree.item(category_item, "text")
            
            # Check category filter
            if selected_category != "All Categories" and category_text != selected_category:
                continue
                
            # Check mods in this category
            for mod_item in self.mod_tree.get_children(category_item):
                mod_values = self.mod_tree.item(mod_item, "values")
                mod_name = mod_values[0].lower()
                mod_status = mod_values[2]
                
                # Check search filter
                if search_term and search_term not in mod_name:
                    continue
                    
                # Check status filter
                if selected_status != "All" and mod_status != selected_status:
                    continue
                    
                # Show this mod
                self.mod_tree.item(mod_item, tags=("visible",))
                
            # Show category if it has visible mods
            visible_mods = [mod for mod in self.mod_tree.get_children(category_item) 
                          if "visible" in self.mod_tree.item(mod, "tags")]
            if visible_mods:
                self.mod_tree.item(category_item, open=True)
                
    def on_mod_select(self, event):
        """Handle mod selection"""
        selection = self.mod_tree.selection()
        if not selection:
            return
            
        selected_item = selection[0]
        parent = self.mod_tree.parent(selected_item)
        
        # Only handle mod items, not category items
        if parent:
            mod_name = self.mod_tree.item(selected_item, "values")[0]
            self.show_mod_details(mod_name)
            
    def show_mod_details(self, mod_name):
        """Show details for the selected mod"""
        if mod_name not in self.mods_data:
            return
            
        mod_data = self.mods_data[mod_name]
        
        # Update mod info
        self.mod_name_label.config(text=mod_data['name'])
        self.mod_version_label.config(text=f"Version: {mod_data['version']}")
        self.mod_desc_label.config(text=mod_data['description'])
        self.mod_category_label.config(text=f"Category: {mod_data['category']}")
        
        # Update icon
        icon_found = False
        for cache_name, icon_photo in self.mod_icons.items():
            if cache_name.lower() in mod_name.lower() or mod_name.lower() in cache_name.lower():
                self.icon_label.config(image=icon_photo, text="")
                icon_found = True
                break
                
        if not icon_found:
            self.icon_label.config(image="", text="📦")
            
        # Update config files list
        self.config_listbox.delete(0, tk.END)
        for config_file in mod_data['config_files']:
            self.config_listbox.insert(tk.END, os.path.basename(config_file))
            
        # Show patches if this is a combined mod
        if 'patches' in mod_data:
            self.config_listbox.insert(tk.END, "")
            self.config_listbox.insert(tk.END, "--- Patches ---")
            for patch in mod_data['patches']:
                self.config_listbox.insert(tk.END, f"  {patch}")
                
    def open_config_file(self):
        """Open the selected config file"""
        selection = self.config_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a config file first")
            return
            
        config_filename = self.config_listbox.get(selection[0])
        if config_filename.startswith("  ") or config_filename == "--- Patches ---" or config_filename == "":
            return
            
        config_path = self.config_path / config_filename
        if config_path.exists():
            try:
                os.startfile(str(config_path))
            except Exception as e:
                messagebox.showerror("Error", f"Could not open config file: {e}")
        else:
            messagebox.showerror("Error", f"Config file not found: {config_path}")
            
    def open_config_folder(self):
        """Open the config folder"""
        if self.config_path.exists():
            try:
                os.startfile(str(self.config_path))
            except Exception as e:
                messagebox.showerror("Error", f"Could not open config folder: {e}")
        else:
            messagebox.showerror("Error", "Config folder not found")
            
    def open_mod_folder(self):
        """Open the mod's cache folder"""
        selection = self.mod_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a mod first")
            return
            
        selected_item = selection[0]
        parent = self.mod_tree.parent(selected_item)
        
        if not parent:
            return
            
        mod_name = self.mod_tree.item(selected_item, "values")[0]
        
        # Find mod folder in cache
        for cache_dir in self.cache_path.iterdir():
            if cache_dir.is_dir():
                if cache_dir.name.lower() in mod_name.lower() or mod_name.lower() in cache_dir.name.lower():
                    try:
                        os.startfile(str(cache_dir))
                        return
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not open mod folder: {e}")
                        return
                        
        messagebox.showerror("Error", f"Mod folder not found for {mod_name}")
        
    def view_readme(self):
        """View the mod's README file"""
        selection = self.mod_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a mod first")
            return
            
        selected_item = selection[0]
        parent = self.mod_tree.parent(selected_item)
        
        if not parent:
            return
            
        mod_name = self.mod_tree.item(selected_item, "values")[0]
        
        # Find README in cache
        for cache_dir in self.cache_path.iterdir():
            if cache_dir.is_dir():
                if cache_dir.name.lower() in mod_name.lower() or mod_name.lower() in cache_dir.name.lower():
                    # Find latest version
                    version_dirs = [d for d in cache_dir.iterdir() if d.is_dir()]
                    if version_dirs:
                        latest_version = max(version_dirs, key=lambda x: x.name)
                        readme_path = latest_version / "README.md"
                        
                        if readme_path.exists():
                            try:
                                os.startfile(str(readme_path))
                                return
                            except Exception as e:
                                messagebox.showerror("Error", f"Could not open README: {e}")
                                return
                                
        messagebox.showerror("Error", f"README not found for {mod_name}")
        
    def toggle_mod_status(self):
        """Toggle mod status (placeholder for future implementation)"""
        messagebox.showinfo("Info", "Mod status toggle functionality would be implemented here.\nThis could involve enabling/disabling mods in the mods.yml file.")
        
    def refresh_data(self):
        """Refresh all mod data"""
        self.mods_data.clear()
        self.mod_icons.clear()
        self.load_mods_data()
        self.filter_mods()

def main():
    root = tk.Tk()
    app = ValheimModManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
