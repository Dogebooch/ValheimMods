# Valheim Modpack Design Document

## 1. Core Vision

**One Sentence Summary:** Exploration‑first, **boss‑gated** Valheim with **RuneScape‑style skilling/progression** and **MMORPG‑style RNG itemization with soft class archetypes** (build‑defined, not hard‑locked), where **materials dominate routine drops** and **items are rare but meaningfully powerful**; **crafting (blacksmithing)** provides the base power ladder while **enchanting** is the primary customization, with Solo‑Leveling undertones across a \~350 to 400‑hour journey.

**Timeframe Target:** 
- **WL7 \~350h avg**
- Full journey **\~350–400h** with WL8+

---
## BIGGEST TODO
- [ ] Review every mod's configuration to understand and document gameplay impact
- [ ] Raise Max level EpicMMO to 120
- [ ] Ensure the rest of the following changes:

### **EpicMMO System (Primary RPG Progression)**
- **Max Level**: 120 (raised from 90)
- **Free Points Per Level**: 2 (reduced from default 5)
- **Start Free Points**: 3 (reduced from default 5)
- **Level Experience**: 300 XP base per level
- **Experience Multiplier**: 1.048 (raised for longer progression)
- **Add Level Experience**: Enabled (adds 300 XP per level)
- **Bonus Level Points**: +5 every 5 levels up to 120
- **Experience Rate**: 1.0x (normal)
- **Death Penalty**: 5-25% (default)
- **Reset Cost**: 3 coins per point (default)
 - **Tuning Note**: Age-based WL schedule targets ~250–300 hours baseline to WL7. With ~+50 hours for added content, expect ~300–350 hours total. Assumes ~30 minutes per in-game day; frequent sleeping can reduce real time by ~15–25%.

## 2. Core Design Pillars

### 2.1 Exploration Over Treadmill

**Goal:** POIs, routes, and biome mastery matter more than raw ARPG loot rain.

**Objectives:**
- Set POI density targets per biome and adjust mods/POI packs accordingly
- Ensure monsters per POI and loot per POI are balanced for FPS and Difficulty
- Make engagements fun but not overwhelming with too many spawns at one time
- Ensure breathing room for combat AND exploration
- Adjust Creature Spawns to match target density and reward curve

**ToDos:**
  - [ ] Set Target Densities per Biome ([poi_density.csv](./poi_density.csv))
    - [x] See how the Warpalicious mods interacts with the poi_density.csv
    - [ ] Set Meadows = 0.40 targets per Km^2
      - [ ] Adjust for Meadows Pack 1 & 2: 24 unique location types, 205 total instances
        - [ ] Balance the amount of monsters per POI (decrease to decrease the overhead), or adjust the loot so it's stronger at those areas.
      - [ ] Adjust for the Resource Nodes: ~40
      - [ ] Adjust for Creature Spawns: +7-11 from Monstrum and MushroomMonsters
        - [ ] Adjust the Creature Spawns to improve fps/overhead, adjust for +400% HP of the monsters, and change drops to compensate for the decreased spawn locations
    - [ ] Set Blackforest = 0.30 targets per Km^2
      - [ ] Adjust for Blackforest Packs 1 & 2, Forbidden Catacombs
    - [ ] Set Swamp set = 0.28 targets per Km^2
      - [ ] Adjust for Swamp Pack 1, Underground Ruins
    - [ ] Set Mountains = 0.22 targets per Km^2
      - [ ] Adjust for Mountains Pack 1
    - [ ] Set Plains = 0.32 targets per Km^2
      - [ ] Adjust for Plains Pack 1
    - [ ] Set Mistlands = 0.20 targets per Km^2
      - [ ] Adjust for Mistlands Pack 1
    - [ ] Set DeepNorth = 0.14 targets per Km^2
    - [ ] Set Ashlands = 0.16 targets per Km^2
      - [ ] Adjust for Ashlands Pack 1
    - [ ] Set Oceans = 0.06 Targets per Km^2
    - [ ] Adjust for the More_World_Traders & the Adventure_Map_Pack

