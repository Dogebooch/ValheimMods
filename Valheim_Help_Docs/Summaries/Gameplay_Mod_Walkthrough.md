# JewelHeim-RelicHeim Gameplay Guide

This guide explains how to play the JewelHeim-RelicHeim mod pack.  It covers the major gameplay mods, where to find new items and practical tips for surviving Valheim's harsher world.

## Getting Started
- **Install the mod pack** with a mod manager or by copying the contents of this repository to your Valheim profile.
- Many systems are gated by **world level (WL)**.  Worlds begin at WL0 and rise over time; higher WL unlocks harder biomes and better drops.
- Read each section below for directions on using the included mods.

## Core Progression Mods
### Wacky EpicMMO System
The primary RPG layer.  Gain experience from combat and activities to level up.
- Press **`K`** (default) to open the MMO menu and allocate attribute points.
- Attributes grant bonuses such as Strength for melee damage and Vigour for health regeneration.
- Death causes 25–50% XP loss; carry **XP potions** or craft a **ResetTrophy** to reclaim points.
- Grouping with the **Smoothbrain Groups** mod shares XP with party members.

### SmartSkills
Enhances the vanilla skill system.
- Lost skill levels regain 50% faster until your previous peak is reached.
- Weapon skills below your highest weapon skill receive a 50% catch‑up bonus.
- Swimming and Sneak have additional XP bonuses.

### EpicLoot
Adds Diablo‑style magic items.
- Monsters and chests drop items in tiers: Magic, Rare, Legendary and Mythic.
- Higher star creatures roll better affixes; Mythic items appear only at world level 6+.
- Use the **Enchantment Table** to reroll affixes or upgrade gear.

### Creature Level & Loot Control (CLLC) and Drop That
- CLLC scales creature stars and applies elite affixes.
- Drop That controls loot tables and gates items behind world level and creature stars.
- Always match `world_level_min` between Drop That and EpicLoot when creating new drops.

### WackyDB Item & Recipe Database
Centralises custom items, recipes and set bonuses.
- Look in the crafting menu for **RelicHeim set pieces** and biome‑themed feasts.
- Many recipes require materials dropped by roaming bosses or high WL creatures.

## Enchanting & Gear Upgrades
EpicLoot and the Valheim Enchantment System let you customise equipment.
- **Disenchant** unwanted drops at the table to recover **Magic Dust**, runes and upgrade materials.
- **Augment** slots to add new affixes; higher table tiers unlock more options.
- Use **Enchanted Keys** from Haldor to open special chests filled with scrolls and crafting reagents.
- Upgrade the table itself to improve success chances and batch‑convert junk trophies into enchanting mats.
- Enchanted items keep their durability percentage, so repair before enchanting to avoid wasting resources.

## Smoothbrain Skill Mods
Each skill module expands a survival activity.  Enable/disable in BepInEx configs if desired.
- **Farming** – Tends crops automatically and adds new plants.
- **Cooking** – Introduces multi‑step cooking and jerky recipes; watch for burn timers.
- **Blacksmithing** – Craft components and refine metals via a dedicated anvil.
- **Building** – Adds advanced snap points and support indicators.
- **Foraging, Lumberjacking, Mining** – Grant passive bonuses and XP as you harvest resources.
- **Backpacks & PackHorse** – Craft backpacks and mounts to increase carry capacity.
- **PassivePowers** – Unlock passive abilities as you level vanilla skills.
- **TargetPortal & Sailing/SailingSpeed** – Upgrade portal usage and ship handling.

## Farming Guide
Farming underpins late‑game self‑sufficiency and requires deliberate leveling to unlock its strongest perks.

### Leveling Path
- **Levels 1‑20:** Plant carrots and turnips in their native biomes to learn basics. Sleep between plantings to accelerate growth.
- **Levels 21‑40:** Expand plots and replant immediately after harvest. Multi‑planting/harvesting increases every 10 levels.
- **Levels 41‑70:** Dedicated farming sessions become essential. Larger harvest radii and stamina reductions make mass farming viable.
- **Level 80+:** Biome restrictions lift (via PlantEverything `EnforceBiomes`), letting you consolidate crops in one safe hub.

### Efficiency Tips
- Keep fields near portals and use fenced grids to maximize space.
- Sleep or pass time between cycles to advance growth timers.
- Replant immediately for continuous XP; every plant/harvest action grants experience.

### Power Spikes
- **L40:** Harvest/plant four crops at a time with ~40% less stamina.
- **L70:** Growth speed hits ~2.4× and yields ~1.7×, making farming a major resource source.
- **L100:** Zero stamina cost and wide harvest radius enable massive automated fields.

