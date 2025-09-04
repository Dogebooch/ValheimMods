# Dogeheim Changelog

## [1.6.10]
*Changes coming in the next version*

### 🔄 Changed
- **EpicLoot Backpack Consolidation**: Consolidated redundant EpicLoot material storage backpacks:
  - **Kept**: "EpicLoot Backpack" (6x4 → 7x4 upgrade path) - Primary storage for EpicLoot materials
  - **Removed**: "Andvaranaut Backpack" (5x2 → 5x3 upgrade path) - Redundant smaller backpack
  - **Benefits**: Eliminated confusion between two identical-purpose backpacks, streamlined EpicLoot material storage
  - **Configuration**: Updated `Backpacks.MajesticEpicLoot.yml` and `Detalhes.ItemRequiresSkillLevel.yml` in both main and Dogeheim configs

- **Complete Backpack Disabling**: Disabled all craftable backpacks for clean gameplay:
  - **Disabled**: All backpacks including EpicLoot Backpack and Mining Backpack
  - **Kept**: Backpacks mod itself (for potential future use or other mod integration)
  - **Benefits**: Eliminates "weird mechanic" feeling, cleaner vanilla-like experience
  - **Configuration**: Updated all backpack configs with `disabled: true` in both main and Dogeheim configs

- **Final Backpack Status**: All 12 backpacks completely disabled:
  - **EpicLoot Backpack**: Disabled (EpicLoot materials)
  - **Mining Backpack**: Disabled (ores/metals with weight reduction)
  - **General Backpacks**: All 10 disabled (Explorers, Simple, Foraging, Treasures, Troll, Food, Trophy, Scroll, Ammo, Wishbone)
  - **Result**: Clean, vanilla-like gameplay with no specialized storage containers
  - **Mod Status**: Backpacks mod remains active for potential future use or mod integration

### 🗑️ Removed
- **Bows Before Hoes (Azumatt)** - Removed due to quiver system conflicts:
  - **Issues**: Quiver system caused inventory slot problems and interaction conflicts
  - **Problems**: Interfered with other mod inventory systems and created slot management issues
  - **Benefits**: Cleaner inventory management, eliminated mod conflicts, improved stability
  - **Result**: Core bow functionality remains through other bow mods (BowPlugin, MagicBows, Bow of Frey)

---

## [1.6.9] - 2025-01-XX - Dependency Cleanup & Configuration Optimization

### ✨ Added
- **CraftingFilter (cjayride)** - Enhanced crafting interface with filtering capabilities
- **WieldEquipmentWhileSwimming (blacks7ar)** - Allows using weapons and tools while swimming

### 🔄 Changed
- **Dependency Updates**:
  - BepInEx updated to 5.4.2333
  - WackyEpicMMOSystem updated to 1.9.46
  - Marlthon-OdinShipPlus updated to 0.6.8
  - OdinsFoodBarrels updated to 1.2.0
  - SaveCrossbowState updated to 1.0.2
  - EpicLoot updated to 0.11.4
  - Jotunn updated to 2.26.1
  - RelicHeim updated to 5.4.12
  - HugotheDwarf-Shapekeys_and_More updated to 3.1.0

### 🗑️ Removed
- **ZenUI (ZenDragon)** - Removed unused UI framework
- **Character Customization (Balrond)** - Removed unused character appearance mod
- **Zen ModLib (ZenDragon)** - Removed unused core library
- **Adventure Backpacks (Vapok)** - Removed duplicate backpack system
- **PressurePlate (MSchmoecker)** - Removed unused mod
- **Display BepInEx Info** - Removed unused debugging mod

### ⚙️ Configuration Updates
- **WieldEquipmentWhileSwimming**: Configured to allow all equipment types in water with Hoe blacklisted
- **Hugo's Armory**: Disabled external localization to use built-in English only
- **Modpack optimization**: Removed conflicting and unused configurations for improved stability

---

## [1.6.8] - 2025-01-XX - New Mod Integration & Dependency Updates

### ✨ Added
- **ZenUI (ZenDragon)** - Enhanced UI framework for better mod integration
- **WieldEquipmentWhileSwimming (blacks7ar)** - Allows using weapons and tools while swimming
- **Character Customization (Balrond)** - Enhanced character appearance options
- **Zen ModLib (ZenDragon)** - Core library for ZenUI functionality

