# BepInEx Configuration Documentation

This document provides a comprehensive overview of the BepInEx configuration directory structure and file formats for a heavily modded Valheim server. The configuration files control various aspects of gameplay, from basic mod settings to complex spawn systems and item requirements.

## Directory Structure

```
BepInEx/
├── config/                    # Main configuration directory
│   ├── wackyDatabase-BulkYML/ # Custom item/creature database
│   │   ├── Items/            # Item definitions
│   │   ├── Creatures/        # Creature definitions
│   │   ├── Recipes/          # Crafting recipes
│   │   └── Pickables/        # Harvestable items
│   ├── .git/                 # Version control
│   └── .snapshots/           # Configuration snapshots
└── [other BepInEx directories]
```

## Configuration File Types

### 1. Standard BepInEx Configuration Files (.cfg)

These files use the standard BepInEx configuration format with sections, keys, and values.

#### Format Example:
```ini
[SectionName]

## Description of setting
# Setting type: DataType
# Default value: defaultValue
# Acceptable values: value1, value2, value3
SettingName = value
```

#### Key Configuration Files:

**BepInEx.cfg** (5.6KB, 157 lines)
- Core BepInEx framework settings
- Controls logging, caching, console output
- Sections: Caching, Chainloader, Harmony.Logger, Logging, Logging.Console, Logging.Disk

**spawn_that.cfg** (3.4KB, 110 lines)
- Spawn That mod configuration
- Controls creature spawning systems
- Sections: Datamining, Debug, LocalSpawner, Simple, SpawnAreaSpawner, WorldSpawner

**custom_raids.cfg** (3.9KB, 110 lines)
- Custom Raids mod configuration
- Controls raid event system
- Sections: Debug, EventSystem, General, IndividualRaids

**WackyMole.EpicMMOSystem.cfg** (42KB, 1374 lines)
- Epic MMO System configuration
- RPG-style leveling and progression system
- Sections: General, LevelSystem, Skills, Combat, etc.

### 2. YAML Configuration Files (.yml)

These files use YAML format for more complex data structures.

#### CreatureConfig_Creatures.yml (4.7KB, 288 lines)
**Purpose**: Configures creature stats and behaviors by biome
**Format**:
```yaml
#Meadows
Greyling:
  health: 1.5
  damage: 2
  damage per star: 0.6
Neck:
  damage: 2
  health: 4
  health per star: 2
```

**Structure**:
- Organized by biome (Meadows, BlackForest, Swamp, Mountains, etc.)
- Each creature has base stats and per-star multipliers
- Some creatures have biome-specific variations
- Supports special effects like infusions

#### Detalhes.ItemRequiresSkillLevel.yml (247KB, 12457 lines)
**Purpose**: Defines skill requirements for crafting and equipping items
**Format**:
```yaml
- PrefabName: 9bchest
  Requirements:
    - Skill: Blacksmithing
      Level: 20
      BlockCraft: true
      BlockEquip: false
      EpicMMO: false
      ExhibitionName: 
```

**Structure**:
- Each item has a PrefabName and Requirements list
- Skills include: Blacksmithing, Cooking, Farming, etc.
- Controls both crafting and equipping restrictions
- Integrates with EpicMMO system

#### warpalicious.More_World_Locations_CreatureLists.yml (31KB, 1330 lines)
**Purpose**: Defines creature spawn lists for different location types
**Format**:
```yaml
MeadowsCreatures1:
  # Common locations - Diverse mix for early-game progression
  - Skeleton
  - Skeleton_Poison
  - Skeleton_NoArcher
  # Rare spawns for excitement
  - Skeleton_NoArcher
  - Skeleton_Poison
```

**Structure**:
- Organized by biome and location tier (Creatures1, Creatures2, etc.)
- Lists creature prefab names for spawn pools
- Comments indicate spawn frequency and purpose
- Supports thematic consistency and progression

### 3. WackyDatabase Bulk YML Files

Located in `wackyDatabase-BulkYML/` directory, these files define custom game content.

#### Items Directory
Contains individual YAML files for each custom item (79+ files)
**Example: Item_SimpleBackpack.yml**
```yaml
name: SimpleBackpack
m_weight: 4
m_name: $item_SimpleBackpack
m_description: $itemdesc_SimpleBackpack
m_maxStackSize: 1
m_canBeReparied: false
m_teleportable: true
m_backstabbonus: 4
m_knockback: 10
m_useDurability: false
m_maxDurability: 1200
m_durabilityPerLevel: 50
m_skillType: Swords
m_animationState: OneHanded
m_itemType: Misc
m_toolTier: 0
m_maxQuality: 2
m_value: 0
```

**Structure**:
- Standard Valheim item properties
- Custom modifiers and effects
- Integration with skill systems
- Quality and durability settings

## Major Mod Categories

### 1. Spawn and Creature Mods
- **Spawn That**: Advanced creature spawning system
- **Custom Raids**: Custom raid event system
- **Creature Level and Loot Control**: Creature scaling and drops
- **More World Locations**: Additional spawn locations

### 2. RPG and Progression Mods
- **Epic MMO System**: Level-based progression
- **Item Requires Skill Level**: Skill-gated content
- **Smart Skills**: Enhanced skill system
- **Epic Loot**: Enhanced loot system

### 3. Building and Crafting Mods
- **Plant Everything**: Plant placement system
- **Fine Wood Build Pieces**: Additional building pieces
- **Cooking Additions**: Enhanced cooking system
- **Blacksmithing**: Enhanced crafting system

### 4. Quality of Life Mods
- **Quick Stack Store**: Inventory management
- **Extended Player Inventory**: Larger inventory
- **Backpacks**: Additional storage options
- **Mouse Tweaks**: UI improvements

### 5. Content Expansion Mods
- **Therzie Mods**: Armory, Warfare, Wizardry, Monstrum
- **Warpalicious Packs**: Biome-specific content packs
- **Blacks7ar Mods**: Magic, cooking, and building additions
- **Azumatt Mods**: Various utility and enhancement mods

## Configuration Management

### Version Control
- `.git/` directory indicates version control is active
- `.snapshots/` directory for configuration backups
- Allows tracking changes and rollbacks

### File Sizes and Complexity
- Largest files: southsil.SouthsilArmor.cfg (526KB), blacks7ar.MagicRevamp.cfg (364KB)
- Most complex: Epic MMO System with 1374 lines
- YAML files can be very large (ItemRequiresSkillLevel.yml: 247KB)

### Integration Points
- Mods often reference each other's configurations
- Epic MMO System integrates with skill requirements
- Spawn systems work together for comprehensive creature management
- Item databases support multiple mod systems

## Key Configuration Patterns

### 1. Boolean Toggles
```ini
# Setting type: Boolean
# Default value: false
EnableFeature = true
```

### 2. Numeric Values
```ini
# Setting type: Single
# Default value: 1.0
Multiplier = 1.5
```

### 3. String Lists
```ini
# Setting type: String
# Acceptable values: value1, value2, value3
Selection = value1
```

### 4. YAML Lists
```yaml
CreatureList:
  - Creature1
  - Creature2
  - Creature3
```

### 5. Nested YAML Structures
```yaml
Creature:
  BaseStats:
    health: 100
    damage: 10
  BiomeVariants:
    Meadows:
      health: 80
    Mountains:
      health: 120
```

This configuration system provides extensive customization for a complex modded Valheim experience, with multiple interconnected systems working together to create a comprehensive gameplay experience.
