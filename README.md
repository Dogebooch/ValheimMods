# Valheim Database Analysis Project

This repository contains tools and analysis for parsing and understanding Valheim's custom binary database format. The project focuses on extracting readable information from Valheim's `.db` world files and other binary data.

## Project Overview

Valheim uses custom binary formats for storing world data, player information, and mod integration data. This project provides tools to parse these files and convert them into human-readable formats.

## Recent Analysis: DogeheimTesting Files

### DogeheimTesting.db - World Database
`DogeheimTesting.db` is a Valheim world database file containing:
- Player character data (Dogeo)
- Inventory and equipment information
- Extensive mod integration data
- World state and progression data

#### Key Findings
The database contains a well-developed character with:
- **EpicLoot Enchanted Items**: Multiple items with magic enchantments
- **Mod Integration**: EpicLoot, Blacksmithing, Cooking, and other mods
- **Equipment**: Armor, weapons, tools, and accessories
- **Materials**: Various crafting materials and resources

#### File Details
- **Size**: 10.37 MB
- **Format**: Custom Valheim binary (not SQLite)
- **Magic Number**: 35 (0x00000023)
- **Data Structure**: Complex binary format with embedded strings and structured data

### DogeheimTesting.fwl - World Metadata
`DogeheimTesting.fwl` is a Valheim world metadata file containing:
- World name and identification
- Procedural generation seed
- World configuration information
- File format versioning

#### Key Findings
The world file contains:
- **World Name**: "Dogeheim"
- **World Seed**: 587202560
- **Encoded Data**: "CdjvRssbHZq" (possibly base64 encoded metadata)
- **File Structure**: Simple binary format with clear metadata sections

#### File Details
- **Size**: 49 bytes
- **Format**: Custom Valheim binary format
- **Magic Numbers**: 45 (0x2d) and 35 (0x23)
- **Structure**: Header + metadata + padding

## Files in This Repository

### Analysis Results
#### Database Files (.db)
- `Valheim_Help_Docs/@Valheim_Binary_Readable/DogeheimTesting_readable_20250806_163647.json` - Complete JSON analysis
- `Valheim_Help_Docs/@Valheim_Binary_Readable/DogeheimTesting_readable_20250806_163656.txt` - Human-readable text summary
- `Valheim_Help_Docs/@Valheim_Binary_Readable/DogeheimTesting_Database_Analysis_Summary.md` - Comprehensive analysis document

#### World Files (.fwl)
- `Valheim_Help_Docs/@Valheim_Binary_Readable/DogeheimTesting_readable_20250806_164029.json` - Complete JSON analysis
- `Valheim_Help_Docs/@Valheim_Binary_Readable/DogeheimTesting_readable_20250806_164029.txt` - Human-readable text summary
- `Valheim_Help_Docs/@Valheim_Binary_Readable/DogeheimTesting_FWL_Analysis_Summary.md` - Comprehensive analysis document

### Tools
- `scripts/parse_valheim_world_db.py` - Specialized parser for Valheim .db files
- `scripts/parse_valheim_fwl.py` - Specialized parser for Valheim .fwl files
- `scripts/parse_valheim_binaries.py` - General binary file parser
- `scripts/parse_prefab_names.py` - Prefab name extraction tool
- `scripts/identify_valuable_context_files.py` - File identification tool

## How to Use

### Running the Parser
```bash
# Parse a specific database file
python scripts/parse_valheim_world_db.py

# Parse a specific world file
python scripts/parse_valheim_fwl.py

# Parse all binary files
python scripts/parse_valheim_binaries.py
```

### Understanding the Output
The parser generates:
1. **JSON Format**: Complete structured data with all extracted information
2. **Text Format**: Human-readable summary with key findings
3. **Analysis Summary**: Comprehensive documentation

## Technical Details

### Binary Format Analysis
- **Header**: 4-byte magic number
- **Data Types**: Mixed strings, numbers, and binary data
- **Compression**: Some sections may use zlib compression
- **Structure**: Organized in data blocks with varying sizes

### Extracted Information
- Player names and character data
- Item names, properties, and enchantments
- Mod references and integration data
- World state information
- Skill levels and progression data

## Mod Integration

The analysis reveals extensive mod usage:
- **EpicLoot**: Magic item enchantment system
- **Blacksmithing**: Enhanced crafting system
- **Cooking**: Enhanced cooking system
- **ValheimEnchantmentSystem**: Enchantment framework

## Contributing

This project is open for contributions. Areas for improvement:
- Enhanced binary format understanding
- Better string extraction algorithms
- Support for additional Valheim file types
- Improved mod data parsing

## License

This project is provided as-is for educational and research purposes. Please respect Valheim's terms of service and mod licenses when using this analysis.

## Acknowledgments

- Iron Gate Studio for creating Valheim
- The Valheim modding community
- Contributors to the various mods analyzed

---

**Note**: This analysis is for educational purposes. Always backup your game files before making any modifications.
