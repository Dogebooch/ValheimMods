#!/usr/bin/env python3
"""
Identify and Copy Valuable Context Files for AI Analysis
Scans Valheim directories for files that provide invaluable context for:
- Game mechanics modification
- Loot table building
- Skill progression analysis
- Difficulty balancing
- Boss/item addition
- Debugging
- GUI development (prefabs, images, recipes)
"""

import shutil
import pathlib
import json
from datetime import datetime

def identify_valuable_files():
    """Identify files that provide valuable context for AI analysis."""
    
    base_dir = pathlib.Path(".")
    dest_dir = base_dir / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
    
    valuable_files = []
    
    # 1. GAME FILES - Core game data and assets
    game_files_dir = base_dir / "Valheim_GameFiles"
    
    # Loot system guide
    loot_guide = game_files_dir / "LOOT_SYSTEM_GUIDE.md"
    if loot_guide.exists():
        valuable_files.append({
            'source': loot_guide,
            'dest': dest_dir / "LOOT_SYSTEM_GUIDE.md",
            'category': 'Game Design',
            'description': 'Comprehensive loot system design and balance guide'
        })
    
    # Game manifest files
    manifest_file = game_files_dir / "valheim_Data" / "StreamingAssets" / "SoftRef" / "manifest"
    if manifest_file.exists():
        valuable_files.append({
            'source': manifest_file,
            'dest': dest_dir / "game_manifest.txt",
            'category': 'Game Assets',
            'description': 'Game asset bundle manifest with prefab dependencies'
        })
    
    # 2. MOD PLUGIN FILES - DLLs with mod data
    plugins_dir = base_dir / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "plugins"
    
    # Key mod DLLs that contain valuable data
    key_mods = [
        "RandyKnapp-EpicLoot/EpicLoot.dll",
        "Therzie-Armory/Armory.dll", 
        "blacks7ar-MagicRevamp/MagicRevamp.dll",
        "WackyMole-WackyEpicMMOSystem/EpicMMOSystem.dll",
        "WackyMole-WackysDatabase/WackysDatabase.dll",
        "Therzie-Warfare/Warfare.dll",
        "Therzie-Monstrum/Monstrum.dll",
        "Therzie-Wizardry/Wizardry.dll"
    ]
    
    for mod_path in key_mods:
        mod_file = plugins_dir / mod_path
        if mod_file.exists():
            mod_name = mod_path.split('/')[0]
            valuable_files.append({
                'source': mod_file,
                'dest': dest_dir / f"{mod_name}.dll",
                'category': 'Mod Data',
                'description': f'Mod DLL containing {mod_name} data and configurations'
            })
    
    # 3. MOD DOCUMENTATION - README files with mod info
    mod_docs = [
        "RandyKnapp-EpicLoot/README.md",
        "Therzie-Armory/README.md",
        "blacks7ar-MagicRevamp/README.md",
        "WackyMole-WackysDatabase/README.md",
        "Therzie-Warfare/README.md",
        "Therzie-Monstrum/README.md"
    ]
    
    for doc_path in mod_docs:
        doc_file = plugins_dir / doc_path
        if doc_file.exists():
            mod_name = doc_path.split('/')[0]
            valuable_files.append({
                'source': doc_file,
                'dest': dest_dir / f"{mod_name}_README.md",
                'category': 'Mod Documentation',
                'description': f'Documentation for {mod_name} mod'
            })
    
    # 4. GAME ICONS - For GUI development
    icons_dir = base_dir / "Valheim_PlayerWorldData" / "Jotunn" / "CachedIcons"
    if icons_dir.exists():
        # Copy a sample of icons (first 50) for GUI development
        icon_files = list(icons_dir.glob("*.png"))[:50]
        for icon_file in icon_files:
            valuable_files.append({
                'source': icon_file,
                'dest': dest_dir / "icons" / icon_file.name,
                'category': 'GUI Assets',
                'description': f'Game icon for {icon_file.stem}'
            })
    
    # 5. GAME ASSEMBLIES - Core game data
    assemblies_dir = base_dir / "Valheim_GameFiles" / "valheim_Data" / "Managed"
    core_assemblies = [
        "Assembly-CSharp.dll",  # Main game assembly
        "gui_framework.dll",    # GUI framework
        "assembly_utils.dll"    # Utility functions
    ]
    
    for assembly in core_assemblies:
        assembly_file = assemblies_dir / assembly
        if assembly_file.exists():
            valuable_files.append({
                'source': assembly_file,
                'dest': dest_dir / assembly,
                'category': 'Game Core',
                'description': f'Core game assembly: {assembly}'
            })
    
    # 6. MOD CONFIGURATION DIRECTORIES - Unique mod data structures
    config_dir = base_dir / "Valheim" / "profiles" / "Dogeheim_Player" / "BepInEx" / "config"
    
    # Copy entire mod config directories that contain structured data
    mod_config_dirs = [
        "EpicLoot",
        "EpicMMOSystem", 
        "ValheimEnchantmentSystem",
        "wackysDatabase"
    ]
    
    for config_dir_name in mod_config_dirs:
        config_subdir = config_dir / config_dir_name
        if config_subdir.exists() and config_subdir.is_dir():
            # Copy the entire directory
            dest_subdir = dest_dir / f"config_{config_dir_name}"
            valuable_files.append({
                'source': config_subdir,
                'dest': dest_subdir,
                'category': 'Mod Configuration Data',
                'description': f'Complete configuration data for {config_dir_name}',
                'is_directory': True
            })
    
    # 7. WARPALICIOUS LOOT AND CREATURE LISTS - Unique structured data
    warpalicious_files = [
        "warpalicious.More_World_Locations_LootLists.yml",
        "warpalicious.More_World_Locations_CreatureLists.yml"
    ]
    
    for warpalicious_file in warpalicious_files:
        source_file = config_dir / warpalicious_file
        if source_file.exists():
            valuable_files.append({
                'source': source_file,
                'dest': dest_dir / warpalicious_file,
                'category': 'World Content',
                'description': f'Warpalicious {warpalicious_file} - structured world content data'
            })
    
    return valuable_files

