# Dogeheim Modpack Changelog

## Version 1.3.4 - Custom Seasonal Music

*Added custom seasonal music tracks with unique configurations for each season.*

### New Features

#### Seasons Mod - Custom Music
- **Added custom music tracks for all four seasons**:
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
