#!/usr/bin/env python3
"""
Unified Valheim Index Generator
Combines functionality to:
1. Generate initial index from source directory
2. Update existing index with TYPE and IMPORTANCE_TAGS columns
3. Support both operations in one script
"""

import os
import re
from pathlib import Path

# Configuration
SOURCE_DIR = r"C:\Users\drumm\OneDrive\Desktop\Valheim_Testing\Valheim"
OUTPUT_FILE = r"C:\Users\drumm\OneDrive\Desktop\Valheim_Testing\important_files.txt"
UPDATED_OUTPUT_FILE = r"C:\Users\drumm\OneDrive\Desktop\Valheim_Testing\important_files_updated.txt"

# File types to include (gameplay-affecting configs & code)
INCLUDE_EXT = {
    ".cfg", ".json", ".cs", ".lua", ".ini",
    ".yaml", ".yml", ".toml", ".xml", ".asset"
}

# Ignore large/unnecessary files
EXCLUDE_EXT = {
    ".dll", ".png", ".jpg", ".jpeg", ".tga", ".psd",
    ".mp3", ".wav", ".ogg"
}

# Auto-tagging rules for initial generation
TAG_RULES = {
    "drop": "drop_rates",
    "loot": "drop_rates",
    "epicloot": "loot_tables",
    "spawn": "spawns",
    "creature": "spawns",
    "npc": "spawns",
    "craft": "crafting",
    "recipe": "crafting",
    "objectdb": "item_database",
    "item": "item_database",
    "biome": "biomes",
    "world": "worldgen"
}

def get_tags(filename):
    """Generate importance tags based on filename keywords for initial generation."""
    tags = set()
    lower_name = filename.lower()
    for key, tag in TAG_RULES.items():
        if key in lower_name:
            tags.add(tag)
    return ", ".join(sorted(tags)) if tags else "misc"

def determine_file_type(filepath):
    """Determine the file type based on extension and path for updating."""
    ext = os.path.splitext(filepath)[1].lower()
    
    # Configuration files
    if ext in ['.cfg', '.yml', '.yaml', '.json', '.xml', '.ini']:
        return 'CONFIG'
    
    # Documentation files
    if ext in ['.md', '.txt']:
        return 'DOCS'
    
    # Code files
    if ext in ['.cs', '.dll', '.exe', '.sh']:
        return 'CODE'
    
    # Data files
    if ext in ['.manifest', '.assets', '.resS']:
        return 'DATA'
    
    # Image files
    if ext in ['.png', '.jpg', '.jpeg']:
        return 'ASSET'
    
    # Archive files
    if ext in ['.zip']:
        return 'ARCHIVE'
    
    # Default
    return 'OTHER'

def determine_importance_tags(filepath, source):
    """Determine importance tags based on file path and source for updating."""
    tags = []
    
    # Base importance based on source
    if source == '[BASE GAME]':
        tags.append('CORE')
    elif source == '[MODDED]':
        tags.append('MOD')
    
    # High importance files
    if any(keyword in filepath.lower() for keyword in [
        'manifest.json', 'readme.md', 'changelog.md', 'config', 'boot.config',
        'doorstop_config.ini', 'steam_appid.txt'
    ]):
        tags.append('CRITICAL')
    
    # Configuration importance
    if any(keyword in filepath.lower() for keyword in [
        'epicloot', 'enchantment', 'drop_that', 'spawn_that', 'custom_raids',
        'wackysdatabase', 'valheimenchantmentsystem'
    ]):
        tags.append('CONFIG')
    
    # Documentation importance
    if any(keyword in filepath.lower() for keyword in [
        'readme', 'changelog', 'guide', 'documentation'
    ]):
        tags.append('DOCS')
    
    # Translation importance
    if 'translation' in filepath.lower() or any(lang in filepath.lower() for lang in [
        'english', 'chinese', 'french', 'german', 'spanish', 'russian'
    ]):
        tags.append('LOCALE')
    
    # Mod-specific importance
    if 'jewelheim' in filepath.lower():
        tags.append('MODPACK')
    
    # If no specific tags, add general importance
    if not tags:
        tags.append('GENERAL')
    
    return ','.join(tags)

def generate_initial_index():
    """Generate initial index from source directory."""
    important_files = []
    total_size = 0

    print(f"Scanning directory: {SOURCE_DIR}")
    
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in INCLUDE_EXT and ext not in EXCLUDE_EXT:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                total_size += size

                rel_path = os.path.relpath(filepath, SOURCE_DIR)
                tags = get_tags(file)

                important_files.append((rel_path, ext[1:], tags, filepath))

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"Total size of included files: {total_size / (1024*1024):.2f} MB\n\n")
        for rel_path, ftype, tags, full_path in important_files:
            f.write(f"[SOURCE] {rel_path} | {ftype} | {tags}\n")
            f.write(f"file:///{full_path.replace(os.sep, '/')}\n\n")

    print(f"✅ Initial index created: {OUTPUT_FILE}")
    print(f"📊 Total files: {len(important_files)}")
    print(f"📦 Total size: {total_size / (1024*1024):.2f} MB")

def update_existing_index():
    """Update existing index with TYPE and IMPORTANCE_TAGS columns."""
    
    if not os.path.exists(OUTPUT_FILE):
        print(f"❌ Error: {OUTPUT_FILE} not found")
        return
    
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and the size header
        if not line or line.startswith('Total size'):
            updated_lines.append(line)
            continue
        
        # Parse the current format: [SOURCE] <RELATIVE_PATH> | <TYPE> | <TAGS>
        match = re.match(r'^(\[.*?\]) (.+?) \| (.+?) \| (.+)$', line)
        if match:
            source = match.group(1)
            relative_path = match.group(2)
            existing_type = match.group(3)
            existing_tags = match.group(4)
            
            # Determine enhanced type and importance tags
            file_type = determine_file_type(relative_path)
            importance_tags = determine_importance_tags(relative_path, source)
            
            # Create new format: [SOURCE] <RELATIVE_PATH> | <TYPE> | <IMPORTANCE_TAGS>
            updated_line = f"{source} {relative_path} | {file_type} | {importance_tags}"
            updated_lines.append(updated_line)
        else:
            # Keep lines that don't match the expected format
            updated_lines.append(line)
    
    # Write the updated file
    with open(UPDATED_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for line in updated_lines:
            f.write(line + '\n')
    
    print(f"✅ Updated index written to: {UPDATED_OUTPUT_FILE}")
    print(f"📊 Processed {len(lines)} lines")

def main():
    """Main function with command line interface."""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "generate":
            print("🔄 Generating initial index...")
            generate_initial_index()
        elif command == "update":
            print("🔄 Updating existing index...")
            update_existing_index()
        elif command == "both":
            print("🔄 Generating initial index...")
            generate_initial_index()
            print("\n🔄 Updating index with enhanced metadata...")
            update_existing_index()
        else:
            print("❌ Unknown command. Use: generate, update, or both")
    else:
        # Default behavior: ask user what to do
        print("🔧 Unified Valheim Index Generator")
        print("=" * 40)
        print("1. Generate initial index from source directory")
        print("2. Update existing index with enhanced metadata")
        print("3. Do both (generate then update)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            generate_initial_index()
        elif choice == "2":
            update_existing_index()
        elif choice == "3":
            generate_initial_index()
            print("\n" + "="*40)
            update_existing_index()
        elif choice == "4":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 