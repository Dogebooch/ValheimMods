# Valheim Mods Project - AI Agent Brain

## 🎯 Core Mission
Build a **RuneScape + Solo Leveling** inspired Valheim experience with RPG/MMO progression, rewarding grind, and exploration.

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
- `Valheim_Help_Docs/master_loot_table.yml` - Single-source loot data
- `Valheim_Help_Docs/generate_loot_configs.py` - Exports Drop That & EpicLoot configs

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
- **Maintain master_loot_table.yml and generate configs automatically**

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

### **Drop Table Consolidation**
- **Problem**: Loot chances scattered across Drop That and Epic Loot configs
- **Solution**: Added master_loot_table.yml and generate_loot_configs.py exporter
- **Result**: Single source of truth for editing drop rates

### **Git Repository Management**
- **Problem**: "Too many active changes" and large binary files
- **Solution**: Refined `.gitignore` for selective inclusion, reset repository
- **Result**: Clean repository with only important configs/docs

### **Legendary Systems Confusion**
- **Problem**: Unclear differences between EpicLoot, RelicHeim sets, T5 legendaries
- **Solution**: Created comprehensive clarification table and progression flow
- **Result**: Clear understanding of 4 distinct legendary systems

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

## 💡 Loot System Ideas / TODO
- Introduce boss-specific unique drops with rare rates and signature effects.
- Expand RelicHeim armor sets with scalable set bonuses tied to world levels.
- Implement tiered loot tables that unlock stronger rewards at higher world levels.
- Add a boss currency or token system for deterministic reward exchanges.
- Highlight rare drops and track boss killcounts for social/cosmetic rewards.
- Provide independent loot rolls for group boss fights to incentivize co-op play.
- Run rotating boss events with temporary loot modifiers or event-exclusive items.
- Drop relic fragments that players combine into upgraded or legendary versions.

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