# RelicHeim Configuration Changes Report

Generated on: 2025-08-18 13:37:02

This report shows **only the changes** made to configuration files compared to the base RelicHeim installation.
Files that are identical to the backup or have no backup file are not shown.

For each modified file, you'll see:
- **Key Changes**: Specific configuration values that changed (old → new)
- **Full Diff**: Complete diff showing all line-by-line changes

## Summary


- **Total Changed Files**: 251
- **Modified**: 34 
- **Errors**: 0
- **Info Items**: 4

## Detailed Changes

### Creature Config

*Files in this category with changes from RelicHeim backup:*

#### CreatureConfig_Bosses.yml

**Status**: Modified

**Summary**: +18, ~9 changes

**Key Changes**:

**Total changes**: 27 (showing top 8)

• **attack speed**: `1.2` → `1.1` (-0.1)
• **damage**: `[1, 1.1, 1.12, 1.14, 1.16, 1.2]` → `[1.2, 1.3, 1.4, 1.5, 1.6, 1.7]`
• **health**: `1` → `1.2` (+0.2)
• **health per star**: `0.02` → `0.1` (+0.08)
• **movement speed**: `1.1` → `1.2` (+0.1)
• **size**: `2` *(new setting)*
• **AvalancheDrake**: `` *(new setting)*
• **Elementalist**: `35` → `40` (+5)
• ... and 19 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| Elementalist | 35 | 40 | +5 |
| Fire | 0.25 | 0.1 | -0.15 |
| Frost | 0.75 | 1 | +0.25 |
| armored | 0 | 100 | +100 |
| attack speed | 1.2 | 1.1 | -0.1 |
| health | 1 | 1.2 | +0.2 |
| health per star | 0.02 | 0.1 | +0.08 |
| movement speed | 1.1 | 1.2 | +0.1 |

**Full Diff**:

```diff
--- backup/CreatureConfig_Bosses.yml+++ current/CreatureConfig_Bosses.yml@@ -43,9 +43,10 @@     Blunt: 0.75
     Bows: 0.5
   affix:
-    Enraged: 80
-    Summoner: 10
-    Mending: 10
+    Enraged: 70
+    Summoner: 10
+    Mending: 10
+    WebSnare: 10
     other: 0
   affix power:
     Mending: 0.2
@@ -64,6 +65,24 @@     other: 0
   affix power:
     Mending: 0.1
+
+AvalancheDrake:
+  size: 1.6
+  infusion:
+    Spirit: 1
+  health: 1.1
+  health per star: 0.1
+  attack speed: 1.2
+  movement speed: 1.2
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    RockSummoner: 10
+    other: 0
+  affix power:
+    RockSummoner: 0.1
 
 GoblinKing:
   health: 1.1
@@ -101,9 +120,10 @@     Frost: 0.75
     Fire: 0.25
   affix:
-    Enraged: 80
-    Summoner: 10
-    Mending: 10
+    Enraged: 70
+    Summoner: 10
+    Mending: 10
+    WebSnare: 10
     other: 0
   affix power:
     Mending: 0.1
@@ -120,6 +140,60 @@     Elementalist: 40
     Summoner: 10
     Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+TempestSerpent:
+  size: 2.5
+  health: 1.15
+  health per star: 0.1
+  attack speed: 1.3
+  movement speed: 1.2
+  damage: [1.4, 1.5, 1.6, 1.7, 1.8, 2.0]
+  infusion:
+    lightning: 100
+  effect:
+    armored: 100
+  affix:
+    Enraged: 60
+    Elementalist: 30
+    Summoner: 10
+    other: 0
+
+MushroomBossSwamp_MP:
+  health: 1.1
+  health per star: 0.1
+  attack speed: 1.2
+  movement speed: 1.3
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  damage taken:
+    Bows: 0.5
+    Fire: 0.75
+    Frost: 0.75
+  affix:
+    Enraged: 60
+    Summoner: 20
+    Mending: 20
+    other: 0
+  affix power:
+    Mending: 0.1
+
+MushroomBossDN_MP:
+  health: 1.2
+  health per star: 0.15
+  attack speed: 1.2
+  movement speed: 1.3
+  damage: [1.4, 1.5, 1.6, 1.7, 1.8, 2.0]
+  damage taken:
+    Bows: 0.5
+    Fire: 0.75
+    Frost: 0.75
+    Spirit: 0.75
+  affix:
+    Enraged: 60
+    Elementalist: 20
+    Summoner: 20
     other: 0
   affix power:
     Mending: 0.1
@@ -327,4 +401,141 @@   affix:
     other: 0
   affix power:
-    Mending: 0.1+    Mending: 0.1
+
+FrostDragon:
+  stars: [0, 15, 50, 25, 10]
+  health: 1
+  health per star: 0.02
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.8]
+  damage taken:
+    Fire: 0.25
+    Bows: 0.5
+  infusion:
+    frost: 100
+
+StoneGolem:
+  stars: [0, 15, 50, 25, 10]
+  damage: [1.15, 1.2, 1.25, 1.3, 1.35, 1.4]
+  damage taken:
+    Fire: 0.1
+  effect:
+    armored: 100
+    other: 0
+
+# Roaming Bosses
+TempestNeck:
+  size: 3
+  health: 1.05
+  health per star: 0.05
+  attack speed: 1.1
+  movement speed: 1.1
+  damage: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+TollTroll:
+  size: 1.3
+  health: 1.1
+  health per star: 0.1
+  attack speed: 1.1
+  movement speed: 1.1
+  damage: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+LeechMatron:
+  size: 4
+  health: 1.1
+  health per star: 0.1
+  attack speed: 1.1
+  movement speed: 1
+  damage: [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+RoyalLox:
+  size: 1.6
+  health: 1.2
+  health per star: 0.08
+  attack speed: 1.1
+  movement speed: 1.1
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+WeaverQueen:
+  size: 1.5
+  health: 1.1
+  health per star: 0.05
+  attack speed: 1.1
+  movement speed: 1.1
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+MagmaGolem:
+  size: 2
+  health: 1.2
+  health per star: 0.1
+  attack speed: 1
+  movement speed: 1
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  damage taken:
+    Fire: 0.1
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1
+
+FrostWyrm:
+  size: 2
+  health: 1.2
+  health per star: 0.1
+  attack speed: 1.1
+  movement speed: 1.2
+  damage: [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
+  infusion:
+    Frost: 1
+  affix:
+    Enraged: 40
+    Elementalist: 40
+    Summoner: 10
+    Mending: 10
+    other: 0
+  affix power:
+    Mending: 0.1

```

#### CreatureConfig_Creatures.yml

**Status**: Modified

**Summary**: +4 changes

**Key Changes**:

**Total changes**: 4 (showing top 4)

• **world level**: `` *(new setting)*
• **LeechMatron**: `` *(new setting)*
• **attacks**: `` *(new setting)*
• **charge**: `` *(new setting)*

**Full Diff**:

```diff
--- backup/CreatureConfig_Creatures.yml+++ current/CreatureConfig_Creatures.yml@@ -86,6 +86,12 @@  Ashlands:
   health: 15
   health per star: 3
+# New swamp elite
+LeechMatron:
+  health: 10
+  health per star: 5
+  damage: 2
+  damage per star: 1
 #Mountains
 Ulv:
   health: 2.2
@@ -244,6 +250,12 @@   count: 5
  effect power:
   Regenerating: 0.5
+ world level:
+  health: 1.2
+  damage: 1.2
+ attacks:
+  charge:
+   damage: 1.5
  tamed:
   damage: 0.6
   damage per star: 0.1

```

### Custom Raids

*Files in this category with changes from RelicHeim backup:*

#### custom_raids.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **EventSystem.EventTriggerChance**: `40` → `20` (-20)
• **EventSystem.EventCheckInterval**: `60` → `90` (+30)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| EventSystem.EventCheckInterval | 60 | 90 | +30 |
| EventSystem.EventTriggerChance | 40 | 20 | -20 |

**Full Diff**:

```diff
--- backup/custom_raids.cfg+++ current/custom_raids.cfg@@ -56,13 +56,13 @@ ## When the interval has passed, all raids are checked for valid conditions and a random valid one is selected. Chance is then rolled for if it should start.
 # Setting type: Single
 # Default value: 46
-EventCheckInterval = 60
+EventCheckInterval = 90
 
 ## Chance of raid, per check interval. 100 is 100%.
 ## Note: Not used if UseIndividualRaidChecks is enabled, each raid will have their own chance in that case.
 # Setting type: Single
 # Default value: 20
-EventTriggerChance = 40
+EventTriggerChance = 20
 
 [General]
 

```

### Drop That

*Files in this category with changes from RelicHeim backup:*

#### drop_that.cfg

**Status**: Modified

**Summary**: ~1 changes

**Key Changes**:

**Total changes**: 1 (showing top 1)

• **Performance.AlwaysAutoStack**: `false` → `true`

**Full Diff**:

```diff
--- backup/drop_that.cfg+++ current/drop_that.cfg@@ -85,7 +85,7 @@ ## Eg. 35 coin stack, instead of 35 individual 1 coin drops.
 # Setting type: Boolean
 # Default value: false
-AlwaysAutoStack = false
+AlwaysAutoStack = true
 
 ## When greater than 0, will limit the maximum number of items dropped at a time. This is intended for guarding against multipliers.
 ## Eg. if limit is 100, and attempting to drop 200 coins, only 100 will be dropped.

```

### Enchantment System

*Files in this category with changes from RelicHeim backup:*

#### kg.ValheimEnchantmentSystem.cfg

**Status**: Modified

**Summary**: No changes detected

**Full Diff**:

```diff
--- backup/kg.ValheimEnchantmentSystem.cfg+++ current/kg.ValheimEnchantmentSystem.cfg@@ -1,4 +1,4 @@-## Settings file was created by plugin Valheim Enchantment System v1.7.3
+## Settings file was created by plugin Valheim Enchantment System v1.7.4
 ## Plugin GUID: kg.ValheimEnchantmentSystem
 
 [Notifications]

```

#### ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found.

### EpicLoot

*Files in this category with changes from RelicHeim backup:*

#### randyknapp.mods.epicloot.cfg

**Status**: Modified

**Summary**: No changes detected

**Full Diff**:

```diff
--- backup/randyknapp.mods.epicloot.cfg+++ current/randyknapp.mods.epicloot.cfg@@ -1,4 +1,4 @@-## Settings file was created by plugin Epic Loot v0.10.6
+## Settings file was created by plugin Epic Loot v0.11.4
 ## Plugin GUID: randyknapp.mods.epicloot
 
 [Abilities]
@@ -137,9 +137,6 @@ 
 [Config Sync]
 
-## [Server Only] The configuration is locked and may not be changed by clients once it has been synced from the server. Only valid for server config, will have no effect on clients.
-# Setting type: Boolean
-# Default value: true
 Lock Config = true
 
 [Crafting UI]

```

### EpicMMO

*Files in this category with changes from RelicHeim backup:*

#### WackyMole.EpicMMOSystem.cfg

**Status**: Modified

**Summary**: ~25 changes

**Key Changes**:

**Total changes**: 25 (showing top 8)

• **1.LevelSystem Dexterity---.StaminaAttack**: `0.3` → `0.2` (-0.1)
• **1.LevelSystem Dexterity---.StaminaReduction**: `0.3` → `0.1` (-0.2)
• **1.LevelSystem Endurance------.AddStamina**: `1` → `1.8` (+0.8)
• **1.LevelSystem Endurance------.StaminaReg**: `0.5` → `0.35` (-0.15)
• **1.LevelSystem Strength-----.StaminaBlock**: `0.3` → `0.15` (-0.15)
• **1.LevelSystem Vigour------.AddHp**: `1` → `2.3` (+1.3)
• **1.LevelSystem-----------.BonusLevelPoints**: `5:2,10:2,15:2,20:3,25:2,30:2,35:2,40:3,45:2,50:2,55:2,60:3,65:2,70:2,75:2,80:4,85:5,90:5` → `5:4,10:4,15:5,20:6,25:4,30:5,35:4,40:7,45:5,50:6,55:5,60:8,65:5,70:6,75:5,80:9,85:7,90:7,95:7,100:9,105:8,110:8,115:8,120:12`
• **1.LevelSystem-----------.FreePointForLevel**: `2` → `4` (+2)
• ... and 17 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 1.LevelSystem Dexterity---.StaminaAttack | 0.3 | 0.2 | -0.1 |
| 1.LevelSystem Dexterity---.StaminaReduction | 0.3 | 0.1 | -0.2 |
| 1.LevelSystem Endurance------.AddStamina | 1 | 1.8 | +0.8 |
| 1.LevelSystem Endurance------.StaminaReg | 0.5 | 0.35 | -0.15 |
| 1.LevelSystem Strength-----.StaminaBlock | 0.3 | 0.15 | -0.15 |
| 1.LevelSystem Vigour------.AddHp | 1 | 2.3 | +1.3 |
| 1.LevelSystem-----------.FreePointForLevel | 2 | 4 | +2 |
| 1.LevelSystem-----------.GroupExp | 0.7 | 0.9 | +0.2 |
| 1.LevelSystem-----------.MaxLevel | 90 | 120 | +30 |
| 1.LevelSystem-----------.MaxLossExp | 0.5 | 0.04 | -0.46 |
| 1.LevelSystem-----------.MinLossExp | 0.25 | 0.01 | -0.24 |
| 1.LevelSystem-----------.MultiplyNextLevelExperience | 1.043 | 1.048 | +0.005 |
| 1.LevelSystem-----------.PriceResetPoints | 55 | 5 | -50 |
| 1.LevelSystem-----------.RateExp | 1 | 1.15 | +0.15 |
| 1.LevelSystem-----------.maxValueDexterity | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueEndurance | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueIntelligence | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueSpecializing | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueStrength | 50 | 100 | +50 |
| 1.LevelSystem-----------.maxValueVigour | 50 | 100 | +50 |
| 2.Creature level control.Low_damage_config | 0 | 3 | +3 |
| 5.Optional perk---------.AddDefaultHealth | 0 | 25 | +25 |

**Full Diff**:

