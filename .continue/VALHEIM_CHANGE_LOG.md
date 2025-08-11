# Valheim Configuration Change Log

## 🌍 World & Combat Balance

### Monster Health & Combat
- **Monster HP**: Increased from 120% → **400%**
- **Stamina Tuning** for 4× Time To Kill (EpicMMO cap 120):
  - **Base Pool**: +20% baseline, +30% from WL-7 onward
  - **Regeneration**: ×1.35 out of combat, ×1.20 in combat
  - **Action Costs**:
    - Attacks: **−20%**
    - Block/Parry: **−15%**
    - Dodge/Roll: **−10%**
    - Sprint: **−10%**
- **Durability**: Global durability doubled (×2 baseline)

## 💰 Loot & Economy

### Mushroom Monsters (Drop That)
- **Swamp**: ThistleCap_MP drop chance: 15% → **20%**
- **Plains**: Flax drop chance: 50% → **40%**
- **Ashlands**: SurtlingCore drop chance: 50% → **35%**

## ⚔️ Skills & Progression

### EpicMMO System
- **Max Level**: Raised to **120**
- **Non-combat XP**: Turned off
- **Attribute Reset Cost**: Lowered to **5 coins per point**
- **XP Loss on Death**: Reduced from 25%–50% → **5%–15%**

### World Level Progression
- **Start Times**: Changed from x days → **9999**
- **Second Factor**: Changed to **BossesKilled** (world level progression from boss kills only)

### Farming
- **Grow Speed Factor**: Changed from 3 → **2** (slightly longer growth cycle for slightly harder food)

## 🍳 Crafting & Recipes

## 🏞️ Biome-Specific Changes

### Meadows
- **Global SpawnFrequencyMultiplier**: Lowered to **1.0**
- **Mushroom World Spawns**: 
  - Interval increased to **900s**
  - Chance reduced to **18%**
- **TempestNeck Spawn**: Removed
- **POI RespawnTime**:
  - Standard: **1200s**
  - Elite: **1500s**
- **Guarded Resource Nodes**: Standardized to 1200s interval, 15–20% chance

### Black Forest
- **Greydwarf Daytime Cap**: **3**
- **Greydwarf Daytime Spawn Chance**: **12%**
- **Troll Respawn Interval**: 600s → **900s** (day & night)
- **Greydwarf Nest Spawn Ticks**: 20s → **25s**
- **Underground Ruins**: Removed final wave elites → replaced with regular Greydwarfs
- **Pack2 Configs**: Removed GuardTower1 and RootsTower1

### Swamp
- **Skeleton & Poison Skeleton Spawn Chance**: **14%**
- **Abomination Interval**: **2400s**
- **Bone Pile Respawn**: **25s**
- **Draugr Pile Respawn**: **25s**
- **POI Spawn Quantities**:
  - SwampTower1: **13**
  - SwampGrave1: **16**
  - SwampHouse1: **13**
- **Elites**: Reduced in SwampHouse sets
- **Sunken Crypt**: Replaced one BlobElite with Blob inside halls
- **Bonemass Fight**: Draugr_Ranged spawn chance reduced to **35%**

### Mountains
- **Mushroom Mountain Interval**: **750s**
- **Avalanche Drake Interval**: **1500s**
- **Stone POIs** (StoneForst1, StoneHall1, StoneTavern1, StoneTower1, StoneTower2): Reduced to **6 spawns each**
- **Elite/Rare Weights**: Reduced in mountain creature lists
- **Wild Lightning Wolf Interval**: **1200s**

### Plains
- **Royal Lox Event**: Verified 5★ lox → magenta L6 Royal Lox works as intended
- **Spawn Chances Reduced**:
  - Skeletons: **−25%**
  - Goblin Brutes: **−20%**
- **Lox Spawn**: **1200s @ 4% chance**
- **Night Spawns** (Seeker, SeekerBrood, Tick, Charred): **3600s @ 4% chance**
- **Mushroom Plains**: **750s interval**
- **StoneTower1**: Goblin brute chance = **6%**
- **StoneHenge5**: Goblin mage respawn = **900s**

### Mistlands
- **Mage Intervals** (GoblinMage_TW, CorruptedDvergerMage_TW, SummonedSeeker_TW): Increased to **1500–1800s**
- **Mushroom Spawn Intervals**: Lengthened to **900s**
- **Seeker/Weaver Queen Chance**: Reduced by **~20%**
- **Giant Brain Ore Node Spacing**: Increased by **~15%**
- **Elite/Rare Weights**: Reduced in creature lists
- **Gjall, Tick, Brood Intervals**: Increased by **~25%**

### Deep North
- **Mushroom Deep North**:
  - Interval: 600s → **750s**
  - Chance: 22.5% → **18%**
- **Frost Dragon**:
  - Interval: **1200s**
  - Chance: 7.5% → **5%**
- **Frost Wyrm**:
  - Interval: **1200s**
  - Chance: 7.5% → **5%**
- **Arctic Wolf Packs**: Added 2–3 wolves, **90% chance every 600s**
- **Jotunn Scout**: Added rare spawn, **5% chance every 1800s**

### Ashlands
- **Mushroom Ashlands Chance**: 25% → **18%**

## 🏪 More World Traders

### Trader POI Adjustments
- **Plains Tavern**: Attempts reduced from 4 → **3**
- **Black Forest** (Blacksmith1 & Blacksmith2): Traders reduced from 4 → **3**
- **Mountains Blacksmith, Mistlands Camp, Ocean Tavern, Plains Camp**: Traders reduced from 4 → **3**

---

*Last Updated: Configuration changes for enhanced gameplay balance and progression*