### 🔄 Changed
- **Dependency Updates**:
  - BepInEx updated to 5.4.2333
  - WackyEpicMMOSystem updated to 1.9.46
  - Marlthon-OdinShipPlus updated to 0.6.8
  - OdinsFoodBarrels updated to 1.2.0
  - SaveCrossbowState updated to 1.0.2
  - EpicLoot updated to 0.11.4
  - Jotunn updated to 2.26.1
  - RelicHeim updated to 5.4.12
- **Mod Integration**: New mods configured for seamless integration with existing modpack

### ⚙️ Configuration Updates
- **WieldEquipmentWhileSwimming**: Configured to allow all equipment types in water with Hoe blacklisted
- **ZenUI**: Optimized for compatibility with existing UI mods
- **Character Customization**: Integrated with existing character systems

---

## [1.6.7] - 2025-01-XX - Backpack System Optimization & Balance Patch

### 🔄 Changed
- **Status effect system consolidated** - Single balanced status effect provides consistent benefits:
  - **BackpackCarryBonus**: +50 carry weight, 20% weight reduction for items in backpack
- **Implementation note**: Changed from progressive scaling to single status effect due to Backpacks mod limitations
- **EpicLoot belts reverted** - Carry weight bonuses now work on both Shoulder and Utility slots
- **Quiver system completely disabled** - All quiver recipes disabled and upgrades blocked
- **Carry capacity adjuncts properly tier-gated** for appropriate game progression:
  - **BeltStrength**: Blacksmithing Level 25 (Bronze Age)
  - **Philosopher Stones (Red/Blue/Green/Purple)**: Blacksmithing Level 35 (Silver Age)
  - **FishExtract**: Fishing Level 50 (Mid-game)
  - **Philosopher Stone Black**: Blacksmithing Level 80 (Endgame)
  - **GP_Fader**: Blacksmithing Level 90 (Ultimate endgame)

### ⚙️ Recipe Balance Updates
- **Philosopher Stone recipes significantly upgraded** to match new skill requirements:
  - **Lower-tier Stones (Red/Blue/Green/Purple)**: 
    - Crafting station level increased from 1 to 3
    - Materials: Flask variants + Iron (10) + Silver (5)
    - Boss requirement: Elder defeated (`defeated_gdking`)
  - **Black Philosopher Stone**: 
    - New recipe added with crafting station level 5
    - Materials: Flask of the Gods (10) + BlackMetal (20) + YmirRemains (10)
    - Boss requirement: Seeker Queen defeated (`defeated_queen`)
- **Recipe progression now properly gates** carry capacity items behind appropriate boss progression and material tiers

### 🗑️ Removed
- **Adventure Backpacks mod completely disabled** - All crafting stations and recipes removed
- **Progressive backpack status effects** - Deleted unused level-specific status effect files
- **Quiver system** - All BowsBeforeHoes quiver recipes disabled and upgrades blocked

### 📝 Documentation Updates
- **Backpack wiki page updated** with comprehensive carry capacity adjunct information
- **Changelog entries** for all backpack system changes and balance updates
- **Implementation notes** added explaining technical limitations and design decisions

---

## [1.6.6] - 2025-01-XX - Initial Backpack System Implementation

### ✨ Added
- **Backpack system foundation** - Single upgradable backpack with consistent carry bonuses
- **Carry capacity adjuncts** - Various items providing additional weight bonuses
- **Skill-based progression** - Items gated behind appropriate skill levels and boss progression

### 🔄 Changed
- **Backpack mechanics consolidated** - Eliminated duplicate backpack systems
- **Status effect optimization** - Single balanced status effect for consistent benefits
- **Recipe balance** - Carry capacity items properly tier-gated for game progression

### ⚙️ Technical Improvements
- **Mod conflict resolution** - Eliminated overlapping backpack mechanics
- **Performance optimization** - Reduced redundant status effects and configurations
- **Balance integration** - Carry capacity system integrated with existing progression systems

---

## [1.6.6] - 2025-01-XX - Drop-Only Items Implementation