```diff
--- backup/WackyMole.EpicMMOSystem.cfg+++ current/WackyMole.EpicMMOSystem.cfg@@ -20,17 +20,17 @@ ## Maximum level. Максимальный уровень [Synced with Server]
 # Setting type: Int32
 # Default value: 100
-MaxLevel = 90
+MaxLevel = 120
 
 ## Reset price per point. Цена сброса за один поинт [Synced with Server]
 # Setting type: Int32
 # Default value: 3
-PriceResetPoints = 55
+PriceResetPoints = 5
 
 ## Free points per level. Свободных поинтов за один уровень [Synced with Server]
 # Setting type: Int32
 # Default value: 5
-FreePointForLevel = 2
+FreePointForLevel = 4
 
 ## Additional free points start. Дополнительных свободных поинтов [Synced with Server]
 # Setting type: Int32
@@ -50,7 +50,7 @@ ## Experience multiplier for the next level - Should never go below 1.00. Умножитель опыта для следующего уровня [Synced with Server]
 # Setting type: Single
 # Default value: 1.05
-MultiplyNextLevelExperience = 1.043
+MultiplyNextLevelExperience = 1.048
 
 ## Extra experience (from the sum of the basic experience) for the level of the monster. Доп опыт (из суммы основного опыта) за уровень монстра [Synced with Server]
 # Setting type: Single
@@ -60,22 +60,22 @@ ## Experience multiplier. Множитель опыта [Synced with Server]
 # Setting type: Single
 # Default value: 1
-RateExp = 1
+RateExp = 1.15
 
 ## Experience multiplier that the other players in the group get. Множитель опыта который получают остальные игроки в группе [Synced with Server]
 # Setting type: Single
 # Default value: 0.7
-GroupExp = 0.7
+GroupExp = 0.9
 
 ## Minimum Loss Exp if player death, default 5% loss [Synced with Server]
 # Setting type: Single
 # Default value: 0.05
-MinLossExp = 0.25
+MinLossExp = 0.01
 
 ## Maximum Loss Exp if player death, default 25% loss [Synced with Server]
 # Setting type: Single
 # Default value: 0.25
-MaxLossExp = 0.5
+MaxLossExp = 0.04
 
 ## Enabled exp loss [Synced with Server]
 # Setting type: Boolean
@@ -85,7 +85,7 @@ ## Added bonus point for level. Example(level:points): 5:10,15:20 add all 30 points  [Synced with Server]
 # Setting type: String
 # Default value: 5:5,10:5
-BonusLevelPoints = 5:2,10:2,15:2,20:3,25:2,30:2,35:2,40:3,45:2,50:2,55:2,60:3,65:2,70:2,75:2,80:4,85:5,90:5
+BonusLevelPoints = 5:4,10:4,15:5,20:6,25:4,30:5,35:4,40:7,45:5,50:6,55:5,60:8,65:5,70:6,75:5,80:9,85:7,90:7,95:7,100:9,105:8,110:8,115:8,120:12
 
 ## The range at which people in a group (Group MOD ONLY) get XP, relative to player who killed mob - only works if the killer gets xp. - Default 70f, a large number like 999999999999f, will probably cover map [Synced with Server]
 # Setting type: Single
@@ -120,32 +120,32 @@ ## Maximum number of points you can put into Strength [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueStrength = 50
+maxValueStrength = 100
 
 ## Maximum number of points you can put into Dexterity [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueDexterity = 50
+maxValueDexterity = 100
 
 ## Maximum number of points you can put into Intelleigence [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueIntelligence = 50
+maxValueIntelligence = 100
 
 ## Maximum number of points you can put into Endurance [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueEndurance = 50
+maxValueEndurance = 100
 
 ## Maximum number of points you can put into Vigour [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueVigour = 50
+maxValueVigour = 100
 
 ## Maximum number of points you can put into Specializing [Synced with Server]
 # Setting type: Int32
 # Default value: 200
-maxValueSpecializing = 50
+maxValueSpecializing = 100
 
 ## You get normal xp amount, times this number for taming a creature [Synced with Server]
 # Setting type: Int32
@@ -167,24 +167,24 @@ ## Reduces attack stamina consumption.  [Synced with Server]
 # Setting type: Single
 # Default value: 0.1
-StaminaAttack = 0.3
+StaminaAttack = 0.2
 
 ## Decrease stamina consumption for running, jumping for one point. [Synced with Server]
 # Setting type: Single
 # Default value: 0.15
-StaminaReduction = 0.3
+StaminaReduction = 0.1
 
 [1.LevelSystem Endurance------]
 
 ## One Point Stamina Increase. [Synced with Server]
 # Setting type: Single
 # Default value: 1
-AddStamina = 1
+AddStamina = 1.8
 
 ## Increase stamina regeneration per point. [Synced with Server]
 # Setting type: Single
 # Default value: 0.4
-StaminaReg = 0.5
+StaminaReg = 0.35
 
 ## Increase in physical protection per point. [Synced with Server]
 # Setting type: Single
@@ -250,7 +250,7 @@ ## Decrease stamina consumption per unit per point. [Synced with Server]
 # Setting type: Single
 # Default value: 0.2
-StaminaBlock = 0.3
+StaminaBlock = 0.15
 
 ## Amount of Critical Dmg done per point [Synced with Server]
 # Setting type: Single
@@ -262,7 +262,7 @@ ## One Point Health Increase.  [Synced with Server]
 # Setting type: Single
 # Default value: 1
-AddHp = 1
+AddHp = 2.3
 
 ## Increase health regeneration per point. [Synced with Server]
 # Setting type: Single
@@ -324,7 +324,7 @@ ## Extra paramater to low damage config - for reference(float)(playerLevel + lowDamageConfig) / monsterLevel; when player is below lvl [Synced with Server]
 # Setting type: Int32
 # Default value: 0
-Low_damage_config = 0
+Low_damage_config = 3
 
 ## Character level - MinLevelRange is less than the level of the monster, then you will receive reduced experience. Уровень персонажа - MinLevelRange меньше уровня монстра, то вы будете получать урезанный опыт [Synced with Server]
 # Setting type: Int32
@@ -388,7 +388,7 @@ ## Add health by default [Synced with Server]
 # Setting type: Single
 # Default value: 0
-AddDefaultHealth = 0
+AddDefaultHealth = 25
 
 ## Add weight by default [Synced with Server]
 # Setting type: Single
@@ -502,7 +502,7 @@ ## Disables all non combat xp. [Synced with Server]
 # Setting type: Boolean
 # Default value: false
-1.Disable All NonCombat XP = true
+1.Disable All NonCombat XP = false
 
 ## Disables Piece XP. You only get xp for once per building, then you have to change to another piece. It still could be abused. [Synced with Server]
 # Setting type: Boolean
@@ -569,7 +569,7 @@ ## Use @, to display the how long the player has been alive in days. Blank for nothing. [Synced with Server]
 # Setting type: String
 # Default value:  <color=red>(@ Days Alive)</color>
-Display Days Alive = 
+Display Days Alive = @
 
 ## Enable PVP XP, victor gets XP of fallen player. [Synced with Server]
 # Setting type: Boolean

```

### Item Config

*Files in this category with changes from RelicHeim backup:*

#### ItemConfig_Base.yml

**Status**: Modified

**Summary**: -39 changes

**Key Changes**:

**Total changes**: 39 (showing top 8)

• **Blackwood**: `` *(removed)*
• **BorealPineWood_TW**: `` *(removed)*
• **BorealWood_TW**: `` *(removed)*
• **Coins**: `` *(removed)*
• **CryptKey**: `` *(removed)*
• **DragonEgg**: `` *(removed)*
• **ElderBark**: `` *(removed)*
• **EnchantedWoodBlackForest_TW**: `` *(removed)*
• ... and 31 more changes

**Full Diff**:

