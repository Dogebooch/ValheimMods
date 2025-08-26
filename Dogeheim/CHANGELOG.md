# Dogeheim Modpack Changelog

---

## Version 1.4.7 - Trader Menu Overlap Fix *(Testing)*

*Fixed overlapping trader menus caused by TradersExtended GUI positioning conflicts.*

#### Trader Interface Fix
- **Fixed overlapping trader menus**: Resolved visual conflict where two trader interfaces would overlap
  - **Root cause**: TradersExtended mod was using fixed GUI positioning `{"x":200.0,"y":150.0}` that conflicted with base game trader interface
  - **Solution**: Reset GUI position to default `{"x":0.0,"y":0.0}` to allow natural positioning
  - **Files updated**: 
    - `config/shudnal.TradersExtended.cfg`
    - `Dogeheim/Configs/shudnal.TradersExtended.cfg`
- **Impact**: Trader menus now display properly without visual overlap or positioning conflicts

#### TradersExtended Configuration Review
- **Comprehensive review completed** of all TradersExtended settings for potential conflicts
- **Confirmed optimal settings** for compatibility with other UI mods
- **No additional conflicts found** in current configuration

#### Divine Armaments Drop Rate Rebalancing
- **Significantly reduced divine armament drop rates** to maintain proper game balance and progression:
  - **Ultimate divine weapons** (Odin's Spear, Svandëm's Bow, Divine Chest): **0.8-1.0% → 0.2%** (5x rarer)
  - **Fire divine gear** (Shawesome Fire Helm/Chest, Fire Swords): **1.0% → 0.3%** (3x rarer)
  - **Frost divine gear** (Shawesome Frost Helm/Chest/Legs): **1.0% → 0.3%** (3x rarer)
  - **Divine capes** (Fire God Surtur Cape, Frost God Jotnar Cape): **0.8-1.0% → 0.2%** (5x rarer)
- **Added level-gated safety restrictions** to prevent early-game acquisition:
  - **Fader drops**: Require minimum level 3 creatures + player kills only
  - **Deep North/Ashlands drops**: Require minimum level 4 creatures + player kills only
- **Root cause addressed**: Previous 1-4% drop rates were causing game-breaking early acquisition
- **Impact**: Divine armaments now properly rare (1 in 300-500 kills) and limited to appropriate end-game content
- **Files updated**:
  - `config/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.additional_missing_items.Doug.cfg`
  - `config/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.missing_items.Doug.cfg`
  - `Dogeheim/Configs/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.additional_missing_items.Doug.cfg`
  - `Dogeheim/Configs/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.missing_items.Doug.cfg`

---

## Version 1.4.6 - Staff of the Artificer Drop Rebalancing *(Testing)*

*Moved Staff of the Artificer from early-game Abomination to late-game Fader enemies for better loot progression and game balance.*

#### Staff of the Artificer Drop Changes
- **Removed from Abomination**: Disabled Staff of the Artificer drops from Swamp biome Abominations
  - **Previous**: 4% drop chance from early-game enemies
  - **Issue**: Players getting end-game weapons too early in progression
- **Added to Fader**: Staff of the Artificer now drops from Ashlands Fader enemies
  - **New drop chance**: 1% (reduced from 4% for rarity)
  - **Better progression**: Players encounter Faders when they have access to required materials
  - **Appropriate difficulty**: Fader enemies match the item's power level and crafting requirements

#### Loot Progression Improvements
- **Material access**: Players will have Arcanium, HasRefiner_Item, and FlametalNew when they reach Ashlands
- **Skill requirements**: Blacksmithing level 80 requirement aligns with late-game progression
- **Thematic fit**: High-tier magical weapon from Shawesomes_Divine_Armaments mod suits end-game enemies
- **Rarity balance**: 1% drop chance makes it a valuable and rare find

#### Configuration Files Updated
- `config/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.additional_missing_items.Doug.cfg`
- `Dogeheim/Configs/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.additional_missing_items.Doug.cfg`

---

## Version 1.4.5 - Greydwarf Spawn Rate Rebalancing *(Testing)*

*Reverted greydwarf nest spawn rates to base RelicHeim values for improved game balance and stability.*

