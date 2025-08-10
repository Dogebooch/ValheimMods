# Valheim Modpack Design Document

**One Sentence Summary:** Exploration‑first, **boss‑gated** Valheim with **RuneScape‑style skilling/progression** and **MMORPG‑style RNG itemization with soft class archetypes** (build‑defined, not hard‑locked), where **materials dominate routine drops** and **items are rare but meaningfully powerful**; **crafting (blacksmithing)** provides the base power ladder while **enchanting** is the primary customization, with Solo‑Leveling undertones across a \~350 to 400‑hour journey.

**Timeframe Target:** 
- **WL7 \~350h avg**
- Full journey **\~350–400h** with WL8+
- Estimated time to kill: Regular mobs (10-30s), Elite mobs (45s to 3 minutes), Mini bosses (5 minutes), Regular/Elite Bosses (10-15 minutes)

---

#### Boss Loot Configuration Tasks

**Boss Enchantment Materials:**
- [] In `Valheim/profiles/Dogeheim_Player/BepInEx/config/drop_that.character_drop.cfg`, create a `[BossName.*]` block for every boss (Eikthyr → Yagluth).
- [] For each block:
  - [] `PrefabName` → WL-appropriate enchantment material pack (e.g., `EnchantPack_T1`, `EnchantPack_T2`, … `EnchantPack_T7`).
  - [] `SetAmountMin/Max` → tiered quantities (e.g., T1: 5–8, T7: 20–25).
  - [] `SetChanceToDrop = 1`, `SetDropOnePerPlayer = true`, `SetScaleByLevel = false`.
- [] Add a second entry `PrefabName = BossToken` with the same guarantees (always 1).
- [] Gate each pair with `ConditionWorldLevelMin/Max` to match WL ranges.
- [] Document the configuration change in `Valheim_Content_Mods_Summary.md`.

**Curated Rare Boss Items:**
- [] Define curated rare items in `Valheim/profiles/Dogeheim_Player/BepInEx/config/EpicLoot/patches/RelicHeimPatches/ItemInfo_BossRare.json`:
  - [] Fixed baseline stats, limited affix list.
  - [] Separate sets per boss or WL tier.
- [] In `zLootables_BossDrops_RelicHeim.json`, add `BossRare_T#` loot groups for each boss level:
  - [] Early bosses (WL1–3): `Rarity` weights targeting ~10% total.
  - [] Late bosses (WL4–7): scale to ~12–15%.
- [] Update `drop_that.character_drop.cfg` to add a corresponding `[BossName.N]` entry that calls `BossRare_T#` so the rare roll only occurs once per kill.
- [] Ensure `drop_one_per_player = true` and WL gates mirror Drop That/EpicLoot.
- [] Remove any duplicate "always item" drops from boss tables — mats should be the default reward.

**T5 Legendary Items:**
- [] Define T5 legendary items (static stats) in `RelicHeim/Legendaries_SetsLegendary_RelicHeim.json` or a new file.
- [] In `zLootables_BossDrops_RelicHeim.json`, add a `Legendary_T5` loot group with `Rarity` ≈3%.
- [] Develop a BepInEx plugin (e.g., `BossLegendaryPity.cs`) under `Valheim/BepInEx/plugins/`:
  - [] Track per-player boss kill counts.
  - [] Each kill rolls 3% chance; increment counter on failure.
  - [] Force drop when counter ≥ streak threshold (target P50≈22, P95≤40) and reset counter.
- [] Hook plugin into `OnBossDeath` to inject the item if pity triggers.
- [] Document plugin purpose and configuration in `Valheim_Content_Mods_Summary.md`.

**Mythic (T7) Items:**
- [] Create Mythic item definitions in `Legendaries_SetsMythic_RelicHeim.json` with minimal affix variance.
- [] In `zLootables_BossDrops_RelicHeim.json`, append `Mythic_T7` loot group with `Rarity` set to ~1%.
- [] Extend the pity plugin (`BossLegendaryPity.cs`) or make a sibling (`BossMythicPity.cs`):
  - [] Activate only if `worldLevel >= 7`.
  - [] Base drop: 1% (early WL7), scale up to 1.5% at WL8+.
  - [] Track kill streaks; guarantee a mythic after threshold (e.g., 70 kills).
- [] Add WL7+ gating (`ConditionWorldLevelMin = 7`) in both Drop That and EpicLoot configs.