### 2.2 Boss → World Level Gating

**Goal:** The world only advances after the relevant boss dies (server-wide), letting players set their own pace.

**Objectives:**
    - Enforce server-wide progression pacing via bosses

**ToDos:**
- [ ] Look for all of the mods that change boss gating/World Leveling
- [ ] Ensure all biomes scale appropriately when unlocked
- [ ] Change gating so that the WL only increases when the base bosses are killed (WL1-8)
  - [ ] Eikthyr kill -> WL2
  - [ ] Elder Kill -> WL3
  - [ ] Bonemass Kill -> WL4
  - [ ] Moder Kill -> WL5
  - [ ] Yagluth Kill -> WL6
  - [ ] The Queen -> WL7
  - [ ] Deep North Boss -> WL8
  - [ ] Ashlands Boss -> WL9

#### Boss Loot Configuration Tasks

**Boss Enchantment Materials:**
- [ ] In `Valheim/profiles/Dogeheim_Player/BepInEx/config/drop_that.character_drop.cfg`, create a `[BossName.*]` block for every boss (Eikthyr → Yagluth).
- [ ] For each block:
  - [ ] `PrefabName` → WL-appropriate enchantment material pack (e.g., `EnchantPack_T1`, `EnchantPack_T2`, … `EnchantPack_T7`).
  - [ ] `SetAmountMin/Max` → tiered quantities (e.g., T1: 5–8, T7: 20–25).
  - [ ] `SetChanceToDrop = 1`, `SetDropOnePerPlayer = true`, `SetScaleByLevel = false`.
- [ ] Add a second entry `PrefabName = BossToken` with the same guarantees (always 1).
- [ ] Gate each pair with `ConditionWorldLevelMin/Max` to match WL ranges.
- [ ] Document the configuration change in `Valheim_Content_Mods_Summary.md`.

**Curated Rare Boss Items:**
- [ ] Define curated rare items in `Valheim/profiles/Dogeheim_Player/BepInEx/config/EpicLoot/patches/RelicHeimPatches/ItemInfo_BossRare.json`:
  - [ ] Fixed baseline stats, limited affix list.
  - [ ] Separate sets per boss or WL tier.
- [ ] In `zLootables_BossDrops_RelicHeim.json`, add `BossRare_T#` loot groups for each boss level:
  - [ ] Early bosses (WL1–3): `Rarity` weights targeting ~10% total.
  - [ ] Late bosses (WL4–7): scale to ~12–15%.
- [ ] Update `drop_that.character_drop.cfg` to add a corresponding `[BossName.N]` entry that calls `BossRare_T#` so the rare roll only occurs once per kill.
- [ ] Ensure `drop_one_per_player = true` and WL gates mirror Drop That/EpicLoot.
- [ ] Remove any duplicate "always item" drops from boss tables — mats should be the default reward.

**T5 Legendary Items:**
- [ ] Define T5 legendary items (static stats) in `RelicHeim/Legendaries_SetsLegendary_RelicHeim.json` or a new file.
- [ ] In `zLootables_BossDrops_RelicHeim.json`, add a `Legendary_T5` loot group with `Rarity` ≈3%.
- [ ] Develop a BepInEx plugin (e.g., `BossLegendaryPity.cs`) under `Valheim/BepInEx/plugins/`:
  - [ ] Track per-player boss kill counts.
  - [ ] Each kill rolls 3% chance; increment counter on failure.
  - [ ] Force drop when counter ≥ streak threshold (target P50≈22, P95≤40) and reset counter.
- [ ] Hook plugin into `OnBossDeath` to inject the item if pity triggers.
- [ ] Document plugin purpose and configuration in `Valheim_Content_Mods_Summary.md`.