```diff
--- backup/ItemConfig_Base.yml+++ current/ItemConfig_Base.yml@@ -1,4 +1,24 @@ groups:
+  CustomFood:
+  - HoneyGlazedDeer
+  - HoneyGlazedMeat
+  - HoneyGlazedNeck
+  - HoneyGlazedLox
+  - HoneyGlazedFish
+  - HoneyGlazedWolf
+  - JellyGlazedHare
+  - JellyGlazedSeeker
+  - CookedEntrails
+  - ElkJerky
+  - LoxJerky_JH
+  - SeekerJerky_JH
+  - FishJerky_JH
+  - FishStew_JH
+  - NeckJerky_JH
+  - SerpentJerky_JH
+  - FishNLoxSkewer
+  - FishMeatSkewer
+  - DandelionTea_JH
   MeadBase:
   - BarleyWineBase
   - MeadBaseTamer
@@ -25,26 +45,14 @@   - MeadBaseLingeringStaminaMedium_TW
   - MeadBaseEitrBlackForest_TW
   - MeadBaseEitrMountain_TW
-  CustomFood:
-  - HoneyGlazedDeer
-  - HoneyGlazedMeat
-  - HoneyGlazedNeck
-  - HoneyGlazedLox
-  - HoneyGlazedFish
-  - HoneyGlazedWolf
-  - JellyGlazedHare
-  - JellyGlazedSeeker
-  - CookedEntrails
-  - ElkJerky
-  - LoxJerky_JH
-  - SeekerJerky_JH
-  - FishJerky_JH
-  - FishStew_JH
-  - NeckJerky_JH
-  - SerpentJerky_JH
-  - FishNLoxSkewer
-  - FishMeatSkewer
-  - DandelionTea_JH
+  MetalsDeepNorth:
+  - RagnoriteBar_TW
+  - TyraniumBar_TW
+  - ThoradusBar_TW
+  - LokvyrBar_TW
+  - RagnoriteOre_TW
+  - TyraniumOre_TW
+  - LokvyrOre_TW
   ReduceWeight:
   - Stone
   - BlackMarble
@@ -61,122 +69,3 @@   - ArcaneScroll_SpeedBuff_TW
   - ArcaneScroll_JumpBuff_TW
   - ArcaneScroll_SlowfallBuff_TW
-  MetalsDeepNorth:
-  - RagnoriteBar_TW
-  - TyraniumBar_TW
-  - ThoradusBar_TW
-  - LokvyrBar_TW
-  - RagnoriteOre_TW
-  - TyraniumOre_TW
-  - LokvyrOre_TW
-#
-all:
-    floating: yes
-    pickup: yes
-# stuff floats in water; everything is pickable
-NeckTailGrilled:
-    floating: no
-SeekerAspic:
-    floating: no
-HoneyGlazedNeck:
-    floating: no
-# NeckTailGrilled doesnt float till its fixed due to floating in air very high.
-Stackable:
-    stack: 200
-WizardryScrolls:
-    stack: 10
-DragonEgg:
-    stack: 3
-    weight: 100
-SurtrDrakeEgg_TW:
-    teleportable: yes
-    weight: 100
-CryptKey:
-    stack: 10
-MeadBase:
-    stack: 100
-mmo_mead_minor:
-    stack: 100
-mmo_mead_med:
-    stack: 100
-mmo_mead_greater:
-    stack: 100
-Food:
-    stack: 200
-    loss: no
-CustomFood:
-    stack: 200
-    loss: no
-Food Backpack:
-    loss: no
-# food stacks to 200 and doesn't be removed from inventory on death
-metal:
-    teleportable: no
-    stack: 100
-    Weight: 10
-ore:
-    teleportable: no
-    stack: 100
-    Weight: 10
-MetalsDeepNorth:
-    teleportable: no
-    stack: 200
-    Weight: 10
-# ores and metals are not teleportable, stack to 100 and metals weight only 10
-ReduceWeight:
-    stack: 200
-    Weight: 1
-# stones stack to 100 and weight only 1
-trophy:
-    stack: 100
-    Weight: 2
-boss trophy:
-    stack: 100
-    Weight: 2
-# trophys stack up to 100 and weight only 2
-Coins:
-    stack: 9999
-valuable:
-    stack: 100
-    weight: 0.05
-# make coins, valuables lighter
-Wood:
-  stack: 200
-  weight: 1
-FineWood:
-    stack: 200
-    weight: 1
-RoundLog:
-    stack: 200
-    weight: 1
-ElderBark:
-    stack: 200
-    weight: 1
-YggdrasilWood:
-    stack: 200
-    weight: 1
-Blackwood:
-    stack: 200
-    weight: 1
-BorealWood_TW:
-    stack: 200
-    weight: 1
-BorealPineWood_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodBlackForest_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodSwamp_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodMountain_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodPlains_TW:
-    stack: 200
-    weight: 1
-EnchantedWoodMistlands_TW:
-    stack: 200
-    weight: 1
-# All Wood types stack to 100 and weight half
```

### Other

*Files in this category with changes from RelicHeim backup:*

#### wackysDatabase/Items\_RelicHeimWDB2.0\Food\Item_SerpentMeatCooked.yml

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found.

#### wackysDatabase/Items\_RelicHeimWDB2.0\Food\Item_SerpentStew.yml

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found.

#### wackysDatabase/Items\_RelicHeimWDB2.0\Food\Feasts\Item_FeastAshlands.yml

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found.

#### wackysDatabase/Items\_RelicHeimWDB2.0\Food\Feasts\Item_FeastMistlands.yml

**Status**: Modified

**Summary**: ~2 changes

**Note**: No backup file mapping found.

#### EpicLoot/localizations\English.json

**Status**: Modified

**Summary**: ~6 changes

**Note**: No backup file mapping found.

#### EpicLoot/patches\RelicHeimPatches\AdventureData_Bounties_RelicHeim.json

**Status**: Modified

**Summary**: +20, -2 changes

**Note**: No backup file mapping found.

#### EpicLoot/patches\RelicHeimPatches\AdventureData_TherzieWizardry_RelicHeim.json

**Status**: Modified

**Summary**: ~1 changes

**Note**: No backup file mapping found.

#### EpicLoot/patches\RelicHeimPatches\MagicEffects_RelicHeim.json

**Status**: Modified

**Summary**: +1, -13 changes

**Note**: No backup file mapping found.

#### EpicLoot/patches\RelicHeimPatches\MaterialConversion_RelicHeim.json

**Status**: Modified

**Summary**: No changes detected

**Note**: No backup file mapping found.

#### EpicLoot/patches\RelicHeimPatches\zLootables_BossDrops_RelicHeim.json

**Status**: Modified

**Summary**: No changes detected

**Note**: No backup file mapping found.

#### EpicLoot/patches\RelicHeimPatches\zLootables_CreatureDrops_RelicHeim.json

**Status**: Modified

**Summary**: +2, -1, ~3 changes

**Note**: No backup file mapping found.

#### EpicLoot/patches\RelicHeimPatches\zLootables_TreasureLoot_RelicHeim.json

**Status**: Modified

**Summary**: +1, ~3 changes

**Note**: No backup file mapping found.

### Plant Everything

*Files in this category with changes from RelicHeim backup:*

#### advize.PlantEverything.cfg

**Status**: Modified

**Summary**: ~12 changes

**Key Changes**:

**Total changes**: 12 (showing top 8)

• **Berries.BlueberryRespawnTime**: `120` → `220` (+100)
• **Berries.CloudberryRespawnTime**: `120` → `300` (+180)
• **Berries.RaspberryRespawnTime**: `120` → `160` (+40)
• **Debris.PickableBranchRespawnTime**: `120` → `240` (+120)
• **Debris.PickableFlintRespawnTime**: `120` → `240` (+120)
• **Debris.PickableStoneRespawnTime**: `120` → `240` (+120)
• **Flowers.DandelionRespawnTime**: `120` → `100` (-20)
• **Flowers.ThistleRespawnTime**: `120` → `110` (-10)
• ... and 4 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| Berries.BlueberryRespawnTime | 120 | 220 | +100 |
| Berries.CloudberryRespawnTime | 120 | 300 | +180 |
| Berries.RaspberryRespawnTime | 120 | 160 | +40 |
| Debris.PickableBranchRespawnTime | 120 | 240 | +120 |
| Debris.PickableFlintRespawnTime | 120 | 240 | +120 |
| Debris.PickableStoneRespawnTime | 120 | 240 | +120 |
| Flowers.DandelionRespawnTime | 120 | 100 | -20 |
| Flowers.ThistleRespawnTime | 120 | 110 | -10 |
| Mushrooms.BlueMushroomRespawnTime | 120 | 110 | -10 |
| Mushrooms.MushroomRespawnTime | 120 | 110 | -10 |
| Mushrooms.SmokepuffRespawnTime | 120 | 100 | -20 |
| Mushrooms.YellowMushroomRespawnTime | 120 | 110 | -10 |

**Full Diff**:

