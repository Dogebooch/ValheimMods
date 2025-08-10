#!/usr/bin/env python3
"""
Centralized Loot Table Manager for Valheim Mods

This script provides a unified interface for managing loot tables across multiple mods:
- Warpalicious More World Locations (YAML)
- EpicLoot (JSON)
- Creature Level & Loot Control (YAML)
- Drop That (CFG)
- Spawn That (CFG)

Features:
- Import loot tables from all sources
- Export back to original formats
- Unified editing interface
- Validation and conflict detection
- Backup and restore functionality
"""

import os
import json
import yaml
import re
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

@dataclass
class LootItem:
    """Represents a single item in a loot table"""
    item_name: str
    stack_min: int = 1
    stack_max: int = 1
    weight: float = 1.0
    chance: float = 1.0
    rarity: Optional[str] = None
    source_mod: str = ""
    conditions: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.conditions is None:
            self.conditions = {}

@dataclass
class LootTable:
    """Represents a complete loot table"""
    name: str
    source: str
    source_file: str
    description: str = ""
    items: List[LootItem] = None
    conditions: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.conditions is None:
            self.conditions = {}
        if self.metadata is None:
            self.metadata = {}

class CentralizedLootManager:
    """Main class for managing centralized loot tables"""
    
    def __init__(self, valheim_path: str = "Valheim"):
        self.valheim_path = Path(valheim_path)
        self.config_path = self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "config"
        self.backup_path = self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "config" / "loot_backups"
        
        # Ensure backup directory exists
        self.backup_path.mkdir(exist_ok=True)
        
        # Centralized loot data
        self.loot_tables: Dict[str, LootTable] = {}
        self.item_registry: Dict[str, List[str]] = {}  # item_name -> [table_names]
        
        # Load existing data
        self.load_centralized_data()
    
    def load_centralized_data(self):
        """Load existing centralized loot data if available"""
        centralized_file = self.config_path / "centralized_loot_tables.json"
        if centralized_file.exists():
            try:
                with open(centralized_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.loot_tables = {}
                    for table_name, table_data in data.get("loot_tables", {}).items():
                        items = [LootItem(**item) for item in table_data.get("items", [])]
                        self.loot_tables[table_name] = LootTable(
                            name=table_data["name"],
                            source=table_data["source"],
                            source_file=table_data["source_file"],
                            description=table_data.get("description", ""),
                            items=items,
                            conditions=table_data.get("conditions", {}),
                            metadata=table_data.get("metadata", {})
                        )
                self._rebuild_item_registry()
                print(f"Loaded {len(self.loot_tables)} loot tables from centralized data")
            except Exception as e:
                print(f"Error loading centralized data: {e}")
    
    def _rebuild_item_registry(self):
        """Rebuild the item registry from loot tables"""
        self.item_registry = {}
        for table_name, table in self.loot_tables.items():
            for item in table.items:
                if item.item_name not in self.item_registry:
                    self.item_registry[item.item_name] = []
                self.item_registry[item.item_name].append(table_name)
    
    def import_from_all_sources(self):
        """Import loot tables from all available sources"""
        print("Starting import from all sources...")
        
        # Import from Warpalicious
        self._import_warpalicious()
        
        # Import from EpicLoot
        self._import_epicloot()
        
        # Import from CLLC
        self._import_cllc()
        
        # Import from Drop That
        self._import_drop_that()
        
        # Rebuild item registry
        self._rebuild_item_registry()
        
        print(f"Import complete. Total loot tables: {len(self.loot_tables)}")
        self.save_centralized_data()
    
    def _import_warpalicious(self):
        """Import loot tables from Warpalicious More World Locations"""
        warpalicious_file = self.config_path / "warpalicious.More_World_Locations_LootLists.yml"
        if not warpalicious_file.exists():
            print("Warpalicious loot file not found")
            return
        
        try:
            with open(warpalicious_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if data and isinstance(data, dict):
                for table_name, items in data.items():
                    if table_name == "version":
                        continue
                    
                    loot_items = []
                    for item_data in items:
                        if isinstance(item_data, dict) and "item" in item_data:
                            loot_item = LootItem(
                                item_name=item_data["item"],
                                stack_min=item_data.get("stackMin", 1),
                                stack_max=item_data.get("stackMax", 1),
                                weight=item_data.get("weight", 1.0),
                                source_mod="Warpalicious"
                            )
                            loot_items.append(loot_item)
                    
                    if loot_items:
                        self.loot_tables[table_name] = LootTable(
                            name=table_name,
                            source="Warpalicious More World Locations",
                            source_file=str(warpalicious_file),
                            description=f"Loot table for {table_name}",
                            items=loot_items
                        )
            
            print(f"Imported {len([t for t in self.loot_tables.values() if t.source == 'Warpalicious More World Locations'])} Warpalicious loot tables")
        except Exception as e:
            print(f"Error importing Warpalicious: {e}")
    
    def _import_epicloot(self):
        """Import loot tables from EpicLoot"""
        epicloot_path = self.config_path / "EpicLoot" / "patches" / "RelicHeimPatches"
        if not epicloot_path.exists():
            print("EpicLoot patches directory not found")
            return
        
        for json_file in epicloot_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "Patches" in data:
                    for patch in data["Patches"]:
                        if "Value" in patch:
                            for loot_table_data in patch["Value"]:
                                if "Object" in loot_table_data and "LeveledLoot" in loot_table_data:
                                    table_name = f"{loot_table_data['Object']}_{json_file.stem}"
                                    
                                    loot_items = []
                                    for level_data in loot_table_data["LeveledLoot"]:
                                        if "Loot" in level_data:
                                            for loot_data in level_data["Loot"]:
                                                if "Item" in loot_data:
                                                    loot_item = LootItem(
                                                        item_name=loot_data["Item"],
                                                        weight=loot_data.get("Weight", 1.0),
                                                        rarity=loot_data.get("Rarity"),
                                                        source_mod="EpicLoot"
                                                    )
                                                    loot_items.append(loot_item)
                                    
                                    if loot_items:
                                        self.loot_tables[table_name] = LootTable(
                                            name=table_name,
                                            source="EpicLoot",
                                            source_file=str(json_file),
                                            description=f"EpicLoot loot table for {loot_table_data['Object']}",
                                            items=loot_items
                                        )
            except Exception as e:
                print(f"Error importing EpicLoot file {json_file}: {e}")
        
        print(f"Imported {len([t for t in self.loot_tables.values() if t.source == 'EpicLoot'])} EpicLoot loot tables")
    
    def _import_cllc(self):
        """Import item groups from Creature Level & Loot Control"""
        cllc_file = self.config_path / "ItemConfig_Base.yml"
        if not cllc_file.exists():
            print("CLLC item config file not found")
            return
        
        try:
            with open(cllc_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if data and isinstance(data, dict) and "groups" in data:
                for group_name, items in data["groups"].items():
                    if isinstance(items, list):
                        table_name = f"CLLC_Group_{group_name}"
                        loot_items = []
                        
                        for item_name in items:
                            loot_item = LootItem(
                                item_name=item_name,
                                source_mod="CLLC"
                            )
                            loot_items.append(loot_item)
                        
                        if loot_items:
                            self.loot_tables[table_name] = LootTable(
                                name=table_name,
                                source="Creature Level & Loot Control",
                                source_file=str(cllc_file),
                                description=f"CLLC item group: {group_name}",
                                items=loot_items
                            )
            
            print(f"Imported {len([t for t in self.loot_tables.values() if t.source == 'Creature Level & Loot Control'])} CLLC item groups")
        except Exception as e:
            print(f"Error importing CLLC: {e}")
    
    def _import_drop_that(self):
        """Import loot tables from Drop That"""
        drop_that_file = self.config_path / "drop_that.character_drop.cfg"
        if not drop_that_file.exists():
            print("Drop That character drop file not found")
            return
        
        try:
            with open(drop_that_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse INI-style configuration
            sections = re.split(r'\n\[', content)
            current_creature = None
            creature_drops = {}
            
            for section in sections:
                if not section.strip():
                    continue
                
                lines = section.strip().split('\n')
                if not lines:
                    continue
                
                header = lines[0].strip('[]')
                if '.' in header:
                    creature, drop_num = header.split('.', 1)
                    if creature not in creature_drops:
                        creature_drops[creature] = []
                    
                    drop_config = {}
                    for line in lines[1:]:
                        if '=' in line:
                            key, value = line.split('=', 1)
                            drop_config[key.strip()] = value.strip()
                    
                    if drop_config:
                        creature_drops[creature].append(drop_config)
            
            # Convert to loot tables
            for creature, drops in creature_drops.items():
                table_name = f"DropThat_{creature}"
                loot_items = []
                
                for drop in drops:
                    if "PrefabName" in drop:
                        loot_item = LootItem(
                            item_name=drop["PrefabName"],
                            stack_min=int(drop.get("SetAmountMin", 1)),
                            stack_max=int(drop.get("SetAmountMax", 1)),
                            chance=float(drop.get("SetChanceToDrop", 1.0)),
                            source_mod="Drop That"
                        )
                        loot_items.append(loot_item)
                
                if loot_items:
                    self.loot_tables[table_name] = LootTable(
                        name=table_name,
                        source="Drop That",
                        source_file=str(drop_that_file),
                        description=f"Drop That configuration for {creature}",
                        items=loot_items
                    )
            
            print(f"Imported {len([t for t in self.loot_tables.values() if t.source == 'Drop That'])} Drop That loot tables")
        except Exception as e:
            print(f"Error importing Drop That: {e}")
    
    def save_centralized_data(self):
        """Save centralized loot data to JSON file"""
        centralized_file = self.config_path / "centralized_loot_tables.json"
        
        # Convert dataclasses to dictionaries
        data = {
            "metadata": {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "total_tables": len(self.loot_tables),
                "total_items": len(self.item_registry)
            },
            "loot_tables": {}
        }
        
        for table_name, table in self.loot_tables.items():
            data["loot_tables"][table_name] = {
                "name": table.name,
                "source": table.source,
                "source_file": table.source_file,
                "description": table.description,
                "items": [asdict(item) for item in table.items],
                "conditions": table.conditions,
                "metadata": table.metadata
            }
        
        try:
            with open(centralized_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved centralized loot data to {centralized_file}")
        except Exception as e:
            print(f"Error saving centralized data: {e}")
    
    def create_backup(self):
        """Create a backup of all loot configuration files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_path / f"backup_{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        # Files to backup
        files_to_backup = [
            "warpalicious.More_World_Locations_LootLists.yml",
            "ItemConfig_Base.yml",
            "drop_that.character_drop.cfg",
            "drop_that.drop_table.cfg",
            "centralized_loot_tables.json"
        ]
        
        for file_name in files_to_backup:
            source_file = self.config_path / file_name
            if source_file.exists():
                shutil.copy2(source_file, backup_dir / file_name)
        
        # Backup EpicLoot directory
        epicloot_source = self.config_path / "EpicLoot"
        if epicloot_source.exists():
            shutil.copytree(epicloot_source, backup_dir / "EpicLoot")
        
        print(f"Backup created at {backup_dir}")
        return backup_dir
    
    def export_to_original_formats(self):
        """Export centralized data back to original mod formats"""
        print("Exporting to original formats...")
        
        # Export to Warpalicious format
        self._export_to_warpalicious()
        
        # Export to EpicLoot format
        self._export_to_epicloot()
        
        # Export to CLLC format
        self._export_to_cllc()
        
        # Export to Drop That format
        self._export_to_drop_that()
        
        print("Export complete")
    
    def _export_to_warpalicious(self):
        """Export loot tables back to Warpalicious format"""
        warpalicious_tables = {name: table for name, table in self.loot_tables.items() 
                              if table.source == "Warpalicious More World Locations"}
        
        if not warpalicious_tables:
            return
        
        data = {"version": "2.0"}
        
        for table_name, table in warpalicious_tables.items():
            data[table_name] = []
            for item in table.items:
                item_data = {
                    "item": item.item_name,
                    "stackMin": item.stack_min,
                    "stackMax": item.stack_max,
                    "weight": item.weight
                }
                data[table_name].append(item_data)
        
        output_file = self.config_path / "warpalicious.More_World_Locations_LootLists.yml"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            print(f"Exported {len(warpalicious_tables)} tables to Warpalicious format")
        except Exception as e:
            print(f"Error exporting to Warpalicious: {e}")
    
    def _export_to_epicloot(self):
        """Export loot tables back to EpicLoot format"""
        epicloot_tables = {name: table for name, table in self.loot_tables.items() 
                          if table.source == "EpicLoot"}
        
        if not epicloot_tables:
            return
        
        # Group by source file
        files_data = {}
        for table_name, table in epicloot_tables.items():
            if table.source_file not in files_data:
                files_data[table.source_file] = {
                    "TargetFile": "loottables.json",
                    "Author": "CentralizedLootManager",
                    "RequireAll": True,
                    "Patches": []
                }
            
            # Extract object name from table name
            if '_' in table_name:
                object_name = table_name.split('_')[0]
            else:
                object_name = table_name
            
            patch_data = {
                "Path": "$.LootTables",
                "Action": "AppendAll",
                "Value": [{
                    "Object": object_name,
                    "LeveledLoot": [{
                        "Level": 1,
                        "Drops": [[0, 85], [1, 10], [2, 5], [3, 0]],
                        "Loot": [{"Item": item.item_name, "Weight": item.weight} for item in table.items]
                    }]
                }]
            }
            
            files_data[table.source_file]["Patches"].append(patch_data)
        
        # Write files
        for file_path, data in files_data.items():
            try:
                output_file = Path(file_path)
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"Exported EpicLoot data to {output_file}")
            except Exception as e:
                print(f"Error exporting EpicLoot to {file_path}: {e}")
    
    def _export_to_cllc(self):
        """Export item groups back to CLLC format"""
        cllc_tables = {name: table for name, table in self.loot_tables.items() 
                      if table.source == "Creature Level & Loot Control"}
        
        if not cllc_tables:
            return
        
        data = {"groups": {}}
        
        for table_name, table in cllc_tables.items():
            # Extract group name from table name
            if table_name.startswith("CLLC_Group_"):
                group_name = table_name.replace("CLLC_Group_", "")
            else:
                group_name = table_name
            
            data["groups"][group_name] = [item.item_name for item in table.items]
        
        output_file = self.config_path / "ItemConfig_Base.yml"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            print(f"Exported {len(cllc_tables)} groups to CLLC format")
        except Exception as e:
            print(f"Error exporting to CLLC: {e}")
    
    def _export_to_drop_that(self):
        """Export loot tables back to Drop That format"""
        drop_that_tables = {name: table for name, table in self.loot_tables.items() 
                           if table.source == "Drop That"}
        
        if not drop_that_tables:
            return
        
        content = []
        content.append("# Auto-generated file for adding CharacterDrop configurations.")
        content.append("# This file is empty by default. It is intended to contains changes only, to avoid unintentional modifications as well as to reduce unnecessary performance cost.")
        content.append("# Full documentation can be found at https://github.com/ASharpPen/Valheim.DropThat/wiki.")
        content.append("")
        
        for table_name, table in drop_that_tables.items():
            # Extract creature name from table name
            if table_name.startswith("DropThat_"):
                creature_name = table_name.replace("DropThat_", "")
            else:
                creature_name = table_name
            
            for i, item in enumerate(table.items, 1):
                content.append(f"[{creature_name}.{i}]")
                content.append(f"PrefabName = {item.item_name}")
                content.append(f"EnableConfig = true")
                content.append(f"SetAmountMin = {item.stack_min}")
                content.append(f"SetAmountMax = {item.stack_max}")
                content.append(f"SetChanceToDrop = {item.chance}")
                content.append(f"SetDropOnePerPlayer = false")
                content.append(f"SetScaleByLevel = false")
                content.append("")
        
        output_file = self.config_path / "drop_that.character_drop.cfg"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
            print(f"Exported {len(drop_that_tables)} tables to Drop That format")
        except Exception as e:
            print(f"Error exporting to Drop That: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the loot tables"""
        stats = {
            "total_tables": len(self.loot_tables),
            "total_items": len(self.item_registry),
            "sources": {},
            "items_per_table": [],
            "most_common_items": []
        }
        
        # Count by source
        for table in self.loot_tables.values():
            source = table.source
            if source not in stats["sources"]:
                stats["sources"][source] = 0
            stats["sources"][source] += 1
        
        # Items per table
        for table_name, table in self.loot_tables.items():
            stats["items_per_table"].append({
                "table": table_name,
                "count": len(table.items),
                "source": table.source
            })
        
        # Most common items
        item_counts = {}
        for item_name, table_names in self.item_registry.items():
            item_counts[item_name] = len(table_names)
        
        most_common = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        stats["most_common_items"] = [{"item": item, "count": count} for item, count in most_common]
        
        return stats

class CentralizedLootGUI:
    """GUI for the centralized loot manager"""
    
    def __init__(self, manager: CentralizedLootManager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Centralized Loot Table Manager")
        self.root.geometry("1200x800")
        
        self.setup_ui()
    
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
        
        ttk.Button(control_frame, text="Import from All Sources", 
                  command=self.import_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Export to Original Formats", 
                  command=self.export_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Create Backup", 
                  command=self.create_backup).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Show Statistics", 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=(0, 5))
        
        # Notebook for different views
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Loot Tables tab
        self.setup_loot_tables_tab()
        
        # Items tab
        self.setup_items_tab()
        
        # Sources tab
        self.setup_sources_tab()
        
        # Refresh data
        self.refresh_data()
    
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
        self.refresh_table_tree()
        self.refresh_item_tree()
        self.refresh_source_tree()
    
    def refresh_table_tree(self):
        """Refresh the loot tables treeview"""
        # Clear existing items
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)
        
        # Add loot tables
        for table_name, table in self.manager.loot_tables.items():
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
        for item_name, table_names in self.manager.item_registry.items():
            sources = set()
            for table_name in table_names:
                if table_name in self.manager.loot_tables:
                    sources.add(self.manager.loot_tables[table_name].source)
            
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
        for table in self.manager.loot_tables.values():
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
    
    def filter_tables(self, *args):
        """Filter loot tables based on search"""
        search_term = self.table_search_var.get().lower()
        
        # Clear existing items
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)
        
        # Add filtered loot tables
        for table_name, table in self.manager.loot_tables.items():
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
        for item_name, table_names in self.manager.item_registry.items():
            if search_term in item_name.lower():
                sources = set()
                for table_name in table_names:
                    if table_name in self.manager.loot_tables:
                        sources.add(self.manager.loot_tables[table_name].source)
                
                self.item_tree.insert("", "end", values=(
                    item_name,
                    len(table_names),
                    ", ".join(sorted(sources))
                ))
    
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
    
    def show_table_details(self, event):
        """Show detailed information about a loot table"""
        selection = self.table_tree.selection()
        if not selection:
            return
        
        item = self.table_tree.item(selection[0])
        table_name = item['values'][0]
        
        if table_name in self.manager.loot_tables:
            table = self.manager.loot_tables[table_name]
            self.show_table_details_window(table)
    
    def show_item_details(self, event):
        """Show detailed information about an item"""
        selection = self.item_tree.selection()
        if not selection:
            return
        
        item = self.item_tree.item(selection[0])
        item_name = item['values'][0]
        
        if item_name in self.manager.item_registry:
            self.show_item_details_window(item_name)
    
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
Appears in {len(self.manager.item_registry[item_name])} loot tables:

"""
        
        for table_name in self.manager.item_registry[item_name]:
            if table_name in self.manager.loot_tables:
                table = self.manager.loot_tables[table_name]
                content += f"• {table.name} ({table.source})\n"
        
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
    
    def import_all(self):
        """Import from all sources"""
        def import_thread():
            self.manager.import_from_all_sources()
            self.root.after(0, self.refresh_data)
            self.root.after(0, lambda: messagebox.showinfo("Import Complete", 
                f"Imported {len(self.manager.loot_tables)} loot tables from all sources"))
        
        threading.Thread(target=import_thread, daemon=True).start()
    
    def export_all(self):
        """Export to all original formats"""
        def export_thread():
            self.manager.export_to_original_formats()
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
        window.title("Loot Table Statistics")
        window.geometry("500x400")
        
        # Create text widget
        text_widget = tk.Text(window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add content
        content = f"""Loot Table Statistics

Total Loot Tables: {stats['total_tables']}
Total Unique Items: {stats['total_items']}

Sources:
"""
        
        for source, count in stats['sources'].items():
            content += f"• {source}: {count} tables\n"
        
        content += "\nMost Common Items:\n"
        for item_data in stats['most_common_items']:
            content += f"• {item_data['item']}: {item_data['count']} tables\n"
        
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    manager = CentralizedLootManager()
    gui = CentralizedLootGUI(manager)
    gui.run()

if __name__ == "__main__":
    main()
