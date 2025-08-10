Combat‑Related Configuration Overview

This repository’s Valheim mod pack stores most tuning knobs under
Valheim/profiles/Dogeheim_Player/BepInEx/config/.
Below is a catalogue of files that influence buffs, skill progression, or combat‑centric statistics, grouped by system.
1. Player Attribute & Skill Systems
File	Purpose
WackyMole.EpicMMOSystem.cfg	Defines the custom RPG system: level caps, XP gains/losses, and per‑attribute bonuses (e.g., Strength adds carry weight and crit damage; Dexterity affects swing speed, stamina cost, etc.).
org.bepinex.plugins.smartskills.cfg	Enhances vanilla skills: catch‑up XP, swimming/sneak modifiers, blood‑magic sharing, and sneak backstab bonuses.
org.bepinex.plugins.tenacity.cfg	Controls XP gain, power scaling, and death‑loss for the Tenacity skill.
org.bepinex.plugins.passivepowers.cfg	Manages active & passive boss powers: how many can run simultaneously, their durations, cooldowns, and specific effect strings per boss (movement speed, elemental resistances, health regen, etc.).
2. Enchantment System (WES)

Directory: Valheim/profiles/Dogeheim_Player/BepInEx/config/ValheimEnchantmentSystem/
File	Purpose
kg.ValheimEnchantmentSystem.cfg	General plugin settings, visuals, notification behaviour.
EnchantmentStats_Armor.yml	Base armor percent bonuses per enchant level.
EnchantmentStats_Weapons.yml	Base weapon damage percent bonuses per enchant level.
EnchantmentChancesV2.yml	Rarity distributions for successful enchant rolls.
EnchantmentReqs.yml & AdditionalEnchantmentReqs/*.yml	Which items are eligible for enchanting and any custom requirements.
AdditionalOverrides_EnchantmentStats/*	Per‑item stat overrides (e.g., Axes_Chop_Upgrades.yml, Pickaxes_Pickaxe_Upgrades.yml, Shields_Upgrades.yml) that replace the generic stats above.
AdditionalOverrides_EnchantmentChances/*	Alters chance tables for specific gear classes (e.g., Shields_Chances.yml).
ScrollRecipes.cfg	Crafting requirements for enchant scrolls.
3. WackyDB – Item & Effect Definitions

Directory: Valheim/profiles/Dogeheim_Player/BepInEx/config/wackysDatabase/
Subdirectory	Content
Effects/	Status‑effect YAMLs (SE_*) used by set bonuses, potions, belts, etc. Parameters cover stamina/health regen, speed modifiers, skill level boosts, carry‑weight changes, and more.
Items/	Hundreds of YAML files describing weapons, armor, belts, staves, trophies, etc., including their base damage, resistances, attachable effects (often referencing entries in Effects/).
Pieces/ & Pickables/	Building piece stats or lootable object properties that can influence combat indirectly (e.g., traps, explosive barrels).
Recipes/	Crafting and upgrade costs tied to the above items, affecting when players access certain power spikes.
4. Potions & Consumable Buffs
File	Purpose
com.odinplus.potionsplus.cfg	Configures Alchemy skill, potion effect durations/ranges (e.g., “Brew of Cunning Toxicity”), and item crafting settings. Many potions grant temporary movement, stamina, or damage buffs.
wackysDatabase/Effects/SE_Potion_*.yml	Actual status‑effect definitions applied by PotionsPlus and other consumables (e.g., SE_Potion_hasty.yml sets +15% speed and Run skill bonus for 10 minutes).
5. Creature & World Combat Balancing
File	Purpose
org.bepinex.plugins.creaturelevelcontrol.cfg	Global difficulty: health/damage multipliers, star scaling, multiplayer scaling, affix/infusion toggles, and respawn timers.
CreatureConfig_BiomeIncrease.yml	Adds biome‑based affix/infusion chances and damage multipliers (e.g., bow damage reduction in late biomes).
CreatureConfig_Bosses.yml	Per‑boss tuning: base HP/damage, element resistances, movement/attack speed, affix chances, etc.
CreatureConfig_Creatures.yml, CreatureConfig_Monstrum.yml, CreatureConfig_Wizardry.yml	Individual creature/boss overrides for HP, damage, affixes, biomes, and tame bonuses.
CreatureConfig_BiomeIncrease.yml (Therzie sections)	Additional scaling for modded creatures in each biome.
6. Miscellaneous Combat‑Related Configs

    Shawesome.Shawesomes_Divine_Armaments.cfg, Therzie.Warfare.cfg, Therzie.Wizardry.cfg, etc.: Crafting/upgrade costs for weapon packs; stats typically defined via WackyDB but these files gate access and upgrade progression.

    wackysDatabase/Effects/SE_SetEffect_ files*: Set bonus buffs for belts, food jerky, or armor sets (carry‑weight boosts, speed modifiers, resistances).

    _RelicHeimFiles/Drop,Spawn_That/*: DropThat/SpawnThat configs gating loot and spawns; while not direct buffs, they govern access to gear providing combat stats.

Configuration Interactions & Overrides

    WackyDB Items ↔ WES Enchantments

        WackyDB establishes base stats for every weapon/armor.

        Enchantment YAMLs (EnchantmentStats_* and per‑item overrides) apply multiplicative bonuses to those base stats.

        AdditionalOverrides_EnchantmentStats supersede the generic enchant tables for listed items; they are evaluated after the base item config loads.

    WackyDB Items ↔ WackyDB Effects

        Many item YAMLs reference SE_* effect entries to grant buffs when equipped or consumed.

        Adjusting or removing a set effect in Effects/ immediately propagates to every item referencing it.

    PotionsPlus ↔ WackyDB Effects

        PotionsPlus determines crafting, durations, and ranges; the actual buff (speed, skill boost, etc.) is defined in the corresponding SE_Potion_* file.

        Changing one without the other can desync tooltips vs. actual effect.

    EpicMMO System ↔ SmartSkills/Tenacity

        EpicMMO supplies attribute point bonuses (damage, stamina, etc.).

        SmartSkills handles vanilla skill XP and special bonuses; Tenacity adds another skill line.

        All bonuses are additive/multiplicative on top of each other—no explicit overrides, but stacking can produce large totals.

    Passive Powers ↔ EpicMMO and Item Buffs

        Boss powers act like long‑duration status effects that stack with attribute bonuses and item effects.

        When an active power triggers, Passive Powers temporarily disables its passive component (Power loss duration).

    Creature Level & Loot Control (CLLC) Overrides

        Global config (creaturelevelcontrol.cfg) sets baseline multipliers.

        Use creature configuration yaml = On causes any matching entries in CreatureConfig_*.yml to override those values for specific creatures or biomes.

        Affixes/infusions from CLLC can further modify damage/defense after item and player buffs are calculated.

    Biome/Boss Progression

        CreatureConfig_BiomeIncrease.yml and DropThat/SpawnThat configs gate enemy strength and loot by boss kills. These gates determine when players can realistically acquire higher‑tier items or set bonuses, indirectly controlling buff access.
