#!/usr/bin/env python3
"""
Comprehensive Item Scanner for Valheim Mods
Scans multiple sources to extract all items from mods:
- Mod cache directories
- VNEI data
- Cached icons
- Translation files
"""

import os
import re
import json
import yaml
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Set, Optional
import glob

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

class ComprehensiveItemScanner:
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
        print("Scanning cached icons...")
        
        if not self.cached_icons_path.exists():
            print(f"Warning: Cached icons path not found: {self.cached_icons_path}")
            return
            
        for icon_file in self.cached_icons_path.glob("*.png"):
            filename = icon_file.stem
            # Parse filename format: ItemName-ModName-Version-c1.png
            parts = filename.split("-")
            if len(parts) >= 3:
                item_name = parts[0]
                mod_name = parts[1]
                version = parts[2]
                
                # Clean up item name (remove prefixes like Pickable_, BMR_, etc.)
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
                
        # Convert to title case and replace underscores with spaces
        clean_name = clean_name.replace("_", " ").title()
        return clean_name

    def scan_translation_files(self) -> None:
        """Extract item information from translation files"""
        print("Scanning translation files...")
        
        translation_files_found = 0
        
        for mod_dir in self.cache_path.iterdir():
            if not mod_dir.is_dir():
                continue
                
            mod_name = mod_dir.name
            config_path = mod_dir / "config"
            if not config_path.exists():
                continue
                
            # Look for translation files
            translation_files = list(config_path.rglob("*.yml")) + list(config_path.rglob("*.yaml"))
            
            if translation_files:
                print(f"Found {len(translation_files)} translation files in {mod_name}")
                translation_files_found += len(translation_files)
            
            for trans_file in translation_files:
                try:
                    with open(trans_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Extract item names from translation files
                    items_found = self.extract_items_from_translations(content, mod_name, trans_file)
                    if items_found > 0:
                        print(f"  Found {items_found} items in {trans_file.name}")
                    
                except Exception as e:
                    print(f"Error reading translation file {trans_file}: {e}")
                    
        print(f"Total translation files scanned: {translation_files_found}")

    def extract_items_from_translations(self, content: str, mod_name: str, file_path: Path) -> int:
        """Extract item information from translation content"""
        items_found = 0
        
        # Look for patterns like: item_name_TW : "Item Display Name"
        pattern = r'([a-zA-Z_]+)_TW\s*:\s*"([^"]+)"'
        matches = re.findall(pattern, content)
        
        for item_id, display_name in matches:
            # Skip non-item entries
            if any(skip in item_id.lower() for skip in ['piece_', 'topic_', 'text_', 'description_', 'buff_', 'set_']):
                continue
                
            # Create unique item ID
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
                # Update existing item with translation info
                self.items[unique_id].name = display_name
                self.items[unique_id].translation_key = f"{item_id}_TW"
                items_found += 1
                
        return items_found

    def scan_vnei_data(self) -> None:
        """Extract item information from VNEI data"""
        print("Scanning VNEI data...")
        
        # Look for VNEI data files
        vnei_data_paths = [
            self.vnei_path,
            self.valheim_path / "profiles" / "Dogeheim_Player" / "BepInEx" / "config" / "VNEI"
        ]
        
        for vnei_path in vnei_data_paths:
            if not vnei_path.exists():
                continue
                
            # Look for VNEI data files
            for data_file in vnei_path.rglob("*.json"):
                try:
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.extract_items_from_vnei_data(data, data_file.name)
                except Exception as e:
                    print(f"Error reading VNEI data file {data_file}: {e}")

    def extract_items_from_vnei_data(self, data: dict, filename: str) -> None:
        """Extract item information from VNEI data structure"""
        # VNEI data structure varies, so we'll try different patterns
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and 'name' in value:
                    item_name = value.get('name', key)
                    mod_source = value.get('mod', 'Unknown')
                    
                    unique_id = f"{key}_{mod_source}"
                    if unique_id not in self.items:
                        self.items[unique_id] = ItemInfo(
                            name=item_name,
                            prefab_id=key,
                            mod_source=mod_source,
                            category=self.get_mod_category(mod_source)
                        )

    def scan_mod_manifests(self) -> None:
        """Extract mod information from manifest files"""
        print("Scanning mod manifests...")
        
        for mod_dir in self.cache_path.iterdir():
            if not mod_dir.is_dir():
                continue
                
            manifest_file = mod_dir / "manifest.json"
            if not manifest_file.exists():
                continue
                
            try:
                with open(manifest_file, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                    
                mod_name = manifest.get('name', mod_dir.name)
                mod_version = manifest.get('version_number', 'unknown')
                
                # Store mod information for reference
                print(f"Found mod: {mod_name} v{mod_version}")
                
            except Exception as e:
                print(f"Error reading manifest {manifest_file}: {e}")

    def get_mod_category(self, mod_name: str) -> str:
        """Determine the category of a mod based on its name"""
        # Handle version numbers (like 0.220.5) - these are vanilla items
        if mod_name.replace('.', '').isdigit():
            return "vanilla"
            
        # Check against our mod categories
        for category, mods in self.mod_categories.items():
            for mod in mods:
                if mod.lower() in mod_name.lower():
                    return category
                    
        # Try to categorize based on mod name patterns
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
        print("Starting comprehensive item scan...")
        
        self.scan_cached_icons()
        self.scan_translation_files()
        self.scan_vnei_data()
        self.scan_mod_manifests()
        
        print(f"Found {len(self.items)} items total")
        return self.items

    def export_to_json(self, output_file: str = "comprehensive_items.json") -> None:
        """Export items to JSON file"""
        items_dict = {item_id: asdict(item) for item_id, item in self.items.items()}
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(items_dict, f, indent=2, ensure_ascii=False)
            
        print(f"Exported {len(self.items)} items to {output_file}")

    def get_statistics(self) -> Dict[str, any]:
        """Get statistics about the scanned items"""
        stats = {
            "total_items": len(self.items),
            "by_category": {},
            "by_mod": {},
            "with_icons": 0,
            "with_translations": 0
        }
        
        for item in self.items.values():
            # Count by category
            category = item.category
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            # Count by mod
            mod = item.mod_source
            stats["by_mod"][mod] = stats["by_mod"].get(mod, 0) + 1
            
            # Count items with icons/translations
            if item.icon_path:
                stats["with_icons"] += 1
            if item.translation_key:
                stats["with_translations"] += 1
                
        return stats

def main():
    """Main function to run the comprehensive item scanner"""
    scanner = ComprehensiveItemScanner()
    items = scanner.scan_all_sources()
    
    # Export results
    scanner.export_to_json()
    
    # Print statistics
    stats = scanner.get_statistics()
    print("\n=== SCAN STATISTICS ===")
    print(f"Total items found: {stats['total_items']}")
    print(f"Items with icons: {stats['with_icons']}")
    print(f"Items with translations: {stats['with_translations']}")
    
    print("\n=== ITEMS BY CATEGORY ===")
    for category, count in sorted(stats['by_category'].items()):
        print(f"{category}: {count}")
    
    print("\n=== TOP MODS BY ITEM COUNT ===")
    sorted_mods = sorted(stats['by_mod'].items(), key=lambda x: x[1], reverse=True)
    for mod, count in sorted_mods[:10]:
        print(f"{mod}: {count}")

if __name__ == "__main__":
    main()
