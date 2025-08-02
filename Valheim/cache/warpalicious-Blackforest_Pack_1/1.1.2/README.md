![Blackforest Pack 1](https://i.imgur.com/5lKv9F0.png)

# Blackforest Pack 1
This mod adds a 9 new custom locations to the Blackforest biome. All locations were made using vanilla build pieces and designed to fit Valheim lore. In order to encourage exploration, the locations spawn at varying distances from world center. Part of the More World Locations series, see below for more details.

## Features
- Adds 9 new custom locations the Blackforest biome.
- Locations spawn at varying distances from world center, see 'World Rings System' below.
- Configurability: Location spawn quantities, location creatures, location loot. See below for instructions.

## Location Details
See this spreadsheet for all More World Locations data: 
[More World Locations data](https://docs.google.com/spreadsheets/d/e/2PACX-1vSbNSeAwhSzd6uuX9X3rt6AnKgmGGW-A658htUk8yxZUUvMgRVS3LIqnvbh1rb4ofqK49HYn35r_mQE/pubhtml#)

## World Rings System
The Valheim world is a circle with a default radius of 10,500 meters. In order to encourage and maintain exploration, I've defined a set of world rings that all locations in the More World Locations series will use when spawning in a world. Below are the defined world rings...

| Ring # | Start Distance (m) | End Distance (m) |
|--------|---------------------|------------------|
| Ring 1 | 0                   | 500              |
| Ring 2 | 500                 | 2000             |
| Ring 3 | 1500                | 3000             |
| Ring 4 | 2500                | 4000             |
| Ring 5 | 3500                | 6000             |
| Ring 6 | 4500                | 8500             |
| Ring 7 | 5000                | 10500            |

## Instructions
- To add these locations to a non-existing world, no action is required. Ensure the mod is installed and create a new world.
- To add these locations to an existing world, install the mod the [Upgrade World](https://valheim.thunderstore.io/package/JereKuusela/Upgrade_World/). Then load into your existing world and paste this command in console. Note, you must have access to the console either via enabling it via Steam or using a mod.

Command: `locations_add MWL_RuinsArena2, MWL_RuinsCastle1, MWL_RuinsCastle3, MWL_RuinsTower3, MWL_RuinsTower8, MWL_Tavern1, MWL_WoodTower1, MWL_WoodTower2, MWL_WoodTower3 start`

## Custom Creature Spawns 
The creatures and loot are all customizable. Modded creatures and items are supported. To customize, create a new YAML file in the BepinEx configuration folder. If using mod manager, then use the BepinEx config folder in your profile folder. All mods from the More World Locations series will share the same Yaml file so you only need to create it once.

For creatures, each instance of the location will randomly select from the list of creatures in the the file. First, it will pick a random index (an item in the list), then it will increment through the list, assigning creatures to available creature spawners until each creature spawner has a creature. For the best results, scatter higher tier creatures throughout the list. You must use the creature's prefab name and not it's in-game name. See here for a list of vanilla creature prefab names: [Creatures List](https://valheim-modding.github.io/Jotunn/data/prefabs/character-list.html)

Creature file name: `warpalicious.More_World_Locations_CreatureLists.yml`
Creature file structure:
```
BlackforestCreatures1:
  - Skeleton
  - Skeleton
  - Skeleton
  - Skeleton
  - Skeleton_Poison
BlackforestCreatures2:
  - Greydwarf
  - Greydwarf
  - Greydwarf
  - Greydwarf_Elite
  - Greydwarf
  - Greydwarf
  - Greydwarf_Shaman
BlackforestCreatures3:
  - Greydwarf
  - Greydwarf
  - Greydwarf_Elite
  - Greydwarf_Elite
  - Greydwarf
  - Greydwarf
  - Greydwarf_Shaman
```

## Custom Loot Lists
For loot, as of 12/19/24 the loot list format has changed. If you're using an old format it will still work but you can't access the new customization feature. To access new customization feature, please convert to the new format below and ensure you include the verision number at top of file.

The new format works as such: 
1 - Random roll for total loot slots available. Roll number between 1 - 3. There will be between 1 - 3 loot slots.
2 - For each loot slot, weighted-random selection for item from loot list. Randomly select item from list based on weights.
3 - For each item, random roll between stackMin and stackMax for loot stack amount.

Example for BlackforestLoot1 below:
1 - Random roll results in 2 loot slots
2 - Weighted-random selection for slot 1 = Ruby
3 - Weighted-random selection for slot 2 = Amber
4 - Random roll for slot 1 stack size = 2
5 - Random roll for slot 2 stack size = 4
6 - Final loot in chest = 2 Ruby, 4 Amber

Modded items are confirmed to work in the loot list.

Loot file name: `warpalicious.More_World_Locations_LootLists.yml`
Loot file structure:
```
version: 2.0
BlackforestLoot1:
  - item: Amber
    stackMin: 1
    stackMax: 4
    weight: 1.0
  - item: Ruby
    stackMin: 1
    stackMax: 2
    weight: 1.0
  - item: BoneFragments
    stackMin: 2
    stackMax: 4
    weight: 1
  - item: Blueberries
    stackMin: 2
    stackMax: 4
    weight: 1.0
```

## More World Locations
The goal of the More World Locations series is to solve Valheims exploration problem. Valheim has a giant map but relatively few points of interest (POI) to find. Once a player learns that each biome is just a copy of what they've already seen, exploring the rest of the map feels unnecessary. The More World Locations series will fix this problem by adding dozens of handcrafted, unique, and interesting POIs to the Valheim world. I started developing the series in Febuary 2024 and have released the following mods in the series. See my mod author page for most up to date list.
- [Meadows Pack 1](https://thunderstore.io/c/valheim/p/warpalicious/Meadows_Pack_1/)
- [Blackforest Pack 1](https://thunderstore.io/c/valheim/p/warpalicious/Blackforest_Pack_1/)
- [Blackforest Pack 2](https://thunderstore.io/c/valheim/p/warpalicious/Blackforest_Pack_2/)
- [Swamp Pack 1](https://thunderstore.io/c/valheim/p/warpalicious/Swamp_Pack_1/)
- [Mountains Pack 1](https://thunderstore.io/c/valheim/p/warpalicious/Mountains_Pack_1/)
- [Plains Pack 1](https://thunderstore.io/c/valheim/p/warpalicious/Plains_Pack_1/)
- [Mistlands Pack 1](https://thunderstore.io/c/valheim/p/warpalicious/Mistlands_Pack_1/)
- [Adventure Map Pack 1](https://thunderstore.io/c/valheim/p/warpalicious/Adventure_Map_Pack_1/)
- [More World Traders](https://thunderstore.io/c/valheim/p/warpalicious/More_World_Traders/)
- [Underground Ruins](https://thunderstore.io/c/valheim/p/warpalicious/Underground_Ruins/)

## Mod Support & Feeback.
Please feel free to share any any all feedback or ask questions. You can find me on my own modding Discord.
- [Warp Mods Discord](https://discord.gg/KjgZ63VZv5)

## Credit & Thanks
I greatly appreciate all the other mod developers that helped me while buidling the More World Locations series! If you're someone that's interested in making mods, I encourage you to try it out!

All the locations used in this mod were created by Valheim community members. If you're a Valheim builder and have some cool locations to share for a future More World Locations mod, please reach out on Discord!

| Location | Creator |
|--------|---------------------|
| MWL_RuinsArena2 | H1lli               |
| MWL_RuinsCastle1 | H1lli               |
| MWL_RuinsCastle3 | H1lli               |
| MWL_RuinsTower3 | H1lli                |
| MWL_RuinsTower8 | H1lli                |
| MWL_Tavern1 | H1lli                |
| MWL_WoodTower1 | H1lli           |
| MWL_WoodTower2 | H1lli           |
| MWL_WoodTower3 | H1lli           |


## Donations/Tips
I make mods because I enjoy it and want to make Valheim more enjoyable for everyone. If you feel like saying thanks you can tip me here.

| My Ko-fi: | [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/warpalicious) |
|-----------|---------------|

## Source Code
Source code is available on Github.

| Github Repository: | <img height="18" src="https://github.githubassets.com/favicons/favicon-dark.svg"></img><a href="https://github.com/jneb802/MoreWorldLocations_All"> MoreWorldLocations</a> |
|-----------|---------------|
