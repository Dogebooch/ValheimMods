# Dogeheim Modpack Changelog

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