#### Greydwarf Nest Spawner Adjustments
- **Restored greydwarf nest spawn rates to base RelicHeim configuration**:
  - `config/_RelicHeimFiles/Drop,Spawn_That/spawn_that.spawnarea_spawners.PilesNests.cfg`:
    - **SpawnInterval**: 25 → 15 seconds (faster spawning, base RelicHeim value)
    - **ConditionMaxCloseCreatures**: 4 → 2 (standard creature limits)
    - **SpawnWeight**: 8 → 5 (standard spawn chance for regular greydwarfs)
- **Applied to both main config and Dogeheim directory** for consistency
- **Impact**: More frequent but balanced greydwarf spawning at nests, matching original RelicHeim experience

#### Spawn Configuration Rationale
- **Faster spawn intervals**: 15-second intervals provide more consistent combat encounters
- **Standard creature limits**: Maximum 2 greydwarfs near nests prevents overwhelming players
- **Balanced spawn weights**: Regular greydwarfs (5) spawn more often than elites (1) and shamans (1)
- **Maintains challenge**: Keeps Black Forest engaging without being overwhelming

---

## Version 1.4.4 - Black Forest Stability & Debugging Improvements *(Testing)*

*Fixed critical Black Forest freezing issues and enhanced debugging capabilities for better troubleshooting.*

#### Black Forest Raid Stability Fixes
- **Disabled problematic Doug's Lore Raids** that were causing Black Forest freezing:
  - `config/_RelicHeimFiles/Raids/custom_raids.supplemental.DougsLoreRaids.cfg`:
    - **Elder_Rite_P1_JH**: Disabled (was causing chained raid conflicts)
    - **Elder_Rite_P2_JH**: Disabled (chained raid with environment conflicts)
- **Root cause identified**: Chained raids with forced environment changes (`DeepForest Mist` → `ThunderStorm`) and high spawn rates (95% per interval) were overwhelming the game's systems
- **Impact**: Should resolve freezing and crashing issues specifically in Black Forest biome

#### Enhanced BepInEx Logging Configuration
- **Enabled comprehensive logging** for better debugging and error tracking:
  - `config/BepInEx.cfg`:
    - **Console Log Levels**: Added `Info` level for detailed console output
    - **Disk Log Levels**: Added `Message, Info` levels for comprehensive log files
    - **Unity Log Listening**: Enabled to catch Unity-specific errors
- **Benefits**: Better visibility into mod conflicts, performance issues, and error tracking

#### Doug's Lore Raids Analysis & Improvements
- **Identified and fixed critical issues** in remaining Doug's Lore raids:
  - **Removed chained raid system**: Eliminated `OnStopStartRaid` to prevent cascading effects
  - **Reduced spawn rates**: All raids reduced from 95% to 65% spawn chance per interval for better balance
  - **Removed forced environments**: Eliminated `ForceEnvironment` settings to prevent conflicts with other mods
  - **Made all raids independent**: Each raid now operates independently without chaining
- **Specific improvements made**:
  - **Bog Uprising raids**: Removed chaining and forced environments, reduced spawn rates
  - **Hunt of Moder raids**: Removed chaining and forced environments, reduced spawn rates  
  - **Warband of Yagluth raids**: Removed chaining and forced environments, reduced spawn rates
  - **Black Forest raids**: Remain disabled due to previous stability issues

#### EpicMMO System Balancing & Quality of Life Improvements
- **Attribute Maximums**: Reduced from 100 to 75 points for all attributes (Strength, Dexterity, Intelligence, Endurance, Vigour, Specializing)
- **Enhanced Bonus Points**: Extended bonus point system to level 120 with improved progression:
  - Levels 5-90: Enhanced bonus points (e.g., level 15: +3, level 20: +4, level 60: +5)
  - Levels 95-120: New bonus points (level 95: +4, level 100: +5, level 120: +7)
- **Improved Drop System**: Enabled drops from non-player kills (`RemoveAllDrops From NonPlayer Kills = false`)
- **Mob Level Display**: Removed mob level UI string for cleaner interface
- **Better Balance**: Attribute caps prevent overpowered characters while maintaining progression

#### Backup Configuration Created
- **Automatic backup** of modified configuration files created in `config/backup_before_debug/`
- **Safe rollback**: Original configurations preserved for easy restoration if needed

---

## Version 1.4.3 - Passive Creature Spawn Balancing *(Testing)*

