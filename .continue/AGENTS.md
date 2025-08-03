# Valheim Mods Project - AI Agent Brain

## 🎯 Core Mission
Build a **RuneScape + Solo Leveling** inspired Valheim experience with RPG/MMO progression, rewarding grind, and exploration.

## 📊 Current Skill Progression Factors

### **EpicMMO System (Primary RPG Progression)**
- **Max Level**: 120 (raised from 90)
- **Free Points Per Level**: 2 (reduced from default 5)
- **Start Free Points**: 3 (reduced from default 5)
- **Level Experience**: 300 XP base per level
- **Experience Multiplier**: 1.048 (raised for longer progression)
- **Add Level Experience**: Enabled (adds 300 XP per level)
- **Bonus Level Points**: +5 every 5 levels up to 120
- **Experience Rate**: 1.0x (normal)
- **Death Penalty**: 25-50% XP loss (increased from default 5-25%)
- **Reset Cost**: 55 coins per point (increased from default 3)
- **Tuning Note**: XP multiplier and world-level schedule may be fine-tuned later to keep progression within the 13–18 month target.

### **Attribute Scaling (Per Point)**
- **Strength**: +0.3 damage, +4 weight, +0.3 block stamina, +0.5 crit damage
- **Dexterity**: +0.3 attack speed, +0.3 attack stamina, +0.3 movement stamina
- **Endurance**: +1 stamina, +0.5 stamina regen, +0.3 physical armor
- **Intelligence**: +0.3 magic attack, +0.3 eitr regen, +1 eitr
- **Vigour**: +1 health, +0.5 health regen, +0.3 magic armor
- **Specializing**: +0.2% crit chance, +0.4 mining speed, +10 building health, +0.4 tree cutting

### **SmartSkills (Vanilla Skill Enhancement)**
- **Skill Recovery Bonus**: 50% XP boost until reaching previous highest level
- **Weapon Catch-up Bonus**: 50% XP boost for weapon skills until caught up to highest weapon skill
- **Swimming**: 100% XP bonus, no death penalty
- **Sneak**: +10% XP on backstab, +25% backstab damage at level 100
- **Blood Magic**: 33% XP sharing between shield caster and attacker

### **Vanilla Skill Experience Factors**
- **Farming**: 1.25x (boosted - most rewarding)
- **Cooking**: 0.6x (reduced)
- **Ranching**: 0.6x (reduced)
- **Exploration**: 0.6x (reduced)
- **Building**: 0.5x (reduced)
- **Blacksmithing**: 0.5x (reduced)
- **Foraging**: 0.5x (reduced)
- **Lumberjacking**: 0.5x (reduced)
- **Mining**: 0.5x (reduced)
- **Sailing**: 0.5x (reduced)
- **Pack Horse**: 0.5x (reduced)
- **Tenacity**: 0.4x (reduced)
- **Warfare Skills**: 1.0x (normal)
- **Enchantment System**: 1.0x (normal)

## 🏗️ Project Architecture

### **Core Systems**
- **JewelHeim-RelicHeim Modpack** - Primary content foundation
- **EpicLoot** - RNG magical item generation (Magic/Rare/Legendary/Mythic)
- **Drop That** - Loot table control & world level gating
- **CLLC** - World level & star scaling, elite affixes
- **WackyDB** - Item/recipe database management
- **WackyMMO** - Skill progression & ability unlocks

### **Content Mods**
- **Therzie Suite**: Warfare, Armory, Monstrum (weapons/armor)
- **Warpalicious**: World generation & locations
- **Smoothbrain**: QoL & gameplay enhancements
- **Magic Revamp & Wizardry**: Expanded spell systems

## 🎮 Game Design Philosophy

### **Progression Flow**
1. **Early (WL 0-2)**: Basic items + EpicLoot Magic/Rare drops
2. **Mid (WL 3-5)**: RelicHeim set items (crafted) + EpicLoot Legendary
3. **Late (WL 6+)**: EpicLoot Mythic + T5 Legendaries (boss-only)

### **World Level Gating**
- **WL 0-1** → Meadows | **WL 2-3** → Black Forest | **WL 3-4** → Swamp
- **WL 4-5** → Mountains | **WL 5-6** → Plains | **WL 6-7** → Mistlands
- **WL 7+** → Deep North/Ashlands
- **Age-Based WL progression**: WL1=15d, WL2=45d, WL3=90d, WL4=180d, WL5=300d, WL6=420d, WL7=540d

### **Loot Systems Integration**

| System | RNG? | Source | Purpose | Affixes |
|--------|------|--------|---------|---------|
| **EpicLoot Magic** | ✅ | Random drops | RNG progression | 1 affix |
| **EpicLoot Rare** | ✅ | Random drops | RNG progression | 2 affixes |
| **EpicLoot Legendary** | ✅ | Random drops | High-tier RNG | 3+ affixes |
| **EpicLoot Mythic** | ✅ | Random drops | Top-tier RNG | Special effects |
| **RelicHeim Sets** | ❌ | Crafted | Set bonuses | Static stats |
| **T5 Legendaries** | ❌ | Boss kills | Best-in-slot | Static, boss-only |