### ✨ Added
- **DragonslayerswordHTD** → Boss Drop-Only (Dragon, 0.002%)
- **ObsidianGreatswordHTD** → Creature Drop-Only (Stone Golem, 0.2%)
- **FlametalGreatswordHTD** → Boss Drop-Only (Fader, 0.002%)
- **TGCapeFlameFeather** → Creature Drop-Only (Wolf, 0.04%)

### 🔄 Changed
- **Summon Damage Nerf** (~50%) - Reduced EpicLoot affix for summoned-creature damage
- **BBP_ElvenBow** → Creature Drops (2% from Charred Archer or Fallen Valkyrie)
- **BBP_SeekerBow** → Boss Drop-Only (Seeker Queen, 3%)

### 🐛 Fixed
- **UI error and Parse errors** in wackysDatabase files

---

## [1.6.5] - 2025-01-XX - Drop-Only Item System *(Testing)*

### 🔄 Changed
- **Multiple high-tier items converted to drop-only**:
  - **Therzie Warfare**: BladeYagluth_TW, DualAxeDemonic_TW, ScytheVampiric_TW, DualScytheBloodthirst_TW, LanceDvergr_TW, WarpikeFlametal_TW, GreatbowDvergr_TW
  - **RtD Staffs**: MistlandsQuake_StaffRtD, AshlandsStaff3_RtD, DeepNorthStaff3_RtD, PlainsVoidstaff_RtD
  - **MagicBows**: BMB_LightningBow, BMB_SpiritBow
  - **Southsil Armor**: Samurai, Valk, Warlord sets
  - **Draconic Weapons**: GreatSword, Sword, Dagger, Scythe

### 📚 Documentation
- **Drop-Only Items Wiki** updated with comprehensive guide
- **Co-op optimization**: All boss specialty drops increased from 1 to 2 items

---

## [1.6.0] - 2025-01-XX - Drop-Only Item System *(Testing)*

### 🔄 Changed
- **Select high-tier items converted to drop-only rewards**:
  - **BowPlugin Items**: BBP Crossbows (Iron/Silver) removed duplicates
  - **BBP_ElvenBow**: Converted to drop-only (5% from Dragon)
  - **BBP_SeekerBow**: Converted to drop-only (5% from Queen)
  - **Therzie Warfare Items**: Multiple weapons converted with 5% drop rates
  - **Fire & Ice Expansion Staffs**: StaffVulkarion_TW, StaffSkrymir_TW, StaffStorm_TW
  - **RtD Staffs**: Multiple staffs converted with 5% drop rates
  - **MagicBows**: LightningBow, SpiritBow converted to drop-only

### 📚 Documentation
- **Drop-Only Items Wiki**: Comprehensive guide documenting all boss-specific drops
- **Drop Table Adjustments**: Co-op optimization and drop rate rebalancing

---

## [1.5.11] - 2025-01-XX - Global Bow Balance & Enchanting Integration

### 🔄 Changed
- **Bow Velocity/Draw-Time Normalization**:
  - Global stacking reduction from 4 to 3
  - Skill-based bow draw speed scaling implemented
  - Crossbow velocity rebalancing for proper progression
- **Quiver Armor Tuning**: All quivers set to Armor = 1
- **EpicLoot Material Drop Ratio**: Changed from 60% to 50/50 balance

### ✨ Added
- **Valheim Enchantment System Updates**:
  - Bow of Frey, Wizardry, MagicBows, ForsakenJVL, BowsBeforeHoes, BowPlugin, Warfare, Southsil Armor, Sages Vault, MagicRevamp, Hugo's Armory, Shawesome Divine Armaments, Biome Lords Quests

### 🐛 Fixed
- **Crafting Station Alignment**: Fletcher Table and Wizard Table integration

---

## [1.5.7] - 2025-01-XX - Missing Arrow Recipe Implementation

### ✨ Added
- **Missing Arrow Recipes**: Frost, Iron, Obsidian, Silver, Poison, Needle, Wood, Pickaxe, Bone arrows
- **Vanilla Trader Support**: Amber trading at reduced prices

### 🔄 Changed
- **Raid Configuration**: Restored RelicHeim raid frequency (60-minute intervals, 35% chance)
- **BowPlugin Integration**: Disabled duplicate crossbows to prevent confusion

---

## [1.5.6] - 2025-01-XX - Fletcher Table Ammunition Centralization

