#!/usr/bin/env python3
"""
Copy Essential Context Files for AI Analysis
Copies important files that provide context for debugging, balance changes, and loot table building.
"""

import shutil
import pathlib
from datetime import datetime

def copy_essential_files():
    """Copy essential context files to @Valheim_Binary_Readable directory."""
    
    # Define source and destination paths
    base_dir = pathlib.Path(".")
    source_dir = base_dir / "Valheim_Help_Docs" / "VNEI-Export"
    config_dir = base_dir / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config"
    mods_file = base_dir / "Valheim" / "profiles" / "Dogeheim_Player" / "mods.yml"
    log_file = base_dir / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "LogOutput.log"
    dest_dir = base_dir / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
    
    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    copied_files = []
    
    # Copy VNEI item database files
    vnei_files = [
        "VNEI.indexed.items.csv",
        "VNEI.indexed.items.yml",
        "VNEI.indexed.items.txt"
    ]
    
    for file_name in vnei_files:
        source_file = source_dir / file_name
        dest_file = dest_dir / file_name
        if source_file.exists():
            shutil.copy2(source_file, dest_file)
            copied_files.append(f"VNEI: {file_name}")
            print(f"✅ Copied {file_name}")
    
    # Copy mods.yml
    if mods_file.exists():
        shutil.copy2(mods_file, dest_dir / "mods.yml")
        copied_files.append("mods.yml")
        print("✅ Copied mods.yml")
    
    # Copy log file
    if log_file.exists():
        shutil.copy2(log_file, dest_dir / "LogOutput.log")
        copied_files.append("LogOutput.log")
        print("✅ Copied LogOutput.log")
    
    # Copy essential config files
    essential_configs = [
        "randyknapp.mods.epicloot.cfg",
        "WackyMole.EpicMMOSystem.cfg", 
        "org.bepinex.plugins.creaturelevelcontrol.cfg",
        "warpalicious.More_World_Locations_LootLists.yml",
        "warpalicious.More_World_Locations_CreatureLists.yml",
        "kg.ValheimEnchantmentSystem.cfg",
        "shudnal.Seasons.cfg",
        "Therzie.Warfare.cfg",
        "Therzie.Armory.cfg",
        "blacks7ar.MagicRevamp.cfg"
    ]
    
    for config_name in essential_configs:
        source_config = config_dir / config_name
        if source_config.exists():
            shutil.copy2(source_config, dest_dir / config_name)
            copied_files.append(config_name)
            print(f"✅ Copied {config_name}")
        else:
            print(f"⚠️  Config not found: {config_name}")
    
    # Create a summary file
    summary_file = dest_dir / "context_files_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("Essential Context Files for AI Analysis\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("Files copied:\n")
        for file_name in copied_files:
            f.write(f"- {file_name}\n")
        f.write("\nPurpose:\n")
        f.write("- VNEI files: Complete item database for loot table building\n")
        f.write("- mods.yml: Mod list and dependencies for compatibility analysis\n")
        f.write("- Config files: Current mod settings for balance evaluation\n")
        f.write("- LogOutput.log: Mod loading and error information for debugging\n")
    
    print(f"\n📋 Summary written to: {summary_file}")
    print(f"📁 Total files copied: {len(copied_files)}")
    
    return copied_files

if __name__ == "__main__":
    print("Copying essential context files for AI analysis...")
    copied = copy_essential_files()
    print(f"\n✅ Completed! {len(copied)} files copied to @Valheim_Binary_Readable/") 