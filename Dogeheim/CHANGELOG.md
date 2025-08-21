# Dogeheim Modpack Changelog

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
