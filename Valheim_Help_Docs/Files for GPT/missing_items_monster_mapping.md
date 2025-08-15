# Missing Items to Monster Mapping

This document maps missing items from `missingitems.md` to appropriate monsters based on their power levels, derived from the `Items.md` database.

## Power Level Tiers

Based on the Items.md analysis, items are categorized by their power levels:
- **Tier 1 (5-20)**: Early game items (Wood, Flint, Bronze)
- **Tier 2 (23-35)**: Mid-early game items (Iron, Silver, basic magic)
- **Tier 3 (35-50)**: Mid game items (Silver, Black Metal, advanced magic)
- **Tier 4 (50-70)**: Late game items (Black Metal, Mistlands materials)
- **Tier 5 (70-95)**: End game items (Flametal, Ashlands materials)
- **Tier 6 (95+)**: Ultimate items (Divine materials, boss drops)

## Monster Power Levels

### Tier 1 Monsters (Early Game - 5-20)
- **Greydwarf** (TrophyGreydwarf) - Basic forest enemy
- **Skeleton** (TrophySkeleton) - Swamp basic enemy
- **Boar** (TrophyBoar) - Meadows passive
- **Deer** (TrophyDeer) - Meadows passive
- **Neck** (TrophyNeck) - Water enemy

### Tier 2 Monsters (Mid-Early - 23-35)
- **Greydwarf Brute** (TrophyGreydwarfBrute) - Forest elite
- **Draugr** (TrophyDraugr) - Swamp basic
- **Draugr Elite** (TrophyDraugrElite) - Swamp elite
- **Frost Troll** (TrophyFrostTroll) - Mountain enemy
- **Wolf** (TrophyWolf) - Mountain enemy
- **Stone Golem** (TrophySGolem) - Mountain elite
- **Abomination** (TrophyAbomination) - Swamp elite
- **Surtling** (TrophySurtling) - Ashlands basic

### Tier 3 Monsters (Mid Game - 35-50)
- **Fenring** (TrophyFenring) - Mountain elite
- **Cultist** (TrophyCultist) - Mountain elite
- **Wraith** (TrophyWraith) - Swamp elite
- **Serpent** (TrophySerpent) - Ocean enemy
- **Hatchling** (TrophyHatchling) - Mountain boss minion

### Tier 4 Monsters (Late Game - 50-70)
- **Goblin** (TrophyGoblin) - Plains basic
- **Goblin Brute** (TrophyGoblinBrute) - Plains elite
- **Goblin Shaman** (TrophyGoblinShaman) - Plains elite
- **Lox** (TrophyLox) - Plains passive
- **Deathsquito** (TrophyDeathsquito) - Plains enemy
- **Goblin King** (TrophyGoblinKing) - Plains boss

### Tier 5 Monsters (End Game - 70-95)
- **Seeker** (TrophySeeker) - Mistlands basic
- **Seeker Brute** (TrophySeekerBrute) - Mistlands elite
- **Gjall** (TrophyGjall) - Mistlands elite
- **Dvergr** (TrophyDvergr) - Mistlands neutral
- **Dragon Queen** (TrophyDragonQueen) - Mountain boss
- **Seeker Queen** (TrophySeekerQueen) - Mistlands boss

### Tier 6 Monsters (Ultimate - 95+)
- **Surtr Hound** (TrophySurtrHound) - Ashlands elite
- **Surtr Brute** (TrophySurtrBrute) - Ashlands elite
- **Surtr Legionnaire** (TrophySurtrLegionnaire) - Ashlands elite
- **Surtr Imp** (TrophySurtrImp) - Ashlands basic
- **Surtr Seer** (TrophySurtrSeer) - Ashlands elite
- **Surtr Warbringer** (TrophySurtrWarbringer) - Ashlands elite
- **Arctic Wolf** (TrophyArcticWolf_TW) - Deep North enemy
- **Arctic Bear** (TrophyArcticBear_TW) - Deep North enemy
- **Arctic Mammoth** (TrophyArcticMammoth_TW) - Deep North enemy
- **Arctic Golem** (TrophyArcticGolem_TW) - Deep North elite
- **Jotunn Brute** (TrophyJotunnBrute_TW) - Deep North elite
- **Jotunn Shaman** (TrophyJotunnShaman_TW) - Deep North elite
- **Jotunn Juggernaut** (TrophyJotunnJuggernaut_TW) - Deep North elite
- **Jotunn Bladefist** (TrophyJotunnBladefist_TW) - Deep North elite
- **Gorr** (TrophyGorr_TW) - Deep North boss
- **Fader** (TrophyFader) - Divine realm enemy
- **Fallen Valkyrie** (TrophyFallenValkyrie) - Divine realm enemy
- **Bonemaw Serpent** (TrophyBonemawSerpent) - Ocean elite
- **Charred Melee** (TrophyCharredMelee) - Ashlands elite
- **Morgen** (TrophyMorgen) - Ashlands elite

