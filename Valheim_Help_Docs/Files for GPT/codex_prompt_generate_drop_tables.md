You are Codex, my Valheim config engineer. Generate **Drop That** creature drop tables that:
1) Combine each creature’s **existing sensible materials** with the **new items** I’ve mapped to that creature.
2) Prevent loot bloat by strictly following these balance rules:
   - Use **ONE rare-item roll per kill** (the new items group) with **low odds**.
   - Keep a **materials-to-items weight ratio ≈ 8:1** for each creature’s total table.
   - Cap new item drops to **max 1** per kill. No multi-stacks for rare items.
   - Maintain **progression gates**: use world/biome or boss-gate conditions consistent with the item’s tier.
   - Keep total average drops **close to vanilla** for that creature (material stack sizes are okay).

3) Formatting:
   - Output **Drop That** v2 config using the standard **Creature.DropTable** file format (one file per creature).
   - Use separate **DropLists**: `Materials` (common stuff) and `NewItems` (my mapped items).
   - Enable `OnlyOneOfEachDropList=true` for `NewItems` to ensure at most one rare roll.
   - Prefer `ConditionWorldLevel`, `ConditionKilled`,`ConditionGlobalKeys` for tier gating where relevant.
   - Include comments above each entry with a short reason (tier/theme/material link).

4) Safety checks to apply for every creature:
   - If a mapped item’s tier is above the creature’s natural tier, **bump the gate** (e.g., require boss key/world level) or **downgrade the weight** to near-zero (≤0.1).
   - If the creature already drops a conflicting copy of the same item, **keep just one source** (this file wins) and note the consolidation in comments.
   - For deep-endgame items (Tier 6 / Ashlands-DeepNorth), require **late-game gate** (e.g., `globalkey defeated_queen` or Ashlands key).

5) Tiers (guidance):
   - Tier 1 (5–20) Early: Wood/Flint/Bronze, Meadows/BlackForest
   - Tier 2 (23–35) Mid-early: Iron/Root/early Silver, Swamp/Mountains
   - Tier 3 (35–50) Mid: Silver/Obsidian/wolves/cultists
   - Tier 4 (50–70) Late: Black Metal/Mistlands fauna
   - Tier 5 (70–95) Endgame: Tyranium/Thoradus/Njord themes (Deep North)
   - Tier 6 (95+) Ultimate: Ragnorite/Surtr/Ashlands+

6) Example (style guide) — Creature: Greydwarf (Tier 1)
# DropThat.Creature.DropTable.Greydwarf.cfg
[DropTable]
DropSelf=true
OnlyOneOfEachDropList=false  # materials roll can produce multiple lines

[DropList.Materials]
# Early-game forest materials to keep vanilla feel
Item=Resin; Weight=3.0; MinAmount=1; MaxAmount=3
Item=Wood; Weight=2.0; MinAmount=1; MaxAmount=2
Item=Stone; Weight=1.2; MinAmount=0; MaxAmount=2
Item=GreydwarfEye; Weight=1.0; MinAmount=0; MaxAmount=1

[DropList.NewItems]
OnlyOneOfEachDropList=true   # rare roll group
# Mapped rare items for Greydwarf (Tier 1 gate, very low odds)
# (progression-friendly: WL>=1)
Item=ArrowPickaxe_TW; Weight=0.15; ConditionWorldLevel=1; MaxAmount=1
Item=ThrowAxeBronze_TW; Weight=0.10; ConditionWorldLevel=1; MaxAmount=1
Item=SwordFlint_TW; Weight=0.12; ConditionWorldLevel=1; MaxAmount=1

# Materials:Items ≈ 8:1 by cumulative weight (Greydwarf example: 7.2 vs 0.37)

7) Deliverables:
   - One config file per creature named `DropThat.Creature.DropTable.<Creature>.cfg`.
   - Include a short header block in each file summarizing: native tier, gates used, materials:items ratio achieved, estimated avg drops.

INPUT — Monster → New Items mapping (use **all** entries below; omit any items you can’t resolve):