**Mythic (T7) Items:**
- [ ] Create Mythic item definitions in `Legendaries_SetsMythic_RelicHeim.json` with minimal affix variance.
- [ ] In `zLootables_BossDrops_RelicHeim.json`, append `Mythic_T7` loot group with `Rarity` set to ~1%.
- [ ] Extend the pity plugin (`BossLegendaryPity.cs`) or make a sibling (`BossMythicPity.cs`):
  - [ ] Activate only if `worldLevel >= 7`.
  - [ ] Base drop: 1% (early WL7), scale up to 1.5% at WL8+.
  - [ ] Track kill streaks; guarantee a mythic after threshold (e.g., 70 kills).
- [ ] Add WL7+ gating (`ConditionWorldLevelMin = 7`) in both Drop That and EpicLoot configs.

**Materials > Items Ratio Guardrails:**
- [ ] Maintain a global **~8:1 materials : items** ratio for all boss fights.
- [ ] Boss fights should **always** drop mats + token; items are a separate rare roll.
- [ ] Elites (non-boss) can drop small mat bundles + rare item chance ≤ 2%.
- [ ] Keep legendary/mythic pity plugins active only for item drops — mats remain deterministic.

### 2.3 Materials > Items

**Goal:** Creatures target **\~8:1** materials:items; chests emphasize **enchant mats + occasional items**.

**Objectives:**
      - Shift emphasis from random gear to crafting resources
      - Make Gear acquisition meaningful and rare
- Ensure enchanting materials are present, and are more abundantly dropped than items, but 10% increased from what it is currently
- Improve scaling with star levels (more enchanting materials if star level)
- **Creatures (avg per WL):** **materials : items ≈ 8:1** (acceptable 7–10:1)
- **Chests:** prioritize **enchanting materials + occasional items** over raw mats
- Target split: **Enchant mats 40–50% | Items 15–25% | Raw mats 30–40%**

**ToDos:**
- [ ] Adjust drop that configs for drop ratio target (8 mats : 1 item)
- [ ] Adjust RelicHeim patches to match drop ratio target (8 mats : 1 item)
  - [ ] Adjust DeepNorth, Ashlands and Ocean Chests (see if there are any)
- [ ] Appraise chests so that they prioritize enchanted materials and rare item drops
- [ ] Ensure balance across the chests/drops so that rare items feel meaningful and earned

#### Lucky Spike Drops (Cross-Tier Enchant Mats)

**Intent:**
- Very rare, memorable moments: a WL-ahead enchant mat drops (1 piece), creating excitement without accelerating progression.

**Rules:**
- Spikes are **single-unit** drops
- Only **next tier** (WL+1); bosses may very rarely hit **WL+2**
- Never more than **one spike per kill/chest**
- Optional **soft cap** per player (e.g., 1–2/day) to prevent streaks

**ToDos:**

**Config – Chests (EpicLoot `zLootables_*.json`):**
- [ ] In each WL chest group, add a **Spike** sub-group:
  - [ ] `EnchantPack_T{WL+1}` with `Rarity` targeting **0.2–0.5%** total chest chance
  - [ ] `SetAmountMin/Max = 1–1`
  - [ ] Keep normal WL mats dominant; this entry sits at the bottom with tiny weight
- [ ] Ensure the chest group rolls **at most one spike** (use one sub-group, not multiple entries)

**Config – Bosses (Drop That + EpicLoot):**
- [ ] Boss guaranteed mats unchanged (WL-tier)
- [ ] Add **BossSpike** roll:
  - [ ] `EnchantPack_T{WL+1}` at **~1.0%**
  - [ ] Optional **WL+2** at **0.2–0.3%** for late bosses only (WL6+)
  - [ ] `SetAmountMin/Max = 1–1`, `SetDropOnePerPlayer = true`
  - [ ] Keep in a **separate call** so spike can only occur **once per kill**

**Guardrails:**
- [ ] No spikes on **trash mobs**; elites may have **≤0.2%** WL+1 spike at WL6+ only
- [ ] Keep **pity systems** for legendaries/mythics **off** for spikes (they must stay lucky)
- [ ] Add **logging** tag `LuckySpike` to drops to audit frequency

