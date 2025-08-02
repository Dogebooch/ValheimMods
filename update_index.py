#!/usr/bin/env python3
"""
Script to update important_files.txt to include TYPE and IMPORTANCE_TAGS columns.
Transforms from: [SOURCE] <RELATIVE_PATH>
To: [SOURCE] <RELATIVE_PATH> | <TYPE> | <IMPORTANCE_TAGS>
"""

import re
import os

def determine_file_type(filepath):
    """Determine the file type based on extension and path."""
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
    """Determine importance tags based on file path and source."""
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

def update_index_file(input_file, output_file):
    """Update the index file with TYPE and IMPORTANCE_TAGS columns."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and the size header
        if not line or line.startswith('Total size'):
            updated_lines.append(line)
            continue
        
        # Parse the current format: [SOURCE] <RELATIVE_PATH>
        match = re.match(r'^(\[.*?\]) (.+)$', line)
        if match:
            source = match.group(1)
            relative_path = match.group(2)
            
            # Determine type and importance tags
            file_type = determine_file_type(relative_path)
            importance_tags = determine_importance_tags(relative_path, source)
            
            # Create new format: [SOURCE] <RELATIVE_PATH> | <TYPE> | <IMPORTANCE_TAGS>
            updated_line = f"{source} {relative_path} | {file_type} | {importance_tags}"
            updated_lines.append(updated_line)
        else:
            # Keep lines that don't match the expected format
            updated_lines.append(line)
    
    # Write the updated file
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in updated_lines:
            f.write(line + '\n')
    
    print(f"Updated index written to {output_file}")
    print(f"Processed {len(lines)} lines")

if __name__ == "__main__":
    input_file = "important_files.txt"
    output_file = "important_files_updated.txt"
    
    if os.path.exists(input_file):
        update_index_file(input_file, output_file)
    else:
        print(f"Error: {input_file} not found") 