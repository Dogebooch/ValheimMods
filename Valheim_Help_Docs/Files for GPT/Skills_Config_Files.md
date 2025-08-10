Skill-Progression Configuration Guide
Core Configuration Files
Skill(s)	Config File & Key Settings
Run, Jump, Sneak, Swim	shudnal.Seasons/Default settings/Custom stats.json – seasonal stat blocks boost skill gain/levels (m_raiseSkills, m_skillLevels) for Run, Jump, Sneak, and Swim during Spring/Summer and modify WoodCutting, Fishing, Pickaxes in Fall/Winter{line_range_start=13 line_range_end=58 path=Valheim/profiles/Dogeheim_Player/BepInEx/config/shudnal.Seasons/Default settings/Custom stats.json git_url="https://github.com/Dogebooch/ValheimMods/blob/main/Valheim/profiles/Dogeheim_Player/BepInEx/config/shudnal.Seasons/Default settings/Custom stats.json#L13-L58"}{line_range_start=80 line_range_end=118 path=Valheim/profiles/Dogeheim_Player/BepInEx/config/shudnal.Seasons/Default settings/Custom stats.json git_url="https://github.com/Dogebooch/ValheimMods/blob/main/Valheim/profiles/Dogeheim_Player/BepInEx/config/shudnal.Seasons/Default settings/Custom stats.json#L80-L118"}
Sneak, Swim, Weapon Skills	org.bepinex.plugins.smartskills.cfg – adds XP recovery bonuses, weapon-skill catch-up, and bespoke swim/sneak adjustments (Swimming skill loss, Swimming experience bonus, Sneak bonus experience)
Sailing	org.bepinex.plugins.sailing.cfg – sets ship speed, required skill levels per vessel, and global XP gain/loss (Skill Experience Gain Factor, Skill Experience Loss)
Blacksmithing	org.bepinex.plugins.blacksmithing.cfg – defines crafting perks and experience parameters (Skill Experience Gain Factor, Skill Experience Loss)
Pickaxe (Mining)	org.bepinex.plugins.mining.cfg – tuning for mining damage/yield and XP (Skill Experience Gain Factor, Skill Experience Loss)
Exploration	org.bepinex.plugins.exploration.cfg – expands map radius, movement speed, and skill XP settings
Foraging	org.bepinex.plugins.foraging.cfg – controls harvest yield, respawn timers, and XP factors
Cooking	org.bepinex.plugins.cooking.cfg – improves food stats, crafting bonuses, and XP gain/loss for the cooking skill
Farming	org.bepinex.plugins.farming.cfg – governs crop growth, harvest radii, and skill XP settings
Ranching	org.bepinex.plugins.ranching.cfg – adjusts tame drops, taming speed, and ranching XP factors
Pack Horse	org.bepinex.plugins.packhorse.cfg – custom “carry weight” skill with XP rate and death penalty settings
Tenacity	org.bepinex.plugins.tenacity.cfg – resilience skill affecting XP rate, effect strength, and loss on death
Lumberjacking	org.bepinex.plugins.lumberjacking.cfg – modifies tree yield, forest movement, and XP factors
Building	org.bepinex.plugins.building.cfg – enhances structural support, stamina usage, and building XP gain/loss
Enchantments	ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg – sets enchantment safety rules and skill scaling (AdditionalEnchantmentChancePerLevel, Skill gain factor, Skill loss)
Configuration Interactions

    Seasonal Buffs + Plugin XP Tweaks
    Run, Jump, Swim, Sneak, WoodCutting, Pickaxes: Season-based boosts (skill raises/levels) apply on top of other plugins. For example, Smart Skills’ swimming and sneak bonuses stack with seasonal multipliers, while Mining and Lumberjacking benefit from Fall/Winter skill raises.

    Sailing vs. Exploration
    Sailing’s Exploration Radius Factor adds an on-ship bonus that complements the base exploration skill radius from org.bepinex.plugins.exploration.cfg; both effects combine rather than override one another.

    Weapon Skills
    Smart Skills’ “catch-up” mechanic increases XP gain for any weapon skill lagging behind the player’s highest weapon skill, without altering per-weapon configs.

    Enchantment System Overrides
    kg.ValheimEnchantmentSystem.cfg provides global enchantment settings. YAML files inside ValheimEnchantmentSystem/AdditionalOverrides_* override default enchantment chances or stats if present, letting server admins layer custom tuning over base values.

    Independent Skill Mods
    Standalone configs (Blacksmithing, Farming, Ranching, Pack Horse, Tenacity, Building, etc.) each govern their own skill without cross-override—changes in one file do not replace settings in another unless they target the same underlying mechanic (rare in this pack).