**Optional Plugin – Soft Cap (BepInEx `LuckySpikeLimiter.cs`):**
- [ ] Track per-player spike count (rolling 24h)
- [ ] If cap reached (e.g., **2 per day**), suppress further spikes → convert to normal WL mat
- [ ] Expose config:
  - [ ] `DailyCap=2`, `BossSpikeChance=1.0%`, `BossSpikePlusTwo=0.25%`, `ChestSpikeChance=0.35%`

**Suggested Rates (start point):**
- [ ] **Chests:** 0.35% for `EnchantPack_T{WL+1}`, 1 unit
- [ ] **Bosses WL1–5:** 1.0% `T{WL+1}`, 0% `T{WL+2}`
- [ ] **Bosses WL6–8+:** 1.0% `T{WL+1}` **and** 0.25% `T{WL+2}`, both single-roll capped to **max one spike**
- [ ] **Elites WL6+:** ≤0.2% `T{WL+1}`, single unit

**Testing:**
- [ ] Simulate **1000 chests / WL** → expect **2–5** spikes total (0.2–0.5%)
- [ ] Simulate **500 boss kills / tier** → expect **~5** WL+1 spikes; WL6–8 expect **~1** WL+2 spike
- [ ] Verify **inventory impact minimal** (single units) and **time-to-first-enchant** remains ≤ 3h from WL entry

**Documentation:**
- [ ] Add a "Lucky Spike" blurb in `Valheim_Content_Mods_Summary.md` with the current rates and caps
- [ ] In your in-game wiki/codex, explain: "**Very rare** chance to find a **future-tier** gem — cherish it!"

### 2.4 Deterministic Safety Nets

**Goal:** Token & streak‑breaker systems prevent droughts while keeping jackpots rare.

**Objectives:**
- Implement Token Systems and Streak breakers for unlucky players

**ToDos:**
- [ ] Add token currency drops for bosses
  - [ ] Ensure the following - **Guaranteed:** WL‑appropriate **enchant‑mat packs** (tiered quantities) + **1 token**
- [ ] Define token thresholds for guaranteed loot tiers
- [ ] Configure traders to trade items for tokens (Will be end game loot)
- [ ] Ensure early bosses cannot be exploited for easy tokens

### 2.5 Power Without Trivialization

**Goal:** Endgame feels strong; elites and bosses remain threatening.

**Objectives:**
- Scale mob HP, damage, and mechanics to keep them threatening, but not impossible
- Prolong out engagements, to promote co-op exploration and engagements
- Maintain combat depth for all content tiers

**ToDos:**
- [ ] Tune EpicMMO point gain per level so that players are naturally encouraged to specialize in a build (e.g., melee, ranged, magic) without locking them into a single playstyle
- [ ] Enable and simplify respecs so players can easily reset and redistribute their points at any stage of progression
- [ ] Assess DPS burst potential in PvE by tuning attack speed, damage multipliers, and cooldown reduction stacking
- [ ] Assess healing potentional in PvE by tuning healing staves, consumbales, and damage mitigation of armor, tenacity and Vitality (EpicMMO)
- [ ] Introduce diminishing returns on certain stacking bonuses (crit chance, attack speed, lifesteal) to prevent runaway scaling
- [ ] Ensure that the end game is still balanced after all of these, to feel powerful but not trivial

### 2.6 Skilling System

**Goal:** Skilling is separated into three tiers: tier 1 (Gamechangers), tier 2 (Strong Utilities), tier 3 (Flavor/minor)

**Objectives:**
- **Tier 1 (Gamechangers):** run, sailing, weapon skills - level 70 by early Ashlands (Early WL-8)
- **Tier 2 (Strong Utilities):** sneak, pickaxe, mining, exploration, foraging, and blacksmithing - level 70 by deep north entry post world level 7 (Early WL-7)
- **Tier 3 (Flavor/minor):** jump, swim, farming, ranching, pack horse, tenacity, lumberjacking, building, enchantment - level 70 by end of mist lands (Late WL-6)
- Assess the Progression factor for sailing, which is going to be a little bit different given the XP per tick system
- **Tier1:** multipliers ≥ **1.0–1.1**; **Tier2:** **0.6–0.75**; **Tier3:** **0.55–0.8** (Swimming may remain higher as QoL)
- **Note:** the factors may change based on balancing