*Adjusted passive creature spawning rates to improve world balance and reduce resource competition.*

#### Fish Spawning Adjustments
- **Restored fish spawning to base RelicHeim values** for better fishing gameplay:
  - `config/spawn_that.simple.cfg`:
    - **Fish1, Fish2, Fish3**: All multipliers restored to 1.0 (from 0.8/0.7)
    - **SpawnMaxMultiplier**: 0.8 → 1.0 (+25% max fish spawns)
    - **GroupSizeMinMultiplier**: 0.8 → 1.0 (+25% min group size)
    - **GroupSizeMaxMultiplier**: 0.8 → 1.0 (+25% max group size)
    - **SpawnFrequencyMultiplier**: 0.7 → 1.0 (+43% spawn frequency)
- Improves fishing experience by restoring natural fish density while maintaining balance

#### Passive Creature Spawn Analysis
- **Deer and Boar**: Maintained at base RelicHeim values (1.0 multipliers)
- **Neck**: Reduced to 0.8 multipliers for better resource balance
- **Crow, FireFlies, Seagal**: Maintained at base values for natural world feel
- **All other passive creatures**: Using base RelicHeim spawn rates

#### Spawn Configuration Documentation
- **No global spawn reductions found** - all adjustments are creature-specific
- **Fish spawning was previously reduced** but has been restored to improve fishing gameplay
- **Passive creature balance** maintains natural world density while preventing resource oversaturation

---

## Version 1.4.2 - Comprehensive Skill Experience Rebalancing *(Testing)*

*Major skill experience rebalancing to address progression disparities and improve gameplay balance across all skill types.*

#### Sneak Skill Experience Boost
- **Increased sneak skill bonus experience** for better stealth gameplay rewards:
  - `config/org.bepinex.plugins.smartskills.cfg`:
    - `Sneak bonus experience`: 10 → 13 (+30% bonus XP for sneak attacks)
- Encourages more strategic stealth gameplay and rewards successful sneak attacks

#### Enchantment Skill Experience Boost
- **Significantly increased enchantment skill experience gain** to address lagging progression:
  - `config/ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg`:
    - `Skill gain factor`: 0.55 → 0.8 (+45% XP gain)
- Addresses the difficulty of progressing enchantment skill with limited access to enchantment opportunities

#### Crossbow Skill Experience Boost
- **Increased crossbow skill experience gain** for better ranged combat progression:
  - `config/Therzie.Warfare.cfg`:
    - `skill_99738506 Skill gain factor`: 0.6 → 0.78 (+30% XP gain)
- Improves progression for crossbow users and ranged combat specialists

#### Tenacity Skill Rebalancing
- **Reduced tenacity skill experience gain** but increased effectiveness:
  - `config/org.bepinex.plugins.tenacity.cfg`:
    - `Skill gain factor`: 0.3 → 0.2 (-33% XP gain, slower progression)
    - `Skill effect factor`: 1.2 → 1.35 (+15% effectiveness at higher levels)
- Creates a more meaningful progression curve with stronger rewards at higher skill levels

#### Blacksmithing Skill Experience Adjustment
- **Slightly reduced blacksmithing skill experience gain** to balance common skill usage:
  - `config/org.bepinex.plugins.blacksmithing.cfg`:
    - `Skill Experience Gain Factor`: 0.7 → 0.6 (-14% XP gain)
- Maintains balanced progression for frequently used crafting skill

#### Fishing Skill Experience Enhancements
- **Significantly increased fishing skill rewards** for successful catches:
  - `config/kam1goroshi.BetterFishing.cfg`:
    - `Hook_Exp_Multiplier`: 4.0 → 5.0 (+25% XP while reeling)
    - `Steps_For_Catch`: 12 → 16 (+33% XP bonus on successful catch)
    - `Bonus_Per_Fish_Level`: 0.8 → 1.0 (+25% bonus for star-level fish)
- Rewards successful fishing more generously while maintaining the challenge

#### Missing Skill Configurations
- **Note**: Jump, run, blocking, and alchemy skills were not found in the current configuration files
- These skills may be handled by different mods or may not have separate configuration options
- Further investigation may be needed to locate these skill configurations if they exist

---

## Version 1.4.1 - Skill Experience Balance & Taming Optimization *(Testing)*

