#!/usr/bin/env python3
"""
Run Enhanced Material Analysis
This script demonstrates the enhanced material drop chance analysis.
"""

import sys
from pathlib import Path

# Add the emt directory to the path
sys.path.insert(0, str(Path(__file__).parent / "emt"))

from enhanced_calculator import EnhancedMaterialCalculator
from compare import compare_snapshots, generate_detailed_report
from db import DB

def main():
    """Run the enhanced analysis"""
    
    # Configuration
    config_root = "Valheim/profiles/Dogeheim_Player/BepInEx/config"  # Adjust path as needed
    db_path = "emt.sqlite3"
    
    print("=== Enhanced Material Drop Chance Analysis ===")
    print()
    
    # Step 1: Calculate baseline chances
    print("Step 1: Calculating baseline drop chances...")
    calculator = EnhancedMaterialCalculator(config_root)
    baseline_chances = calculator.calculate_baseline_chances()
    
    print("\nBaseline Drop Chances:")
    print("======================")
    
    # Show baseline for Runestone materials
    runestone_materials = ["RunestoneMagic", "RunestoneRare", "RunestoneEpic", "RunestoneLegendary", "RunestoneMythic"]
    
    for material in runestone_materials:
        if material in baseline_chances:
            print(f"\n{material}:")
            for source_type, chance in baseline_chances[material].items():
                print(f"  {source_type}: {chance:.2f}%")
        else:
            print(f"\n{material}: Not found in baseline")
    
    # Step 2: Compare with current configuration (if database exists)
    db_file = Path(db_path)
    if db_file.exists():
        print("\n" + "="*50)
        print("Step 2: Comparing with current configuration...")
        
        db = DB(db_path)
        
        # Get latest snapshots
        baseline_id = db.latest_snapshot_id_for_root(config_root)
        if baseline_id:
            # For demonstration, compare baseline with itself
            # In practice, you'd compare with a different snapshot
            comparison = compare_snapshots(db_path, baseline_id, baseline_id)
            
            print("\nComparison Results:")
            print("===================")
            
            for result in comparison:
                if result["material"] in runestone_materials:
                    material = result["material"]
                    total_base = result["total_base"]
                    total_current = result["total_current"]
                    total_change = result["pct_change_total"]
                    
                    print(f"\n{material}:")
                    print(f"  Total Baseline: {total_base:.2f}%")
                    print(f"  Total Current: {total_current:.2f}%")
                    print(f"  Change: {total_change:+.1f}%")
                    
                    # Show by source type
                    by_type = result.get("by_source_type", {})
                    for source_type, data in by_type.items():
                        print(f"  {source_type.capitalize()}: {data['baseline']:.2f}% baseline, {data['current']:.2f}% current")
        
        db.close()
    else:
        print(f"\nNo database found at {db_path}")
        print("Run the EnchantingMaterialTracker first to create snapshots.")
    
    print("\n" + "="*50)
    print("Analysis Complete!")
    print("\nTo fix the baseline issue:")
    print("1. Run: python recreate_baseline.py <config_path> --verify")
    print("2. Run: python -m emt (the main EnchantingMaterialTracker)")
    print("3. Compare the new baseline with current configuration")

if __name__ == "__main__":
    main()
