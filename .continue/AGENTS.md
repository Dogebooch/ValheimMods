# Valheim Mods Project – AI Agent Brain (Slim Version)

## 🎯 Core Mission
Create a **RuneScape + Solo Leveling** inspired Valheim overhaul with MMO-like progression, rewarding grind, and balanced loot pacing.  
Target: ~800 hrs total, 6–12 month playthrough at 10–15 hrs/week.

---

## 📊 Progression & Skill Systems

### EpicMMO (Primary RPG Progression)
- **Max Level**: 120 | XP curve tuned for long-term growth
- **Free Points Per Level**: 5 (RelicHeim default)
- **Start Free Points**: 5 (RelicHeim default)
- **Level Experience**: 300 XP base per level
- **Experience Multiplier**: 1.048 (raised for longer progression)
- **Add Level Experience**: Enabled (adds 300 XP per level)
- **Bonus Level Points**: +5 every 5 levels (RelicHeim default)
- **Experience Rate**: 1.0x (normal)
- **Death Penalty**: 5-25% XP loss (RelicHeim default)
- **Reset Cost**: 3 coins per point (RelicHeim default)
- **Target biome/WL pacing**: ~100–120 hrs per biome

### Attribute Scaling (per point)
- **STR**: +0.3 dmg, +4 weight, +0.5 crit dmg
- **DEX**: +0.3 atk spd, +0.3 atk stam
- **END**: +1 stam, +0.5 regen, +0.3 armor
- **INT**: +0.3 magic atk, +0.3 eitr regen, +1 eitr
- **VIG**: +1 HP, +0.5 regen

### SmartSkills & Vanilla Adjustments
- **Skill Recovery Bonus**: 50% XP boost until reaching previous highest level
- **Weapon Catch-up Bonus**: 50% XP boost for weapon skills until caught up to highest weapon skill
- **Swimming**: 100% XP bonus, no death penalty
- **Sneak**: +10% XP on backstab, +25% backstab damage at level 100
- **Blood Magic**: 33% XP sharing between shield caster and attacker

### Vanilla Skill Experience Factors (Current Configuration)
- **Farming**: 0.8x (reduced for slower progression)
- **Mining**: 0.6x (reduced)
- **Lumberjacking**: 0.6x (reduced)
- **Foraging**: 0.6x (reduced)
- **Building**: 0.65x (reduced)
- **Blacksmithing**: 0.7x (reduced)
- **Pack Horse**: 0.75x (boosted)
- **Sailing**: 0.4x (reduced)
- **Tenacity**: 0.4x (reduced)
- **Warfare & Enchantment**: 1.0x (normal)

---

## 🌍 World Level Gating
| WL | Biome        | Boss Requirement |
|----|--------------|------------------|
| 0  | Meadows      | Start            |
| 1  | Black Forest | Defeat Eikthyr   |
| 2  | Swamp        | Defeat The Elder |
| 3  | Mountains    | Defeat Bonemass  |
| 4  | Plains       | Defeat Moder     |
| 5  | Mistlands    | Defeat Yagluth   |
| 6  | Deep North   | Defeat The Queen |
| 7+ | Ashlands     | Defeat Fader     |

---

## 💎 Loot System Overview

| Type                  | RNG? | Source         | Purpose         | Affixes |
|-----------------------|------|----------------|-----------------|---------|
| EpicLoot Magic/Rare   | ✅   | Random         | Early–mid game  | 1–2     |
| EpicLoot Legendary    | ✅   | Random         | High RNG tier   | 3+      |
| EpicLoot Mythic       | ✅   | Random         | Top RNG tier    | Special |
| RelicHeim Sets        | ❌   | Crafted        | Static bonuses  | Static  |
| T5 Legendaries        | ❌   | Boss-locked    | BiS static loot | Static  |

**Config Rules**
- `world_level_min` identical in Drop That & EpicLoot
- Star gating: Magic/Rare at 2★, T4 at 3★
- All chase loot: `drop_one_per_player = true`
- Tab-delimited → grouped: Master List → DropThat → EpicLoot
- Validate: no duplicates, biome gating correct

---

## 🏗️ Core Systems & Mods
- **Drop That** – Loot table & WL gating
- **EpicLoot** – RNG magical items
- **CLLC** – World level & scaling
- **WackyDB** – Item/recipe management
- **Therzie Suite** – Weapons/armor
- **Warpalicious** – Worldgen & locations
- **Magic Revamp/Wizardry** – Spells

