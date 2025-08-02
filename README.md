# Valheim Mods Repository

This repository contains an index of important files from a comprehensive Valheim modded setup, specifically focused on the JewelHeim-RelicHeim modpack and related configurations.

## Files

### `important_files.txt`
The original index file containing metadata about important files in the Valheim project.

### `important_files_updated.txt`
An enhanced version of the index with additional columns for file type and importance tags.

### `update_index.py`
Python script used to transform the original index format to include TYPE and IMPORTANCE_TAGS columns.

## Index Format

The updated index uses the following format:
```
[SOURCE] <RELATIVE_PATH> | <TYPE> | <IMPORTANCE_TAGS>
```

### Source Types
- `[BASE GAME]` - Core Valheim game files
- `[MODDED]` - Mod-related files

### File Types
- `CONFIG` - Configuration files (.cfg, .yml, .json, .xml, .ini)
- `DOCS` - Documentation files (.md, .txt)
- `CODE` - Code files (.cs, .dll, .exe, .sh)
- `DATA` - Data files (.manifest, .assets, .resS)
- `ASSET` - Image files (.png, .jpg, .jpeg)
- `ARCHIVE` - Archive files (.zip)
- `OTHER` - Other file types

### Importance Tags
- `CORE` - Core game files
- `MOD` - Mod-related files
- `CRITICAL` - High importance files (manifests, configs, etc.)
- `CONFIG` - Configuration-related files
- `DOCS` - Documentation files
- `LOCALE` - Translation/localization files
- `MODPACK` - JewelHeim modpack files
- `GENERAL` - General files

## Mods Included

This index covers a comprehensive mod setup including:
- JewelHeim-RelicHeim modpack
- EpicLoot system
- Valheim Enchantment System
- Drop That / Spawn That
- Custom raids
- Wacky's Database
- Various Therzie mods (Armory, Warfare, Wizardry)
- And many more

## Usage

Use this index to quickly locate relevant files when working with Valheim mods. The importance tags help prioritize which files to examine first when troubleshooting or making changes.

## Repository Structure

The actual game files and mods are not included in this repository due to size constraints. This repository serves as a reference index for the file structure and organization of a comprehensive Valheim modded setup. 