## Missing Items by Mod and Recommended Monster Drops

### Armory (Tier 2-4 Items)
Most Armory items are mid-tier equipment requiring materials from Tier 2-4 monsters.

**Recommended Monster Drops:**
- **Tier 2 Items**: Greydwarf Brute, Draugr Elite, Frost Troll, Wolf
- **Tier 3 Items**: Fenring, Cultist, Wraith, Serpent
- **Tier 4 Items**: Goblin Brute, Goblin Shaman, Lox, Deathsquito

**Specific Mappings:**
- `ArmorBoldCarapaceChest_TW` → **Goblin Brute** (Tier 4, requires Carapace)
- `ArmorBoldFlametalChest_TW` → **Surtr Hound** (Tier 6, requires Flametal)
- `ArmorFenrirBMChest_TW` → **Goblin King** (Tier 4, requires Black Metal)
- `ArmorHunterChestBM_TW` → **Goblin Brute** (Tier 4, requires Black Metal)
- `ArmorLeatherChest_TW` → **Greydwarf Brute** (Tier 2, requires Leather)
- `ArmorRogueBMChest_TW` → **Goblin Shaman** (Tier 4, requires Black Metal)
- `CapeTrollBlack_TW` → **Frost Troll** (Tier 2, requires Troll Hide)

### BiomeLords (Tier 1-3 Items)
BiomeLords items are generally lower tier with some mid-tier options.

**Recommended Monster Drops:**
- **Tier 1 Items**: Greydwarf, Skeleton, Boar
- **Tier 2 Items**: Greydwarf Brute, Draugr Elite, Wolf
- **Tier 3 Items**: Fenring, Cultist, Stone Golem

**Specific Mappings:**
- `HelmetDvergerWishboneTG` → **Greydwarf Brute** (Tier 2)
- `TGCapeFlameFeather` → **Wolf** (Tier 2, requires Wolf Pelt)
- `TGStaff_LightningWolf` → **Fenring** (Tier 3, requires Wolf Trophy)

### Hugos Armory (Tier 1-4 Items)
Hugos Armory spans from basic to advanced equipment.

**Recommended Monster Drops:**
- **Tier 1 Items**: Boar, Greydwarf, Skeleton
- **Tier 2 Items**: Greydwarf Brute, Draugr Elite, Frost Troll
- **Tier 3 Items**: Fenring, Cultist, Wolf
- **Tier 4 Items**: Goblin Brute, Lox, Deathsquito

**Specific Mappings:**
- `ArmorChestBoarHTD` → **Boar** (Tier 1, requires Boar Trophy)
- `BlackMetalBattleaxeHTD` → **Goblin Brute** (Tier 4, requires Black Metal)
- `BronzeBattleaxeHTD` → **Greydwarf Brute** (Tier 2, requires Bronze)
- `DragonSlayerSwordHTD` → **Dragon Queen** (Tier 5, requires Dragon materials)
- `FlametalAxeHTD` → **Surtr Hound** (Tier 6, requires Flametal)
- `SilverBattleaxeHTD` → **Fenring** (Tier 3, requires Silver)

### MagicRevamp (Tier 1-3 Items)
MagicRevamp focuses on magical equipment and staves.

**Recommended Monster Drops:**
- **Tier 1 Items**: Greydwarf Shaman, Skeleton, Boar
- **Tier 2 Items**: Draugr, Abomination, Wraith
- **Tier 3 Items**: Cultist, Stone Golem, Wolf

**Specific Mappings:**
- `BMR_AncientStaff` → **Greydwarf Shaman** (Tier 1, requires Ancient materials)
- `BMR_CrimsonCape` → **Wraith** (Tier 2, requires Wraith Trophy)
- `BMR_CrystalStaff` → **Stone Golem** (Tier 3, requires Crystal)
- `BMR_PolarWolfCape` → **Wolf** (Tier 2, requires Wolf Trophy)
- `BMR_SeekerCape` → **Seeker** (Tier 5, requires Seeker materials)
- `BMR_SorcerersCape` → **Wraith** (Tier 2, requires Wraith Trophy)

