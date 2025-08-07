# Valheim Mods Project – AI Agent Brain (Slim Version)

## 🎯 Core Mission
Create a **RuneScape + Solo Leveling** inspired Valheim overhaul with MMO-like progression, rewarding grind, and balanced loot pacing.  
Target: ~800 hrs total, 6–12 month playthrough at 10–15 hrs/week.

---

## 📊 Progression & Skill Systems

### EpicMMO (Primary RPG Progression)
- **Max Level**: 120 | XP curve tuned for long-term growth
- **Free Points Per Level**: 2 (reduced from default 5)
- **Start Free Points**: 3 (reduced from default 5)
- **Level Experience**: 300 XP base per level
- **Experience Multiplier**: 1.048 (raised for longer progression)
- **Add Level Experience**: Enabled (adds 300 XP per level)
- **Bonus Level Points**: +2 every 5 levels, +3 at 20/40/60, +4 at 80, +5 at 85+
- **Experience Rate**: 1.0x (normal)
- **Death Penalty**: 25-50% XP loss (increased from default 5-25%)
- **Reset Cost**: 55 coins per point (increased from default 3)
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
| WL | Biome        | Days to Unlock |
|----|--------------|----------------|
| 0-1| Meadows      | 15             |
| 2-3| Black Forest | 45             |
| 3-4| Swamp        | 90             |
| 4-5| Mountains    | 180            |
| 5-6| Plains       | 300            |
| 6-7| Mistlands    | 420            |
| 7+ | Deep North / Ashlands | 540  |

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
