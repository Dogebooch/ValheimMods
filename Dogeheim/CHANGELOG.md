# Dogeheim Modpack Changelog

## Version 1.6.0 - Drop-Only Item System *(Testing)*

*Converting select high-tier items to drop-only rewards, removing crafting recipes to enhance progression and loot discovery.*

#### BowPlugin Items
- **BBP Crossbows (Iron/Silver)**: Removed duplicates in favor of RelicHeim/Warfare
  - Base mod disabled: `config/blacks7ar.BowPlugin.cfg` → `[Iron Crossbow]` and `[Silver Crossbow]` set to `Crafting Station = Disabled`
  - Recipes disabled: `Recipe_BBP_Crossbow_Iron.yml`, `Recipe_BBP_Crossbow_Silver.yml` set to `disabled: true`
  - Loot/Gambling removed: EpicLoot entries deleted from integration and adventure data patches
  - Enchant lists cleaned: Removed from `blacks7ar.BowPlugin.Majestic.yml`
  - Kept: RelicHeim/Warfare `CrossbowIron_TW` and `CrossbowSilver_TW` (crafting blocked via `Detalhes.ItemRequiresSkillLevel.yml`)

- **BBP_ElvenBow**: Converted to drop-only item
  - Disabled crafting via BowPlugin configuration (`Crafting Station = Disabled`)
  - Disabled WackyDB recipe (`Recipe_BBP_ElvenBow.yml` set to `disabled: true`)
  - Created WackyDB item definition with proper stats (72 Pierce + 60 Lightning damage)
  - Added as 5% drop from Dragon (Moder) with thematic tooltip
  - File created: `config/wackysDatabase/Items/_RelicHeimWDB2.0/Weapons_Bows/Item_BBP_ElvenBow.yml`
  - Drop config: `config/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.Bosses.cfg`

- **BBP_SeekerBow**: Converted to drop-only item
  - Disabled crafting via BowPlugin configuration (`Crafting Station = Disabled`)
  - Disabled WackyDB recipe (`Recipe_BBP_SeekerBow.yml` set to `disabled: true`)
  - Created WackyDB item definition with proper stats (72 Pierce + 60 Fire damage)
  - Added as 5% drop from Queen with thematic tooltip
  - File created: `config/wackysDatabase/Items/_RelicHeimWDB2.0/Weapons_Bows/Item_BBP_SeekerBow.yml`

#### Therzie Warfare Items
- **BladeYagluth_TW**: Converted to drop-only item
  - Created WackyDB item definition with A-tier stats (95 Slash + 75 Fire damage)
  - Disabled WackyDB recipe (`Recipe_BladeYagluth_TW.yml` set to `disabled: true`)
  - Reduced drop rate from 10% to 5% from Yagluth with thematic tooltip
  - Files created: `config/wackysDatabase/Items/_RelicHeimWDB2.0/zOther/Therzie/Item_BladeYagluth_TW.yml`, `Recipe_BladeYagluth_TW.yml`

- **DualAxeDemonic_TW**: Converted to drop-only item
  - Created WackyDB item definition with D-tier stats (50 Slash + 20 Chop + 25 Spirit damage)
  - Disabled WackyDB recipe (`Recipe_DualAxeDemonic_TW.yml` set to `disabled: true`)
  - Reduced drop rate from 10% to 5% from Svalt with thematic tooltip
  - Files created: `config/wackysDatabase/Items/_RelicHeimWDB2.0/zOther/Therzie/Item_DualAxeDemonic_TW.yml`, `Recipe_DualAxeDemonic_TW.yml`

- **ScytheVampiric_TW**: Converted to drop-only item
  - Disabled WackyDB recipe (`Recipe_ScytheVampiric_TW.yml` set to `disabled: true`)
  - Reduced drop rate from 10% to 5% from Vrykolathas with thematic tooltip
  - Uses existing WackyDB item definition (C-tier Swamp weapon)

- **DualScytheBloodthirst_TW**: Converted to drop-only item
  - Disabled WackyDB recipe (`Recipe_DualScytheBloodthirst_TW.yml` set to `disabled: true`)
  - Reduced drop rate from 10% to 5% from Vrykolathas with thematic tooltip
  - Uses existing WackyDB item definition (C-tier Swamp weapon)

- **LanceDvergr_TW**: Converted to drop-only item
  - Created WackyDB item definition with S-tier stats (110 Pierce + 40 Spirit damage)
  - Disabled WackyDB recipe (`Recipe_LanceDvergr_TW.yml` set to `disabled: true`)
  - Added as 5% drop from Queen with thematic tooltip
  - Files created: `config/wackysDatabase/Items/_RelicHeimWDB2.0/zOther/Therzie/Item_LanceDvergr_TW.yml`, `Recipe_LanceDvergr_TW.yml`

- **WarpikeFlametal_TW**: Converted to drop-only item
  - Created WackyDB item definition with S-tier stats (120 Pierce + 90 Fire damage)
  - Disabled WackyDB recipe (`Recipe_WarpikeFlametal_TW.yml` set to `disabled: true`)
  - Added as 5% drop from Fader with thematic tooltip
  - Files created: `config/wackysDatabase/Items/_RelicHeimWDB2.0/zOther/Therzie/Item_WarpikeFlametal_TW.yml`, `Recipe_WarpikeFlametal_TW.yml`

- **GreatbowDvergr_TW**: Converted to drop-only item
  - Disabled WackyDB recipe (`Recipe_GreatbowDvergr_TW.yml` set to `disabled: true`)
  - Added as 5% drop from Queen with thematic tooltip
  - Uses existing WackyDB item definition (S-tier Mistlands weapon)
  - File created: `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/Weapons_Bows/Recipe_GreatbowDvergr_TW.yml`

#### Fire & Ice Expansion Staffs
- **StaffVulkarion_TW**: Converted to drop-only item
  - No WackyDB item override (uses mod default stats)
  - Disabled WackyDB recipe (`Recipe_StaffVulkarion_TW.yml` set to `disabled: true`)
  - Added as 5% drop from Surtr with thematic tooltip

- **StaffSkrymir_TW**: Converted to drop-only item
  - No WackyDB item override (uses mod default stats)
  - Disabled WackyDB recipe (`Recipe_StaffSkrymir_TW.yml` set to `disabled: true`)
  - Added as 5% drop from Jotunn with thematic tooltip

- **StaffStorm_TW**: Converted to drop-only item
  - No WackyDB item override (uses mod default stats)
  - Disabled WackyDB recipe (`Recipe_StaffStorm_TW.yml` set to `disabled: true`)
  - Added as 5% drop from Sea Serpent with thematic tooltip
  - Drop config: `config/_RelicHeimFiles/Drop,Spawn_That/drop_that.character_drop.zBase.cfg`

#### RtD Staffs (Drop-Only)
- **MistlandsQuake_StaffRtD**: Converted to drop-only
  - No WackyDB item override (uses mod default stats)
  - Disabled WackyDB recipe (`Recipe_MistlandsQuake_StaffRtD.yml` set to `disabled: true`)
  - Added as 5% drop from Storm Herald with co-op 2 items
  - Files created: `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/zOther/ForsakenJVL/Recipe_MistlandsQuake_StaffRtD.yml`

- **AshlandsStaff3_RtD**: Converted to drop-only
  - No WackyDB item override (uses mod default stats)
  - Disabled WackyDB recipe (`Recipe_AshlandsStaff3_RtD.yml` set to `disabled: true`)
  - Added as 5% drop from Fader with co-op 2 items
  - Files created: `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/zOther/ForsakenJVL/Recipe_AshlandsStaff3_RtD.yml`

- **DeepNorthStaff3_RtD**: Converted to drop-only
  - No WackyDB item override (uses mod default stats)
  - Disabled WackyDB recipe (`Recipe_DeepNorthStaff3_RtD.yml` set to `disabled: true`)
  - Added as 5% drop from Jotunn with co-op 2 items
  - Files created: `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/zOther/ForsakenJVL/Recipe_DeepNorthStaff3_RtD.yml`

- **PlainsVoidstaff_RtD**: Converted to drop-only
  - No WackyDB item override (uses mod default stats)
  - Disabled WackyDB recipe (`Recipe_PlainsVoidstaff_RtD.yml` set to `disabled: true`)
  - Added as 5% drop from Yagluth with co-op 2 items
  - Files created: `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/zOther/ForsakenJVL/Recipe_PlainsVoidstaff_RtD.yml`

#### MagicBows (Drop-Only)
- **BMB_LightningBow**: Converted to drop-only
  - Disabled WackyDB recipe (`Recipe_BMB_LightningBow.yml` set to `disabled: true`)
  - Added as 3% drop from Storm Herald with co-op 2 items
  - Drops remain thematic with storm content (boss + serpent synergy)

- **BMB_SpiritBow**: Converted to drop-only
  - Disabled WackyDB recipe (`Recipe_BMB_SpiritBow.yml` set to `disabled: true`)
  - Added as 1% drop from Wraiths (single item) for rare ambient encounters

#### Documentation
- **Drop-Only Items Wiki**: Updated comprehensive guide documenting all boss-specific drops
  - New boss-specific drop section with co-op optimizations
  - Complete drop rates and item descriptions for all 17 boss weapons
  - Strategic tips for boss farming and progression
  - File updated: `Wiki/Items/Drop_Only_Items.md`

#### Drop Table Adjustments
- **Co-op Optimization**: All boss specialty drops increased from 1 to 2 items (17 items adjusted)
  - Ensures both players get rewards from rare boss-specific drops
  - Affects: CrossbowEikthyr_TW, SledgeStagbreaker_TW, BattlehammerElder_TW, WarpikeElder_TW, SledgeBonemass_TW, GreatbowModer_TW, BBP_ElvenBow, BladeYagluth_TW, FistQueen_TW, BBP_SeekerBow, KnifeViper_TW, DualAxeDemonic_TW, ScytheVampiric_TW, DualScytheBloodthirst_TW, DualHammerStormstrike_TW, StaffStorm_TW, BattleaxeDragon_TW, ClaymoreJotunn_TW
- **Drop Rate Rebalancing**: Multiple boss weapons reduced from 10% to 5% drop rates
  - BladeYagluth_TW, DualAxeDemonic_TW, ScytheVampiric_TW adjusted for consistency with new drop-only system