### PlanBuild (Tier 1 Item)
- `PlanHammer` → **Greydwarf** (Tier 1, basic tool)

### PotionsPlus (Tier 1-2 Items)
- `Odins_Alchemy_Wand` → **Greydwarf Shaman** (Tier 1, magical item)
- `Odins_Dragon_Staff` → **Dragon Queen** (Tier 5, requires Dragon materials)

### Shawesomes Divine Armaments (Tier 5-6 Items)
High-tier divine equipment requiring powerful materials.

**Recommended Monster Drops:**
- **Tier 5 Items**: Dragon Queen, Seeker Queen, Gjall
- **Tier 6 Items**: Surtr variants, Fader, Fallen Valkyrie

**Specific Mappings:**
- `9bchest` → **Fader** (Tier 6, divine armor)
- `DhakharShield` → **Surtr Brute** (Tier 6, requires divine materials)
- `shawarcaniumshield` → **Fallen Valkyrie** (Tier 6, requires Arcanium)
- `shawesomesledge` → **Surtr Legionnaire** (Tier 6, requires Arcanium)
- `shawfirehelm` → **Surtr Hound** (Tier 6, requires Thunderstorm materials)
- `spearodingungnir` → **Fader** (Tier 6, divine weapon)
- `svandemhidenbow` → **Fader** (Tier 6, requires divine materials)

### SouthsilArmor (Tier 1-5 Items)
Wide range of armor from basic to advanced.

**Recommended Monster Drops:**
- **Tier 1 Items**: Boar, Deer, Skeleton
- **Tier 2 Items**: Greydwarf Brute, Frost Troll, Draugr Elite
- **Tier 3 Items**: Fenring, Cultist, Wolf
- **Tier 4 Items**: Goblin variants, Lox, Deathsquito
- **Tier 5 Items**: Dragon Queen, Seeker Queen, Gjall

**Specific Mappings:**
- `ancientchest` → **Greydwarf Shaman** (Tier 1, requires Ancient materials)
- `bearchest` → **Wolf** (Tier 2, requires Wolf Pelt)
- `bpchest` → **Goblin Brute** (Tier 4, requires Black Metal)
- `chiefchest` → **Skeleton** (Tier 1, requires Bone materials)
- `druidchest` → **Greydwarf Shaman** (Tier 1, druidic theme)
- `frostmagechest` → **Frost Troll** (Tier 2, frost theme)
- `knightchest` → **Draugr Elite** (Tier 2, knight theme)
- `lagichest` → **Dragon Queen** (Tier 5, requires Dragon materials)
- `skogchest` → **Stone Golem** (Tier 3, requires Crystal)
- `ss_ashcape` → **Surtr Hound** (Tier 6, requires Ashlands materials)
- `ss_barbchest` → **Goblin Shaman** (Tier 4, barbarian theme)
- `ss_serpentcape` → **Serpent** (Tier 3, requires Serpent Scale)
- `valkchest` → **Seeker Queen** (Tier 5, requires Mistlands materials)
- `wschest` → **Fader** (Tier 6, divine armor)

### Valheim Enchantment System (Tier 1 Items)
- All enchantment scrolls → **Greydwarf Shaman** (Tier 1, magical items)

### WackysDatabase (Tier 1-2 Items)
- `PickaxeStone_JH` → **Greydwarf** (Tier 1, basic tool)
- `SkillPotionAxe_JH` → **Greydwarf** (Tier 1, skill potion)
- `StaffBurst_JH` → **Greydwarf Shaman** (Tier 1, magical staff)
- `StaffFireBurst_JH` → **Greydwarf Shaman** (Tier 1, fire magic)
- `StaffFrostBurst_JH` → **Frost Troll** (Tier 2, frost magic)
- `StaffLightningBurst_JH` → **Goblin Shaman** (Tier 4, lightning magic)
- `StaffPoisonBurst_JH` → **Abomination** (Tier 2, poison magic)
- `StaffofHealing_JH` → **Greydwarf Shaman** (Tier 1, healing magic)
- `StaffofHealing2_JH` → **Cultist** (Tier 3, advanced healing)

### Warfare (Tier 1-4 Items)
Comprehensive weapon and armor mod with wide tier range.

