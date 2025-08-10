# Centralized Mod Manager

A comprehensive mod management tool for Valheim that combines mod management with loot table management in a unified interface.

## Features

### 🎯 Core Functionality
- **Integrated Mod Management**: Manage mod installations, configurations, and status
- **Loot Table Management**: Import, export, and manage loot tables from multiple mods
- **Content Filtering**: Filter mods by categories based on the Valheim Content Mods Summary
- **Icon Support**: Display mod icons in the interface
- **Backup & Restore**: Automatic backup functionality for all configurations

### 🖥️ GUI Interface
- **Mods Tab**: Browse and manage all installed mods with icons and categories
- **Loot Tables Tab**: View and manage loot tables from all sources
- **Items Tab**: See which items appear in which loot tables
- **Sources Tab**: View statistics by mod source
- **Search & Filter**: Find specific mods, tables, or items quickly
- **Category Filtering**: Filter mods by content categories (Armor, Weapons, Magic, etc.)

### 📊 Data Management
- **Centralized Storage**: All data stored in organized JSON and YAML files
- **Mod Categories**: Automatic categorization based on content type
- **Icon Loading**: Automatic loading and caching of mod icons
- **Statistics**: Comprehensive statistics for mods and loot tables

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:
   ```bash
   pip install pyyaml pillow
   ```
3. Run the manager:
   ```bash
   python scripts/run_centralized_mod_manager.py
   ```

## Usage

### First Time Setup

1. **Launch the GUI**: Run the script from your Valheim project directory
2. **Scan Cache**: Click "Scan Cache" to discover mods in the cache directory
3. **Import Loot Tables**: Click "Import Loot Tables" to load existing configurations
4. **Review**: Browse the mods and loot tables in the GUI
5. **Create Backup**: Click "Create Backup" before making changes

### Daily Workflow

1. **Scan for Updates**: Use "Scan Cache" to find new mods
2. **Import Changes**: Re-import loot tables if mods have updated
3. **Manage Mods**: Use the Mods tab to view and manage mod configurations
4. **Edit Loot Tables**: Use the Loot Tables tab to modify loot configurations
5. **Export Changes**: Click "Export Loot Tables" to apply changes
6. **Test**: Start Valheim to verify changes work as expected

### Mod Categories

The manager automatically categorizes mods based on the Valheim Content Mods Summary:

- **🛡️ Armor & Equipment**: Armor, equipment, and gear mods
- **⚔️ Weapons & Combat**: Weapons, combat, and warfare mods
- **🧙‍♂️ Magic & Spell**: Magic, spells, and wizardry mods
- **🎒 Loot & Progression**: Loot, backpacks, and progression mods
- **🍖 Food & Consumable**: Food, cooking, and consumable mods
- **🌱 Farming & Agriculture**: Farming, agriculture, and resource gathering
- **🏰 Building & Location**: Building, locations, and architectural mods
- **⛵ Naval & Ship**: Ship, sailing, and naval mods
- **🌍 Environmental & Seasonal**: Environment, seasons, and weather mods
- **🐉 Monster & Boss**: Monster, boss, and creature mods
- **🎮 Gameplay & Systems**: Gameplay mechanics and system mods
- **🗑️ Quality of Life**: Quality of life and utility mods
- **🔧 Framework & Utility**: Framework, utility, and development mods

## File Structure

```
Valheim/
├── profiles/
│   └── Dogeheim_Player/
│       ├── mods.yml                                    # Mod configuration
│       └── BepInEx/
│           └── config/
│               ├── centralized_loot_tables.json        # Centralized loot data
│               ├── mod_backups/                        # Backup directory
│               ├── warpalicious.More_World_Locations_LootLists.yml
│               ├── ItemConfig_Base.yml
│               ├── drop_that.character_drop.cfg
│               └── EpicLoot/
│                   └── patches/
│                       └── RelicHeimPatches/
├── cache/                                              # Mod cache directory
│   └── [mod_name]/
│       ├── manifest.json
│       └── icon.png
└── scripts/
    ├── centralized_mod_manager.py                      # Main manager
    ├── centralized_loot_manager.py                     # Loot manager
    ├── run_centralized_mod_manager.py                  # Launcher
    └── README_Centralized_Mod_Manager.md              # This file
```

