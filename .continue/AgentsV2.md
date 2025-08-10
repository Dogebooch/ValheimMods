# AGENTS\_v2 – JewelHeim/RelicHeim Overhaul (Draft)

## 1) Core Vision (one sentence)

Exploration‑first, **boss‑gated** Valheim with **RuneScape‑style skilling/progression** and **MMORPG‑style RNG itemization with soft class archetypes** (build‑defined, not hard‑locked), where **materials dominate routine drops** and **items are rare but meaningfully powerful**; **crafting (blacksmithing)** provides the base power ladder while **enchanting** is the primary customization, and **select relics grow with the player** (Solo‑Leveling undertones) across a \~350 to 400‑hour journey.

---

## 2) Design Pillars

1. **Exploration over treadmill** – POIs, routes, and biome mastery matter more than raw ARPG loot rain.
    [ ] Set Target Densities per Biome ([poi_density.csv](./poi_density.csv))
        [x] See how the Warpalicious mods interacts with the poi_density.csv
        [ ] Set Meadows = 0.40 targets per Km^2
            [ ] Adjust for Meadows Pack 1 & 2: 24 unique location types, 205 total instances
                [ ] Balance the amount of monsters per POI (decrease to decrease the overhead), or adjust the loot so it's stronger at those areas.
            [ ] Adjust for the Resource Nodes: ~40
            [ ] Adjust for Creature Spawns: +7-11 from Monstrum and MushroomMonsters
                [ ] Adjust the Creature Spawns to improve fps/overhead, adjust for +400% HP of the monsters, and change drops to compensate for the decreased spawn locations
        [ ] Set Blackforest = 0.30 targets per Km^2
            [ ] Adjust for Blackforest Packs 1 & 2, Forbidden Catacombs
        [ ] Set Swamp set = 0.28 targets per Km^2
            [ ] Adjust for Swamp Pack 1, Underground Ruins
        [ ] Set Mountains = 0.22 targets per Km^2
            [ ] Adjust for Mountains Pack 1
        [ ] Set Plains = 0.32 targets per Km^2
            [ ] Adjust for Plains Pack 1
        [ ] Set Mistlands = 0.20 targets per Km^2
            [ ] Adjust for Mistlands Pack 1
        [ ] Set DeepNorth = 0.14 targets per Km^2
        [ ] Set Ashlands = 0.16 targets per Km^2
            [ ] Adjust for Ashlands Pack 1
        [ ] Set Oceans = 0.06 Targets per Km^2
        [ ] Adjust for the More_World_Traders & the Adventure_Map_Pack


# Pillar 1 – Exploration
POI_density: Meadows=__, BlackForest=__, Swamp=__, Mountains=__, Plains=__, Mistlands=__, DN=__, Ocean=__, Ashlands=__
Event_rate_per_hour: WL1=__%, WL3=__%, WL6=__%, WL8=__%
Raid_cooldown_hours=__
Onscreen_hostiles_avg<=__, p95<=__
Sailing_mix_WL3_7=__%
Dungeon_rooms_by_WL: WL2=__, WL4=__, WL6=__, WL8=__
High_tier_chest_share: WL1=__%, WL7=__%, WL9=__%

# Pillar 2 – Boss→WL
WL_map_confirm=YES/edits(...)
Server_wide_only=YES/NO
Disable_age_gates=YES/NO
Hours_per_WL: 2=__,3=__,4=__,5=__,6=__,7=350,8=__,9=400

# Pillar 3 – Mats>Items
Creatures_ratio=__:1   (recommend 9:1)
Chest_WL1_2=Enchant__/Items__/Raw__
Chest_WL3_5=Enchant__/Items__/Raw__
Chest_WL6_7=Enchant__/Items__/Raw__
Chest_WL8_9=Enchant__/Items__/Raw__
Chest_tolerance=±__%
Drop_one_per_player: Elites=YES/NO, Boss=YES
First_enchant_SLA_hours=__

# Pillar 4 – Safety Nets
Tokens_per_kill=__
Legendary_token_cost=__
Mythic_token_cost=__
Shard_drop_chance=__%
Shards_to_token=__:1
Tokens_tradeable=YES/NO
Voucher_item_IDs=[...]
Late_boss_RNG_bumps: Legendary=+__%, Mythic=+__% (or NONE)