**Recommended Monster Drops:**
- **Tier 1 Items**: Greydwarf, Skeleton, Boar
- **Tier 2 Items**: Greydwarf Brute, Draugr Elite, Frost Troll
- **Tier 3 Items**: Fenring, Cultist, Wolf, Stone Golem
- **Tier 4 Items**: Goblin variants, Lox, Deathsquito

**Specific Mappings:**
- `ArrowPickaxe_TW` → **Greydwarf** (Tier 1, basic tool)
- `AtgeirFlint_TW` → **Greydwarf** (Tier 1, requires Flint)
- `AtgeirSilver_TW` → **Obsidian Golem** (Tier 3, requires Silver)
- `AxeDvergr_TW` → **Tick** (Tier 5, requires Dvergr materials)
- `AxeFlametal_TW` → **Bonemaw Serpent** (Tier 6, requires Flametal)
- `AxeSilver_TW` → **Wolf** (Tier 2, requires Silver)
- `BattleaxeBlackmetal_TW` → **Lox** (Tier 4, requires Black Metal)
- `BattleaxeCrystal_TW` → **Stone Golem** (Tier 3, requires Crystal)
- `BattleaxeDvergr_TW` → **Gjall** (Tier 5, requires Dvergr materials)
- `BattleaxeFlametal_TW` → **Fallen Valkyrie** (Tier 6, requires Flametal)
- `BattleaxeIron_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `BattleaxeSilver_TW` → **Fenring** (Tier 3, requires Silver)
- `BowBlackmetal_TW` → **Deathsquito** (Tier 4, requires Black Metal)
- `ClaymoreBlackmetal_TW` → **Goblin Shaman** (Tier 4, requires Black Metal)
- `ClaymoreBone_TW` → **Skeleton** (Tier 1, requires Bone)
- `ClaymoreDvergr_TW` → **Seeker Brute** (Tier 5, requires Dvergr materials)
- `ClaymoreIron_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `ClaymoreSilver_TW` → **Grizzly Bear** (Tier 3, requires Silver)
- `CrossbowBlackmetal_TW` → **Goblin Brute** (Tier 4, requires Black Metal)
- `CrossbowChitin_TW` → **Frost Troll** (Tier 2, requires Chitin)
- `DualKnifeBM_TW` → **Goblin** (Tier 4, requires Black Metal)
- `DualKnifeBone_TW` → **Skeleton** (Tier 1, requires Bone)
- `DualKnifeChitin_TW` → **Frost Troll** (Tier 2, requires Chitin)
- `DualKnifeFlametal_TW` → **Surtr Hound** (Tier 6, requires Flametal)
- `DualKnifeIron_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `DualKnifeSilver_TW` → **Wolf** (Tier 2, requires Silver)
- `FistBlackmetal_TW` → **Goblin Brute** (Tier 4, requires Black Metal)
- `FistBronze_TW` → **Greydwarf Brute** (Tier 2, requires Bronze)
- `FistChitin_TW` → **Frost Troll** (Tier 2, requires Chitin)
- `FistDvergr_TW` → **Tick** (Tier 5, requires Dvergr materials)
- `FistFlametal_TW` → **Bonemaw Serpent** (Tier 6, requires Flametal)
- `FistIron_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `FistSilver_TW` → **Wolf** (Tier 2, requires Silver)
- `GreatClub_TW` → **Greydwarf Brute** (Tier 2, requires Wood)
- `GreatbowBlackmetal_TW` → **Goblin Brute** (Tier 4, requires Black Metal)
- `GreatbowDvergr_TW` → **Gjall** (Tier 5, requires Dvergr materials)
- `KnifeBronze_TW` → **Greydwarf** (Tier 1, requires Bronze)
- `KnifeIron_TW` → **Draugr** (Tier 2, requires Iron)
- `MaceChitin_TW` → **Frost Troll** (Tier 2, requires Chitin)
- `MaceDvergr_TW` → **Tick** (Tier 5, requires Dvergr materials)
- `MaceFlint_TW` → **Greydwarf** (Tier 1, requires Flint)
- `PickaxeFader_TW` → **Fader** (Tier 6, requires divine materials)
- `PickaxeSilver_TW` → **Stone Golem** (Tier 3, requires Silver)
- `ShieldBlackmetalBuckler_TW` → **Lox** (Tier 4, requires Black Metal)
- `ShieldBronzeBanded_TW` → **Greydwarf Brute** (Tier 2, requires Bronze)
- `ShieldBronzeTower_TW` → **Greydwarf Brute** (Tier 2, requires Bronze)
- `ShieldCarapaceTower_TW` → **Gjall** (Tier 5, requires Carapace)
- `ShieldChitinBuckler_TW` → **Frost Troll** (Tier 2, requires Chitin)
- `ShieldChitinTower_TW` → **Frost Troll** (Tier 2, requires Chitin)
- `ShieldChitin_TW` → **Frost Troll** (Tier 2, requires Chitin)
- `ShieldSilverBuckler_TW` → **Stone Golem** (Tier 3, requires Silver)
- `SledgeBlackmetal_TW` → **Goblin Brute** (Tier 4, requires Black Metal)
- `SledgeBronze_TW` → **Greydwarf Brute** (Tier 2, requires Bronze)
- `SledgeDemolisher_TW` → **Gjall** (Tier 5, requires Eitr)
- `SledgeFlametal_TW` → **Morgen** (Tier 6, requires Flametal)
- `SledgeIron_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `SledgeSilver_TW` → **Cultist** (Tier 3, requires Silver)
- `SpearBlackmetal_TW` → **Lox** (Tier 4, requires Black Metal)
- `SwordBone_TW` → **Skeleton** (Tier 1, requires Bone)
- `SwordChitin_TW` → **Frost Troll** (Tier 2, requires Chitin)
- `SwordFlint_TW` → **Greydwarf** (Tier 1, requires Flint)
- `SwordScimitar_TW` → **Prowler** (Tier 4, requires Black Metal)
- `ThrowAxeBlackmetal_TW` → **Goblin Brute** (Tier 4, requires Black Metal)
- `ThrowAxeBronze_TW` → **Greydwarf** (Tier 1, requires Bronze)
- `ThrowAxeDvergr_TW` → **Tick** (Tier 5, requires Dvergr materials)
- `ThrowAxeFlint_TW` → **Greydwarf** (Tier 1, requires Flint)
- `ThrowAxeIron_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `ThrowAxeSilver_TW` → **Wolf** (Tier 2, requires Silver)

