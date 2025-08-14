#!/usr/bin/env python3
"""
Validate that all prefabs in Detalhes.ItemRequiresSkillLevel.yml exist in VNEI item list.
"""

import re
from pathlib import Path
from typing import Set, List, Tuple


def load_vnei_items(vnei_dir: Path) -> Set[str]:
    """Load all item names from VNEI export files."""
    items: Set[str] = set()
    
    # Try CSV first, then TXT
    csv_file = vnei_dir / "VNEI.indexed.items.csv"
    txt_file = vnei_dir / "VNEI.indexed.items.txt"
    
    source_file = None
    if csv_file.exists():
        source_file = csv_file
    elif txt_file.exists():
        source_file = txt_file
    
    if not source_file:
        print(f"Warning: No VNEI export files found in {vnei_dir}")
        return items
    
    try:
        import csv
        with open(source_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Try different possible column names for internal name
                internal_name = (
                    row.get('Internal Name', '') or 
                    row.get('internalname', '') or 
                    row.get('Name', '') or
                    row.get('name', '')
                ).strip()
                if internal_name:
                    items.add(internal_name)
    except Exception as e:
        print(f"Error reading VNEI file: {e}")
    
    return items


def extract_yaml_prefabs(yaml_path: Path) -> List[Tuple[str, int]]:
    """Extract all PrefabName entries from the YAML file with their line numbers."""
    prefabs: List[Tuple[str, int]] = []
    
    if not yaml_path.exists():
        print(f"Error: YAML file not found: {yaml_path}")
        return prefabs
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # Match PrefabName lines
                match = re.match(r'^\s*-\s*PrefabName:\s*(.+?)\s*$', line)
                if match:
                    prefab_name = match.group(1).strip()
                    prefabs.append((prefab_name, line_num))
    except Exception as e:
        print(f"Error reading YAML file: {e}")
    
    return prefabs


def validate_prefabs(yaml_prefabs: List[Tuple[str, int]], vnei_items: Set[str]) -> Tuple[List[str], List[Tuple[str, int]]]:
    """Validate prefabs and return lists of valid and invalid ones."""
    valid_prefabs: List[str] = []
    invalid_prefabs: List[Tuple[str, int]] = []
    
    for prefab, line_num in yaml_prefabs:
        if prefab in vnei_items:
            valid_prefabs.append(prefab)
        else:
            invalid_prefabs.append((prefab, line_num))
    
    return valid_prefabs, invalid_prefabs


def main():
    # Setup paths
    repo_root = Path(__file__).resolve().parents[1]
    yaml_path = repo_root / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config" / "Detalhes.ItemRequiresSkillLevel.yml"
    vnei_dir = repo_root / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "VNEI-Export"
    
    print("Validating YAML prefabs against VNEI item list...")
    print(f"YAML file: {yaml_path}")
    print(f"VNEI directory: {vnei_dir}")
    print()
    
    # Load VNEI items
    print("Loading VNEI items...")
    vnei_items = load_vnei_items(vnei_dir)
    print(f"Found {len(vnei_items)} items in VNEI export")
    
    # Extract YAML prefabs
    print("Extracting prefabs from YAML...")
    yaml_prefabs = extract_yaml_prefabs(yaml_path)
    print(f"Found {len(yaml_prefabs)} prefab entries in YAML")
    
    # Validate
    print("Validating prefabs...")
    valid_prefabs, invalid_prefabs = validate_prefabs(yaml_prefabs, vnei_items)
    
    # Report results
    print()
    print("=== VALIDATION RESULTS ===")
    print(f"Total prefabs in YAML: {len(yaml_prefabs)}")
    print(f"Valid prefabs: {len(valid_prefabs)}")
    print(f"Invalid prefabs: {len(invalid_prefabs)}")
    print()
    
    if invalid_prefabs:
        print("=== INVALID PREFABS ===")
        print("These prefabs in the YAML file were not found in the VNEI item list:")
        print()
        for prefab, line_num in invalid_prefabs:
            print(f"Line {line_num}: {prefab}")
        
        # Try to find similar names for suggestions
        print()
        print("=== SUGGESTIONS ===")
        print("Similar names found in VNEI (case-insensitive):")
        for prefab, line_num in invalid_prefabs:
            suggestions = []
            prefab_lower = prefab.lower()
            for vnei_item in vnei_items:
                if prefab_lower in vnei_item.lower() or vnei_item.lower() in prefab_lower:
                    suggestions.append(vnei_item)
            
            if suggestions:
                print(f"  {prefab} (line {line_num}):")
                for suggestion in suggestions[:5]:  # Limit to 5 suggestions
                    print(f"    -> {suggestion}")
                if len(suggestions) > 5:
                    print(f"    ... and {len(suggestions) - 5} more")
                print()
    else:
        print("✅ All prefabs in the YAML file are valid!")
    
    return 0 if not invalid_prefabs else 1


if __name__ == "__main__":
    exit(main())