*Adjusted skill experience gains and taming mechanics for better progression balance and reduced frustration.*

#### Swimming Skill Experience Boost
- **Increased swimming skill experience gain** to better match moderate usage patterns:
  - `config/org.bepinex.plugins.smartskills.cfg`:
    - `Swimming experience bonus`: 100% → 150% (+50% XP gain)
- Addresses the skill level disparity where swimming lags behind other skills in mid-game progression

#### Ranching Skill Experience & Taming Speed Improvements
- **Significantly increased ranching skill experience gain** for low-usage skill progression:
  - `config/org.bepinex.plugins.ranching.cfg`:
    - `Skill Experience Gain Factor`: 0.6 → 1.2 (+100% XP gain)
- **Improved taming speed** to reduce frustration with long taming times:
  - `config/org.bepinex.plugins.ranching.cfg`:
    - `Taming Factor`: 2.0 → 3.0 (+50% faster taming)
- Addresses the difficulty of progressing ranching skill with limited animal access

#### Cooking Skill Experience Adjustment
- **Slightly reduced cooking skill experience gain** to balance common skill usage:
  - `config/org.bepinex.plugins.cooking.cfg`:
    - `Skill Experience Gain Factor`: 0.6 → 0.5 (-17% XP gain)
- Maintains balanced progression for frequently used cooking skill

---

## Version 1.4.0 - Fine Wood Furniture & Smart Containers *(Testing)*

*Added fine wood furniture building pieces and smart container functionality for enhanced building and storage options.*

#### Fine Wood Build Pieces Integration
- **Added FineWoodBuildPieces mod** for expanded furniture and building options:
  - Enhanced fine wood furniture crafting recipes
  - Additional decorative building pieces
  - Improved aesthetic options for base building
- **Mod**: `blacks7ar-FineWoodBuildPieces-1.1.7`

#### Smart Containers System
- **Added SmarterContainers mod** for improved storage management:
  - Enhanced container functionality and organization
  - Better inventory management features
  - Improved storage capacity and sorting options
- **Mod**: `Roses-SmarterContainers-1.7.0`

#### Food Barrel Recipe Rebalancing
- **Reapplied food barrel crafting cost increases** for better game balance:
  - Increased crafting costs from 10 to 15 items for most barrels
  - OdinsSeedBag increased from 5 to 8 DeerHide
  - Maintains balance while allowing for increased storage capacity
- **Configuration**: `config/gravebear.odinsfoodbarrels.cfg`

---

## Version 1.3.9 - Custom Raids & Enhanced Loot Systems *(Testing)*

*Added lore-accurate custom raids and expanded loot distribution across biomes for improved exploration rewards.*

#### Custom Raids - Doug's Lore Raids
- **Added comprehensive custom raid system** with four two-phase events:
  - `config/_RelicHeimFiles/Raids/custom_raids.supplemental.DougsLoreRaids.cfg`:
    - **Elder Rite**: Black Forest ritual with Greydwarf shamans and elites
    - **Bog Uprising**: Swamp uprising with Draugr, blobs, and wraiths
    - **Hunt of Moder**: Mountain hunt with wolves, Ulv, and dragon hatchlings
    - **Warband of Yagluth**: Plains warband with goblins, shamans, and deathsquitos
- **Progressive difficulty scaling** tied to boss progression:
  - Requires defeating previous bosses to unlock new raid types
  - Two-phase events with escalating intensity
  - Balanced spawn rates (95% chance per interval) for manageable frequency
- **Lore-accurate theming** with appropriate biomes, environments, and creature combinations

#### Enhanced Cartography Table Integration
- **Improved Better Cartography Table configuration**:
  - `config/nbusseneau.BetterCartographyTable.cfg`:
    - Enhanced map sharing functionality for group exploration
    - Public pin sharing for coordinated exploration
    - Optimized modifier key settings for seamless interaction

#### Missing Items & Drop Table Expansions
- **Added missing items to drop tables** across multiple biomes:
  - **Cross-biome loot distribution** for improved exploration rewards
  - **Low-chance rare items** from different biomes in various drop tables
  - **Enhanced boss loot tables** with additional material variety
- **Expanded chest loot tables** for better treasure hunting rewards
- **Improved creature drop configurations** for more diverse loot distribution