- **GreatbowModer_TW**: Reduced drop rate from 10% to 5% (rebalanced with BBP_ElvenBow addition)
  - Added thematic tooltip indicating drop-only status
  - Total Dragon bow drop rate remains 10% (5% + 5%)
- **FistQueen_TW**: Reduced drop rate from 10% to 5% (rebalanced with BBP_SeekerBow addition)
  - Total Queen weapon drop rate remains 10% (5% + 5%)

---

## Version 1.5.11 - Global Bow Balance, Quiver Tuning & Enchanting Integration *(Testing)*

*Reduced stacked projectile speed effects and standardized bow handling across mods; converted quivers to utility pieces with minimal armor; enabled VES scroll enchanting for MagicBows, Bow of Frey, and Wizardry items.*

#### Bow Velocity/Draw-Time Normalization
- **Global stacking reduction**:
  - BowPlugin: `Velocity Multiplier = 2` (was 3) in both main and Dogeheim configs
  - Files updated: `config/blacks7ar.BowPlugin.cfg`, `Dogeheim/Configs/blacks7ar.BowPlugin.cfg`
- **BowsBeforeHoes (bows)**:
  - Black Forest, Seeker, Surtling bows set to `Velocity = 55`, `Maximum Draw Time = 2.6`
  - Files updated: `config/Azumatt.BowsBeforeHoes.cfg`, `Dogeheim/Configs/Azumatt.BowsBeforeHoes.cfg`
- **MagicBows (bows)**:
  - Fiery, Frozen, Lightning, Spirit, Toxic bows set to `Velocity = 55`, `Maximum Draw Time = 2.4`
  - File updated: `config/blacks7ar.MagicBows.cfg`
- **Crossbows**: unchanged (retain distinct feel via higher projectile speed/instant draw)

#### Quiver Armor Tuning
- All quivers (Black Forest, Lox, OdinPlus, Seeker): `Armor = 1`, `Armor per Level = 0`
- Files updated: `config/Azumatt.BowsBeforeHoes.cfg`, `Dogeheim/Configs/Azumatt.BowsBeforeHoes.cfg`

#### Impact
- **Consistent trajectories**: Less variance between mods; reduced early overperformance from stacked velocity
- **Progression preserved**: Power now tracks bow tier, upgrades, bow skill, and arrow choice more than raw projectile speed
- **Quivers**: Serve as utility without adding significant armor

#### Valheim Enchantment System Updates
- **Bow of Frey**:
  - Added `rh_bowoffrey` to S-tier weapon scrolls (1) and blessed S (1)
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/ragehatred.BowOfFrey.Majestic.yml`

- **Wizardry**:
  - Added Ashlands Spellslinger armor to S-tier armor scrolls:
    - `HelmetSpellslinger_Surtr_TW`, `ArmorSpellSlingerChest_Surtr_TW`, `ArmorSpellslingerLegs_Surtr_TW`
  - Added missing staffs with biome-appropriate tiers:
    - `StaffSurtling_TW` → C-tier weapon scrolls (Swamp)
    - `StaffGolem_TW` → B-tier weapon scrolls (Mountain)
  - File updated: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/Therzie,Wizardry.Majestic.yml`

- **MagicBows**:
  - Added all five elemental bows and crossbows to S-tier weapon scrolls (1) and blessed S (1):
    - Bows: `BMB_FieryBow`, `BMB_FrozenBow`, `BMB_LightningBow`, `BMB_SpiritBow`, `BMB_ToxicBow`
    - Crossbows: `BMB_Crossbow_Fiery`, `BMB_Crossbow_Frozen`, `BMB_Crossbow_Lightning`, `BMB_Crossbow_Spirit`, `BMB_Crossbow_Toxic`
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/blacks7ar.MagicBows.Majestic.yml`

- **ForsakenJVL (RtD)**:
  - Weapons:
    - Meadows: `MeadowsAirWand_RtD`, `MeadowsAirStaff_RtD` → F-tier
    - Black Forest: `BlackForestLightningWand_RtD`, `BlackForestFireStaff_RtD`, `BlackForestLightStaff_RtD` → D-tier
    - Swamp: `SwampPoisonWand_RtD`, `SwampEarthStaff_RtD` → C-tier
    - Mountain: `MountainIceWand_RtD`, `MountainIceStaff_RtD` → B-tier
    - Plains: `PlainsVoidWand_RtD`, `PlainsVoidStaff_RtD` → A-tier
    - Mistlands/Ashlands/Deep North: `MistlandsElementWand_RtD`, `MistlandsQuakeStaff_RtD`, `AshLandsFireWand_RtD`, `AshLandsStaff1_RtD`, `AshLandsStaff2_RtD`, `AshLandsStaff3_RtD`, `DeepNorthArcaneWand_RtD`, `DeepNorthStaff1_RtD`, `DeepNorthStaff2_RtD`, `DeepNorthStaff3_RtD` → S-tier
    - Healing Staffs: T1→D, T2→C, T3→B, T4→A
  - Mage Armor: Black Forest (D), Swamp (C), Mountain (B), Plains (A), Mistlands/Ashlands/Deep North (S) sets (Hood/Chest/Legs + Capes)
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/Digitalroot.ForsakenJVL.Majestic.yml`

- **Warfare**:
  - Weapons: Added missing Swamp item `SledgeBonemass_TW` → C-tier weapon scrolls
  - Armor coverage:
    - Iron (C): Hunter, Rogue, Vigorous
    - Silver (B): Hunter, Rogue, Vigorous, Warrior
    - Black Metal (A): Hunter, Rogue, Vigorous, Warrior, Vidar, Fenrir
    - Carapace/Flametal (S): Hunter, Rogue, Vigorous, Warrior, Vidar, Fenrir, Bold, Legion
    - Leather (F): Leather set
  - File updated: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/Therzie.Warfare.Majestic.yml`

- **Warfare Fire & Ice**:
  - Confirmed comprehensive S-tier coverage for Njord/Surtr weapons, shields, bows/crossbows, staffs, capes, and high-end armors
  - File verified: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/Therzie.WarfareFI.Majestic.yml`

- **BowsBeforeHoes**:
  - Bows (Weapons): `BBH_BlackForest_Bow` → D-tier; `BBH_Seeker_Bow`, `BBH_Surtling_Bow` → S-tier
  - Quivers (Armor): `BBH_BlackForest_Quiver` → D-tier; `BBH_PlainsLox_Quiver` → A-tier; `BBH_Seeker_Quiver`, `BBH_OdinPlus_Quiver` → S-tier
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/Azumatt.BowsBeforeHoes.Majestic.yml`

- **BowPlugin**:
  - Crossbows (Weapons): Flint→F, Bronze→D, Iron→C, Silver→B, BlackMetal→A
  - Bows (Weapons): Bone→D, Silver/BlackMetal→A, Elven/Seeker→S
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/blacks7ar.BowPlugin.Majestic.yml`

- **Southsil Armor** (highest material keyword used per set):
  - F: Neck | D: Chief/Troll/Skog/Bronze/Ancient (+ Boar cape) | C: Swamp/Iron/Ancient Iron | B: Wolf/Silver/Frost | A: Loxhunt/Samurai/Valk/Warlord (+ Serpent cape) | S: Carapace/Ash (+ Storr cape)
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/SouthsilArmor.Majestic.yml`

- **Sages Vault**:
  - Armor: Robes/Tunics/Pants/Hoods → C; Crowns → B. Shields: SageBook01–04 → B. Weapons: Sage staffs + ScholarFireStaff → A; NeedleBlade/DeathBlade → B
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/SagesVault.Majestic.yml`

- **MagicRevamp (BMR_)**:
  - Weapons: Wood→F; Ember/Root→D; Ancient/Crystal/Cursed→C; Elven→A; Flametal→S. Armor/Capes tiered per set progression; Spellbook (utility) → B
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/blacks7ar.MagicRevamp.Majestic.yml`

- **Hugo's Armory**:
  - Weapons tiered by material: Wood/Leather→F; Bronze→D; Iron→C; Silver→B; BlackMetal→A; Obsidian/Flametal→S
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/HugosArmory.Majestic.yml`

