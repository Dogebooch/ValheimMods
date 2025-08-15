#!/usr/bin/env python3
"""
More World Locations Spawn Extractor
Extracts all spawn information from warpalicious More World Locations mods
and compiles them into a single markdown document.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Any
import argparse

class MoreWorldLocationsSpawnExtractor:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.spawn_data = {}
        self.creature_lists = {}
        self.loot_lists = {}
        self.pickable_lists = {}
        
    def extract_spawns_from_yml(self, file_path: Path) -> Dict[str, Any]:
        """Extract spawn information from YAML files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                return {}
            
            spawns = {}
            for key, value in data.items():
                if isinstance(value, list):
                    # Clean up creature names and remove duplicates
                    creatures = []
                    for creature in value:
                        if isinstance(creature, str) and creature.strip():
                            creatures.append(creature.strip())
                    
                    # Remove duplicates while preserving order
                    unique_creatures = []
                    seen = set()
                    for creature in creatures:
                        if creature not in seen:
                            unique_creatures.append(creature)
                            seen.add(creature)
                    
                    spawns[key] = unique_creatures
            
            return spawns
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {}
    
    def extract_locations_from_cfg(self, file_path: Path) -> Dict[str, Any]:
        """Extract location spawn information from CFG files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            locations = {}
            
            # Find all location sections
            location_pattern = r'\[([^\]]+)\]\s*\n((?:[^\[]*\n)*?)(?=\[|$)'
            matches = re.finditer(location_pattern, content, re.MULTILINE)
            
            for match in matches:
                section_name = match.group(1)
                section_content = match.group(2)
                
                # Skip non-location sections
                if not section_name.startswith(('MWL_', '1 -', '2 -', '3 -', '4 -', '5 -', '6 -', '7 -', '8 -', '9 -', '10 -')):
                    continue
                
                location_info = {}
                
                # Extract spawn quantity
                spawn_match = re.search(r'Spawn Quantity\s*=\s*(\d+)', section_content)
                if spawn_match:
                    location_info['spawn_quantity'] = int(spawn_match.group(1))
                
                # Extract creature list name
                creature_list_match = re.search(r'Name of Creature List\s*=\s*([^\n]+)', section_content)
                if creature_list_match:
                    location_info['creature_list'] = creature_list_match.group(1).strip()
                
                # Extract loot list name
                loot_list_match = re.search(r'Name of Loot List\s*=\s*([^\n]+)', section_content)
                if loot_list_match:
                    location_info['loot_list'] = loot_list_match.group(1).strip()
                
                # Check if custom creatures are enabled
                custom_creatures_match = re.search(r'Use Custom Creature YAML file\s*=\s*(On|Off)', section_content)
                if custom_creatures_match:
                    location_info['use_custom_creatures'] = custom_creatures_match.group(1) == 'On'
                
                # Check if custom loot is enabled
                custom_loot_match = re.search(r'Use Custom Loot YAML file\s*=\s*(On|Off)', section_content)
                if custom_loot_match:
                    location_info['use_custom_loot'] = custom_loot_match.group(1) == 'On'
                
                if location_info:
                    locations[section_name] = location_info
            
            return locations
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {}
    
    def get_more_world_locations_files(self) -> List[Path]:
        """Get all More World Locations configuration files."""
        files = []
        
        # Look for warpalicious files
        for file_path in self.config_dir.glob("warpalicious.*"):
            if file_path.is_file():
                files.append(file_path)
        
        return files
    
    def categorize_file(self, file_path: Path) -> str:
        """Categorize the file based on its name."""
        name = file_path.name.lower()
        
        if "meadows" in name:
            return "Meadows"
        elif "blackforest" in name or "black_forest" in name:
            return "Black Forest"
        elif "swamp" in name:
            return "Swamp"
        elif "mountains" in name:
            return "Mountains"
        elif "plains" in name:
            return "Plains"
        elif "mistlands" in name:
            return "Mistlands"
        elif "ashlands" in name:
            return "Ashlands"
        elif "underground" in name or "catacombs" in name:
            return "Underground"
        elif "adventure" in name:
            return "Adventure"
        elif "traders" in name:
            return "Traders"
        elif "creature" in name:
            return "Creature Lists"
        elif "loot" in name:
            return "Loot Lists"
        elif "pickable" in name:
            return "Pickable Items"
        else:
            return "Other"
    
    def extract_all_spawns(self) -> Dict[str, Dict[str, Any]]:
        """Extract spawns from all More World Locations files."""
        files = self.get_more_world_locations_files()
        
        categorized_data = {}
        
        # First pass: Extract YAML lists
        for file_path in files:
            if file_path.suffix.lower() == '.yml':
                print(f"Processing YAML: {file_path.name}")
                
                category = self.categorize_file(file_path)
                if category not in categorized_data:
                    categorized_data[category] = {}
                
                spawns = self.extract_spawns_from_yml(file_path)
                
                if spawns:
                    categorized_data[category][file_path.name] = {
                        'file_path': str(file_path),
                        'spawns': spawns,
                        'file_type': 'yaml'
                    }
                    
                    # Store for reference
                    if 'creature' in category.lower():
                        self.creature_lists.update(spawns)
                    elif 'loot' in category.lower():
                        self.loot_lists.update(spawns)
                    elif 'pickable' in category.lower():
                        self.pickable_lists.update(spawns)
        
        # Second pass: Extract CFG locations
        for file_path in files:
            if file_path.suffix.lower() == '.cfg':
                print(f"Processing CFG: {file_path.name}")
                
                category = self.categorize_file(file_path)
                if category not in categorized_data:
                    categorized_data[category] = {}
                
                locations = self.extract_locations_from_cfg(file_path)
                
                if locations:
                    categorized_data[category][file_path.name] = {
                        'file_path': str(file_path),
                        'locations': locations,
                        'file_type': 'cfg'
                    }
        
        return categorized_data
    
    def generate_markdown(self, categorized_data: Dict[str, Dict[str, Any]]) -> str:
        """Generate markdown documentation from the spawn data."""
        md_content = []
        
        # Header
        md_content.append("# More World Locations - Complete Spawn Documentation")
        md_content.append("")
        md_content.append("This document contains all spawn information from the warpalicious More World Locations mods.")
        md_content.append("")
        md_content.append("## Table of Contents")
        md_content.append("")
        
        # Generate TOC
        for category in sorted(categorized_data.keys()):
            if categorized_data[category]:
                md_content.append(f"- [{category}](#{category.lower().replace(' ', '-')})")
        
        md_content.append("")
        md_content.append("---")
        md_content.append("")
        
        # Generate content for each category
        for category in sorted(categorized_data.keys()):
            if not categorized_data[category]:
                continue
                
            md_content.append(f"## {category}")
            md_content.append("")
            
            for file_name, file_data in categorized_data[category].items():
                md_content.append(f"### {file_name}")
                md_content.append("")
                
                if file_data['file_type'] == 'yaml':
                    # Handle YAML files (creature/loot lists)
                    spawns = file_data['spawns']
                    if spawns:
                        for spawn_group, items in spawns.items():
                            md_content.append(f"#### {spawn_group}")
                            md_content.append("")
                            
                            if items:
                                for item in items:
                                    md_content.append(f"- {item}")
                                md_content.append("")
                            else:
                                md_content.append("*No items defined*")
                                md_content.append("")
                    else:
                        md_content.append("*No spawn data found*")
                        md_content.append("")
                
                elif file_data['file_type'] == 'cfg':
                    # Handle CFG files (location configurations)
                    locations = file_data['locations']
                    if locations:
                        for location_name, location_info in locations.items():
                            md_content.append(f"#### {location_name}")
                            md_content.append("")
                            
                            # Location details
                            if 'spawn_quantity' in location_info:
                                md_content.append(f"**Spawn Quantity**: {location_info['spawn_quantity']}")
                                md_content.append("")
                            
                            # Creature information
                            if 'use_custom_creatures' in location_info and location_info['use_custom_creatures']:
                                if 'creature_list' in location_info:
                                    creature_list_name = location_info['creature_list']
                                    md_content.append(f"**Creature List**: {creature_list_name}")
                                    
                                    # Show actual creatures if available
                                    if creature_list_name in self.creature_lists:
                                        md_content.append("")
                                        md_content.append("**Creatures**:")
                                        for creature in self.creature_lists[creature_list_name]:
                                            md_content.append(f"- {creature}")
                                        md_content.append("")
                                    else:
                                        md_content.append(" *(list not found)*")
                                    md_content.append("")
                            
                            # Loot information
                            if 'use_custom_loot' in location_info and location_info['use_custom_loot']:
                                if 'loot_list' in location_info:
                                    loot_list_name = location_info['loot_list']
                                    md_content.append(f"**Loot List**: {loot_list_name}")
                                    
                                    # Show actual loot if available
                                    if loot_list_name in self.loot_lists:
                                        md_content.append("")
                                        md_content.append("**Loot Items**:")
                                        for item in self.loot_lists[loot_list_name]:
                                            md_content.append(f"- {item}")
                                        md_content.append("")
                                    else:
                                        md_content.append(" *(list not found)*")
                                    md_content.append("")
                            
                            md_content.append("---")
                            md_content.append("")
                    else:
                        md_content.append("*No location data found*")
                        md_content.append("")
                
                md_content.append("---")
                md_content.append("")
        
        # Summary
        md_content.append("## Summary")
        md_content.append("")
        
        total_files = sum(len(files) for files in categorized_data.values())
        total_locations = sum(
            len(file_data.get('locations', {})) 
            for category in categorized_data.values() 
            for file_data in category.values()
            if file_data.get('file_type') == 'cfg'
        )
        total_spawn_groups = sum(
            len(file_data.get('spawns', {})) 
            for category in categorized_data.values() 
            for file_data in category.values()
            if file_data.get('file_type') == 'yaml'
        )
        
        md_content.append(f"- **Total Files Processed**: {total_files}")
        md_content.append(f"- **Total Locations**: {total_locations}")
        md_content.append(f"- **Total Spawn Groups**: {total_spawn_groups}")
        md_content.append(f"- **Categories**: {len([c for c in categorized_data.keys() if categorized_data[c]])}")
        md_content.append("")
        
        # File breakdown
        md_content.append("### Files by Category")
        md_content.append("")
        for category in sorted(categorized_data.keys()):
            if categorized_data[category]:
                md_content.append(f"- **{category}**: {len(categorized_data[category])} files")
        md_content.append("")
        
        # Creature list summary
        if self.creature_lists:
            md_content.append("### Creature Lists Summary")
            md_content.append("")
            for list_name, creatures in self.creature_lists.items():
                md_content.append(f"- **{list_name}**: {len(creatures)} creatures")
            md_content.append("")
        
        # Loot list summary
        if self.loot_lists:
            md_content.append("### Loot Lists Summary")
            md_content.append("")
            for list_name, items in self.loot_lists.items():
                md_content.append(f"- **{list_name}**: {len(items)} items")
            md_content.append("")
        
        return "\n".join(md_content)
    
    def save_markdown(self, content: str, output_path: Path) -> None:
        """Save the markdown content to a file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Markdown documentation saved to: {output_path}")
        except Exception as e:
            print(f"Error saving markdown: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract More World Locations spawn information")
    parser.add_argument("--config-dir", type=str, 
                       default="Valheim/profiles/Dogeheim_Player/BepInEx/config",
                       help="Path to the BepInEx config directory")
    parser.add_argument("--output", type=str,
                       default="Valheim_Help_Docs/Files for GPT/More_World_Locations_Spawns.md",
                       help="Output markdown file path")
    
    args = parser.parse_args()
    
    config_dir = Path(args.config_dir)
    output_path = Path(args.output)
    
    if not config_dir.exists():
        print(f"Config directory not found: {config_dir}")
        return 1
    
    print(f"Extracting spawns from: {config_dir}")
    print(f"Output will be saved to: {output_path}")
    print()
    
    extractor = MoreWorldLocationsSpawnExtractor(config_dir)
    
    # Extract all spawn data
    categorized_data = extractor.extract_all_spawns()
    
    if not categorized_data:
        print("No More World Locations files found or no spawn data extracted.")
        return 1
    
    # Generate markdown
    markdown_content = extractor.generate_markdown(categorized_data)
    
    # Save to file
    extractor.save_markdown(markdown_content, output_path)
    
    print("\nExtraction completed successfully!")
    return 0

if __name__ == "__main__":
    exit(main())
