# Centralized Loot Table Manager

This tool provides a unified interface for managing loot tables across multiple Valheim mods, solving the problem of loot tables being spread across different configuration files.

## Problem Solved

Currently, loot tables are distributed across multiple mod configuration files:
- **Warpalicious More World Locations** (`warpalicious.More_World_Locations_LootLists.yml`)
- **EpicLoot** (`EpicLoot/patches/RelicHeimPatches/*.json`)
- **Creature Level & Loot Control** (`ItemConfig_Base.yml`)
- **Drop That** (`drop_that.character_drop.cfg`)
- **Spawn That** (spawn configuration files)

This makes manual configuration difficult and error-prone.

## Solution

The Centralized Loot Table Manager provides:

1. **Unified Import**: Import loot tables from all sources into a single JSON format
2. **Centralized Management**: Edit all loot tables through one interface
3. **Export Back**: Export changes back to the original mod formats
4. **Backup & Restore**: Automatic backup functionality
5. **Validation**: Conflict detection and validation

## Features

### Core Functionality
- **Import from All Sources**: Automatically reads all loot table configurations
- **Export to Original Formats**: Writes changes back to mod-specific formats
- **Backup System**: Creates timestamped backups before making changes
- **Statistics**: Provides overview of loot table distribution

### GUI Interface
- **Loot Tables Tab**: Browse and search all loot tables
- **Items Tab**: See which items appear in which tables
- **Sources Tab**: View statistics by mod source
- **Search & Filter**: Find specific tables or items quickly
- **Detailed Views**: Double-click for detailed information

### Data Management
- **Centralized Storage**: All data stored in `centralized_loot_tables.json`
- **Item Registry**: Tracks which items appear in which tables
- **Conflict Detection**: Identifies overlapping configurations
- **Validation**: Ensures data integrity

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:
   ```bash
   pip install pyyaml
   ```
3. Run the manager:
   ```bash
   python scripts/run_centralized_loot_manager.py
   ```

## Usage

### First Time Setup

1. **Launch the GUI**: Run the script from your Valheim project directory
2. **Import Data**: Click "Import from All Sources" to load existing configurations
3. **Review**: Browse the imported loot tables in the GUI
4. **Create Backup**: Click "Create Backup" before making changes

### Daily Workflow

1. **Import Changes**: If mods have updated, re-import to get latest changes
2. **Edit Loot Tables**: Use the GUI to modify loot configurations
3. **Export Changes**: Click "Export to Original Formats" to apply changes
4. **Test**: Start Valheim to verify changes work as expected

### Advanced Usage

#### Manual Configuration
You can also edit the `centralized_loot_tables.json` file directly:

```json
{
  "metadata": {
    "version": "1.0",
    "created": "2024-01-01T12:00:00",
    "total_tables": 80,
    "total_items": 201
  },
  "loot_tables": {
    "MeadowsLoot1": {
      "name": "MeadowsLoot1",
      "source": "Warpalicious More World Locations",
      "source_file": "path/to/file.yml",
      "description": "Loot table for MeadowsLoot1",
      "items": [
        {
          "item_name": "Coins",
          "stack_min": 5,
          "stack_max": 20,
          "weight": 1.0,
          "chance": 1.0,
          "rarity": null,
          "source_mod": "Warpalicious",
          "conditions": {}
        }
      ],
      "conditions": {},
      "metadata": {}
    }
  }
}
```

#### Command Line Usage
You can also use the manager programmatically:

```python
from centralized_loot_manager import CentralizedLootManager

# Create manager instance
manager = CentralizedLootManager("Valheim")

# Import from all sources
manager.import_from_all_sources()

# Get statistics
stats = manager.get_statistics()
print(f"Total loot tables: {stats['total_tables']}")

# Export changes
manager.export_to_original_formats()
```

## File Structure