{
  "Abomination": [
    "StaffPoisonBurst_JH",
    "ArmorSpellSlingerChest_Swamp_TW",
    "ArmorSpellslingerLegs_Swamp_TW",
    "CapeSpellslinger_Swamp_TW",
    "HelmetSpellslinger_Swamp_TW",
    "StaffSwamp_TW",
    "Staffbase_Swamp_TW",
    "NTSTAFF"
  ],
  "Arctic Bear": [
    "ArmorHunterChestTyranium_TW",
    "ArmorVidarTyraniumChest_TW",
    "BattlehammerNjord_TW",
    "CapeNorth_TW",
    "DualSwordSkadi_TW",
    "FistNjord_TW",
    "HelmetHunterTyranium_TW",
    "HelmetVidarTyranium_TW",
    "MaceNjord_TW",
    "ShieldNjordBuckler_TW",
    "ShieldNjord_TW",
    "SwordNjord_TW",
    "FrostGodJotnarCape",
    "shawfrostchest",
    "shawfrosthelm",
    "shawfrostlegs"
  ],
  "Arctic Golem": [
    "CapeYmir_TW",
    "PickaxeLokvyr_TW",
    "SledgeNjord_TW"
  ],
  "Arctic Mammoth": [
    "ArmorLegionThoradusChest_TW",
    "AtgeirNjord_TW",
    "HelmetLegionThoradus_TW",
    "ShieldNjordTower_TW",
    "SpearNjord_TW"
  ],
  "Arctic Serpent": [
    "ShieldArcticSerpentscale_TW"
  ],
  "Arctic Wolf": [
    "ArmorFenrirThoradusChest_TW",
    "ArmorRogueTyraniumChest_TW",
    "AxeNjord_TW",
    "CapeFenrir_TW",
    "DualKnifeNjord_TW",
    "FistFenrir_TW",
    "HelmetFenrirThoradus_TW",
    "HelmetRogueTyranium_TW",
    "KnifeNjord_TW",
    "ThrowAxeNjord_TW",
    "MeldursonCape"
  ],
  "Boar": [
    "ArmorChestBoarHTD"
  ],
  "Bonemaw Serpent": [
    "AxeFlametal_TW",
    "FistFlametal_TW"
  ],
  "Cultist": [
    "StaffofHealing2_JH",
    "SledgeSilver_TW",
    "ArmorSpellSlingerChest_Mountain_TW",
    "ArmorSpellslingerLegs_Mountain_TW",
    "CapeSpellslinger_Mountain_TW",
    "HelmetCircletSilver_Elemental_TW",
    "HelmetCircletSilver_Hunter_TW",
    "HelmetCircletSilver_Sneak_TW",
    "HelmetCircletSilver_Stamina_TW",
    "HelmetCircletSilver_TW",
    "HelmetSpellslinger_Mountain_TW",
    "StaffMountain_TW",
    "Staffbase_Mountain_TW",
    "SageHolyStaff"
  ],
  "Deathsquito": [
    "BowBlackmetal_TW"
  ],
  "Dragon Queen": [
    "DragonSlayerSwordHTD",
    "Odins_Dragon_Staff",
    "lagichest",
    "mythrillchest",
    "mythrilllegs"
  ],
  "Draugr": [
    "KnifeIron_TW"
  ],
  "Draugr Elite": [
    "knightchest",
    "BattleaxeIron_TW",
    "ClaymoreIron_TW",
    "DualKnifeIron_TW",
    "FistIron_TW",
    "SledgeIron_TW",
    "ThrowAxeIron_TW",
    "HelmetCircletIron_Elemental_TW",
    "HelmetCircletIron_Hunter_TW",
    "HelmetCircletIron_Sneak_TW",
    "HelmetCircletIron_Stamina_TW",
    "HelmetCircletIron_TW"
  ],
  "Dvergr": [
    "Staffcore_Mistlands_TW"
  ],
  "Fader": [
    "9bchest",
    "spearodingungnir",
    "svandemhidenbow",
    "wschest",
    "PickaxeFader_TW",
    "dhakharianchest",
    "EOMrelicsword",
    "ShawesomeCape"
  ],
  "Fallen Valkyrie": [
    "shawarcaniumshield",
    "BattleaxeFlametal_TW",
    "EOMchest"
  ],
  "Fenring": [
    "TGStaff_LightningWolf",
    "SilverBattleaxeHTD",
    "BattleaxeSilver_TW"
  ],
  "Frost Troll": [
    "CapeTrollBlack_TW",
    "frostmagechest",
    "StaffFrostBurst_JH",
    "CrossbowChitin_TW",
    "DualKnifeChitin_TW",
    "FistChitin_TW",
    "MaceChitin_TW",
    "ShieldChitinBuckler_TW",
    "ShieldChitinTower_TW",
    "ShieldChitin_TW",
    "SwordChitin_TW",
    "SageIceStaff"
  ],
  "Gjall": [
    "BattleaxeDvergr_TW",
    "GreatbowDvergr_TW",
    "ShieldCarapaceTower_TW",
    "SledgeDemolisher_TW",
    "HelmetCircletCarapace_Elemental_TW",
    "HelmetCircletCarapace_Hunter_TW",
    "HelmetCircletCarapace_Sneak_TW",
    "HelmetCircletCarapace_Stamina_TW",
    "HelmetCircletCarapace_TW",
    "StaffMistlands_TW",
    "Staffbase_Mistlands_TW"
  ],
  "Goblin": [
    "DualKnifeBM_TW"
  ],
  "Goblin Brute": [
    "ArmorBoldCarapaceChest_TW",
    "ArmorHunterChestBM_TW",
    "BlackMetalBattleaxeHTD",
    "bpchest",
    "CrossbowBlackmetal_TW",
    "FistBlackmetal_TW",
    "GreatbowBlackmetal_TW",
    "SledgeBlackmetal_TW",
    "ThrowAxeBlackmetal_TW"
  ],
  "Goblin King": [
    "ArmorFenrirBMChest_TW"
  ],
  "Goblin Shaman": [
    "ArmorRogueBMChest_TW",
    "ss_barbchest",
    "StaffLightningBurst_JH",
    "ClaymoreBlackmetal_TW",
    "ArmorSpellSlingerChest_Plains_TW",
    "ArmorSpellslingerLegs_Plains_TW",
    "CapeSpellslinger_Plains_TW",
    "HelmetCircletBM_Elemental_TW",
    "HelmetCircletBM_Hunter_TW",
    "HelmetCircletBM_Sneak_TW",
    "HelmetCircletBM_Stamina_TW",
    "HelmetCircletBM_TW",
    "HelmetSpellslinger_Plains_TW",
    "StaffPlains_TW",
    "Staffbase_Plains_TW",
    "Staffcore_Plains_TW",
    "SageLightningStaff"
  ],
  "Greydwarf": [
    "PlanHammer",
    "PickaxeStone_JH",
    "SkillPotionAxe_JH",
    "ArrowPickaxe_TW",
    "AtgeirFlint_TW",
    "KnifeBronze_TW",
    "MaceFlint_TW",
    "SwordFlint_TW",
    "ThrowAxeBronze_TW",
    "ThrowAxeFlint_TW"
  ],
  "Greydwarf Brute": [
    "ArmorLeatherChest_TW",
    "HelmetDvergerWishboneTG",
    "BronzeBattleaxeHTD",
    "FistBronze_TW",
    "GreatClub_TW",
    "ShieldBronzeBanded_TW",
    "ShieldBronzeTower_TW",
    "SledgeBronze_TW"
  ],
  "Greydwarf Shaman": [
    "BMR_AncientStaff",
    "Odins_Alchemy_Wand",
    "ancientchest",
    "druidchest",
    "StaffBurst_JH",
    "StaffFireBurst_JH",
    "StaffofHealing_JH",
    "ArmorSpellSlingerChest_BlackForest_TW",
    "ArmorSpellslingerLegs_BlackForest_TW",
    "CapeSpellslinger_Blackforest_TW",
    "HelmetCircletBronze_Elemental_TW",
    "HelmetCircletBronze_Hunter_TW",
    "HelmetCircletBronze_Sneak_TW",
    "HelmetCircletBronze_Stamina_TW",
    "HelmetCircletBronze_TW",
    "HelmetSpellslinger_BlackForest_TW",
    "StaffBlackforest_TW",
    "Staffbase_BlackForest_TW"
  ],
  "Grizzly Bear": [
    "ClaymoreSilver_TW"
  ],
  "Growth": [
    "StaffGolem_TW"
  ],
  "Jotunn Bladefist": [
    "BowNjord_TW",
    "ClaymoreNjord_TW"
  ],
  "Jotunn Brute": [
    "BattleaxeCrystalJotunnheim_TW",
    "BattleaxeNjord_TW",
    "DualSpearSvigaFrekk_TW"
  ],
  "Jotunn Juggernaut": [
    "DualAxeKrom_TW"
  ],
  "Jotunn Shaman": [
    "CrossbowNjord_TW",
    "GreatbowNjord_TW",
    "StaffSkrymir_TW"
  ],
  "Lox": [
    "BattleaxeBlackmetal_TW",
    "ShieldBlackmetalBuckler_TW",
    "SpearBlackmetal_TW"
  ],
  "Moder": [
    "Staffcore_Mountain_TW"
  ],
  "Morgen": [
    "SledgeFlametal_TW"
  ],
  "Obsidian Golem": [
    "AtgeirSilver_TW"
  ],
  "Prowler": [
    "SwordScimitar_TW"
  ],
  "Seeker": [
    "BMR_SeekerCape"
  ],
  "Seeker Brute": [
    "ClaymoreDvergr_TW"
  ],
  "Seeker Queen": [
    "valkchest",
    "ArmorSpellSlingerChest_Mistlands_TW",
    "ArmorSpellslingerLegs_Mistlands_TW",
    "CapeSpellslinger_Mistlands_TW",
    "HelmetSpellslinger_Mistlands_TW"
  ],
  "Serpent": [
    "ss_serpentcape"
  ],
  "Sheep": [
    "Staffcore_Swamp_TW"
  ],
  "Skeleton": [
    "chiefchest",
    "ClaymoreBone_TW",
    "DualKnifeBone_TW",
    "SwordBone_TW"
  ],
  "Stone Golem": [
    "BMR_CrystalStaff",
    "skogchest",
    "BattleaxeCrystal_TW",
    "PickaxeSilver_TW",
    "ShieldSilverBuckler_TW"
  ],
  "Surtling": [
    "StaffSurtling_TW",
    "SageFireStaff",
    "ScholarFireStaff"
  ],
  "Surtr Brute": [
    "DhakharShield",
    "ArmorWarriorRagnoriteChest_TW",
    "BattleaxeSurtr_TW",
    "ClaymoreSurtr_TW",
    "HelmetWarriorRagnorite_TW",
    "MaceSurtr_TW",
    "ShieldSurtr_TW"
  ],
  "Surtr Hound": [
    "ArmorBoldFlametalChest_TW",
    "FlametalAxeHTD",
    "shawfirehelm",
    "ss_ashcape",
    "DualKnifeFlametal_TW",
    "ArmorRaiderRagnoriteChest_TW",
    "BowSurtr_TW",
    "CapeSurtr_TW",
    "CrossbowSurtr_TW",
    "DualKnifeSurtr_TW",
    "FistSurtr_TW",
    "HelmetRaiderRagnorite_TW",
    "KnifeSurtr_TW",
    "ShieldSurtrBuckler_TW",
    "SpearSurtr_TW",
    "ThrowAxeSurtr_TW",
    "FireGodSurturCape",
    "shawfirechest",
    "swordochili",
    "swordodweller"
  ],
  "Surtr Imp": [
    "CapeDemon_TW",
    "StaffImpDemon_TW"
  ],
  "Surtr Legionnaire": [
    "shawesomesledge",
    "BattleaxeCrystalMuspelheim_TW",
    "DualHammerRageHatred_TW",
    "ShieldSurtrTower_TW"
  ],
  "Surtr Seer": [
    "ArmorSpellSlingerChest_Surtr_TW",
    "GreatbowSurtr_TW",
    "HelmetSpellslinger_Surtr_TW",
    "StaffVulkarion_TW"
  ],
  "Surtr Warbringer": [
    "BattlehammerSurtr_TW",
    "SledgeSurtr_TW"
  ],
  "The Elder": [
    "Staffcore_BlackForest_TW"
  ],
  "Tick": [
    "AxeDvergr_TW",
    "FistDvergr_TW",
    "MaceDvergr_TW",
    "ThrowAxeDvergr_TW"
  ],
  "Wolf": [
    "TGCapeFlameFeather",
    "BMR_PolarWolfCape",
    "bearchest",
    "AxeSilver_TW",
    "DualKnifeSilver_TW",
    "FistSilver_TW",
    "ThrowAxeSilver_TW"
  ],
  "Wraith": [
    "BMR_CrimsonCape",
    "BMR_SorcerersCape",
    "NecroTechBow",
    "SageDarkStaff"
  ]
}