```diff
--- backup/advize.PlantEverything.cfg+++ current/advize.PlantEverything.cfg@@ -1,4 +1,4 @@-## Settings file was created by plugin PlantEverything v1.18.2
+## Settings file was created by plugin PlantEverything v1.19.1
 ## Plugin GUID: advize.PlantEverything
 
 [Berries]
@@ -21,17 +21,17 @@ ## Number of minutes it takes for a raspberry bush to respawn berries.
 # Setting type: Int32
 # Default value: 300
-RaspberryRespawnTime = 120
+RaspberryRespawnTime = 160
 
 ## Number of minutes it takes for a blueberry bush to respawn berries.
 # Setting type: Int32
 # Default value: 300
-BlueberryRespawnTime = 120
+BlueberryRespawnTime = 220
 
 ## Number of minutes it takes for a cloudberry bush to respawn berries.
 # Setting type: Int32
 # Default value: 300
-CloudberryRespawnTime = 120
+CloudberryRespawnTime = 300
 
 ## Number of berries a raspberry bush will spawn.
 # Setting type: Int32
@@ -220,7 +220,7 @@ ## Number of minutes it takes for a pickable branch to respawn.
 # Setting type: Int32
 # Default value: 240
-PickableBranchRespawnTime = 120
+PickableBranchRespawnTime = 240
 
 ## Amount of stone required to place stone debris. Set to 0 to disable the ability to plant this resource.
 # Setting type: Int32
@@ -235,7 +235,7 @@ ## Number of minutes it takes for a pickable Stone to respawn.
 # Setting type: Int32
 # Default value: 0
-PickableStoneRespawnTime = 120
+PickableStoneRespawnTime = 240
 
 ## Amount of flint required to place flint debris. Set to 0 to disable the ability to plant this resource.
 # Setting type: Int32
@@ -250,7 +250,7 @@ ## Number of minutes it takes for pickable flint to respawn.
 # Setting type: Int32
 # Default value: 240
-PickableFlintRespawnTime = 120
+PickableFlintRespawnTime = 240
 
 [Difficulty]
 
@@ -319,12 +319,12 @@ ## Number of minutes it takes for thistle to respawn.
 # Setting type: Int32
 # Default value: 240
-ThistleRespawnTime = 120
+ThistleRespawnTime = 110
 
 ## Number of minutes it takes for dandelion to respawn.
 # Setting type: Int32
 # Default value: 240
-DandelionRespawnTime = 120
+DandelionRespawnTime = 100
 
 ## Number of minutes it takes for fiddlehead to respawn.
 # Setting type: Int32
@@ -428,22 +428,22 @@ ## Number of minutes it takes for mushrooms to respawn.
 # Setting type: Int32
 # Default value: 240
-MushroomRespawnTime = 120
+MushroomRespawnTime = 110
 
 ## Number of minutes it takes for yellow mushrooms to respawn.
 # Setting type: Int32
 # Default value: 240
-YellowMushroomRespawnTime = 120
+YellowMushroomRespawnTime = 110
 
 ## Number of minutes it takes for blue mushrooms to respawn.
 # Setting type: Int32
 # Default value: 240
-BlueMushroomRespawnTime = 120
+BlueMushroomRespawnTime = 110
 
 ## Number of minutes it takes for smoke puffs to respawn.
 # Setting type: Int32
 # Default value: 240
-SmokepuffRespawnTime = 120
+SmokepuffRespawnTime = 100
 
 ## Number of mushrooms a pickable mushroom spawner will spawn.
 # Setting type: Int32

```

### Smoothbrain

*Files in this category with changes from RelicHeim backup:*

#### org.bepinex.plugins.tenacity.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **skill_1612888259.Skill gain factor**: `0.4` → `0.5` (+0.1)
• **skill_1612888259.Skill loss**: `10` → `6` (-4)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| skill_1612888259.Skill gain factor | 0.4 | 0.5 | +0.1 |
| skill_1612888259.Skill loss | 10 | 6 | -4 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.tenacity.cfg+++ current/org.bepinex.plugins.tenacity.cfg@@ -7,7 +7,7 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill gain factor = 0.4
+Skill gain factor = 0.5
 
 ## The power of the skill, based on the default power.
 # Setting type: Single
@@ -19,5 +19,5 @@ # Setting type: Int32
 # Default value: 5
 # Acceptable value range: From 0 to 100
-Skill loss = 10
+Skill loss = 6
 

```

#### org.bepinex.plugins.sailing.cfg

**Status**: Modified

**Summary**: +56, ~11 changes

**Key Changes**:

**Total changes**: 67 (showing top 8)

• **2 - Ship Speed.Big Cargo Ship Full Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Big Cargo Ship Half Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Big Cargo Ship Paddle Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Big Cargo Ship Speed Factor**: `1.5` *(new setting)*
• **2 - Ship Speed.Cargo Caravel Full Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Cargo Caravel Half Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Cargo Caravel Paddle Requirement**: `0` *(new setting)*
• **2 - Ship Speed.Cargo Caravel Speed Factor**: `1.5` *(new setting)*
• ... and 59 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Ship Speed.Drakkar Full Requirement | 0 | 50 | +50 |
| 2 - Ship Speed.Drakkar Half Requirement | 0 | 50 | +50 |
| 2 - Ship Speed.Drakkar Paddle Requirement | 0 | 50 | +50 |
| 2 - Ship Speed.Karve Full Requirement | 0 | 10 | +10 |
| 2 - Ship Speed.Karve Half Requirement | 0 | 10 | +10 |
| 2 - Ship Speed.Karve Paddle Requirement | 0 | 10 | +10 |
| 2 - Ship Speed.Longship Full Requirement | 0 | 30 | +30 |
| 2 - Ship Speed.Longship Half Requirement | 0 | 30 | +30 |
| 2 - Ship Speed.Longship Paddle Requirement | 0 | 30 | +30 |
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.4 | -0.1 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.sailing.cfg+++ current/org.bepinex.plugins.sailing.cfg@@ -50,19 +50,19 @@ # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Karve Paddle Requirement = 0
+Karve Paddle Requirement = 10
 
 ## Required sailing skill level to be able to sail a Karve with reduced sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Karve Half Requirement = 0
+Karve Half Requirement = 10
 
 ## Required sailing skill level to be able to sail a Karve with full sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Karve Full Requirement = 0
+Karve Full Requirement = 10
 
 ## Speed factor for Longship at skill level 100.
 # Setting type: Single
@@ -74,19 +74,19 @@ # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Longship Paddle Requirement = 0
+Longship Paddle Requirement = 30
 
 ## Required sailing skill level to be able to sail a Longship with reduced sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Longship Half Requirement = 0
+Longship Half Requirement = 30
 
 ## Required sailing skill level to be able to sail a Longship with full sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Longship Full Requirement = 0
+Longship Full Requirement = 30
 
 ## Speed factor for Drakkar at skill level 100.
 # Setting type: Single
@@ -98,19 +98,355 @@ # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Drakkar Paddle Requirement = 0
+Drakkar Paddle Requirement = 50
 
 ## Required sailing skill level to be able to sail a Drakkar with reduced sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Drakkar Half Requirement = 0
+Drakkar Half Requirement = 50
 
 ## Required sailing skill level to be able to sail a Drakkar with full sail.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Drakkar Full Requirement = 0
+Drakkar Full Requirement = 50
+
+## Speed factor for Merchant's boat at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Merchants boat Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Merchant's boat.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Merchants boat Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Merchant's boat with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Merchants boat Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Merchant's boat with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Merchants boat Full Requirement = 0
+
+## Speed factor for Cargo Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Cargo Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Cargo Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Cargo Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Cargo Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Ship Full Requirement = 0
+
+## Speed factor for Big Cargo Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Big Cargo Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Big Cargo Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Big Cargo Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Big Cargo Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Big Cargo Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Big Cargo Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Big Cargo Ship Full Requirement = 0
+
+## Speed factor for Cargo Caravel at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Cargo Caravel Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Cargo Caravel.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Caravel Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Cargo Caravel with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Caravel Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Cargo Caravel with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Cargo Caravel Full Requirement = 0
+
+## Speed factor for Huge Cargo Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Huge Cargo Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Huge Cargo Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Huge Cargo Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Huge Cargo Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Huge Cargo Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Huge Cargo Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Huge Cargo Ship Full Requirement = 0
+
+## Speed factor for Rowing canoe at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Rowing canoe Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Rowing canoe.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Rowing canoe Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Rowing canoe with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Rowing canoe Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Rowing canoe with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Rowing canoe Full Requirement = 0
+
+## Speed factor for Double rowing canoe at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Double rowing canoe Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Double rowing canoe.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Double rowing canoe Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Double rowing canoe with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Double rowing canoe Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Double rowing canoe with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Double rowing canoe Full Requirement = 0
+
+## Speed factor for Little Boat at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Little Boat Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Little Boat.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Little Boat Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Little Boat with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Little Boat Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Little Boat with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Little Boat Full Requirement = 0
+
+## Speed factor for War Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+War Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a War Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a War Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a War Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Full Requirement = 0
+
+## Speed factor for War Ship Skuldelev at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+War Ship Skuldelev Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a War Ship Skuldelev.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Skuldelev Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a War Ship Skuldelev with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Skuldelev Half Requirement = 0
+
+## Required sailing skill level to be able to sail a War Ship Skuldelev with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+War Ship Skuldelev Full Requirement = 0
+
+## Speed factor for Taurus War Ship at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Taurus War Ship Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Taurus War Ship.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Taurus War Ship Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Taurus War Ship with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Taurus War Ship Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Taurus War Ship with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Taurus War Ship Full Requirement = 0
+
+## Speed factor for Fast Ship Skuldelev at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Fast Ship Skuldelev Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Fast Ship Skuldelev.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Fast Ship Skuldelev Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Fast Ship Skuldelev with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Fast Ship Skuldelev Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Fast Ship Skuldelev with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Fast Ship Skuldelev Full Requirement = 0
+
+## Speed factor for Goblin Boat at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Goblin Boat Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Goblin Boat.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Goblin Boat Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Goblin Boat with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Goblin Boat Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Goblin Boat with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Goblin Boat Full Requirement = 0
+
+## Speed factor for Hercule Fishing boat at skill level 100.
+# Setting type: Single
+# Default value: 1.5
+# Acceptable value range: From 1 to 3
+Hercule Fishing boat Speed Factor = 1.5
+
+## Required sailing skill level to be able to paddle a Hercule Fishing boat.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Hercule Fishing boat Paddle Requirement = 0
+
+## Required sailing skill level to be able to sail a Hercule Fishing boat with reduced sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Hercule Fishing boat Half Requirement = 0
+
+## Required sailing skill level to be able to sail a Hercule Fishing boat with full sail.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Hercule Fishing boat Full Requirement = 0
 
 [3 - Other]
 
@@ -130,13 +466,13 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.4
 
 ## How much experience to lose in the sailing skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 
 ## If on, players can press a hotkey, to give their ship a nudge, if it is stuck.
 # Setting type: Toggle

```

