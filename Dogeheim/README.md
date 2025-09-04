# Dogeheim
## The Ultimate Valheim MMO Experience

[![Version](https://img.shields.io/badge/version-1.4.7-blue.svg)](https://thunderstore.io/c/valheim/p/dogebooch/Dogeheim/)
[![Valheim](https://img.shields.io/badge/Valheim-Compatible-green.svg)](https://www.valheimgame.com/)
[![Mods](https://img.shields.io/badge/Mods-100+-orange.svg)](https://valheim.thunderstore.io/)
[![Multiplayer](https://img.shields.io/badge/Multiplayer-Ready-blue.svg)](https://www.valheimgame.com/)

**Transform your Valheim experience into an epic MMO adventure** with Dogeheim - a meticulously crafted modpack featuring over 100 mods that revolutionize every aspect of your Viking journey. Whether you're a seasoned warrior or fresh recruit, Dogeheim offers an unparalleled gaming experience that will test your skills and reward your dedication.

### ⚠️ What to Expect

**Dogeheim is designed to be very hard** with increased monster XP, skill caps, and stamina requirements. This is not your typical Valheim experience - expect a **prolonged gametime** with strategic grinding, boss repetition, and intense combat encounters. This modpack is **actively in development** with consistent tweaks and improvements - please be patient as we perfect your ultimate Viking adventure. Multiplayer compatible, currently tweaked for 2-3 players, but is fairly balanced with 4.

---

## 📋 Table of Contents
- [Why Choose Dogeheim?](#-why-choose-dogeheim)
- [Core Systems](#-core-systems)
- [Installation](#-installation)
- [System Requirements](#-system-requirements)
- [Configuration Overview](#-configuration-overview)
- [Updating the Modpack](#-updating-the-modpack)
- [Multiplayer Setup](#-multiplayer-setup)
- [Known Issues & Support](#-known-issues--support)
- [Credits](#-credits)

---

## 🎮 Why Choose Dogeheim?

### 🌟 True MMO Progression System
- **Level Cap**: 120 levels with deep character progression
- **6 Attributes**: Strength, Dexterity, Intelligence, Endurance, Vigour, Specializing
- **Skill-Based Equipment**: Items locked behind skill level requirements
- **Experience Sharing**: Group-based XP distribution (70-unit range)
- **Balanced Death Penalties**: 5-20% XP loss (reduced from vanilla)
- **Attribute Caps**: Maximum 100 points per attribute for balanced gameplay

### ⚔️ Enhanced Combat & Magic Systems
- **Therzie Warfare**: Advanced weapons, bastard swords, claymores, and specialized combat mechanics
- **Therzie Wizardry**: Comprehensive spell system with arcane anvils, potions, and magical crafting
- **Therzie Armory**: Expanded weapon varieties and combat equipment
- **EpicLoot**: Five-tier magic item system (Magic→Rare→Epic→Legendary→Mythic) with enchantments
- **Magic Revamp**: Overhauled magical combat with new spell mechanics
- **ValheimEnchantmentSystem**: Weapon and armor enchanting with scrolls and materials

### 🌍 Massive World Expansion
- **Therzie Monstrum**: New creatures and challenging boss encounters across all biomes
- **Warpalicious World Locations**: Underground Ruins, Forbidden Catacombs, and enhanced POIs
- **Dynamic Seasons**: Weather patterns that affect gameplay, farming, and visibility
- **Biome Lords**: Quest system with unique rewards and progressive challenges
- **Extended Traders**: Additional NPCs and trading opportunities throughout the world

### 🛠️ Advanced Inventory & Quality of Life
- **Adventure Backpacks**: Tiered backpack system (2x3 to 5x7 slots) with upgrade progression
- **Quick Stack Store**: Advanced inventory management with smart sorting and stacking
- **Smart Containers**: Intelligent storage solutions that auto-organize items
- **Better UI**: Enhanced interface elements for improved user experience
- **Target Portals**: Advanced portal system for precise travel
- **Enhanced Cartography**: Shared mapping and pin systems for multiplayer coordination

### 🏗️ Comprehensive Building & Crafting
- **PlanBuild**: Blueprint system for complex construction projects
- **OdinArchitect**: Advanced building tools and architectural elements
- **blacks7ar Fine Wood Pieces**: Expanded building materials and decorative options
- **Enhanced Crafting Stations**: Specialized stations for different crafting disciplines
- **Cooking Additions**: Expanded culinary system with new recipes and cooking mechanics
- **Food Barrels**: Advanced food storage and preservation systems

### 🎣 Specialized Skills & Activities
- **Better Fishing**: Enhanced fishing mechanics with improved rewards and progression
- **Advanced Farming**: Expanded agriculture with seasonal crops and growing mechanics
- **Animal Husbandry**: Comprehensive taming and breeding systems
- **Mining & Lumberjacking**: Specialized progression trees for resource gathering
- **Sailing Improvements**: Enhanced seafaring with better ship mechanics

---

## 🔧 Core Systems

### MMO Progression (EpicMMOSystem)
```
Max Level: 120
Base XP Required: 300 per level (multiplier: 1.048)
Experience Rate: 1.2x standard
Group Experience: 0.9x (90% of normal when in party)
Death Penalty: 5-20% XP loss
Free Points per Level: 3 + bonus points at milestone levels
Attribute Maximums: 100 points each
```

### Creature & Boss Scaling
```
Boss Health per Star: 10-24% increase (varies by boss)
Boss Damage Scaling: Dynamic per boss type
Star Spawn Rates: Optimized for challenge progression
Drop Rates: 100% chance per star (creatures), 50% (bosses)
Level Range: MinRange: 10, MaxRange: 15 (for XP/loot eligibility)
```

### Magic Item System (EpicLoot)
```
Rarity Tiers: Magic (Gray) → Rare (Indigo) → Epic (Pink) → Legendary (Red) → Mythic (Orange)
Set Item Chance: 35% for legendary items
Enchanting Table: 6 functions (Sacrifice, Convert, Enchant, Augment, Disenchant, Upgrade)
Adventure Mode: Treasure maps, bounties, secret stashes enabled
```

### Inventory & Backpacks
```
Backpack Tiers: 5 upgrade levels
Slot Progression: 2x3 → 3x4 → 4x4 → 4x6 → 5x7
Weight Reduction: 100% normal weight for backpack contents
Portal Restrictions: Backpack contents checked for metal items
```

### Seasonal System
```
Day Length: 1800 seconds (30 minutes)
Season Effects: Weather, crop growth, and visual changes
Winter Features: Reduced bloom, snow particle optimization
Freezing Protection: Enabled outside Mountains/Deep North
Seasonal Items: Halloween, Midsummer, Yule decorations available
```

---

## 🚀 Installation

### Recommended: Thunderstore Mod Manager
1. **Download & Install** [Thunderstore Mod Manager](https://www.overwolf.com/app/Thunderstore-Thunderstore_Mod_Manager)
2. **Launch** the mod manager and select Valheim
3. **Search** for "Dogeheim" in the modpack browser
4. **Click** "Install with Dependencies"
5. **Launch** through the mod manager

### Using Profile Codes (R2modman)
If you want to use the exact configurations from Dogeheim, you can import the profile code:

1. **Open** R2modman
2. **Click** "Import Profile" or the import button
3. **Paste** the profile code from the latest changelog entry
4. **Confirm** the import and let R2modman download all mods
5. **Launch** through R2modman

**Note**: Profile codes are provided in each version's changelog and include all mods with their exact configurations. This ensures you get the intended balance and gameplay experience.

### Manual Installation
1. **Install** [BepInEx 5.4.2332](https://valheim.thunderstore.io/package/denikson/BepInExPack_Valheim/)
2. **Download** Dogeheim and all dependencies from Thunderstore
3. **Extract** all mods to `Valheim/BepInEx/plugins/`
4. **Copy** configuration files to `Valheim/BepInEx/config/`
5. **Launch** Valheim normally

### First-Time Setup
1. **Start** a new world (recommended for full experience)
2. **Check** that the MMO UI appears (level indicator, attribute points)
3. **Verify** magic items drop with colored names
4. **Test** backpack functionality with 'B' key
5. **Confirm** seasonal effects are active

---

## 💻 System Requirements

### Minimum Specifications
- **CPU**: Intel i5-4590 / AMD FX 8350 or equivalent
- **RAM**: 8GB (16GB strongly recommended)
- **GPU**: GTX 960 / R9 280 or equivalent
- **Storage**: 10GB free space for mods and cache
- **Network**: Stable internet for multiplayer

### Recommended Specifications
- **CPU**: Intel i7-7700K / AMD Ryzen 5 2600 or better
- **RAM**: 16GB+
- **GPU**: GTX 1060 / RX 580 or better
- **Storage**: SSD with 15GB+ free space
- **Network**: Broadband connection

### Performance Optimization
- **Graphics Settings**: Start with Medium, adjust based on performance
- **Particle Reduction**: Winter snow particles automatically reduced
- **Debug Logging**: Disabled by default in all mods
- **Memory Management**: Mods configured for optimal memory usage

---

## ⚙️ Configuration Overview

### Key Configuration Files
```
config/
├── WackyMole.EpicMMOSystem.cfg          # Core MMO progression
├── randyknapp.mods.epicloot.cfg         # Magic item system
├── Therzie.Warfare.cfg                  # Combat mechanics
├── Therzie.Wizardry.cfg                 # Magic system
├── org.bepinex.plugins.backpacks.cfg    # Inventory expansion
├── drop_that.cfg                        # Loot table management
├── spawn_that.cfg                       # Creature spawning
├── custom_raids.cfg                     # Raid event system
└── shudnal.Seasons.cfg                  # Seasonal mechanics
```

### Server Configuration
All major systems are **server-synchronized** for multiplayer compatibility:
- MMO progression settings locked to server
- Magic item configurations enforced
- Creature scaling synchronized
- Seasonal changes coordinated

### Customization Options
While core balance is locked, players can adjust:
- UI positioning and visibility
- Graphics and performance settings
- Keybind assignments
- Audio preferences

---

## 🔄 Updating the Modpack

### ⚠️ Pre-Update Backup Procedure

**CRITICAL**: Always backup before updating to prevent world/character loss.

#### 1. Backup Your World Data
```
Navigate to: %USERPROFILE%\AppData\LocalLow\IronGate\Valheim\
Copy these folders to a safe location:
├── worlds/           # Your world files
├── characters/       # Character progression
└── screenshots/      # Optional: your captured moments
```

#### 2. Backup Configuration Files
```
Navigate to: Valheim\BepInEx\config\
Copy entire config folder to safe location
Important files to preserve:
├── WackyMole.EpicMMOSystem.cfg
├── EpicMMOSystem/                 # Character progression data
├── ValheimEnchantmentSystem/      # Enchantment configurations
└── wackysDatabase/                # Item modifications
```

#### 3. Backup Local Mod Data
```
Navigate to: Valheim\BepInEx\cache\
Copy cache folder (contains mod-specific data)
```

### Update Process

#### Using Thunderstore Mod Manager (Recommended)
1. **Create Profile Backup**: Use mod manager's profile export feature
2. **Update Modpack**: Click "Update" when available
3. **Verify Dependencies**: Ensure all dependencies updated correctly
4. **Test Launch**: Start game and verify all systems functional

#### Manual Update Process
1. **Download** latest Dogeheim version
2. **Extract** new files to temporary folder
3. **Replace** old mod files with new versions
4. **Merge** configuration files carefully (compare old vs new)
5. **Launch** and verify functionality

### Post-Update Verification
- [ ] MMO system functional (level/XP display)
- [ ] Magic items still have proper colors/effects
- [ ] Backpacks accessible and contents intact
- [ ] Seasonal effects working
- [ ] Multiplayer synchronization active

### Rollback Procedure (If Issues Occur)
1. **Restore** world and character backups
2. **Replace** updated mod files with previous versions
3. **Restore** configuration backups
4. **Clear** mod cache folder
5. **Restart** game and verify stability

---

## 🌐 Multiplayer Setup

### Server Requirements
- **Dedicated Server**: Recommended for 3+ players
- **Mod Synchronization**: All players must have identical mod versions
- **Configuration Sync**: Server configurations automatically distributed

### Setting Up a Dedicated Server
1. **Install** Valheim Dedicated Server
2. **Install** BepInEx on server
3. **Copy** Dogeheim configuration to server
4. **Configure** server settings for player count
5. **Open** necessary ports (2456-2458 UDP)

### Player Requirements
- **Identical Modpack**: All players need same Dogeheim version
- **Character Sync**: MMO progression synchronized via server
- **World Sync**: Seasonal changes and events coordinated

### Multiplayer Balance
```
Boss Health Scaling: +40% per additional player
Boss Damage Scaling: +4% per additional player
Experience Range: 70 units for group sharing
Boss Drops: One trophy per player in range
Raid Frequency: Adjusted for group play
```

---

## 🐛 Known Issues & Support

### Current Known Issues

#### Bow & Arrow System
- **Issue**: Launching the game from R2mod man will take a while. BepinEx has to patch in all of the mods and configurations, it can take 5-10 minutes. But it will work! Please be patient. I'm sorry there isn't a workaround for this, it's annoying for me too.

#### Bow & Arrow System
- **Issue**: Bow draw blocked when arrows only in BBH quiver
- **Workaround**: Keep at least one arrow stack in main inventory. Also I am currently looking into just disabling the quiver system, it kinds of breaks the game.
- **Solution**: Use LeftShift+1-3 to select arrows from quiver bar

#### Performance Considerations
- **Winter Lag**: Snow particles automatically reduced (250/1000 vs 500/2000)
- **Memory Usage**: 16GB RAM recommended for optimal performance
- **Loading Times**: Initial world load may take 2-3 minutes. 

#### Mod Conflicts
- **Other Modpacks**: May conflict with major overhaul modpacks
- **Custom Mods**: Adding mods may break balance or cause issues
- **Version Mismatch**: Multiplayer requires identical mod versions

### Recent Fixes (v1.4.7)
- ✅ **Trader GUI Overlap**: Fixed visual conflicts with extended traders (kind of lol)
- ✅ **Divine Armament Balance**: Reduced early-game drop rates
- ✅ **Staff Progression**: Moved Staff of Artificer to appropriate tier
- ✅ **Black Forest Stability**: Resolved freezing issues

### Troubleshooting Guide

#### Game Won't Start
1. **Verify** BepInEx installation (check for winhttp.dll in game folder)
2. **Check** mod file integrity (re-download corrupted files)
3. **Review** console for error messages
4. **Disable** mods one by one to isolate issues

#### Mods Not Loading
1. **Confirm** all files in `BepInEx/plugins/` folder
2. **Check** dependencies are installed
3. **Verify** configuration files present
4. **Review** BepInEx console for mod loading errors

#### Multiplayer Issues
1. **Ensure** all players have identical mod versions
2. **Verify** server has all required mods
3. **Check** network connectivity and ports
4. **Confirm** server configuration synchronization

#### Performance Problems
1. **Lower** graphics settings to Medium
2. **Disable** bloom in Winter (automatic)
3. **Close** unnecessary background programs
4. **Verify** sufficient RAM available (16GB recommended)

### Getting Support

#### Community Resources
- **Discord**: dogebooch
- **Steam**: Friend Code 895642613
- **Email**: drummerfr3ak@gmail.com

#### Reporting Issues
When reporting bugs, please include:
- Dogeheim version number
- Detailed description of issue
- Steps to reproduce
- Console log files (if applicable)
- System specifications

#### Contributing
If you're familiar with Valheim modding and would like to contribute:
- Balance suggestions welcome
- Bug fixes appreciated
- New content ideas considered
- Wiki documentation help needed

---

## 📄 Credits & Acknowledgments

### Core Systems
- **WackyMole**: EpicMMOSystem, WackysDatabase
- **RandyKnapp**: EpicLoot magic item system
- **Smoothbrain**: Drop That, Spawn That systems

### Combat & Magic
- **Therzie**: Warfare, Wizardry, Armory, Monstrum series
- **blacks7ar**: Magic Revamp, Bow Plugin, cooking systems
- **Azumatt**: BowsBeforeHoes, inventory extensions

### World & Content
- **Warpalicious**: World expansion mods
- **Shudnal**: Seasons system
- **OdinPlus**: Building and crafting extensions
- **Digitalroot**: Forsaken content

### Quality of Life
- **Vapok**: Adventure Backpacks system
- **GoldenRevolver**: Quick Stack Store
- **Marcopogo**: PlanBuild blueprint system
- **Nexmods contributors**: Various enhancement mods

### Special Recognition
This modpack represents hundreds of hours of development from talented modders. Each mod retains its original license and authorship. Dogeheim serves as a curated experience showcasing these incredible works in harmony.

---

## 🎯 Ready for Your Epic Journey?

**Dogeheim awaits, warrior.** This isn't just another modpack - it's a complete transformation of Valheim into a challenging MMO experience where every battle matters, every level earned feels significant, and every victory is truly epic.

### Quick Start Checklist
- [ ] Install via Thunderstore Mod Manager
- [ ] Start fresh world for full experience  
- [ ] Invite friends for multiplayer adventure
- [ ] Check out the [Wiki](link-when-ready) for detailed guides
- [ ] Join the community for tips and strategies

**Remember**: This modpack is designed for extended play sessions and meaningful progression. Embrace the challenge, work with your team, and prepare for the ultimate Viking adventure.

*For optimal experience, ensure all multiplayer participants use identical mod versions.*