**Materials > Items Ratio Guardrails:**
- [] Maintain a global **~8:1 materials : items** ratio for all boss fights.
- [] Boss fights should **always** drop mats + token; items are a separate rare roll.
- [] Elites (non-boss) can drop small mat bundles + rare item chance ≤ 2%.
- [] Keep legendary/mythic pity plugins active only for item drops — mats remain deterministic.

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
- [] Adjust drop that configs for drop ratio target (8 mats : 1 item)
- [] Adjust RelicHeim patches to match drop ratio target (8 mats : 1 item)
  - [] Adjust DeepNorth, Ashlands and Ocean Chests (see if there are any)
- [] Appraise chests so that they prioritize enchanted materials and rare item drops
- [] Ensure balance across the chests/drops so that rare items feel meaningful and earned

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
- [] In each WL chest group, add a **Spike** sub-group:
  - [] `EnchantPack_T{WL+1}` with `Rarity` targeting **0.2–0.5%** total chest chance
  - [] `SetAmountMin/Max = 1–1`
  - [] Keep normal WL mats dominant; this entry sits at the bottom with tiny weight
- [] Ensure the chest group rolls **at most one spike** (use one sub-group, not multiple entries)

**Config – Bosses (Drop That + EpicLoot):**
- [] Boss guaranteed mats unchanged (WL-tier)
- [] Add **BossSpike** roll:
  - [] `EnchantPack_T{WL+1}` at **~1.0%**
  - [] Optional **WL+2** at **0.2–0.3%** for late bosses only (WL6+)
  - [] `SetAmountMin/Max = 1–1`, `SetDropOnePerPlayer = true`
  - [] Keep in a **separate call** so spike can only occur **once per kill**

**Guardrails:**
- [] No spikes on **trash mobs**; elites may have **≤0.2%** WL+1 spike at WL6+ only
- [] Keep **pity systems** for legendaries/mythics **off** for spikes (they must stay lucky)
- [] Add **logging** tag `LuckySpike` to drops to audit frequency

**Optional Plugin – Soft Cap (BepInEx `LuckySpikeLimiter.cs`):**
- [] Track per-player spike count (rolling 24h)
- [] If cap reached (e.g., **2 per day**), suppress further spikes → convert to normal WL mat
- [] Expose config:
  - [] `DailyCap=2`, `BossSpikeChance=1.0%`, `BossSpikePlusTwo=0.25%`, `ChestSpikeChance=0.35%`

**Suggested Rates (start point):**
- [] **Chests:** 0.35% for `EnchantPack_T{WL+1}`, 1 unit
- [] **Bosses WL1–5:** 1.0% `T{WL+1}`, 0% `T{WL+2}`
- [] **Bosses WL6–8+:** 1.0% `T{WL+1}` **and** 0.25% `T{WL+2}`, both single-roll capped to **max one spike**
- [] **Elites WL6+:** ≤0.2% `T{WL+1}`, single unit

**Testing:**
- [] Simulate **1000 chests / WL** → expect **2–5** spikes total (0.2–0.5%)
- [] Simulate **500 boss kills / tier** → expect **~5** WL+1 spikes; WL6–8 expect **~1** WL+2 spike
- [] Verify **inventory impact minimal** (single units) and **time-to-first-enchant** remains ≤ 3h from WL entry

**Documentation:**
- [] Add a "Lucky Spike" blurb in `Valheim_Content_Mods_Summary.md` with the current rates and caps
- [] In your in-game wiki/codex, explain: "**Very rare** chance to find a **future-tier** gem — cherish it!"

### 2.4 Deterministic Safety Nets

**Goal:** Token & streak‑breaker systems prevent droughts while keeping jackpots rare.

**Objectives:**
- Implement Token Systems and Streak breakers for unlucky players

**ToDos:**
- [] Add token currency drops for bosses
  - [] Ensure the following - **Guaranteed:** WL‑appropriate **enchant‑mat packs** (tiered quantities) + **1 token**
- [] Define token thresholds for guaranteed loot tiers
- [] Configure traders to trade items for tokens (Will be end game loot)
- [] Ensure early bosses cannot be exploited for easy tokens

### 2.5 Power Without Trivialization

**Goal:** Endgame feels strong; elites and bosses remain threatening.

**Objectives:**
- Scale mob HP, damage, and mechanics to keep them threatening, but not impossible
- Prolong out engagements, to promote co-op exploration and engagements
- Maintain combat depth for all content tiers