## 📁 Critical File Structure

### **Configuration Directories**
```
Valheim/profiles/Dogeheim_Player/BepInEx/config/
├── EpicLoot/patches/RelicHeimPatches/
│   ├── Legendaries_SetsLegendary_RelicHeim.json
│   └── Legendaries_SetsMythic_RelicHeim.json
├── wackysDatabase/
│   ├── Effects/SE_SetEffect_*.yml
│   ├── Items/
│   └── Recipes/
└── DropThat/
```

### **Project Management**
- `important_files_updated.txt` - Enhanced file index with metadata
- `List_Important_files.py` - Unified index generator
- `.gitignore` - Selective file inclusion (configs/docs only)

## ⚙️ Configuration Standards

### **Drop That Rules**
- All chase loot: `drop_one_per_player = true`
- Star gating: `creature_stars_required = 2` (Magic/Rare), `= 3` (T4)
- Scaling: `scale_by_level = true`
- **CRITICAL**: `world_level_min` must match EpicLoot configs

### **EpicLoot Rules**
- Effect types: `"Magic" | "Rare" | "Legendary" | "None"`
- Use `GuaranteedMagicEffects` for affix pools
- Legendary items: fixed UniqueIDs, predefined stats
- **CRITICAL**: `world_level_min` must equal Drop That's

### **Spawn That Rules**
- Global `SpawnFrequencyMultiplier` tuned to `0.95` across world and raid spawners for a slight overall spawn reduction

### **Data Formatting**
- **Tab-delimited** for spreadsheets
- **Grouped order**: Master List → DropThat Config → EpicLoot Config
- **Consistent naming** across all configs
- **Proactive validation** for biome gating errors

## 🎯 AI Work Preferences

### **Balance Philosophy**
- **No early BiS drops** - maintain proper gating
- **Consistent progression** across biomes
- **Moderate creativity** for stats/names, **strict** on formatting
- **Proactive validation** for misclassification

### **Automation Goals**
- **Minimize repetitive edits**
- **AI-assisted config generation**
- **Keep Drop That/EpicLoot/CLLC consistent**
- **Avoid duplicate loot entries**

### **Output Standards**
- **Tab-delimited** for spreadsheets
- **Grouped configurations** in consistent order
- **Master loot list** as single source of truth
- **Cross-reference validation** between mods

## 📚 Problems Solved & Fixes Applied

### **File Organization & Indexing**
- **Problem**: Large number of files (2,979+) needed proper organization
- **Solution**: Created unified index generator with TYPE/IMPORTANCE_TAGS classification
- **Result**: Comprehensive file index with enhanced metadata

### **Git Repository Management**
- **Problem**: "Too many active changes" and large binary files
- **Solution**: Refined `.gitignore` for selective inclusion, reset repository
- **Result**: Clean repository with only important configs/docs

### **Legendary Systems Confusion**
- **Problem**: Unclear differences between EpicLoot, RelicHeim sets, T5 legendaries
- **Solution**: Created comprehensive clarification table and progression flow
- **Result**: Clear understanding of 4 distinct legendary systems

### **EpicMMO Dexterity Soft Cap**
- **Problem**: Added Dexterity stamina soft cap entries were not recognized by EpicMMO System
- **Solution**: Removed unsupported soft cap settings, keeping base stamina bonuses only
- **Result**: Prevents non-functional config lines and maintains balanced stamina progression

### **Biome-Specific Treasure Loot**
- **Problem**: Generic MagicMaterials set used across all chests limited biome-based progression
- **Solution**: Replaced chest loot with biome-specific sets and boosted legendary/mythic weights for late biomes
- **Result**: Higher-tier chests now provide proportionally better materials

### **Treasure Chest Loot Rolls**
- **Problem**: Some treasure chests could roll zero items.
- **Solution**: Updated drop tables to remove zero-roll chance, ensuring a minimum of one item.
- **Result**: Treasure chests now always yield at least one piece of loot.

### **Mod Creature Drop World Levels**
- **Problem**: Newly added modded creature loot tables were not yet reviewed for biome/world-level balance.
- **Solution**: Audited each mod creature drop list to ensure materials match the creature's intended biome (e.g., Fox_TW drops early-game LeatherScraps while CorruptedDvergerMage_TW yields Mistlands BlackCore/Softtissue).
- **Result**: Mod creature loot tables align with world-level progression.

### **VNEI Load Performance**
- **Problem**: VNEI UI loaded slowly with unknown items and recipes visible
- **Solution**: Enabled "Show Only Known" (server-forced) in com.maxsch.valheim.vnei.cfg
- **Result**: Faster VNEI load times
- 
### **Loot Generation Validation**
- **Problem**: Duplicate `(PrefabID, ItemPrefab)` pairs could stack drop probabilities in generated configs
- **Solution**: Added validation in `generate_loot_configs.py` to detect duplicates and abort generation
- **Result**: Prevents accidental probability stacking during loot config creation

