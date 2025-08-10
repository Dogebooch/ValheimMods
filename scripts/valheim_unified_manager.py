#!/usr/bin/env python3
"""
Valheim Unified Mod Manager
A comprehensive tool for managing Valheim mods, items, and loot tables.
Combines mod management, item scanning, and loot table management into one application.
"""

import os
import sys
import re
import json
import yaml
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Set, Optional
from PIL import Image, ImageTk
import glob

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

@dataclass
class ItemInfo:
    """Information about an item"""
    name: str
    prefab_id: str
    mod_source: str
    category: str
    description: str = ""
    icon_path: str = ""
    translation_key: str = ""

@dataclass
class LootItem:
    """Information about a loot item"""
    name: str
    stack_size: int = 1
    weight: float = 1.0
    rarity: str = "common"
    source: str = ""

@dataclass
class LootTable:
    """Information about a loot table"""
    name: str
    items: List[LootItem]
    source: str = ""
    category: str = ""

@dataclass
class ModInfo:
    """Information about a mod"""
    name: str
    version: str
    category: str
    description: str = ""
    icon_path: str = ""

class ComprehensiveItemScanner:
    """Scans multiple sources to extract all items from mods"""
    
    def __init__(self, valheim_path: str = "Valheim"):
        self.valheim_path = Path(valheim_path)
        self.cache_path = self.valheim_path / "cache"
        self.vnei_path = self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "plugins" / "VNEI"
        self.cached_icons_path = Path("Valheim_Help_Docs/Valheim_PlayerWorldData/Jotunn/CachedIcons")
        
        self.items: Dict[str, ItemInfo] = {}
        self.mod_categories = {
            "armor": ["Therzie-Armory", "HugotheDwarf-Hugos_Armory", "Southsil-SouthsilArmor", "Fantu-Sages_Vault"],
            "weapons": ["Therzie-Warfare", "Therzie-WarfareFireAndIce", "Shawesome-Shawesomes_Divine_Armaments"],
            "magic": ["blacks7ar-MagicRevamp", "Therzie-Wizardry", "Soloredis-RtDMagic"],
            "loot": ["RandyKnapp-EpicLoot", "JewelHeim-RelicHeim", "KGvalheim-Valheim_Enchantment_System"],
            "food": ["blacks7ar-CookingAdditions", "OdinPlus-PotionPlus", "Smoothbrain-Cooking"],
            "farming": ["Advize-PlantEverything", "Smoothbrain-Farming", "Smoothbrain-Foraging"],
            "building": ["warpalicious", "OdinPlus-OdinArchitect", "blacks7ar-FineWoodBuildPieces"],
            "monsters": ["Therzie-Monstrum", "Therzie-MonstrumDeepNorth", "Horem-MushroomMonsters"],
            "utility": ["Smoothbrain-Backpacks", "Vapok-AdventureBackpacks", "Goldenrevolver-Quick_Stack_Store_Sort_Trash_Restock"]
        }

    def scan_cached_icons(self) -> None:
        """Extract item information from cached icon filenames"""
        if not self.cached_icons_path.exists():
            return
            
        for icon_file in self.cached_icons_path.glob("*.png"):
            filename = icon_file.stem
            parts = filename.split("-")
            if len(parts) >= 3:
                item_name = parts[0]
                mod_name = parts[1]
                version = parts[2]
                
                clean_item_name = self.clean_item_name(item_name)
                item_id = f"{item_name}_{mod_name}"
                
                if item_id not in self.items:
                    self.items[item_id] = ItemInfo(
                        name=clean_item_name,
                        prefab_id=item_name,
                        mod_source=mod_name,
                        category=self.get_mod_category(mod_name),
                        icon_path=str(icon_file)
                    )

    def clean_item_name(self, item_name: str) -> str:
        """Clean up item names by removing common prefixes"""
        prefixes_to_remove = [
            "Pickable_", "BMR_", "MWL_", "BFD_", "CD_kit_", "Spawner_",
            "Warp_", "loot_drop_", "CaveDeepNorth_", "DeepNorth_"
        ]
        
        clean_name = item_name
        for prefix in prefixes_to_remove:
            if clean_name.startswith(prefix):
                clean_name = clean_name[len(prefix):]
                break
                
        clean_name = clean_name.replace("_", " ").title()
        return clean_name

    def scan_translation_files(self) -> None:
        """Extract item information from translation files"""
        for mod_dir in self.cache_path.iterdir():
            if not mod_dir.is_dir():
                continue
                
            mod_name = mod_dir.name
            config_path = mod_dir / "config"
            if not config_path.exists():
                continue
                
            translation_files = list(config_path.rglob("*.yml")) + list(config_path.rglob("*.yaml"))
            
            for trans_file in translation_files:
                try:
                    with open(trans_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.extract_items_from_translations(content, mod_name, trans_file)
                except Exception as e:
                    pass

    def extract_items_from_translations(self, content: str, mod_name: str, file_path: Path) -> int:
        """Extract item information from translation content"""
        items_found = 0
        pattern = r'([a-zA-Z_]+)_TW\s*:\s*"([^"]+)"'
        matches = re.findall(pattern, content)
        
        for item_id, display_name in matches:
            if any(skip in item_id.lower() for skip in ['piece_', 'topic_', 'text_', 'description_', 'buff_', 'set_']):
                continue
                
            unique_id = f"{item_id}_{mod_name}"
            
            if unique_id not in self.items:
                self.items[unique_id] = ItemInfo(
                    name=display_name,
                    prefab_id=item_id,
                    mod_source=mod_name,
                    category=self.get_mod_category(mod_name),
                    translation_key=f"{item_id}_TW"
                )
                items_found += 1
            else:
                self.items[unique_id].name = display_name
                self.items[unique_id].translation_key = f"{item_id}_TW"
                items_found += 1
                
        return items_found

    def get_mod_category(self, mod_name: str) -> str:
        """Determine the category of a mod based on its name"""
        if mod_name.replace('.', '').isdigit():
            return "vanilla"
            
        for category, mods in self.mod_categories.items():
            for mod in mods:
                if mod.lower() in mod_name.lower():
                    return category
                    
        mod_lower = mod_name.lower()
        if any(word in mod_lower for word in ['armory', 'armor']):
            return "armor"
        elif any(word in mod_lower for word in ['warfare', 'weapon', 'sword', 'axe']):
            return "weapons"
        elif any(word in mod_lower for word in ['magic', 'wizard', 'spell']):
            return "magic"
        elif any(word in mod_lower for word in ['loot', 'epic', 'relic']):
            return "loot"
        elif any(word in mod_lower for word in ['cooking', 'food', 'potion']):
            return "food"
        elif any(word in mod_lower for word in ['plant', 'farm', 'forage']):
            return "farming"
        elif any(word in mod_lower for word in ['warpalicious', 'architect', 'build']):
            return "building"
        elif any(word in mod_lower for word in ['monstrum', 'monster', 'mushroom']):
            return "monsters"
        elif any(word in mod_lower for word in ['backpack', 'utility', 'tool']):
            return "utility"
            
        return "other"

    def scan_all_sources(self) -> Dict[str, ItemInfo]:
        """Scan all sources and return comprehensive item database"""
        self.scan_cached_icons()
        self.scan_translation_files()
        return self.items

class CentralizedLootManager:
    """Manages loot tables from various mod sources"""
    
    def __init__(self, valheim_path: str = "Valheim"):
        self.valheim_path = Path(valheim_path)
        self.config_path = self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "config"
        self.backup_path = Path("backups")
        self.backup_path.mkdir(exist_ok=True)
        
        self.loot_tables: Dict[str, LootTable] = {}
        self.item_registry: Dict[str, List[str]] = {}  # item_name -> [table_names]
        self.centralized_file = Path("centralized_loot_tables.json")

    def import_from_all_sources(self) -> None:
        """Import loot tables from all supported sources"""
        self._import_warpalicious()
        self._import_epicloot()
        self._import_cllc()
        self._import_drop_that()
        self._rebuild_item_registry()

    def _import_warpalicious(self) -> None:
        """Import from Warpalicious More World Locations"""
        config_file = self.config_path / "warpalicious.More_World_Locations_LootLists.yml"
        if not config_file.exists():
            return
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if isinstance(data, dict) and 'LootPools' in data:
                for pool_name, pool_data in data['LootPools'].items():
                    items = []
                    if 'Items' in pool_data:
                        for item_data in pool_data['Items']:
                            if isinstance(item_data, dict):
                                item = LootItem(
                                    name=item_data.get('Name', ''),
                                    stack_size=item_data.get('StackSize', 1),
                                    weight=item_data.get('Weight', 1.0),
                                    source="Warpalicious"
                                )
                                items.append(item)
                    
                    if items:
                        self.loot_tables[f"warpalicious_{pool_name}"] = LootTable(
                            name=pool_name,
                            items=items,
                            source="Warpalicious",
                            category="world_locations"
                        )
        except Exception as e:
            print(f"Error importing Warpalicious loot: {e}")

    def _import_epicloot(self) -> None:
        """Import from EpicLoot patches"""
        epicloot_path = self.config_path / "EpicLoot" / "patches" / "RelicHeimPatches"
        if not epicloot_path.exists():
            return
            
        for json_file in epicloot_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                table_name = f"epicloot_{json_file.stem}"
                items = []
                
                if isinstance(data, dict) and 'Items' in data:
                    for item_data in data['Items']:
                        if isinstance(item_data, dict):
                            item = LootItem(
                                name=item_data.get('Name', ''),
                                rarity=item_data.get('Rarity', 'common'),
                                source="EpicLoot"
                            )
                            items.append(item)
                
                if items:
                    self.loot_tables[table_name] = LootTable(
                        name=json_file.stem,
                        items=items,
                        source="EpicLoot",
                        category="epic_loot"
                    )
            except Exception as e:
                print(f"Error importing EpicLoot file {json_file}: {e}")

    def _import_cllc(self) -> None:
        """Import from Creature Level & Loot Control"""
        config_file = self.config_path / "ItemConfig_Base.yml"
        if not config_file.exists():
            return
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if isinstance(data, dict) and 'ItemGroups' in data:
                for group_name, group_data in data['ItemGroups'].items():
                    items = []
                    if 'Items' in group_data:
                        for item_name in group_data['Items']:
                            item = LootItem(
                                name=item_name,
                                source="CLLC"
                            )
                            items.append(item)
                    
                    if items:
                        self.loot_tables[f"cllc_{group_name}"] = LootTable(
                            name=group_name,
                            items=items,
                            source="CLLC",
                            category="creature_drops"
                        )
        except Exception as e:
            print(f"Error importing CLLC loot: {e}")

    def _import_drop_that(self) -> None:
        """Import from Drop That mod"""
        config_file = self.config_path / "drop_that.character_drop.cfg"
        if not config_file.exists():
            return
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse Drop That config format
            pattern = r'\[([^\]]+)\]\s*([^[]+)'
            matches = re.findall(pattern, content, re.DOTALL)
            
            for creature_name, drop_data in matches:
                items = []
                lines = drop_data.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(',')
                        if len(parts) >= 1:
                            item_name = parts[0].strip()
                            item = LootItem(
                                name=item_name,
                                source="Drop That"
                            )
                            items.append(item)
                
                if items:
                    self.loot_tables[f"dropthat_{creature_name}"] = LootTable(
                        name=creature_name,
                        items=items,
                        source="Drop That",
                        category="creature_drops"
                    )
        except Exception as e:
            print(f"Error importing Drop That loot: {e}")

    def _rebuild_item_registry(self) -> None:
        """Rebuild the item-to-table mapping"""
        self.item_registry.clear()
        for table_name, table in self.loot_tables.items():
            for item in table.items:
                if item.name not in self.item_registry:
                    self.item_registry[item.name] = []
                self.item_registry[item.name].append(table_name)

    def save_centralized_data(self) -> None:
        """Save the unified loot data to JSON"""
        data = {
            'loot_tables': {name: asdict(table) for name, table in self.loot_tables.items()},
            'item_registry': self.item_registry
        }
        
        with open(self.centralized_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_centralized_data(self) -> None:
        """Load the unified loot data from JSON"""
        if not self.centralized_file.exists():
            return
            
        try:
            with open(self.centralized_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'loot_tables' in data:
                self.loot_tables.clear()
                for name, table_data in data['loot_tables'].items():
                    items = [LootItem(**item_data) for item_data in table_data['items']]
                    self.loot_tables[name] = LootTable(
                        name=table_data['name'],
                        items=items,
                        source=table_data.get('source', ''),
                        category=table_data.get('category', '')
                    )
                    
            if 'item_registry' in data:
                self.item_registry = data['item_registry']
        except Exception as e:
            print(f"Error loading centralized data: {e}")

class ValheimUnifiedManager:
    """Main unified manager class"""
    
    def __init__(self, valheim_path: str = "Valheim"):
        self.valheim_path = Path(valheim_path)
        self.item_scanner = ComprehensiveItemScanner(valheim_path)
        self.loot_manager = CentralizedLootManager(valheim_path)
        
        self.items: Dict[str, ItemInfo] = {}
        self.mods: Dict[str, ModInfo] = {}
        self.mod_categories = {}
        
        # Load data
        self.load_mod_categories()
        self.load_mod_data()
        self.loot_manager.load_centralized_data()

    def load_mod_categories(self) -> None:
        """Load mod categories from the summary file"""
        summary_file = Path("Valheim_Help_Docs/Files for GPT/Valheim_Content_Mods_Summary.md")
        if not summary_file.exists():
            return
            
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse categories from markdown
            category_pattern = r'### \*\*([^*]+)\*\*'
            categories = re.findall(category_pattern, content)
            
            for category in categories:
                self.mod_categories[category.lower().replace(' ', '_')] = category
        except Exception as e:
            print(f"Error loading mod categories: {e}")

    def load_mod_data(self) -> None:
        """Load mod information from mods.yml"""
        mods_file = self.valheim_path / "profiles" / "Dogeheim_Player" / "mods.yml"
        if not mods_file.exists():
            return
            
        try:
            with open(mods_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if isinstance(data, dict) and 'mods' in data:
                for mod_data in data['mods']:
                    if isinstance(mod_data, dict):
                        mod_name = mod_data.get('name', '')
                        mod_info = ModInfo(
                            name=mod_name,
                            version=mod_data.get('version', 'unknown'),
                            category=self.get_mod_category(mod_name),
                            description=mod_data.get('description', '')
                        )
                        self.mods[mod_name] = mod_info
        except Exception as e:
            print(f"Error loading mod data: {e}")

    def get_mod_category(self, mod_name: str) -> str:
        """Get category for a mod"""
        for category in self.mod_categories:
            if category.lower() in mod_name.lower():
                return self.mod_categories[category]
        return "Other"

    def scan_items(self) -> None:
        """Scan for all items"""
        self.items = self.item_scanner.scan_all_sources()

    def import_loot_tables(self) -> None:
        """Import loot tables from all sources"""
        self.loot_manager.import_from_all_sources()
        self.loot_manager.save_centralized_data()

    def get_statistics(self) -> Dict[str, any]:
        """Get comprehensive statistics"""
        stats = {
            "mods": {
                "total": len(self.mods),
                "by_category": {}
            },
            "items": {
                "total": len(self.items),
                "by_category": {},
                "with_icons": sum(1 for item in self.items.values() if item.icon_path),
                "with_translations": sum(1 for item in self.items.values() if item.translation_key)
            },
            "loot_tables": {
                "total": len(self.loot_manager.loot_tables),
                "by_source": {},
                "by_category": {}
            }
        }
        
        # Count mods by category
        for mod in self.mods.values():
            category = mod.category
            stats["mods"]["by_category"][category] = stats["mods"]["by_category"].get(category, 0) + 1
            
        # Count items by category
        for item in self.items.values():
            category = item.category
            stats["items"]["by_category"][category] = stats["items"]["by_category"].get(category, 0) + 1
            
        # Count loot tables by source and category
        for table in self.loot_manager.loot_tables.values():
            source = table.source
            category = table.category
            stats["loot_tables"]["by_source"][source] = stats["loot_tables"]["by_source"].get(source, 0) + 1
            stats["loot_tables"]["by_category"][category] = stats["loot_tables"]["by_category"].get(category, 0) + 1
            
        return stats

class ValheimUnifiedManagerGUI:
    """GUI for the unified mod manager"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Valheim Unified Mod Manager")
        self.root.geometry("1200x800")
        
        self.manager = ValheimUnifiedManager()
        self.icon_cache = {}
        
        self.setup_style()
        self.setup_ui()
        self.refresh_data()

    def setup_style(self):
        """Setup the GUI style"""
        style = ttk.Style()
        try:
            style.theme_use("vista")
        except:
            style.theme_use("default")
            
        # Configure Treeview
        try:
            style.configure("Treeview", rowheight=30)
            style.map("Treeview", background=[("selected", "#0078D7")])
        except:
            pass

    def setup_ui(self):
        """Setup the main UI"""
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Scan Items", command=self.scan_items).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Import Loot Tables", command=self.import_loot).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Statistics", command=self.show_statistics).pack(side=tk.LEFT, padx=2)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Setup tabs
        self.setup_mods_tab()
        self.setup_items_tab()
        self.setup_loot_tables_tab()
        self.setup_items_tab()

    def setup_mods_tab(self):
        """Setup the mods tab"""
        mods_frame = ttk.Frame(self.notebook)
        self.notebook.add(mods_frame, text="Mods")
        
        # Search and filter
        filter_frame = ttk.Frame(mods_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT)
        self.mod_search_var = tk.StringVar()
        self.mod_search_var.trace('w', lambda *args: self.filter_mods())
        ttk.Entry(filter_frame, textvariable=self.mod_search_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=(10, 0))
        self.mod_category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(filter_frame, textvariable=self.mod_category_var, 
                                     values=["All"] + list(self.manager.mod_categories.values()))
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_mods())
        
        # Mods treeview
        tree_frame = ttk.Frame(mods_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Name", "Version", "Category", "Description")
        self.mods_tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")
        
        for col in columns:
            self.mods_tree.heading(col, text=col, command=lambda c=col: self.sort_mod_tree(c))
            self.mods_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.mods_tree.yview)
        self.mods_tree.configure(yscrollcommand=scrollbar.set)
        
        self.mods_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.mods_tree.bind("<Double-1>", lambda e: self.show_mod_details())

    def setup_items_tab(self):
        """Setup the items tab"""
        items_frame = ttk.Frame(self.notebook)
        self.notebook.add(items_frame, text="Items")
        
        # Search and filter
        filter_frame = ttk.Frame(items_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT)
        self.item_search_var = tk.StringVar()
        self.item_search_var.trace('w', lambda *args: self.filter_items())
        ttk.Entry(filter_frame, textvariable=self.item_search_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=(10, 0))
        self.item_category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(filter_frame, textvariable=self.item_category_var, 
                                     values=["All", "vanilla", "armor", "weapons", "magic", "loot", "food", "farming", "building", "monsters", "utility", "other"])
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_items())
        
        # Items treeview
        tree_frame = ttk.Frame(items_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Name", "Prefab ID", "Mod Source", "Category", "Has Icon", "Has Translation")
        self.items_tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")
        
        for col in columns:
            self.items_tree.heading(col, text=col, command=lambda c=col: self.sort_item_tree(c))
            self.items_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.items_tree.bind("<Double-1>", lambda e: self.show_item_details())

    def setup_loot_tables_tab(self):
        """Setup the loot tables tab"""
        loot_frame = ttk.Frame(self.notebook)
        self.notebook.add(loot_frame, text="Loot Tables")
        
        # Search and filter
        filter_frame = ttk.Frame(loot_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT)
        self.loot_search_var = tk.StringVar()
        self.loot_search_var.trace('w', lambda *args: self.filter_loot_tables())
        ttk.Entry(filter_frame, textvariable=self.loot_search_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Source:").pack(side=tk.LEFT, padx=(10, 0))
        self.loot_source_var = tk.StringVar(value="All")
        source_combo = ttk.Combobox(filter_frame, textvariable=self.loot_source_var, 
                                   values=["All", "Warpalicious", "EpicLoot", "CLLC", "Drop That"])
        source_combo.pack(side=tk.LEFT, padx=5)
        source_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_loot_tables())
        
        # Loot tables treeview
        tree_frame = ttk.Frame(loot_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Name", "Source", "Category", "Item Count")
        self.loot_tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")
        
        for col in columns:
            self.loot_tree.heading(col, text=col, command=lambda c=col: self.sort_loot_tree(c))
            self.loot_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.loot_tree.yview)
        self.loot_tree.configure(yscrollcommand=scrollbar.set)
        
        self.loot_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.loot_tree.bind("<Double-1>", lambda e: self.show_loot_table_details())

    def refresh_data(self):
        """Refresh all data displays"""
        self.refresh_mod_tree()
        self.refresh_item_tree()
        self.refresh_loot_tree()

    def refresh_mod_tree(self):
        """Refresh the mods treeview"""
        for item in self.mods_tree.get_children():
            self.mods_tree.delete(item)
            
        for mod_name, mod_info in self.manager.mods.items():
            self.mods_tree.insert("", "end", values=(
                mod_info.name,
                mod_info.version,
                mod_info.category,
                mod_info.description
            ))

    def refresh_item_tree(self):
        """Refresh the items treeview"""
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
            
        for item_id, item_info in self.manager.items.items():
            self.items_tree.insert("", "end", values=(
                item_info.name,
                item_info.prefab_id,
                item_info.mod_source,
                item_info.category,
                "Yes" if item_info.icon_path else "No",
                "Yes" if item_info.translation_key else "No"
            ))

    def refresh_loot_tree(self):
        """Refresh the loot tables treeview"""
        for item in self.loot_tree.get_children():
            self.loot_tree.delete(item)
            
        for table_name, table in self.manager.loot_manager.loot_tables.items():
            self.loot_tree.insert("", "end", values=(
                table.name,
                table.source,
                table.category,
                len(table.items)
            ))

    def filter_mods(self):
        """Filter mods based on search and category"""
        search_term = self.mod_search_var.get().lower()
        category_filter = self.mod_category_var.get()
        
        for item in self.mods_tree.get_children():
            self.mods_tree.delete(item)
            
        for mod_name, mod_info in self.manager.mods.items():
            if search_term and search_term not in mod_info.name.lower():
                continue
            if category_filter != "All" and mod_info.category != category_filter:
                continue
                
            self.mods_tree.insert("", "end", values=(
                mod_info.name,
                mod_info.version,
                mod_info.category,
                mod_info.description
            ))

    def filter_items(self):
        """Filter items based on search and category"""
        search_term = self.item_search_var.get().lower()
        category_filter = self.item_category_var.get()
        
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
            
        for item_id, item_info in self.manager.items.items():
            if search_term and search_term not in item_info.name.lower():
                continue
            if category_filter != "All" and item_info.category != category_filter:
                continue
                
            self.items_tree.insert("", "end", values=(
                item_info.name,
                item_info.prefab_id,
                item_info.mod_source,
                item_info.category,
                "Yes" if item_info.icon_path else "No",
                "Yes" if item_info.translation_key else "No"
            ))

    def filter_loot_tables(self):
        """Filter loot tables based on search and source"""
        search_term = self.loot_search_var.get().lower()
        source_filter = self.loot_source_var.get()
        
        for item in self.loot_tree.get_children():
            self.loot_tree.delete(item)
            
        for table_name, table in self.manager.loot_manager.loot_tables.items():
            if search_term and search_term not in table.name.lower():
                continue
            if source_filter != "All" and table.source != source_filter:
                continue
                
            self.loot_tree.insert("", "end", values=(
                table.name,
                table.source,
                table.category,
                len(table.items)
            ))

    def scan_items(self):
        """Scan for items in a separate thread"""
        def scan():
            self.manager.scan_items()
            self.root.after(0, self.refresh_item_tree)
            self.root.after(0, lambda: messagebox.showinfo("Scan Complete", f"Found {len(self.manager.items)} items"))
            
        threading.Thread(target=scan, daemon=True).start()

    def import_loot(self):
        """Import loot tables in a separate thread"""
        def import_loot():
            self.manager.import_loot_tables()
            self.root.after(0, self.refresh_loot_tree)
            self.root.after(0, lambda: messagebox.showinfo("Import Complete", f"Imported {len(self.manager.loot_manager.loot_tables)} loot tables"))
            
        threading.Thread(target=import_loot, daemon=True).start()

    def show_statistics(self):
        """Show comprehensive statistics"""
        stats = self.manager.get_statistics()
        
        stats_text = f"""
=== VALHEIM UNIFIED MANAGER STATISTICS ===

MODS:
  Total: {stats['mods']['total']}
  By Category:
"""
        for category, count in stats['mods']['by_category'].items():
            stats_text += f"    {category}: {count}\n"
            
        stats_text += f"""
ITEMS:
  Total: {stats['items']['total']}
  With Icons: {stats['items']['with_icons']}
  With Translations: {stats['items']['with_translations']}
  By Category:
"""
        for category, count in stats['items']['by_category'].items():
            stats_text += f"    {category}: {count}\n"
            
        stats_text += f"""
LOOT TABLES:
  Total: {stats['loot_tables']['total']}
  By Source:
"""
        for source, count in stats['loot_tables']['by_source'].items():
            stats_text += f"    {source}: {count}\n"
            
        stats_text += "  By Category:\n"
        for category, count in stats['loot_tables']['by_category'].items():
            stats_text += f"    {category}: {count}\n"
            
        # Create a new window to show statistics
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statistics")
        stats_window.geometry("600x500")
        
        text_widget = tk.Text(stats_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, stats_text)
        text_widget.config(state=tk.DISABLED)

    def show_mod_details(self):
        """Show detailed mod information"""
        selection = self.mods_tree.selection()
        if not selection:
            return
            
        item = self.mods_tree.item(selection[0])
        mod_name = item['values'][0]
        
        if mod_name in self.mods:
            mod_info = self.mods[mod_name]
            
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Mod Details - {mod_name}")
            details_window.geometry("500x300")
            
            text_widget = tk.Text(details_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            details_text = f"""
Name: {mod_info.name}
Version: {mod_info.version}
Category: {mod_info.category}
Description: {mod_info.description}
"""
            text_widget.insert(tk.END, details_text)
            text_widget.config(state=tk.DISABLED)

    def show_item_details(self):
        """Show detailed item information"""
        selection = self.items_tree.selection()
        if not selection:
            return
            
        item = self.items_tree.item(selection[0])
        item_name = item['values'][0]
        
        # Find the item
        for item_id, item_info in self.items.items():
            if item_info.name == item_name:
                details_window = tk.Toplevel(self.root)
                details_window.title(f"Item Details - {item_name}")
                details_window.geometry("500x400")
                
                text_widget = tk.Text(details_window, wrap=tk.WORD)
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                details_text = f"""
Name: {item_info.name}
Prefab ID: {item_info.prefab_id}
Mod Source: {item_info.mod_source}
Category: {item_info.category}
Description: {item_info.description}
Icon Path: {item_info.icon_path}
Translation Key: {item_info.translation_key}
"""
                text_widget.insert(tk.END, details_text)
                text_widget.config(state=tk.DISABLED)
                break

    def show_loot_table_details(self):
        """Show detailed loot table information"""
        selection = self.loot_tree.selection()
        if not selection:
            return
            
        item = self.loot_tree.item(selection[0])
        table_name = item['values'][0]
        
        # Find the table
        for table_id, table in self.loot_manager.loot_tables.items():
            if table.name == table_name:
                details_window = tk.Toplevel(self.root)
                details_window.title(f"Loot Table Details - {table_name}")
                details_window.geometry("600x500")
                
                text_widget = tk.Text(details_window, wrap=tk.WORD)
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                details_text = f"""
Name: {table.name}
Source: {table.source}
Category: {table.category}
Item Count: {len(table.items)}

Items:
"""
                for item in table.items:
                    details_text += f"  - {item.name} (Stack: {item.stack_size}, Weight: {item.weight}, Rarity: {item.rarity})\n"
                    
                text_widget.insert(tk.END, details_text)
                text_widget.config(state=tk.DISABLED)
                break

    def sort_mod_tree(self, column):
        """Sort mod tree by column"""
        # Placeholder for sorting functionality
        pass

    def sort_item_tree(self, column):
        """Sort item tree by column"""
        # Placeholder for sorting functionality
        pass

    def sort_loot_tree(self, column):
        """Sort loot tree by column"""
        # Placeholder for sorting functionality
        pass

    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def main():
    """Main function"""
    app = ValheimUnifiedManagerGUI()
    app.run()

if __name__ == "__main__":
    main()