### 🔄 Changed
- **All ammunition crafting centralized** to Fletcher Table:
  - Antler Bolt, Fire Arrow, Flinthead Arrow, Flint Bolt, Torch Arrow, Bronze Bolt
- **Crafting station conflicts resolved** between Warfare and BowPlugin mods

---

## [1.5.5] - 2025-01-XX - Quiver Crafting Station Fix

### 🐛 Fixed
- **Quiver Recipe Fixes**: Black Forest, Lox, OdinPlus, Seeker quivers now properly use Fletching Table
- **Internal name correction**: All quiver recipes use proper `$piece_fletchertable_TW` reference

---

## [1.5.4] - 2025-01-XX - EpicMMO Balance Evaluation

### 🔄 Changed
- **EpicMMO scaling parameters**: User maintained original 0.3 scaling values for late-game power progression
- **Integration fixes**: VanillaShip_Integration.json created with correct RelicHeim patch formatting

---

## [1.5.3] - 2025-01-XX - AllTheHeims EpicLoot Integration

### ✨ Added
- **Comprehensive EpicLoot patches** for enhanced mod integration:
  - Adventure Backpacks, BowPlugin Weapons, SouthsilArmor Sets, HugosArmory Weapons
- **Proper rarity distributions** across Novus/Nexus/Zodiac/Zeta/Relic tiers
- **Haldor gamble system** with tier-appropriate coin costs

### 🐛 Fixed
- **Rarity display**: Restored Novus/Nexus/Zodiac/Zeta/Relic names
- **Menu text**: "Convert Items" instead of "Convert Shards"
- **Rarity colors**: Restored RelicHeim's custom color scheme

---

## [1.5.2] - 2025-01-XX - Magic Items Crafting Station Fixes

### 🐛 Fixed
- **Magic Weapons & Staffs**: Now use Wizard Table instead of workbench/forge
- **Magic Armor**: Now use Arcane Anvil instead of workbench
- **Crafting station consistency**: All magic items use appropriate stations

---

## [1.5.1] - 2025-01-XX - Missing Dependencies & Jotunn Update

### ✨ Added
- **5 missing bow-related mods** to complete dependency list
- **Jotunn Framework Update**: 2.26.0 → 2.26.1

---

## [1.5.0] - 2025-01-XX - EpicLoot Integration & Bow Combat Enhancement

### 🔄 Changed
- **Bow Velocity & Accuracy Balance**:
  - Global velocity multiplier reduced from 4 to 3
  - Skill-based bow draw speed scaling implemented
  - Crossbow velocity rebalancing for proper progression
- **EpicLoot Material Drop Ratio**: Changed from 60% to 50/50 balance

### ✨ Added
- **EpicLoot AllTheHeims Patches**: Comprehensive integration for enhanced loot variety
- **Quiver Crafting Station Centralization**: All quivers now crafted at Fletching Table
- **Enhanced loot variety**: 22+ different bow variants with unique properties

---

## [1.4.9] - 2025-01-XX - AzuAreaRepair Integration

### ✨ Added
- **AzuAreaRepair mod** for enhanced area repair functionalities

---

## [1.4.8] - 2025-01-XX - AzuCrafty Boxes Range Enhancement

### 🔄 Changed
- **Container range increased** from 20 to 50 units for better convenience

---

## [1.4.7] - 2025-01-XX - Trader Menu Overlap Fix

### 🐛 Fixed
- **Overlapping trader menus**: Resolved TradersExtended GUI positioning conflicts
- **Divine Armament drop rates**: Significantly reduced to maintain proper game balance

---

## [1.4.6] - 2025-01-XX - Staff of the Artificer Drop Rebalancing

### 🔄 Changed
- **Staff of the Artificer**: Moved from early-game Abomination to late-game Fader enemies
- **Drop chance**: Reduced from 4% to 1% for rarity

---

## [1.4.5] - 2025-01-XX - Greydwarf Spawn Rate Rebalancing

### 🔄 Changed
- **Greydwarf nest spawn rates**: Restored to base RelicHeim values
- **Spawn intervals**: 25 → 15 seconds for more consistent combat encounters

---

## [1.4.4] - 2025-01-XX - Black Forest Stability & Debugging

