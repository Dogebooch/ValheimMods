# DogeheimTesting.db - Valheim World Database Analysis

## Overview
This document provides a comprehensive analysis of the `DogeheimTesting.db` file, which is a Valheim world database containing player data, items, and world state information.

## File Information
- **Filename**: DogeheimTesting.db
- **Size**: 10.37 MB (10,872,879 bytes)
- **Analysis Date**: 2025-08-06T16:36:38
- **File Type**: Valheim Custom Binary Database Format

## Database Structure

### Header Information
- **Magic Number**: 35 (0x00000023)
- **Format**: Custom Valheim binary format (not SQLite)

### Data Composition
- **Null Bytes**: 1,398,569 (12.86% of file)
- **Most Common Bytes**:
  - 0x00: 1,398,569 times (null bytes)
  - 0xff: 451,916 times
  - 0x43: 373,376 times
  - 0x42: 317,736 times
  - 0xc4: 273,063 times

## Extracted Content

### Player Information
- **Player Name**: Dogeo
- **Character Data**: Contains player inventory, skills, and progression

### Items and Equipment
The database contains extensive item data including:

#### EpicLoot Enchanted Items
1. **Deer Hide Cape** - Epic rarity with effects:
   - ModifyEitrRegen: +11.0
   - AddPiercingResistancePercentage: +5.0

2. **BattleaxeBronze_TW** - Epic rarity with effects:
   - RemoveSpeedPenalty: +1.0
   - ModifyParryWindow: +77.0
   - EitrWave: +4.0

3. **BattlehammerElder_TW** - Epic rarity with effects:
   - LifeSteal: +2.0
   - AddPoisonDamage: +6.0
   - AddClubsSkill: +5.0

4. **LeatherBelt** - Epic rarity with effects:
   - ModifyDiscoveryRadius: +8.4
   - ModifySprintStaminaUse: +6.0

5. **WarpikeChitin_TW** - Epic rarity with effects:
   - AddPoisonDamage: +5.0
   - LifeSteal: +1.5
   - ModifyParry: +7.5

#### Blacksmithing Items
- **BMR_EmberStaff** - Staff with enchantments
- **BMR_EmberWand** - Wand with enchantments
- **BMR_WoodenStaff** - Staff with enchantments
- **Staffbase_BlackForest_TW** - Base staff

#### Armor and Equipment
- **HelmetTrollLeather** - Troll leather helmet with effects:
  - IncreaseEitr: +9.0
  - ModifyDiscoveryRadius: +8.7

- **CapeDeerHide** - Deer hide cape with effects:
  - ModifyArmor: +3.5

- **CrossbowBronze_TW** - Bronze crossbow with effects:
  - ModifyDurability: +80.0
  - ModifyStaggerDuration: +3.0

- **ShieldBoneTower** - Bone tower shield with effects:
  - QuickLearner: +3.0
  - Immovable: +1.0

#### Cooking and Food Items
- **BerryCandyBlackForest_TW** - Cooking skill item
- **ShroomSoupBlackForest_TW** - Cooking skill item
- **BearJerky_TW** - Cooking skill item
- **BoarJerky** - Cooking skill item
- **MincedMeatSauce** - Cooking skill item
- **NeckTailGrilled** - Cooking skill item
- **CookedFoxMeat_TW** - Cooking skill item
- **CookedMeat** - Various cooked meat items
- **Honey** - Honey item

#### Crafting and Materials
- **Cultivator** - Farming tool
- **Heavybronzechest** - Heavy bronze chest armor
- **Heavybronzelegs** - Heavy bronze leg armor
- **RawMeat** - Raw meat
- **Thistle** - Thistle plant
- **DeerMeat** - Deer meat
- **FoxPelt_TW** - Fox pelt
- **BlackBearPelt_TW** - Black bear pelt
- **TrollHide** - Troll hide
- **DeerHide** - Deer hide
- **RazorbackLeather_TW** - Razorback leather
- **RazorbackTusk_TW** - Razorback tusk
- **ShardElder_TW** - Elder shard
- **BoneFragments** - Bone fragments
- **WoodScraps_TW** - Wood scraps

#### Scrolls and Magic Items
- **BMR_IceScroll2** - Ice magic scroll
- **BMR_PoisonScroll1** - Poison magic scroll
- **BMR_PoisonScroll2** - Poison magic scroll
- **BMR_SkeletonScroll** - Skeleton magic scroll
- **BMR_SurtlingScroll** - Surtling magic scroll
- **BMR_IceScroll1** - Ice magic scroll
- **BMR_FireScroll2** - Fire magic scroll
- **BMR_FireScroll1** - Fire magic scroll
- **FreyjaEssence_TW** - Freyja essence
- **BMR_LightningEssence** - Lightning essence
- **BMR_HealScroll1** - Healing scroll
- **BMR_PoisonScroll3** - Poison magic scroll
- **RunestoneMagic** - Runestone with magic
- **kg_EnchantScroll_Armor_D** - Armor enchantment scroll
- **ShardMagic** - Magic shard
- **DustMagic** - Dust magic
- **RunestoneRare** - Rare runestone
- **InfusedCrystal_JH** - Infused crystal
- **ShardElder_TW** - Elder shard
- **DustEpic** - Epic dust
- **ShardLegendary** - Legendary shard
- **DustLegendary** - Legendary dust
- **RunestoneLegendary** - Legendary runestone

### Mod Integration
The database shows integration with several mods:
- **EpicLoot** - Magic item enchantment system
- **Blacksmithing** - Enhanced crafting system
- **Cooking** - Enhanced cooking system
- **ValheimEnchantmentSystem** - Enchantment framework

## Technical Analysis

### Data Sections
- **Large Zero Runs**: 2 significant empty regions
- **Data Regions**: 10 major data blocks
- **Zlib Signatures**: 363 potential compressed sections
- **High Entropy Sections**: 20 sections with high data complexity

### String Extraction
- **ASCII Strings Found**: 50 meaningful strings
- **Potential Names**: Various item and player identifiers
- **Mod References**: Multiple mod names and component references

## File Structure Insights

### Binary Format
The file uses a custom binary format with:
- 4-byte header (magic number: 35)
- Mixed data types (strings, numbers, binary data)
- Potential compression in some sections
- Structured data blocks with varying sizes

### Data Organization
- Player data appears to be stored in structured blocks
- Item data includes metadata, enchantments, and properties
- Mod data is integrated throughout the file
- World state information is embedded in the binary structure

## Usage Notes

### For Mod Developers
- The database contains extensive mod integration data
- EpicLoot enchantments are well-represented
- Blacksmithing and cooking mods have significant data presence
- Custom item types and properties are stored

### For Players
- Contains complete character progression data
- All equipped items and inventory contents
- Skill levels and experience data
- World exploration and building data

## File Location
- **Original**: `Valheim_PlayerWorldData/worlds_local/DogeheimTesting.db`
- **Readable Versions**: 
  - JSON: `Valheim_Help_Docs/@Valheim_Binary_Readable/DogeheimTesting_readable_20250806_163647.json`
  - Text: `Valheim_Help_Docs/@Valheim_Binary_Readable/DogeheimTesting_readable_20250806_163656.txt`

## Conclusion
The DogeheimTesting.db file is a comprehensive Valheim world database containing extensive player data, item information, and mod integration. The file shows heavy use of EpicLoot and other enhancement mods, with a well-developed character carrying numerous enchanted items and materials.

The binary format is complex but structured, allowing for detailed analysis of game state and mod interactions. This analysis provides valuable insights into Valheim's data storage methods and mod integration capabilities.