```
Valheim/
├── profiles/
│   └── Dogeheim_Player/
│       └── BepInEx/
│           └── config/
│               ├── centralized_loot_tables.json          # Centralized data
│               ├── loot_backups/                         # Backup directory
│               │   └── backup_20240101_120000/
│               ├── warpalicious.More_World_Locations_LootLists.yml
│               ├── ItemConfig_Base.yml
│               ├── drop_that.character_drop.cfg
│               └── EpicLoot/
│                   └── patches/
│                       └── RelicHeimPatches/
└── scripts/
    ├── centralized_loot_manager.py                       # Main manager
    ├── run_centralized_loot_manager.py                   # Launcher
    └── README_Centralized_Loot_Manager.md               # This file
```

## Supported Mods

### Warpalicious More World Locations
- **Format**: YAML
- **Purpose**: POI location loot tables
- **Features**: Stack sizes, weights, item lists

### EpicLoot
- **Format**: JSON
- **Purpose**: Magic item drops for bosses/creatures
- **Features**: Rarity distributions, leveled loot

### Creature Level & Loot Control (CLLC)
- **Format**: YAML
- **Purpose**: Item groups for creature drops
- **Features**: Item groupings, stack configurations

### Drop That
- **Format**: CFG (INI-style)
- **Purpose**: Creature drop configurations
- **Features**: Drop chances, amounts, conditions

### Spawn That
- **Format**: CFG
- **Purpose**: Creature spawning (affects loot indirectly)
- **Features**: Spawn conditions, creature types

## Best Practices

### Before Making Changes
1. **Always create a backup** before importing or exporting
2. **Test changes** in a development environment first
3. **Document modifications** for future reference

### When Importing
1. **Check for conflicts** between different mod sources
2. **Review item names** for consistency
3. **Validate weights and chances** are reasonable

### When Exporting
1. **Verify file permissions** allow writing to config directories
2. **Check mod compatibility** with exported formats
3. **Test in-game** to ensure changes work as expected

### Data Management
1. **Keep backups organized** with descriptive timestamps
2. **Version control** the centralized JSON file
3. **Document custom changes** for team collaboration

## Troubleshooting

### Common Issues

#### Import Errors
- **File not found**: Check that mod configuration files exist
- **Parse errors**: Verify file formats are correct
- **Permission errors**: Ensure read access to config directories

#### Export Errors
- **File not writable**: Check write permissions to config directories
- **Format errors**: Verify mod-specific format requirements
- **Path issues**: Ensure correct file paths are configured

#### GUI Issues
- **Display problems**: Check tkinter installation and display settings
- **Performance**: Large loot tables may take time to load
- **Memory usage**: Monitor memory usage with very large datasets

### Error Messages

#### "Warpalicious loot file not found"
- Check that `warpalicious.More_World_Locations_LootLists.yml` exists
- Verify the file path in the configuration

#### "EpicLoot patches directory not found"
- Ensure EpicLoot mod is installed
- Check that patches directory exists

#### "Error parsing [file]"
- Verify file format is correct
- Check for syntax errors in configuration files
- Ensure proper encoding (UTF-8)

### Getting Help

1. **Check logs**: Look for detailed error messages in console output
2. **Verify paths**: Ensure all file paths are correct
3. **Test individually**: Try importing from one source at a time
4. **Check permissions**: Verify file and directory permissions

## Future Enhancements

### Planned Features
- **Real-time validation**: Validate changes as you make them
- **Conflict resolution**: GUI for resolving conflicts between mods
- **Template system**: Pre-built loot table templates
- **Import/Export filters**: Selective import/export of specific tables
- **Version comparison**: Compare changes between versions

### Integration Ideas
- **Mod manager integration**: Direct integration with r2modman
- **Web interface**: Browser-based management interface
- **API support**: REST API for programmatic access
- **Plugin system**: Support for custom import/export plugins

## Contributing

To contribute to this project:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Setup
```bash
# Clone the repository
git clone <repository-url>

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 scripts/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Warpalicious** for More World Locations mod
- **RandyKnapp** for EpicLoot mod
- **Smoothbrain** for Creature Level & Loot Control
- **ASharpPen** for Drop That and Spawn That mods
- **Valheim modding community** for inspiration and feedback
