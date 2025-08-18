#!/usr/bin/env python3
"""
Enhanced Material Drop Calculator for RelicHeim
Calculates baseline drop chances for materials from all loot sources and compares to current configuration.
"""

import os
import json
import yaml
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import re

@dataclass
class DropSource:
    """Represents a drop source (monster, chest, etc.)"""
    name: str
    source_type: str  # "monster", "chest", "boss", "pickable", etc.
    is_boss: bool = False
    weight: float = 1.0  # How common this source is
    loot_tables: List[str] = None  # Which loot tables this source uses

@dataclass
class MaterialDrop:
    """Represents a material drop chance"""
    material: str
    source: str
    weight: float
    stack_min: int = 1
    stack_max: int = 1
    chance: float = 0.0  # Calculated chance

class EnhancedMaterialCalculator:
    def __init__(self, config_root: str):
        self.config_root = Path(config_root)
        self.materials = self._load_materials()
        self.aliases = self._load_aliases()
        
    def _load_materials(self) -> Dict[str, List[str]]:
        """Load material definitions from materials.json"""
        materials_file = Path(__file__).parent.parent / "materials.json"
        if materials_file.exists():
            with open(materials_file, 'r') as f:
                data = json.load(f)
                return data.get("tiers", {})
        return {}
    
    def _load_aliases(self) -> Dict[str, str]:
        """Load material aliases from materials.json"""
        materials_file = Path(__file__).parent.parent / "materials.json"
        if materials_file.exists():
            with open(materials_file, 'r') as f:
                data = json.load(f)
                return data.get("aliases", {})
        return {}
    
    def _get_all_materials(self) -> List[str]:
        """Get all material names including aliases"""
        materials = set()
        for tier_materials in self.materials.values():
            materials.update(tier_materials)
        # Add aliases
        for alias, target in self.aliases.items():
            materials.add(alias)
        return sorted(list(materials))
    
    def _parse_loot_tables(self) -> Dict[str, List[MaterialDrop]]:
        """Parse all loot tables and extract material drops"""
        loot_tables = {}
        
        # Parse EpicLoot loot tables
        epicloot_dir = self.config_root / "EpicLoot" / "patches"
        if epicloot_dir.exists():
            for patch_file in epicloot_dir.rglob("*.json"):
                if "loottables" in patch_file.name.lower():
                    loot_tables.update(self._parse_epicloot_patch(patch_file))
        
        # Parse world locations YAML
        world_locations_file = self.config_root / "warpalicious.More_World_Locations_LootLists.yml"
        if world_locations_file.exists():
            loot_tables.update(self._parse_world_locations(world_locations_file))
        
        # Parse Drop That configurations
        drop_that_dir = self.config_root / "Drop_That"
        if drop_that_dir.exists():
            for cfg_file in drop_that_dir.rglob("*.cfg"):
                loot_tables.update(self._parse_drop_that_cfg(cfg_file))
        
        return loot_tables
    
    def _parse_epicloot_patch(self, patch_file: Path) -> Dict[str, List[MaterialDrop]]:
        """Parse EpicLoot patch files for loot tables"""
        loot_tables = {}
        
        try:
            with open(patch_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for patch in data.get("Patches", []):
                if patch.get("Path", "").startswith("$.ItemSets"):
                    for item_set in patch.get("Value", []):
                        table_name = item_set.get("Name", "")
                        drops = []
                        
                        for loot_item in item_set.get("Loot", []):
                            item_name = loot_item.get("Item", "")
                            weight = loot_item.get("Weight", 1.0)
                            amount = loot_item.get("Amount", 1)
                            
                            # Check if this is a material we're tracking
                            if item_name in self._get_all_materials():
                                drops.append(MaterialDrop(
                                    material=item_name,
                                    source=table_name,
                                    weight=weight,
                                    stack_min=amount,
                                    stack_max=amount
                                ))
                        
                        if drops:
                            loot_tables[table_name] = drops
                            
        except Exception as e:
            print(f"Error parsing EpicLoot patch {patch_file}: {e}")
        
        return loot_tables
    
    def _parse_world_locations(self, yaml_file: Path) -> Dict[str, List[MaterialDrop]]:
        """Parse world locations YAML file"""
        loot_tables = {}
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            
            for table_name, items in data.items():
                drops = []
                
                for item_data in items:
                    if isinstance(item_data, dict):
                        item_name = item_data.get("item", "")
                        weight = item_data.get("weight", 1.0)
                        stack_min = item_data.get("stackMin", 1)
                        stack_max = item_data.get("stackMax", 1)
                        
                        # Check if this is a material we're tracking
                        if item_name in self._get_all_materials():
                            drops.append(MaterialDrop(
                                material=item_name,
                                source=table_name,
                                weight=weight,
                                stack_min=stack_min,
                                stack_max=stack_max
                            ))
                
                if drops:
                    loot_tables[table_name] = drops
                    
        except Exception as e:
            print(f"Error parsing world locations {yaml_file}: {e}")
        
        return loot_tables
    
    def _parse_drop_that_cfg(self, cfg_file: Path) -> Dict[str, List[MaterialDrop]]:
        """Parse Drop That configuration files"""
        loot_tables = {}
        
        try:
            with open(cfg_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse Drop That format
            current_table = None
            current_drops = []
            
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Check for table start
                if line.startswith('[') and line.endswith(']'):
                    # Save previous table
                    if current_table and current_drops:
                        loot_tables[current_table] = current_drops
                    
                    current_table = line[1:-1]
                    current_drops = []
                    continue
                
                # Parse drop entries
                if '=' in line and current_table:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key.startswith('DropList'):
                        # Parse drop list format
                        parts = value.split(',')
                        if len(parts) >= 3:
                            item_name = parts[0].strip()
                            weight = float(parts[1].strip())
                            amount = int(parts[2].strip())
                            
                            if item_name in self._get_all_materials():
                                current_drops.append(MaterialDrop(
                                    material=item_name,
                                    source=current_table,
                                    weight=weight,
                                    stack_min=amount,
                                    stack_max=amount
                                ))
            
            # Save last table
            if current_table and current_drops:
                loot_tables[current_table] = current_drops
                
        except Exception as e:
            print(f"Error parsing Drop That config {cfg_file}: {e}")
        
        return loot_tables
    
    def _calculate_drop_chances(self, loot_tables: Dict[str, List[MaterialDrop]]) -> Dict[str, Dict[str, float]]:
        """Calculate drop chances for each material from each source"""
        drop_chances = defaultdict(lambda: defaultdict(float))
        
        for table_name, drops in loot_tables.items():
            # Calculate total weight for this table
            total_weight = sum(drop.weight for drop in drops)
            
            if total_weight > 0:
                for drop in drops:
                    # Calculate chance as (drop_weight / total_weight) * 100
                    chance = (drop.weight / total_weight) * 100.0
                    drop_chances[drop.material][table_name] = chance
        
        return dict(drop_chances)
    
    def _classify_sources(self, loot_tables: Dict[str, List[MaterialDrop]]) -> Dict[str, str]:
        """Classify loot tables as boss, monster, chest, etc."""
        source_types = {}
        
        # Define patterns for classification
        boss_patterns = [
            r'boss', r'elder', r'bonemass', r'moder', r'yagluth', r'queen', r'king'
        ]
        monster_patterns = [
            r'greydwarf', r'troll', r'draugr', r'skeleton', r'blob', r'leech', 
            r'wraith', r'surtling', r'wolf', r'fenring', r'lox', r'goblin'
        ]
        chest_patterns = [
            r'chest', r'treasure', r'crypt', r'tomb', r'burial', r'vault'
        ]
        
        for table_name in loot_tables.keys():
            table_lower = table_name.lower()
            
            if any(re.search(pattern, table_lower) for pattern in boss_patterns):
                source_types[table_name] = "boss"
            elif any(re.search(pattern, table_lower) for pattern in monster_patterns):
                source_types[table_name] = "monster"
            elif any(re.search(pattern, table_lower) for pattern in chest_patterns):
                source_types[table_name] = "chest"
            else:
                source_types[table_name] = "other"
        
        return source_types
    
    def calculate_baseline_chances(self) -> Dict[str, Dict[str, float]]:
        """Calculate baseline drop chances for all materials"""
        print("Parsing loot tables...")
        loot_tables = self._parse_loot_tables()
        
        print("Calculating drop chances...")
        drop_chances = self._calculate_drop_chances(loot_tables)
        
        print("Classifying sources...")
        source_types = self._classify_sources(loot_tables)
        
        # Aggregate chances by source type
        baseline_chances = defaultdict(lambda: defaultdict(float))
        
        for material, sources in drop_chances.items():
            for source, chance in sources.items():
                source_type = source_types.get(source, "other")
                baseline_chances[material][source_type] += chance
        
        return dict(baseline_chances)
    
    def compare_configurations(self, baseline_chances: Dict[str, Dict[str, float]], 
                             current_chances: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Compare baseline vs current configuration"""
        comparison = {}
        
        all_materials = set(baseline_chances.keys()) | set(current_chances.keys())
        
        for material in all_materials:
            baseline = baseline_chances.get(material, {})
            current = current_chances.get(material, {})
            
            comparison[material] = {
                "baseline": baseline,
                "current": current,
                "changes": {}
            }
            
            all_source_types = set(baseline.keys()) | set(current.keys())
            
            for source_type in all_source_types:
                baseline_chance = baseline.get(source_type, 0.0)
                current_chance = current.get(source_type, 0.0)
                
                if baseline_chance > 0:
                    percent_change = ((current_chance - baseline_chance) / baseline_chance) * 100.0
                elif current_chance > 0:
                    percent_change = 100.0  # New drop source
                else:
                    percent_change = 0.0
                
                comparison[material]["changes"][source_type] = {
                    "baseline": baseline_chance,
                    "current": current_chance,
                    "percent_change": percent_change
                }
        
        return comparison
    
    def generate_report(self, comparison: Dict[str, Dict[str, Dict[str, float]]]) -> str:
        """Generate a human-readable report"""
        report_lines = []
        report_lines.append("# Material Drop Chance Analysis")
        report_lines.append("")
        
        # Group by material tier
        for tier, materials in self.materials.items():
            report_lines.append(f"## {tier} Tier Materials")
            report_lines.append("")
            
            for material in materials:
                if material in comparison:
                    data = comparison[material]
                    report_lines.append(f"### {material}")
                    report_lines.append("")
                    
                    # Show boss drops
                    if "boss" in data["changes"]:
                        boss_data = data["changes"]["boss"]
                        report_lines.append(f"**Boss Drops:**")
                        report_lines.append(f"- Baseline: {boss_data['baseline']:.2f}%")
                        report_lines.append(f"- Current: {boss_data['current']:.2f}%")
                        report_lines.append(f"- Change: {boss_data['percent_change']:+.1f}%")
                        report_lines.append("")
                    
                    # Show monster drops
                    if "monster" in data["changes"]:
                        monster_data = data["changes"]["monster"]
                        report_lines.append(f"**Monster Drops:**")
                        report_lines.append(f"- Baseline: {monster_data['baseline']:.2f}%")
                        report_lines.append(f"- Current: {monster_data['current']:.2f}%")
                        report_lines.append(f"- Change: {monster_data['percent_change']:+.1f}%")
                        report_lines.append("")
                    
                    # Show chest drops
                    if "chest" in data["changes"]:
                        chest_data = data["changes"]["chest"]
                        report_lines.append(f"**Chest Drops:**")
                        report_lines.append(f"- Baseline: {chest_data['baseline']:.2f}%")
                        report_lines.append(f"- Current: {chest_data['current']:.2f}%")
                        report_lines.append(f"- Change: {chest_data['percent_change']:+.1f}%")
                        report_lines.append("")
                    
                    report_lines.append("---")
                    report_lines.append("")
        
        return "\n".join(report_lines)

def main():
    """Main function to run the enhanced calculator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Material Drop Calculator")
    parser.add_argument("config_root", help="Path to Valheim config directory")
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument("--baseline-only", action="store_true", help="Only calculate baseline")
    
    args = parser.parse_args()
    
    calculator = EnhancedMaterialCalculator(args.config_root)
    
    print("Calculating baseline drop chances...")
    baseline_chances = calculator.calculate_baseline_chances()
    
    if args.baseline_only:
        print("\nBaseline Drop Chances:")
        for material, sources in baseline_chances.items():
            print(f"\n{material}:")
            for source_type, chance in sources.items():
                print(f"  {source_type}: {chance:.2f}%")
    else:
        # For now, use baseline as current (you can modify this to load current config)
        current_chances = baseline_chances.copy()
        
        print("Comparing configurations...")
        comparison = calculator.compare_configurations(baseline_chances, current_chances)
        
        print("Generating report...")
        report = calculator.generate_report(comparison)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

if __name__ == "__main__":
    main()
