
## Description

This is a **Modpack Resource**. Adds 8 Mushroom Monsters and Spores along with 2 bosses, 2 boss Altars, 2 boss Runestones and 2 boss Vegvisirs.


## Usage

- No monsters or spores have world spawns, you will need to either set them up via code or use a 3rd party mod.
- All 6 locations are disabled by default. You can enable them in the config file for new worlds or to use a 3rd party mod.
- If all 6 locations are enabled and added to the map, you will have all you need to summon the bosses, as the Vegvisir and Runestone locations have 2 defenders that can drop the summoning items.


## Brief Overview

- Bosses are designed as group encounters (3-5+).
- There is one monster for each Biome. All have basic attacks and an anti melee AoE ability.
- There are spores for most Biomes, they do not move, have a ranged attack and are de-spawned if you leave the zone.


## Spawn That Usage

Open spawn_that.world_spawners_advanced.cfg located in your BepInEx\Config folder and add an entry similar to this, or you can do 1 for each monster and just increase the number by 1 each time. 666, 667 etc. You can find more in depth tutorials on the Spawn That Github Wiki.

	[WorldSpawner.666]
	Name = Nom Nom
	PrefabName = MushroomMeadows_MP
	Biomes = Meadows
	Enabled = true
	MaxSpawned = 2
	SpawnInterval = 300
	SpawnChance = 25
	ConditionDistanceToCenterMin = 500


## Donations

<a href="https://www.buymeacoffee.com/horemvore"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=horemvore&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


## Prefab Names

**Bosses**

- MushroomBossDN_MP
- MushroomBossSwamp_MP

**Summoning Items**

- ThistleCap_MP (Swamp)
- IceCap_MP (Deep North)

**Items that can be used in Recipes**

- NonNonFungus_MP
- MonMonFungus_MP
- UnedibleMushroom_MP

**Trophies**

- GoldNonNonStatue_MP
- GoldMonMonStatue_MP
- SilverNonNonStatue_MP
- SilverMonMonStatue_MP

**Monsters**

- MushroomAshLands_MP
- MushroomDeepNorth_MP (Drops Summoning item for Deep North boss, 15% chance)
- MushroomForest_MP (Drops Summoning item for Swamp boss, 7.5% chance)
- MushroomMeadows_MP
- MushroomMistlands_MP
- MushroomMountain_MP (Drops Summoning item for Deep North boss, 7.5% chance)
- MushroomPlains_MP
- MushroomSwamp_MP (Drops Summoning item for Swamp boss, 15% chance)

**Spores**

- SporeForest_MP
- SporeMistland_MP
- SporeMountain_MP
- SporeNorth_MP
- SporePlains_MP
- SporeSwamp_MP

**Summons**

- MushroomSporeJack_MP (Swamp)
- MushroomSummonSpore_MP (Deep North)
- MushroomSummonSporeling_MP (Deep North)

**Location Names**

- Loc_FungusGrove_MP (Deep North)
- Loc_MushroomGrove_MP (Swamp)
- Loc_Vegvisr_MonMon_MP (Black Forest)
- Loc_Vegvisr_NonNon_MP (Mountain)
- Loc_Runestone_MonMon_MP (Deep North)
- Loc_Runestone_NonNon_MP (Swamp)


## Patch Notes

**1.0.2**

	Added SFX to the SFX mixer instead of the generic Ambient mixer.
	
**1.0.1**

	Fixed Localization of Inedible Fungus
	Fixed Moder event starting upon boss summons

**1.0.0**

- Initial Release