#### org.bepinex.plugins.packhorse.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **skill_1443093080.Skill gain factor**: `0.5` → `0.7` (+0.2)
• **skill_1443093080.Skill loss**: `5` → `3` (-2)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| skill_1443093080.Skill gain factor | 0.5 | 0.7 | +0.2 |
| skill_1443093080.Skill loss | 5 | 3 | -2 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.packhorse.cfg+++ current/org.bepinex.plugins.packhorse.cfg@@ -7,7 +7,7 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill gain factor = 0.5
+Skill gain factor = 0.7
 
 ## The power of the skill, based on the default power.
 # Setting type: Single
@@ -19,5 +19,5 @@ # Setting type: Int32
 # Default value: 5
 # Acceptable value range: From 0 to 100
-Skill loss = 5
+Skill loss = 3
 

```

#### org.bepinex.plugins.foraging.cfg

**Status**: Modified

**Summary**: ~5 changes

**Key Changes**:

**Total changes**: 5 (showing top 5)

• **2 - Foraging.Minimum Level Respawn Display**: `10` → `30` (+20)
• **2 - Foraging.Multiplier for Respawn Speed**: `2` → `1.5` (-0.5)
• **2 - Foraging.Maximum Mass Picking Range**: `10` → `8` (-2)
• **3 - Other.Skill Experience Gain Factor**: `0.5` → `0.6` (+0.1)
• **3 - Other.Skill Experience Loss**: `1` → `0` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Foraging.Maximum Mass Picking Range | 10 | 8 | -2 |
| 2 - Foraging.Minimum Level Respawn Display | 10 | 30 | +20 |
| 2 - Foraging.Multiplier for Respawn Speed | 2 | 1.5 | -0.5 |
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.6 | +0.1 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.foraging.cfg+++ current/org.bepinex.plugins.foraging.cfg@@ -29,19 +29,19 @@ # Setting type: Int32
 # Default value: 30
 # Acceptable value range: From 0 to 100
-Minimum Level Respawn Display = 10
+Minimum Level Respawn Display = 30
 
 ## Mass picking radius at skill level 100 in meters.
 # Setting type: Int32
 # Default value: 10
 # Acceptable value range: From 0 to 20
-Maximum Mass Picking Range = 10
+Maximum Mass Picking Range = 8
 
 ## Multiplier for the respawn speed at skill level 100.
 # Setting type: Single
 # Default value: 2
 # Acceptable value range: From 1 to 10
-Multiplier for Respawn Speed = 2
+Multiplier for Respawn Speed = 1.5
 
 [3 - Other]
 
@@ -49,11 +49,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.6
 
 ## How much experience to lose in the foraging skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

#### org.bepinex.plugins.lumberjacking.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **2 - Other.Skill Experience Gain Factor**: `0.5` → `0.6` (+0.1)
• **2 - Other.Skill Experience Loss**: `1` → `0` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Other.Skill Experience Gain Factor | 0.5 | 0.6 | +0.1 |
| 2 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.lumberjacking.cfg+++ current/org.bepinex.plugins.lumberjacking.cfg@@ -39,11 +39,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.6
 
 ## How much experience to lose in the lumberjacking skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

#### org.bepinex.plugins.mining.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **3 - Other.Skill Experience Gain Factor**: `0.5` → `0.72` (+0.22)
• **3 - Other.Skill Experience Loss**: `1` → `0` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.72 | +0.22 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.mining.cfg+++ current/org.bepinex.plugins.mining.cfg@@ -46,11 +46,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.72
 
 ## How much experience to lose in the mining skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

#### org.bepinex.plugins.farming.cfg

**Status**: Modified

**Summary**: ~7 changes

**Key Changes**:

**Total changes**: 7 (showing top 7)

• **2 - Crops.Grow Speed Factor**: `3` → `1.6` (-1.4)
• **2 - Crops.Show Progress Level**: `10` → `25` (+15)
• **2 - Crops.Harvest Increase Interval**: `10` → `15` (+5)
• **2 - Crops.Plant Increase Interval**: `10` → `15` (+5)
• **2 - Crops.Random Rotation**: `Off` → `On`
• **3 - Other.Skill Experience Gain Factor**: `1.25` → `0.57` (-0.68)
• **3 - Other.Skill Experience Loss**: `2` → `1` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Crops.Grow Speed Factor | 3 | 1.6 | -1.4 |
| 2 - Crops.Harvest Increase Interval | 10 | 15 | +5 |
| 2 - Crops.Plant Increase Interval | 10 | 15 | +5 |
| 2 - Crops.Show Progress Level | 10 | 25 | +15 |
| 3 - Other.Skill Experience Gain Factor | 1.25 | 0.57 | -0.68 |
| 3 - Other.Skill Experience Loss | 2 | 1 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.farming.cfg+++ current/org.bepinex.plugins.farming.cfg@@ -15,7 +15,7 @@ # Setting type: Single
 # Default value: 3
 # Acceptable value range: From 1 to 10
-Grow Speed Factor = 3
+Grow Speed Factor = 1.6
 
 ## Item yield factor for crops at skill level 100.
 # Setting type: Single
@@ -27,7 +27,7 @@ # Setting type: Int32
 # Default value: 30
 # Acceptable value range: From 0 to 100
-Show Progress Level = 10
+Show Progress Level = 25
 
 ## Required skill level to ignore the required biome of planted crops. 0 is disabled.
 # Setting type: Int32
@@ -39,13 +39,13 @@ # Setting type: Int32
 # Default value: 20
 # Acceptable value range: From 0 to 100
-Plant Increase Interval = 10
+Plant Increase Interval = 15
 
 ## Level interval to increase the radius harvested at the same time. 0 is disabled.
 # Setting type: Int32
 # Default value: 20
 # Acceptable value range: From 0 to 100
-Harvest Increase Interval = 10
+Harvest Increase Interval = 15
 
 ## Reduces the stamina usage while planting and harvesting your crops. Percentage stamina reduction per level. 0 is disabled.
 # Setting type: Int32
@@ -57,7 +57,7 @@ # Setting type: Toggle
 # Default value: Off
 # Acceptable values: Off, On
-Random Rotation = Off
+Random Rotation = On
 
 [3 - Other]
 
@@ -65,13 +65,13 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 1.25
+Skill Experience Gain Factor = 0.57
 
 ## How much experience to lose in the farming skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 2
+Skill Experience Loss = 1
 
 ## Shortcut to press to toggle between the single plant mode and the mass plant mode. Please note that you have to stand still, to toggle this.
 # Setting type: KeyboardShortcut

```

#### org.bepinex.plugins.conversionsizespeed.cfg

**Status**: Modified

**Summary**: +18 changes

**Key Changes**:

**Total changes**: 18 (showing top 8)

