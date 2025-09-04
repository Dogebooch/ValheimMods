# Changelog

## Backpack System Consolidation

- **EpicLoot Backpack Consolidation**: Consolidated redundant EpicLoot material storage backpacks:
  - **Kept**: "EpicLoot Backpack" (6x4 → 7x4 upgrade path) - Primary storage for EpicLoot materials
  - **Removed**: "Andvaranaut Backpack" (5x2 → 5x3 upgrade path) - Redundant smaller backpack
  - **Benefits**: Eliminated confusion between two identical-purpose backpacks, streamlined EpicLoot material storage
  - **Configuration**: Updated `Backpacks.MajesticEpicLoot.yml` and `Detalhes.ItemRequiresSkillLevel.yml` in both main and Dogeheim configs
  - **Impact**: Single, larger EpicLoot backpack provides better storage efficiency and clearer progression

- **General Backpack Disabling**: Disabled all general-purpose backpacks except EpicLoot and Mining backpacks:
  - **Disabled**: Explorers, Simple, Foraging, Treasures, Troll, Food, Trophy, Scroll, Ammo, Wishbone backpacks
  - **Kept**: EpicLoot Backpack (EpicLoot materials) and Mining Backpack (ores/metals)
  - **Benefits**: Streamlined backpack system, reduced redundancy, focused on specialized storage needs
  - **Configuration**: Updated `Backpacks.Majestic.yml` in both main and Dogeheim configs with `disabled: true`
  - **Impact**: Cleaner progression system with two focused, specialized backpacks

- **Complete Backpack Disabling**: Disabled all craftable backpacks for clean gameplay:
  - **Disabled**: All backpacks including EpicLoot Backpack and Mining Backpack
  - **Kept**: Backpacks mod itself (for potential future use or other mod integration)
  - **Benefits**: Eliminates "weird mechanic" feeling, cleaner vanilla-like experience
  - **Configuration**: Updated all backpack configs with `disabled: true` in both main and Dogeheim configs
  - **Impact**: Players use standard inventory management without specialized storage containers

- **Final Backpack Status**: All 12 backpacks completely disabled:
  - **EpicLoot Backpack**: Disabled (EpicLoot materials)
  - **Mining Backpack**: Disabled (ores/metals with weight reduction)
  - **General Backpacks**: All 10 disabled (Explorers, Simple, Foraging, Treasures, Troll, Food, Trophy, Scroll, Ammo, Wishbone)
  - **Result**: Clean, vanilla-like gameplay with no specialized storage containers
  - **Mod Status**: Backpacks mod remains active for potential future use or mod integration

## Drop-Only Updates

- Added WeaponAdditions items as drop-only with minimal WackyDB overrides:
  - BWA_GiantAxe — Jotunn — 2% — 2 items
  - BWA_GiantCleaver — Jotunn — 2% — 2 items
  - BWA_giantMace — Jotunn — 2% — 2 items
  - BWA_ObsidianGreatsword — Stone Golem — 0.2% — 1 item
  - BWA_ObsidianBuckler — Stone Golem — 0.2% — 1 item

- Recipes disabled for all five items in `wackysDatabase/Recipes/_RelicHeimWDB2.0/zOther/WeaponAdditions/`.
- Added minimal item overrides for gold names and tooltips in `wackysDatabase/Items/_RelicHeimWDB2.0/zOther/WeaponAdditions/`.
- Configured Drop That entries in:
  - `drop_that.character_drop.Bosses.cfg` (Jotunn drops)
  - `drop_that.character_drop.zBase.cfg` (StoneGolem drops)


