import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
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
        self.root.geometry("1600x1000")  # Increased size for notes panel
        
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
        
        # Notes storage
        self.notes_file = Path("mod_manager_notes.json")
        self.notes_data = {}
        self.current_selected_item = None
        
        # Data storage
        self.mods_data = {}
        self.filtered_mods = []
        self.mod_icons = {}
        self.vnei_data = {}
        self.vnei_icons = {}
        self.loot_data = {}  # Loot table data
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
        
        # Load notes data
        self.load_notes()
        
        self.setup_ui()
        self.load_mods_data()
        self.load_vnei_data()
        self.load_loot_data()
        
        # Update notes counter
        self.update_notes_counter()
        
    def load_notes(self):
        """Load notes from JSON file"""
        if self.notes_file.exists():
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    self.notes_data = json.load(f)
                print(f"Loaded notes for {len(self.notes_data)} items")
            except Exception as e:
                print(f"Error loading notes: {e}")
                self.notes_data = {}
        else:
            self.notes_data = {}
            
    def save_notes(self):
        """Save notes to JSON file"""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes_data, f, indent=2, ensure_ascii=False)
            print("Notes saved successfully")
        except Exception as e:
            print(f"Error saving notes: {e}")
            messagebox.showerror("Error", f"Could not save notes: {e}")
            
    def get_item_key(self, item_type, item_name):
        """Generate a unique key for an item"""
        return f"{item_type}:{item_name}"
        
    def get_note(self, item_type, item_name):
        """Get note for an item"""
        key = self.get_item_key(item_type, item_name)
        return self.notes_data.get(key, "")
        
    def set_note(self, item_type, item_name, note_text):
        """Set note for an item"""
        key = self.get_item_key(item_type, item_name)
        if note_text.strip():
            self.notes_data[key] = note_text
        else:
            # Remove empty notes
            self.notes_data.pop(key, None)
        self.save_notes()
        self.update_notes_counter()
        
    def update_notes_counter(self):
        """Update the notes counter display"""
        notes_count = len(self.notes_data)
        self.notes_count_label.config(text=f"Notes: {notes_count}")
        
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
        
        # Notes counter
        self.notes_count_label = ttk.Label(search_frame, text="Notes: 0")
        self.notes_count_label.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
        
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
        
        # Loot Tables tab
        loot_frame = ttk.Frame(self.notebook)
        self.notebook.add(loot_frame, text="Loot Tables")
        
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
        # Use a more compatible theme approach
        try:
            self.mod_tree_style = style.theme_use()
        except:
            self.mod_tree_style = "default"
        # Don't configure style directly to avoid vista layout issues
        
        # Configure columns
        self.mod_tree.heading("#0", text="Icon")
        self.mod_tree.column("#0", width=60, minwidth=40)  # Increased default width for zoom
        self.mod_tree.heading("Name", text="Mod Name")
        self.mod_tree.column("Name", width=200, minwidth=150)
        self.mod_tree.heading("Version", text="Version")
        self.mod_tree.column("Version", width=80, minwidth=80)
        self.mod_tree.heading("Status", text="Status")
        self.mod_tree.column("Status", width=80, minwidth=80)
        
        # Configure tree styling for notes indicators
        style = ttk.Style()
        try:
            style.configure("Treeview", rowheight=25)
            style.map("Treeview", 
                     background=[("tag", "has_notes", "#e6f3ff")],  # Light blue background for items with notes
                     foreground=[("tag", "has_notes", "#000000")])  # Black text
        except Exception as e:
            print(f"Warning: Could not configure Treeview style: {e}")
        
        # Scrollbar for mod list
        mod_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.mod_tree.yview)
        self.mod_tree.configure(yscrollcommand=mod_scrollbar.set)
        
        self.mod_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mod_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.mod_tree.bind('<<TreeviewSelect>>', self.on_mod_select)
        
        # Right panel - Mod details and notes
        right_frame = ttk.Frame(mods_content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Mod details frame
        details_frame = ttk.LabelFrame(right_frame, text="Mod Details")
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Mod icon
        self.icon_label = ttk.Label(details_frame, text="No mod selected")
        self.icon_label.pack(pady=10)
        
        # Mod info text
        info_frame = ttk.Frame(details_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
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
        
        # Notes section for mods
        notes_frame = ttk.LabelFrame(right_frame, text="Notes")
        notes_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notes text area
        self.mod_notes_text = scrolledtext.ScrolledText(notes_frame, height=8, wrap=tk.WORD)
        self.mod_notes_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Notes buttons
        notes_btn_frame = ttk.Frame(notes_frame)
        notes_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(notes_btn_frame, text="Save Note", command=self.save_mod_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(notes_btn_frame, text="Clear Note", command=self.clear_mod_note).pack(side=tk.LEFT, padx=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind window close event to save notes
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # VNEI Items tab content
        self.setup_vnei_ui(vnei_frame)
        
        # Loot Tables tab content
        self.setup_loot_tables_ui(loot_frame)
        
        # Apply initial scaling after all UI components are initialized
        self.update_tree_scaling()
        
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
                
                # Check if mod has notes
                has_notes = bool(self.get_note("mod", mod_data['name']))
                note_tag = "has_notes" if has_notes else ""
                
                # Insert with icon or placeholder
                if icon_photo:
                    self.mod_tree.insert(category_item, "end", image=icon_photo,
                                       values=(mod_data['name'], mod_data['version'], mod_data['status']),
                                       tags=(note_tag,))
                else:
                    self.mod_tree.insert(category_item, "end", text="📦",
                                       values=(mod_data['name'], mod_data['version'], mod_data['status']),
                                       tags=(note_tag,))
                                   
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
            self.current_selected_item = mod_name
            self.show_mod_details(mod_name)
            
            # Load and display note for this mod
            note_text = self.get_note("mod", mod_name)
            self.mod_notes_text.delete("1.0", tk.END)
            self.mod_notes_text.insert("1.0", note_text)
            
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
        
    def save_mod_note(self):
        """Save the note for the currently selected mod"""
        if self.current_selected_item:
            mod_name = self.current_selected_item
            if mod_name in self.mods_data:
                note_text = self.mod_notes_text.get("1.0", tk.END).strip()
                self.set_note("mod", mod_name, note_text)
                messagebox.showinfo("Info", f"Note for '{mod_name}' saved.")
                # Refresh the tree to update visual indicators
                self.populate_mod_tree()
            else:
                messagebox.showwarning("Warning", "No mod selected to save note for.")
        else:
            messagebox.showwarning("Warning", "Please select a mod first to save a note.")
            
    def clear_mod_note(self):
        """Clear the note for the currently selected mod"""
        if self.current_selected_item:
            mod_name = self.current_selected_item
            if mod_name in self.mods_data:
                self.set_note("mod", mod_name, "")
                self.mod_notes_text.delete("1.0", tk.END)
                messagebox.showinfo("Info", f"Note for '{mod_name}' cleared.")
                # Refresh the tree to update visual indicators
                self.populate_mod_tree()
            else:
                messagebox.showwarning("Warning", "No mod selected to clear note for.")
        else:
            messagebox.showwarning("Warning", "Please select a mod first to clear a note.")
            
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
        
        # Left panel - VNEI items tree
        vnei_left_frame = ttk.Frame(vnei_content_frame)
        vnei_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # VNEI items tree
        vnei_list_frame = ttk.LabelFrame(vnei_left_frame, text="Items by Mod")
        vnei_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview for VNEI items
        vnei_columns = ("Item Name", "Prefab", "Type", "Description")
        self.vnei_tree = ttk.Treeview(vnei_list_frame, columns=vnei_columns, show="tree headings", height=25)
        
        # Configure tree style for better scaling
        style = ttk.Style()
        # Use a more compatible theme approach
        try:
            self.vnei_tree_style = style.theme_use()
        except:
            self.vnei_tree_style = "default"
        # Don't configure style directly to avoid vista layout issues
        
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
        
        # Configure VNEI tree styling for notes indicators
        style = ttk.Style()
        try:
            style.configure("VNEITreeview", rowheight=25)
            style.map("VNEITreeview", 
                     background=[("tag", "has_notes", "#e6f3ff")],  # Light blue background for items with notes
                     foreground=[("tag", "has_notes", "#000000")])  # Black text
            self.vnei_tree.configure(style="VNEITreeview")
        except Exception as e:
            print(f"Warning: Could not configure VNEITreeview style: {e}")
        
        # Scrollbar for VNEI items
        vnei_scrollbar = ttk.Scrollbar(vnei_list_frame, orient=tk.VERTICAL, command=self.vnei_tree.yview)
        self.vnei_tree.configure(yscrollcommand=vnei_scrollbar.set)
        
        self.vnei_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vnei_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.vnei_tree.bind('<<TreeviewSelect>>', self.on_vnei_item_select)
        
        # Right panel - VNEI item details and notes
        vnei_right_frame = ttk.Frame(vnei_content_frame)
        vnei_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # VNEI item details frame
        vnei_details_frame = ttk.LabelFrame(vnei_right_frame, text="Item Details")
        vnei_details_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Item info
        vnei_info_frame = ttk.Frame(vnei_details_frame)
        vnei_info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Item name
        self.vnei_item_name_label = ttk.Label(vnei_info_frame, text="", font=("Arial", 12, "bold"))
        self.vnei_item_name_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Item prefab
        self.vnei_item_prefab_label = ttk.Label(vnei_info_frame, text="")
        self.vnei_item_prefab_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Item type
        self.vnei_item_type_label = ttk.Label(vnei_info_frame, text="")
        self.vnei_item_type_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Item description
        self.vnei_item_desc_label = ttk.Label(vnei_info_frame, text="", wraplength=400)
        self.vnei_item_desc_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Notes section for VNEI items
        vnei_notes_frame = ttk.LabelFrame(vnei_right_frame, text="Notes")
        vnei_notes_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notes text area
        self.vnei_notes_text = scrolledtext.ScrolledText(vnei_notes_frame, height=12, wrap=tk.WORD)
        self.vnei_notes_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Notes buttons
        vnei_notes_btn_frame = ttk.Frame(vnei_notes_frame)
        vnei_notes_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(vnei_notes_btn_frame, text="Save Note", command=self.save_vnei_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(vnei_notes_btn_frame, text="Clear Note", command=self.clear_vnei_note).pack(side=tk.LEFT, padx=2)

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
                
                # Check if item has notes
                has_notes = bool(self.get_note(item_data['item_type'], item_data['localized_name']))
                note_tag = "has_notes" if has_notes else ""
                
                # Insert with icon or placeholder
                if icon_photo:
                    self.vnei_tree.insert(mod_item, "end", image=icon_photo,
                                        values=(item_data['localized_name'], 
                                               item_data['internal_name'],
                                               item_data['item_type'],
                                               item_data['description']),
                                        tags=(note_tag,))
                else:
                    self.vnei_tree.insert(mod_item, "end", text="📦",
                                        values=(item_data['localized_name'], 
                                               item_data['internal_name'],
                                               item_data['item_type'],
                                               item_data['description']),
                                        tags=(note_tag,))
        
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
            
            # Update item details display
            self.vnei_item_name_label.config(text=item_name)
            self.vnei_item_prefab_label.config(text=f"Prefab: {item_prefab}")
            self.vnei_item_type_label.config(text=f"Type: {item_type}")
            self.vnei_item_desc_label.config(text=item_desc)
            
            # Load and display note for this item
            note_text = self.get_note(item_type, item_name)
            self.vnei_notes_text.delete("1.0", tk.END)
            self.vnei_notes_text.insert("1.0", note_text)
            
            # Show item details in status bar
            self.status_var.set(f"Selected: {item_name} ({item_prefab}) - {item_type}")
            
    def save_vnei_note(self):
        """Save the note for the currently selected VNEI item"""
        selection = self.vnei_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item first to save a note.")
            return
            
        selected_item = selection[0]
        parent = self.vnei_tree.parent(selected_item)
        
        if not parent:
            return
            
        item_values = self.vnei_tree.item(selected_item, "values")
        item_name = item_values[0]
        item_type = item_values[2]
        
        note_text = self.vnei_notes_text.get("1.0", tk.END).strip()
        self.set_note(item_type, item_name, note_text)
        messagebox.showinfo("Info", f"Note for '{item_name}' saved.")
        # Refresh the tree to update visual indicators
        self.populate_vnei_tree()
        
    def clear_vnei_note(self):
        """Clear the note for the currently selected VNEI item"""
        selection = self.vnei_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item first to clear a note.")
            return
            
        selected_item = selection[0]
        parent = self.vnei_tree.parent(selected_item)
        
        if not parent:
            return
            
        item_values = self.vnei_tree.item(selected_item, "values")
        item_name = item_values[0]
        item_type = item_values[2]
        
        self.set_note(item_type, item_name, "")
        self.vnei_notes_text.delete("1.0", tk.END)
        messagebox.showinfo("Info", f"Note for '{item_name}' cleared.")
        # Refresh the tree to update visual indicators
        self.populate_vnei_tree()
        
    def clear_notes_display(self):
        """Clear the notes display when no item is selected"""
        self.mod_notes_text.delete("1.0", tk.END)
        self.vnei_notes_text.delete("1.0", tk.END)
        
    def on_closing(self):
        """Handle window closing - save any unsaved notes"""
        # Save current note if any item is selected
        if self.current_selected_item:
            note_text = self.mod_notes_text.get("1.0", tk.END).strip()
            if note_text:
                self.set_note("mod", self.current_selected_item, note_text)
                
        # Save VNEI note if any item is selected
        selection = self.vnei_tree.selection()
        if selection:
            selected_item = selection[0]
            parent = self.vnei_tree.parent(selected_item)
            if parent:
                item_values = self.vnei_tree.item(selected_item, "values")
                item_name = item_values[0]
                item_type = item_values[2]
                note_text = self.vnei_notes_text.get("1.0", tk.END).strip()
                if note_text:
                    self.set_note(item_type, item_name, note_text)
                    
        # Save notes and close
        self.save_notes()
        self.root.destroy()
        
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
        
        try:
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
        except Exception as e:
            print(f"Warning: Could not update tree scaling: {e}")
        
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

    def setup_loot_tables_ui(self, parent_frame):
        """Setup the loot tables interface"""
        # Loot Tables control frame
        loot_control_frame = ttk.LabelFrame(parent_frame, text="Loot Tables Analysis")
        loot_control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Parse button
        ttk.Button(loot_control_frame, text="🔄 Parse Config Files", command=self.parse_loot_configs).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Load data button
        ttk.Button(loot_control_frame, text="📂 Load Data", command=self.load_loot_data).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Export button
        ttk.Button(loot_control_frame, text="💾 Export Data", command=self.export_loot_data).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Search entry
        ttk.Label(loot_control_frame, text="Search:").pack(side=tk.LEFT, padx=(20, 5), pady=5)
        self.loot_search_var = tk.StringVar()
        self.loot_search_var.trace('w', self.filter_loot_data)
        loot_search_entry = ttk.Entry(loot_control_frame, textvariable=self.loot_search_var, width=20)
        loot_search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # View selector
        ttk.Label(loot_control_frame, text="View:").pack(side=tk.LEFT, padx=(20, 5), pady=5)
        self.loot_view_var = tk.StringVar(value="overview")
        loot_view_combo = ttk.Combobox(loot_control_frame, textvariable=self.loot_view_var, 
                                      values=["overview", "loot_tables", "items", "sources", "statistics"],
                                      state="readonly", width=15)
        loot_view_combo.pack(side=tk.LEFT, padx=5, pady=5)
        loot_view_combo.bind("<<ComboboxSelected>>", self.change_loot_view)
        
        # Loot Tables content area
        loot_content_frame = ttk.Frame(parent_frame)
        loot_content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create notebook for different loot views
        self.loot_notebook = ttk.Notebook(loot_content_frame)
        self.loot_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Overview tab
        self.loot_overview_frame = ttk.Frame(self.loot_notebook)
        self.loot_notebook.add(self.loot_overview_frame, text="Overview")
        
        # Loot Tables tab
        self.loot_tables_frame = ttk.Frame(self.loot_notebook)
        self.loot_notebook.add(self.loot_tables_frame, text="Loot Tables")
        
        # Items tab
        self.loot_items_frame = ttk.Frame(self.loot_notebook)
        self.loot_notebook.add(self.loot_items_frame, text="Items")
        
        # Sources tab
        self.loot_sources_frame = ttk.Frame(self.loot_notebook)
        self.loot_notebook.add(self.loot_sources_frame, text="Sources")
        
        # Statistics tab
        self.loot_stats_frame = ttk.Frame(self.loot_notebook)
        self.loot_notebook.add(self.loot_stats_frame, text="Statistics")
        
        # Setup individual tabs
        self.setup_loot_overview_tab()
        self.setup_loot_tables_tab()
        self.setup_loot_items_tab()
        self.setup_loot_sources_tab()
        self.setup_loot_statistics_tab()

    def setup_loot_overview_tab(self):
        """Setup the loot overview tab"""
        # Statistics display
        stats_frame = ttk.LabelFrame(self.loot_overview_frame, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.loot_stats_text = tk.Text(stats_frame, height=8, wrap=tk.WORD)
        self.loot_stats_text.pack(fill=tk.X)
        
        # Charts frame
        charts_frame = ttk.Frame(self.loot_overview_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create matplotlib figure for charts
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            self.loot_overview_fig, (self.loot_ax1, self.loot_ax2) = plt.subplots(1, 2, figsize=(12, 6))
            self.loot_overview_canvas = FigureCanvasTkAgg(self.loot_overview_fig, charts_frame)
            self.loot_overview_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except ImportError:
            # Fallback if matplotlib is not available
            self.loot_overview_canvas = None
            ttk.Label(charts_frame, text="Matplotlib not available for charts").pack(pady=20)

    def setup_loot_tables_tab(self):
        """Setup the loot tables tab"""
        # Treeview for loot tables
        tree_frame = ttk.Frame(self.loot_tables_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview for loot tables
        columns = ("Name", "Source", "Items", "Description")
        self.loot_tables_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        for col in columns:
            self.loot_tables_tree.heading(col, text=col, command=lambda c=col: self.sort_loot_treeview(self.loot_tables_tree, c, False))
            self.loot_tables_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.loot_tables_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.loot_tables_tree.xview)
        self.loot_tables_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.loot_tables_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click to show details
        self.loot_tables_tree.bind("<Double-1>", self.show_loot_table_details)

    def setup_loot_items_tab(self):
        """Setup the loot items tab"""
        # Treeview for items
        tree_frame = ttk.Frame(self.loot_items_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview for items
        columns = ("Item", "Loot Tables", "Sources")
        self.loot_items_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        for col in columns:
            self.loot_items_tree.heading(col, text=col, command=lambda c=col: self.sort_loot_treeview(self.loot_items_tree, c, False))
            self.loot_items_tree.column(col, width=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.loot_items_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.loot_items_tree.xview)
        self.loot_items_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.loot_items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click to show details
        self.loot_items_tree.bind("<Double-1>", self.show_loot_item_details)

    def setup_loot_sources_tab(self):
        """Setup the loot sources tab"""
        # Treeview for sources
        tree_frame = ttk.Frame(self.loot_sources_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview for sources
        columns = ("Source", "Loot Tables", "Items", "Description")
        self.loot_sources_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        for col in columns:
            self.loot_sources_tree.heading(col, text=col, command=lambda c=col: self.sort_loot_treeview(self.loot_sources_tree, c, False))
            self.loot_sources_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.loot_sources_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.loot_sources_tree.xview)
        self.loot_sources_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.loot_sources_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_loot_statistics_tab(self):
        """Setup the loot statistics tab"""
        # Charts frame
        charts_frame = ttk.Frame(self.loot_stats_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create matplotlib figure for detailed charts
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            self.loot_stats_fig, ((self.loot_ax3, self.loot_ax4), (self.loot_ax5, self.loot_ax6)) = plt.subplots(2, 2, figsize=(14, 10))
            self.loot_stats_canvas = FigureCanvasTkAgg(self.loot_stats_fig, charts_frame)
            self.loot_stats_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except ImportError:
            # Fallback if matplotlib is not available
            self.loot_stats_canvas = None
            ttk.Label(charts_frame, text="Matplotlib not available for statistics charts").pack(pady=20)

    def refresh_data(self):
        """Refresh all mod data"""
        self.mods_data.clear()
        self.mod_icons.clear()
        self.load_mods_data()
        self.filter_mods()

    def load_loot_data(self):
        """Load loot table data from JSON file"""
        try:
            data_file = Path("loot_table_data.json")
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    self.loot_data = json.load(f)
                self.update_loot_views()
                self.status_var.set(f"Loaded loot data: {len(self.loot_data.get('loot_tables', {}))} tables")
            else:
                self.status_var.set("No loot data file found. Please parse config files first.")
        except Exception as e:
            self.status_var.set(f"Error loading loot data: {e}")

    def parse_loot_configs(self):
        """Parse loot table configuration files"""
        self.status_var.set("Parsing loot table configurations...")
        self.root.update()
        
        try:
            # Import the loot table parser functionality
            from collections import defaultdict
            import re
            
            # Initialize data structures
            loot_tables = {}
            item_mappings = defaultdict(list)
            all_items = set()
            
            # Parse Warpalicious loot lists
            loot_file = self.config_path / "warpalicious.More_World_Locations_LootLists.yml"
            if loot_file.exists():
                with open(loot_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                if data and isinstance(data, dict):
                    for table_name, items in data.items():
                        if table_name == "version":
                            continue
                            
                        loot_items = []
                        for item_data in items:
                            if isinstance(item_data, dict) and "item" in item_data:
                                loot_item = {
                                    "item_name": item_data["item"],
                                    "stack_min": item_data.get("stackMin", 1),
                                    "stack_max": item_data.get("stackMax", 1),
                                    "weight": item_data.get("weight", 1.0),
                                    "rarity": None
                                }
                                loot_items.append(loot_item)
                                all_items.add(item_data["item"])
                        
                        if loot_items:
                            loot_tables[table_name] = {
                                "name": table_name,
                                "source": "Warpalicious More World Locations",
                                "items": loot_items,
                                "description": f"Loot table for {table_name}"
                            }
            
            # Parse EpicLoot configurations
            epicloot_path = self.config_path / "EpicLoot" / "patches" / "RelicHeimPatches"
            if epicloot_path.exists():
                for file_name in ["zLootables_CreatureDrops_RelicHeim.json", 
                                 "zLootables_BossDrops_RelicHeim.json",
                                 "zLootables_TreasureLoot_RelicHeim.json"]:
                    file_path = epicloot_path / file_name
                    if file_path.exists():
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                
                            if "Patches" in data:
                                for patch in data["Patches"]:
                                    if patch.get("Action") == "AppendAll" and "Value" in patch:
                                        for loot_table_data in patch["Value"]:
                                            if "Object" in loot_table_data and "LeveledLoot" in loot_table_data:
                                                table_name = f"{loot_table_data['Object']}_{file_name.replace('.json', '')}"
                                                
                                                loot_items = []
                                                for level_data in loot_table_data["LeveledLoot"]:
                                                    if "Loot" in level_data:
                                                        for loot_data in level_data["Loot"]:
                                                            if "Item" in loot_data:
                                                                loot_item = {
                                                                    "item_name": loot_data["Item"],
                                                                    "stack_min": 1,
                                                                    "stack_max": 1,
                                                                    "weight": loot_data.get("Weight", 1.0),
                                                                    "rarity": loot_data.get("Rarity")
                                                                }
                                                                loot_items.append(loot_item)
                                                                all_items.add(loot_data["Item"])
                                                
                                                if loot_items:
                                                    loot_tables[table_name] = {
                                                        "name": table_name,
                                                        "source": f"EpicLoot {file_name.replace('.json', '')}",
                                                        "items": loot_items,
                                                        "description": f"EpicLoot loot table for {loot_table_data['Object']}"
                                                    }
                        except Exception as e:
                            print(f"Error parsing {file_path}: {e}")
            
            # Parse CLLC configurations
            item_config = self.config_path / "ItemConfig_Base.yml"
            if item_config.exists():
                try:
                    with open(item_config, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        
                    if data and isinstance(data, dict) and "groups" in data:
                        for group_name, items in data["groups"].items():
                            if isinstance(items, list):
                                table_name = f"CLLC_Group_{group_name}"
                                loot_items = []
                                
                                for item_name in items:
                                    loot_item = {
                                        "item_name": item_name,
                                        "stack_min": 1,
                                        "stack_max": 1,
                                        "weight": 1.0,
                                        "rarity": None
                                    }
                                    loot_items.append(loot_item)
                                    all_items.add(item_name)
                                
                                if loot_items:
                                    loot_tables[table_name] = {
                                        "name": table_name,
                                        "source": "Creature Level & Loot Control",
                                        "items": loot_items,
                                        "description": f"CLLC item group: {group_name}"
                                    }
                except Exception as e:
                    print(f"Error parsing {item_config}: {e}")
            
            # Build item mappings
            for table_name, loot_table in loot_tables.items():
                for item in loot_table["items"]:
                    item_mappings[item["item_name"]].append(table_name)
            
            # Create statistics
            stats = {
                "total_loot_tables": len(loot_tables),
                "total_items": len(all_items),
                "sources": defaultdict(int),
                "items_per_table": [],
                "most_common_items": [],
                "largest_tables": []
            }
            
            # Count sources
            for table in loot_tables.values():
                stats["sources"][table["source"]] += 1
            
            # Items per table
            for table in loot_tables.values():
                stats["items_per_table"].append({
                    "table": table["name"],
                    "count": len(table["items"]),
                    "source": table["source"]
                })
            
            # Most common items
            stats["most_common_items"] = sorted(
                [(item, len(tables)) for item, tables in item_mappings.items()],
                key=lambda x: x[1],
                reverse=True
            )[:20]
            
            # Largest tables
            stats["largest_tables"] = sorted(
                stats["items_per_table"],
                key=lambda x: x["count"],
                reverse=True
            )[:10]
            
            # Create final data structure
            self.loot_data = {
                "loot_tables": loot_tables,
                "item_mappings": dict(item_mappings),
                "statistics": stats,
                "all_items": list(all_items)
            }
            
            # Export data
            self.export_loot_data()
            
            # Update views
            self.update_loot_views()
            
            self.status_var.set(f"Parsed {len(loot_tables)} loot tables with {len(all_items)} unique items")
            
        except Exception as e:
            self.status_var.set(f"Error parsing loot configs: {e}")
            messagebox.showerror("Error", f"Failed to parse loot configurations: {e}")

    def export_loot_data(self):
        """Export loot table data to JSON file"""
        if not self.loot_data:
            messagebox.showwarning("Warning", "No loot data to export")
            return
            
        try:
            with open("loot_table_data.json", 'w', encoding='utf-8') as f:
                json.dump(self.loot_data, f, indent=2, ensure_ascii=False)
            self.status_var.set("Loot data exported successfully")
        except Exception as e:
            self.status_var.set(f"Error exporting loot data: {e}")
            messagebox.showerror("Error", f"Could not export loot data: {e}")

    def update_loot_views(self):
        """Update all loot table views"""
        if not self.loot_data:
            return
            
        self.update_loot_overview()
        self.update_loot_tables()
        self.update_loot_items()
        self.update_loot_sources()
        self.update_loot_statistics()

    def update_loot_overview(self):
        """Update the loot overview tab"""
        if not self.loot_data:
            return
            
        stats = self.loot_data["statistics"]
        
        # Update statistics text
        self.loot_stats_text.delete(1.0, tk.END)
        stats_text = f"""
Total Loot Tables: {stats['total_loot_tables']}
Total Unique Items: {stats['total_items']}

Sources:
"""
        for source, count in stats['sources'].items():
            stats_text += f"  {source}: {count} tables\n"
        
        stats_text += f"\nTop 5 Most Common Items:\n"
        for item, count in stats['most_common_items'][:5]:
            stats_text += f"  {item}: {count} loot tables\n"
        
        stats_text += f"\nLargest Loot Tables:\n"
        for table_info in stats['largest_tables'][:5]:
            stats_text += f"  {table_info['table']}: {table_info['count']} items\n"
        
        self.loot_stats_text.insert(1.0, stats_text)
        
        # Update charts if available
        if hasattr(self, 'loot_overview_canvas') and self.loot_overview_canvas:
            self.update_loot_overview_charts()

    def update_loot_overview_charts(self):
        """Update overview charts"""
        if not self.loot_data or not hasattr(self, 'loot_overview_canvas') or not self.loot_overview_canvas:
            return
            
        stats = self.loot_data["statistics"]
        
        # Clear previous charts
        self.loot_ax1.clear()
        self.loot_ax2.clear()
        
        # Chart 1: Sources distribution
        sources = list(stats['sources'].keys())
        counts = list(stats['sources'].values())
        
        self.loot_ax1.pie(counts, labels=sources, autopct='%1.1f%%', startangle=90)
        self.loot_ax1.set_title('Loot Tables by Source')
        
        # Chart 2: Items per table distribution
        item_counts = [table['count'] for table in stats['items_per_table']]
        self.loot_ax2.hist(item_counts, bins=20, alpha=0.7, edgecolor='black')
        self.loot_ax2.set_xlabel('Items per Table')
        self.loot_ax2.set_ylabel('Number of Tables')
        self.loot_ax2.set_title('Distribution of Items per Loot Table')
        
        self.loot_overview_canvas.draw()

    def update_loot_tables(self):
        """Update the loot tables tab"""
        if not self.loot_data:
            return
            
        # Clear existing items
        for item in self.loot_tables_tree.get_children():
            self.loot_tables_tree.delete(item)
        
        # Add loot tables
        for table_name, table_data in self.loot_data["loot_tables"].items():
            self.loot_tables_tree.insert("", tk.END, values=(
                table_name,
                table_data["source"],
                len(table_data["items"]),
                table_data["description"][:50] + "..." if len(table_data["description"]) > 50 else table_data["description"]
            ))

    def update_loot_items(self):
        """Update the loot items tab"""
        if not self.loot_data:
            return
            
        # Clear existing items
        for item in self.loot_items_tree.get_children():
            self.loot_items_tree.delete(item)
        
        # Add items
        for item_name, table_names in self.loot_data["item_mappings"].items():
            # Get unique sources for this item
            sources = set()
            for table_name in table_names:
                if table_name in self.loot_data["loot_tables"]:
                    sources.add(self.loot_data["loot_tables"][table_name]["source"])
            
            self.loot_items_tree.insert("", tk.END, values=(
                item_name,
                len(table_names),
                ", ".join(sorted(sources))
            ))

    def update_loot_sources(self):
        """Update the loot sources tab"""
        if not self.loot_data:
            return
            
        # Clear existing items
        for item in self.loot_sources_tree.get_children():
            self.loot_sources_tree.delete(item)
        
        # Group by source
        source_data = defaultdict(lambda: {"tables": [], "items": set(), "descriptions": []})
        
        for table_name, table_data in self.loot_data["loot_tables"].items():
            source = table_data["source"]
            source_data[source]["tables"].append(table_name)
            source_data[source]["descriptions"].append(table_data["description"])
            
            for item in table_data["items"]:
                source_data[source]["items"].add(item["item_name"])
        
        # Add sources
        for source, data in source_data.items():
            self.loot_sources_tree.insert("", tk.END, values=(
                source,
                len(data["tables"]),
                len(data["items"]),
                f"{len(data['descriptions'])} loot tables"
            ))

    def update_loot_statistics(self):
        """Update the loot statistics tab"""
        if not self.loot_data or not hasattr(self, 'loot_stats_canvas') or not self.loot_stats_canvas:
            return
            
        stats = self.loot_data["statistics"]
        
        # Clear previous charts
        self.loot_ax3.clear()
        self.loot_ax4.clear()
        self.loot_ax5.clear()
        self.loot_ax6.clear()
        
        # Chart 1: Top items by loot table count
        top_items = stats['most_common_items'][:10]
        items = [item[0] for item in top_items]
        counts = [item[1] for item in top_items]
        
        self.loot_ax3.barh(items, counts)
        self.loot_ax3.set_xlabel('Number of Loot Tables')
        self.loot_ax3.set_title('Top 10 Items by Loot Table Count')
        
        # Chart 2: Largest loot tables
        largest_tables = stats['largest_tables'][:10]
        table_names = [table['table'][:20] + "..." if len(table['table']) > 20 else table['table'] for table in largest_tables]
        table_counts = [table['count'] for table in largest_tables]
        
        self.loot_ax4.barh(table_names, table_counts)
        self.loot_ax4.set_xlabel('Number of Items')
        self.loot_ax4.set_title('Largest Loot Tables')
        
        # Chart 3: Items per table histogram
        item_counts = [table['count'] for table in stats['items_per_table']]
        self.loot_ax5.hist(item_counts, bins=30, alpha=0.7, edgecolor='black')
        self.loot_ax5.set_xlabel('Items per Table')
        self.loot_ax5.set_ylabel('Number of Tables')
        self.loot_ax5.set_title('Distribution of Items per Table')
        
        # Chart 4: Sources pie chart
        sources = list(stats['sources'].keys())
        counts = list(stats['sources'].values())
        
        self.loot_ax6.pie(counts, labels=sources, autopct='%1.1f%%', startangle=90)
        self.loot_ax6.set_title('Loot Tables by Source')
        
        self.loot_stats_canvas.draw()

    def change_loot_view(self, event=None):
        """Change the current loot view"""
        view = self.loot_view_var.get()
        if view == "overview":
            self.loot_notebook.select(0)
        elif view == "loot_tables":
            self.loot_notebook.select(1)
        elif view == "items":
            self.loot_notebook.select(2)
        elif view == "sources":
            self.loot_notebook.select(3)
        elif view == "statistics":
            self.loot_notebook.select(4)

    def filter_loot_data(self, event=None):
        """Filter loot data based on search term"""
        search_term = self.loot_search_var.get().lower()
        
        # Clear current view
        current_tab = self.loot_notebook.index(self.loot_notebook.select())
        
        if current_tab == 1:  # Loot tables
            for item in self.loot_tables_tree.get_children():
                self.loot_tables_tree.delete(item)
            
            if self.loot_data:
                for table_name, table_data in self.loot_data["loot_tables"].items():
                    if (search_term in table_name.lower() or 
                        search_term in table_data["source"].lower() or
                        search_term in table_data["description"].lower()):
                        self.loot_tables_tree.insert("", tk.END, values=(
                            table_name,
                            table_data["source"],
                            len(table_data["items"]),
                            table_data["description"][:50] + "..." if len(table_data["description"]) > 50 else table_data["description"]
                        ))
        
        elif current_tab == 2:  # Items
            for item in self.loot_items_tree.get_children():
                self.loot_items_tree.delete(item)
            
            if self.loot_data:
                for item_name, table_names in self.loot_data["item_mappings"].items():
                    if search_term in item_name.lower():
                        sources = set()
                        for table_name in table_names:
                            if table_name in self.loot_data["loot_tables"]:
                                sources.add(self.loot_data["loot_tables"][table_name]["source"])
                        
                        self.loot_items_tree.insert("", tk.END, values=(
                            item_name,
                            len(table_names),
                            ", ".join(sorted(sources))
                        ))

    def sort_loot_treeview(self, tree, col, reverse):
        """Sort loot treeview by column"""
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        
        # Reverse sort next time
        tree.heading(col, command=lambda: self.sort_loot_treeview(tree, col, not reverse))

    def show_loot_table_details(self, event):
        """Show details for a selected loot table"""
        selection = self.loot_tables_tree.selection()
        if not selection:
            return
            
        item = self.loot_tables_tree.item(selection[0])
        table_name = item['values'][0]
        
        if self.loot_data and table_name in self.loot_data["loot_tables"]:
            table_data = self.loot_data["loot_tables"][table_name]
            
            # Create detail window
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Loot Table Details: {table_name}")
            detail_window.geometry("600x400")
            
            # Create text widget
            text_widget = tk.Text(detail_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add details
            details = f"Name: {table_name}\n"
            details += f"Source: {table_data['source']}\n"
            details += f"Description: {table_data['description']}\n"
            details += f"Items ({len(table_data['items'])}):\n\n"
            
            for item in table_data['items']:
                details += f"  {item['item_name']}\n"
                details += f"    Stack: {item['stack_min']}-{item['stack_max']}\n"
                details += f"    Weight: {item['weight']}\n"
                if item['rarity']:
                    details += f"    Rarity: {item['rarity']}\n"
                details += "\n"
            
            text_widget.insert(1.0, details)
            text_widget.config(state=tk.DISABLED)

    def show_loot_item_details(self, event):
        """Show details for a selected loot item"""
        selection = self.loot_items_tree.selection()
        if not selection:
            return
            
        item = self.loot_items_tree.item(selection[0])
        item_name = item['values'][0]
        
        if self.loot_data and item_name in self.loot_data["item_mappings"]:
            table_names = self.loot_data["item_mappings"][item_name]
            
            # Create detail window
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Item Details: {item_name}")
            detail_window.geometry("600x400")
            
            # Create text widget
            text_widget = tk.Text(detail_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add details
            details = f"Item: {item_name}\n"
            details += f"Found in {len(table_names)} loot tables:\n\n"
            
            for table_name in table_names:
                if table_name in self.loot_data["loot_tables"]:
                    table_data = self.loot_data["loot_tables"][table_name]
                    details += f"  {table_name} ({table_data['source']})\n"
                    
                    # Find the specific item data
                    for item_data in table_data['items']:
                        if item_data['item_name'] == item_name:
                            details += f"    Stack: {item_data['stack_min']}-{item_data['stack_max']}\n"
                            details += f"    Weight: {item_data['weight']}\n"
                            if item_data['rarity']:
                                details += f"    Rarity: {item_data['rarity']}\n"
                            break
                    details += "\n"
            
            text_widget.insert(1.0, details)
            text_widget.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = ValheimModManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