- **Shawesome Divine Armaments**:
  - Armor/capes: Mythrill/9b/EOM/ShawFire/ShawFrost→A; Dhakharian/SVandemDraco/Paladin/Slayer→S. Weapons: Divine sledge and DragonSlayer → S
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/Shawesome.DivineArmaments.Majestic.yml`

- **Biome Lords Quests**:
  - Armor: `HelmetDvergerWishboneTG`, `TGCapeFlameFeather` → S. Weapons: `TGStaff_LightningWolf`, `TGWhisper_chainattack` → S
  - File created: `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/BiomeLordsQuests.Majestic.yml`

- **Armory**:
  - Confirmed comprehensive tier coverage in `config/ValheimEnchantmentSystem/AdditionalEnchantmentReqs/Therzie.Armory.Majestic.yml`

#### Enchanting Impact
- Bow of Frey, Wizardry, MagicBows, ForsakenJVL, BowsBeforeHoes, BowPlugin, Warfare, Warfare FI, Southsil Armor, Sages Vault, MagicRevamp (BMR_), Hugo's Armory, Shawesome Divine Armaments, and Biome Lords Quests gear are now compatible with S–F enchantment scrolls
- Tiering matches RelicHeim progression across F/D/C/B/A/S with biome/material alignment
- Seamless with existing RelicHeim configuration; no load-order changes

#### Crafting Station Alignment (Fletcher Table)
- Updated recipes to craft at Fletcher Table (`FletcherTable_TW`):
  - Finewood Bow (`BowFineWood`)
  - Flinthead Arrow (`ArrowFlint`)
  - Torch Arrow (`TorchArrow`)
  - Antler Bolts (`BoltAntler_TW`)
  - Flint Bolt (`BBP_Bolt_Flint`)

#### Crafting Station Alignment (Wizard Table)
- Updated the crafting/repair station to Wizard Table (`$piece_wizardtable_TW`) for:
  - RtDMagic staffs/wands:
    - `MountainIceStaff_RtD`, `MountainIceWand_RtD`
    - `SwampEarthStaff_RtD`, `SwampPoisonWand_RtD`
  - RtDMagic additional mage apparel:
    - `BlackForestMageHood_RtD`, `BlackForestMageLegs_RtD`
    - `SwampMageChest_RtD`, `SwampMageHood_RtD`, `SwampMageLegs_RtD`

  - RtDMagic Mage apparel:
    - `BlackForestMageChest_RtD` (Forest Garment)
    - `MountainMageCape_RtD` (Frostfell Wrap)
    - `MountainMageChest_RtD` (Frostfell Tunic)
    - `MountainMageHood_RtD` (Frostfell Hood)
    - `MountainMageLegs_RtD` (Frostfell Legs)
    - `SwampMageCape_RtD` (Blood Drape)
  - EpicLoot jewelry and Sages Vault crowns:
    - `SilverRing`
    - `SageCrownGold01/02/03`, `SageCrownSilver01/02/03`, `SageCrownObsidian01/02/03`

  - Fire Staff (`BlackForestFireStaff_RtD`)
  - Light Staff (`BlackForestLightStaff_RtD`)
  - Crystal Wand (`BMR_CrystalWand`)
  - Crystal Staff (`BMR_CrystalStaff`)
  - Eir Staff T1 (`HealingStaff_T1_RtD`)
  - Eir Staff T2 (`HealingStaff_T2_RtD`)
  - Eir Staff T3 (`HealingStaff_T3_RtD`)
  - Air Staff (`MeadowsAirStaff_RtD`)
  - Air Wand (`MeadowsAirWand_RtD`)
  - Lightning Staff (`StaffLightning`)
  - Scholar Fire Staff (`ScholarFireStaff`)

*Added README Known Issue and changelog note for quiver-related bow draw blocking and its workaround.*

- Documentation:
  - Known issue: Bow draw can be blocked when using a quiver with no arrows in the main inventory.
  - Workaround: Keep at least one arrow stack in main inventory; quiver selection still applies via the quiver bar.

#### Crafting Station Requirement (Forge Level)
- OdinArchitect: Odin's Hammer (`odin_hammer`) now requires Forge level 5

---
## Version 1.5.7 - Missing Arrow Recipe Implementation & Raid Configuration Adjustment *(Testing)*

*Created WackyDatabase recipe files for all missing vanilla arrow types that were not appearing in the Fletcher Table, ensuring complete arrow crafting availability. Adjusted raid configurations to restore RelicHeim-style raid frequency. Fixed additional missing recipes with incorrect prefab names. Added vanilla trader support for Amber trading at reduced prices.*

#### Missing Arrow Recipes Added
- **Frost Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 2)
  - Materials: 8 Wood, 4 Obsidian, 2 Feathers, 1 FreezeGland
- **Iron Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 2)
  - Materials: 8 Wood, 1 Iron, 2 Feathers
- **Obsidian Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 2)
  - Materials: 8 Wood, 4 Obsidian, 2 Feathers
- **Silver Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 2)
  - Materials: 8 Wood, 1 Silver, 2 Feathers
- **Poison Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 2)
  - Materials: 8 Wood, 4 Obsidian, 2 Feathers, 2 Ooze
- **Needle Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 2)
  - Materials: 4 Needle, 2 Feathers
- **Wood Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 1)
  - Materials: 8 Wood
- **Pickaxe Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 1)
  - Materials: 8 ElderBark, 1 Resin, 1 SurtlingCore, 2 Feathers
- **Bone Arrows**: New WackyDatabase recipe at FletcherTable_TW (Level 1)
  - Materials: 8 Wood, 4 BoneFragments, 2 Feathers

#### Technical Implementation
- **Recipe Files Created**: 7 new WackyDatabase recipe files in `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/`
- **Crafting Station**: All recipes use `FletcherTable_TW` (corrected from `$piece_fletchertable_TW`)
- **Batch Production**: All recipes craft 20 arrows per batch
- **Progression Tiers**: Wood Arrows (Level 1) → All others (Level 2)
- **Material Requirements**: Based on vanilla Valheim recipes from Items.md data

#### Files Created
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowFrost.yml`
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowIron.yml`
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowObsidian.yml`
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowSilver.yml`
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowPoison.yml`
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowNeedle.yml`
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowWood.yml`
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowPickaxe.yml`
- `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaRecipes/Recipe_ArrowBone.yml`
- `config/shudnal.TradersExtended.MWL_Haldor_Trader.buy.json`
- `config/shudnal.TradersExtended.MWL_Hildir_Trader.buy.json`

#### Configuration Changes
- **BowPlugin Iron Crossbow**: Disabled duplicate Iron Crossbow from BowPlugin mod to prevent confusion with RelicHeim's CrossbowIron_TW
- **BowPlugin Silver Crossbow**: Disabled duplicate Silver Crossbow from BowPlugin mod to prevent confusion with RelicHeim's crossbow progression
- **BowPlugin Fletcher Table Integration**: Updated all active bow and crossbow items to use FletcherTable_TW crafting station for consistency with RelicHeim's bow progression system

#### Raid Configuration Adjustments
- **Restored RelicHeim raid frequency**: Changed `EventCheckInterval` from 90 to 60 minutes
- **Increased raid chance**: Changed `EventTriggerChance` from 20% to 35%
- **Maintained DougsLoreRaids**: Kept existing enabled raids (Bog_Uprising, Hunt_of_Moder, Warband_of_Yagluth)
- **Disabled multi-phase raids**: Elder_Rite raids remain disabled to avoid progression mechanics complexity
- **Balanced dangerous enemies**: Reduced spawn rates and increased spawn distances for Wraiths, Hatchlings, and Deathsquitos
- **Files updated**: `config/custom_raids.cfg`, `Dogeheim/Configs/custom_raids.cfg`, and DougsLoreRaids files

#### Impact
- **Complete arrow availability**: All vanilla arrow types now craftable at Fletcher Table
- **Progressive crafting**: Wood → Flint → Iron/Obsidian/Silver → Frost/Poison/Needle
- **Thematic consistency**: All archery equipment and ammunition centralized
- **Enhanced gameplay**: Players can now access full arrow progression system
- **Material balance**: Recipes follow vanilla Valheim material requirements
- **Restored raid intensity**: Raids now occur more frequently (60-minute intervals vs 90-minute)
- **Balanced raid chance**: 35% trigger chance provides moderate challenge without being overwhelming
- **Enhanced lore raids**: DougsLoreRaids provide additional thematic raid content for different biomes
- **Balanced difficulty**: Dangerous enemies (Wraiths, Hatchlings, Deathsquitos) now spawn less frequently and from greater distances

---

## Version 1.5.6 - Fletcher Table Ammunition Centralization *(Testing)*

*Centralized all ammunition crafting to the Fletcher Table for improved thematic consistency and better crafting organization.*

#### Ammunition Moved to Fletcher Table
- **Antler Bolt**: Now crafted at FletcherTable_TW (Workbench → Fletcher Table)
- **Fire Arrow**: New WackyDatabase recipe at FletcherTable_TW (vanilla item)
- **Flinthead Arrow**: New WackyDatabase recipe at FletcherTable_TW (vanilla item)
- **Flint Bolt**: Now crafted at FletcherTable_TW (Workbench → Fletcher Table)
- **Torch Arrow**: Now crafted at FletcherTable_TW (Workbench → Fletcher Table)
- **Bronze Bolt**: Fixed configuration conflict, now properly uses FletcherTable_TW

#### Technical Implementation
- **Vanilla Items**: Created WackyDatabase recipe files for Fire Arrow and Flinthead Arrow
  - `Recipe_ArrowFire_Recipe_FletcherTable.yml`: 8 Wood, 8 Resin, 2 Feathers (Level 2)
  - `Recipe_ArrowFlint_Recipe_FletcherTable.yml`: 8 Wood, 2 Flint, 2 Feathers (Level 1)
- **Modded Items**: Updated existing mod configuration files to use Custom crafting station
- **Crafting Station**: All ammunition now uses `$piece_fletchertable_TW` reference
- **Configuration Conflict Resolution**: Fixed Bronze Bolt conflict between Warfare and BowPlugin mods

#### Files Modified
- `Dogeheim/Configs/Therzie.Warfare.cfg` - Antler Bolt crafting station
- `Dogeheim/Configs/blacks7ar.BowPlugin.cfg` - Flint Bolt and Bronze Bolt crafting stations
- `Dogeheim/Configs/Azumatt.BowsBeforeHoes.cfg` - Torch Arrow crafting station
- `config/Therzie.Warfare.cfg` - Antler Bolt crafting station
- `config/blacks7ar.BowPlugin.cfg` - Flint Bolt and Bronze Bolt crafting stations
- `config/Azumatt.BowsBeforeHoes.cfg` - Torch Arrow crafting station
- `Valheim_Help_Docs/wackyDatabase-BulkYML/Recipes/Recipe_ArrowFire_Recipe_FletcherTable.yml` (new)
- `Valheim_Help_Docs/wackyDatabase-BulkYML/Recipes/Recipe_ArrowFlint_Recipe_FletcherTable.yml` (new)

#### Impact
- **Centralized crafting**: All ammunition now crafted at Fletcher Table
- **Thematic consistency**: Archery equipment and ammunition in one location
- **Improved organization**: Better crafting station distribution
- **Enhanced gameplay**: Streamlined ammunition production workflow

---

## Version 1.5.5 - Quiver Crafting Station Fix *(Testing)*

*Fixed quiver recipes that were incorrectly configured with wrong crafting station internal names, preventing Black Forest and Lox quivers from appearing in the Fletching Table.*

#### Quiver Recipe Fixes
- **Black Forest Quiver**: Fixed crafting station from `FletcherTable_TW` to `$piece_fletchertable_TW`
- **Lox Quiver**: Fixed crafting station from `FletcherTable_TW` to `$piece_fletchertable_TW`
- **OdinPlus Quiver**: Fixed crafting station from `FletcherTable_TW` to `$piece_fletchertable_TW`
- **Seeker Quiver**: Fixed crafting station from `FletcherTable_TW` to `$piece_fletchertable_TW`

#### Technical Details
- **Internal name correction**: All quiver recipes now use proper Fletching Table internal name
- **Consistent configuration**: Updated both main config and Dogeheim config directories
- **Recipe validation**: Ensured all quivers appear in Fletching Table with correct requirements
- **Crafting station levels**: Maintained appropriate progression (Level 1-2 requirements)

#### Impact
- **Complete quiver availability**: All 4 quivers now properly appear in Fletching Table
- **Progressive crafting**: Black Forest (Level 2) → Lox (Level 2) → OdinPlus/Seeker (Level 1)
- **Thematic consistency**: All archery equipment centralized at Fletching Table
- **Enhanced gameplay**: Players can now access full quiver progression system

---

## Version 1.5.4 - EpicMMO Balance Evaluation & Integration Fixes *(Testing)*

*Evaluated EpicMMO scaling parameters for 400% monster HP environment and performed integration fixes. User maintained original 0.3 scaling values for late-game power progression.*

#### Integration Fixes
- **VanillaShip_Integration.json**: Created with correct RelicHeim patch formatting
- **Smart Containers Configuration**: Maintained existing functionality
  - Magic materials already included in valuables group
  - Fuzzy grouping enabled for better item organization

#### Technical Improvements
- **Format consistency**: All patch files follow RelicHeim standards
- **Item validation**: Verified all referenced items exist in wackysDatabase
- **Configuration integrity**: Ensured proper YAML/JSON formatting throughout
- **Mod integration**: Enhanced compatibility between EpicLoot, OdinShipPlus, and Smart Containers

#### Impact
- **Preserved late-game power**: Original scaling maintained for powerful progression feel
- **Improved mod integration**: Seamless crafting station consolidation
- **Enhanced QoL**: Better item organization and sorting
- **Maintained challenge**: 400% monster HP still provides appropriate difficulty curve

---

## Version 1.5.3 - AllTheHeims EpicLoot Integration *(Testing)*

*Seamlessly integrated AllTheHeims mod items into EpicLoot drop system while maintaining RelicHeim's custom rarity names and functionality.*

#### AllTheHeims Items Added to EpicLoot
- **Adventure Backpacks**: 9 tier-appropriate backpacks (Meadows → Mistlands)
  - BackpackMeadows, BackpackBlackForest, BackpackSwamp, BackpackMountains
  - BackpackPlains, BackpackMistlands, CapeIronBackpack, BackpackNecromancy, CapeSilverBackpack
- **BowPlugin Weapons**: 9 crossbows and bows across all progression tiers
  - BBP_BoneBow, BBP_Crossbow_Flint, BBP_Crossbow_Bronze, BBP_Crossbow_Iron
  - BBP_Crossbow_Silver, BBP_SilverBow, BBP_BlackMetalBow, BBP_Crossbow_BlackMetal
  - BBP_ElvenBow, BBP_SeekerBow
- **SouthsilArmor Sets**: 15 armor pieces (Bronze → Carapace progression)
- **HugosArmory Weapons**: 10 battleaxes and greatswords across all tiers

#### EpicLoot Integration Features
- **Proper rarity distributions**: Balanced across Novus/Nexus/Zodiac/Zeta/Relic tiers
- **Haldor gamble system**: All items available with tier-appropriate coin costs (100-9860 coins)
- **Treasure drop integration**: Items spawn in appropriate biome treasure chests
- **RelicHeim compatibility**: Maintains custom rarity names and colors

#### Technical Implementation
- **3 new patch files**: `AllTheHeims_RelicHeim_Integration.json`, `AllTheHeims_AdventureData_RelicHeim.json`, `AllTheHeims_Extended_RelicHeim.json`
- **Localization fixes**: Restored "Convert Items" text and corrected menu descriptions
- **Priority system**: Proper loading order with Priority values (1000-1600)
- **Clean structure**: Removed conflicting AllTheHeims patches, empty directories

#### Bug Fixes
- **Fixed rarity display**: Restored Novus/Nexus/Zodiac/Zeta/Relic names instead of Magic/Rare/Epic/Legendary
- **Fixed menu text**: "Convert Items" instead of "Convert Shards"
- **Fixed augment description**: Corrected token requirement text
- **Fixed rarity colors**: Restored RelicHeim's custom color scheme

---

## Version 1.5.2 - Magic Items Crafting Station Fixes *(Testing)*

*Fixed magic items that were incorrectly configured to use workbench/forge instead of appropriate magic crafting stations for thematic consistency.*

#### Magic Weapons & Staffs - Wizard Table Fixes
- **BMR Crystal Staff**: Fixed from workbench to wizard table
- **BMR Crystal Wand**: Fixed from workbench to wizard table  
- **BMR Cursed Wand**: Fixed from workbench to wizard table
- **BMR Ember Staff**: Fixed from forge to wizard table
- **BMR Flametal Staff**: Fixed from black forge to wizard table
- **BMR Elven Wand**: Fixed from black forge to wizard table
- **BMR Elven Staff**: Fixed from black forge to wizard table
- **BMR Ancient Staff**: Fixed from forge to wizard table
- **BMR Ancient Wand**: Fixed from black forge to wizard table

#### Magic Armor - Arcane Anvil Fixes
- **BMR Crimson Armor Set**: Fixed from workbench to arcane anvil
  - Crimson Chest, Hood, Legs, Cape
- **BMR Polar Wolf Armor Set**: Fixed from workbench to arcane anvil
  - Polar Wolf Chest, Hood, Legs, Cape
- **BMR Seeker Cape**: Fixed from workbench to arcane anvil

#### Technical Details
- **Crafting stations updated**: All magic items now use appropriate stations
  - **Weapons/Staffs**: `$piece_wizardtable_TW` (Wizard Table)
  - **Magic Armor**: `$piece_arcaneanvil_TW` (Arcane Anvil)
- **Repair stations updated**: Items can now be repaired at their crafting stations
- **Requirements preserved**: All original crafting materials and station levels maintained
- **Individual patch files**: Each item has its own patch file for easy maintenance

#### Impact
- **Thematic consistency**: Magic items now crafted where they logically belong
- **Improved gameplay**: Clear separation between regular crafting and magic crafting
- **Better progression**: Magic items require appropriate infrastructure investment
- **Enhanced immersion**: Players must build wizard tables and arcane anvils for magic items

---

## Version 1.5.1 - Missing Dependencies & Jotunn Update *(Testing)*

*Added missing bow-related dependencies and updated Jotunn to latest version for improved compatibility and expanded bow combat options.*

#### Missing Dependencies Added
- **Added 5 missing bow-related mods** to complete the modpack dependency list:
  - `blacks7ar-BowPlugin-1.8.2`: Core bow mechanics and enhancements
  - `Azumatt-BowsBeforeHoes-1.3.11`: Additional bow variants and quivers
  - `blacks7ar-MagicBows-1.1.5`: Magical bow variants with elemental effects
  - `Digitalroot-ForsakenJVL-2.0.40`: Additional content and features
  - `OdinPlus-BowOfFrey-1.0.6`: Specialized bow equipment
- **Manifest updated**: All dependencies now properly listed in `manifest.json`
- **Version bumped**: Updated to version 1.5.1 to reflect dependency additions

#### Jotunn Framework Update
- **Updated ValheimModding-Jotunn** from version 2.26.0 to 2.26.1:
  - **Previous version**: 2.26.0
  - **New version**: 2.26.1
  - **Benefit**: Latest framework version with improved stability and compatibility
  - **Impact**: Better mod integration and reduced potential conflicts

#### Dependency Verification
- **Comprehensive dependency check completed** against provided list
- **All 95 dependencies** now properly included in manifest
- **No missing dependencies** identified in current configuration
- **Version consistency**: All dependencies match specified versions

---

## Version 1.5.0 - EpicLoot Integration & Bow Combat Enhancement *(Testing)*

*Comprehensive EpicLoot integration with AllTheHeims patches for enhanced bow combat, armor variety, and balanced loot distribution.*

#### Bow Velocity & Accuracy Balance Adjustments
- **Reduced global velocity multiplier** from 4 to 3 for better projectile balance:
  - **Previous setting**: `Velocity Multiplier = 4` (excessive projectile speed)
  - **New setting**: `Velocity Multiplier = 3` (recommended balance)
  - **Impact**: More realistic arrow trajectories and improved skill requirement
  - **Benefit**: Better combat balance while maintaining effectiveness
  - **Files updated**: `config/blacks7ar.BowPlugin.cfg`

- **Implemented skill-based bow draw speed scaling** for balanced progression:
  - **Previous settings**: `Draw Speed = 1`, `Bow Draw Speed Factor = 0.6` (too fast, minimal skill impact)
  - **New settings**: `Draw Speed = 2.2`, `Bow Draw Speed Factor = 1.2` (balanced skill progression)
  - **Impact**: Creates meaningful skill progression from 2.5s (skill 0) to 1.36s (skill 100) for bows
  - **Benefit**: New archers face appropriate challenge while skilled archers are significantly rewarded
  - **Crossbow mechanics**: Maintained `Maximum Draw Time = 0` for instant fire with separate reload scaling
  - **Files updated**: `config/blacks7ar.BowPlugin.cfg`

- **Comprehensive crossbow velocity rebalancing** for proper progression:
  - **BlackMetal Crossbow**: 200 → 60 → 200 (end-game power level, restored to maximum)
  - **Silver Crossbow**: 200 → 55 → 175 (high-tier performance, enhanced)
  - **Iron Crossbow**: 200 → 50 → 150 (mid-game progression, improved)
  - **Bronze Crossbow**: 200 → 40 (early-game balance)
  - **Flint Crossbow**: 200 → 30 (starter weapon)
  - **Impact**: Creates proper velocity progression from early to end-game with enhanced mid/late-game performance
  - **Benefit**: Crossbows now feel distinct from bows with improved projectile speed for mid and late-game variants
  - **Files updated**: `config/blacks7ar.BowPlugin.cfg`

- **Magic crossbow velocity standardization** for elemental variants:
  - **All Magic Crossbows**: 200 → 45 (Fiery, Frozen, Lightning, Spirit, Toxic)
  - **Impact**: Consistent performance across all magical crossbow variants
  - **Benefit**: Magic crossbows maintain their special effects while having balanced projectile speed
  - **Files updated**: `config/blacks7ar.MagicBows.cfg`

- **Maintained existing bow velocities** for proper weapon differentiation:
  - **Regular bows**: 35-80 velocity range (faster projectiles, less accurate)
  - **Crossbows**: 30-200 velocity range (slower projectiles, more accurate, with enhanced mid/late-game performance)
  - **Magic bows**: 45-70 velocity range (enhanced performance)
  - **Impact**: Clear distinction between weapon types and progression tiers
  - **Benefit**: Players must choose between speed (bows) and accuracy (crossbows)
  - **Files updated**: `config/blacks7ar.BowPlugin.cfg`

#### EpicLoot AllTheHeims Patches Integration
- **Added comprehensive EpicLoot patches** for enhanced mod integration and loot variety:
  - **BowPlugin Integration**: Added 9 bow variants to EpicLoot gambling and loot tables
    - **Items**: Bone Bow, Crossbows (Flint, Bronze, Iron, Silver, Black Metal), Silver Bow, Black Metal Bow, Elven Bow, Seeker Bow
    - **Tiers**: Distributed across weapon tiers 1-7 with appropriate rarity distributions
    - **Gambling Costs**: 100-3,500 coins based on item power level (properly tier-balanced)
  - **MagicBows Integration**: Added 10 magical bow variants to EpicLoot systems
    - **Items**: Fiery, Frozen, Lightning, Spirit, Toxic variants of bows and crossbows
    - **Tiers**: Placed in weapon tiers 6-7 for end-game progression
    - **Gambling Costs**: 5,964-8,920 coins for high-tier magical weapons
  - **SouthsilArmor Integration**: Added 80+ armor pieces to EpicLoot gambling and loot tables
    - **Items**: Comprehensive armor collection including neck, chief, troll, bronze, swamp, bear, wolf, and high-tier armors
    - **Tiers**: Distributed across all armor tiers with appropriate power scaling
    - **Gambling Costs**: 256-15,998 coins based on armor tier and rarity
  - **HugosArmory Integration**: Added 20+ weapons to EpicLoot systems
    - **Items**: Boar armor, bone weapons, bronze/iron/silver/black metal weapons, great swords, battleaxes, fists, hammers, maces
    - **Tiers**: Placed in weapon tiers 1-5 and armor tier 1
    - **Gambling Costs**: 250-1,500 coins for balanced progression
  - **BowsBeforeHoes Integration**: Added 7 items (4 quivers, 3 bows) to EpicLoot
    - **Items**: Black Forest, Seeker, Plains Lox, Odin Plus quivers and bows
    - **Tiers**: Bows in weapon tiers 3,4,7; quivers in armor tiers 2,5,7
    - **Gambling Costs**: 1,232-13,113 coins for specialized equipment
  - **AdventureBackpacks Integration**: Added 9 backpacks to EpicLoot systems
    - **Items**: Biome-specific backpacks (Meadows, Black Forest, Swamp, Mountains, Plains, Mistlands) plus special variants
    - **Tiers**: Distributed across armor tiers 1-6 for progressive access
    - **Gambling Costs**: 649-6,618 coins for storage convenience
  - **Files updated**: `config/EpicLoot/patches/AllTheHeims/`

#### EpicLoot Material Drop Ratio Rebalancing
- **Changed EpicLoot material drop ratio** from 60% materials to 50/50 balance:
  - **Previous setting**: `Items To Materials Drop Ratio = 0.6` (60% materials, 40% items)
  - **New setting**: `Items To Materials Drop Ratio = 0.5` (50% materials, 50% items)
  - **Impact**: More balanced loot distribution between magic items and crafting materials
  - **Benefit**: Players get more magic items while still maintaining material availability for enchanting
  - **Files updated**: `config/randyknapp.mods.epicloot.cfg`

#### Bow Combat Enhancement
- **Significantly enhanced bow combat variety** through EpicLoot integration:
  - **Base bows**: 9 variants from BowPlugin mod now available as magic items
  - **Magical bows**: 10 elemental variants from MagicBows mod with special effects
  - **Specialized bows**: 3 unique bows from BowsBeforeHoes mod for specific playstyles
  - **Quiver variety**: 4 quiver types providing different bonuses and storage options
  - **Progressive access**: Bows distributed across all weapon tiers for natural progression
  - **Enchantment compatibility**: All bows can receive EpicLoot enchantments for further customization
- **Combat diversity**: Players now have access to 22+ different bow variants with unique properties
- **Gambling system**: All bows available through EpicLoot's gambling system for targeted acquisition

- **Balanced sneak attack multiplier** for improved stealth gameplay:
  - **Previous setting**: `Sneak Attack Multiplier = 1` (no bonus damage)
  - **New setting**: `Sneak Attack Multiplier = 1.3` (30% bonus damage)
  - **Impact**: Provides meaningful but balanced damage bonus for stealth archery
  - **Benefit**: Encourages tactical gameplay while maintaining combat balance
  - **Files updated**: `config/blacks7ar.BowPlugin.cfg`

#### Quiver Crafting Station Centralization
- **Centralized all quiver crafting to Fletching Table** for improved thematic consistency:
  - **Black Forest Quiver**: Changed from `Workbench` to `FletchingTable`
  - **Lox Quiver**: Changed from `Forge` to `FletchingTable`
  - **OdinPlus Quiver**: Changed from `BlackForge` to `FletchingTable`
  - **Seeker Quiver**: Changed from `BlackForge` to `FletchingTable`
  - **Impact**: All quivers now crafted at the dedicated archery crafting station
  - **Benefit**: Logical progression and centralized archery equipment crafting
  - **Files updated**: `config/Azumatt.BowsBeforeHoes.cfg`
- **Added quiver recipes to Wackys database** for proper integration:
  - **Black Forest Quiver**: Level 2 FletchingTable, requires HardAntler + DeerHide
  - **Lox Quiver**: Level 2 FletchingTable, requires FineWood + SerpentScale + LoxPelt
  - **OdinPlus Quiver**: Level 1 FletchingTable, requires Thunderstone + YggdrasilWood + FlametalNew
  - **Seeker Quiver**: Level 1 FletchingTable, requires YggdrasilWood + Carapace + Mandible
  - **Impact**: Quivers now properly integrated into Wackys database with correct crafting requirements
  - **Benefit**: Consistent crafting system and proper progression integration
  - **Files updated**: `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/BowsBeforeHoes/`

- **Optimized critical hit chance** for balanced bow combat progression:
  - **Previous setting**: `Critical Chance = 7` (too low for EpicMMO integration)
  - **New setting**: `Critical Chance = 12` (balanced with EpicMMO progression)
  - **Impact**: Creates meaningful progression path where EpicMMO Specializing skill (max 16% crit) exceeds base bow crit chance
  - **Benefit**: Players start with 12% bow crit chance and can invest in Specializing to reach 16%+ total critical chance
  - **EpicMMO Integration**: Aligns with Specializing skill tree (1% base + 0.2% per point, max 75 points = 16% total)
  - **Gameplay Balance**: 12% = 1 in 8.3 shots, frequent enough to feel rewarding but not overwhelming
  - **Files updated**: `config/blacks7ar.BowPlugin.cfg`

#### EpicLoot Configuration Optimization
- **Maintained existing EpicLoot settings** for optimal balance:
  - **Set Item Drop Chance**: 35% (increased from default 15%)
  - **Global Drop Rate Modifier**: 1.0 (standard drop rates)
  - **Bounty limits**: 6 bounties per player (increased from default 5)
  - **Item gating**: PlayerMustKnowRecipe (prevents overpowered early-game items)
- **Enhanced loot variety**: All mod items now properly integrated into EpicLoot's magic item system
- **Balanced progression**: Items placed in appropriate tiers based on power level and material requirements

#### EpicLoot Patch Balance Corrections
- **Fixed HugosArmory rarity distributions** to match RelicHeim standards:
  - **Tier 1**: Changed from `[38, 50, 8, 4]` to `[92, 4, 2, 1, 0]` (proper Magic/Rare/Epic/Legendary/Mythic distribution)
  - **Tier 2**: Changed from `[38, 50, 8, 4]` to `[80, 11, 5, 3, 0]` (standard RelicHeim progression)
  - **Tier 3**: Changed from `[38, 50, 8, 4]` to `[67, 18, 8, 5, 0]` (balanced mid-game distribution)
  - **Tier 4**: Changed from `[5, 35, 50, 20]` to `[55, 22, 13, 7, 1]` (proper Silver-tier distribution)
  - **Tier 5**: Changed from `[0, 15, 60, 25]` to `[32, 32, 27, 8, 1]` (balanced Black Metal distribution)
- **Standardized gambling costs** across all AllTheHeims patches to match RelicHeim's tier-based pricing:
  - **Tier 1**: 250 coins (Leather/Deer items)
  - **Tier 2**: 1000 coins (Troll items)
  - **Tier 3**: 1500 coins (Bronze items)
  - **Tier 4**: 2000 coins (Iron items)
  - **Tier 5**: 2500 coins (Silver/Wolf items)
  - **Tier 6**: 3000 coins (Black Metal items)
  - **Tier 7**: 3500 coins (High-end items)
  - **Tier 8**: 4000 coins (Ultimate items)
- **Corrected pricing inconsistencies** in BowPlugin, HugosArmory, and SouthsilArmor patches
- **Maintained proper tier placement** for all items based on material requirements and power level
- **Adjusted item weights** to prevent loot table overcrowding:
  - **BowPlugin items**: Reduced weights from 1.0 to 0.5 to balance with existing RelicHeim bows
  - **HugosArmory items**: Reduced weights from 1.0 to 0.5 to prevent weapon proliferation
  - **Impact**: Maintains variety while preventing specific item types from becoming too common
- **Balanced integration**: All patches now work harmoniously with RelicHeim's existing loot tables

#### Patch File Locations
- **Main RelicHeim patches**: `config/EpicLoot/patches/RelicHeimPatches/` (29 patch files)
- **AllTheHeims patches**: `config/EpicLoot/patches/AllTheHeims/` (6 mod directories)
  - BowPlugin, MagicBows, SouthsilArmor, HugosArmory, BowsBeforeHoes, AdventureBackpacks
- **Configuration files**: All patches automatically applied through EpicLoot's patching system

---

## Version 1.4.9 - AzuAreaRepair Integration *(Testing)*

*Added AzuAreaRepair mod to enhance area repair functionalities and improve building maintenance convenience.*

#### AzuAreaRepair Mod Addition
- **Added AzuAreaRepair package** to the modpack dependencies for enhanced building repair capabilities
  - **Mod author**: Azumatt
  - **Version**: 1.1.6
  - **Purpose**: Provides area repair functionality to repair multiple building pieces simultaneously
  - **Benefit**: Significantly improves building maintenance efficiency, especially for large structures
- **Manifest updated**: Added to dependencies list in `manifest.json`
- **Version bumped**: Updated to version 1.4.9 to reflect new dependency addition

---

## Version 1.4.8 - AzuCrafty Boxes Range Enhancement *(Testing)*

*Increased AzuCrafty Boxes container range for improved convenience and reduced need to move between storage containers.*

#### AzuCrafty Boxes Range Improvement
- **Increased container range from 20 to 50 units** for better convenience:
  - **Previous range**: 20 units (limited reach for nearby containers)
  - **New range**: 50 units (significantly improved access to distant containers)
  - **Benefit**: Players can now pull items from containers across larger areas without moving
  - **Use case**: Particularly useful in large bases with multiple storage areas
- **Files updated**:
  - `config/Azumatt.AzuCraftyBoxes.cfg`
  - `Dogeheim/Configs/Azumatt.AzuCraftyBoxes.cfg`

---

## Version 1.4.7 - Trader Menu Overlap Fix *(Testing)*

*Fixed overlapping trader menus caused by TradersExtended GUI positioning conflicts.*

#### Trader Interface Fix
- **Fixed overlapping trader menus**: Resolved visual conflict where two trader interfaces would overlap
  - **Root cause**: TradersExtended mod was using fixed GUI positioning `{"x":200.0,"y":150.0}` that conflicted with base game trader interface
  - **Solution**: Reset GUI position to default `{"x":0.0,"y":0.0}` to allow natural positioning
  - **Files updated**: 
    - `config/shudnal.TradersExtended.cfg`
    - `Dogeheim/Configs/shudnal.TradersExtended.cfg`
- **Impact**: Trader menus now display properly without visual overlap or positioning conflicts

#### TradersExtended Configuration Review
- **Comprehensive review completed** of all TradersExtended settings for potential conflicts
- **Confirmed optimal settings** for compatibility with other UI mods
- **No additional conflicts found** in current configuration

#### Divine Armaments Drop Rate Rebalancing
- **Significantly reduced divine armament drop rates** to maintain proper game balance and progression:
  - **Ultimate divine weapons** (Odin's Spear, Svandëm's Bow, Divine Chest): **0.8-1.0% → 0.2%** (5x rarer)
  - **Fire divine gear** (Shawesome Fire Helm/Chest, Fire Swords): **1.0% → 0.3%** (3x rarer)
  - **Frost divine gear** (Shawesome Frost Helm/Chest/Legs): **1.0% → 0.3%** (3x rarer)
  - **Divine capes** (Fire God Surtur Cape, Frost God Jotnar Cape): **0.8-1.0% → 0.2%** (5x rarer)
- **Added level-gated safety restrictions** to prevent early-game acquisition:
  - **Fader drops**: Require minimum level 3 creatures + player kills only
  - **Deep North/Ashlands drops**: Require minimum level 4 creatures + player kills only
- **Root cause addressed**: Previous 1-4% drop rates were causing game-breaking early acquisition
- **Impact**: Divine armaments now properly rare (1 in 300-500 kills) and limited to appropriate end-game content
- **Files updated**:
  - `config/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.additional_missing_items.Doug.cfg`
  - `config/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.missing_items.Doug.cfg`
  - `Dogeheim/Configs/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.additional_missing_items.Doug.cfg`
  - `Dogeheim/Configs/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.missing_items.Doug.cfg`

---

## Version 1.4.6 - Staff of the Artificer Drop Rebalancing *(Testing)*

*Moved Staff of the Artificer from early-game Abomination to late-game Fader enemies for better loot progression and game balance.*

#### Staff of the Artificer Drop Changes
- **Removed from Abomination**: Disabled Staff of the Artificer drops from Swamp biome Abominations
  - **Previous**: 4% drop chance from early-game enemies
  - **Issue**: Players getting end-game weapons too early in progression
- **Added to Fader**: Staff of the Artificer now drops from Ashlands Fader enemies
  - **New drop chance**: 1% (reduced from 4% for rarity)
  - **Better progression**: Players encounter Faders when they have access to required materials
  - **Appropriate difficulty**: Fader enemies match the item's power level and crafting requirements

#### Loot Progression Improvements
- **Material access**: Players will have Arcanium, HasRefiner_Item, and FlametalNew when they reach Ashlands
- **Skill requirements**: Blacksmithing level 80 requirement aligns with late-game progression
- **Thematic fit**: High-tier magical weapon from Shawesomes_Divine_Armaments mod suits end-game enemies
- **Rarity balance**: 1% drop chance makes it a valuable and rare find

#### Configuration Files Updated
- `config/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.additional_missing_items.Doug.cfg`
- `Dogeheim/Configs/_RelicHeimFiles/Drop,Spawn_That/zz_Doug/drop_that.character_drop.additional_missing_items.Doug.cfg`

---

## Version 1.4.5 - Greydwarf Spawn Rate Rebalancing *(Testing)*

*Reverted greydwarf nest spawn rates to base RelicHeim values for improved game balance and stability.*

#### Greydwarf Nest Spawner Adjustments
- **Restored greydwarf nest spawn rates to base RelicHeim configuration**:
  - `config/_RelicHeimFiles/Drop,Spawn_That/spawn_that.spawnarea_spawners.PilesNests.cfg`:
    - **SpawnInterval**: 25 → 15 seconds (faster spawning, base RelicHeim value)
    - **ConditionMaxCloseCreatures**: 4 → 2 (standard creature limits)
    - **SpawnWeight**: 8 → 5 (standard spawn chance for regular greydwarfs)
- **Applied to both main config and Dogeheim directory** for consistency
- **Impact**: More frequent but balanced greydwarf spawning at nests, matching original RelicHeim experience

#### Spawn Configuration Rationale
- **Faster spawn intervals**: 15-second intervals provide more consistent combat encounters
- **Standard creature limits**: Maximum 2 greydwarfs near nests prevents overwhelming players
- **Balanced spawn weights**: Regular greydwarfs (5) spawn more often than elites (1) and shamans (1)
- **Maintains challenge**: Keeps Black Forest engaging without being overwhelming

---

## Version 1.4.4 - Black Forest Stability & Debugging Improvements *(Testing)*

*Fixed critical Black Forest freezing issues and enhanced debugging capabilities for better troubleshooting.*

#### Black Forest Raid Stability Fixes
- **Disabled problematic Doug's Lore Raids** that were causing Black Forest freezing:
  - `config/_RelicHeimFiles/Raids/custom_raids.supplemental.DougsLoreRaids.cfg`:
    - **Elder_Rite_P1_JH**: Disabled (was causing chained raid conflicts)
    - **Elder_Rite_P2_JH**: Disabled (chained raid with environment conflicts)
- **Root cause identified**: Chained raids with forced environment changes (`DeepForest Mist` → `ThunderStorm`) and high spawn rates (95% per interval) were overwhelming the game's systems
- **Impact**: Should resolve freezing and crashing issues specifically in Black Forest biome

#### Enhanced BepInEx Logging Configuration
- **Enabled comprehensive logging** for better debugging and error tracking:
  - `config/BepInEx.cfg`:
    - **Console Log Levels**: Added `Info` level for detailed console output
    - **Disk Log Levels**: Added `Message, Info` levels for comprehensive log files
    - **Unity Log Listening**: Enabled to catch Unity-specific errors
- **Benefits**: Better visibility into mod conflicts, performance issues, and error tracking

#### Doug's Lore Raids Analysis & Improvements
- **Identified and fixed critical issues** in remaining Doug's Lore raids:
  - **Removed chained raid system**: Eliminated `OnStopStartRaid` to prevent cascading effects
  - **Reduced spawn rates**: All raids reduced from 95% to 65% spawn chance per interval for better balance
  - **Removed forced environments**: Eliminated `ForceEnvironment` settings to prevent conflicts with other mods
  - **Made all raids independent**: Each raid now operates independently without chaining
- **Specific improvements made**:
  - **Bog Uprising raids**: Removed chaining and forced environments, reduced spawn rates
  - **Hunt of Moder raids**: Removed chaining and forced environments, reduced spawn rates  
  - **Warband of Yagluth raids**: Removed chaining and forced environments, reduced spawn rates
  - **Black Forest raids**: Remain disabled due to previous stability issues

#### EpicMMO System Balancing & Quality of Life Improvements
- **Attribute Maximums**: Reduced from 100 to 75 points for all attributes (Strength, Dexterity, Intelligence, Endurance, Vigour, Specializing)
- **Enhanced Bonus Points**: Extended bonus point system to level 120 with improved progression:
  - Levels 5-90: Enhanced bonus points (e.g., level 15: +3, level 20: +4, level 60: +5)
  - Levels 95-120: New bonus points (level 95: +4, level 100: +5, level 120: +7)
- **Improved Drop System**: Enabled drops from non-player kills (`RemoveAllDrops From NonPlayer Kills = false`)
- **Mob Level Display**: Removed mob level UI string for cleaner interface
- **Better Balance**: Attribute caps prevent overpowered characters while maintaining progression

#### Backup Configuration Created
- **Automatic backup** of modified configuration files created in `config/backup_before_debug/`
- **Safe rollback**: Original configurations preserved for easy restoration if needed

---

## Version 1.4.3 - Passive Creature Spawn Balancing *(Testing)*

*Adjusted passive creature spawning rates to improve world balance and reduce resource competition.*

#### Fish Spawning Adjustments
- **Restored fish spawning to base RelicHeim values** for better fishing gameplay:
  - `config/spawn_that.simple.cfg`:
    - **Fish1, Fish2, Fish3**: All multipliers restored to 1.0 (from 0.8/0.7)
    - **SpawnMaxMultiplier**: 0.8 → 1.0 (+25% max fish spawns)
    - **GroupSizeMinMultiplier**: 0.8 → 1.0 (+25% min group size)
    - **GroupSizeMaxMultiplier**: 0.8 → 1.0 (+25% max group size)
    - **SpawnFrequencyMultiplier**: 0.7 → 1.0 (+43% spawn frequency)
- Improves fishing experience by restoring natural fish density while maintaining balance

#### Passive Creature Spawn Analysis
- **Deer and Boar**: Maintained at base RelicHeim values (1.0 multipliers)
- **Neck**: Reduced to 0.8 multipliers for better resource balance
- **Crow, FireFlies, Seagal**: Maintained at base values for natural world feel
- **All other passive creatures**: Using base RelicHeim spawn rates

#### Spawn Configuration Documentation
- **No global spawn reductions found** - all adjustments are creature-specific
- **Fish spawning was previously reduced** but has been restored to improve fishing gameplay
- **Passive creature balance** maintains natural world density while preventing resource oversaturation

---

## Version 1.4.2 - Comprehensive Skill Experience Rebalancing *(Testing)*

*Major skill experience rebalancing to address progression disparities and improve gameplay balance across all skill types.*

#### Sneak Skill Experience Boost
- **Increased sneak skill bonus experience** for better stealth gameplay rewards:
  - `config/org.bepinex.plugins.smartskills.cfg`:
    - `Sneak bonus experience`: 10 → 13 (+30% bonus XP for sneak attacks)
- Encourages more strategic stealth gameplay and rewards successful sneak attacks

#### Enchantment Skill Experience Boost
- **Significantly increased enchantment skill experience gain** to address lagging progression:
  - `config/ValheimEnchantmentSystem/kg.ValheimEnchantmentSystem.cfg`:
    - `Skill gain factor`: 0.55 → 0.8 (+45% XP gain)
- Addresses the difficulty of progressing enchantment skill with limited access to enchantment opportunities

#### Crossbow Skill Experience Boost
- **Increased crossbow skill experience gain** for better ranged combat progression:
  - `config/Therzie.Warfare.cfg`:
    - `skill_99738506 Skill gain factor`: 0.6 → 0.78 (+30% XP gain)
- Improves progression for crossbow users and ranged combat specialists

#### Tenacity Skill Rebalancing
- **Reduced tenacity skill experience gain** but increased effectiveness:
  - `config/org.bepinex.plugins.tenacity.cfg`:
    - `Skill gain factor`: 0.3 → 0.2 (-33% XP gain, slower progression)
    - `Skill effect factor`: 1.2 → 1.35 (+15% effectiveness at higher levels)
- Creates a more meaningful progression curve with stronger rewards at higher skill levels

#### Blacksmithing Skill Experience Adjustment
- **Slightly reduced blacksmithing skill experience gain** to balance common skill usage:
  - `config/org.bepinex.plugins.blacksmithing.cfg`:
    - `Skill Experience Gain Factor`: 0.7 → 0.6 (-14% XP gain)
- Maintains balanced progression for frequently used crafting skill

#### Fishing Skill Experience Enhancements
- **Significantly increased fishing skill rewards** for successful catches:
  - `config/kam1goroshi.BetterFishing.cfg`:
    - `Hook_Exp_Multiplier`: 4.0 → 5.0 (+25% XP while reeling)
    - `Steps_For_Catch`: 12 → 16 (+33% XP bonus on successful catch)
    - `Bonus_Per_Fish_Level`: 0.8 → 1.0 (+25% bonus for star-level fish)
- Rewards successful fishing more generously while maintaining the challenge

#### Missing Skill Configurations
- **Note**: Jump, run, blocking, and alchemy skills were not found in the current configuration files
- These skills may be handled by different mods or may not have separate configuration options
- Further investigation may be needed to locate these skill configurations if they exist

---

## Version 1.4.1 - Skill Experience Balance & Taming Optimization *(Testing)*

*Adjusted skill experience gains and taming mechanics for better progression balance and reduced frustration.*

#### Swimming Skill Experience Boost
- **Increased swimming skill experience gain** to better match moderate usage patterns:
  - `config/org.bepinex.plugins.smartskills.cfg`:
    - `Swimming experience bonus`: 100% → 150% (+50% XP gain)
- Addresses the skill level disparity where swimming lags behind other skills in mid-game progression

#### Ranching Skill Experience & Taming Speed Improvements
- **Significantly increased ranching skill experience gain** for low-usage skill progression:
  - `config/org.bepinex.plugins.ranching.cfg`:
    - `Skill Experience Gain Factor`: 0.6 → 1.2 (+100% XP gain)
- **Improved taming speed** to reduce frustration with long taming times:
  - `config/org.bepinex.plugins.ranching.cfg`:
    - `Taming Factor`: 2.0 → 3.0 (+50% faster taming)
- Addresses the difficulty of progressing ranching skill with limited animal access

#### Cooking Skill Experience Adjustment
- **Slightly reduced cooking skill experience gain** to balance common skill usage:
  - `config/org.bepinex.plugins.cooking.cfg`:
    - `Skill Experience Gain Factor`: 0.6 → 0.5 (-17% XP gain)
- Maintains balanced progression for frequently used cooking skill

---

## Version 1.4.0 - Fine Wood Furniture & Smart Containers *(Testing)*

*Added fine wood furniture building pieces and smart container functionality for enhanced building and storage options.*

#### Fine Wood Build Pieces Integration
- **Added FineWoodBuildPieces mod** for expanded furniture and building options:
  - Enhanced fine wood furniture crafting recipes
  - Additional decorative building pieces
  - Improved aesthetic options for base building
- **Mod**: `blacks7ar-FineWoodBuildPieces-1.1.7`

#### Smart Containers System
- **Added SmarterContainers mod** for improved storage management:
  - Enhanced container functionality and organization
  - Better inventory management features
  - Improved storage capacity and sorting options
- **Mod**: `Roses-SmarterContainers-1.7.0`

#### Food Barrel Recipe Rebalancing
- **Reapplied food barrel crafting cost increases** for better game balance:
  - Increased crafting costs from 10 to 15 items for most barrels
  - OdinsSeedBag increased from 5 to 8 DeerHide
  - Maintains balance while allowing for increased storage capacity
- **Configuration**: `config/gravebear.odinsfoodbarrels.cfg`

---

## Version 1.3.9 - Custom Raids & Enhanced Loot Systems *(Testing)*

*Added lore-accurate custom raids and expanded loot distribution across biomes for improved exploration rewards.*

#### Custom Raids - Doug's Lore Raids
- **Added comprehensive custom raid system** with four two-phase events:
  - `config/_RelicHeimFiles/Raids/custom_raids.supplemental.DougsLoreRaids.cfg`:
    - **Elder Rite**: Black Forest ritual with Greydwarf shamans and elites
    - **Bog Uprising**: Swamp uprising with Draugr, blobs, and wraiths
    - **Hunt of Moder**: Mountain hunt with wolves, Ulv, and dragon hatchlings
    - **Warband of Yagluth**: Plains warband with goblins, shamans, and deathsquitos
- **Progressive difficulty scaling** tied to boss progression:
  - Requires defeating previous bosses to unlock new raid types
  - Two-phase events with escalating intensity
  - Balanced spawn rates (95% chance per interval) for manageable frequency
- **Lore-accurate theming** with appropriate biomes, environments, and creature combinations

#### Enhanced Cartography Table Integration
- **Improved Better Cartography Table configuration**:
  - `config/nbusseneau.BetterCartographyTable.cfg`:
    - Enhanced map sharing functionality for group exploration
    - Public pin sharing for coordinated exploration
    - Optimized modifier key settings for seamless interaction

#### Missing Items & Drop Table Expansions
- **Added missing items to drop tables** across multiple biomes:
  - **Cross-biome loot distribution** for improved exploration rewards
  - **Low-chance rare items** from different biomes in various drop tables
  - **Enhanced boss loot tables** with additional material variety
- **Expanded chest loot tables** for better treasure hunting rewards
- **Improved creature drop configurations** for more diverse loot distribution

#### Drop Table Optimization
- **Enhanced loot variety** across all biomes:
  - Cross-biome material distribution for better crafting progression
  - Rare item chances in appropriate creature/chest drop tables
  - Balanced drop rates to maintain progression without overwhelming players

---

## Version 1.3.8 - Better Cartography & Hugo's Armory Integration

*Added enhanced map sharing functionality and improved exploration skill balance.*

#### Better Cartography Table Integration
- **Added Better Cartography Table mod** for enhanced group map sharing:
  - `config/nbusseneau.BetterCartographyTable.cfg`:
    - `Map exploration sharing mode`: Public (automatic map sharing)
    - `Pin sharing mode`: Public (custom pins shared between group members)
    - `Modifier key`: LeftShift (for interacting with shared pins)
- **Reduced exploration skill experience gain** to compensate:
  - `config/org.bepinex.plugins.exploration.cfg`:
    - `Skill Experience Gain Factor`: 0.48 → 0.35 (-27% reduction), was definitely finding exploration skill to be blown out of proportion

#### Hugo's Armory Drop Configuration Issue
- **Identified missing drop configurations** for Hugo's Armory items
- **Issue**: Hugo's Armory items are not configured in any drop tables
- **Status**: Requires drop table configuration to enable loot drops

---

## Version 1.3.7 - Monster Difficulty Balance & Spawn Optimization Update

*Balanced monster difficulty scaling and optimized creature spawn rates for improved gameplay experience.*

#### Monster Difficulty Rebalancing
- **Reduced creature size scaling** for better visual clarity:
  - `config/org.bepinex.plugins.creaturelevelcontrol.cfg`:
    - `Creature size increase per star`: 14% → 12% (-14% size reduction)
- **Optimized star spawn chances** to reduce overwhelming encounters:
  - **Star spawn rates reduced by 30%** across all world levels:
    - 1-Star: 20% → 14%
    - 2-Star: 15% → 10.5%
    - 3-Star: 10% → 7%
    - 4-Star: 3% → 2.1%
    - 5-Star: 2% → 1.4%
  - **Total starred creatures**: 50% → 35% (more manageable encounters)
- **Increased loot rewards** to compensate for fewer starred creatures:
  - `Chance for additional loot per star`: 50% → 65% (+30% better rewards)
- **Reduced creature affix spawn rates** for more balanced special effects:
  - `Aggressive effect`: 20% → 10% (-50% reduction)
  - `Curious effect`: 5% → 2% (-60% reduction - reduces mining harassment)
  - `Quick effect`: 10% → 7% (-30% reduction)
  - `Regenerating effect`: 10% → 7% (-30% reduction)
  - Other affixes unchanged (Splitting: 5%, Armored: 1%)
- **Increased elemental infusion variety**:
  - `Fire infusion`: 7% → 9% (+29% increase)
  - `Frost infusion`: 7% → 9% (+29% increase)
  - `Poison infusion`: 4% → 6% (+50% increase)
  - `Lightning infusion`: 3% → 5% (+67% increase)
- **Enhanced boss loot rewards**:
  - `Chance for additional loot per star for bosses`: 60% → 70% (+17% increase)

#### EpicLoot Item Drop Optimization
- **Improved item-to-materials ratio** for better gear acquisition:
  - `config/randyknapp.mods.epicloot.cfg`:
    - `Items To Materials Drop Ratio`: 0.8 → 0.6 (-25% materials, +25% items)

#### Creature Sector System Rebalancing
- **Adjusted creature sector progression** for extended biome exploration:
  - `config/org.bepinex.plugins.creaturelevelcontrol.cfg`:
    - `Kills required for bonus levels`: 10, 35, 100 → 50, 150, 300 (5x more generous)
    - `Sector reset timer`: 30 minutes → 45 minutes (50% longer recovery)
- **Benefits**: Takes 5x longer for areas to become difficult, but areas recover to normal difficulty relatively quickly. Perfect balance for extended exploration without permanent difficulty spikes.

#### Swamp Biome Spawn Optimization
- **Reduced swamp creature spawn density by 50%** to address overcrowding:
  - `config/spawn_that.simple.cfg`:
    - `Blob`: All spawn multipliers reduced to 0.5x
    - `BlobElite`: All spawn multipliers reduced to 0.5x
    - `Draugr`: All spawn multipliers reduced to 0.5x
    - `Draugr_Ranged`: All spawn multipliers reduced to 0.5x
    - `Draugr_Elite`: All spawn multipliers reduced to 0.5x
    - `Leech`: All spawn multipliers reduced to 0.5x
    - `Surtling`: All spawn multipliers reduced to 0.5x
    - `Wraith`: All spawn multipliers reduced to 0.5x
    - `Abomination`: All spawn multipliers reduced to 0.5x

**Impact**: More balanced combat encounters with fewer but more rewarding starred creatures. Swamp biome is now less overwhelming while maintaining challenge. Same total loot rewards but concentrated in fewer, more meaningful encounters.

---

## Version 1.3.5 - Skill Tweaks, Gameplay & Progression Update

*Major update combining workbench alignment, skill progression tuning, wool spawn improvements, fishing enhancements, and custom seasonal music.*

#### Workbench Alignment
- Set Wizard Table (`$piece_wizardtable_TW`) as the crafting and repair station for:
  - `StaffVulkarion_TW` (Vulkarion's Rage)
  - `StaffStorm_TW` (Stormcaller)
  - `StaffSkrymir_TW` (Skrymir's Chill)
  - `StaffMistlands_TW` (Tempest Staff)
  - `StaffBlackforest_TW` (Evergrowth Staff)
  - `BMR_WoodenStaff` (Wood Staff)
  - `HelmetPointyHat` (Pointy Hat)
  - `BMR_SorcerersHat` (Shadowleaf Vanguard Hat)
  - `BMR_SorcerersTrousers` (Shadowleaf Vanguard Trousers)
  - `BMR_SorcerersTunic` (Shadowleaf Vanguard Tunic)
  - `ScholarFireStaff`
- Standardized recipe file placement:
  - Staff-related recipes under `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/StaffBurst/`
  - Vanilla/armor recipes under `config/wackysDatabase/Recipes/_RelicHeimWDB2.0/VanillaItems/`
- Moved glazing recipes to the Cauldron (`$piece_cauldron`):
  - `HoneyGlazedMeat`
  - `HoneyGlazedDeer`

#### EpicMMO System - Experience Rate Adjustment
- **Increased global experience gain rate** for smoother progression:
  - `config/WackyMole.EpicMMOSystem.cfg`:
    - `RateExp`: 1.15 → 1.18 (+2.6% XP gain)
- Maintains balanced progression while reducing grind in mid-late game biomes

#### Smoothbrain Skills - Death Experience Loss Removal
- **Removed death experience loss** from utility skills to reduce frustration:
  - `config/org.bepinex.plugins.tenacity.cfg`:
    - `Skill loss`: 6 → 0 (no XP loss on death)
  - `config/org.bepinex.plugins.packhorse.cfg`:
    - `Skill loss`: 3 → 0 (no XP loss on death)
  - `config/org.bepinex.plugins.farming.cfg`:
    - `Skill Experience Loss`: 1 → 0 (no XP loss on death)
- **Adjusted Tenacity skill balance**:
  - `config/org.bepinex.plugins.tenacity.cfg`:
    - `Skill gain factor`: 0.5 → 0.3 (slower XP gain)
    - `Skill effect factor`: 0.7 → 1.2 (stronger effect)
- Reduces frustration from losing utility skill progress while maintaining balanced progression

#### Fishing Skill Progression Tuning
- **Fishing skill XP rewards increased** to better match effort and success:
  - `config/kam1goroshi.BetterFishing.cfg`:
    - `Hook_Exp_Multiplier`: 3.0 → 4.0 (more XP while reeling a hooked fish)
    - `Steps_For_Catch`: 5 → 12 (much larger XP bonus on a successful catch)
    - `Bonus_Per_Fish_Level`: 0.6 → 0.8 (higher bonus for star-level fish)
- No change to empty-reel XP; empty reels remain the low baseline
- Seasonal bonuses remain intact (e.g., Fall `Fishing` raise multiplier via `shudnal.Seasons`)

#### Increased Wool Spawn Rates
- **Increased Sheep_TW spawn rates by 30-50%** for better wool availability:
  - SpawnMaxMultiplier: 1 → 1.5 (50% increase in max spawned sheep)
  - GroupSizeMaxMultiplier: 1.5 → 2 (33% increase in group size)
  - SpawnFrequencyMultiplier: 1.5 → 2 (33% increase in spawn frequency)
- Sheep_TW drops WoolScraps_TW, providing more crafting materials for Therzie.Wizardry items

---

## Version 1.3.4 - Custom Seasonal Music

#### Seasons Mod - Custom Music
- **Added custom music tracks for all four seasons - Currently not working, still trying to debug and figure it out**:
  - **Spring**: 16MB track with 0.9 volume, 4.0s fade-in, non-looping
  - **Summer**: 2.8MB track with 1.0 volume, 3.0s fade-in, non-looping with resume
  - **Fall**: 12MB track with 1.0 volume, 5.0s fade-in, looping
  - **Winter**: 1.1MB track with 0.8 volume, 6.0s fade-in, looping

**Configuration Details**:
- All tracks are enabled with ambient music settings
- Each season has unique volume levels and fade-in times
- Spring and Summer tracks are non-looping for variety
- Fall and Winter tracks loop continuously for atmospheric effect
- Summer track includes resume functionality for seamless transitions

---

## Session 2025-08-18_13-23-39 - 2025-08-20

*Configuration changes that affect gameplay - automatically generated from tracked changes.*

### Summary
- **Modified configurations**: 6
- **New configurations**: 0
- **Removed configurations**: 0

### Configuration Changes by Mod

#### RelicHeim Configuration

**Configuration Changes** in `_RelicHeimFiles\Drop,Spawn_That\drop_that.character_drop.Bosses.cfg`:
  - Changed: Bonemass.3.SetDropOnePerPlayer from False to True
  - Changed: BossAsmodeus_TW.0.SetDropOnePerPlayer from False to True
  - Changed: BossGorr_TW.1.SetDropOnePerPlayer from False to True
  - Changed: BossGorr_TW.2.SetDropOnePerPlayer from False to True
  - Changed: BossStormHerald_TW.3.SetDropOnePerPlayer from False to True

**Configuration Changes** in `_RelicHeimFiles\Drop,Spawn_That\drop_that.character_drop.GoldTrophy.cfg`:
  - Changed: Bonemass.59.SetDropOnePerPlayer from False to True
  - Changed: BossAsmodeus_TW.59.SetDropOnePerPlayer from False to True
  - Changed: BossSvalt_TW.59.SetDropOnePerPlayer from False to True
  - Changed: BossVrykolathas_TW.59.SetDropOnePerPlayer from False to True
  - Changed: Dragon.59.SetDropOnePerPlayer from False to True

**Configuration Changes** in `_RelicHeimFiles\Drop,Spawn_That\drop_that.character_drop.Wizardry.cfg`:
  - Changed: CorruptedDvergerMage_TW.0.ChanceToDrop from 50 to 100

**Configuration Changes** in `_RelicHeimFiles\Drop,Spawn_That\drop_that.drop_table.Chests.cfg`:
  - Removed: TreasureChest_swamp.SetDropChance (was 100)
  - Removed: TreasureChest_swamp.SetDropMax (was 4)
  - Removed: TreasureChest_swamp.SetDropMin (was 2)
  - Removed: TreasureChest_swamp.SetDropOnlyOnce (was True)

#### org

**Configuration Changes** in `org.bepinex.plugins.creaturelevelcontrol.cfg`:
  - Changed: 3 - Loot.Chance for additional loot per star for bosses from 60 to 50
  - Changed: 3 - Loot.Chance for additional loot per star for creatures from 50 to 100
  - Changed: 3 - Loot.Drop multiplier for passive creatures (like Seagulls and Crows) from 2 to 1
  - Changed: 4 - Bosses.Boss size increase per star (percentage) from 7 to 5

#### randyknapp

**Configuration Changes** in `randyknapp.mods.epicloot.cfg`:
  - Changed: Balance.Items To Materials Drop Ratio from 0.8 to 0

---

**Note**: This changelog focuses on configuration changes that affect gameplay. 
Patch file additions, database files, and other non-configuration changes are not included.

*Generated on 2025-08-20 19:18:28 from config snapshots*
*Initial snapshot: 2025-08-18T14:40:52.508697*
*Current snapshot: 2025-08-18T13:23:39.293727*
