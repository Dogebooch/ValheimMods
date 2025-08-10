# Valheim Modpack Change Log

**This file tracks major gameplay and configuration changes for the RelicHeim/JewelHeim overhaul.**

## World & Combat
- Monster HP: 120% -> 400%

## Loot & Economy

## Skills & Progression
- Raised EpicMMO Max Level to 120
- Turned off non-combat XP
- Lower EpicMMO attribute reset cost to 5 coins per point
- XP loss on death : 25%-50% -> 5-15%
- World Level start times : x days -> 9999 and changed "Second Factor" to BossesKilled (makes world level progression from boss killing, not in game days)

## Crafting & Recipes


**Meadows**
    - Lowered the global SpawnFrequencyMultiplier to 0.85
    - Pruned Mushroom world spawns: Set longer intervals and lower chances
    - Removed Tempest Neck Spawn
    - Extended POI RespawnTime Values: Standard site cooldown 1200, elite 1500
    - Standardized guarded resource nodes: 1200s interval with 15-20% spawn chance
**Black Forest**
    - Blackforest Greydwarf daytime spawns capped at 3
    - Decreased daytime Blackforest Greydwarf daytime spawns to 12%
    - Troll respawn -> from 600 to 900 for both day and night
    - Greydwarf nest spawn ticks : increased to 25s
    - Decreased Elites in Underground Ruins by replacing final wave with regular Greydwarfs
    - Trimmed overlapping Black Forest POI's by removing GuardTower1 and RootsTower1 entries from Blackforest Pack2 configs
**Swamp**
    - Cut skeleton and poison skeleton spawn chances to 14%
    - Abomination intervals increased to 2400s
    - Bone pile respawn to 25s
    - Draugr pile respawn to 25s
    - Decreased spawn quantities of SwampTower1 to 13, SwampGrave1 to 16, SwampHouse1 to 13
    - Reduced Elite listings in SwampHouse creature sets
    - Replaced one BlobElite with a regular Blob inside Sunken Crypt halls
    - Reduced Draugr_Ranged spawn chance to 35% during Bonemass fight
**Mountains**
    - Mushroom Mountain now checking every 750s
    - Avalanche Drake checks every 1500s
    - StoneForst1, StoneHall1, StoneTavern1, StoneTower1, StoneTower2 - Reduced spawn quantity to six
    - elite and rare weights in mountains creature lists decreased
    - extended Wild Lightning Wolf's spawn - increased to 1200s
**Plains**
    - Verified that the Royal Lox event mod spawns a magenta, level‑6 Royal Lox whenever a five‑star lox dies, confirming the configuration works as intended
    - Rebalanced roaming Plains mobs by reducing spawn chance for skeletons and goblin brutes, and slowing lox spawns to a 1200 s interval at 4% chance
    - Lengthened cooldowns and lowered chances for Seeker, SeekerBrood, Tick, and Charred night spawns (3600 s at 4%) to ease late‑game Plains pressure
    - Increased Mushroom Plains spawn interval to 750 s and softened POI spawns by reducing StoneTower1 goblin brute chance to 6% and adding a 900 s respawn to StoneHenge5 goblin mage
**Mistlands**
    - Restored default spawn timing across most creatures while slowing GoblinMage_TW, CorruptedDvergerMage_TW, and SummonedSeeker_TW checks to ease overlapping roamer pulls
    - Stretched Mistlands exploration pacing by lengthening Mushroom spawn intervals, trimming Seeker/Weaver Queen chances, and spacing giant_brain ore nodes
    - Reduced Mistlands point-of-interest density and elite surge potential to create more breathing room between fights
    - Calibrated Mistlands creature lists and raid waves by trimming elite/rare weights and slowing Gjall, Tick, and Brood spawn intervals
    - Logged the adjustments in the modpack change log for future tracking
**Deep North**
    - Documented the new target POI density to guide Deep North spawn balancing
    - Reduced the Mushroom Deep North POI’s frequency and pushed spawns deeper from center for lower map noise
    - Made apex flyers rarer, higher-altitude “weather moments” by slowing Frost Dragon and Frost Wyrm intervals and lowering their chances
    - Added atmospheric patrol life via small Arctic Wolf packs and a rare Jotunn Scout to hint at late-game threats
**Ashlands**
    - Reduced the Mushroom Ashlands world-spawner’s spawn chance to 18%, spacing out mushroom spawns for a slightly lower density in the Ashlands biome
**More World Traders**
    - Reduced the number of world-generation attempts for the Plains Tavern trader POI from four to three, aligning its spawn rate with the desired configuration
    - Updated both Black Forest blacksmith locations so each now spawns only three traders instead of four
    - Lowered spawn quantities to three for the Mountains Blacksmith, Mistlands Camp, Ocean Tavern, and Plains Camp trader POIs, ensuring consistent trader density across all More World Traders locations