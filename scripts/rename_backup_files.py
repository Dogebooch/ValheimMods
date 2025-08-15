#!/usr/bin/env python3
"""
Script to rename RelicHeim backup files with a clear prefix to avoid naming conflicts
with current user configuration files.
"""

import os
import shutil
from pathlib import Path

def rename_backup_files():
    """Rename all files in the RelicHeim backup with a clear prefix."""
    
    # Define paths
    backup_dir = Path("Valheim_Help_Docs/JewelHeim-RelicHeim-5.4.10Backup/config")
    backup_prefix = "BACKUP_5.4.10_"
    
    if not backup_dir.exists():
        print(f"Backup directory not found: {backup_dir}")
        return
    
    # Get all files in the backup config directory
    files_to_rename = []
    
    # Collect all .cfg and .yml files
    for file_path in backup_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.cfg', '.yml']:
            # Skip files that are already prefixed
            if not file_path.name.startswith(backup_prefix):
                files_to_rename.append(file_path)
    
    print(f"Found {len(files_to_rename)} files to rename")
    
    # Rename files
    renamed_count = 0
    for file_path in files_to_rename:
        try:
            # Create new filename with prefix
            new_name = f"{backup_prefix}{file_path.name}"
            new_path = file_path.parent / new_name
            
            # Rename the file
            file_path.rename(new_path)
            print(f"Renamed: {file_path.name} -> {new_name}")
            renamed_count += 1
            
        except Exception as e:
            print(f"Error renaming {file_path.name}: {e}")
    
    print(f"Successfully renamed {renamed_count} files")
    
    # Create a README file explaining the naming convention
    readme_content = f"""# RelicHeim Backup Files - Naming Convention

This directory contains backup files from RelicHeim version 5.4.10.
All files have been prefixed with "{backup_prefix}" to avoid naming conflicts with current user configuration files.

## File Naming Convention
- Original: `org.bepinex.plugins.sailing.cfg`
- Backup: `{backup_prefix}org.bepinex.plugins.sailing.cfg`

## Purpose
These files serve as reference material and backup copies of the original RelicHeim configuration.
They should not be confused with current user configuration files located in:
`Valheim/profiles/Dogeheim_Player/BepInEx/config/`

## Usage
When parsing or analyzing configuration files:
1. Current user configs: Use files WITHOUT the "{backup_prefix}" prefix
2. Reference/backup files: Use files WITH the "{backup_prefix}" prefix

This naming convention ensures no conflicts when comparing or processing configuration files.
"""
    
    readme_path = backup_dir / "BACKUP_README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"Created README file: {readme_path}")

if __name__ == "__main__":
    rename_backup_files()