**ToDos:**
- [] Tune EpicMMO point gain per level so that players are naturally encouraged to specialize in a build (e.g., melee, ranged, magic) without locking them into a single playstyle
- [] Enable and simplify respecs so players can easily reset and redistribute their points at any stage of progression
- [] Assess DPS burst potential in PvE by tuning attack speed, damage multipliers, and cooldown reduction stacking
- [] Assess healing potentional in PvE by tuning healing staves, consumbales, and damage mitigation of armor, tenacity and Vitality (EpicMMO)
- [] Introduce diminishing returns on certain stacking bonuses (crit chance, attack speed, lifesteal) to prevent runaway scaling
- [] Ensure that the end game is still balanced after all of these, to feel powerful but not trivial

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
**ToDos:**
- [] Adjust the base Relicheim skilling levels so that it's adjusted for the new prolonged gametime: 400% XP boost
- [] Conduct a comprehensive skills audit to identify balance issues
- [] Add level gating to all soft skills
- [] Set the Exp Factor gain for Tier 1 skills
  - [] Run
  - [] Weapon Skills
- [] Set the Exp Factor Gain for Tier 2 Skills
  - [] Sneak
  - [] Pickaxe
  - [] Exploration
  - [] Foraging
- [] Set the Exp Factor Gain for Tier 3 Skills
  - [] Jump
  - [] Swim
  - [] Farming
  - [] Cooking
  - [] Ranching
  - [] Pack Horse
  - [] Tenacity
  - [] Lumberjacking
  - [] Building
  - [] Enchantments
  - [] Fishing
- [] Adjust Stamina exp factor gain to take into account the prolonged enounters (400% HP boost)
- [] Balance the combat around the new level 120
    - [] Cap Exp Orb drops to 1.5x
    - [] XP Curve & Progression
        - [] Recalculate total XP from 1–120; keep 90–120 stretch engaging without grind spikes
        - [] Distribute unlocks evenly across 90–120 to avoid "dead zones"
        - [] Adjust XP source balance so combat, crafting, and exploration stay within ~10–15% of each other in leveling potential
        - [] Add diminishing returns for farming low-level mobs
        - [] Set group XP bonuses so co-op is rewarding but solo viable
    - [] Skill Growth & Balance
        - [] Flatten scaling or add soft caps for key stats beyond ~level 100 to prevent snowballing with +400% HP mobs
        - [] Review cross-skill synergies (esp. damage multipliers) to avoid runaway stacking
        - [] Decide if players should max few skills or keep many viable; adjust XP cost curves accordingly
    - [] Combat Tuning (Target TTK)
        - [] Set mob HP/damage to achieve:
            - [] Regular mobs: 10–30 s
            - [] Elites: 45 s–3 min
            - [] Mini-bosses: 5–12 min
            - [] Raid bosses: 10–15 min
        - [] Modify attack speed, resistances, armor instead of raw HP bloat to keep fights dynamic
        - [] Scale XP & loot directly with TTK and difficulty
    - [] Gear & Stat Scaling
        - [] Introduce gear tiers for levels 90–120; align stat curves to prevent trivializing content
        - [] Add upgrade paths for legacy gear to retain player investment
        - [] Implement stat soft caps to preserve challenge in Ashlands/Deep North
    - [] Survivability & Player Power
        - [] Tune armor/resistance curves so players can handle longer fights without becoming immortal
        - [] Adjust resource mechanics (stamina, mana) to match longer combat pacing
        - [] Keep cooldowns relevant—prevent ability spam at high levels
    - [] Economy & Crafting
        - [] Raise crafting costs for 90–120 gear; match drop rates to higher mob HP
        - [] Ensure rare mats are tied to elites/bosses to encourage exploration
        - [] Align crafting XP gains with combat XP to prevent bypassing intended progression
    - [] Progression Flow & Player Experience
        - [] Keep exploration:combat ratio ~2.5:1 to balance resource gathering and engagement
        - [] Smooth level 90 transition to avoid a "power cliff"
        - [] Add catch-up mechanics for new/alt characters post-launch
        - [] Provide tangible rewards (cosmetics, titles, abilities) for late-game milestones
    - [] Testing & Iteration
        - [] Simulate XP gain rates & TTK across multiple builds before finalizing
        - [] Run biome-by-biome playtests for pacing verification
        - [] Plan for post-launch tuning based on player data

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
- [] Space out POI density in late biomes to reduce clustering
- [] Lower passive raid frequency to avoid constant interruptions
- [] Slow or cap routine world spawns in high-density areas
- [] Calibrate loot drops to account for decreased monster spawns