**ToDos:**
- [ ] Adjust the base Relicheim skilling levels so that it's adjusted for the new prolonged gametime: 400% XP boost
- [ ] Set the Exp Factor gain for Tier 1 skills
  - [ ] Run
  - [ ] Weapon Skills
- [ ] Set the Exp Factor Gain for Tier 2 Skills
  - [ ] Sneak
  - [ ] Pickaxe
  - [ ] Exploration
  - [ ] Foraging
- [ ] Set the Exp Factor Gain for Tier 3 Skills
  - [ ] Jump
  - [ ] Swim
  - [ ] Farming
  - [ ] Cooking
  - [ ] Ranching
  - [ ] Pack Horse
  - [ ] Tenacity
  - [ ] Lumberjacking
  - [ ] Building
  - [ ] Enchantments
- [ ] Adjust Stamina exp factor gain to take into account the prolonged enounters (400% HP boost)

---

## 3. Additional Optimization Tasks

### 3.1 Performance & Spawn Optimization

**Goals:**
- Reduce server/client overhead in late-game biomes without breaking biome identity or pacing
- Ensure all relevant items are accessible in-game (crafted or dropped) with clear acquisition paths
- Pace introduction of recipes, skills, and items to encourage long-term progression
- Consolidate and streamline crafting systems for better accessibility
- Maintain consistent configuration and balance across all mods

**ToDos:**
- [ ] Space out POI density in late biomes to reduce clustering
- [ ] Lower passive raid frequency to avoid constant interruptions
- [ ] Slow or cap routine world spawns in high-density areas
- [ ] Apply stronger global spawn throttles for peak load times
- [ ] Calibrate loot drops to account for decreased monster spawns

### 3.2 Itemization & Drop Table Management

**ToDos:**
- [ ] Identify all items not currently obtainable in-game or missing from drop tables
- [ ] Create a list of endgame or "drop-only" items (non-craftable)
- [ ] Add modded items to loot tables via Drop That configuration
- [ ] Configure drop rates so non-craftable items drop in pairs (one for me, one for Brett)

### 3.3 Recipe & Crafting Progression

**ToDos:**
- [ ] Remove or lock recipes for early-game items that should be introduced later
- [ ] Strategically reintroduce items across world levels instead of all at once
- [ ] Consolidate crafting to fewer, more versatile crafting tables
- [ ] Assign blacksmithing level requirements to item crafting
- [ ] Adjust Durability to compensate for the 400% HP boost of the monsters

### 3.4 Skills & Gating

**ToDos:**
- [ ] Pace skilling rates (integrate with AzuExp if applicable)
- [ ] Conduct a comprehensive skills audit to identify balance issues
- [ ] Add level gating to all soft skills

### 3.5 Balance & Mod Configuration

**ToDos:**
- [ ] Audit stacking effects of gear, consumables, and buffs for balance issues
- [ ] Ensure Mushroom Monsters are correctly configured with biome-appropriate drops
- [ ] Balance drops objectively with measurable rarity/ratio targets
- [ ] Ensure world level progression is boss-kill gated (not tied to in-game days)

### 3.6 Boats & Vehicles

**ToDos:**
- [ ] Ensure all boats are assigned to correct workbenches
- [ ] Stratify boats by weight vs. speed and distribute them across world levels

### Other Ideas
- Highlight rare drops and track boss killcounts for social/cosmetic rewards.
- Provide independent loot rolls for group boss fights to incentivize co-op play.
- Run rotating boss events with temporary loot modifiers or event-exclusive items.
- Drop relic fragments that players combine into upgraded or legendary versions.
- Introduce boss-specific unique drops with rare rates and signature effects.
- Expand RelicHeim armor sets with scalable set bonuses tied to world levels.
- Implement tiered loot tables that unlock stronger rewards at higher world levels.
