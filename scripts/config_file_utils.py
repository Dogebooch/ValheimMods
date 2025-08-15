#!/usr/bin/env python3
"""
Utility functions for processing configuration files with backup awareness.
Handles the distinction between current user configs and backup files.
"""

from pathlib import Path
from typing import List, Tuple, Dict, Any
import yaml
import configparser
import json

# Backup prefix used for RelicHeim backup files
BACKUP_PREFIX = "BACKUP_5.4.10_"

def is_backup_file(filename: str) -> bool:
    """
    Check if a filename is a backup file based on the prefix.
    
    Args:
        filename: The filename to check
        
    Returns:
        bool: True if it's a backup file, False otherwise
    """
    return filename.startswith(BACKUP_PREFIX)

def get_original_filename(backup_filename: str) -> str:
    """
    Extract the original filename from a backup filename.
    
    Args:
        backup_filename: The backup filename with prefix
        
    Returns:
        str: The original filename without the backup prefix
    """
    if is_backup_file(backup_filename):
        return backup_filename[len(BACKUP_PREFIX):]
    return backup_filename

def get_backup_filename(original_filename: str) -> str:
    """
    Create a backup filename from an original filename.
    
    Args:
        original_filename: The original filename
        
    Returns:
        str: The backup filename with prefix
    """
    return f"{BACKUP_PREFIX}{original_filename}"

def separate_config_files(config_directory: Path) -> Tuple[List[Path], List[Path]]:
    """
    Separate configuration files into current and backup lists.
    
    Args:
        config_directory: Path to the configuration directory
        
    Returns:
        Tuple[List[Path], List[Path]]: (current_files, backup_files)
    """
    current_files = []
    backup_files = []
    
    if not config_directory.exists():
        return current_files, backup_files
    
    for file_path in config_directory.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.cfg', '.yml']:
            if is_backup_file(file_path.name):
                backup_files.append(file_path)
            else:
                current_files.append(file_path)
    
    return current_files, backup_files

def find_matching_configs(current_files: List[Path], backup_files: List[Path]) -> Dict[str, Tuple[Path, Path]]:
    """
    Find matching pairs of current and backup configuration files.
    
    Args:
        current_files: List of current configuration file paths
        backup_files: List of backup configuration file paths
        
    Returns:
        Dict[str, Tuple[Path, Path]]: Dictionary mapping original filename to (current_file, backup_file) tuple
    """
    matches = {}
    
    for current_file in current_files:
        backup_filename = get_backup_filename(current_file.name)
        backup_file = next((f for f in backup_files if f.name == backup_filename), None)
        
        if backup_file:
            matches[current_file.name] = (current_file, backup_file)
    
    return matches

def load_config_file(file_path: Path) -> Dict[str, Any]:
    """
    Load a configuration file (supports both .cfg and .yml formats).
    
    Args:
        file_path: Path to the configuration file
        
    Returns:
        Dict[str, Any]: Parsed configuration data
    """
    if not file_path.exists():
        return {}
    
    try:
        if file_path.suffix == '.yml':
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        elif file_path.suffix == '.cfg':
            config = configparser.ConfigParser()
            config.read(file_path, encoding='utf-8')
            
            # Convert to dictionary format
            result = {}
            for section in config.sections():
                result[section] = dict(config[section])
            return result
        else:
            return {}
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def compare_configs(current_file: Path, backup_file: Path) -> Dict[str, Any]:
    """
    Compare current and backup configuration files.
    
    Args:
        current_file: Path to current configuration file
        backup_file: Path to backup configuration file
        
    Returns:
        Dict[str, Any]: Comparison results including differences
    """
    current_data = load_config_file(current_file)
    backup_data = load_config_file(backup_file)
    
    comparison = {
        'current_file': str(current_file),
        'backup_file': str(backup_file),
        'current_sections': list(current_data.keys()),
        'backup_sections': list(backup_data.keys()),
        'added_sections': [],
        'removed_sections': [],
        'modified_sections': [],
        'unchanged_sections': []
    }
    
    # Find section differences
    current_sections = set(current_data.keys())
    backup_sections = set(backup_data.keys())
    
    comparison['added_sections'] = list(current_sections - backup_sections)
    comparison['removed_sections'] = list(backup_sections - current_sections)
    comparison['unchanged_sections'] = list(current_sections & backup_sections)
    
    # Check for modifications in common sections
    for section in comparison['unchanged_sections']:
        if current_data[section] != backup_data[section]:
            comparison['modified_sections'].append(section)
            comparison['unchanged_sections'].remove(section)
    
    return comparison

def generate_config_report(config_directory: Path) -> Dict[str, Any]:
    """
    Generate a comprehensive report of configuration files.
    
    Args:
        config_directory: Path to the configuration directory
        
    Returns:
        Dict[str, Any]: Report containing file statistics and comparisons
    """
    current_files, backup_files = separate_config_files(config_directory)
    matches = find_matching_configs(current_files, backup_files)
    
    report = {
        'directory': str(config_directory),
        'total_current_files': len(current_files),
        'total_backup_files': len(backup_files),
        'matching_pairs': len(matches),
        'current_only_files': [f.name for f in current_files if f.name not in matches],
        'backup_only_files': [f.name for f in backup_files if get_original_filename(f.name) not in [cf.name for cf in current_files]],
        'comparisons': {}
    }
    
    # Generate comparisons for matching files
    for original_name, (current_file, backup_file) in matches.items():
        report['comparisons'][original_name] = compare_configs(current_file, backup_file)
    
    return report

def save_report(report: Dict[str, Any], output_file: Path):
    """
    Save a configuration report to a JSON file.
    
    Args:
        report: The report dictionary to save
        output_file: Path to the output JSON file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

def main():
    """Example usage of the utility functions."""
    # Example: Process the current user config directory
    config_dir = Path("Valheim/profiles/Dogeheim_Player/BepInEx/config")
    
    if config_dir.exists():
        print(f"Processing configuration directory: {config_dir}")
        
        # Generate report
        report = generate_config_report(config_dir)
        
        # Save report
        output_file = Path("scripts/config_analysis_report.json")
        save_report(report, output_file)
        
        print(f"Report saved to: {output_file}")
        print(f"Found {report['total_current_files']} current files")
        print(f"Found {report['total_backup_files']} backup files")
        print(f"Found {report['matching_pairs']} matching pairs")
    else:
        print(f"Configuration directory not found: {config_dir}")

if __name__ == "__main__":
    main()