def copy_valuable_files(valuable_files):
    """Copy identified valuable files to the destination directory."""
    
    base_dir = pathlib.Path(".")
    dest_dir = base_dir / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
    
    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Create icons subdirectory
    icons_dir = dest_dir / "icons"
    icons_dir.mkdir(exist_ok=True)
    
    copied_files = []
    total_size = 0
    
    for file_info in valuable_files:
        try:
            if file_info['source'].exists():
                if file_info.get('is_directory', False):
                    # Copy entire directory
                    if file_info['dest'].exists():
                        shutil.rmtree(file_info['dest'])
                    shutil.copytree(file_info['source'], file_info['dest'])
                    # Calculate directory size
                    dir_size = sum(f.stat().st_size for f in file_info['source'].rglob('*') if f.is_file())
                    total_size += dir_size
                    copied_files.append({
                        'name': file_info['dest'].name,
                        'category': file_info['category'],
                        'description': file_info['description'],
                        'size_mb': dir_size / (1024 * 1024)
                    })
                    print(f"✅ Copied directory {file_info['dest'].name} ({dir_size / (1024 * 1024):.1f}MB)")
                else:
                    # Copy single file
                    shutil.copy2(file_info['source'], file_info['dest'])
                    file_size = file_info['source'].stat().st_size
                    total_size += file_size
                    copied_files.append({
                        'name': file_info['dest'].name,
                        'category': file_info['category'],
                        'description': file_info['description'],
                        'size_mb': file_size / (1024 * 1024)
                    })
                    print(f"✅ Copied {file_info['dest'].name} ({file_size / (1024 * 1024):.1f}MB)")
        except Exception as e:
            print(f"❌ Failed to copy {file_info['source']}: {e}")
    
    return copied_files, total_size

def create_context_summary(copied_files, total_size):
    """Create a summary of the copied context files."""
    
    base_dir = pathlib.Path(".")
    dest_dir = base_dir / "Valheim_Help_Docs" / "@Valheim_Binary_Readable"
    
    summary_file = dest_dir / "ai_context_summary.txt"
    
    with open(summary_file, 'w') as f:
        f.write("AI Context Files Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total files: {len(copied_files)}\n")
        f.write(f"Total size: {total_size / (1024 * 1024):.1f}MB\n\n")
        
        f.write("File Categories:\n")
        f.write("-" * 20 + "\n")
        
        categories = {}
        for file_info in copied_files:
            cat = file_info['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(file_info)
        
        for category, files in categories.items():
            f.write(f"\n{category} ({len(files)} files):\n")
            for file_info in files:
                f.write(f"  - {file_info['name']} ({file_info['size_mb']:.1f}MB)\n")
                f.write(f"    {file_info['description']}\n")
        
        f.write("\n\nAI Analysis Use Cases:\n")
        f.write("-" * 25 + "\n")
        f.write("1. Game Design: Loot system guide for balance understanding\n")
        f.write("2. Mod Data: DLL files contain mod configurations and data structures\n")
        f.write("3. Mod Documentation: README files explain mod capabilities\n")
        f.write("4. GUI Assets: Icons for building interactive item databases\n")
        f.write("5. Game Core: Assembly files for understanding game mechanics\n")
        f.write("6. Mod Configuration Data: Structured mod data directories\n")
        f.write("7. World Content: Loot lists and creature spawn data\n")
    
    print(f"\n📋 Context summary written to: {summary_file}")

def main():
    """Main function to identify and copy valuable context files."""
    
    print("🔍 Identifying valuable context files for AI analysis...")
    valuable_files = identify_valuable_files()
    
    print(f"\n📁 Found {len(valuable_files)} valuable files")
    
    print("\n📋 Copying files to @Valheim_Binary_Readable/...")
    copied_files, total_size = copy_valuable_files(valuable_files)
    
    print(f"\n✅ Successfully copied {len(copied_files)} files ({total_size / (1024 * 1024):.1f}MB)")
    
    print("\n📝 Creating context summary...")
    create_context_summary(copied_files, total_size)
    
    print(f"\n🎯 AI Context Enhancement Complete!")
    print(f"📊 Total context files: {len(copied_files)}")
    print(f"💾 Total size added: {total_size / (1024 * 1024):.1f}MB")

if __name__ == "__main__":
    main() 