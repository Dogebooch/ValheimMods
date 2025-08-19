#!/usr/bin/env python3
"""
Simple script to analyze changes from the config tracker snapshots
"""

import json
from pathlib import Path
from datetime import datetime

def analyze_snapshots():
    """Analyze the snapshots and show session changes."""
    snapshots_dir = Path('scripts/snapshots')
    
    try:
        # Load snapshots
        with open(snapshots_dir / 'current_snapshot.json', 'r', encoding='utf-8', errors='replace') as f:
            current = json.load(f)
        with open(snapshots_dir / 'initial_snapshot.json', 'r', encoding='utf-8', errors='replace') as f:
            initial = json.load(f)
        
        print(f"Current snapshot: {current.get('timestamp', 'N/A')} (Session: {current.get('session', 'N/A')})")
        print(f"Initial snapshot: {initial.get('timestamp', 'N/A')} (Session: {initial.get('session', 'N/A')})")
        print(f"Files in current: {len(current.get('files', {}))}")
        print(f"Files in initial: {len(initial.get('files', {}))}")
        print()
        
        # Compare files
        current_files = current.get('files', {})
        initial_files = initial.get('files', {})
        
        changes = []
        
        # Find modified files
        for file_path, file_info in current_files.items():
            if file_path in initial_files:
                if file_info.get('hash') != initial_files[file_path].get('hash'):
                    changes.append(('Modified', file_path))
            else:
                changes.append(('Added', file_path))
        
        # Find deleted files
        for file_path in initial_files:
            if file_path not in current_files:
                changes.append(('Deleted', file_path))
        
        print(f"Found {len(changes)} changes:")
        for status, file_path in changes[:20]:  # Show first 20
            print(f"  {status}: {file_path}")
        
        if len(changes) > 20:
            print(f"  ... and {len(changes) - 20} more changes")
        
        return changes
        
    except Exception as e:
        print(f"Error reading snapshots: {e}")
        return []

if __name__ == "__main__":
    analyze_snapshots()
