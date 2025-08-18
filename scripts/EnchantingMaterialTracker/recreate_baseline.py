#!/usr/bin/env python3
"""
Recreate Baseline Snapshot with Proper RelicHeim Configuration
This script recreates the baseline snapshot to ensure proper baseline values are calculated.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import sqlite3

# Add the emt directory to the path
sys.path.insert(0, str(Path(__file__).parent / "emt"))

from emt.db import DB
from emt.scanner import map_files
from emt.registry import PARSERS
from emt.models import MaterialMetric

def load_settings():
    """Load settings from settings.json"""
    settings_file = Path(__file__).parent / "settings.json"
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            return json.load(f)
    return {}

def recreate_baseline(config_root: str, db_path: str = None):
    """Recreate the baseline snapshot with proper configuration"""
    
    if db_path is None:
        db_path = str(Path(__file__).parent / "emt.sqlite3")
    
    print(f"Recreating baseline snapshot for: {config_root}")
    print(f"Database: {db_path}")
    
    # Load settings
    settings = load_settings()
    scan_globs = settings.get("scan_globs", {})
    
    # Initialize database
    db = DB(db_path)
    
    # Create new snapshot
    created_at = datetime.now().isoformat()
    snapshot_id = db.insert_snapshot(config_root, created_at)
    
    print(f"Created snapshot ID: {snapshot_id}")
    
    # Scan all files
    all_metrics = []
    
    for source_type, file_path in map_files(config_root, scan_globs):
        print(f"Scanning: {source_type} - {file_path}")
        
        # Get parser for this source type
        parser_class = PARSERS.get(source_type)
        if not parser_class:
            print(f"  No parser found for {source_type}")
            continue
        
        parser = parser_class()
        
        # Get materials and aliases
        materials_file = Path(__file__).parent / "materials.json"
        materials = set()
        aliases = {}
        
        if materials_file.exists():
            with open(materials_file, 'r') as f:
                data = json.load(f)
                for tier_materials in data.get("tiers", {}).values():
                    materials.update(tier_materials)
                aliases = data.get("aliases", {})
        
        try:
            # Parse file
            metrics = list(parser.parse(str(file_path), materials, aliases))
            all_metrics.extend(metrics)
            print(f"  Found {len(metrics)} material entries")
            
        except Exception as e:
            print(f"  Error parsing {file_path}: {e}")
    
    # Insert all metrics into database
    print(f"Inserting {len(all_metrics)} total metrics...")
    db.insert_metrics(snapshot_id, all_metrics)
    
    # Close database
    db.close()
    
    print(f"Baseline snapshot {snapshot_id} created successfully!")
    print(f"Total materials found: {len(all_metrics)}")
    
    return snapshot_id

def verify_baseline(db_path: str, snapshot_id: int):
    """Verify the baseline snapshot has proper data"""
    
    db = DB(db_path)
    
    # Get metrics for this snapshot
    metrics = db.fetch_snapshot_metrics(snapshot_id)
    
    print(f"\nVerifying baseline snapshot {snapshot_id}:")
    print(f"Total metric entries: {len(metrics)}")
    
    # Group by material
    material_totals = {}
    for material, source, score in metrics:
        if material not in material_totals:
            material_totals[material] = 0.0
        material_totals[material] += score
    
    print(f"\nMaterial totals:")
    for material, total in sorted(material_totals.items()):
        print(f"  {material}: {total:.2f}")
    
    # Check for zero totals (problematic)
    zero_totals = [mat for mat, total in material_totals.items() if total == 0.0]
    if zero_totals:
        print(f"\nWARNING: Materials with zero totals (baseline issue):")
        for mat in zero_totals:
            print(f"  {mat}")
    
    db.close()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Recreate Baseline Snapshot")
    parser.add_argument("config_root", help="Path to Valheim config directory")
    parser.add_argument("--db", help="Database path (default: emt.sqlite3)")
    parser.add_argument("--verify", action="store_true", help="Verify baseline after creation")
    
    args = parser.parse_args()
    
    # Recreate baseline
    snapshot_id = recreate_baseline(args.config_root, args.db)
    
    # Verify if requested
    if args.verify:
        db_path = args.db or str(Path(__file__).parent / "emt.sqlite3")
        verify_baseline(db_path, snapshot_id)
    
    print(f"\nBaseline recreation complete!")
    print(f"Snapshot ID: {snapshot_id}")
    print(f"You can now run the EnchantingMaterialTracker to compare against this baseline.")

if __name__ == "__main__":
    main()
