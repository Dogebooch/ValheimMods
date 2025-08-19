#!/usr/bin/env python3
"""
Generate a CHANGELOG.md for Dogeheim based on config tracker data
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def get_mod_name(file_path: str) -> str:
    """Extract mod name from file path."""
    # Handle EpicLoot patches specially
    if 'EpicLoot' in file_path and 'patches' in file_path:
        if 'RelicHeimPatches' in file_path:
            return 'EpicLoot RelicHeim Patches'
        else:
            return 'EpicLoot Patches'
    
    # Handle RelicHeim files
    if '_RelicHeimFiles' in file_path:
        return 'RelicHeim Configuration'
    
    if '.' in file_path:
        parts = file_path.split('.')
        if len(parts) >= 2:
            return parts[0]  # First part is usually mod name
    return Path(file_path).stem

def parse_cfg_like(text: str) -> dict:
    """Parse config file content into key-value pairs."""
    data = {}
    current_section = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(('#', ';', '//')):
            continue
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1].strip()
            continue
        m = re.match(r"^([^#;=:\n]+?)\s*[:=]\s*(.*)$", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            full_key = f"{current_section}.{key}" if current_section else key
            data[full_key] = val
    return data

def analyze_file_changes(current_content: str, initial_content: str, file_path: str) -> list:
    """Analyze changes in a config file and return meaningful changes."""
    changes = []
    
    try:
        # Parse both versions
        current_kv = parse_cfg_like(current_content)
        initial_kv = parse_cfg_like(initial_content)
        
        # Find changes
        for key in sorted(set(current_kv.keys()) | set(initial_kv.keys())):
            old_val = initial_kv.get(key)
            new_val = current_kv.get(key)
            
            if old_val != new_val:
                if old_val is None:
                    changes.append(f"Added: {key} = {new_val}")
                elif new_val is None:
                    changes.append(f"Removed: {key} (was {old_val})")
                else:
                    changes.append(f"Changed: {key} from {old_val} to {new_val}")
    
    except Exception as e:
        # Fallback for non-config files
        current_lines = set(current_content.splitlines())
        initial_lines = set(initial_content.splitlines())
        
        added = len(current_lines - initial_lines)
        removed = len(initial_lines - current_lines)
        
        if added or removed:
            changes.append(f"Content modified: +{added} lines, -{removed} lines")
    
    return changes

def generate_changelog():
    """Generate changelog from snapshots."""
    snapshots_dir = Path('scripts/snapshots')
    
    try:
        # Load snapshots
        with open(snapshots_dir / 'current_snapshot.json', 'r', encoding='utf-8', errors='replace') as f:
            current = json.load(f)
        with open(snapshots_dir / 'initial_snapshot.json', 'r', encoding='utf-8', errors='replace') as f:
            initial = json.load(f)
        
        current_files = current.get('files', {})
        initial_files = initial.get('files', {})
        
        # Group changes by mod
        mod_changes = defaultdict(list)
        
        print("Analyzing changes...")
        
        # Analyze each changed file - focus on configuration changes
        for file_path, file_info in current_files.items():
            if file_path.startswith('.snapshots'):
                continue  # Skip our own snapshot files
                
            mod_name = get_mod_name(file_path)
            
            if file_path in initial_files:
                # Check if modified
                if file_info.get('hash') != initial_files[file_path].get('hash'):
                    current_content = file_info.get('content', '')
                    initial_content = initial_files[file_path].get('content', '')
                    
                    file_changes = analyze_file_changes(current_content, initial_content, file_path)
                    if file_changes:
                        mod_changes[mod_name].append({
                            'type': 'Modified',
                            'file': file_path,
                            'changes': file_changes[:5]  # Limit to 5 most important changes
                        })
            else:
                # Only include new files if they're actual config files, not patches
                if file_path.endswith(('.cfg', '.yml', '.yaml')) and not 'patches' in file_path.lower():
                    mod_changes[mod_name].append({
                        'type': 'Added',
                        'file': file_path,
                        'changes': ['New configuration file']
                    })
        
        # Check for deleted files
        for file_path in initial_files:
            if file_path not in current_files and not file_path.startswith('.snapshots'):
                mod_name = get_mod_name(file_path)
                mod_changes[mod_name].append({
                    'type': 'Removed',
                    'file': file_path,
                    'changes': ['Configuration file removed']
                })
        
        # Generate changelog content
        modified_count = sum(1 for mod in mod_changes.values() for change in mod if change['type'] == 'Modified')
        added_count = sum(1 for mod in mod_changes.values() for change in mod if change['type'] == 'Added')
        removed_count = sum(1 for mod in mod_changes.values() for change in mod if change['type'] == 'Removed')
        
        changelog_content = f"""# Dogeheim Modpack Changelog

## Session {current.get('session', 'Unknown')} - {datetime.now().strftime('%Y-%m-%d')}

*Configuration changes that affect gameplay - automatically generated from tracked changes.*

### Summary
- **Modified configurations**: {modified_count}
- **New configurations**: {added_count}
- **Removed configurations**: {removed_count}

### Configuration Changes by Mod

"""
        
        # Add changes by mod
        for mod_name in sorted(mod_changes.keys()):
            changes = mod_changes[mod_name]
            if not changes:
                continue
                
            changelog_content += f"#### {mod_name}\n\n"
            
            for change in changes:
                if change['type'] == 'Modified':
                    changelog_content += f"**Configuration Changes** in `{change['file']}`:\n"
                    if change['changes']:
                        for detail in change['changes']:
                            changelog_content += f"  - {detail}\n"
                elif change['type'] == 'Added':
                    changelog_content += f"**New Configuration**: `{change['file']}`\n"
                elif change['type'] == 'Removed':
                    changelog_content += f"**Removed Configuration**: `{change['file']}`\n"
                changelog_content += "\n"
        
        changelog_content += f"""
---

**Note**: This changelog focuses on configuration changes that affect gameplay. 
Patch file additions, database files, and other non-configuration changes are not included.

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} from config snapshots*
*Initial snapshot: {initial.get('timestamp', 'N/A')}*
*Current snapshot: {current.get('timestamp', 'N/A')}*
"""
        
        return changelog_content
        
    except Exception as e:
        print(f"Error generating changelog: {e}")
        return None

if __name__ == "__main__":
    content = generate_changelog()
    if content:
        with open('Dogeheim/CHANGELOG.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print("CHANGELOG.md generated successfully!")
        print(f"File saved to: Dogeheim/CHANGELOG.md")
    else:
        print("Failed to generate changelog")
