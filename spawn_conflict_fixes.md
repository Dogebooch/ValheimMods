# Spawn Title Conflict Resolution Report

## Overview
This document summarizes the overlapping spawn configurations found between the main `spawn_that.world_spawners_advanced.cfg` file and the RelicHeim files in `_RelicHeimFiles/Drop,Spawn_That/`, along with the fixes applied.

## Conflicts Found and Fixed

### 1. Troll Spawn Conflicts

**Original Conflict:**
- **Main file**: `[WorldSpawner.30]` - "Troll Day" (daytime spawn)
- **RelicHeim zVanilla**: `[WorldSpawner.30]` - "Troll Night" (nighttime spawn)
- **RelicHeim zBase**: `[WorldSpawner.32001]` - "Troll Night" (different configuration)

**Fixes Applied:**
- Changed RelicHeim zVanilla `[WorldSpawner.30]` to `[WorldSpawner.32030]` with name "RelicHeim Troll Day"
- Updated RelicHeim zBase `[WorldSpawner.32001]` name to "RelicHeim Troll Night"
- Updated main file `[WorldSpawner.30]` name to "Custom Troll Day"

### 2. Abomination Spawn Conflicts

**Original Conflict:**
- **Main file**: `[WorldSpawner.52]` - "Abomination" (custom configuration)
- **RelicHeim zVanilla**: `[WorldSpawner.52]` - "Abomination" (different configuration)

**Fixes Applied:**
- Changed RelicHeim zVanilla `[WorldSpawner.52]` to `[WorldSpawner.32052]` with name "RelicHeim Abomination"
- Updated main file `[WorldSpawner.52]` name to "Custom Abomination"

### 3. Skeleton Spawn Conflicts

**Original Conflict:**
- **Main file**: `[WorldSpawner.32]` - Disabled vanilla swamp skeleton spawner
- **RelicHeim zVanilla**: `[WorldSpawner.32]` - "Skeleton_Poison" spawner

**Fixes Applied:**
- Changed RelicHeim zVanilla `[WorldSpawner.32]` to `[WorldSpawner.32032]` with name "RelicHeim Swamp Skeleton"
- Updated main file skeleton spawn names to "Custom SwampSkeletonDay" and "Custom SwampSkeletonNight"

## Files Modified

1. `Valheim/profiles/Dogeheim_Player/BepInEx/config/spawn_that.world_spawners_advanced.cfg`
   - Updated spawn names to include "Custom" prefix for clarity

2. `Valheim/profiles/Dogeheim_Player/BepInEx/config/_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zVanilla.cfg`
   - Changed conflicting spawn IDs to 32030, 32032, and 32052
   - Updated spawn names to include "RelicHeim" prefix

3. `Valheim/profiles/Dogeheim_Player/BepInEx/config/_RelicHeimFiles/Drop,Spawn_That/spawn_that.world_spawners.zBase.cfg`
   - Updated spawn name to include "RelicHeim" prefix

## Result

All spawn title conflicts have been resolved by:
- Using unique spawn IDs (32030, 32032, 32052) for RelicHeim configurations
- Adding descriptive prefixes ("Custom" and "RelicHeim") to distinguish between different spawn configurations
- Maintaining all original spawn functionality while eliminating conflicts

## Recommendations

1. **Future Configuration**: When adding new spawn configurations, always check for existing spawn IDs to avoid conflicts
2. **Naming Convention**: Use descriptive prefixes to distinguish between different mod configurations
3. **Documentation**: Keep track of spawn ID ranges used by different mods to prevent future conflicts

## Testing

After applying these changes, test the following:
1. Troll spawns in Black Forest (both day and night)
2. Abomination spawns in Swamp
3. Skeleton spawns in Swamp
4. Verify that all spawn configurations work as intended without conflicts