---

## 📌 Active Priorities
- Refine endgame loot pools (existing assets only)
- Add coin-gated encounters (Troll event)
- Monitor roaming boss balance (Tempest Serpent, Royal Lox, Avalanche Drake, Leech Matron, etc.)
- Maintain AI → config → game pipeline
- Track mushroom mob spawn & loot balance

---

## 🔄 Recent Critical Fixes (Summary)
| Change | Impact |
|--------|--------|
| Fixed prefab IDs & missing chests | No config load errors |
| Re-balanced boss loot | Proper WL scaling |
| Reduced monster density | Lower world load |
| Restored biome-specific chest loot | Better progression |
| Integrated bounty board API | Co-op rewards |
| Validated mod creature drops | WL alignment |
| Switched WL progression to boss kills | Removes day-based gating |

---

## 🧠 AI Agent Protocol
- **Always update this file** after config changes
- Document decisions & solutions here, archive older logs in `CHANGELOG.md`
- Keep only active rules, priorities, and standards in this file
- Validate WL gating, loot balance, and mod integration before commit

---

## 🛠️ Common Commands
```bash
# Update file index
python List_Important_files.py both

# Git workflow
git status
git add .
git commit -m "Update: [module] configs"

# Validation checklist
# - WL min matches Drop That & EpicLoot
# - No duplicate entries
# - Star gating correct
# - Biome progression enforced
```

## 📈 Adjusted Pacing with Ashlands & Deep North

If **Mistlands** isn’t the final biome (you’ve added **Ashlands** + **Deep North**), then “early Mistlands” is closer to **mid‑game** rather than late endgame. That implies:

- **Tier‑1 skills** *(Run, Sailing, Weapons, Blacksmithing)* don’t need to be as slow as earlier numbers, because there are **two more biomes** after Mistlands.
- If Tier‑1 remains too slow, you risk not seeing the “fun part” of those skills until the last **10–20%** of the ~800‑hour run — which feels like “why bother?” instead of “earned power.”
- Aim for **Tier‑1 caps around early/mid Ashlands (~70–75% of total playtime)** so you get to use the payoff across two late biomes, not just one.

### Adjusted pacing goals (with Ashlands & Deep North)

| Tier | Skills | Target max level | Target biome | % of 800h | Hours to cap |
|---|---|---:|---|---:|---:|
| **T1 – Gamechangers** | Run, Sailing, Weapons, Blacksmithing | ~70 | Early **Ashlands** | 70–75% | ~560–600h |
| **T2 – Strong utilities** | Sneak, Pickaxes, Exploration, Foraging | ~70 | Late **Mistlands** | 55–60% | ~440–480h |
| **T3 – Flavor/minors** | Jump, Swim, Cooking, Farming, Ranching, Pack Horse, Tenacity, Lumberjacking, Building, Enchanting | ~70 | Early **Mistlands** | 50% | ~400h |

This spreads rewards so progression still **feels meaningful** in **Ashlands/Deep North**, not only at the very end.

### What that does to multipliers

Scale from the **baseline 1→70 time** (from micro‑tests) to the **target hours** using:

```
avg_factor = baseline_hours / target_hours
```

#### Example — Run (Tier‑1 target ~580h to L70)

- Baseline (from test, realistic uptime): **7.6 h**
- `avg_factor = 7.6 / 580 ≈ 0.0131`

Seasonal flavor (±20% around the mean):

- **Spring:** 0.0157  
- **Summer:** 0.0144  
- **Fall:** 0.0118  
- **Winter:** 0.0105  

Still very slow vs. vanilla, but faster than the 530h “early Mistlands” pacing.

#### Example — Sailing (Tier‑1, same target as Run)

If Sailing’s baseline to 70 is **~4.8 h** (test like Run):

- `avg_factor = 4.8 / 580 ≈ 0.00828`

Seasonal flavor (±20%):

- **Spring:** 0.00994  
- **Summer:** 0.00911  
- **Fall:** 0.00745  
- **Winter:** 0.00662  

**Bottom line:** With **Ashlands & Deep North**, shift T1 “payoff” **later than Mistlands but before final biome**, and let **T2/T3** cap sooner so players enjoy them throughout late game.

> Next: rebuild the **Skill → Tier → Biome → Gain Factor** table with these biome targets baked in to produce exact seasonal/global values to paste into configs.