#### Drop Table Optimization
- **Enhanced loot variety** across all biomes:
  - Cross-biome material distribution for better crafting progression
  - Rare item chances in appropriate creature/chest drop tables
  - Balanced drop rates to maintain progression without overwhelming players

---

## Version 1.3.8 - Better Cartography & Hugo's Armory Integration

*Added enhanced map sharing functionality and improved exploration skill balance.*

#### Better Cartography Table Integration
- **Added Better Cartography Table mod** for enhanced group map sharing:
  - `config/nbusseneau.BetterCartographyTable.cfg`:
    - `Map exploration sharing mode`: Public (automatic map sharing)
    - `Pin sharing mode`: Public (custom pins shared between group members)
    - `Modifier key`: LeftShift (for interacting with shared pins)
- **Reduced exploration skill experience gain** to compensate:
  - `config/org.bepinex.plugins.exploration.cfg`:
    - `Skill Experience Gain Factor`: 0.48 → 0.35 (-27% reduction), was definitely finding exploration skill to be blown out of proportion

#### Hugo's Armory Drop Configuration Issue
- **Identified missing drop configurations** for Hugo's Armory items
- **Issue**: Hugo's Armory items are not configured in any drop tables
- **Status**: Requires drop table configuration to enable loot drops

---

## Version 1.3.7 - Monster Difficulty Balance & Spawn Optimization Update

*Balanced monster difficulty scaling and optimized creature spawn rates for improved gameplay experience.*

#### Monster Difficulty Rebalancing
- **Reduced creature size scaling** for better visual clarity:
  - `config/org.bepinex.plugins.creaturelevelcontrol.cfg`:
    - `Creature size increase per star`: 14% → 12% (-14% size reduction)
- **Optimized star spawn chances** to reduce overwhelming encounters:
  - **Star spawn rates reduced by 30%** across all world levels:
    - 1-Star: 20% → 14%
    - 2-Star: 15% → 10.5%
    - 3-Star: 10% → 7%
    - 4-Star: 3% → 2.1%
    - 5-Star: 2% → 1.4%
  - **Total starred creatures**: 50% → 35% (more manageable encounters)
- **Increased loot rewards** to compensate for fewer starred creatures:
  - `Chance for additional loot per star`: 50% → 65% (+30% better rewards)
- **Reduced creature affix spawn rates** for more balanced special effects:
  - `Aggressive effect`: 20% → 10% (-50% reduction)
  - `Curious effect`: 5% → 2% (-60% reduction - reduces mining harassment)
  - `Quick effect`: 10% → 7% (-30% reduction)
  - `Regenerating effect`: 10% → 7% (-30% reduction)
  - Other affixes unchanged (Splitting: 5%, Armored: 1%)
- **Increased elemental infusion variety**:
  - `Fire infusion`: 7% → 9% (+29% increase)
  - `Frost infusion`: 7% → 9% (+29% increase)
  - `Poison infusion`: 4% → 6% (+50% increase)
  - `Lightning infusion`: 3% → 5% (+67% increase)
- **Enhanced boss loot rewards**:
  - `Chance for additional loot per star for bosses`: 60% → 70% (+17% increase)

#### EpicLoot Item Drop Optimization
- **Improved item-to-materials ratio** for better gear acquisition:
  - `config/randyknapp.mods.epicloot.cfg`:
    - `Items To Materials Drop Ratio`: 0.8 → 0.6 (-25% materials, +25% items)

#### Creature Sector System Rebalancing
- **Adjusted creature sector progression** for extended biome exploration:
  - `config/org.bepinex.plugins.creaturelevelcontrol.cfg`:
    - `Kills required for bonus levels`: 10, 35, 100 → 50, 150, 300 (5x more generous)
    - `Sector reset timer`: 30 minutes → 45 minutes (50% longer recovery)
- **Benefits**: Takes 5x longer for areas to become difficult, but areas recover to normal difficulty relatively quickly. Perfect balance for extended exploration without permanent difficulty spikes.