• **Advanced cooking station.Conversion time**: `5` *(new setting)*
• **Bird House.Conversion time**: `20` *(new setting)*
• **Fish Trap.Conversion time**: `30` *(new setting)*
• **Fishing Dock.Conversion time**: `120` *(new setting)*
• **Primitive Compost.Conversion time**: `30` *(new setting)*
• **Bird House.Storage space**: `50` *(new setting)*
• **Bird House.Storage space increase per boss**: `0` *(new setting)*
• **Advanced cooking station.Fuel per product**: `1` *(new setting)*
• ... and 10 more changes

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.conversionsizespeed.cfg+++ current/org.bepinex.plugins.conversionsizespeed.cfg@@ -14,6 +14,44 @@ # Default value: LeftShift
 Fill up modifier key = LeftShift
 
+[Advanced cooking station]
+
+## Sets the maximum number of items that a Advanced cooking station can hold.
+# Setting type: Int32
+# Default value: 100
+# Acceptable value range: From 1 to 1000
+Storage space = 100
+
+## Increases the maximum number of items that a Advanced cooking station can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Sets the maximum number of fuel that a Advanced cooking station can hold.
+# Setting type: Int32
+# Default value: 100
+# Acceptable value range: From 1 to 1000
+Fuel space = 100
+
+## Increases the maximum number of fuel that a Advanced cooking station can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Fuel space increase per boss = 0
+
+## Sets how much fuel a Advanced cooking station needs per produced product.
+# Setting type: Int32
+# Default value: 1
+# Acceptable value range: From 1 to 20
+Fuel per product = 1
+
+## Time in seconds that a Advanced cooking station needs for one conversion.
+# Setting type: Int32
+# Default value: 5
+# Acceptable value range: From 1 to 1000
+Conversion time = 5
+
 [Armory]
 
 ## Sets the maximum number of items that a Armory can hold.
@@ -72,6 +110,26 @@ # Acceptable value range: From 1 to 1000
 Conversion time = 20
 
+[Bird House]
+
+## Sets the maximum number of items that a Bird House can hold.
+# Setting type: Int32
+# Default value: 50
+# Acceptable value range: From 1 to 1000
+Storage space = 50
+
+## Increases the maximum number of items that a Bird House can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Time in seconds that a Bird House needs for one conversion.
+# Setting type: Int32
+# Default value: 20
+# Acceptable value range: From 1 to 1000
+Conversion time = 20
+
 [Blast Furnace]
 
 ## Sets the maximum number of items that a Blast Furnace can hold.
@@ -205,6 +263,46 @@ # Default value: 40
 # Acceptable value range: From 1 to 1000
 Conversion time = 20
+
+[Fish Trap]
+
+## Sets the maximum number of items that a Fish Trap can hold.
+# Setting type: Int32
+# Default value: 50
+# Acceptable value range: From 1 to 1000
+Storage space = 50
+
+## Increases the maximum number of items that a Fish Trap can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Time in seconds that a Fish Trap needs for one conversion.
+# Setting type: Int32
+# Default value: 30
+# Acceptable value range: From 1 to 1000
+Conversion time = 30
+
+[Fishing Dock]
+
+## Sets the maximum number of items that a Fishing Dock can hold.
+# Setting type: Int32
+# Default value: 100
+# Acceptable value range: From 1 to 1000
+Storage space = 100
+
+## Increases the maximum number of items that a Fishing Dock can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Time in seconds that a Fishing Dock needs for one conversion.
+# Setting type: Int32
+# Default value: 120
+# Acceptable value range: From 1 to 1000
+Conversion time = 120
 
 [Hot Tub]
 
@@ -225,6 +323,26 @@ # Default value: 5000
 # Acceptable value range: From 1 to 10000
 Conversion time = 5000
+
+[Primitive Compost]
+
+## Sets the maximum number of items that a Primitive Compost can hold.
+# Setting type: Int32
+# Default value: 50
+# Acceptable value range: From 1 to 1000
+Storage space = 50
+
+## Increases the maximum number of items that a Primitive Compost can hold for each boss killed.
+# Setting type: Int32
+# Default value: 0
+# Acceptable value range: From 0 to 100
+Storage space increase per boss = 0
+
+## Time in seconds that a Primitive Compost needs for one conversion.
+# Setting type: Int32
+# Default value: 30
+# Acceptable value range: From 1 to 1000
+Conversion time = 30
 
 [Smelter]
 

```

#### org.bepinex.plugins.creaturelevelcontrol.cfg

**Status**: Modified

**Summary**: ~12 changes

**Key Changes**:

**Total changes**: 12 (showing top 8)

• **2 - Creatures.Base damage for creatures (percentage)**: `120` → `110` (-10)
• **2 - Creatures.Base health for creatures (percentage)**: `120` → `400` (+280)
• **2 - Creatures.Creature size increase per star (percentage)**: `10` → `14` (+4)
• **5 - Age of world.World level 1 start (days)**: `10` → `9999` (+9989)
• **5 - Age of world.World level 2 start (days)**: `25` → `9999` (+9974)
• **5 - Age of world.World level 3 start (days)**: `50` → `9999` (+9949)
• **5 - Age of world.World level 4 start (days)**: `100` → `9999` (+9899)
• **5 - Age of world.World level 5 start (days)**: `250` → `9999` (+9749)
• ... and 4 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Creatures.Base damage for creatures (percentage) | 120 | 110 | -10 |
| 2 - Creatures.Base health for creatures (percentage) | 120 | 400 | +280 |
| 2 - Creatures.Creature size increase per star (percentage) | 10 | 14 | +4 |
| 5 - Age of world.World level 1 start (days) | 10 | 9999 | +9989 |
| 5 - Age of world.World level 2 start (days) | 25 | 9999 | +9974 |
| 5 - Age of world.World level 3 start (days) | 50 | 9999 | +9949 |
| 5 - Age of world.World level 4 start (days) | 100 | 9999 | +9899 |
| 5 - Age of world.World level 5 start (days) | 250 | 9999 | +9749 |
| 5 - Age of world.World level 6 start (days) | 500 | 9999 | +9499 |
| 5 - Age of world.World level 7 start (days) | 600 | 9999 | +9399 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.creaturelevelcontrol.cfg+++ current/org.bepinex.plugins.creaturelevelcontrol.cfg@@ -98,7 +98,7 @@ # Setting type: DifficultySecondFactor
 # Default value: BossesKilled
 # Acceptable values: None, Age_of_world, Distance, BossesKilled
-Second factor = Distance
+Second factor = BossesKilled
 
 ## Display circles on the map for distance from spawn option.
 # Setting type: Toggle
@@ -162,7 +162,7 @@ # Setting type: Int32
 # Default value: 10
 # Acceptable value range: From 0 to 40
-Creature size increase per star (percentage) = 10
+Creature size increase per star (percentage) = 14
 
 ## If creature size will be increased in dungeons as well, where they might get stuck if they get too big.
 # Setting type: Toggle
@@ -174,7 +174,7 @@ # Setting type: Single
 # Default value: 100
 # Acceptable value range: From 1 to 500
-Base health for creatures (percentage) = 120
+Base health for creatures (percentage) = 400
 
 ## Health gained per star for creatures in percentage.
 # Setting type: Single
@@ -186,7 +186,7 @@ # Setting type: Single
 # Default value: 100
 # Acceptable value range: From 1 to 500
-Base damage for creatures (percentage) = 120
+Base damage for creatures (percentage) = 110
 
 ## Damage gained per star for creatures in percentage.
 # Setting type: Single
@@ -280,7 +280,7 @@ # Setting type: Toggle
 # Default value: Off
 # Acceptable values: Off, On
-Creatures can drop multiple trophies = Off
+Creatures can drop multiple trophies = On
 
 ## If bosses can drop multiple trophies.
 # Setting type: Toggle
@@ -341,37 +341,37 @@ ## Days needed to pass before your world gets to world level 1.
 # Setting type: Int32
 # Default value: 10
-World level 1 start (days) = 10
+World level 1 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 2.
 # Setting type: Int32
 # Default value: 25
-World level 2 start (days) = 25
+World level 2 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 3.
 # Setting type: Int32
 # Default value: 50
-World level 3 start (days) = 50
+World level 3 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 4.
 # Setting type: Int32
 # Default value: 100
-World level 4 start (days) = 100
+World level 4 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 5.
 # Setting type: Int32
 # Default value: 250
-World level 5 start (days) = 250
+World level 5 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 6.
 # Setting type: Int32
 # Default value: 400
-World level 6 start (days) = 500
+World level 6 start (days) = 9999
 
 ## Days needed to pass before your world gets to world level 7.
 # Setting type: Int32
 # Default value: 600
-World level 7 start (days) = 600
+World level 7 start (days) = 9999
 
 [5 - Custom level chances]
 

```

