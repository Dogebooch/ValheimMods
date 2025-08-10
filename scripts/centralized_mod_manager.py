#!/usr/bin/env python3
"""
Centralized Mod Manager for Valheim

This script provides a unified interface for managing:
- Mod installations and configurations
- Loot tables across multiple mods
- Content filtering and organization
- Mod icons and visual management

Features:
- Integrated mod and loot table management
- Icon support for mods and items
- Content-based filtering using mod categories
- Backup and restore functionality
- Unified configuration interface
"""

import os
import json
import yaml
import re
import shutil
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import urllib.request
import io

# Import the centralized loot manager
from centralized_loot_manager import CentralizedLootManager, LootItem, LootTable

@dataclass
class ModInfo:
    """Represents information about a mod"""
    name: str
    display_name: str
    version: str
    description: str
    author: str
    category: str
    icon_path: str = ""
    website_url: str = ""
    dependencies: List[str] = None
    conflicts: List[str] = None
    status: str = "Unknown"
    enabled: bool = True
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.conflicts is None:
            self.conflicts = []

class CentralizedModManager:
    """Main class for managing centralized mod and loot table management"""
    
    def __init__(self, valheim_path: str = "Valheim"):
        self.valheim_path = Path(valheim_path)
        self.config_path = self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "config"
        self.cache_path = self.valheim_path / "cache"
        self.backup_path = self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "config" / "mod_backups"
        
        # Ensure directories exist
        self.backup_path.mkdir(exist_ok=True)
        
        # Mod data
        self.mods: Dict[str, ModInfo] = {}
        self.mod_categories = {}
        self.mod_icons = {}
        
        # Loot manager
        self.loot_manager = CentralizedLootManager(valheim_path)
        
        # Load mod categories from content summary
        self.load_mod_categories()
        
        # Load existing data
        self.load_mod_data()
    
    def load_mod_categories(self):
        """Load mod categories from the content summary"""
        self.mod_categories = {
            "🛡️ Armor & Equipment": [
                "Shawesome-Shawesomes_Divine_Armaments",
                "Therzie-Armory",
                "HugotheDwarf-Hugos_Armory",
                "Southsil-SouthsilArmor",
                "Fantu-Sages_Vault"
            ],
            "⚔️ Weapons & Combat": [
                "Therzie-Warfare",
                "Therzie-WarfareFireAndIce"
            ],
            "🧙‍♂️ Magic & Spell": [
                "blacks7ar-MagicRevamp",
                "Therzie-Wizardry",
                "Soloredis-RtDMagic"
            ],
            "🎒 Loot & Progression": [
                "Vapok-AdventureBackpacks",
                "Smoothbrain-Backpacks",
                "RandyKnapp-EpicLoot",
                "JewelHeim-RelicHeim",
                "KGvalheim-Valheim_Enchantment_System"
            ],
            "🍖 Food & Consumable": [
                "blacks7ar-CookingAdditions",
                "OdinPlus-PotionPlus",
                "Smoothbrain-Cooking"
            ],
            "🌱 Farming & Agriculture": [
                "Advize-PlantEverything",
                "Smoothbrain-Farming",
                "Smoothbrain-Foraging",
                "Smoothbrain-Lumberjacking",
                "Smoothbrain-Mining",
                "Smoothbrain-Ranching"
            ],
            "🏰 Building & Location": [
                "warpalicious",
                "OdinPlus-OdinArchitect",
                "blacks7ar-FineWoodBuildPieces",
                "blacks7ar-FineWoodFurnitures",
                "MathiasDecrock-PlanBuild",
                "ComfyMods-Scenic",
                "BentoG-MissingPieces"
            ],
            "⛵ Naval & Ship": [
                "Marlthon-OdinShipPlus",
                "Smoothbrain-Sailing",
                "Smoothbrain-SailingSpeed"
            ],
            "🌍 Environmental & Seasonal": [
                "RustyMods-Seasonality",
                "shudnal-Seasons",
                "Willybach-Willybachs_HD_Seasonality"
            ],
            "🐉 Monster & Boss": [
                "Therzie-Monstrum",
                "Therzie-MonstrumDeepNorth",
                "Horem-MushroomMonsters",
                "TaegukGaming-Biome_Lords_Quest"
            ],
            "🎮 Gameplay & Systems": [
                "Smoothbrain-CreatureLevelAndLootControl",
                "Smoothbrain-SmartSkills",
                "Smoothbrain-PassivePowers",
                "Smoothbrain-DualWield",
                "Smoothbrain-Exploration",
                "Smoothbrain-Blacksmithing",
                "Smoothbrain-Building",
                "Smoothbrain-PackHorse",
                "Smoothbrain-Groups",
                "Smoothbrain-ServerCharacters",
                "Smoothbrain-TargetPortal",
                "Smoothbrain-Tenacity",
                "Smoothbrain-ConversionSizeAndSpeed",
                "Smoothbrain-ConfigWatcher",
                "Smoothbrain-DarwinAwards",
                "Smoothbrain-AntiCensorship",
                "WackyMole-WackyEpicMMOSystem",
                "WackyMole-WackysDatabase",
                "WackyMole-Tone_Down_the_Twang",
                "OdinPlus-OdinsKingdom",
                "shudnal-TradersExtended",
                "RandomSteve-BreatheEasy",
                "Nextek-SpeedyPaths",
                "MSchmoecker-VNEI",
                "MSchmoecker-PressurePlate",
                "MSchmoecker-MultiUserChest",
                "Korppis-ReliableBlock",
                "JereKuusela-World_Edit_Commands",
                "JereKuusela-Upgrade_World",
                "JereKuusela-Server_devcommands",
                "HugotheDwarf-Shapekeys_and_More",
                "HugotheDwarf-More_and_Modified_Player_Cloth_Colliders",
                "HS-HS_FancierConsole",
                "Goldenrevolver-Quick_Stack_Store_Sort_Trash_Restock",
                "TastyChickenLegs-AutomaticFuel",
                "vaffle1-FPSPlus",
                "UpdatedMods-SkToolbox",
                "ZenDragon-Zen_ModLib",
                "ZenDragon-ZenUI",
                "zamboni-Gungnir"
            ],
            "🗑️ Quality of Life": [
                "virtuaCode-TrashItems",
                "VegettaPT-No_Food_Degradation"
            ],
            "🔧 Framework & Utility": [
                "denikson-BepInExPack_Valheim",
                "ValheimModding-Jotunn",
                "ValheimModding-HookGenPatcher",
                "ValheimModding-JsonDotNET",
                "ValheimModding-YamlDotNet",
                "DrakeMods-ServerSync",
                "CATALYSTC-AutoHookGenPatcher_by_Hamunii_Valheim_Publish",
                "CATALYSTC-Hamunii_Detour_Context_Dispose_Fix_Valheim_Publish",
                "Azumatt-SaveCrossbowState",
                "Azumatt-FactionAssigner",
                "Azumatt-PetPantry",
                "Azumatt-TrueInstantLootDrop",
                "Azumatt-AzuCraftyBoxes",
                "ASharpPen-Custom_Raids",
                "ASharpPen-Spawn_That",
                "ASharpPen-Drop_That",
                "ASharpPen-This_Goes_Here"
            ]
        }
    
    def load_mod_data(self):
        """Load mod data from cache and configuration"""
        # Load from mods.yml
        mods_file = self.valheim_path / "profiles" / "Dogeheim_Player" / "mods.yml"
        if mods_file.exists():
            try:
                with open(mods_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                for mod_data in data:
                    mod_name = mod_data.get("name", "")
                    if mod_name:
                        # Determine category
                        category = self.get_mod_category(mod_name)
                        
                        mod_info = ModInfo(
                            name=mod_name,
                            display_name=mod_data.get("displayName", mod_name),
                            version=mod_data.get("version", "Unknown"),
                            description=mod_data.get("description", ""),
                            author=mod_data.get("author", ""),
                            category=category,
                            icon_path=mod_data.get("icon", ""),
                            website_url=mod_data.get("websiteUrl", ""),
                            status=mod_data.get("status", "Unknown"),
                            enabled=mod_data.get("enabled", True)
                        )
                        
                        self.mods[mod_name] = mod_info
                        
                        # Load icon if available
                        if mod_info.icon_path and os.path.exists(mod_info.icon_path):
                            self.load_mod_icon(mod_name, mod_info.icon_path)
                
                print(f"Loaded {len(self.mods)} mods from configuration")
            except Exception as e:
                print(f"Error loading mod data: {e}")
    
    def get_mod_category(self, mod_name: str) -> str:
        """Get the category for a mod based on its name"""
        for category, mods in self.mod_categories.items():
            for mod in mods:
                if mod.lower() in mod_name.lower():
                    return category
        return "🔧 Framework & Utility"  # Default category
    
    def load_mod_icon(self, mod_name: str, icon_path: str):
        """Load and cache a mod icon"""
        try:
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
                image = image.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.mod_icons[mod_name] = photo
        except Exception as e:
            print(f"Error loading icon for {mod_name}: {e}")
    
    def get_mod_icon(self, mod_name: str) -> Optional[ImageTk.PhotoImage]:
        """Get the icon for a mod"""
        return self.mod_icons.get(mod_name)
    
    def scan_cache_for_mods(self):
        """Scan the cache directory for additional mods"""
        if not self.cache_path.exists():
            return
        
        for mod_dir in self.cache_path.iterdir():
            if mod_dir.is_dir():
                # Look for manifest.json
                manifest_file = mod_dir / "manifest.json"
                if manifest_file.exists():
                    try:
                        with open(manifest_file, 'r', encoding='utf-8') as f:
                            manifest = json.load(f)
                        
                        mod_name = manifest.get("name", mod_dir.name)
                        if mod_name not in self.mods:
                            # Look for icon
                            icon_path = ""
                            for icon_file in mod_dir.glob("*.png"):
                                icon_path = str(icon_file)
                                break
                            
                            mod_info = ModInfo(
                                name=mod_name,
                                display_name=manifest.get("displayName", mod_name),
                                version=manifest.get("version", "Unknown"),
                                description=manifest.get("description", ""),
                                author=manifest.get("author", ""),
                                category=self.get_mod_category(mod_name),
                                icon_path=icon_path,
                                website_url=manifest.get("website_url", ""),
                                status="Cached",
                                enabled=False
                            )
                            
                            self.mods[mod_name] = mod_info
                            
                            if icon_path:
                                self.load_mod_icon(mod_name, icon_path)
                    except Exception as e:
                        print(f"Error loading manifest for {mod_dir.name}: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about mods and loot tables"""
        # Mod statistics
        mod_stats = {
            "total_mods": len(self.mods),
            "enabled_mods": len([m for m in self.mods.values() if m.enabled]),
            "categories": {}
        }
        
        for mod in self.mods.values():
            if mod.category not in mod_stats["categories"]:
                mod_stats["categories"][mod.category] = 0
            mod_stats["categories"][mod.category] += 1
        
        # Loot statistics
        loot_stats = self.loot_manager.get_statistics()
        
        return {
            "mods": mod_stats,
            "loot": loot_stats
        }
    
    def create_backup(self):
        """Create a backup of all configuration files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_path / f"backup_{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        # Backup mod configuration
        mods_file = self.valheim_path / "profiles" / "Dogeheim_Player" / "mods.yml"
        if mods_file.exists():
            shutil.copy2(mods_file, backup_dir / "mods.yml")
        
        # Backup centralized data
        centralized_file = self.config_path / "centralized_loot_tables.json"
        if centralized_file.exists():
            shutil.copy2(centralized_file, backup_dir / "centralized_loot_tables.json")
        
        # Backup mod configuration files
        config_files = [
            "warpalicious.More_World_Locations_LootLists.yml",
            "ItemConfig_Base.yml",
            "drop_that.character_drop.cfg",
            "drop_that.drop_table.cfg"
        ]
        
        for file_name in config_files:
            source_file = self.config_path / file_name
            if source_file.exists():
                shutil.copy2(source_file, backup_dir / file_name)
        
        # Backup EpicLoot directory
        epicloot_source = self.config_path / "EpicLoot"
        if epicloot_source.exists():
            shutil.copytree(epicloot_source, backup_dir / "EpicLoot")
        
        print(f"Backup created at {backup_dir}")
        return backup_dir

class CentralizedModManagerGUI:
    """GUI for the centralized mod manager"""
    
    def __init__(self, manager: CentralizedModManager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Centralized Mod Manager")
        self.root.geometry("1400x900")
        
        # Configure style
        self.setup_style()
        
        self.setup_ui()
    
    def setup_style(self):
        """Setup the GUI style"""
        style = ttk.Style()
        
        # Try to use a modern theme
        try:
            style.theme_use("vista")
        except:
            try:
                style.theme_use("clam")
            except:
                style.theme_use("default")
        
        # Configure treeview style
        try:
            style.configure("Treeview", rowheight=40)
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        except:
            pass
    
    def setup_ui(self):
        """Setup the main UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="Scan Cache", 
                  command=self.scan_cache).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Import Loot Tables", 
                  command=self.import_loot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Export Loot Tables", 
                  command=self.export_loot).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Create Backup", 
                  command=self.create_backup).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Show Statistics", 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=(0, 5))
        
        # Notebook for different views
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Mods tab
        self.setup_mods_tab()
        
        # Loot Tables tab
        self.setup_loot_tables_tab()
        
        # Items tab
        self.setup_items_tab()
        
        # Sources tab
        self.setup_sources_tab()
        
        # Refresh data
        self.refresh_data()
    
    def setup_mods_tab(self):
        """Setup the mods tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Mods")
        
        # Search and filter frame
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT)
        self.mod_search_var = tk.StringVar()
        self.mod_search_var.trace('w', self.filter_mods)
        ttk.Entry(filter_frame, textvariable=self.mod_search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar()
        self.category_var.set("All Categories")
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, state="readonly")
        self.category_combo.pack(side=tk.LEFT, padx=(5, 0))
        self.category_combo.bind("<<ComboboxSelected>>", self.filter_mods)
        
        # Treeview
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Icon", "Name", "Version", "Category", "Status", "Description")
        self.mod_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.mod_tree.heading("Icon", text="")
        self.mod_tree.column("Icon", width=40, minwidth=40)
        
        self.mod_tree.heading("Name", text="Name", command=lambda: self.sort_mod_tree("Name"))
        self.mod_tree.column("Name", width=200, minwidth=150)
        
        self.mod_tree.heading("Version", text="Version", command=lambda: self.sort_mod_tree("Version"))
        self.mod_tree.column("Version", width=100, minwidth=80)
        
        self.mod_tree.heading("Category", text="Category", command=lambda: self.sort_mod_tree("Category"))
        self.mod_tree.column("Category", width=150, minwidth=120)
        
        self.mod_tree.heading("Status", text="Status", command=lambda: self.sort_mod_tree("Status"))
        self.mod_tree.column("Status", width=100, minwidth=80)
        
        self.mod_tree.heading("Description", text="Description")
        self.mod_tree.column("Description", width=300, minwidth=200)
        
        # Scrollbars
        mod_scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.mod_tree.yview)
        mod_scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.mod_tree.xview)
        self.mod_tree.configure(yscrollcommand=mod_scrollbar_y.set, xscrollcommand=mod_scrollbar_x.set)
        
        # Grid layout
        self.mod_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        mod_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        mod_scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Double-click binding
        self.mod_tree.bind("<Double-1>", self.show_mod_details)
    
    def setup_loot_tables_tab(self):
        """Setup the loot tables tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Loot Tables")
        
        # Search frame
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.table_search_var = tk.StringVar()
        self.table_search_var.trace('w', self.filter_tables)
        ttk.Entry(search_frame, textvariable=self.table_search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Treeview
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Name", "Source", "Items", "Description")
        self.table_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.table_tree.heading(col, text=col, command=lambda c=col: self.sort_table_tree(c))
            self.table_tree.column(col, width=150)
        
        # Scrollbars
        table_scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.table_tree.yview)
        table_scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.table_tree.xview)
        self.table_tree.configure(yscrollcommand=table_scrollbar_y.set, xscrollcommand=table_scrollbar_x.set)
        
        # Grid layout
        self.table_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        table_scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Double-click binding
        self.table_tree.bind("<Double-1>", self.show_table_details)
    
    def setup_items_tab(self):
        """Setup the items tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Items")
        
        # Search frame
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.item_search_var = tk.StringVar()
        self.item_search_var.trace('w', self.filter_items)
        ttk.Entry(search_frame, textvariable=self.item_search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Treeview
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Item", "Tables", "Sources")
        self.item_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.item_tree.heading(col, text=col, command=lambda c=col: self.sort_item_tree(c))
            self.item_tree.column(col, width=200)
        
        # Scrollbars
        item_scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.item_tree.yview)
        item_scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.item_tree.xview)
        self.item_tree.configure(yscrollcommand=item_scrollbar_y.set, xscrollcommand=item_scrollbar_x.set)
        
        # Grid layout
        self.item_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        item_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        item_scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Double-click binding
        self.item_tree.bind("<Double-1>", self.show_item_details)
    
    def setup_sources_tab(self):
        """Setup the sources tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Sources")
        
        # Treeview
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Source", "Tables", "Items")
        self.source_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        for col in columns:
            self.source_tree.heading(col, text=col, command=lambda c=col: self.sort_source_tree(c))
            self.source_tree.column(col, width=200)
        
        # Scrollbars
        source_scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.source_tree.yview)
        source_scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.source_tree.xview)
        self.source_tree.configure(yscrollcommand=source_scrollbar_y.set, xscrollcommand=source_scrollbar_x.set)
        
        # Grid layout
        self.source_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        source_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        source_scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
    
    def refresh_data(self):
        """Refresh all data displays"""
        self.refresh_mod_tree()
        self.refresh_table_tree()
        self.refresh_item_tree()
        self.refresh_source_tree()
        
        # Update category combo
        categories = ["All Categories"] + list(self.manager.mod_categories.keys())
        self.category_combo['values'] = categories
    
    def refresh_mod_tree(self):
        """Refresh the mods treeview"""
        # Clear existing items
        for item in self.mod_tree.get_children():
            self.mod_tree.delete(item)
        
        # Add mods
        for mod_name, mod in self.manager.mods.items():
            icon = self.manager.get_mod_icon(mod_name)
            icon_text = "📦" if icon else "📄"
            
            self.mod_tree.insert("", "end", values=(
                icon_text,
                mod.display_name,
                mod.version,
                mod.category,
                mod.status,
                mod.description[:50] + "..." if len(mod.description) > 50 else mod.description
            ))
    
    def refresh_table_tree(self):
        """Refresh the loot tables treeview"""
        # Clear existing items
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)
        
        # Add loot tables
        for table_name, table in self.manager.loot_manager.loot_tables.items():
            self.table_tree.insert("", "end", values=(
                table.name,
                table.source,
                len(table.items),
                table.description[:50] + "..." if len(table.description) > 50 else table.description
            ))
    
    def refresh_item_tree(self):
        """Refresh the items treeview"""
        # Clear existing items
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        
        # Add items
        for item_name, table_names in self.manager.loot_manager.item_registry.items():
            sources = set()
            for table_name in table_names:
                if table_name in self.manager.loot_manager.loot_tables:
                    sources.add(self.manager.loot_manager.loot_tables[table_name].source)
            
            self.item_tree.insert("", "end", values=(
                item_name,
                len(table_names),
                ", ".join(sorted(sources))
            ))
    
    def refresh_source_tree(self):
        """Refresh the sources treeview"""
        # Clear existing items
        for item in self.source_tree.get_children():
            self.source_tree.delete(item)
        
        # Group by source
        source_stats = {}
        for table in self.manager.loot_manager.loot_tables.values():
            if table.source not in source_stats:
                source_stats[table.source] = {"tables": 0, "items": set()}
            source_stats[table.source]["tables"] += 1
            for item in table.items:
                source_stats[table.source]["items"].add(item.item_name)
        
        # Add sources
        for source, stats in source_stats.items():
            self.source_tree.insert("", "end", values=(
                source,
                stats["tables"],
                len(stats["items"])
            ))
    
    def filter_mods(self, *args):
        """Filter mods based on search and category"""
        search_term = self.mod_search_var.get().lower()
        selected_category = self.category_var.get()
        
        # Clear existing items
        for item in self.mod_tree.get_children():
            self.mod_tree.delete(item)
        
        # Add filtered mods
        for mod_name, mod in self.manager.mods.items():
            # Check category filter
            if selected_category != "All Categories" and mod.category != selected_category:
                continue
            
            # Check search filter
            if (search_term in mod.display_name.lower() or 
                search_term in mod.description.lower() or
                search_term in mod.category.lower()):
                
                icon = self.manager.get_mod_icon(mod_name)
                icon_text = "📦" if icon else "📄"
                
                self.mod_tree.insert("", "end", values=(
                    icon_text,
                    mod.display_name,
                    mod.version,
                    mod.category,
                    mod.status,
                    mod.description[:50] + "..." if len(mod.description) > 50 else mod.description
                ))
    
    def filter_tables(self, *args):
        """Filter loot tables based on search"""
        search_term = self.table_search_var.get().lower()
        
        # Clear existing items
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)
        
        # Add filtered loot tables
        for table_name, table in self.manager.loot_manager.loot_tables.items():
            if (search_term in table.name.lower() or 
                search_term in table.source.lower() or 
                search_term in table.description.lower()):
                self.table_tree.insert("", "end", values=(
                    table.name,
                    table.source,
                    len(table.items),
                    table.description[:50] + "..." if len(table.description) > 50 else table.description
                ))
    
    def filter_items(self, *args):
        """Filter items based on search"""
        search_term = self.item_search_var.get().lower()
        
        # Clear existing items
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        
        # Add filtered items
        for item_name, table_names in self.manager.loot_manager.item_registry.items():
            if search_term in item_name.lower():
                sources = set()
                for table_name in table_names:
                    if table_name in self.manager.loot_manager.loot_tables:
                        sources.add(self.manager.loot_manager.loot_tables[table_name].source)
                
                self.item_tree.insert("", "end", values=(
                    item_name,
                    len(table_names),
                    ", ".join(sorted(sources))
                ))
    
    def sort_mod_tree(self, column):
        """Sort the mod treeview by column"""
        # Implementation would sort the treeview items
        pass
    
    def sort_table_tree(self, column):
        """Sort the table treeview by column"""
        # Implementation would sort the treeview items
        pass
    
    def sort_item_tree(self, column):
        """Sort the item treeview by column"""
        # Implementation would sort the treeview items
        pass
    
    def sort_source_tree(self, column):
        """Sort the source treeview by column"""
        # Implementation would sort the treeview items
        pass
    
    def show_mod_details(self, event):
        """Show detailed information about a mod"""
        selection = self.mod_tree.selection()
        if not selection:
            return
        
        item = self.mod_tree.item(selection[0])
        mod_name = item['values'][1]  # Name is in column 1
        
        # Find the mod by display name
        for name, mod in self.manager.mods.items():
            if mod.display_name == mod_name:
                self.show_mod_details_window(mod)
                break
    
    def show_table_details(self, event):
        """Show detailed information about a loot table"""
        selection = self.table_tree.selection()
        if not selection:
            return
        
        item = self.table_tree.item(selection[0])
        table_name = item['values'][0]
        
        if table_name in self.manager.loot_manager.loot_tables:
            table = self.manager.loot_manager.loot_tables[table_name]
            self.show_table_details_window(table)
    
    def show_item_details(self, event):
        """Show detailed information about an item"""
        selection = self.item_tree.selection()
        if not selection:
            return
        
        item = self.item_tree.item(selection[0])
        item_name = item['values'][0]
        
        if item_name in self.manager.loot_manager.item_registry:
            self.show_item_details_window(item_name)
    
    def show_mod_details_window(self, mod: ModInfo):
        """Show a window with detailed mod information"""
        window = tk.Toplevel(self.root)
        window.title(f"Mod Details: {mod.display_name}")
        window.geometry("600x500")
        
        # Create text widget
        text_widget = tk.Text(window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add content
        content = f"""Mod: {mod.display_name}
Name: {mod.name}
Version: {mod.version}
Author: {mod.author}
Category: {mod.category}
Status: {mod.status}
Enabled: {mod.enabled}

Description:
{mod.description}

Website: {mod.website_url}
Icon Path: {mod.icon_path}

Dependencies: {', '.join(mod.dependencies) if mod.dependencies else 'None'}
Conflicts: {', '.join(mod.conflicts) if mod.conflicts else 'None'}
"""
        
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
    
    def show_table_details_window(self, table: LootTable):
        """Show a window with detailed table information"""
        window = tk.Toplevel(self.root)
        window.title(f"Loot Table Details: {table.name}")
        window.geometry("600x400")
        
        # Create text widget
        text_widget = tk.Text(window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add content
        content = f"""Loot Table: {table.name}
Source: {table.source}
File: {table.source_file}
Description: {table.description}

Items ({len(table.items)}):
"""
        
        for i, item in enumerate(table.items, 1):
            content += f"\n{i}. {item.item_name}"
            content += f"\n   Stack: {item.stack_min}-{item.stack_max}"
            content += f"\n   Weight: {item.weight}"
            if item.chance != 1.0:
                content += f"\n   Chance: {item.chance}"
            if item.rarity:
                content += f"\n   Rarity: {item.rarity}"
            content += "\n"
        
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
    
    def show_item_details_window(self, item_name: str):
        """Show a window with detailed item information"""
        window = tk.Toplevel(self.root)
        window.title(f"Item Details: {item_name}")
        window.geometry("600x400")
        
        # Create text widget
        text_widget = tk.Text(window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add content
        content = f"""Item: {item_name}
Appears in {len(self.manager.loot_manager.item_registry[item_name])} loot tables:

"""
        
        for table_name in self.manager.loot_manager.item_registry[item_name]:
            if table_name in self.manager.loot_manager.loot_tables:
                table = self.manager.loot_manager.loot_tables[table_name]
                content += f"• {table.name} ({table.source})\n"
        
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
    
    def scan_cache(self):
        """Scan cache for mods"""
        def scan_thread():
            self.manager.scan_cache_for_mods()
            self.root.after(0, self.refresh_data)
            self.root.after(0, lambda: messagebox.showinfo("Scan Complete", 
                f"Found {len(self.manager.mods)} mods in cache"))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def import_loot(self):
        """Import loot tables"""
        def import_thread():
            self.manager.loot_manager.import_from_all_sources()
            self.root.after(0, self.refresh_data)
            self.root.after(0, lambda: messagebox.showinfo("Import Complete", 
                f"Imported {len(self.manager.loot_manager.loot_tables)} loot tables"))
        
        threading.Thread(target=import_thread, daemon=True).start()
    
    def export_loot(self):
        """Export loot tables"""
        def export_thread():
            self.manager.loot_manager.export_to_original_formats()
            self.root.after(0, lambda: messagebox.showinfo("Export Complete", 
                "Exported all loot tables to original formats"))
        
        threading.Thread(target=export_thread, daemon=True).start()
    
    def create_backup(self):
        """Create a backup"""
        def backup_thread():
            backup_dir = self.manager.create_backup()
            self.root.after(0, lambda: messagebox.showinfo("Backup Complete", 
                f"Backup created at {backup_dir}"))
        
        threading.Thread(target=backup_thread, daemon=True).start()
    
    def show_statistics(self):
        """Show statistics window"""
        stats = self.manager.get_statistics()
        
        window = tk.Toplevel(self.root)
        window.title("Mod Manager Statistics")
        window.geometry("600x500")
        
        # Create text widget
        text_widget = tk.Text(window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add content
        content = f"""Mod Manager Statistics

MODS:
Total Mods: {stats['mods']['total_mods']}
Enabled Mods: {stats['mods']['enabled_mods']}

Mod Categories:
"""
        
        for category, count in stats['mods']['categories'].items():
            content += f"• {category}: {count} mods\n"
        
        content += f"""

LOOT TABLES:
Total Loot Tables: {stats['loot']['total_tables']}
Total Unique Items: {stats['loot']['total_items']}

Loot Sources:
"""
        
        for source, count in stats['loot']['sources'].items():
            content += f"• {source}: {count} tables\n"
        
        content += "\nMost Common Items:\n"
        for item_data in stats['loot']['most_common_items']:
            content += f"• {item_data['item']}: {item_data['count']} tables\n"
        
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    manager = CentralizedModManager()
    gui = CentralizedModManagerGUI(manager)
    gui.run()

if __name__ == "__main__":
    main()