### Warfare Fire and Ice (Tier 5-6 Items)
High-tier equipment requiring advanced materials from Deep North and Ashlands.

**Recommended Monster Drops:**
- **Tier 5 Items**: Arctic variants, Jotunn variants
- **Tier 6 Items**: Surtr variants, Gorr

**Specific Mappings:**
- `ArmorFenrirThoradusChest_TW` → **Arctic Wolf** (Tier 6, requires Thoradus)
- `ArmorHunterChestTyranium_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `ArmorLegionThoradusChest_TW` → **Arctic Mammoth** (Tier 6, requires Thoradus)
- `ArmorRaiderRagnoriteChest_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `ArmorRogueTyraniumChest_TW` → **Arctic Wolf** (Tier 6, requires Tyranium)
- `ArmorSpellSlingerChest_Surtr_TW` → **Surtr Seer** (Tier 6, requires Surtr materials)
- `ArmorVidarTyraniumChest_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `ArmorWarriorRagnoriteChest_TW` → **Surtr Brute** (Tier 6, requires Ragnorite)
- `AtgeirNjord_TW` → **Arctic Mammoth** (Tier 6, requires Tyranium)
- `AxeNjord_TW` → **Arctic Wolf** (Tier 6, requires Tyranium)
- `BattleaxeCrystalJotunnheim_TW` → **Jotunn Brute** (Tier 6, requires Jotunnheim Crystal)
- `BattleaxeCrystalMuspelheim_TW` → **Surtr Legionnaire** (Tier 6, requires Muspelheim materials)
- `BattleaxeNjord_TW` → **Jotunn Brute** (Tier 6, requires Tyranium)
- `BattleaxeSurtr_TW` → **Surtr Brute** (Tier 6, requires Ragnorite)
- `BattlehammerNjord_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `BattlehammerSurtr_TW` → **Surtr Warbringer** (Tier 6, requires Ragnorite)
- `BowNjord_TW` → **Jotunn Bladefist** (Tier 6, requires Tyranium)
- `BowSurtr_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `CapeDemon_TW` → **Surtr Imp** (Tier 6, demonic theme)
- `CapeFenrir_TW` → **Arctic Wolf** (Tier 6, wolf theme)
- `CapeNorth_TW` → **Arctic Bear** (Tier 6, northern theme)
- `CapeSurtr_TW` → **Surtr Hound** (Tier 6, fire theme)
- `CapeYmir_TW` → **Arctic Golem** (Tier 6, ice theme)
- `ClaymoreNjord_TW` → **Jotunn Bladefist** (Tier 6, requires Tyranium)
- `ClaymoreSurtr_TW` → **Surtr Brute** (Tier 6, requires Ragnorite)
- `CrossbowNjord_TW` → **Jotunn Shaman** (Tier 6, requires Tyranium)
- `CrossbowSurtr_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `DualAxeKrom_TW` → **Jotunn Juggernaut** (Tier 6, requires Tyranium)
- `DualHammerRageHatred_TW` → **Surtr Legionnaire** (Tier 6, requires Ragnorite)
- `DualKnifeNjord_TW` → **Arctic Wolf** (Tier 6, requires Tyranium)
- `DualKnifeSurtr_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `DualSpearSvigaFrekk_TW` → **Jotunn Brute** (Tier 6, requires Tyranium)
- `DualSwordSkadi_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `FistFenrir_TW` → **Arctic Wolf** (Tier 6, requires Tyranium)
- `FistNjord_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `FistSurtr_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `GreatbowNjord_TW` → **Jotunn Shaman** (Tier 6, requires Tyranium)
- `GreatbowSurtr_TW` → **Surtr Seer** (Tier 6, requires Ragnorite)
- `HelmetFenrirThoradus_TW` → **Arctic Wolf** (Tier 6, requires Thoradus)
- `HelmetHunterTyranium_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `HelmetLegionThoradus_TW` → **Arctic Mammoth** (Tier 6, requires Thoradus)
- `HelmetRaiderRagnorite_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `HelmetRogueTyranium_TW` → **Arctic Wolf** (Tier 6, requires Tyranium)
- `HelmetSpellslinger_Surtr_TW` → **Surtr Seer** (Tier 6, requires Surtr materials)
- `HelmetVidarTyranium_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `HelmetWarriorRagnorite_TW` → **Surtr Brute** (Tier 6, requires Ragnorite)
- `KnifeNjord_TW` → **Arctic Wolf** (Tier 6, requires Tyranium)
- `KnifeSurtr_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `MaceNjord_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `MaceSurtr_TW` → **Surtr Brute** (Tier 6, requires Ragnorite)
- `PickaxeLokvyr_TW` → **Arctic Golem** (Tier 6, requires Lokvyr)
- `ShieldArcticSerpentscale_TW` → **Arctic Serpent** (Tier 6, requires Arctic Serpent Scale)
- `ShieldNjordBuckler_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `ShieldNjordTower_TW` → **Arctic Mammoth** (Tier 6, requires Tyranium)
- `ShieldNjord_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `ShieldSurtrBuckler_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `ShieldSurtrTower_TW` → **Surtr Legionnaire** (Tier 6, requires Ragnorite)
- `ShieldSurtr_TW` → **Surtr Brute** (Tier 6, requires Ragnorite)
- `SledgeNjord_TW` → **Arctic Golem** (Tier 6, requires Tyranium)
- `SledgeSurtr_TW` → **Surtr Warbringer** (Tier 6, requires Ragnorite)
- `SpearNjord_TW` → **Arctic Mammoth** (Tier 6, requires Tyranium)
- `SpearSurtr_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)
- `StaffImpDemon_TW` → **Surtr Imp** (Tier 6, demonic magic)
- `StaffSkrymir_TW` → **Jotunn Shaman** (Tier 6, requires Tyranium)
- `StaffVulkarion_TW` → **Surtr Seer** (Tier 6, requires Ragnorite)
- `SwordNjord_TW` → **Arctic Bear** (Tier 6, requires Tyranium)
- `ThrowAxeNjord_TW` → **Arctic Wolf** (Tier 6, requires Tyranium)
- `ThrowAxeSurtr_TW` → **Surtr Hound** (Tier 6, requires Ragnorite)

### Wizardry (Tier 1-5 Items)
Magical equipment spanning from basic to advanced tiers.

**Recommended Monster Drops:**
- **Tier 1 Items**: Greydwarf Shaman, Skeleton, Boar
- **Tier 2 Items**: Draugr, Abomination, Wraith
- **Tier 3 Items**: Cultist, Stone Golem, Wolf
- **Tier 4 Items**: Goblin Shaman, Lox, Deathsquito
- **Tier 5 Items**: Seeker Queen, Gjall, Dvergr

**Specific Mappings:**
- `ArmorSpellSlingerChest_BlackForest_TW` → **Greydwarf Shaman** (Tier 1, Black Forest theme)
- `ArmorSpellSlingerChest_Mistlands_TW` → **Seeker Queen** (Tier 5, Mistlands theme)
- `ArmorSpellSlingerChest_Mountain_TW` → **Cultist** (Tier 3, Mountain theme)
- `ArmorSpellSlingerChest_Plains_TW` → **Goblin Shaman** (Tier 4, Plains theme)
- `ArmorSpellSlingerChest_Swamp_TW` → **Abomination** (Tier 2, Swamp theme)
- `ArmorSpellslingerLegs_BlackForest_TW` → **Greydwarf Shaman** (Tier 1, Black Forest theme)
- `ArmorSpellslingerLegs_Mistlands_TW` → **Seeker Queen** (Tier 5, Mistlands theme)
- `ArmorSpellslingerLegs_Mountain_TW` → **Cultist** (Tier 3, Mountain theme)
- `ArmorSpellslingerLegs_Plains_TW` → **Goblin Shaman** (Tier 4, Plains theme)
- `ArmorSpellslingerLegs_Swamp_TW` → **Abomination** (Tier 2, Swamp theme)
- `CapeSpellslinger_Blackforest_TW` → **Greydwarf Shaman** (Tier 1, Black Forest theme)
- `CapeSpellslinger_Mistlands_TW` → **Seeker Queen** (Tier 5, Mistlands theme)
- `CapeSpellslinger_Mountain_TW` → **Cultist** (Tier 3, Mountain theme)
- `CapeSpellslinger_Plains_TW` → **Goblin Shaman** (Tier 4, Plains theme)
- `CapeSpellslinger_Swamp_TW` → **Abomination** (Tier 2, Swamp theme)
- `HelmetCircletBM_Elemental_TW` → **Goblin Shaman** (Tier 4, requires Black Metal)
- `HelmetCircletBM_Hunter_TW` → **Goblin Shaman** (Tier 4, requires Black Metal)
- `HelmetCircletBM_Sneak_TW` → **Goblin Shaman** (Tier 4, requires Black Metal)
- `HelmetCircletBM_Stamina_TW` → **Goblin Shaman** (Tier 4, requires Black Metal)
- `HelmetCircletBM_TW` → **Goblin Shaman** (Tier 4, requires Black Metal)
- `HelmetCircletBronze_Elemental_TW` → **Greydwarf Shaman** (Tier 1, requires Bronze)
- `HelmetCircletBronze_Hunter_TW` → **Greydwarf Shaman** (Tier 1, requires Bronze)
- `HelmetCircletBronze_Sneak_TW` → **Greydwarf Shaman** (Tier 1, requires Bronze)
- `HelmetCircletBronze_Stamina_TW` → **Greydwarf Shaman** (Tier 1, requires Bronze)
- `HelmetCircletBronze_TW` → **Greydwarf Shaman** (Tier 1, requires Bronze)
- `HelmetCircletCarapace_Elemental_TW` → **Gjall** (Tier 5, requires Carapace)
- `HelmetCircletCarapace_Hunter_TW` → **Gjall** (Tier 5, requires Carapace)
- `HelmetCircletCarapace_Sneak_TW` → **Gjall** (Tier 5, requires Carapace)
- `HelmetCircletCarapace_Stamina_TW` → **Gjall** (Tier 5, requires Carapace)
- `HelmetCircletCarapace_TW` → **Gjall** (Tier 5, requires Carapace)
- `HelmetCircletIron_Elemental_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `HelmetCircletIron_Hunter_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `HelmetCircletIron_Sneak_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `HelmetCircletIron_Stamina_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `HelmetCircletIron_TW` → **Draugr Elite** (Tier 2, requires Iron)
- `HelmetCircletSilver_Elemental_TW` → **Cultist** (Tier 3, requires Silver)
- `HelmetCircletSilver_Hunter_TW` → **Cultist** (Tier 3, requires Silver)
- `HelmetCircletSilver_Sneak_TW` → **Cultist** (Tier 3, requires Silver)
- `HelmetCircletSilver_Stamina_TW` → **Cultist** (Tier 3, requires Silver)
- `HelmetCircletSilver_TW` → **Cultist** (Tier 3, requires Silver)
- `HelmetSpellslinger_BlackForest_TW` → **Greydwarf Shaman** (Tier 1, Black Forest theme)
- `HelmetSpellslinger_Mistlands_TW` → **Seeker Queen** (Tier 5, Mistlands theme)
- `HelmetSpellslinger_Mountain_TW` → **Cultist** (Tier 3, Mountain theme)
- `HelmetSpellslinger_Plains_TW` → **Goblin Shaman** (Tier 4, Plains theme)
- `HelmetSpellslinger_Swamp_TW` → **Abomination** (Tier 2, Swamp theme)
- `StaffBlackforest_TW` → **Greydwarf Shaman** (Tier 1, Black Forest theme)
- `StaffGolem_TW` → **Growth** (Tier 4, requires Tar)
- `StaffMistlands_TW` → **Gjall** (Tier 5, Mistlands theme)
- `StaffMountain_TW` → **Cultist** (Tier 3, Mountain theme)
- `StaffPlains_TW` → **Goblin Shaman** (Tier 4, Plains theme)
- `StaffSurtling_TW` → **Surtling** (Tier 2, fire theme)
- `StaffSwamp_TW` → **Abomination** (Tier 2, Swamp theme)
- `Staffbase_BlackForest_TW` → **Greydwarf Shaman** (Tier 1, Black Forest theme)
- `Staffbase_Mistlands_TW` → **Gjall** (Tier 5, Mistlands theme)
- `Staffbase_Mountain_TW` → **Cultist** (Tier 3, Mountain theme)
- `Staffbase_Plains_TW` → **Goblin Shaman** (Tier 4, Plains theme)
- `Staffbase_Swamp_TW` → **Abomination** (Tier 2, Swamp theme)
- `Staffcore_BlackForest_TW` → **The Elder** (Tier 2, requires Elder Shard)
- `Staffcore_Mistlands_TW` → **Dvergr** (Tier 5, requires Queen Shard)
- `Staffcore_Mountain_TW` → **Moder** (Tier 3, requires Moder Shard)
- `Staffcore_Plains_TW` → **Goblin Shaman** (Tier 4, requires Yagluth Shard)
- `Staffcore_Swamp_TW` → **Sheep** (Tier 2, requires Bonemass Shard)

### Miscellaneous Items
Items whose mod names could not be parsed, but can be mapped based on materials:

- `dhakharianchest` → **Fader** (Tier 6, divine armor)
- `EOMchest` → **Fallen Valkyrie** (Tier 6, divine armor)
- `EOMrelicsword` → **Fader** (Tier 6, divine weapon)
- `FireGodSurturCape` → **Surtr Hound** (Tier 6, fire god theme)
- `FrostGodJotnarCape` → **Arctic Bear** (Tier 6, frost god theme)
- `MeldursonCape` → **Arctic Wolf** (Tier 6, northern theme)
- `mythrillchest` → **Dragon Queen** (Tier 5, requires Dragon materials)
- `mythrilllegs` → **Dragon Queen** (Tier 5, requires Dragon materials)
- `NecroTechBow` → **Wraith** (Tier 2, necromantic theme)
- `NTSTAFF` → **Abomination** (Tier 2, necromantic theme)
- `SageDarkStaff` → **Wraith** (Tier 2, dark magic)
- `SageFireStaff` → **Surtling** (Tier 2, fire magic)
- `SageHolyStaff` → **Cultist** (Tier 3, holy magic)
- `SageIceStaff` → **Frost Troll** (Tier 2, ice magic)
- `SageLightningStaff` → **Goblin Shaman** (Tier 4, lightning magic)
- `ScholarFireStaff` → **Surtling** (Tier 2, fire magic)
- `ShawesomeCape` → **Fader** (Tier 6, divine cape)
- `shawfirechest` → **Surtr Hound** (Tier 6, fire theme)
- `shawfrostchest` → **Arctic Bear** (Tier 6, frost theme)
- `shawfrosthelm` → **Arctic Bear** (Tier 6, frost theme)
- `shawfrostlegs` → **Arctic Bear** (Tier 6, frost theme)
- `swordochili` → **Surtr Hound** (Tier 6, requires Flametal)
- `swordodweller` → **Surtr Hound** (Tier 6, requires Flametal)

## Summary

This mapping provides a comprehensive guide for assigning missing items to appropriate monster drops based on:

1. **Material Requirements**: Items requiring specific materials are mapped to monsters that drop or are associated with those materials
2. **Power Level Matching**: Items are matched to monsters of appropriate difficulty tiers
3. **Thematic Consistency**: Items with specific themes (fire, frost, divine, etc.) are mapped to thematically appropriate monsters
4. **Progression Balance**: Lower tier items are assigned to early-game monsters, while high-tier items go to end-game enemies

This ensures a balanced loot progression system that maintains game difficulty while providing appropriate rewards for defeating monsters of various power levels.