#### Swamp Biome Spawn Optimization
- **Reduced swamp creature spawn density by 50%** to address overcrowding:
  - `config/spawn_that.simple.cfg`:
    - `Blob`: All spawn multipliers reduced to 0.5x
    - `BlobElite`: All spawn multipliers reduced to 0.5x
    - `Draugr`: All spawn multipliers reduced to 0.5x
    - `Draugr_Ranged`: All spawn multipliers reduced to 0.5x
    - `Draugr_Elite`: All spawn multipliers reduced to 0.5x
    - `Leech`: All spawn multipliers reduced to 0.5x
    - `Surtling`: All spawn multipliers reduced to 0.5x
    - `Wraith`: All spawn multipliers reduced to 0.5x
    - `Abomination`: All spawn multipliers reduced to 0.5x

**Impact**: More balanced combat encounters with fewer but more rewarding starred creatures. Swamp biome is now less overwhelming while maintaining challenge. Same total loot rewards but concentrated in fewer, more meaningful encounters.

---

## Version 1.3.5 - Skill Tweaks, Gameplay & Progression Update

*Major update combining workbench alignment, skill progression tuning, wool spawn improvements, fishing enhancements, and custom seasonal music.*

#### Workbench Alignment
- Set Wizard Table (`$piece_wizardtable_TW`) as the crafting and repair station for:
  - `StaffVulkarion_TW` (Vulkarion's Rage)
  - `StaffStorm_TW` (Stormcaller)
  - `StaffSkrymir_TW` (Skrymir's Chill)
  - `StaffMistlands_TW` (Tempest Staff)
  - `StaffBlackforest_TW` (Evergrowth Staff)
  - `BMR_WoodenStaff` (Wood Staff)
  - `HelmetPointyHat` (Pointy Hat)
  - `BMR_SorcerersHat` (Shadowleaf Vanguard Hat)
  - `BMR_SorcerersTrousers` (Shadowleaf Vanguard Trousers)
  - `BMR_SorcerersTunic` (Shadowleaf Vanguard Tunic)
  - `ScholarFireStaff`
- Standardized recipe file placement:
  - Staff-related recipes under `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/StaffBurst/`
  - Vanilla/armor recipes under `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaItems/`
- Moved glazing recipes to the Cauldron (`$piece_cauldron`):
  - `HoneyGlazedMeat`
  - `HoneyGlazedDeer`

#### EpicMMO System - Experience Rate Adjustment
- **Increased global experience gain rate** for smoother progression:
  - `config/WackyMole.EpicMMOSystem.cfg`:
    - `RateExp`: 1.15 → 1.18 (+2.6% XP gain)
- Maintains balanced progression while reducing grind in mid-late game biomes

#### Smoothbrain Skills - Death Experience Loss Removal
- **Removed death experience loss** from utility skills to reduce frustration:
  - `config/org.bepinex.plugins.tenacity.cfg`:
    - `Skill loss`: 6 → 0 (no XP loss on death)
  - `config/org.bepinex.plugins.packhorse.cfg`:
    - `Skill loss`: 3 → 0 (no XP loss on death)
  - `config/org.bepinex.plugins.farming.cfg`:
    - `Skill Experience Loss`: 1 → 0 (no XP loss on death)
- **Adjusted Tenacity skill balance**:
  - `config/org.bepinex.plugins.tenacity.cfg`:
    - `Skill gain factor`: 0.5 → 0.3 (slower XP gain)
    - `Skill effect factor`: 0.7 → 1.2 (stronger effect)
- Reduces frustration from losing utility skill progress while maintaining balanced progression

#### Fishing Skill Progression Tuning
- **Fishing skill XP rewards increased** to better match effort and success:
  - `config/kam1goroshi.BetterFishing.cfg`:
    - `Hook_Exp_Multiplier`: 3.0 → 4.0 (more XP while reeling a hooked fish)
    - `Steps_For_Catch`: 5 → 12 (much larger XP bonus on a successful catch)
    - `Bonus_Per_Fish_Level`: 0.6 → 0.8 (higher bonus for star-level fish)
- No change to empty-reel XP; empty reels remain the low baseline
- Seasonal bonuses remain intact (e.g., Fall `Fishing` raise multiplier via `shudnal.Seasons`)

#### Increased Wool Spawn Rates
- **Increased Sheep_TW spawn rates by 30-50%** for better wool availability:
  - SpawnMaxMultiplier: 1 → 1.5 (50% increase in max spawned sheep)
  - GroupSizeMaxMultiplier: 1.5 → 2 (33% increase in group size)
  - SpawnFrequencyMultiplier: 1.5 → 2 (33% increase in spawn frequency)
- Sheep_TW drops WoolScraps_TW, providing more crafting materials for Therzie.Wizardry items

---

## Version 1.3.4 - Custom Seasonal Music

#### Seasons Mod - Custom Music
- **Added custom music tracks for all four seasons - Currently not working, still trying to debug and figure it out**:
  - **Spring**: 16MB track with 0.9 volume, 4.0s fade-in, non-looping
  - **Summer**: 2.8MB track with 1.0 volume, 3.0s fade-in, non-looping with resume
  - **Fall**: 12MB track with 1.0 volume, 5.0s fade-in, looping
  - **Winter**: 1.1MB track with 0.8 volume, 6.0s fade-in, looping

**Configuration Details**:
- All tracks are enabled with ambient music settings
- Each season has unique volume levels and fade-in times
- Spring and Summer tracks are non-looping for variety
- Fall and Winter tracks loop continuously for atmospheric effect
- Summer track includes resume functionality for seamless transitions

---

## Session 2025-08-18_13-23-39 - 2025-08-20

*Configuration changes that affect gameplay - automatically generated from tracked changes.*

### Summary
- **Modified configurations**: 6
- **New configurations**: 0
- **Removed configurations**: 0

### Configuration Changes by Mod

#### RelicHeim Configuration

**Configuration Changes** in `_RelicHeimFiles\Drop,Spawn_That\drop_that.character_drop.Bosses.cfg`:
  - Changed: Bonemass.3.SetDropOnePerPlayer from False to True
  - Changed: BossAsmodeus_TW.0.SetDropOnePerPlayer from False to True
  - Changed: BossGorr_TW.1.SetDropOnePerPlayer from False to True
  - Changed: BossGorr_TW.2.SetDropOnePerPlayer from False to True
  - Changed: BossStormHerald_TW.3.SetDropOnePerPlayer from False to True

**Configuration Changes** in `_RelicHeimFiles\Drop,Spawn_That\drop_that.character_drop.GoldTrophy.cfg`:
  - Changed: Bonemass.59.SetDropOnePerPlayer from False to True
  - Changed: BossAsmodeus_TW.59.SetDropOnePerPlayer from False to True
  - Changed: BossSvalt_TW.59.SetDropOnePerPlayer from False to True
  - Changed: BossVrykolathas_TW.59.SetDropOnePerPlayer from False to True
  - Changed: Dragon.59.SetDropOnePerPlayer from False to True

**Configuration Changes** in `_RelicHeimFiles\Drop,Spawn_That\drop_that.character_drop.Wizardry.cfg`:
  - Changed: CorruptedDvergerMage_TW.0.ChanceToDrop from 50 to 100

**Configuration Changes** in `_RelicHeimFiles\Drop,Spawn_That\drop_that.drop_table.Chests.cfg`:
  - Removed: TreasureChest_swamp.SetDropChance (was 100)
  - Removed: TreasureChest_swamp.SetDropMax (was 4)
  - Removed: TreasureChest_swamp.SetDropMin (was 2)
  - Removed: TreasureChest_swamp.SetDropOnlyOnce (was True)

#### org

**Configuration Changes** in `org.bepinex.plugins.creaturelevelcontrol.cfg`:
  - Changed: 3 - Loot.Chance for additional loot per star for bosses from 60 to 50
  - Changed: 3 - Loot.Chance for additional loot per star for creatures from 50 to 100
  - Changed: 3 - Loot.Drop multiplier for passive creatures (like Seagulls and Crows) from 2 to 1
  - Changed: 4 - Bosses.Boss size increase per star (percentage) from 7 to 5

#### randyknapp

**Configuration Changes** in `randyknapp.mods.epicloot.cfg`:
  - Changed: Balance.Items To Materials Drop Ratio from 0.8 to 0


---

**Note**: This changelog focuses on configuration changes that affect gameplay. 
Patch file additions, database files, and other non-configuration changes are not included.

*Generated on 2025-08-20 19:18:28 from config snapshots*
*Initial snapshot: 2025-08-18T14:40:52.508697*
*Current snapshot: 2025-08-18T13:23:39.293727*