# Pillar 5 – Power without trivialization
EnemyHPMult=4.0 (y/n), EnemyDamageMult=__
Elite_affix_caps: [...]
Armor_EHP_increase_per_WL>=__%
TTK_elite=10–25s (y/n), TTK_boss_late=4–8m (y/n)
SpawnCoupling=STRICT (y/n); Exceptions=[...]
Test_food_baseline=[...]


















2. **Boss → WL gate** – The world only advances after the relevant boss dies (server‑wide), letting players set their own pace.
3. **Materials > Items** – Creatures target **\~8:1** materials\:items; chests emphasize **enchant mats + occasional items**.
4. **Deterministic safety nets** – Token & streak‑breaker systems prevent droughts while keeping jackpots rare.
5. **Power without trivialization** – Endgame feels strong; elites and bosses remain threatening.

---
## 3.0) Other ToDos:
  [ ] Optimize the overhead by doing the following
      { } Space out POI density in late biomes.
      { } Lower passive raid frequency.
      { } Slow or cap routine world spawns.
      { } Apply stronger global spawn throttles.
      { } Ensure that loot drops have been calibrated to the decreased monster spawns
  [ ] Figure out which items aren't in the game or currently configured to a drop table
      [ ] Also, make a list of end game items, or items that wont be able to be crafted (only dropped)
      [ ] Configure Drops to add items from mods I added (loot tables)
      [ ] Change settings so that for all of the items that can't be crafted, there is 2 that drop: one for me and one for brett
  [ ] Remove recipes for a lot of items; brainstorm how to introduce items throughout the game, rather than all at once
  [ ] Pace out the skilling (see below if there's already a section for this), Dont forget the AzuExp
      [ ] Do a comprehensive skills Audit
  [ ] Do a comprehensive balance assessment of the stacking of different items
  [ ] Go through each mods configs to see what is affected by each setting and to see what other gameplay changes can be made
  [ ] Consolidate Items to a smaller amount of tables?
  [ ] Make a "Wiki" app, at least for key items at different points in the game
  [ ] Change Items so they require a blacksmithing level to make (see below)
  [ ] Ensure the Mushroom Monsters are correctly configured and have appropriate drops
  [ ] Balance the drops (see below), you need to make some decisions to make it more objective
  [ ] Make all the soft skills have level gating
  [ ] Ensure the world level increases by boss kills, not in game days
  [ ] Ensure boats are correctly configured to their respective workbenches 
      [ ] Stratify by weight vs. speed, then divy them up across world levels

## 3) Pacing & World Levels (WL)

* **WL mapping (server‑wide, first kill):**

  * Start → **WL1**
  * **Eikthyr** kill → **WL2**
  * **Elder** → **WL3**
  * **Bonemass** → **WL4**
  * **Moder** → **WL5**
  * **Yagluth** → **WL6**
  * **The Queen** → **WL7**
  * **Ashlands/Deep North boss** (if present) → **WL8+** (optional)
* **Group scaling:** Enemies scale by players in area; caps tuned to keep co‑op rewarding.
* **Timeframe target:** **WL7 \~350h avg**; full journey **\~350–400h** with WL8+.

**Success metrics**

* WL progression occurs only via boss kills; no unintended time/age bumps.
* Median hours to WL7 ≈ **350** (±10%).

---

### 3b) New Biomes & Content Packs

* **Deep North / Ocean / Ashlands** additions are mapped to **WL8+**. Chest tables and boss drops for these biomes follow the **materials‑first** and **curated rare** rules; enchanting mats introduce **Tier‑7** effects gated to WL8+.
* POI mods (new locations, monsters, items) must inherit **WorldLevelMin/Max** consistently across **Drop That**, **EpicLoot**, and **SpawnThat**.

### 3c) WL8–WL9 Timing Targets

* **WL8 (Deep North / Ocean)**: target **\~380 hours** cumulative playtime.
* **WL9 (Ashlands endgame)**: target **\~400 hours** cumulative playtime (cap total journey at \~400h).

---

## 4) Loot Philosophy

**Creatures (avg per WL):** **materials : items ≈ 8:1** (acceptable 7–10:1).

**Chests:** prioritize **enchanting materials + occasional items** over raw mats. Target split: **Enchant mats 40–50% | Items 15–25% | Raw mats 30–40%**.

**Boss Rewards (per kill):**

* **Guaranteed:** WL‑appropriate **enchant‑mat packs** (tiered quantities) + **1 token**.
* **Rare item roll:** **Boss Rare (strong, curated)** — **\~10%** early bosses, scaling to **\~12–15%** late bosses. Items are **pre‑curated** (fixed baselines, small affix set) so a drop is exciting and build‑shaping.
* **Legendary path (T5 static):** base **\~3%** with streak‑breaker → **P50 ≈ 22 kills, P95 ≤ 40**.
* **Mythic (WL7+):** effective **\~1–1.5%** with pity.

**Success metrics**

* Materials constitute ≥70% of non‑chest drops; chest rolls feel exciting due to enchant mats.
* Boss kills feel rewarding **even without an item** due to mat packs + token; item drops feel **rare and strong**.

---

## 5) Skills (Tier Targets → WL Windows)

**Tier 1 – Gamechangers** *(Run, Sailing, Weapon skills)* → **L70 by early Ashlands (WL7‑early)**.
**Tier 2 – Strong Utilities** *(Sneak, Pickaxe/Mining, Exploration, Foraging, Blacksmithing)* → **L70 by Deep North entry (post‑WL7)**.
**Tier 3 – Flavor/Minor** *(Jump, Swim, Cooking, Farming, Ranching, Pack Horse, Tenacity, Lumberjacking, Building, Enchanting)* → **L70 by late Mistlands (WL6‑late)**.

**XP tuning (initial anchors)**

* Tier1: multipliers ≥ **1.0–1.1**; Tier2: **0.6–0.75**; Tier3: **0.55–0.8** (Swimming may remain higher as QoL).

**Success metrics**

* Sim shows median player meeting the tier targets within WL windows without grinding exploits.

### 5b) Classes & Co‑op Roles (Config Blueprint)

> **Soft archetypes, no hard locks.** Implemented via items/enchants/sets/skills only.

**Tank**

* **Goal:** Soak sustained damage, stabilize fights, hold attention.
* **Knobs (config‑only):**

  * **Armor sets** (WackyDB): +% **Physical/Magic DR**, +**Block Power**, **Stagger resist**; WL‑gated.
  * **Enchant affixes** (EpicLoot pools): **Block Power**, **Flat DR on Block**, **Thorns (low)**; later WL unlocks.

    * **Skills:** **Blocking** XP slightly boosted (AzoSkillTweaks) to hit Tier‑1 window.
* **Targets:** With WL‑appropriate gear, **no one‑shots**; elites **TTK 10–25s** with group; tank death rate ≤ DPS.

**Mage**

* **Goal:** Reliable DPS/control; fragile but not paper.
* **Knobs:**

  * **Staves/robes** (WackyDB): Eitr, **Eitr regen**, **Magic pen**, **Ward** (small %DR) at WL gates.
  * **Affixes:** **Int→Eitr regen**, **Spell crit**, **DoT amp** unlocked gradually.
  * **Consumables:** **Barrier Flask** (+20% magic DR for 10s, CD 90s).
* **Targets:** Comparable boss contribution to melee at same WL; not out‑DPS by pure RNG melee legendaries.

**Ranger**

* **Knobs:** Bows/javelins sets; affixes for **Projectile speed**, **Headshot**, **Stamina on hit**; WL‑gated.

**Stealth/Assassin**

* **Knobs:**

  * **Affixes:** **Backstab amp**, **Sneak stamina cost ↓** (late WL).
  * **Consumables:** **Smoke Bomb** (SE: reduced detection radius for 6s, CD 90s).
* **Targets:** Backstabs feel rewarding without trivializing elites; no single‑hit deletes bosses.

**Support/Healer** *(optional if mod set allows)*

* **Knobs:** small **group buffs**, **regen totem** via SE items; WL‑gated.

**Guardrails (across roles)**

* Maintain **enemy HP ×4** while tuning **damage down 10–20%** globally (CLLC).
* Adjust **SpawnThat** using **§8c coupling** so longer fights don’t create crowding.
* Class items/affixes unlock by WL; avoid early spikes.

---

## 6) Enchanting System (RelicHeim‑centric)

* **Primary customization path**; crafting sets the base, enchanting personalizes.
* **Enchant mats** are the excitement driver in chests and bosses/elites; **tier‑gated by WL**.
* **Abundance rule**: engaging but controlled — **first meaningful enchant ≤ 3 hours** after entering a new WL.
* **Affix scope**: early WL affixes are utility/defense‑leaning; offensive affixes unlock later WLs to avoid early spikes.

**Success metrics**

* Average time from new WL → first meaningful enchant ≤ **3 hours**.
* No high‑tier affixes appearing before their WL gate.

---

## 6b) Blacksmithing Progression (Base‑Item Ladder)

* **Goal:** crafting is the **base power ladder**; enchanting personalizes.
* **Gates (skill + bench + WL)**

  * **Tier 0 (Meadows / WL1):** Blacksmithing ≥ **1**, Bench **1**
  * **Tier 1 (Black Forest / WL2):** ≥ **15**, Bench **2**
  * **Tier 2 (Swamp / WL3):** ≥ **30**, Bench **3**
  * **Tier 3 (Mountains / WL4):** ≥ **45**, Bench **4**
  * **Tier 4 (Plains / WL5):** ≥ **60**, Bench **5**
  * **Tier 5 (Mistlands / WL6):** ≥ **75**, Bench **6**
  * **Tier 6 (Ash/Deep North / WL7+):** ≥ **90**, Bench **7**
* **Recipe policy:** higher tiers require WL mats + prior‑tier item; keeps crafting relevant through endgame.

**Success metrics**

* Players typically craft a **new base tier every 30–40 hours**.
* Crafted bases + enchants outperform dropped generics at the same WL.

---

## 7) Signature “Growing” Items *(Requires plugin; see Appendix E.1)*

* **Bonded relics** that automatically scale with **WL** and **kill milestones** are **not possible via configs alone**. They require runtime logic to adjust stats per item instance.
* **Interim (config-only) fallback:** implement **static upgrade tiers** (e.g., *Relic I → II → III*) via **WackyDB** recipes that consume **BossShards/Tokens**; keep each tier within §C1 power budgets.

**Success metrics**

* With the plugin: relic upgrades every **\~20–40 hours**; competitive but not dominant; no duplication exploits.
* Without plugin: tier upgrades feel meaningful but do not exceed Mythic caps.

---

## 8) Difficulty Targets

* **Normal foes TTK** (mid‑game): **5–12s**
* **Elites TTK** (WL6–7): **10–25s**
* **Boss TTK**: early‑WL **2–6m**; late‑WL **4–8m**
* **HP scaling:** Enemies **HP ×4.0** (liked), with **damage multipliers tuned down** to keep one‑shots rare.
* **Player survivability**: common hits threaten; mistakes punish; perfect play rewarded; **no unavoidable one‑shots**.

---

### 8b) One‑Shot Mitigation (Config‑Only)

> Pure config can’t add true “prevent lethal once” logic, but we can approximate.

* **CLLC damage tuning:** reduce global enemy **damage multiplier** by **10–20%** while keeping **HP ×4.0**.
* **Armor floor:** ensure base gear per WL provides **≥35–45% EHP increase** vs prior WL (via equipment curves), preventing extreme one‑shots on progression gear.

**Success metrics**

* One‑shot rate (hits causing >80% max HP in one instance) **< 5%** of deaths in WL6–7 logs.
* Elite median TTK stays within **10–25s** after damage/HP tuning.

---

### 8c) Combat–Spawn Coupling (Keep Fights Longer, World Playable)

**Principle:** If TTK increases, **density and inflow must decrease** so exploration isn’t crowded out.

**Rule of thumb (apply per spawner/event):**

* Let **TTK\_boost = NewTTK / BaselineTTK**.
* Set \**spawn\_chance\_pct *= 1 / TTK\_boost**.
* Set \**spawn\_interval\_s *= TTK\_boost**.
* Keep **max\_spawned** the same or **–1** if swarms form.

**Examples:**

* If elites go from 12s → 20s (**TTK\_boost=1.67**): reduce spawn chance by **\~40%** and increase interval by **\~67%**.
* For raids, apply the same to **chance\_per\_hour** and **cooldown\_hours**.

**Success metrics**

* Average on‑screen hostiles **≤ 6**, p95 **≤ 12** in open‑world play.
* Combat time share **≤ 55%** of playtime at WL6–7 (leaves room for exploration/gathering).

---

## 9) Economy & Vendors

* Control coin inflows (limit CoinTroll/event spikes).
* **Vendor daily limits** on sellbacks; price tiers tied to WL. *(Requires plugin; see Appendix E.4).*
* Token store provides deterministic chase **without** bypassing exploration.

**Success metrics**

* Coins/hour within target bands; vendor items do not trivialize WL tiers.

---

## 10) Anti‑Drought Systems (Config‑only Plan)

**Goal:** Keep jackpots rare but fair while avoiding code hooks. Use only editable configs.

### 10a) Token System (Deterministic, Soft)

* **Mechanic:** Each boss kill drops **1× `BossToken`** (per player) via **Drop That** (`DropOnePerPlayer=true`, `WorldLevelMin` aligned).
* **Exchange (config‑only):** Use **WackyDB Recipes** (or Vendor trades if available) to craft chase items:

  * **Legendary voucher** = `BossToken × 20` + WL mats → crafts to **curated Legendary** (T5 static, boss‑locked list).
  * **Mythic voucher** (WL7+) = `BossToken × 60` + WL7 mats → crafts to **curated Mythic**.
* **Vendor limits (optional):** Daily limits and WL locks in merchant config to avoid front‑loading.
* **Softness:** Token costs are **high**; tokens **don’t** reduce RNG chance.

### 10b) Streak‑Breaker (Bad‑Luck Protection, Soft Proxy)

> True per‑player pity isn’t stateful in pure configs. We approximate **soft pity** without code.

* **Baseline boss RNG (EpicLoot weights):**

  * **Legendary:** base **2.5–3.0%**
  * **Mythic (WL7+):** base **\~1.0%**
* **Soft proxies:**

  * Slightly higher weights on later bosses (e.g., +0.25–0.5% absolute by tier) and **stars/elite variants**.
  * Rare **`BossShard`** drop (low chance) → **5 shards = 1 BossToken** (WackyDB recipe). Feels like pity without state.
* **Guardrails:** Keep combined effect (RNG + tokens + shards) below **effective \~6–7% legendary** and **\~2% mythic** at WL7.

**Success metrics**

* Legendary first‑drop **P50 \~22–28 kills**, **P95 ≤ 45** (simulated via weights + token accrual).
* No early flooding; tokens pace deterministic progress while RNG remains exciting.

---

## 11) Telemetry & Validation

* Enable spawn/kill/drop logs; WL change audit.
* Track per‑player: **boss kills, tokens earned/spent, shards, RNG drops**.
* Dashboards: loot mix (mats/items), TTK bands, boss progress, coin flow, enchant usage.
* **Audit after changes:** verify effective legendary/mythic rates against guardrails.

---

## 12) Immediate Tasks (v0.1 Build)

* [ ] Switch WL progression to **boss‑gated** (mapping above; apply kill→WL with a short delay).
* [ ] **Boss loot pass**: remove weak guaranteed items; add **mat packs + 1 token** guaranteed; add **Boss Rare roll** (\~10% early, 12–15% late) with curated, strong items; keep **Legendary 2.5–3% base** and **Mythic \~1%** at WL7+.
* [ ] **Chest tables**: enforce **Enchant mats 40–50% | Items 15–25% | Raw mats 30–40%**.
* [ ] **Skill tier multipliers** to hit L70 windows (Tier1 ≥1.0, Tier2 0.6–0.75, Tier3 0.55–0.8; Swimming higher if QoL).
* [ ] **Blacksmithing gates**: require skill + bench levels for base‑item tiers by WL (§6b).
* [ ] Add **bonded relic** framework (WL & kill‑based scaling, shard drops from bosses).
* [ ] Vendors: daily limits and coin‑sink pricing.
* [ ] **CLLC tuning**: set **EnemyHPMult = 4.0**, **EnemyDamageMult = 0.8–0.9**, verify elite affix multipliers; adjust resistances if needed.
* [ ] **SpawnThat coupling** (see §8c): reduce **spawn\_chance\_pct** and/or increase **spawn\_interval\_s** in proportion to TTK increase; set **local caps** to avoid crowding.

---

## 13) Open Decisions (need your call)

1. **Boss‑gate delay:** 10 minutes vs “at next dawn” after kill?
2. **Chest ratio:** keep **(enchants+items) 60–70%** vs another split?
3. **Token costs:** Legendary **20** tokens, Mythic **60** tokens (soft, high cost) – adjust?
4. **Swimming XP:** keep higher (QoL) or align with Tier‑3 1.2x?
5. **BossShard proxy:** enable **shards → tokens** at **5:1** (soft pity)?

---

## 14) Balance Dependency Matrix (Change‑Impact Cheat Sheet)

| Module                           | Main knobs                                          | Increases                                   | Decreases              | Observe/Guardrails                                          |
| -------------------------------- | --------------------------------------------------- | ------------------------------------------- | ---------------------- | ----------------------------------------------------------- |
| **Drop That – Boss**             | `ChanceToDrop`, `DropOnePerPlayer`, `WorldLevelMin` | Legendary/Mythic availability, token inflow | Streak experience      | Keep effective legendary ≤ \~6–7% at WL7 incl. token pacing |
| **Drop That – Creatures/Chests** | weights, guaranteed rolls                           | Mats inflow, enchant pace                   | Scarcity fantasy       | Chests: Enchant 40–50% \| Items 15–25% \| Mats 30–40%       |
| **EpicLoot Weights**             | rarity weights per source/WL                        | RNG excitement                              | Drought protection     | Maintain low early‑WL rates; small late‑WL bumps only       |
| **WackyDB Recipes**              | skill/bench/WL gates, token/voucher crafts          | Deterministic progress, crafting relevance  | RNG dominance          | Vouchers high‑cost; WL mats required                        |
| **AzoSkillTweaks**               | `xp_mult` per skill tier                            | Faster tier goals                           | Grind time             | Tier1 ≥1.0; Tier2 0.6–0.75; Tier3 0.55–0.8                  |
| **SpawnThat**                    | spawn weights, caps                                 | Resource & coin inflow                      | Scarcity and challenge | Plains/Farm inflations; event spikes                        |
| **CLLC**                         | WL enemy scaling                                    | Challenge, TTK                              | Accessibility          | Elites TTK 10–25s at WL6–7                                  |

---

## 15) AI Edit Contract (to prevent hallucinations/bugs)

1. **Only touch** keys/lines explicitly listed in change tickets (selector + param).
2. **Preserve** comments, blank lines, key order, and file formatting.
3. **No new sections** unless ticket includes a schema‑backed snippet.
4. **Validate** after edit: syntax, ranges, and cross‑mod consistency (WL gates, item IDs).
5. **Log diff** per file: before/after, line numbers, reason.
6. **Reject** changes that would breach guardrails; request human approval.

---

## 16) Consistency Notes

* Core vision: full journey **\~350–400h**; **WL7 \~350h** target. Ensure all WL gates and XP/loot pacing match this timeline.
* Boss loot now: **mat packs + token** guaranteed; **curated rare items** low chance; legendary/mythic stay rare. Align all drop tables.
* For new biomes (DN/Ocean/Ashlands): ensure **WorldLevelMin/Max** and chest/boss tables follow the materials‑first + curated‑rare philosophy and WL8+ gating.

---

## Appendix E — Code‑Required Features & Implementation Tickets

> These features cannot be delivered with configs alone. Below are concise plugin specs, config bindings, and success criteria.

### E.1 Bonded / Growing Relics

**Why code is needed**
Per‑item **runtime scaling** (by WL or kill milestones) requires reading item instance IDs and adjusting stats dynamically—beyond WackyDB/EpicLoot configs.

**Minimal plugin surface**

* **Events:** `OnWorldLevelChanged(newWL)`, `OnEnemyKilled(victimPrefab, stars, wl, killerId)`, `OnBossKilled(bossId, wl, killerId)`.
* **Item hooks:** read/write **UniqueID** metadata; apply temporary **stat multipliers** or attach a hidden **StatusEffect** to the equipped relic.
* **Persistence:** per‑player relic progress saved server‑side; server authoritative.

**Config bindings**

* EpicLoot item tagged `RelicId` and **growth curve** (WL multipliers, kill milestones, hard caps).
* WackyDB optional **shard upgrades**: `RelicShard` → +2–3% EDPS (max 2).

**Success criteria**

* Upgrade cadence **20–40h**; relic EDPS stays within Appendix C caps; no duplicate/dupe abuse; logs include relic state changes.

**Fallback (config‑only)**

* Static **Relic I/II/III** crafting chain via WackyDB using **BossShards/Tokens**.

---

### E.2 Prospector’s Kit (+1 yield roll with cooldown)

**Why code is needed**
Configs can’t intercept **node harvest** nor enforce per‑player cooldowns.

**Minimal plugin surface**

* **Event:** `OnNodeMined(nodeType, playerId)`; if player has **Prospector SE** and cooldown ready → roll **extra loot table**.
* **Cooldown:** per‑player timer; config `cooldown_seconds` (e.g., 120s).
* **Gates:** requires equipping **Prospector’s Kit** (WackyDB item) and `Mining≥80`.

**Config bindings**

* WackyDB item `Prospector_Kit` (equip SE flag).
* Drop That table `Prospector_ExtraRoll` per nodeType with low weights.

**Success criteria**

* Long‑run yield +10–15% at `Mining≥80` without flooding mats; cooldown respected; logs show proc rate.

**Fallback (config‑only)**

* Small **flat yield** increase on ore recipes and rare **BossShard→Ore Cache** crafts to mimic progress, without on‑hit procs.

---

### E.3 Freyja’s Planter (plant any crop anywhere)

**Why code is needed**
Vanilla **biome checks** block growth; configs cannot bypass.

**Minimal plugin surface**

* **Placement:** a `FreyjasPlanter` piece defines a **growth radius**.
* **Rule:** crops inside radius **ignore biome restriction** and optionally apply `growth_time_mult` (e.g., 1.25–1.5) and **yield\_penalty\_pct** (e.g., –10%) to keep balance.
* **Gates:** `Farming≥80`, WL gate, upkeep fuel or durability.

**Config bindings**

* WackyDB piece `FreyjasPlanter`; upkeep item; recipe gates (skill+WL).

**Success criteria**

* Off‑biome crops grow reliably **only** within planter radius; mats/hour stays within target bands.

**Fallback (config‑only)**

* None (requires plugin) or use an existing **PlantAnywhere**‑style plugin if compatible.

---

### E.4 Vendor Daily Item Limits / Sellback Caps

**Why code is needed**
TradersExtended doesn’t enforce **per‑item per‑day** caps.

**Minimal plugin surface**

* **PrePurchaseCheck(playerId, itemId, qty)** → returns `allowedQty`.
* **Counters:** per‑item **daily limits** (server‑wide and/or per‑player); **sellback caps** and WL‑tiered prices.
* **Reset:** daily at server midnight or configurable `reset_utc_hour`.

**Config bindings**

* Table `VendorLimits.csv`: `itemId, wl_min, daily_limit, per_player, sell_cap, price_mult_by_wl`.

**Success criteria**

* Purchases over cap are blocked; restock at reset; economy logs show smooth coin sink with no exploits.

**Fallback (config‑only)**

* Price/recipe increases as soft throttle (doesn’t prevent hoarding).

---

### E.5 Telemetry & Dashboards

**Why code is needed**
Configs can’t emit or aggregate the following metrics.

**Minimal plugin surface**

* **Events logged**: spawns, kills (with WL/star), boss kills, drops (item vs mats, rarity), chest opens, coins in/out, crafting/enchanting, deaths, WL changes.
* **Format:** JSONL (one event per line) with server timestamp; rolling files by day.
* **Privacy:** no PII beyond a stable anonymized player hash.

**Success criteria**

* p50/95 TTK bands, loot ratios, and boss‑progress charts match §8/§4 targets within tolerance; anomalies catch misconfigs quickly.

**Fallback (config‑only)**

* Manual sampling (impractical); recommend plugin for accuracy.

---