## Content & World Mods
- **Therzie Warfare, Armory and Monstrum** – Large collections of weapons, armours and enemies.  Craft items at new stations such as the **Warfare Forge**.
- **Therzie Wizardry** and **Magic Revamp** – Adds staffs, spells and Eitr‑based combat.  Equip wands and cast from a dedicated hotbar.
- **Warpalicious Location Packs** – New dungeons, ruins and world events scattered through each biome.  Explore to find custom chests and bosses.
- **Adventure Backpacks** – Craftable backpacks with upgrade slots for weight reduction and utilities.
- **Seasons** – Dynamic seasonal changes affecting temperature and crops.
- **Traders Extended** – Multiple wandering traders with expanded inventories.

## Roaming Bosses & Events
Unique world bosses appear under specific conditions.  Prepare before hunting them.
- **Tempest Neck** – Spawns on coastlines during thunderstorms; drops **Storm Glands** and chance for Thunderstones.
- **Toll Troll** – Lurks near bridges at night; drops **Coin Sacks** and **Toll Tokens** used to unlock traders.
- **Leech Matron** – Emerges from deep swamp water after dusk; yields **Blood Sacs** for alchemy.
- **Avalanche Drake** – Circles mountain peaks in blizzards; drops **Frost Cores** and Dragon Tears.
- **Royal Lox** – Appears in plains herds during daylight; drops **Regal Hides** and linen.
- **Tempest Serpent** – Surfaces during ocean squalls; provides **Abyssal Fangs** for naval gear.
- **Weaver Queen** – Hidden in mistland nests; drops **Silk Bundles** used for advanced weaving.
- **Magma Golem** – Rises in ashlands lava pools; drops **Magma Cores** for fire weapons.
- **Frost Wyrm** – Patrols deep north blizzards; drops **Frozen Hearts** for frost enchantments.

## Loot Hunting & Exploration
Track world level and star ratings to target the best loot.
- High star (2+) creatures and elites have improved drop tables and affix rolls.
- Warpalicious dungeons hide locked chests; carry keys or bombs to reach their rewards.
- Seasonal events and storms increase roaming boss spawns—follow thunder or blizzards for rare drops.
- Use **Adventure Backpacks** or pack animals to haul treasures and crafting mats home.

## Questing & Contracts
Mods like **Biome Lords Quest** and **Traders Extended** provide structured goals.
- Check quest boards in settlements or speak with Haldor for contracts.
- Objectives often send you to specific biomes or bosses and reward coins, XP and reputation.
- **Toll Tokens** from Toll Trolls unlock trader quest lines and rare stock.
- Quests scale with world level; revisit them as the world advances for better loot.

## Item Sources
| Item | Source |
|------|-------|
| Storm Gland | Tempest Neck (Meadows thunderstorms) |
| Toll Token | Toll Troll (Bridge crossings at night) |
| Blood Sac | Leech Matron (Swamps after dusk) |
| Frost Core | Avalanche Drake (Mountains during blizzards) |
| Regal Hide | Royal Lox (Plains herds, daytime) |
| Abyssal Fang | Tempest Serpent (Ocean squalls) |
| Silk Bundle | Weaver Queen (Mistlands nests) |
| Magma Core | Magma Golem (Ashlands lava flows) |
| Frozen Heart | Frost Wyrm (Deep North blizzards) |

RelicHeim crafting uses these materials to forge end‑game gear and feast recipes for each biome.

## Boss Trophy Uses
Once the Forsaken altars are activated, extra boss trophies still provide value:
- **Enchanting reagents** – Break trophies down at the Enchanting Table to produce Novus Reagent and other crafting materials.
- **XP orbs and potions** – Wacky EpicMMO repurposes trophies, letting you grind bosses for ingredients used in XP orbs or experience potions.
- **Reset tokens** – Spare trophies can become Reset Trophies, rare items the MMO system accepts in place of coins when refunding attribute points.

## Tips
- Track world level progression and tackle biomes in order.
- Carry repair materials; many mods increase durability loss.
- Use backpacks and mounts to manage the reduced base carry weight.
- Seasonal storms can spawn roaming bosses—watch the skies.
- Keep `important_files_updated.txt` and configs under version control when tweaking settings.
- Disenchant duplicate drops for dust instead of selling them; enchant only fully repaired gear.
- Upgrade the Enchanting Table early to improve success chances and unlock mass conversion recipes.
- Turn in quests while rested for a small bonus to the XP rewards.
- Party members share MMO XP, so group up for difficult hunts and faster progression.

Enjoy exploring JewelHeim‑RelicHeim!