#### org.bepinex.plugins.blacksmithing.cfg

**Status**: Modified

**Summary**: ~9 changes

**Key Changes**:

**Total changes**: 9 (showing top 8)

• **2 - Crafting.Skill Level for Extra Upgrade Level**: `80` → `70` (-10)
• **2 - Crafting.Skill Level for Inventory Repair**: `70` → `50` (-20)
• **2 - Crafting.Base Durability Factor**: `1` → `2` (+1)
• **2 - Crafting.Durability Factor**: `2` → `4` (+2)
• **2 - Crafting.Experience Reduction Factor**: `0.5` → `0.25` (-0.25)
• **2 - Crafting.Experience Reduction Threshold**: `5` → `10` (+5)
• **2 - Crafting.First Craft Bonus**: `75` → `100` (+25)
• **3 - Other.Skill Experience Gain Factor**: `0.5` → `0.7` (+0.2)
• ... and 1 more changes

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Crafting.Base Durability Factor | 1 | 2 | +1 |
| 2 - Crafting.Durability Factor | 2 | 4 | +2 |
| 2 - Crafting.Experience Reduction Factor | 0.5 | 0.25 | -0.25 |
| 2 - Crafting.Experience Reduction Threshold | 5 | 10 | +5 |
| 2 - Crafting.First Craft Bonus | 75 | 100 | +25 |
| 2 - Crafting.Skill Level for Extra Upgrade Level | 80 | 70 | -10 |
| 2 - Crafting.Skill Level for Inventory Repair | 70 | 50 | -20 |
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.7 | +0.2 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.blacksmithing.cfg+++ current/org.bepinex.plugins.blacksmithing.cfg@@ -63,25 +63,25 @@ # Setting type: Int32
 # Default value: 70
 # Acceptable value range: From 0 to 100
-Skill Level for Inventory Repair = 70
+Skill Level for Inventory Repair = 50
 
 ## Minimum skill level for an additional upgrade level for armor and weapons. 0 means disabled.
 # Setting type: Int32
 # Default value: 80
 # Acceptable value range: From 0 to 100
-Skill Level for Extra Upgrade Level = 80
+Skill Level for Extra Upgrade Level = 70
 
 ## Factor for durability of armor and weapons at skill level 0.
 # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Base Durability Factor = 1
+Base Durability Factor = 2
 
 ## Factor for durability of armor and weapons at skill level 100.
 # Setting type: Single
 # Default value: 2
 # Acceptable value range: From 1 to 5
-Durability Factor = 2
+Durability Factor = 4
 
 ## Factor for the price of the additional upgrade.
 # Setting type: Single
@@ -93,19 +93,19 @@ # Setting type: Int32
 # Default value: 75
 # Acceptable value range: From 0 to 200
-First Craft Bonus = 75
+First Craft Bonus = 100
 
 ## After crafting an item this amount of times, crafting it will give reduced blacksmithing experience. Use 0 to disable this.
 # Setting type: Int32
 # Default value: 5
 # Acceptable value range: From 0 to 50
-Experience Reduction Threshold = 5
+Experience Reduction Threshold = 10
 
 ## Factor at which the blacksmithing experience gain is reduced, once too many of the same item have been crafted. Additive, not multiplicative. E.g. reducing the experience gained by 50% every 5 crafts means that you won't get any experience anymore after the 10th craft.
 # Setting type: Single
 # Default value: 0.5
 # Acceptable value range: From 0 to 1
-Experience Reduction Factor = 0.5
+Experience Reduction Factor = 0.25
 
 [3 - Other]
 
@@ -113,11 +113,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.7
 
 ## How much experience to lose in the blacksmithing skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

#### org.bepinex.plugins.building.cfg

**Status**: Modified

**Summary**: ~6 changes

**Key Changes**:

**Total changes**: 6 (showing top 6)

• **2 - Building.Durability Increase Level Requirement**: `30` → `25` (-5)
• **2 - Building.Free Build Level Requirement**: `50` → `100` (+50)
• **2 - Building.Maximum Support Factor**: `1.5` → `1.8` (+0.3)
• **2 - Building.Support Loss Factor**: `0.75` → `0.85` (+0.1)
• **3 - Other.Skill Experience Gain Factor**: `0.5` → `0.8` (+0.3)
• **3 - Other.Skill Experience Loss**: `1` → `0` (-1)

**Numeric Values Comparison**:

| Setting | Old Value | New Value | Difference |
|---------|-----------|-----------|------------|
| 2 - Building.Durability Increase Level Requirement | 30 | 25 | -5 |
| 2 - Building.Free Build Level Requirement | 50 | 100 | +50 |
| 2 - Building.Maximum Support Factor | 1.5 | 1.8 | +0.3 |
| 2 - Building.Support Loss Factor | 0.75 | 0.85 | +0.1 |
| 3 - Other.Skill Experience Gain Factor | 0.5 | 0.8 | +0.3 |
| 3 - Other.Skill Experience Loss | 1 | 0 | -1 |

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.building.cfg+++ current/org.bepinex.plugins.building.cfg@@ -15,13 +15,13 @@ # Setting type: Single
 # Default value: 1.5
 # Acceptable value range: From 1 to 5
-Maximum Support Factor = 1.5
+Maximum Support Factor = 1.8
 
 ## Support loss factor for vertical and horizontal building at skill level 100.
 # Setting type: Single
 # Default value: 0.75
 # Acceptable value range: From 0.01 to 1
-Support Loss Factor = 0.75
+Support Loss Factor = 0.85
 
 ## Health factor for building pieces at skill level 100.
 # Setting type: Single
@@ -33,13 +33,13 @@ # Setting type: Int32
 # Default value: 50
 # Acceptable value range: From 0 to 100
-Free Build Level Requirement = 50
+Free Build Level Requirement = 100
 
 ## Minimum required skill level to reduce the durability usage of hammers by 30%. 0 is disabled.
 # Setting type: Int32
 # Default value: 30
 # Acceptable value range: From 0 to 100
-Durability Increase Level Requirement = 30
+Durability Increase Level Requirement = 25
 
 ## Reduces the stamina usage while building. Percentage stamina reduction per level. 0 is disabled.
 # Setting type: Int32
@@ -53,11 +53,11 @@ # Setting type: Single
 # Default value: 1
 # Acceptable value range: From 0.01 to 5
-Skill Experience Gain Factor = 0.5
+Skill Experience Gain Factor = 0.8
 
 ## How much experience to lose in the building skill on death.
 # Setting type: Int32
 # Default value: 0
 # Acceptable value range: From 0 to 100
-Skill Experience Loss = 1
+Skill Experience Loss = 0
 

```

#### org.bepinex.plugins.backpacks.cfg

**Status**: Modified

**Summary**: ~2 changes

**Key Changes**:

**Total changes**: 2 (showing top 2)

• **2 - Backpack.Hide Backpack**: `Off` → `On`
• **Explorers Backpack.Crafting Station**: `Disabled` → `Workbench`

**Full Diff**:

```diff
--- backup/org.bepinex.plugins.backpacks.cfg+++ current/org.bepinex.plugins.backpacks.cfg@@ -80,7 +80,7 @@ # Setting type: Toggle
 # Default value: Off
 # Acceptable values: Off, On
-Hide Backpack = Off
+Hide Backpack = On
 
 ## If on, the backpack in your backpack slot is opened automatically, if the inventory is opened.
 # Setting type: Toggle
@@ -111,7 +111,7 @@ # Setting type: CraftingTable
 # Default value: Workbench
 # Acceptable values: Disabled, Inventory, Workbench, Cauldron, Forge, ArtisanTable, StoneCutter, MageTable, BlackForge, FoodPreparationTable, MeadKetill, Custom
-Crafting Station = Disabled
+Crafting Station = Workbench
 
 # Setting type: String
 # Default value: 

```

