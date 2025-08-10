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
        self.root.geometry("1400x900")
        
        # Paths - try multiple possible locations
        possible_valheim_paths = [
            Path("Valheim"),
            Path("../Valheim"),
            Path("../../Valheim")
        ]
        
        self.valheim_path = None
        for path in possible_valheim_paths:
            if path.exists():
                self.valheim_path = path
                break
                
        if not self.valheim_path:
            messagebox.showerror("Error", "Valheim directory not found!")
            return
            
        print(f"Using Valheim path: {self.valheim_path.absolute()}")
        
        self.cache_path = self.valheim_path / "cache"
        self.profiles_path = self.valheim_path / "profiles"
        self.config_path = self.profiles_path / "Dogeheim_Player" / "BepInEx" / "config"
        
        # Data storage
        self.mods_data = {}
        self.filtered_mods = []
        self.mod_icons = {}
        self.vnei_data = {}
        self.vnei_icons = {}
        self.zoom_level = 1.0  # Default zoom level
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
        self.load_vnei_data()
        
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
        
        # Zoom controls
        zoom_frame = ttk.LabelFrame(control_frame, text="Zoom Controls")
        zoom_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(zoom_frame, text="Icon Zoom:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.zoom_var = tk.DoubleVar(value=1.0)
        zoom_scale = ttk.Scale(zoom_frame, from_=0.5, to=3.0, variable=self.zoom_var, 
                              orient=tk.HORIZONTAL, length=200, command=self.on_zoom_change)
        zoom_scale.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.zoom_label = ttk.Label(zoom_frame, text="100%")
        self.zoom_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Zoom preset buttons
        ttk.Button(zoom_frame, text="50%", command=lambda: self.set_zoom(0.5)).grid(row=0, column=3, padx=2, pady=5)
        ttk.Button(zoom_frame, text="100%", command=lambda: self.set_zoom(1.0)).grid(row=0, column=4, padx=2, pady=5)
        ttk.Button(zoom_frame, text="150%", command=lambda: self.set_zoom(1.5)).grid(row=0, column=5, padx=2, pady=5)
        ttk.Button(zoom_frame, text="200%", command=lambda: self.set_zoom(2.0)).grid(row=0, column=6, padx=2, pady=5)
        
        # Main content area with tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Mods tab
        mods_frame = ttk.Frame(self.notebook)
        self.notebook.add(mods_frame, text="Mods")
        
        # VNEI Items tab
        vnei_frame = ttk.Frame(self.notebook)
        self.notebook.add(vnei_frame, text="VNEI Items")
        
        # Mods tab content
        mods_content_frame = ttk.Frame(mods_frame)
        mods_content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Mod list
        left_frame = ttk.Frame(mods_content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Mod list with scrollbar
        list_frame = ttk.LabelFrame(left_frame, text="Mods")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for mod list
        columns = ("Name", "Version", "Status")
        self.mod_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=20)
        
        # Configure tree style for better scaling
        style = ttk.Style()
        self.mod_tree_style = style.theme_use()
        self.mod_tree.configure(style=self.mod_tree_style)
        
        # Configure columns
        self.mod_tree.heading("#0", text="Icon")
        self.mod_tree.column("#0", width=60, minwidth=40)  # Increased default width for zoom
        self.mod_tree.heading("Name", text="Mod Name")
        self.mod_tree.column("Name", width=200, minwidth=150)
        self.mod_tree.heading("Version", text="Version")
        self.mod_tree.column("Version", width=80, minwidth=80)
        self.mod_tree.heading("Status", text="Status")
        self.mod_tree.column("Status", width=80, minwidth=80)
        
        # Apply initial scaling
        self.update_tree_scaling()
        
        # Scrollbar for mod list
        mod_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.mod_tree.yview)
        self.mod_tree.configure(yscrollcommand=mod_scrollbar.set)
        
        self.mod_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mod_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.mod_tree.bind('<<TreeviewSelect>>', self.on_mod_select)
        
        # Right panel - Mod details
        right_frame = ttk.Frame(mods_content_frame)
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
        
        # VNEI Items tab content
        self.setup_vnei_ui(vnei_frame)
        
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
        # Try multiple possible paths
        possible_paths = [
            Path("Valheim_Help_Docs/Summaries/Valheim_Content_Mods_Summary.md"),
            Path("../Valheim_Help_Docs/Summaries/Valheim_Content_Mods_Summary.md"),
            Path("../../Valheim_Help_Docs/Summaries/Valheim_Content_Mods_Summary.md"),
            Path("Valheim_Content_Mods_Summary.md")
        ]
        
        summary_file = None
        for path in possible_paths:
            if path.exists():
                summary_file = path
                break
                
        if not summary_file:
            error_msg = f"Valheim_Content_Mods_Summary.md not found! Tried paths:\n"
            for path in possible_paths:
                error_msg += f"  - {path.absolute()}\n"
            messagebox.showerror("Error", error_msg)
            return
            
        print(f"Loading mods from: {summary_file.absolute()}")
            
        with open(summary_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the summary file to extract mod information
        # This is a simplified parser - you might want to enhance it
        lines = content.split('\n')
        current_mod = None
        mod_count = 0
        
        print(f"Parsing {len(lines)} lines from summary file...")
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            
            # Look for mod links in the format [ModName](#modname-version)
            if line.startswith('- [') and '](#' in line and line.endswith(')'):
                # Extract mod name and version from link format
                # Format: [ModName](#modname-version)
                start_bracket = line.find('[')
                end_bracket = line.find(']')
                hash_start = line.find('(#')
                hash_end = line.rfind(')')
                
                if start_bracket != -1 and end_bracket != -1 and hash_start != -1 and hash_end != -1:
                    mod_name = line[start_bracket + 1:end_bracket]
                    version_part = line[hash_start + 2:hash_end]  # Remove (# and )
                    
                    # Extract version from the end of the version_part
                    if '-' in version_part:
                        version = version_part.split('-')[-1]
                    else:
                        version = "unknown"
                    
                    current_mod = {
                        'name': mod_name,
                        'version': version,
                        'description': f'Mod from {mod_name}',
                        'category': self.categorize_mod(mod_name),
                        'config_files': [],
                        'status': 'Unknown'
                    }
                    self.mods_data[mod_name] = current_mod
                    mod_count += 1
                    print(f"Found mod {mod_count}: {mod_name} (v{version})")
                    
            # Also look for the old format just in case
            elif line.startswith('### **') and line.endswith('**'):
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
                    mod_count += 1
                    print(f"Found mod {mod_count}: {mod_name} (v{version})")
                    
            elif current_mod and line.startswith('- **'):
                # Extract key features
                feature = line[4:].strip()
                if current_mod['description']:
                    current_mod['description'] += '; ' + feature
                else:
                    current_mod['description'] = feature
                    
        print(f"Total mods parsed: {mod_count}")
        print(f"Mods data keys: {list(self.mods_data.keys())}")
                    
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
            print("Cache path not found")
            return
            
        print(f"Loading icons from: {self.cache_path}")
        icon_count = 0
        
        # Store original images for zooming
        self.mod_original_images = {}
        
        for mod_dir in self.cache_path.iterdir():
            if mod_dir.is_dir():
                # Find the latest version directory
                version_dirs = [d for d in mod_dir.iterdir() if d.is_dir()]
                if version_dirs:
                    latest_version = max(version_dirs, key=lambda x: x.name)
                    icon_path = latest_version / "icon.png"
                    
                    if icon_path.exists():
                        try:
                            # Load original image
                            original_image = Image.open(icon_path)
                            self.mod_original_images[mod_dir.name] = original_image
                            
                            # Create resized icon with current zoom
                            resized_image = self.resize_image_with_zoom(original_image, 24)
                            photo = ImageTk.PhotoImage(resized_image)
                            self.mod_icons[mod_dir.name] = photo
                            icon_count += 1
                            print(f"Loaded icon for: {mod_dir.name}")
                        except Exception as e:
                            print(f"Error loading icon for {mod_dir.name}: {e}")
                    else:
                        print(f"No icon found for: {mod_dir.name}")
                        
        print(f"Loaded {icon_count} icons total")
                            
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
                # Find matching icon
                icon_photo = None
                for cache_name, photo in self.mod_icons.items():
                    # Try to match mod name with cache name
                    if (cache_name.lower() in mod_name.lower() or 
                        mod_name.lower() in cache_name.lower() or
                        cache_name.lower().replace('-', '').replace('_', '') in mod_name.lower().replace('-', '').replace('_', '') or
                        mod_name.lower().replace('-', '').replace('_', '') in cache_name.lower().replace('-', '').replace('_', '')):
                        icon_photo = photo
                        break
                
                # Insert with icon or placeholder
                if icon_photo:
                    self.mod_tree.insert(category_item, "end", image=icon_photo,
                                       values=(mod_data['name'], mod_data['version'], mod_data['status']))
                else:
                    self.mod_tree.insert(category_item, "end", text="📦",
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
            # Try to match mod name with cache name
            if (cache_name.lower() in mod_name.lower() or 
                mod_name.lower() in cache_name.lower() or
                cache_name.lower().replace('-', '').replace('_', '') in mod_name.lower().replace('-', '').replace('_', '') or
                mod_name.lower().replace('-', '').replace('_', '') in cache_name.lower().replace('-', '').replace('_', '')):
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
        
    def setup_vnei_ui(self, parent_frame):
        """Setup the VNEI items interface"""
        # VNEI control frame
        vnei_control_frame = ttk.LabelFrame(parent_frame, text="VNEI Items Search & Filter")
        vnei_control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Search entry
        ttk.Label(vnei_control_frame, text="Search Items:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.vnei_search_var = tk.StringVar()
        self.vnei_search_var.trace('w', self.filter_vnei_items)
        vnei_search_entry = ttk.Entry(vnei_control_frame, textvariable=self.vnei_search_var, width=30)
        vnei_search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Mod filter
        ttk.Label(vnei_control_frame, text="Mod:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.vnei_mod_var = tk.StringVar()
        self.vnei_mod_var.set("All Mods")
        vnei_mod_combo = ttk.Combobox(vnei_control_frame, textvariable=self.vnei_mod_var, 
                                      values=["All Mods"], state="readonly", width=25)
        vnei_mod_combo.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        vnei_mod_combo.bind('<<ComboboxSelected>>', self.filter_vnei_items)
        
        # Item type filter
        ttk.Label(vnei_control_frame, text="Type:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.vnei_type_var = tk.StringVar()
        self.vnei_type_var.set("All Types")
        vnei_type_combo = ttk.Combobox(vnei_control_frame, textvariable=self.vnei_type_var,
                                       values=["All Types"], state="readonly", width=15)
        vnei_type_combo.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        vnei_type_combo.bind('<<ComboboxSelected>>', self.filter_vnei_items)
        
        # Refresh button
        vnei_refresh_btn = ttk.Button(vnei_control_frame, text="🔄 Refresh VNEI", command=self.refresh_vnei_data)
        vnei_refresh_btn.grid(row=0, column=6, padx=5, pady=5)
        
        # VNEI content area
        vnei_content_frame = ttk.Frame(parent_frame)
        vnei_content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # VNEI items tree
        vnei_list_frame = ttk.LabelFrame(vnei_content_frame, text="Items by Mod")
        vnei_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for VNEI items
        vnei_columns = ("Item Name", "Prefab", "Type", "Description")
        self.vnei_tree = ttk.Treeview(vnei_list_frame, columns=vnei_columns, show="tree headings", height=25)
        
        # Configure tree style for better scaling
        style = ttk.Style()
        self.vnei_tree_style = style.theme_use()
        self.vnei_tree.configure(style=self.vnei_tree_style)
        
        # Configure columns
        self.vnei_tree.heading("#0", text="Icon")
        self.vnei_tree.column("#0", width=60, minwidth=40)  # Increased default width for zoom
        self.vnei_tree.heading("Item Name", text="Item Name")
        self.vnei_tree.column("Item Name", width=200, minwidth=150)
        self.vnei_tree.heading("Prefab", text="Prefab")
        self.vnei_tree.column("Prefab", width=150, minwidth=100)
        self.vnei_tree.heading("Type", text="Type")
        self.vnei_tree.column("Type", width=100, minwidth=80)
        self.vnei_tree.heading("Description", text="Description")
        self.vnei_tree.column("Description", width=300, minwidth=200)
        
        # Apply initial scaling
        self.update_tree_scaling()
        
        # Scrollbar for VNEI items
        vnei_scrollbar = ttk.Scrollbar(vnei_list_frame, orient=tk.VERTICAL, command=self.vnei_tree.yview)
        self.vnei_tree.configure(yscrollcommand=vnei_scrollbar.set)
        
        self.vnei_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vnei_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.vnei_tree.bind('<<TreeviewSelect>>', self.on_vnei_item_select)
        
    def load_vnei_data(self):
        """Load VNEI items data from CSV and icons"""
        self.status_var.set("Loading VNEI data...")
        self.root.update()
        
        # Load VNEI items from CSV
        self.load_vnei_items_from_csv()
        
        # Load VNEI icons
        self.load_vnei_icons()
        
        # Populate the VNEI tree
        self.populate_vnei_tree()
        
        self.status_var.set(f"Loaded {len(self.vnei_data)} VNEI items")
        
    def load_vnei_items_from_csv(self):
        """Load VNEI items from the CSV file"""
        vnei_csv_path = self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "VNEI-Export" / "VNEI.indexed.items.csv"
        
        if not vnei_csv_path.exists():
            print(f"VNEI CSV file not found: {vnei_csv_path}")
            return
            
        print(f"Loading VNEI items from: {vnei_csv_path}")
        
        import csv
        item_count = 0
        
        with open(vnei_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                internal_name = row.get('Internal Name', '').strip('"')
                localized_name = row.get('Localized Name', '').strip('"')
                item_type = row.get('Item Type', '').strip('"')
                description = row.get('Description', '').strip('"')
                source_mod = row.get('Source Mod', '').strip('"')
                
                if internal_name and localized_name:
                    item_data = {
                        'internal_name': internal_name,
                        'localized_name': localized_name,
                        'item_type': item_type,
                        'description': description,
                        'source_mod': source_mod,
                        'icon_path': None
                    }
                    
                    # Group by source mod
                    if source_mod not in self.vnei_data:
                        self.vnei_data[source_mod] = []
                    
                    self.vnei_data[source_mod].append(item_data)
                    item_count += 1
                    
        print(f"Loaded {item_count} VNEI items from {len(self.vnei_data)} mods")
        
    def load_vnei_icons(self):
        """Load VNEI item icons"""
        vnei_icons_path = self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "VNEI-Export" / "icons"
        
        if not vnei_icons_path.exists():
            print(f"VNEI icons path not found: {vnei_icons_path}")
            return
            
        print(f"Loading VNEI icons from: {vnei_icons_path}")
        icon_count = 0
        
        # Store original images for zooming
        self.vnei_original_images = {}
        
        # Walk through all mod directories
        for mod_dir in vnei_icons_path.iterdir():
            if mod_dir.is_dir():
                mod_name = mod_dir.name
                
                # Walk through all PNG files in this mod directory
                for icon_file in mod_dir.glob("*.png"):
                    try:
                        # Load original image
                        original_image = Image.open(icon_file)
                        icon_key = f"{mod_name}_{icon_file.stem}"
                        self.vnei_original_images[icon_key] = original_image
                        
                        # Create resized icon with current zoom
                        resized_image = self.resize_image_with_zoom(original_image, 24)
                        photo = ImageTk.PhotoImage(resized_image)
                        self.vnei_icons[icon_key] = photo
                        icon_count += 1
                        
                    except Exception as e:
                        print(f"Error loading VNEI icon {icon_file}: {e}")
                        
        print(f"Loaded {icon_count} VNEI icons")
        
    def populate_vnei_tree(self):
        """Populate the VNEI tree with loaded data"""
        # Clear existing items
        for item in self.vnei_tree.get_children():
            self.vnei_tree.delete(item)
            
        # Get unique mods and types for filters
        mods = ["All Mods"] + list(self.vnei_data.keys())
        types = set()
        
        # Add mods and items to tree
        for mod_name, items in self.vnei_data.items():
            mod_item = self.vnei_tree.insert("", "end", text=mod_name, values=("", "", "", ""))
            
            for item_data in items:
                # Add item type to set for filter
                if item_data['item_type']:
                    types.add(item_data['item_type'])
                
                # Find matching icon
                icon_photo = None
                icon_key = f"{mod_name}_{item_data['internal_name']}"
                if icon_key in self.vnei_icons:
                    icon_photo = self.vnei_icons[icon_key]
                else:
                    # Try alternative icon names
                    for alt_key in self.vnei_icons.keys():
                        if (mod_name in alt_key and 
                            (item_data['internal_name'].lower() in alt_key.lower() or 
                             alt_key.lower().endswith(item_data['internal_name'].lower()))):
                            icon_photo = self.vnei_icons[alt_key]
                            break
                
                # Create display name with prefab
                display_name = f"{item_data['localized_name']} ({item_data['internal_name']})"
                
                # Insert with icon or placeholder
                if icon_photo:
                    self.vnei_tree.insert(mod_item, "end", image=icon_photo,
                                        values=(item_data['localized_name'], 
                                               item_data['internal_name'],
                                               item_data['item_type'],
                                               item_data['description']))
                else:
                    self.vnei_tree.insert(mod_item, "end", text="📦",
                                        values=(item_data['localized_name'], 
                                               item_data['internal_name'],
                                               item_data['item_type'],
                                               item_data['description']))
        
        # Update filter dropdowns
        types = ["All Types"] + sorted(list(types))
        
        # Update comboboxes if they exist
        if hasattr(self, 'vnei_mod_combo'):
            self.vnei_mod_combo['values'] = mods
        if hasattr(self, 'vnei_type_combo'):
            self.vnei_type_combo['values'] = types
            
        # Expand all mods
        for item in self.vnei_tree.get_children():
            self.vnei_tree.item(item, open=True)
            
    def filter_vnei_items(self, event=None):
        """Filter VNEI items based on search and filter criteria"""
        search_term = self.vnei_search_var.get().lower()
        selected_mod = self.vnei_mod_var.get()
        selected_type = self.vnei_type_var.get()
        
        # Hide all items first
        for item in self.vnei_tree.get_children():
            self.vnei_tree.item(item, open=False)
            
        # Show matching items
        for mod_item in self.vnei_tree.get_children():
            mod_text = self.vnei_tree.item(mod_item, "text")
            
            # Check mod filter
            if selected_mod != "All Mods" and mod_text != selected_mod:
                continue
                
            # Check items in this mod
            visible_items = 0
            for item in self.vnei_tree.get_children(mod_item):
                item_values = self.vnei_tree.item(item, "values")
                item_name = item_values[0].lower()
                item_prefab = item_values[1].lower()
                item_type = item_values[2]
                
                # Check search filter
                if search_term and (search_term not in item_name and search_term not in item_prefab):
                    continue
                    
                # Check type filter
                if selected_type != "All Types" and item_type != selected_type:
                    continue
                    
                # Show this item
                self.vnei_tree.item(item, tags=("visible",))
                visible_items += 1
                
            # Show mod if it has visible items
            if visible_items > 0:
                self.vnei_tree.item(mod_item, open=True)
                
    def on_vnei_item_select(self, event):
        """Handle VNEI item selection"""
        selection = self.vnei_tree.selection()
        if not selection:
            return
            
        selected_item = selection[0]
        parent = self.vnei_tree.parent(selected_item)
        
        # Only handle item selections, not mod selections
        if parent:
            item_values = self.vnei_tree.item(selected_item, "values")
            item_name = item_values[0]
            item_prefab = item_values[1]
            item_type = item_values[2]
            item_desc = item_values[3]
            
            # Show item details in status bar
            self.status_var.set(f"Selected: {item_name} ({item_prefab}) - {item_type}")
            
    def resize_image_with_zoom(self, image, base_size):
        """Resize image with current zoom level"""
        zoomed_size = int(base_size * self.zoom_level)
        return image.resize((zoomed_size, zoomed_size), Image.Resampling.LANCZOS)
        
    def on_zoom_change(self, value):
        """Handle zoom level change"""
        self.zoom_level = float(value)
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
        self.update_all_icons()
        
    def set_zoom(self, zoom_level):
        """Set zoom level to specific value"""
        self.zoom_var.set(zoom_level)
        self.zoom_level = zoom_level
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
        self.update_all_icons()
        
    def update_all_icons(self):
        """Update all icons with new zoom level"""
        # Update mod icons
        if hasattr(self, 'mod_original_images'):
            for mod_name, original_image in self.mod_original_images.items():
                resized_image = self.resize_image_with_zoom(original_image, 24)
                photo = ImageTk.PhotoImage(resized_image)
                self.mod_icons[mod_name] = photo
                
        # Update VNEI icons
        if hasattr(self, 'vnei_original_images'):
            for icon_key, original_image in self.vnei_original_images.items():
                resized_image = self.resize_image_with_zoom(original_image, 24)
                photo = ImageTk.PhotoImage(resized_image)
                self.vnei_icons[icon_key] = photo
                
        # Update column widths based on zoom
        icon_width = max(40, int(60 * self.zoom_level))
        self.mod_tree.column("#0", width=icon_width, minwidth=40)
        self.vnei_tree.column("#0", width=icon_width, minwidth=40)
        
        # Update text scaling and row heights
        self.update_tree_scaling()
        
        # Refresh the trees to show updated icons
        self.populate_mod_tree()
        self.populate_vnei_tree()
        
    def update_tree_scaling(self):
        """Update tree view scaling for better readability"""
        # Calculate scaled font size
        base_font_size = 9
        scaled_font_size = max(8, int(base_font_size * self.zoom_level))
        
        # Calculate scaled row height
        base_row_height = 20
        scaled_row_height = max(16, int(base_row_height * self.zoom_level))
        
        # Update tree styles with scaled fonts
        style = ttk.Style()
        
        # Configure Treeview style with larger font
        style.configure("Treeview", 
                       font=("TkDefaultFont", scaled_font_size),
                       rowheight=scaled_row_height)
        
        # Configure Treeview headings with larger font
        style.configure("Treeview.Heading", 
                       font=("TkDefaultFont", scaled_font_size, "bold"))
        
        # Apply the style to both trees
        self.mod_tree.configure(style="Treeview")
        self.vnei_tree.configure(style="Treeview")
        
        # Update column widths for better text display
        name_width = max(150, int(200 * self.zoom_level))
        version_width = max(80, int(80 * self.zoom_level))
        status_width = max(80, int(80 * self.zoom_level))
        prefab_width = max(100, int(150 * self.zoom_level))
        type_width = max(80, int(100 * self.zoom_level))
        desc_width = max(200, int(300 * self.zoom_level))
        
        # Update mod tree column widths
        self.mod_tree.column("Name", width=name_width, minwidth=150)
        self.mod_tree.column("Version", width=version_width, minwidth=80)
        self.mod_tree.column("Status", width=status_width, minwidth=80)
        
        # Update VNEI tree column widths
        self.vnei_tree.column("Item Name", width=name_width, minwidth=150)
        self.vnei_tree.column("Prefab", width=prefab_width, minwidth=100)
        self.vnei_tree.column("Type", width=type_width, minwidth=80)
        self.vnei_tree.column("Description", width=desc_width, minwidth=200)

    def refresh_vnei_data(self):
        """Refresh VNEI data"""
        self.vnei_data.clear()
        self.vnei_icons.clear()
        self.load_vnei_data()
        self.filter_vnei_items()

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