### 3.2 Itemization & Drop Table Management

**ToDos:**
- [] Identify all items not currently obtainable in-game or missing from drop tables
- [] Create a list of endgame or "drop-only" items (non-craftable)
- [] Add modded items to loot tables via Drop That configuration
- [] Configure drop rates so non-craftable items drop in pairs (one for me, one for Brett)

### 3.3 Recipe & Crafting Progression

**ToDos:**
- [] Remove or lock recipes for early-game items that should be introduced later
- [] Strategically reintroduce items across world levels instead of all at once
- [] Consolidate crafting to fewer, more versatile crafting tables
- [] Assign blacksmithing level requirements to item crafting
- [] Adjust Durability to compensate for the 400% HP boost of the monsters

### 3.5 Balance & Mod Configuration

**ToDos:**
- [] Audit stacking effects of gear, consumables, and buffs for balance issues
- [] Ensure Mushroom Monsters are correctly configured with biome-appropriate drops
- [] Balance drops objectively with measurable rarity/ratio targets
- [] Ensure world level progression is boss-kill gated (not tied to in-game days)

### 3.6 Boats & Vehicles

**ToDos:**
- [] Ensure all boats are assigned to correct workbenches
- [] Stratify boats by weight vs. speed and distribute them across world levels

**Update World**
- genloc Loc_FungusGrove_MP
- genloc Loc_MushroomGrove_MP
- genloc Loc_Vegvisr_MonMon_MP
- genloc Loc_Vegvisr_NonNon_MP
- genloc Loc_Runestone_MonMon_MP
- genloc Loc_Runestone_NonNon_MP
- Reset known recipes (if VNEI doesn't accomodate them)


### Other Idea Dump
- Highlight rare drops and track boss killcounts for social/cosmetic rewards.
- Provide independent loot rolls for group boss fights to incentivize co-op play.
- Run rotating boss events with temporary loot modifiers or event-exclusive items.
- Drop relic fragments that players combine into upgraded or legendary versions.
- Introduce boss-specific unique drops with rare rates and signature effects.
- Expand RelicHeim armor sets with scalable set bonuses tied to world levels.
- Implement tiered loot tables that unlock stronger rewards at higher world levels.
- Expanding Deep North Content: 
Raids (Custom Raids)
Global framework
You currently check raids every 60 min with a 40% global chance. In DN that can feel busy once seasonal & vanilla events pile on. Two good options:
Option A (minimal change): keep global, but tone down DN raids locally by raising their per‑interval timers and lowering their per‑interval chances.
Option B (cleaner long‑term): turn on UseIndividualRaidChecks = true and set:
    MinimumTimeBetweenRaids = 120 (2 h biome breathing room)
    lower the per‑raid chances (see below)
Either way, DN raids should be short, sharp, and rarer than Meadows/Mistlands.
Per‑raid edits (examples)
DireWolf_Army_JH – stays scary, but fewer procs and smaller waves.
# [DireWolf_Army_JH]
Duration = 90
# waves
MaxSpawned = 2                    # keep cap tight
SpawnInterval = 45                # was 30 → fewer rolls per raid
SpawnChancePerInterval = 60       # was 95 → lower flood risk
GroupSizeMin = 2
GroupSizeMax = 3
# optional: weather to make it “storm hunts”
RequiredEnvironments = SnowStorm
# If using individual checks:
# ChanceToStart = 18   # instead of relying on global, keep DN raids rare
Jotunn_Army_JH → Jotunn_Army1_JH – WL8+ set‑piece, trim frequency; keep spectacle.
# [Jotunn_Army_JH]
Duration = 90
SpawnInterval = 45           # was 30
SpawnChancePerInterval = 60  # was 95
GroupSizeMin = 2
GroupSizeMax = 3
ConditionWorldLevelMin = 8   # push real Jotunn pushes to WL8
# follow-up
# [Jotunn_Army1_JH]
Duration = 60
SpawnInterval = 45
SpawnChancePerInterval = 60
ConditionWorldLevelMin = 8
Storm_Army_JH – bind strictly to storms so it becomes a “weather event”.
# [Storm_Army_JH]
SpawnInterval = 45
SpawnChancePerInterval = 55
RequiredEnvironments = SnowStorm   # make it a true storm event
ConditionWorldLevelMin = 7
HelHounds/WarBringer/Doomcaller/Legionnaire/Daggerfang (Surtr set)
These read as Ashlands‑aligned. Let them appear in DN only as night‑rarities at WL8, and cut density so they don’t dilute DN identity:
# e.g., [WarBringer_Army_JH]
SpawnAtNight = true
SpawnAtDay = false
SpawnInterval = 50
SpawnChancePerInterval = 45
GroupSizeMin = 2
GroupSizeMax = 2
ConditionWorldLevelMin = 8
IceStalker_Army_JH (serpents) – keep spectacle but avoid shoreline spam:
SpawnInterval = 75           # was 60
SpawnChancePerInterval = 55  # was 95
ConditionDistanceToCenterMin = 2500   # was 2000
    TL;DR raids get longer intervals and lower per‑interval chance; late‑tier raids WL‑gated (Jotunn/Surtr at WL8), and several bind to SnowStorm or Night so you naturally get “quiet stretches.”
Seasonal & vanilla event pressure
    Seasonal: keep your “wolves in winter” weight bump, but set DN weights to 0 or 0.5 for off‑theme events (e.g., army_charred, army_charredspawners, army_seekers) so DN keeps its icy identity.
    Vanilla: allow Bats only during Night and SnowStorm, and drop their per‑interval chance to avoid bat‑spam in DN.
    Hildir bosses (in DN): WL‑gate them to 7+ and reduce their support minions’ SpawnChancePerInterval by ~30–40% in DN so they don’t crowd the biome baseline.
(Exact JSON/YAML knobs depend on your Seasons/Events files; mirror the same pattern you used for Meadows/Black Forest: set allowed biomes, weights, RequiredEnvironments, and WorldLevel conditions.)
------------------------------------------------------------------------------------------------------------------------------------------------------



### Finished (See Change Log):
**Goal:** POIs, routes, and biome mastery matter more than raw ARPG loot rain.
**Goal:** Set POI density targets per biome and adjust mods/POI packs accordingly
**Goal:** Ensure monsters per POI and loot per POI are balanced for FPS and difficulty
**Goal:** Make engagements fun but not overwhelming by making an exploration:Combat ratio
**Goal:** Ensure breathing room for combat AND exploration
**Goal:** Adjust Creature Spawns to match target density and reward curve\
**Goal:** The world only advances after the relevant boss dies (server-wide), letting players set their own pace.


- [x] Review every mod's configuration to understand and document gameplay impact
- [x] Raise Max level EpicMMO to 120
- [x] Make the death XP cost less punishing
- [x] Make resetting attributes easier, so that we can respec pretty much whenever we want
- [x] Set Target Densities per Biome as below
    - [x] See how the Warpalicious mods interacts with the poi_density.csv
    - [x] Decide on estimated time to kill for:
          - [x] Regular Mobs - 10-30s
          - [x] Elite Mobs - 45 seconds to 3 minutes
          - [x] Mini Bosses - 7-12 minutes
          - [x] Regular/Elite Bosses - 10-15 minutes
    - [x] Target "Exploration:Combat" ratio of about 3:1 most of the game, can be 2:1 in the Ashlands. Can estimate it by taking into account the density, chance to spawn and time interval for spawn for each mob
    - [x] Set Meadows from 0.535/km^2 reduce to 0.4/km² (0.3 standard, 0.1 elite/challenge).
    - [x] Set Blackforest = _ targets per Km^2
    - [x] Set Swamp set = _ targets per Km^2
    - [x] Set Mountains = _ targets per Km^2
    - [x] Set Plains = _ targets per Km^2
    - [x] Set Mistlands = _ targets per Km^2
    - [x] Set DeepNorth = _ targets per Km^2: 24 new Creature spawns + 6 boss spawns
    - [x] Set Ashlands = _ targets per Km^2
    - [x] Set Oceans = _ Targets per Km^2  
    - [x] Adjust for the More_World_Traders & the Adventure_Map_Pack
    - [x] Look for all of the mods that change boss gating/World Leveling
- [x] Ensure all biomes scale appropriately when unlocked
- [x] Change gating so that the WL only increases when the base bosses are killed (WL1-8)
  - [x] Eikthyr kill -> WL2
  - [x] Elder Kill -> WL3
  - [x] Bonemass Kill -> WL4
  - [x] Moder Kill -> WL5
  - [x] Yagluth Kill -> WL6
  - [x] The Queen -> WL7
  - [x] Deep North Boss -> WL8
  - [x] Ashlands Boss -> WL9