### **AxeSilver Prefab Error**
- **Problem**: More World Locations loot lists referenced `AxeSilver` causing prefab errors.
- **Solution**: Replaced with `AxeSilver_TW` to match modded prefab.
- **Result**: AxeSilver loot lists load without errors.

## 🚨 Current Pain Points

### **Technical Challenges**
- Keeping loot scaling consistent across 100s of entries
- Preventing early-tier loot from persisting into late-game
- Managing multiple mod item lists without missing prefabs

### **Current Priorities**
- Refine endgame loot pool using existing assets
- Balance magic vs static loot drop rates
- Ensure boss-locked BiS items feel worth the grind
- Streamline AI → config → game pipeline
- Monitor increased Mushroom Monster spawn rates across biomes for balance
- Balanced Mushroom boss drops: WL-scaled coins guaranteed, portal key guaranteed, and rare (~5%/1% overall via 2.5%/0.5% per-roll) gold/silver statues per player
- Maintain progression-based loot tables for Mushroom Monsters (bosses excluded; rare mushrooms drop-one-per-player)

## 💡 Loot System Ideas / TODO
- Introduce boss-specific unique drops with rare rates and signature effects.
- Expand RelicHeim armor sets with scalable set bonuses tied to world levels.
- Implement tiered loot tables that unlock stronger rewards at higher world levels.
- Add a boss currency or token system for deterministic reward exchanges.
- Highlight rare drops and track boss killcounts for social/cosmetic rewards.
- Provide independent loot rolls for group boss fights to incentivize co-op play.
- Run rotating boss events with temporary loot modifiers or event-exclusive items.
- Drop relic fragments that players combine into upgraded or legendary versions.
- Added Ashlands Stone Golem spawning near lava in clear weather with high fire resistance, CLLC scaling, and world-level gated loot (Flametal/Obsidian/MagmaCore) plus rare XP orbs.

## 🛠️ Common Tasks & Commands

### **File Management**
```bash
# Generate/update file index
python List_Important_files.py both

# Check Git status
git status
git add .
git commit -m "Add/Update: [specific mod] configuration files"
```

### **Validation Checklist**
- [ ] `world_level_min` matches between Drop That & EpicLoot
- [ ] No duplicate loot entries across mods
- [ ] Proper star gating for affix tiers
- [ ] Biome progression follows WL guidelines
- [ ] File sizes reasonable (no large binaries)

## 🔧 Troubleshooting Quick Reference

### **Common Issues**
1. **Large repo size** → Check for binary files, update `.gitignore`
2. **Missing configs** → Verify file paths, mod installations
3. **Mod conflicts** → Check load order, compatibility
4. **Loot scaling issues** → Verify WL gating across all mods
5. **Duplicate entries** → Cross-reference all loot tables

### **Recovery Steps**
1. **Reset repo**: `git reset --hard` if needed
2. **Regenerate index**: `python List_Important_files.py both`
3. **Clean files**: `git clean`, update `.gitignore`
4. **Validate loot**: Cross-reference Drop That & EpicLoot configs

## 🧠 AI Agent Memory Management

### **CRITICAL: Use AGENTS.md as Working Memory**
- **ALWAYS update AGENTS.md** after making any significant changes
- **Document decisions, solutions, and learnings** in relevant sections
- **Add new pain points, priorities, or solutions** as they arise
- **Update file paths, configurations, or procedures** when changed
- **Record successful troubleshooting steps** for future reference

### **Memory Update Protocol**
1. **After each change**: Update relevant section in AGENTS.md
2. **New problems solved**: Add to "Problems Solved and Fixes Applied"
3. **New pain points**: Add to "Current Pain Points & Priorities"
4. **Configuration changes**: Update "Configuration Standards"
5. **File structure changes**: Update "Critical File Structure"
6. **New learnings**: Add to appropriate sections

### **Benefits of Memory Management**
- **Reduces token usage** by avoiding repeated explanations
- **Maintains continuity** across AI sessions
- **Builds institutional knowledge** over time
- **Prevents duplicate work** and repeated mistakes
- **Enables faster problem-solving** with historical context

## 🎯 Key Decision Framework

### **When Making Changes**
1. **Check biome progression** - ensure proper WL gating
2. **Validate consistency** - Drop That ↔ EpicLoot ↔ CLLC
3. **Consider balance** - no early BiS, maintain progression
4. **Document changes** - update relevant READMEs AND AGENTS.md
5. **Test in isolation** - before applying to main configs
6. **Update working memory** - record learnings in AGENTS.md

### **File Inclusion Rules**
- **✅ Include**: `.cfg`, `.json`, `.yml`, `.md`, `.txt`, `.cs`, `.lua`
- **❌ Exclude**: `.dll`, `.exe`, `.png`, `.mp3`, large data files
- **🎯 Priority**: Configuration files, documentation, metadata

---

**🎯 Remember**: This is a **comprehensive Valheim modding reference** focused on JewelHeim-RelicHeim. Every change impacts mod compatibility, user experience, and maintainability. **Progression balance is paramount**. 