# Dogeheim - Comprehensive Valheim Modpack

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/thunderstore-io)
[![Valheim](https://img.shields.io/badge/Valheim-Compatible-green.svg)](https://www.valheimgame.com/)

A comprehensive Valheim modpack featuring MMO progression, enhanced combat/magic systems, expanded biomes, quality-of-life improvements, and extensive building/crafting options.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Key Features](#key-features)
- [Mod Categories](#mod-categories)
- [Configuration](#configuration)
- [Recent Changes](#recent-changes)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

## 🎯 Overview

Dogeheim transforms Valheim into an expansive MMO-style experience with over 100 carefully selected mods. This modpack enhances every aspect of the game while maintaining balance and compatibility.

### What's New in This Modpack:
- **MMO Progression System** - Level-based character development with skill trees
- **Enhanced Combat & Magic** - New weapons, spells, and combat mechanics
- **Expanded World** - New biomes, dungeons, and exploration content
- **Quality of Life** - Inventory management, automation, and convenience features
- **Advanced Building** - Expanded construction options and tools

## 🚀 Installation

### Prerequisites
- Valheim (latest version)
- Thunderstore Mod Manager (recommended) or manual BepInEx installation

### Quick Install (Thunderstore)
1. Download and install [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager)
2. Search for "Dogeheim" in the mod browser
3. Click "Install with Dependencies"
4. Launch Valheim through Thunderstore

### Manual Install
1. Install [BepInEx 5.4.2332](https://valheim.thunderstore.io/package/denikson/BepInExPack_Valheim/)
2. Download all dependencies listed in the manifest
3. Extract mods to your `BepInEx/plugins` folder
4. Launch Valheim

## ⭐ Key Features

### 🎮 MMO Progression System
- **WackyEpicMMOSystem** - Level-based progression with experience points
- **SmartSkills** - Skill-based character development
- **Skill Requirements** - Items require specific skill levels to use
- **Groups** - Party system with shared experience

### ⚔️ Enhanced Combat & Magic
- **Therzie Mods Suite**:
  - **Warfare** - Advanced combat mechanics and weapons
  - **Wizardry** - Magic system with spells and mana
  - **Monstrum** - New creatures and boss encounters
  - **Armory** - Expanded weapon and armor options
- **EpicLoot** - Enchantment system for gear
- **RelicHeim** - Legendary items and artifacts

### 🌍 Expanded World Content
- **Warpalicious Biome Packs**:
  - Meadows, Black Forest, Swamp, Mountains, Plains, Mistlands, Ashlands
  - Underground Ruins and Forbidden Catacombs
  - Adventure Map Pack with new locations
- **Seasons** - Dynamic weather and seasonal changes
- **Biome Lords Quest** - New quest system
- **Mushroom Monsters** - Additional creature variety

### 🛠️ Quality of Life Improvements
- **Inventory Management**:
  - Extended player inventory
  - Backpacks and adventure backpacks
  - Quick stack, store, sort, and trash functionality
  - Multi-user chests
- **Automation**:
  - Automatic fuel management
  - Plant everything system
  - Instant loot drops
- **Convenience**:
  - Target portals for fast travel
  - Speedy paths for faster movement
  - Mouse tweaks for better interaction
  - No food degradation

### 🏗️ Advanced Building & Crafting
- **OdinArchitect** - Advanced building tools and planning
- **Fine Wood** - Additional building pieces and furniture
- **PlanBuild** - Blueprint system for construction
- **Enhanced Crafting**:
  - Blacksmithing improvements
  - Cooking additions
  - Potion crafting system
  - Workbench tweaks

## 📦 Mod Categories

### Core Framework
- BepInEx Pack (5.4.2332)
- Jotunn (2.26.0)
- Configuration Manager
- HookGenPatcher

### MMO & Progression
- WackyEpicMMOSystem (1.9.44)
- WackysDatabase (2.4.56)
- SmartSkills (1.0.2)
- WackyItemRequiresSkillLevel (1.3.6)
- Groups (1.2.9)

### Combat & Magic
- Therzie Warfare (1.8.9)
- Therzie Wizardry (1.1.8)
- Therzie Monstrum (1.5.1)
- Therzie Armory (1.3.1)
- EpicLoot (0.11.4)
- RelicHeim (5.4.10)

### World Expansion
- Warpalicious Biome Packs (All biomes)
- Seasons (1.6.6)
- Biome Lords Quest (3.2.0)
- Mushroom Monsters (1.0.2)
- Custom Raids (1.8.0)

### Quality of Life
- Backpacks (1.3.6)
- Extended Inventory (1.4.9)
- Quick Stack (1.4.13)
- Target Portal (1.2.0)
- SpeedyPaths (1.0.8)

### Building & Crafting
- OdinArchitect (1.5.3)
- Fine Wood Pieces (1.1.7)
- PlanBuild (0.18.2)
- Blacksmithing (1.3.2)
- Cooking Additions (1.2.7)

## ⚙️ Configuration

### Current Active Configuration Environment

The modpack is configured for **balanced multiplayer gameplay** with the following key settings:

#### 🎮 MMO Progression Settings
- **Maximum Level**: 120 (increased from default 100)
- **Experience Rate**: 1.15x (15% bonus experience)
- **Group Experience**: 0.9x (90% of normal XP in groups)
- **Experience Loss on Death**: 1-4% (reduced from 5-25%)
- **Free Points per Level**: 4 (reduced from 5 for balance)
- **Level Experience**: 300 base + 4.8% increase per level

#### ⚔️ Combat & Loot Balance
- **Creature Level Control**: Very Hard difficulty
- **Boss Loot per Star**: 50% chance (reduced from 60%)
- **Creature Loot per Star**: 100% chance (increased from 50%)
- **Passive Creature Drops**: 1x multiplier (reduced from 2x)
- **Boss Size Increase**: 5% per star (reduced from 7%)

#### 🏆 Boss Drop Improvements
- **Boss Trophies**: One per player (ensures all players get rewards)
- **Boss Range**: 100 units for multi-player drops
- **Crypt Keys & Wishbones**: One per player near boss

#### 🎲 EpicLoot Configuration
- **Item Drop Limits**: Player must know recipe (prevents overpowered early drops)
- **Bounty Gating**: Boss kills unlock next biome bounties
- **Freebuild Gating**: Current biome pieces unlocked by boss kills
- **Materials Drop Ratio**: 0 (items only, no material conversion)

#### 🌍 World & Exploration
- **Multiplayer Scaling**: 40% HP, 4% damage per additional player
- **Player Range**: 70 units for experience sharing
- **Visual Indicators**: On for all creatures and bosses

### Important Configuration Files
The modpack includes pre-configured settings for optimal gameplay. Key configuration files:

- `WackyMole.EpicMMOSystem.cfg` - MMO progression settings
- `org.bepinex.plugins.creaturelevelcontrol.cfg` - Creature and loot balance
- `randyknapp.mods.epicloot.cfg` - EpicLoot enchantment system
- `Therzie.*.cfg` - Combat and magic system configurations
- `warpalicious.*.cfg` - World expansion settings
- `org.bepinex.plugins.*.cfg` - Quality of life mod settings

### Customization
You can modify any configuration file in `BepInEx/config/` to adjust:
- Experience rates and skill progression
- Loot drop rates and item availability
- Creature difficulty and spawn rates
- Building and crafting requirements

## 📝 Recent Changes

### Latest Configuration Updates (Session 2025-08-18)

#### 🏆 Boss Drop Improvements
- **One Per Player Drops**: All boss drops now ensure each player gets rewards
- **Affected Bosses**: Bonemass, Dragon, Asmodeus, Gorr, Storm Herald, Svalt, Vrykolathas
- **Gold Trophy Drops**: Also set to one per player for fair distribution

#### ⚖️ Loot Balance Adjustments
- **Creature Loot**: Increased from 50% to 100% chance per star level
- **Boss Loot**: Reduced from 60% to 50% chance per star level
- **Passive Creatures**: Reduced drop multiplier from 2x to 1x
- **Boss Size**: Reduced size increase from 7% to 5% per star

#### 🎲 EpicLoot Refinements
- **Materials Conversion**: Disabled (items drop as items, not materials)
- **Wizardry Drops**: Increased Corrupted Dverger Mage drop chance to 100%

#### 🗑️ Cleanup
- **Swamp Chests**: Removed redundant treasure chest configuration

*For detailed change tracking, see [CHANGELOG.md](CHANGELOG.md)*

## 🔧 Troubleshooting

### Common Issues

**Game Crashes on Startup**
- Ensure all dependencies are installed
- Check BepInEx version compatibility
- Verify mod load order

**Performance Issues**
- Reduce graphics settings
- Disable resource-intensive mods temporarily
- Check for conflicting mods

**Missing Items or Features**
- Verify all mods are properly installed
- Check configuration files for disabled features
- Ensure mod versions are compatible

### Performance Optimization
- **Recommended RAM**: 8GB minimum, 16GB recommended
- **Graphics**: Medium to High settings recommended
- **Storage**: 10GB free space for mods and saves

### Known Conflicts
- Some mods may conflict with vanilla game updates
- EpicLoot and RelicHeim work together but may need configuration adjustment
- Multiple biome mods may cause world generation issues

## 🆘 Support

### Getting Help
1. Check the [Troubleshooting](#troubleshooting) section above
2. Review mod-specific documentation
3. Check the [Thunderstore Discord](https://discord.gg/thunderstore)
4. Report issues with specific error messages and mod versions

### Useful Links
- [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager)
- [BepInEx Documentation](https://docs.bepinex.dev/)
- [Valheim Official Discord](https://discord.gg/valheim)

### Contributing
If you find issues or have suggestions:
1. Check if the issue is already reported
2. Provide detailed information about the problem
3. Include your mod versions and configuration

## 📄 License

This modpack is a collection of mods created by various authors. Each mod retains its original license. Please respect individual mod authors' rights and licensing terms.

## 🙏 Credits

Special thanks to all the mod authors who made this modpack possible:
- **WackyMole** - MMO system and progression
- **Therzie** - Combat and magic systems
- **Warpalicious** - World expansion content
- **Smoothbrain** - Quality of life improvements
- **Azumatt** - Inventory and convenience features
- **OdinPlus** - Building and crafting enhancements

And all other mod authors whose work is included in this modpack.

---

**Note**: This modpack is designed for multiplayer compatibility but may require all players to use the same mod versions for optimal experience.
