# Valheim Mod Configurations Reference

This document consolidates all the important mod configuration information from the Valheim_Testing project, organized by mod category for easy reference.

## Table of Contents

1. [Drop That Configuration](#drop-that-configuration)
2. [EpicLoot Configuration](#epicloot-configuration)
3. [Creature Level & Loot Control](#creature-level--loot-control)
4. [EpicMMO System](#epicmmo-system)
5. [RelicHeim Content](#relicheim-content)
6. [Smoothbrain Mods](#smoothbrain-mods)
7. [Other Important Mods](#other-important-mods)

---

## Drop That Configuration

**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/drop_that.character_drop.cfg`

### Key Features
- Controls all mob and boss loot drops
- Configures drop rates, amounts, and conditions
- Integrates with Spawn That for conditional drops

### Notable Configurations

#### Leech Matron Drops
```cfg
[Leech.1]
PrefabName = Ooze
SetAmountMin = 2
SetAmountMax = 4
SetChanceToDrop = 1
SetDropOnePerPlayer = false
SetScaleByLevel = false

[Leech.2]
PrefabName = BloodPearl
SetAmountMin = 1
SetAmountMax = 2
SetChanceToDrop = 0.25
SetDropOnePerPlayer = false
SetScaleByLevel = false

[Leech.3]
PrefabName = ReagentRare
SetAmountMin = 1
SetAmountMax = 1
SetChanceToDrop = 0.05
SetDropOnePerPlayer = true
SetScaleByLevel = false
```

#### Boss Drops (Dragon Example)
```cfg
[Dragon.1]
PrefabName = FrostScale
SetAmountMin = 1
SetAmountMax = 3
SetChanceToDrop = 1
SetDropOnePerPlayer = true
SetScaleByLevel = true

[Dragon.2]
PrefabName = Silver
SetAmountMin = 10
SetAmountMax = 20
SetChanceToDrop = 0.3
SetDropOnePerPlayer = true
SetScaleByLevel = true

[Dragon.3]
PrefabName = LegendaryWeaponSchematic
SetAmountMin = 1
SetAmountMax = 1
SetChanceToDrop = 0.05
SetDropOnePerPlayer = true
SetScaleByLevel = true
```

---

## EpicLoot Configuration

**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/randyknapp.mods.epicloot.cfg`

### Key Settings

#### Balance Settings
```cfg
# Item Drop Limits - Controls when items can drop
Item Drop Limits = PlayerMustKnowRecipe

# Gated Bounty Mode - Controls bounty availability
Gated Bounty Mode = BossKillUnlocksNextBiomeBounties

# Boss Trophy Drop Mode - Controls trophy distribution
Boss Trophy Drop Mode = OnePerPlayerNearBoss
Boss Trophy Drop Player Range = 100

# Adventure Mode
Adventure Mode Enabled = true
```

#### Ability Settings
```cfg
Ability Hotkey 1 = h
Ability Hotkey 2 = g
Ability Hotkey 3 = j
Ability Bar Anchor = LowerLeft
Ability Bar Position = {"x":230.0,"y":93.0}
```

### Boss Loot Tables

**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/EpicLoot/patches/RelicHeimPatches/zLootables_BossDrops_RelicHeim.json`

#### Example Boss Configuration (Eikthyr)
```json
{
  "Path": "$.LootTables[?(@.Object == 'Eikthyr')].LeveledLoot",
  "Action": "Overwrite",
  "Value": [
    {
      "Level": 1,
      "Drops": [ [1, 0], [2, 60], [3, 30], [4, 10] ],
      "Loot": [
        { "Item": "Tier1Everything", "Weight": 1, "Rarity": [ 90, 10, 0, 0, 0 ] }
      ]
    },
    {
      "Level": 6,
      "Drops": [ [1, 0], [2, 60], [3, 30], [4, 10] ],
      "Loot": [
        { "Item": "Eikthyr.1", "Weight": 1, "Rarity": [ 10, 75, 10, 5, 0 ] }
      ]
    }
  ]
}
```

---

## Creature Level & Loot Control

**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.creaturelevelcontrol.cfg`

### Key Settings

#### General Configuration
```cfg
# Configuration Lock
Lock Configuration = On
Use creature configuration yaml = On
Use item configuration yaml = On

# Multiplayer Scaling
HP increase per player in multiplayer (percentage) = 40
DMG increase per player in multiplayer (percentage) = 4
Minimum player count for multiplayer scaling = 1
Maximum player count for multiplayer scaling = 10
Multiplayer scaling per player range (0 is unlimited) = 0
```

#### Creature Difficulty
```cfg
# Difficulty Settings
Difficulty = Very_hard
Second factor = Distance
Creatures can spawn with special effects = On
Creatures can spawn with elemental infusions = On

# Visual Indicators
Visual indicators for level = On
Visual indicator for special effects = Text
Add the infusion to the creatures name = On
```

#### Creature Stats
```cfg
# Health and Damage Scaling
Base health for creatures (percentage) = 120
Health gained per star for creatures (percentage) = 50
Base damage for creatures (percentage) = 120
Damage gained per star for creatures (percentage) = 35

# Creature Size
Creature size increase per star (percentage) = 11
Increase creature size even in dungeons = Off

# Respawn Times
Time until creatures in dungeons respawn in minutes = 300
Time until creatures in camps respawn in minutes = 300
```

---

## EpicMMO System

**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/WackyMole.EpicMMOSystem.cfg`

### Key Settings

#### Level System
```cfg
# Level Configuration
MaxLevel = 120
PriceResetPoints = 55
FreePointForLevel = 2
StartFreePoint = 3
LevelExperience = 300
Add LevelExperience on each level = true
MultiplyNextLevelExperience = 1.048

# Experience Settings
ExpForLvlMonster = 0.25
RateExp = 1
GroupExp = 0.7
Group EXP Range = 70
Player EXP Range = 70

# Death Penalty
MinLossExp = 0.25
MaxLossExp = 0.5
LossExp = true

# Bonus Points
BonusLevelPoints = 5:2,10:2,15:2,20:3,25:2,30:2,35:2,40:3,45:2,50:2,55:2,60:3,65:2,70:2,75:2,80:4,85:5,90:5,95:5,100:5,105:5,110:5,115:5,120:5
```

#### Attribute Scaling
```cfg
# Attribute Costs
StrengthCost = 1
AgilityCost = 1
IntelligenceCost = 1
VitalityCost = 1
WisdomCost = 1
DexterityCost = 1

# Attribute Caps
StrengthCap = 100
AgilityCap = 100
IntelligenceCap = 100
VitalityCap = 100
WisdomCap = 100
DexterityCap = 100
```

---

## RelicHeim Content

### Legendary Items
**File:** `Valheim/BepInEx/plugins/RelicHeim/Legendaries_SetsLegendary_RelicHeim.json`

### Mythic Items  
**File:** `Valheim/BepInEx/plugins/RelicHeim/Legendaries_SetsMythic_RelicHeim.json`

### Enchantments
**File:** `Valheim/BepInEx/plugins/RelicHeim/Enchantments_RelicHeim.json`

---

## Smoothbrain Mods

### Smart Skills
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.smartskills.cfg`

### Building
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.building.cfg`

### Cooking
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.cooking.cfg`

### Farming
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.farming.cfg`

### Mining
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.mining.cfg`

### Lumberjacking
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.lumberjacking.cfg`

### Foraging
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.foraging.cfg`

### Exploration
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.exploration.cfg`

### Blacksmithing
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.blacksmithing.cfg`

### Ranching
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.ranching.cfg`

### Groups
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.groups.cfg`

### Passive Powers
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.passivepowers.cfg`

### Backpacks
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.backpacks.cfg`

### Sailing
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.sailing.cfg`

### Sailing Speed
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.sailingspeed.cfg`

### Tenacity
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.tenacity.cfg`

### Pack Horse
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.packhorse.cfg`

### Target Portal
**File:** `Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.targetportal.cfg`

---

## Other Important Mods

### Azumatt Mods
- **AzuExtendedPlayerInventory:** `Azumatt.AzuExtendedPlayerInventory.cfg`
- **AzuCraftyBoxes:** `Azumatt.AzuCraftyBoxes.cfg`
- **AzuClock:** `Azumatt.AzuClock.cfg`
- **AzuWorkbenchTweaks:** `Azumatt.AzuWorkbenchTweaks.cfg`
- **AzuMouseTweaks:** `Azumatt.MouseTweaks.cfg`
- **AzuPetPantry:** `Azumatt.PetPantry.cfg`
- **AzuTrueInstantLootDrop:** `Azumatt.TrueInstantLootDrop.cfg`

### Therzie Mods
- **Wizardry:** `Therzie.Wizardry.cfg` (211KB, 6095 lines)
- **Warfare:** `Therzie.Warfare.cfg` (238KB, 7558 lines)
- **WarfareFireAndIce:** `Therzie.WarfareFireAndIce.cfg` (281KB, 8452 lines)
- **Armory:** `Therzie.Armory.cfg` (162KB, 4506 lines)
- **Monstrum:** `Therzie.Monstrum.cfg` (65KB, 2372 lines)
- **MonstrumDeepNorth:** `Therzie.MonstrumDeepNorth.cfg` (98KB, 3433 lines)

### Content Mods
- **SouthsilArmor:** `southsil.SouthsilArmor.cfg` (526KB, 17301 lines)
- **MagicRevamp:** `blacks7ar.MagicRevamp.cfg` (364KB, 12627 lines)
- **FineWoodFurnitures:** `blacks7ar.FineWoodFurnitures.cfg` (93KB, 2988 lines)
- **FineWoodBuildPieces:** `blacks7ar.FineWoodBuildPieces.cfg` (66KB, 2068 lines)
- **CookingAdditions:** `blacks7ar.CookingAdditions.cfg` (61KB, 2264 lines)
- **BiomeLords:** `Taeguk.BiomeLords.cfg` (184KB, 7114 lines)

### World Generation Mods
- **Warpalicious Packs:** Multiple biome packs for world generation
- **Seasons:** `shudnal.Seasons.cfg`
- **TradersExtended:** `shudnal.TradersExtended.cfg`

### Utility Mods
- **VNEI:** `com.maxsch.valheim.vnei.cfg`
- **PlanBuild:** `marcopogo.PlanBuild.cfg`
- **SpeedyPaths:** `nex.SpeedyPaths.cfg`
- **AdventureBackpacks:** `vapok.mods.adventurebackpacks.cfg`
- **QuickStackStore:** `goldenrevolver.quick_stack_store.cfg`

---

## Configuration Notes

### Key Balance Points
1. **Level 120 Progression:** EpicMMO configured for extended progression
2. **400% HP Boost:** Creature Level Control configured for challenging combat
3. **Boss Gating:** World level progression tied to boss kills
4. **Loot Balance:** 8:1 materials to items ratio maintained
5. **Skill Scaling:** Smart Skills system for balanced progression

### Important Files for Modding
1. `drop_that.character_drop.cfg` - Primary loot configuration
2. `org.bepinex.plugins.creaturelevelcontrol.cfg` - Monster scaling
3. `WackyMole.EpicMMOSystem.cfg` - Player progression
4. `randyknapp.mods.epicloot.cfg` - Loot system
5. `zLootables_BossDrops_RelicHeim.json` - Boss loot tables

### Configuration Philosophy
- **Progression Gating:** Content unlocked through boss kills
- **Balanced Scaling:** Monsters scale with distance and player count
- **Extended Endgame:** Level 120 cap with meaningful progression
- **Cooperative Play:** Multiplayer-friendly loot and scaling systems
- **Modular Design:** Each mod handles specific aspects of gameplay