## Supported Mod Sources

### Mod Management
- **r2modman Configuration**: Reads from `mods.yml` configuration
- **Cache Directory**: Scans cache for additional mods
- **Manifest Files**: Reads mod metadata from `manifest.json` files
- **Icon Loading**: Automatically loads mod icons from cache

### Loot Table Management
- **Warpalicious More World Locations**: YAML-based POI loot tables
- **EpicLoot**: JSON-based magic item drops
- **Creature Level & Loot Control**: YAML-based item groups
- **Drop That**: CFG-based creature drops
- **Spawn That**: CFG-based spawn configurations

## Advanced Usage

### Command Line Usage
You can also use the manager programmatically:

```python
from centralized_mod_manager import CentralizedModManager

# Create manager instance
manager = CentralizedModManager("Valheim")

# Scan for mods
manager.scan_cache_for_mods()

# Get statistics
stats = manager.get_statistics()
print(f"Total mods: {stats['mods']['total_mods']}")

# Import loot tables
manager.loot_manager.import_from_all_sources()

# Export changes
manager.loot_manager.export_to_original_formats()
```

### Mod Configuration
The manager reads mod information from the `mods.yml` file:

```yaml
- name: "ModName"
  displayName: "Display Name"
  version: "1.0.0"
  description: "Mod description"
  author: "Author Name"
  icon: "path/to/icon.png"
  websiteUrl: "https://example.com"
  status: "Enabled"
  enabled: true
```

## Best Practices

### Before Making Changes
1. **Always create a backup** before importing or exporting
2. **Test changes** in a development environment first
3. **Document modifications** for future reference

### When Managing Mods
1. **Scan cache regularly** to discover new mods
2. **Review mod categories** for proper organization
3. **Check mod dependencies** and conflicts

### When Managing Loot Tables
1. **Import after mod updates** to get latest configurations
2. **Review loot table conflicts** between different mods
3. **Test loot changes** in-game before committing

### Data Management
1. **Keep backups organized** with descriptive timestamps
2. **Version control** the configuration files
3. **Document custom changes** for team collaboration

## Troubleshooting

### Common Issues

#### Import Errors
- **File not found**: Check that mod configuration files exist
- **Parse errors**: Verify file formats are correct
- **Permission errors**: Ensure read access to directories

#### GUI Issues
- **Display problems**: Check tkinter installation and display settings
- **Icon loading**: Verify PIL/Pillow installation
- **Performance**: Large mod lists may take time to load

#### Mod Issues
- **Missing mods**: Use "Scan Cache" to discover mods
- **Category errors**: Check mod name matching in categories
- **Icon loading**: Verify icon file paths and formats

### Error Messages

#### "Error importing centralized_mod_manager"
- Check that all dependencies are installed: `pip install pyyaml pillow`
- Verify the script is run from the correct directory

#### "Mod not found in cache"
- Use "Scan Cache" button to refresh mod discovery
- Check that mods are properly installed in the cache directory

#### "Icon loading failed"
- Verify PIL/Pillow is installed: `pip install pillow`
- Check that icon files exist and are valid image formats

### Getting Help

1. **Check logs**: Look for detailed error messages in console output
2. **Verify paths**: Ensure all file paths are correct
3. **Test individually**: Try scanning cache and importing loot separately
4. **Check permissions**: Verify file and directory permissions

## Future Enhancements

### Planned Features
- **Real-time mod validation**: Validate mod configurations as you edit
- **Conflict resolution**: GUI for resolving mod conflicts
- **Mod installation**: Direct mod installation from the GUI
- **Profile management**: Multiple mod profiles support
- **Version comparison**: Compare mod versions and configurations

### Integration Ideas
- **Thunderstore integration**: Direct integration with Thunderstore API
- **Mod update checking**: Automatic mod update detection
- **Web interface**: Browser-based management interface
- **Plugin system**: Support for custom mod management plugins

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

- **Valheim modding community** for inspiration and feedback
- **r2modman** for mod management concepts
- **Thunderstore** for mod hosting and metadata
- **BepInEx** for the modding framework
- **All mod authors** for creating amazing Valheim mods
