# Valheim Unified Mod Manager

A comprehensive tool for managing Valheim mods, items, and loot tables in one centralized application.

## Features

### 🎮 Mod Management
- **Mod Overview**: View all installed mods with versions and categories
- **Mod Categorization**: Automatic categorization based on mod content
- **Mod Details**: Detailed information about each mod
- **Search & Filter**: Find mods by name or category

### 🎒 Item Scanning & Management
- **Comprehensive Item Database**: Scans cached icons, translation files, and VNEI data
- **Item Categorization**: Automatically categorizes items (vanilla, armor, weapons, magic, etc.)
- **Icon Support**: Displays item icons from cached data
- **Translation Support**: Shows proper item names from translation files
- **Search & Filter**: Find items by name, category, or mod source

### 💰 Loot Table Management
- **Multi-Source Import**: Imports loot tables from:
  - Warpalicious More World Locations
  - EpicLoot patches
  - Creature Level & Loot Control (CLLC)
  - Drop That mod
- **Centralized Storage**: All loot tables stored in one JSON file
- **Item Registry**: Track which items appear in which loot tables
- **Search & Filter**: Find loot tables by name, source, or category

### 📊 Statistics & Analytics
- **Comprehensive Statistics**: View counts and breakdowns for mods, items, and loot tables
- **Category Analysis**: See distribution across different categories
- **Source Tracking**: Track which mods and sources contribute the most content

## Installation

### Prerequisites
- Python 3.7 or higher
- Required packages: `pillow`, `pyyaml`

### Setup
1. Install required packages:
   ```bash
   pip install pillow pyyaml
   ```

2. Run the unified manager:
   ```bash
   python scripts/run_unified_manager.py
   ```

## Usage

### Main Interface
The application has a tabbed interface with three main sections:

#### 1. Mods Tab
- **View**: All installed mods with version and category information
- **Search**: Filter mods by name
- **Filter**: Filter by category (Armor, Weapons, Magic, etc.)
- **Details**: Double-click a mod to see detailed information

#### 2. Items Tab
- **View**: All discovered items from mods and vanilla game
- **Search**: Filter items by name
- **Filter**: Filter by category (vanilla, armor, weapons, magic, etc.)
- **Details**: Double-click an item to see detailed information
- **Icons**: Shows which items have cached icons
- **Translations**: Shows which items have translation data

#### 3. Loot Tables Tab
- **View**: All loot tables from various mod sources
- **Search**: Filter loot tables by name
- **Filter**: Filter by source (Warpalicious, EpicLoot, CLLC, Drop That)
- **Details**: Double-click a loot table to see all items in it

### Control Buttons
- **Scan Items**: Scan for all items from cached icons and translation files
- **Import Loot Tables**: Import loot tables from all supported sources
- **Refresh**: Refresh all data displays
- **Statistics**: Show comprehensive statistics about mods, items, and loot tables

## Data Sources

### Item Scanning
The application scans multiple sources for item information:

1. **Cached Icons**: `Valheim_Help_Docs/Valheim_PlayerWorldData/Jotunn/CachedIcons/`
   - Extracts item names from icon filenames
   - Provides visual representation of items

2. **Translation Files**: `Valheim/cache/*/config/**/*.yml`
   - Extracts proper item names from translation files
   - Provides localized item names

3. **VNEI Data**: VNEI mod data files
   - Extracts item information from VNEI database

### Loot Table Import
The application imports loot tables from:

1. **Warpalicious More World Locations**: `warpalicious.More_World_Locations_LootLists.yml`
   - World location loot pools
   - Configurable item stacks and weights

2. **EpicLoot**: `EpicLoot/patches/RelicHeimPatches/*.json`
   - Epic loot patches for bosses, creatures, and treasures
   - Rarity-based loot distribution

3. **Creature Level & Loot Control**: `ItemConfig_Base.yml`
   - Item groups for creature drops
   - Configurable drop rates and conditions

4. **Drop That**: `drop_that.character_drop.cfg`
   - Custom creature drop configurations
   - Character-specific loot tables

## File Structure

```
scripts/
├── valheim_unified_manager.py      # Main unified manager application
├── run_unified_manager.py          # Launcher script
├── README_Unified_Manager.md       # This documentation
├── comprehensive_item_scanner.py   # Standalone item scanner (legacy)
├── centralized_mod_manager.py      # Legacy mod manager
├── centralized_loot_manager.py     # Legacy loot manager
└── __pycache__/                    # Python cache files
```

## Data Files

The application creates and manages several data files:

- `centralized_loot_tables.json`: Centralized loot table database
- `comprehensive_items.json`: Comprehensive item database (from scanner)
- `backups/`: Backup directory for configuration files

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Make sure all required packages are installed: `pip install pillow pyyaml`
   - Check that the Valheim path is correct

2. **No Items Found**
   - Run "Scan Items" to populate the item database
   - Check that cached icons exist in the expected location
   - Verify translation files are present in mod cache directories

3. **No Loot Tables Found**
   - Run "Import Loot Tables" to import from all sources
   - Check that loot configuration files exist
   - Verify file paths and permissions

4. **GUI Issues**
   - Try running with different Python versions
   - Check for tkinter installation issues
   - Verify display settings and resolution

### Debug Information
The application provides detailed console output for debugging:
- Item scanning progress
- Translation file processing
- Loot table import status
- Error messages and warnings

## Advanced Usage

### Custom Categories
You can modify the mod categories in the `ComprehensiveItemScanner` class:
```python
self.mod_categories = {
    "armor": ["Therzie-Armory", "HugotheDwarf-Hugos_Armory"],
    "weapons": ["Therzie-Warfare", "Therzie-WarfareFireAndIce"],
    # Add your own categories here
}
```

### Extending Loot Sources
To add support for new loot table sources, extend the `CentralizedLootManager` class:
```python
def _import_new_source(self) -> None:
    """Import from a new loot source"""
    # Add your import logic here
    pass
```

### Custom Item Processing
To customize item name cleaning, modify the `clean_item_name` method:
```python
def clean_item_name(self, item_name: str) -> str:
    # Add your custom cleaning logic
    return cleaned_name
```

## Contributing

The unified manager is designed to be extensible. Key areas for contribution:

1. **New Data Sources**: Add support for additional mod data sources
2. **Enhanced UI**: Improve the user interface and user experience
3. **Performance**: Optimize scanning and import performance
4. **Documentation**: Improve documentation and add examples

## License

This tool is provided as-is for managing Valheim mods. Use at your own discretion.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review console output for error messages
3. Verify file paths and permissions
4. Ensure all dependencies are installed correctly
