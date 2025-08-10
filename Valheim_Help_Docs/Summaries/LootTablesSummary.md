Loot Table Configuration Overview

This repository aggregates multiple Valheim mods that collaborate to control drops from creatures, bosses, and chests. The main configuration files that affect loot tables are summarized below.
1. Monster Drop Configurations
File	Purpose
Valheim/profiles/Dogeheim_Player/BepInEx/config/drop_that.character_drop.cfg	Configures creature-specific drops through the Drop That mod (e.g., Leech Matron loot entries).
Valheim/profiles/Dogeheim_Player/BepInEx/config/EpicLoot/patches/RelicHeimPatches/zLootables_CreatureDrops_RelicHeim.json	Adds or modifies creature loot pools for Epic Loot by patching loottables.json.
Valheim/profiles/Dogeheim_Player/BepInEx/config/EpicLoot/patches/RelicHeimPatches/zLootables_Adjustments_RelicHeim.json	Tweaks default Epic Loot loot-table behavior for creatures (e.g., gating, weighting).
2. Boss Drop Configurations
File	Purpose
Valheim/profiles/Dogeheim_Player/BepInEx/config/EpicLoot/patches/RelicHeimPatches/zLootables_BossDrops_RelicHeim.json	High‑priority patch (Priority: 1000) that overwrites boss loot sections in Epic Loot’s loottables.json.
Valheim/profiles/Dogeheim_Player/BepInEx/config/drop_that.character_drop.cfg	Can also define boss drops (none shown in current file but it is the Drop That location for boss tweaks).
3. Chest / Treasure Configurations
File	Purpose
Valheim/profiles/Dogeheim_Player/BepInEx/config/warpalicious.More_World_Locations_LootLists.yml	Defines explicit item lists for lootable containers added by Warpalicious location packs.
Valheim/profiles/Dogeheim_Player/BepInEx/config/EpicLoot/patches/RelicHeimPatches/zLootables_TreasureLoot_RelicHeim.json	Appends Epic‑Loot treasure pools and material sets for randomized chest contents.
Valheim/profiles/Dogeheim_Player/BepInEx/config/drop_that.drop_table.cfg	Placeholder for Drop That chest/drop-table overrides (currently empty but used when custom chest tables are needed).
4. Supplementary Files
File	Purpose
Valheim/profiles/Dogeheim_Player/BepInEx/config/randyknapp.mods.epicloot.cfg	General Epic Loot plugin settings (ability bar, UI, etc.)—indirectly affects loot generation behavior.
Valheim/profiles/Dogeheim_Player/BepInEx/config/Backpacks.MajesticEpicLoot.yml	Integrates backpack mod with Epic Loot item tiers.
Valheim/profiles/Dogeheim_Player/BepInEx/config/org.bepinex.plugins.creaturelevelcontrol.cfg	Creature Level & Loot Control (CLLC): global multipliers and star-based loot adjustments; reads optional YAML configs if present.
5. How the Configurations Interact
Drop That vs. Epic Loot

    Drop That (drop_that.*.cfg) directly edits Valheim’s native drop tables for creatures and containers.

    Epic Loot patch files modify its own loottables.json to inject magical items or material sets. These patches override Epic Loot’s default loot rules, not Drop That’s.

    When both are active:

        Drop That decides what base items drop.

        Epic Loot rolls additional magic items or replaces items within its own system after base drops occur.

        Result: Epic Loot layers on top of Drop That rather than replacing it. Removing an item via Drop That does not stop Epic Loot from adding its own loot entries, but Epic Loot patches will not restore items disabled by Drop That.

Warpalicious vs. Epic Loot

    Warpalicious .cfg files control world-generation and container placement; More_World_Locations_LootLists.yml supplies fixed chest contents.

    Epic Loot’s treasure patches add dynamic loot pools that operate when an Epic Loot–managed chest is generated or opened.

    There is no direct override: Warpalicious chests drop exactly what the YAML defines, while Epic Loot’s chests (or loot rolls) use its patched loottables.json. They can coexist; a chest defined by Warpalicious will not automatically use Epic Loot’s randomization unless explicitly configured to do so.

CLLC Integration

    Creature Level & Loot Control introduces star-based multipliers and world-level gating.

    It does not define explicit item lists; instead, it multiplies quantities or adds extra drop chances after other mods (Drop That, Epic Loot) have selected items.

    Because CLLC runs at runtime across all creature drops, its multipliers apply to loot produced by both Drop That and Epic Loot, but it does not override their item selections.

Summary

    Base drops: drop_that.character_drop.cfg (and potential drop_that.drop_table.cfg) are the foundation.

    Magic & RNG layers: Epic Loot patches (zLootables_*) extend or overwrite Epic Loot’s own loot rules without replacing Drop That.

    World-location chests: Warpalicious YAML files specify fixed contents; Epic Loot patches handle randomized treasures separately.

    Scaling: CLLC mod globally scales loot output after the above configurations have run.