### 🐛 Fixed
- **Black Forest freezing issues**: Disabled problematic Doug's Lore Raids
- **Enhanced BepInEx logging**: Comprehensive logging for better debugging

### 🔄 Changed
- **EpicMMO System Balancing**: Attribute maximums reduced from 100 to 75 points
- **Doug's Lore Raids**: Removed chained raid system and forced environments

---

## [1.4.3] - 2025-01-XX - Passive Creature Spawn Balancing

### 🔄 Changed
- **Fish spawning**: Restored to base RelicHeim values for better fishing gameplay
- **Passive creature balance**: Maintained natural world density while preventing resource oversaturation

---

## [1.4.2] - 2025-01-XX - Comprehensive Skill Experience Rebalancing

### 🔄 Changed
- **Sneak skill**: Bonus experience increased from 10 to 13
- **Enchantment skill**: Skill gain factor increased from 0.55 to 0.8
- **Crossbow skill**: Skill gain factor increased from 0.6 to 0.78
- **Tenacity skill**: XP gain reduced but effectiveness increased
- **Fishing skill**: Significantly increased rewards for successful catches

---

## [1.4.1] - 2025-01-XX - Skill Experience Balance & Taming Optimization

### 🔄 Changed
- **Swimming skill**: Experience bonus increased from 100% to 150%
- **Ranching skill**: Experience gain increased from 0.6 to 1.2, taming speed improved
- **Cooking skill**: Experience gain reduced from 0.6 to 0.5

---

## [1.4.0] - 2025-01-XX - Fine Wood Furniture & Smart Containers

### ✨ Added
- **FineWoodBuildPieces mod** for expanded furniture and building options
- **SmarterContainers mod** for improved storage management

### 🔄 Changed
- **Food barrel crafting costs**: Increased for better game balance

---

## [1.3.9] - 2025-01-XX - Custom Raids & Enhanced Loot Systems

### ✨ Added
- **Doug's Lore Raids**: Four two-phase events with progressive difficulty scaling
- **Enhanced Cartography Table**: Improved map sharing functionality

### 🔄 Changed
- **Missing items**: Added to drop tables across multiple biomes
- **Loot variety**: Enhanced across all biomes for better exploration rewards

---

## [1.3.8] - 2025-01-XX - Better Cartography & Hugo's Armory Integration

### ✨ Added
- **Better Cartography Table mod** for enhanced group map sharing

### 🔄 Changed
- **Exploration skill**: Experience gain reduced from 0.48 to 0.35

---

## [1.3.7] - 2025-01-XX - Monster Difficulty Balance & Spawn Optimization

### 🔄 Changed
- **Creature size scaling**: Reduced from 14% to 12% per star
- **Star spawn chances**: Reduced by 30% across all world levels
- **Swamp creature spawn density**: Reduced by 50% to address overcrowding

---

## [1.3.5] - 2025-01-XX - Skill Tweaks, Gameplay & Progression Update

### 🔄 Changed
- **Workbench alignment**: Wizard Table and Cauldron integration
- **EpicMMO System**: Experience gain rate increased from 1.15 to 1.18
- **Death experience loss**: Removed from utility skills
- **Fishing skill**: XP rewards increased for better progression
- **Wool spawn rates**: Increased by 30-50% for better availability

---

## [1.3.4] - 2025-01-XX - Custom Seasonal Music

### ✨ Added
- **Custom music tracks** for all four seasons (currently debugging)

---

## [1.3.3] - 2025-01-XX - Configuration Changes

### 🔄 Changed
- **Drop configurations**: Multiple boss and creature drop adjustments
- **EpicLoot settings**: Material drop ratio and loot balance adjustments

---

## [1.3.2] - 2025-01-XX - Initial Release

### ✨ Added
- **Base modpack configuration** with comprehensive mod integration
- **RelicHeim foundation** with custom configurations

---

## 📋 Changelog Guidelines

This changelog follows the [Keep a Changelog](https://keepachangelog.com/) format and uses the following categories:

- **✨ Added** - New features
- **🔄 Changed** - Changes in existing functionality
- **🐛 Fixed** - Bug fixes
- **⚠️ BREAKING CHANGES** - Changes that require user action
- **📚 Documentation** - Documentation updates
- **🔧 Technical** - Technical improvements
